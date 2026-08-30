"""tools/deliver.sh — a pull's words reach the model and the answer comes back.

The half `card:session-program.md` named (the road, brick 1): until this,
`pull` recorded the words and nothing carried them.  The node's real port
is not reachable from inside the fence (--unshare-net), so the model is a
stub HTTP server on the test's own loopback; what is exercised is the
delivery — read the unanswered questions, ask, write the replies, and do
not ask twice.
"""
import http.server
import json
import subprocess
import threading
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
DELIVER = ROOT / "tools" / "deliver.sh"
NODE = ROOT / "llm"


BODIES = []   # every request the stub answered, for the tests that read what was sent


class _Stub(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def do_GET(self):
        self.send_response(200); self.end_headers(); self.wfile.write(b"ok")

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        BODIES.append(body)
        asked = body["messages"][-1]["content"]
        out = {"choices": [{"message": {"role": "assistant", "content": f"echo<{asked}>"}}]}
        self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers()
        self.wfile.write(json.dumps(out).encode())


@pytest.fixture
def stub():
    srv = http.server.HTTPServer(("127.0.0.1", 0), _Stub)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{srv.server_address[1]}"
    yield {"TEND_LLM_URL": base + "/v1/chat/completions", "TEND_LLM_HEALTH": base + "/health"}
    srv.shutdown()


def deliver(node, *args, state, stub, **extra):
    env = {"PATH": "/usr/bin:/bin", "TEND_STATE_DIR": str(state), **stub, **extra}
    return subprocess.run(["sh", str(DELIVER), str(node), *args], capture_output=True, text=True, env=env)


def test_it_answers_the_unanswered_questions_and_skips_a_wordless_line(tmp_path, stub):
    st = tmp_path / "st"; st.mkdir()
    (st / "pull").write_text("100 how do I brew tea\n200\n300 second question\n")
    (st / "delivered").write_text("0")
    r = deliver(NODE, state=st, stub=stub)
    assert r.returncode == 0, r.stdout + r.stderr
    replies = (st / "replies").read_text()
    assert "Q: how do I brew tea" in replies and "A: echo<how do I brew tea>" in replies
    assert "Q: second question" in replies and "echo<second question>" in replies
    assert "200" not in replies, "a line with no words is not an ask"
    assert (st / "delivered").read_text().strip() == "3"


def test_it_does_not_answer_twice(tmp_path, stub):
    st = tmp_path / "st"; st.mkdir()
    (st / "pull").write_text("100 only question\n")
    (st / "delivered").write_text("0")
    deliver(NODE, state=st, stub=stub)
    first = (st / "replies").read_text()
    r = deliver(NODE, state=st, stub=stub)
    assert "nothing new" in r.stdout
    assert (st / "replies").read_text() == first, "a delivered question is not delivered again"


def test_first_run_with_no_marker_arms_and_delivers_nothing(tmp_path, stub):
    st = tmp_path / "st"; st.mkdir()
    (st / "pull").write_text("100 a backlog question\n")
    r = deliver(NODE, state=st, stub=stub)
    assert r.returncode == 0 and "armed at 1 lines" in r.stdout
    assert not (st / "replies").exists(), "arming answers no backlog"
    assert (st / "delivered").read_text().strip() == "1"


def test_a_question_argument_is_recorded_and_answered(tmp_path, stub):
    st = tmp_path / "st"; st.mkdir()
    r = deliver(NODE, "what is jidoka", state=st, stub=stub, TEND_NO_START="1")
    assert r.returncode == 0, r.stdout + r.stderr
    assert "what is jidoka" in (st / "pull").read_text(), "the ask is recorded in the pull file"
    assert "A: echo<what is jidoka>" in (st / "replies").read_text()


def test_inside_the_fence_it_records_and_does_not_deliver(tmp_path, stub):
    st = tmp_path / "st"; st.mkdir()
    r = deliver(NODE, "a fenced ask", state=st, stub=stub, TEND_FENCED="1")
    assert r.returncode == 0 and "the runner's side delivers it" in r.stderr
    assert "a fenced ask" in (st / "pull").read_text()
    assert not (st / "replies").exists()


def test_the_conversation_rides_along_as_history(tmp_path, stub):
    """tools/panel.py's talk, 2026-08-30: TEND_HISTORY is the exchanges so
    far, prepended to the ask; unset is cold, as a pull line always was;
    not an array is refused before anything is asked."""
    st = tmp_path / "s"; st.mkdir()
    hist = [{"role": "user", "content": "one"}, {"role": "assistant", "content": "echo<one>"}]
    r = deliver(NODE, "two", state=st, stub=stub, TEND_NO_START="1", TEND_HISTORY=json.dumps(hist))
    assert r.returncode == 0, r.stderr
    assert BODIES[-1]["messages"] == hist + [{"role": "user", "content": "two"}]
    r = deliver(NODE, "cold", state=st, stub=stub, TEND_NO_START="1")
    assert r.returncode == 0 and BODIES[-1]["messages"] == [{"role": "user", "content": "cold"}]
    n = len(BODIES)
    r = deliver(NODE, "three", state=st, stub=stub, TEND_NO_START="1", TEND_HISTORY="not json")
    assert r.returncode == 2 and "TEND_HISTORY" in r.stderr and len(BODIES) == n
