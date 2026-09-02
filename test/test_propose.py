"""tools/propose.sh — the model writes, and only ever proposes (card:session-program.md, brick 3).

Brick 2 let the model read the tree; brick 3 lets it produce tree-shaped
work — a kaizen draft, a card-edit proposal — under the boundary the
whole tree is built on: a party may not bound itself, so the model may
not land its own words in the tree.  propose writes ONLY to a gitignored
proposals area, banner-marked as not-tree-until-a-person-lands-it, and
never touches a tracked file.  The node is a stub here; what is tested is
the boundary and that the draft is written.
"""
import http.server
import json
import subprocess
import threading
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
PROPOSE = ROOT / "tools" / "propose.sh"
NODE = ROOT / "llm"


class _Draft(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        self.send_response(200); self.end_headers(); self.wfile.write(b"ok")
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        task = body["messages"][-1]["content"]
        out = {"choices": [{"message": {"role": "assistant",
               "content": f"DRAFT for: {task}\n\nsome proposed lines."}}]}
        self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers()
        self.wfile.write(json.dumps(out).encode())


@pytest.fixture
def stub():
    srv = http.server.HTTPServer(("127.0.0.1", 0), _Draft)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{srv.server_address[1]}"
    yield {"TEND_LLM_URL": base + "/v1/chat/completions", "TEND_LLM_HEALTH": base + "/health"}
    srv.shutdown()


def propose(node, *args, stub, propdir, **extra):
    env = {"PATH": "/usr/bin:/bin", "TEND_PROPOSAL_DIR": str(propdir), **stub, **extra}
    return subprocess.run(["sh", str(PROPOSE), str(node), *args], capture_output=True, text=True, env=env)


def test_it_writes_a_banner_marked_draft_into_the_proposals_area(tmp_path, stub):
    propdir = tmp_path / "proposals"
    r = propose(NODE, "draft a kaizen line", stub=stub, propdir=propdir)
    assert r.returncode == 0, r.stdout + r.stderr
    files = list(propdir.glob("*.md"))
    assert len(files) == 1, "one proposal written"
    text = files[0].read_text()
    assert "PROPOSAL" in text and "not tree content until" in text.lower(), "banner marks it unlanded"
    assert "some proposed lines." in text, "the model's draft is in it"
    assert str(files[0]) in r.stdout, "the path is printed for the person to review"


def test_two_drafts_in_one_minute_with_one_task_are_two_files(tmp_path, stub):
    """2026-09-02: the gemma4 conditioning arm is 24 draft turns on one
    pinned task through `doors/llm/door`, and the file was named by the
    minute and the task's slug — so the second draft of a minute silently
    overwrote the first.  A proposal is never overwritten: the name gets
    a suffix, the way compare.py's accounts do."""
    propdir = tmp_path / "proposals"
    for _ in range(3):
        r = propose(NODE, "draft a kaizen line", stub=stub, propdir=propdir)
        assert r.returncode == 0, r.stdout + r.stderr
    files = sorted(propdir.glob("*.md"))
    assert len(files) == 3, [f.name for f in files]
    assert all("some proposed lines." in f.read_text() for f in files)


def test_it_never_writes_a_tracked_file(tmp_path, stub):
    """The boundary: the model proposes, the person applies.  propose must
    write only under the proposals area — given a card as material it must
    not edit that card."""
    card = tmp_path / "a-card.md"
    card.write_text("original card body\n")
    propdir = tmp_path / "proposals"
    r = propose(NODE, "propose an edit to this card", str(card), stub=stub, propdir=propdir)
    assert r.returncode == 0, r.stdout + r.stderr
    assert card.read_text() == "original card body\n", "the material file is untouched"
    assert list(propdir.glob("*.md")), "the proposal is written to the proposals area, not the card"


def test_the_material_reaches_the_model(tmp_path, stub):
    doc = tmp_path / "m.md"; doc.write_text("the ground truth line")
    propdir = tmp_path / "proposals"
    r = propose(NODE, "use the material", str(doc), stub=stub, propdir=propdir)
    text = list(propdir.glob("*.md"))[0].read_text()
    assert "the material" in text.lower()  # task echoed in the draft banner/body


def test_inside_the_fence_it_refuses(tmp_path, stub):
    propdir = tmp_path / "proposals"
    r = propose(NODE, "x", stub=stub, propdir=propdir, TEND_FENCED="1")
    assert r.returncode != 0 and "fence" in (r.stdout + r.stderr).lower()


def test_a_missing_material_file_is_refused(tmp_path, stub):
    propdir = tmp_path / "proposals"
    r = propose(NODE, "x", str(tmp_path / "nope.md"), stub=stub, propdir=propdir)
    assert r.returncode != 0 and "no such" in (r.stdout + r.stderr).lower()
