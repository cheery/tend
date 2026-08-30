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
HEADS = []    # the Authorization header of each, or None


PAUSE = 0.4   # between the two halves of a streamed answer: long enough for a reader to see the first


class _Stub(http.server.BaseHTTPRequestHandler):
    """A model at a port that streams, as llama-server does: one SSE line per
    delta, the reasoning first when thinking was asked for, the answer in
    two halves with a pause between, then [DONE]."""
    def log_message(self, *a): pass

    def do_GET(self):
        self.send_response(200); self.end_headers(); self.wfile.write(b"ok")

    def do_POST(self):
        import time
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        BODIES.append(body); HEADS.append(self.headers.get("Authorization"))
        asked = body["messages"][-1]["content"]
        deltas = []
        if body.get("chat_template_kwargs", {}).get("enable_thinking"):
            deltas.append({"reasoning_content": f"think<{asked}>"})     # llama-server's spelling
        elif body.get("reasoning", {}).get("enabled"):
            deltas.append({"reasoning": f"think<{asked}>"})             # OpenRouter's
        deltas += [{"content": "echo<"}, {"content": f"{asked}>"}]
        self.send_response(200); self.send_header("Content-Type", "text/event-stream"); self.end_headers()
        for i, d in enumerate(deltas):
            if i == len(deltas) - 1:
                time.sleep(PAUSE)
            self.wfile.write(("data: " + json.dumps({"choices": [{"delta": d}]}) + "\n\n").encode()); self.wfile.flush()
        self.wfile.write(b"data: [DONE]\n\n")


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


def test_thinking_is_asked_for_with_tend_think_and_kept_as_a_t_line(tmp_path, stub):
    """Henri, 2026-08-30: "can I enable thinking for the model somehow?" —
    TEND_THINK turns the template's thinking on; the reasoning comes back
    apart from the answer and is a `T:` line between the Q and the A;
    off, the request says so and no T line is written.  The cap is 2000
    by default ("lift the token cap") and TEND_MAXTOK still sets it."""
    st = tmp_path / "s"; st.mkdir()
    r = deliver(NODE, "two", state=st, stub=stub, TEND_NO_START="1", TEND_THINK="1")
    assert r.returncode == 0, r.stderr
    assert BODIES[-1]["chat_template_kwargs"] == {"enable_thinking": True}
    assert BODIES[-1]["max_tokens"] == 2000
    lines = (st / "replies").read_text().splitlines()
    assert [l.split(" ", 2)[2] for l in lines if l] == ["Q: two", "T: think<two>", "A: echo<two>"]
    assert "  T: think<two>" in r.stdout and "  A: echo<two>" in r.stdout
    r = deliver(NODE, "cold", state=st, stub=stub, TEND_NO_START="1", TEND_MAXTOK="50")
    assert r.returncode == 0 and BODIES[-1]["chat_template_kwargs"] == {"enable_thinking": False}
    assert BODIES[-1]["max_tokens"] == 50
    assert "T:" not in (st / "replies").read_text().split("Q: cold", 1)[1]


def test_the_reply_is_written_as_it_arrives_and_the_live_files_go_when_it_is_whole(tmp_path, stub):
    """Henri, 2026-08-30: "I'd like the model to stream it's output, so
    that I can see where it's going in its work."  The stub sends the
    answer in two halves with a pause between; while deliver is still
    running, turn.answer holds the first half — that is the streaming,
    measured — and when it is done the record has the whole and the live
    files are gone."""
    import time
    st = tmp_path / "s"; st.mkdir()
    env = {"PATH": "/usr/bin:/bin", "TEND_STATE_DIR": str(st), **stub, "TEND_NO_START": "1", "TEND_THINK": "1"}
    p = subprocess.Popen(["sh", str(DELIVER), str(NODE), "half"], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    seen = None
    t = time.monotonic()
    while time.monotonic() - t < 10 and p.poll() is None:
        try:
            a = (st / "turn.answer").read_text()
        except OSError:
            a = ""
        if a.startswith("echo<") and not a.endswith(">"):
            seen = ((st / "turn.thinking").read_text(), a)
            break
        time.sleep(0.02)
    out, err = p.communicate(timeout=30)
    assert p.returncode == 0, err
    assert seen == ("think<half>", "echo<"), "the first half was never on disk while the turn was in flight"
    lines = [l.split(" ", 2)[2] for l in (st / "replies").read_text().splitlines() if l]
    assert lines == ["Q: half", "T: think<half>", "A: echo<half>"]
    assert not (st / "turn.answer").exists() and not (st / "turn.thinking").exists()
    assert "  A: echo<half>" in out


def test_a_reply_with_newlines_and_backslashes_survives_the_stream(tmp_path, stub):
    """The stream is one line per delta; a token with a newline, a tab or a
    backslash in it must land in the record as itself."""
    st = tmp_path / "s"; st.mkdir()
    r = deliver(NODE, "a\\b\tc", state=st, stub=stub, TEND_NO_START="1")
    assert r.returncode == 0, r.stderr
    ex = (st / "replies").read_text()
    assert "A: echo<a\\b\tc>" in ex, ex


def a_door(tmp_path, stub, name="openrouter"):
    """A door at the stub: url, a model name, a key file outside the tree
    with mode 600 (tools/door.sh refuses anything else)."""
    key = tmp_path / "keys" / f"{name}.key"; key.parent.mkdir(exist_ok=True)
    key.write_text("sk-test-0000\n"); key.chmod(0o600)
    d = tmp_path / "doors" / name; d.mkdir(parents=True)
    (d / "door").write_text(f"url  {stub['TEND_LLM_URL']}\nmodel  vendor/some-model\nkey  {key}\nadmitted  the test\n")
    return {"TEND_DOOR_DIR": str(tmp_path / "doors"), "TEND_DOOR": name, "HOME": str(tmp_path)}


def test_a_door_carries_the_turn_with_its_model_and_key_and_is_never_a_pull(tmp_path, stub):
    """Henri, 2026-08-30: "I now have the openrouter available for use."
    Through a door the request names the door's model and carries its key
    (on stdin to curl, never the argument line); no chat_template_kwargs,
    which is the node's loader knob; the ask is not a pull line — a pull
    would start the local node — and the record's V line says who
    answered.  Thinking through a door is OpenRouter's `reasoning`, read
    back from its own spelling."""
    st = tmp_path / "s"; st.mkdir()
    door = a_door(tmp_path, stub)
    # the stub is the "door": point the node's url elsewhere so a turn that ignored the door would fail
    r = deliver(NODE, "through", state=st, stub={"TEND_LLM_URL": "http://127.0.0.1:9/x", "TEND_LLM_HEALTH": "http://127.0.0.1:9/h"}, **door)
    assert r.returncode == 0, r.stderr
    assert BODIES[-1]["model"] == "vendor/some-model" and "chat_template_kwargs" not in BODIES[-1]
    assert HEADS[-1] == "Bearer sk-test-0000"
    assert not (st / "pull").exists(), "a door turn is not a pull"
    lines = [l.split(" ", 2)[2] for l in (st / "replies").read_text().splitlines() if l]
    assert lines == ["Q: through", "V: openrouter vendor/some-model", "A: echo<through>"]
    assert "  via: openrouter (vendor/some-model)" in r.stdout
    r = deliver(NODE, "deep", state=st, stub=stub, TEND_THINK="1", **door)
    assert r.returncode == 0, r.stderr
    assert BODIES[-1]["reasoning"] == {"enabled": True} and "chat_template_kwargs" not in BODIES[-1]
    assert "T: think<deep>" in (st / "replies").read_text()
    assert "sk-test" not in (st / "replies").read_text()


def test_a_door_that_does_not_answer_says_the_doors_name(tmp_path, stub):
    st = tmp_path / "s"; st.mkdir()
    door = a_door(tmp_path, stub)
    (tmp_path / "doors" / "openrouter" / "door").write_text(
        f"url  http://127.0.0.1:9/nothing\nmodel  vendor/x\nkey  {tmp_path}/keys/openrouter.key\n")
    r = deliver(NODE, "hello", state=st, stub=stub, **door)
    assert r.returncode == 1 and "the openrouter door did not answer" in r.stderr, r.stderr
    assert not (st / "replies").exists()
