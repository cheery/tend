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
import re
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
        if "LOADING" in task:   # llama-server while the model loads: a JSON error, no choices
            self.send_response(503); self.send_header("Content-Type", "application/json"); self.end_headers()
            self.wfile.write(json.dumps({"error": {"code": 503, "message": "Loading model", "type": "unavailable_error"}}).encode()); return
        content = f"DRAFT for: {task}\n\nsome proposed lines."
        if "ECHOSYS" in task:   # F010's test: the draft is the system prompt the model was handed
            content = " || ".join(m["role"] + ":" + m["content"] for m in body["messages"])
        out = {"choices": [{"message": {"role": "assistant", "content": content}}]}
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


def test_a_reply_with_no_completion_writes_no_proposal(tmp_path, stub):
    """2026-09-02, run 2 of the gemma4 arm: the node's sitting fired
    mid-loop, the hold's tick restarted it, and while it loaded
    llama-server answered every ask with a 503 JSON error — and propose.sh
    wrote seventeen banner-only proposals in three seconds, because its
    `jq -e` cannot tell an empty draft from a draft.  A reply with no
    completion is a refusal said out loud, and no file."""
    propdir = tmp_path / "proposals"
    r = propose(NODE, "LOADING draft a kaizen line", stub=stub, propdir=propdir)
    assert r.returncode == 1, r.stdout + r.stderr
    assert "not a completion" in r.stderr and "Loading model" in r.stderr, r.stderr
    assert not list(propdir.glob("*.md")), "no banner with nothing under it"


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


def test_a_cut_material_tells_the_model_what_it_lost_and_that_nothing_can_fetch_it(tmp_path, stub):
    """F010: the draft was written from material cut at TEND_CTXCHARS with
    nothing said to the mind — a byte cut, mid-word.  Now the cut is a line
    in the material, in tools/compare.py's cut_notice wording: chars of chars,
    the first line not shown of the lines there are, and that there is no way
    to ask for the rest.  A material that fits carries no such line."""
    doc = tmp_path / "m.md"
    doc.write_text("\n".join(f"line {i} of the ground truth" for i in range(1, 41)) + "\n")
    propdir = tmp_path / "proposals"
    r = propose(NODE, "ECHOSYS", str(doc), stub=stub, propdir=propdir, TEND_CTXCHARS="300")
    assert r.returncode == 0, r.stdout + r.stderr
    text = list(propdir.glob("*.md"))[0].read_text()
    assert "[… cut at 300 chars of " in text and "no way to ask for it" in text, text
    assert re.search(r"at line \d+ of 4[12] of the material", text), text   # the cut line, of the lines there are
    assert "line 40 of the ground truth" not in text, "the tail is cut, and the notice says so"
    # a material that fits is handed whole, with no notice
    propdir2 = tmp_path / "p2"
    propose(NODE, "ECHOSYS", str(doc), stub=stub, propdir=propdir2, TEND_CTXCHARS="6000")
    text = list(propdir2.glob("*.md"))[0].read_text()
    assert "line 40 of the ground truth" in text and "cut at" not in text, text


def test_a_missing_material_file_is_refused(tmp_path, stub):
    propdir = tmp_path / "proposals"
    r = propose(NODE, "x", str(tmp_path / "nope.md"), stub=stub, propdir=propdir)
    assert r.returncode != 0 and "no such" in (r.stdout + r.stderr).lower()
