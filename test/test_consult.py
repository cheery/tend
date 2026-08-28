"""tools/consult.sh — the model acting on what it reads (card:session-program.md, brick 2).

deliver.sh carries a bare question; consult grounds it in named tree
files, so the answer is shaped by the tree's own documents rather than
the model's cold memory — the conditioning question made runnable
(gemma cold called jidoka Buddhist; grounded in a tree doc that says
stop-the-line, does it read it?).  The node's port is unreachable from
the fence, so the model is a stub that echoes the material it was given;
what is tested is that the tree's text reaches the model and the answer
comes back.
"""
import http.server
import json
import subprocess
import threading
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
CONSULT = ROOT / "tools" / "consult.sh"
NODE = ROOT / "llm"


class _Echo(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        self.send_response(200); self.end_headers(); self.wfile.write(b"ok")
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        # echo the whole prompt the model was given, system + user
        seen = " || ".join(m["role"] + ":" + m["content"] for m in body["messages"])
        out = {"choices": [{"message": {"role": "assistant", "content": seen}}]}
        self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers()
        self.wfile.write(json.dumps(out).encode())


@pytest.fixture
def stub():
    srv = http.server.HTTPServer(("127.0.0.1", 0), _Echo)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{srv.server_address[1]}"
    yield {"TEND_LLM_URL": base + "/v1/chat/completions", "TEND_LLM_HEALTH": base + "/health"}
    srv.shutdown()


def consult(node, *args, stub, **extra):
    env = {"PATH": "/usr/bin:/bin", **stub, **extra}
    return subprocess.run(["sh", str(CONSULT), str(node), *args], capture_output=True, text=True, env=env)


def test_the_named_file_reaches_the_model_and_the_answer_returns(tmp_path, stub):
    doc = tmp_path / "note.md"
    doc.write_text("Jidoka is stop-the-line: a machine halts itself on a defect.")
    r = consult(NODE, "What is jidoka?", str(doc), stub=stub)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "stop-the-line" in r.stdout, "the file's text was given to the model"
    assert "What is jidoka?" in r.stdout, "the question was asked"


def test_it_defaults_to_the_board_readme_when_no_file_is_named(tmp_path, stub):
    r = consult(NODE, "What is the board?", stub=stub)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "one file per task" in r.stdout.lower() or "board" in r.stdout.lower()


def test_a_missing_file_is_refused_out_loud(tmp_path, stub):
    r = consult(NODE, "anything", str(tmp_path / "nope.md"), stub=stub)
    assert r.returncode != 0 and "no such" in (r.stdout + r.stderr).lower()


def test_inside_the_fence_it_says_the_runners_side_answers(tmp_path, stub):
    doc = tmp_path / "d.md"; doc.write_text("x")
    r = consult(NODE, "q", str(doc), stub=stub, TEND_FENCED="1")
    assert r.returncode != 0 and "fence" in (r.stdout + r.stderr).lower()
