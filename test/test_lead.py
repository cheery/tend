"""tools/lead.sh — one led turn: the node reads the board, picks one thing, proposes or pulls the cord (card:session-program.md, §"a node that leads work").

The three bricks — deliver, consult, propose — put under a loop with the
cords.  A led turn reads the open board, names one card and one small
thing, and either proposes it (through propose.sh, into the gitignored
proposals area) or, when it cannot decide, pulls the andon — the record,
no reach row (card:andon-panel.md).  Either way it writes its own account
under proposals/lead/: the node's lamp, the reflective account the card
said waits for the first node that leads.  The node is a stub; what is
tested is the shape of a turn and the boundary — no tracked file is ever
written, and a card the node makes up is a cord pull, not a proposal.
"""
import http.server
import json
import subprocess
import threading
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
LEAD = ROOT / "tools" / "lead.sh"
NODE = ROOT / "llm"


def _stub(reply):
    class H(http.server.BaseHTTPRequestHandler):
        seen = []
        def log_message(self, *a): pass
        def do_GET(self):
            self.send_response(200); self.end_headers(); self.wfile.write(b"ok")
        def do_POST(self):
            body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            H.seen.append(body)
            # the first ask is the lead's pick; a second (propose's) gets a draft
            content = reply if len(H.seen) == 1 else "DRAFT: some proposed lines."
            out = {"choices": [{"message": {"role": "assistant", "content": content}}]}
            self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers()
            self.wfile.write(json.dumps(out).encode())
    return H


@pytest.fixture
def board(tmp_path):
    b = tmp_path / "board"; b.mkdir(); (b / "done").mkdir()
    (b / "README.md").write_text("# board\n")
    (b / "lander.md").write_text("# lander — a change waits\n\n    status   open\n    because  a commit waits on a hand\n    asked    Henri\n\nbody\n")
    (b / "silent-cord.md").write_text("# silent-cord — quiet\n\n    status   open\n    because  the cord needs a row\n    asked    Henri\n")
    (b / "done" / "grant.md").write_text("# grant\n\n    status   done — 2026-08-25\n    because  x\n    asked    Henri\n")
    return b


def lead(reply, board, tmp_path, **extra):
    H = _stub(reply)
    srv = http.server.HTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{srv.server_address[1]}"
    env = {"PATH": "/usr/bin:/bin", "HOME": str(tmp_path),
           "TEND_LLM_URL": base + "/v1/chat/completions", "TEND_LLM_HEALTH": base + "/health",
           "TEND_NO_START": "1",
           "TEND_PROPOSAL_DIR": str(tmp_path / "proposals"),
           "TEND_ANDON_STATE": str(tmp_path / "andon"),
           "TEND_BOARD_DIR": str(board),
           "TEND_STATE_DIR": str(tmp_path / "state"), **extra}
    try:
        r = subprocess.run(["sh", str(LEAD), str(NODE)], capture_output=True, text=True, env=env)
    finally:
        srv.shutdown()
    return r, H.seen


def test_a_pick_becomes_a_proposal_and_an_account(board, tmp_path):
    r, seen = lead("CARD: lander.md\nTASK: draft the lamp's one line\nWHY: it is day one", board, tmp_path)
    assert r.returncode == 0, r.stdout + r.stderr
    props = [p for p in (tmp_path / "proposals").glob("*.md")]
    assert len(props) == 1, "one proposal, through propose.sh"
    assert "some proposed lines." in props[0].read_text()
    accounts = list((tmp_path / "proposals" / "lead").glob("*.md"))
    assert len(accounts) == 1, "the node's account of its turn — the lamp"
    acc = accounts[0].read_text()
    assert "lander.md" in acc and "draft the lamp's one line" in acc and "it is day one" in acc
    assert "lander.md" in seen[0]["messages"][0]["content"], "the open board reached the model"
    assert "grant.md" not in seen[0]["messages"][0]["content"], "done/ is not on the open board"


def test_it_never_writes_a_tracked_file(board, tmp_path):
    before = {p: p.read_text() for p in board.rglob("*.md")}
    r, _ = lead("CARD: lander.md\nTASK: rewrite the card\nWHY: x", board, tmp_path)
    assert r.returncode == 0, r.stdout + r.stderr
    assert {p: p.read_text() for p in board.rglob("*.md")} == before, "the board is untouched"


def test_when_it_cannot_decide_it_pulls_the_cord(board, tmp_path):
    r, _ = lead("ANDON: which of lander and silent-cord is yours to pick?", board, tmp_path)
    assert r.returncode == 0, r.stdout + r.stderr
    pending = (tmp_path / "andon" / "andon.pending").read_text()
    assert "which of lander and silent-cord" in pending, "the question is on the record, no reach row"
    assert not list((tmp_path / "proposals").glob("*.md")), "no proposal when the cord is pulled"
    acc = list((tmp_path / "proposals" / "lead").glob("*.md"))[0].read_text()
    assert "andon" in acc.lower()


def test_a_card_not_on_the_board_is_a_cord_pull_not_a_proposal(board, tmp_path):
    r, _ = lead("CARD: unicorn.md\nTASK: build it\nWHY: y", board, tmp_path)
    assert r.returncode == 0, r.stdout + r.stderr
    assert not list((tmp_path / "proposals").glob("*.md")), "an invented card is not proposed on"
    pending = (tmp_path / "andon" / "andon.pending").read_text()
    assert "unicorn.md" in pending


def test_a_reply_with_no_shape_is_a_cord_pull(board, tmp_path):
    r, _ = lead("I think the board is interesting.", board, tmp_path)
    assert r.returncode == 0, r.stdout + r.stderr
    assert (tmp_path / "andon" / "andon.pending").exists()
    assert not list((tmp_path / "proposals").glob("*.md"))


def test_inside_the_fence_it_refuses(board, tmp_path):
    r, _ = lead("CARD: lander.md\nTASK: x\nWHY: y", board, tmp_path, TEND_FENCED="1")
    assert r.returncode != 0 and "fence" in (r.stdout + r.stderr).lower()
