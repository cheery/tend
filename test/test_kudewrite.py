"""`tools/kudewrite.py` — card:kude.md chapter 1's second half: a door
model, given the llm wire's session type and the language's reference and
nothing else, writes the ask node in Kude; every try goes through the
check, a refusal goes back as its own words alone, and the count is kept.

A stand-in door on a free port plays the model from a script, and records
every conversation it was sent.  The test builds the side it means: a
scratch HOME with a key at mode 600, a scratch doors/ and a scratch out.

Red first, 2026-09-24: every test below was run before the tool existed.
"""

import http.server
import json
import os
import pathlib
import subprocess
import sys
import threading

ROOT = pathlib.Path(__file__).resolve().parent.parent
TOOL = ROOT / "tools" / "kudewrite.py"
GOOD = (ROOT / "ask-kude" / "ask.kude").read_text(encoding="utf-8")
BAD = 'main(llm: Llm; answer: Str) <- llm.pull, llm.ask, llm ! "q", llm ? answer, llm.let_go.\n'


class _Door:
    """The OpenAI chat wire, answering each request with the next reply of
    a script; a reply that is an int is an HTTP error with that status."""

    def __init__(self, replies):
        self.replies, self.sent = list(replies), []
        door = self

        class H(http.server.BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def do_POST(self):
                body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                door.sent.append((body, self.headers.get("Authorization")))
                reply = door.replies.pop(0)
                if isinstance(reply, int):
                    self.send_response(reply)
                    self.end_headers()
                    self.wfile.write(b'{"error": {"message": "no such key"}}')
                    return
                out = {"choices": [{"message": {"role": "assistant", "content": reply}}]}
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(out).encode())

        self.srv = http.server.HTTPServer(("127.0.0.1", 0), H)
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()
        self.url = f"http://127.0.0.1:{self.srv.server_address[1]}/v1/chat/completions"

    def close(self):
        self.srv.shutdown()


def write(tmp_path, door, *args):
    home = tmp_path / "home"
    home.mkdir(exist_ok=True)
    key = home / "k.key"
    key.write_text("sk-test\n")
    key.chmod(0o600)
    d = tmp_path / "doors" / "stand-in"
    d.mkdir(parents=True, exist_ok=True)
    (d / "door").write_text(f"url  {door.url}\nmodel  stand-in-1\nkey  ~/k.key\ntemperature  none\n")
    env = dict(os.environ, HOME=str(home), TEND_DOOR_DIR=str(tmp_path / "doors"))
    return subprocess.run([sys.executable, str(TOOL), "--door", "stand-in", "--out", str(tmp_path / "out"),
                           "--node", str(tmp_path / "node"), *args],
                          capture_output=True, text=True, env=env, timeout=60)


def record(tmp_path):
    (run,) = (tmp_path / "out").iterdir()
    return run


def test_it_parses():
    assert subprocess.run([sys.executable, "-m", "py_compile", str(TOOL)]).returncode == 0


def test_the_hand_over_is_the_type_the_reference_and_the_task_and_nothing_else():
    r = subprocess.run([sys.executable, str(TOOL), "--handed"], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    handed = r.stdout
    for t in ("type Llm      = +{ pull: LlmWait }.", "type LlmLetGo = +{ let_go: end }."):
        assert t in handed, t
    assert "Kude: deterministic Horn clauses" in handed, "the language's reference is kude.py's header"
    assert "'main(llm)'" in handed and "What is tend for?  Answer in one sentence." in handed
    # nothing else: not the node, not the example programs
    for program in ("asked(llm", "client(c: ~Bank", "gcd(a, b", "line(io: Input"):
        assert program not in handed, program


def test_a_first_try_that_checks_is_counted_and_becomes_the_node(tmp_path):
    door = _Door([f"Here it is:\n\n```kude\n{GOOD}```\n"])
    try:
        r = write(tmp_path, door)
    finally:
        door.close()
    assert r.returncode == 0, r.stderr
    run = record(tmp_path)
    count = (run / "count").read_text()
    assert "tries 1, refused 0, checked at try 1" in count, count
    assert (run / "try-1.kude").read_text() == GOOD
    assert (tmp_path / "node" / "node.kude").read_text() == GOOD
    (body, auth), = door.sent
    assert auth == "Bearer sk-test" and body["model"] == "stand-in-1" and "temperature" not in body


def test_a_refusal_goes_back_as_its_own_words_alone_and_the_fix_is_counted(tmp_path):
    door = _Door([f"```\n{BAD}```", f"```\n{GOOD}```"])
    try:
        r = write(tmp_path, door)
    finally:
        door.close()
    assert r.returncode == 0, r.stderr
    run = record(tmp_path)
    refusal = (run / "try-1.check").read_text()
    assert "ask is not a branch of llm's LlmWait" in refusal, refusal
    second, _ = door.sent[1]
    assert second["messages"][-1] == {"role": "user", "content": refusal}, "the refusal's words, nothing added"
    assert second["messages"][-2]["role"] == "assistant"
    count = (run / "count").read_text()
    assert "tries 2, refused 1, checked at try 2" in count and "from the refusal's words alone" in count, count
    assert (tmp_path / "node" / "node.kude").read_text() == GOOD


def test_no_try_that_checks_is_counted_and_no_node_is_written(tmp_path):
    door = _Door([f"```\n{BAD}```"] * 2)
    try:
        r = write(tmp_path, door, "--tries", "2")
    finally:
        door.close()
    assert r.returncode == 1, (r.returncode, r.stderr)
    count = (record(tmp_path) / "count").read_text()
    assert "tries 2, refused 2, none checked" in count, count
    assert not (tmp_path / "node" / "node.kude").exists()


def test_a_door_that_refuses_the_turn_is_said_and_the_record_kept(tmp_path):
    door = _Door([401])
    try:
        r = write(tmp_path, door)
    finally:
        door.close()
    assert r.returncode == 2 and "401" in r.stderr, (r.returncode, r.stderr)
    assert "door refused" in (record(tmp_path) / "count").read_text()
