"""tools/door.sh — a door read, listed, and its model picked.

The three-line read is exercised by test_lead.py through a turn; what is
held here is the listing and the pick (2026-08-30, Henri: "I'd need a way
to browse through all 500 models there are"): the door's own `/models`,
one line per model with what a person chooses by, and `--use` refusing an
id the door does not list — a typo refused here, not a 404 on the first
turn.  The door's side is a stub on the test's loopback.
"""
import http.server
import json
import subprocess
import threading
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
DOOR = ROOT / "tools" / "door.sh"

MODELS = {"data": [
    {"id": "qwen/qwen3.8-flash", "context_length": 262144, "pricing": {"prompt": "0.0000003", "completion": "0.0000012"}},
    {"id": "anthropic/claude-sonnet-5", "context_length": 200000, "pricing": {"prompt": "0.000003", "completion": "0.000015"}},
    {"id": "free/tiny", "pricing": {"prompt": "0", "completion": "0"}},
]}


class _Side(http.server.BaseHTTPRequestHandler):
    heads = []

    def log_message(self, *a): pass

    def do_GET(self):
        _Side.heads.append(self.headers.get("Authorization"))
        if self.path.endswith("/models"):
            self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers()
            self.wfile.write(json.dumps(MODELS).encode())
        else:
            self.send_response(404); self.end_headers()


@pytest.fixture
def door(tmp_path):
    srv = http.server.HTTPServer(("127.0.0.1", 0), _Side)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{srv.server_address[1]}"
    key = tmp_path / "keys" / "openrouter.key"; key.parent.mkdir(); key.write_text("sk-test-0000\n"); key.chmod(0o600)
    d = tmp_path / "doors" / "openrouter"; d.mkdir(parents=True)
    (d / "door").write_text(f"url  {base}/v1/chat/completions\nmodel  anthropic/claude-sonnet-5\nkey  {key}\nadmitted  the test\n")
    _Side.heads.clear()
    yield d / "door"
    srv.shutdown()


def run(tmp_path, *args):
    env = {"PATH": "/usr/bin:/bin", "HOME": str(tmp_path), "TEND_DOOR_DIR": str(tmp_path / "doors")}
    return subprocess.run(["sh", str(DOOR), *args], capture_output=True, text=True, env=env, timeout=30)


def test_it_parses():
    assert subprocess.run(["sh", "-n", str(DOOR)]).returncode == 0


def test_the_three_lines_are_as_before(tmp_path, door):
    r = run(tmp_path, "openrouter")
    assert r.returncode == 0, r.stderr
    url, model, key = r.stdout.splitlines()
    assert url.endswith("/v1/chat/completions") and model == "anthropic/claude-sonnet-5" and key.endswith("openrouter.key")
    assert _Side.heads == [], "a plain read touches the door's side not at all"


def test_models_lists_id_context_and_price_by_id_and_a_pattern_narrows_it(tmp_path, door):
    r = run(tmp_path, "openrouter", "--models")
    assert r.returncode == 0, r.stderr
    lines = [l for l in r.stdout.splitlines() if l.startswith("  ")]
    assert [l.split()[0] for l in lines] == ["anthropic/claude-sonnet-5", "free/tiny", "qwen/qwen3.8-flash"], "by id"
    assert "qwen/qwen3.8-flash" in lines[2] and "262144 ctx" in lines[2] and "$0.3/M in" in lines[2] and "$1.2/M out" in lines[2], lines[2]
    assert "0 ctx" in lines[1] and "$0/M in" in lines[1], lines[1]
    assert r.stdout.rstrip().endswith("door: openrouter lists 3 models; the door's model is anthropic/claude-sonnet-5")
    assert "sk-test" not in r.stdout and _Side.heads[-1] == "Bearer sk-test-0000"
    r = run(tmp_path, "openrouter", "--models", "QWEN")
    assert r.returncode == 0 and [l.split()[0] for l in r.stdout.splitlines() if l.startswith("  ")] == ["qwen/qwen3.8-flash"]
    assert "lists 3 models, 1 matching `QWEN`" in r.stdout
    r = run(tmp_path, "openrouter", "--models", "nothing-like-this")
    assert r.returncode == 0 and "0 matching" in r.stdout


def test_use_sets_the_model_line_only_to_an_id_the_door_lists(tmp_path, door):
    before = door.read_text()
    r = run(tmp_path, "openrouter", "--use", "vendor/no-such")
    assert r.returncode == 2 and "does not list `vendor/no-such`" in r.stderr and "--models vendor/no-such" in r.stderr
    assert door.read_text() == before, "refused, and the door is untouched"
    r = run(tmp_path, "openrouter", "--use", "qwen/qwen3.8-flash")
    assert r.returncode == 0 and "model is qwen/qwen3.8-flash (was anthropic/claude-sonnet-5)" in r.stdout, r.stderr
    assert door.read_text() == before.replace("model  anthropic/claude-sonnet-5", "model  qwen/qwen3.8-flash")
    assert run(tmp_path, "openrouter").stdout.splitlines()[1] == "qwen/qwen3.8-flash"
    r = run(tmp_path, "openrouter", "--use", "qwen; rm -rf /")
    assert r.returncode == 2 and "not a model id" in r.stderr


def test_a_side_that_does_not_answer_and_an_unknown_argument_are_refused(tmp_path, door):
    key = [l for l in door.read_text().splitlines() if l.startswith("key")][0]
    door.write_text(f"url  http://127.0.0.1:9/nothing/chat/completions\nmodel  x/y\n{key}\n")
    r = run(tmp_path, "openrouter", "--models")
    assert r.returncode == 1 and "did not answer" in r.stderr
    r = run(tmp_path, "openrouter", "--browse")
    assert r.returncode == 2 and "unknown argument" in r.stderr


def test_tools_prints_the_doors_tools_word_and_its_calls_cap_or_empty_lines(tmp_path, door):
    """card:tools.md: who gets tools is the door's word — `tools  read ls`,
    `calls  N` and `readchars  N` on the door file; absent, three empty
    lines, and the three-line read is as before."""
    r = run(tmp_path, "openrouter", "--tools")
    assert r.returncode == 0 and r.stdout == "\n\n\n" and _Side.heads == [], r.stderr
    door.write_text(door.read_text() + "tools  read ls\ncalls  4\n")
    assert run(tmp_path, "openrouter", "--tools").stdout == "read ls\n4\n\n"
    door.write_text(door.read_text() + "readchars  60000\n")
    assert run(tmp_path, "openrouter", "--tools").stdout == "read ls\n4\n60000\n"
    assert len(run(tmp_path, "openrouter").stdout.splitlines()) == 3, "the three-line read is as before"
