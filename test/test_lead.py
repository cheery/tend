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
import re
import subprocess
import threading
from pathlib import Path

import pytest
import time

ROOT = Path(__file__).resolve().parent.parent
LEAD = ROOT / "tools" / "lead.sh"
NODE = ROOT / "llm"


def _stub(reply):
    class H(http.server.BaseHTTPRequestHandler):
        seen = []
        heads = []
        def log_message(self, *a): pass
        def do_GET(self):
            self.send_response(200); self.end_headers(); self.wfile.write(b"ok")
        def do_POST(self):
            body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            H.seen.append(body); H.heads.append({k.lower(): v for k, v in self.headers.items()})
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


def _landlock_abi():
    import ctypes
    libc = ctypes.CDLL(None, use_errno=True)
    v = libc.syscall(444, 0, 0, 1)  # landlock_create_ruleset(NULL, 0, VERSION)
    return v if v > 0 else 0


@pytest.mark.skipif(_landlock_abi() < 4 or not Path("/usr/bin/python3").exists(),
                    reason="the kept turn needs Landlock ABI 4 and a system python3 for keep")
def test_a_kept_turn_drafts_and_the_boundary_is_keeps_not_the_scripts(board, tmp_path):
    """`lead.sh NODE --kept` runs the turn under keep: the tree readable,
    only proposals/, the node's state and the andon record writable, one
    connect to the node's port.  The turn drafts as before — and a write
    to the board from the same confinement is refused, so the boundary
    brick 3 held in propose.sh's code is now held by the kernel."""
    r, seen = lead("CARD: lander.md\nTASK: one line\nWHY: w", board, tmp_path, TEND_LEAD_KEPT="1",
                   TEND_KEPT_PROBE=str(board / "lander.md"))
    assert r.returncode == 0, r.stdout + r.stderr
    assert list((tmp_path / "proposals").glob("*.md")), "the kept turn still drafts"
    assert "probe: refused" in r.stdout + r.stderr, r.stdout + r.stderr
    assert (board / "lander.md").read_text().startswith("# lander"), "the board is untouched under keep"


def test_a_kept_turn_on_a_node_that_died_says_why_it_died(board, tmp_path):
    """Henri, 2026-08-28 13:27: `lead.sh llm --kept` said "not up — start
    it first" while the log said llama-server could not load libsvml.so.
    A kept turn that finds no node reads the last stop and the log's last
    error line, so the person sees the cause, not the symptom."""
    st = tmp_path / "state"; st.mkdir()
    (st / "stopped").write_text("exited 127: llm stopped by itself\n")
    (st / "log").write_text("keep.py:153: DeprecationWarning: noise\n  class path_beneath_attr\n"
                            "llama-server: error while loading shared libraries: libsvml.so: cannot open\n")
    r, _ = lead("CARD: lander.md\nTASK: x\nWHY: y", board, tmp_path, TEND_LEAD_KEPT="1",
                TEND_LLM_HEALTH="http://127.0.0.1:1/health")
    assert r.returncode != 0
    out = r.stdout + r.stderr
    assert "exited 127" in out and "libsvml.so" in out, out
    assert "DeprecationWarning" not in out, "the warning noise is not the reason"


def test_a_kept_turn_waits_for_a_runner_that_is_still_loading(board, tmp_path):
    """A runner holds the lock and its port is not yet answering (the llm
    node takes ~80 s to load): the kept turn waits for /health rather
    than refusing at once."""
    import http.server, threading, subprocess as sp
    st = tmp_path / "state"; st.mkdir()
    holder = sp.Popen(["sh", "-c", 'exec 9>>"$1"; flock 9; exec sleep 30', "_", str(st / "run.lock")])
    t0 = time.monotonic()
    class Slow(http.server.BaseHTTPRequestHandler):
        def log_message(self, *a): pass
        def do_GET(self):
            self.send_response(200 if time.monotonic() - t0 > 2 else 503); self.end_headers()
        def do_POST(self):
            body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            out = {"choices": [{"message": {"role": "assistant", "content": "CARD: lander.md\nTASK: t\nWHY: w"}}]}
            self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers()
            self.wfile.write(json.dumps(out).encode())
    srv = http.server.HTTPServer(("127.0.0.1", 0), Slow)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{srv.server_address[1]}"
    env = {"PATH": "/usr/bin:/bin", "HOME": str(tmp_path), "TEND_LEAD_KEPT": "1",
           "TEND_LLM_URL": base + "/v1/chat/completions", "TEND_LLM_HEALTH": base + "/health",
           "TEND_PROPOSAL_DIR": str(tmp_path / "proposals"), "TEND_ANDON_STATE": str(tmp_path / "andon"),
           "TEND_BOARD_DIR": str(board), "TEND_STATE_DIR": str(st)}
    try:
        r = sp.run(["sh", str(LEAD), str(NODE)], capture_output=True, text=True, env=env, timeout=60)
    finally:
        srv.shutdown(); holder.kill(); holder.wait()
    assert r.returncode == 0, r.stdout + r.stderr
    assert "waiting" in r.stderr, r.stderr


def test_two_turns_in_one_minute_leave_two_accounts(board, tmp_path):
    """2026-08-28, 13:48: the first two live led turns fell in the same
    minute — lead.log has two 13:48 lines and proposals/lead/ one
    13:48 account, the second turn's over the first's (an andon pull,
    gone).  The lamp is per turn; a stamp by the minute is a stamp
    that lies once a loop runs.  Red first."""
    lead("CARD: lander.md\nTASK: one line\nWHY: because\n", board, tmp_path)
    lead("ANDON: which card?\n", board, tmp_path)
    accounts = sorted((tmp_path / "proposals" / "lead").glob("*.md"))
    assert len(accounts) == 2, [a.name for a in accounts]
    texts = [a.read_text() for a in accounts]
    assert any("outcome  proposed" in t for t in texts) and any("outcome  andon" in t for t in texts)
    log = (tmp_path / "state" / "lead.log").read_text().splitlines()
    assert len(log) == 2


def test_a_pick_in_the_prompts_own_angle_brackets_resolves_to_the_open_card(board, tmp_path):
    """13:57 and 13:58, live: gemma answered `CARD: <canvas-script.md>` —
    the prompt's `CARD: <filename from the list>` placeholder echoed,
    brackets and all — and the turn was a cord pull on a name not on the
    board, which was right.  But `<lander.md>` is lander.md said in the
    prompt's own typography: the brackets are the shape, the name is
    what is checked against the open shelf, and the shelf is still the
    judge.  Red first."""
    r, _ = lead("CARD: <lander.md>\nTASK: one line\nWHY: because\n", board, tmp_path)
    assert r.returncode == 0, r.stdout + r.stderr
    assert list((tmp_path / "proposals").glob("*.md")), "a bracketed open card is a pick"
    assert "lead proposed lander.md" in (tmp_path / "state" / "lead.log").read_text()
    r, _ = lead("CARD: <unicorn.md>\nTASK: build it\nWHY: y", board, tmp_path)
    assert "unicorn.md" in (tmp_path / "andon" / "andon.pending").read_text(), "an invented card, bracketed, is still a cord pull"


def test_a_pick_decorated_with_the_digests_own_fence_is_read_by_its_filename(board, tmp_path):
    """17:46 and 18:01, live, after the angle brackets were taken out of the
    prompt: `CARD: canvas.md ===` — the digest's `=== name ===` fence
    echoed this time, and the shelf refused `canvas.md ===`.  The
    filename is the one thing checked; whatever the model wraps it in
    is not.  Red first."""
    r, _ = lead("CARD: lander.md ===\nTASK: one line\nWHY: because\n=== lander.md ===\nmore\n", board, tmp_path)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "lead proposed lander.md" in (tmp_path / "state" / "lead.log").read_text()
    r, _ = lead("CARD: `unicorn.md` ===\nTASK: x\nWHY: y", board, tmp_path)
    assert "unicorn.md" in (tmp_path / "andon" / "andon.pending").read_text()


# --- the door: where a model other than the node's is admitted (card:session-program.md, card:model-acceptance.md, 2026-08-29 —
#     Henri: "build capability for both gemma and claude, also I'm thinking about subscribing to openrouter") ---

def _tool_stub(reply):
    """A door that streams, as the courier's wire does, and calls one tool
    first: the pick's first round is `ls board/`, the second the reply;
    propose's draft ask is not streamed and gets a plain completion."""
    class H(http.server.BaseHTTPRequestHandler):
        seen = []
        heads = []
        def log_message(self, *a): pass
        def do_GET(self):
            self.send_response(200); self.end_headers(); self.wfile.write(b"ok")
        def _sse(self, deltas):
            self.send_response(200); self.send_header("Content-Type", "text/event-stream"); self.end_headers()
            for d in deltas:
                self.wfile.write(("data: " + json.dumps({"choices": [{"delta": d}]}) + "\n\n").encode())
            self.wfile.write(b"data: [DONE]\n\n")
        def do_POST(self):
            body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            H.seen.append(body); H.heads.append({k.lower(): v for k, v in self.headers.items()})
            if not body.get("stream"):
                out = {"choices": [{"message": {"role": "assistant", "content": "DRAFT: some proposed lines."}}]}
                self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers()
                self.wfile.write(json.dumps(out).encode()); return
            rounds = sum(1 for m in body["messages"] if m["role"] == "assistant" and m.get("tool_calls"))
            if rounds == 0 and body.get("tools"):
                args = json.dumps({"dir": "board/"})
                self._sse([{"tool_calls": [{"index": 0, "id": "call_0", "type": "function", "function": {"name": "ls", "arguments": ""}}]},
                           {"tool_calls": [{"index": 0, "function": {"arguments": args}}]}])
            else:
                self._sse([{"content": reply[:4]}, {"content": reply[4:]}])
    return H


def door_turn(reply, board, tmp_path, key_mode=0o600, key_path=None, door="openrouter", door_lines="", stub=None, **extra):
    """One turn through a door: the door names the stub's url, a model, and
    a key file outside the tree; the stub records what arrived.
    `door_lines` are appended to the door file (F015: `thinking  template`)."""
    H = (stub or _stub)(reply)
    srv = http.server.HTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{srv.server_address[1]}"
    key = Path(key_path) if key_path else tmp_path / "keys" / "openrouter.key"
    if not key_path:
        key.parent.mkdir(); key.write_text("sk-test-0000\n"); key.chmod(key_mode)
    d = tmp_path / "doors" / "openrouter"; d.mkdir(parents=True)
    (d / "door").write_text(f"url  {base}/v1/chat/completions\nmodel  vendor/some-model\nkey  {key}\n"
                            "admitted  the test, for the stub\n" + door_lines)
    env = {"PATH": "/usr/bin:/bin", "HOME": str(tmp_path),
           "TEND_DOOR_DIR": str(tmp_path / "doors"), "TEND_DOOR": door,
           "TEND_PROPOSAL_DIR": str(tmp_path / "proposals"),
           "TEND_ANDON_STATE": str(tmp_path / "andon"),
           "TEND_BOARD_DIR": str(board),
           "TEND_STATE_DIR": str(tmp_path / "state"), **extra}
    try:
        r = subprocess.run(["sh", str(LEAD), str(NODE)], capture_output=True, text=True, env=env, timeout=60)
    finally:
        srv.shutdown()
    return r, H.seen, H.heads


def test_a_door_carries_the_model_and_the_key_and_the_account_names_it(board, tmp_path):
    r, seen, heads = door_turn("CARD: lander.md\nTASK: draft the lamp's one line\nWHY: day one", board, tmp_path)
    assert r.returncode == 0, r.stdout + r.stderr
    assert len(seen) == 2, "the pick and the draft both went through the door"
    for body, head in zip(seen, heads):
        assert body["model"] == "vendor/some-model"
        assert head.get("authorization") == "Bearer sk-test-0000"
        assert "chat_template_kwargs" not in body, "the node's own loader knob does not go out of a door"
    acc = next((tmp_path / "proposals" / "lead").glob("*.md")).read_text()
    assert "door     openrouter (vendor/some-model)" in acc, acc
    assert "sk-test" not in acc, "the key is never in an account"
    prop = next((tmp_path / "proposals").glob("*.md")).read_text()
    assert "through the openrouter door" in prop and "sk-test" not in prop, prop


def test_a_door_that_says_thinking_template_sends_the_nodes_knob_with_the_model(board, tmp_path):
    """F015 (2026-09-02): `doors/llm/door` is the node at its own port, and
    a led turn through it got a model line and no loader knob, so gemma4
    thought in the content channel.  `thinking  template` on the door
    sends `enable_thinking:false` beside the model's name, on the pick
    and on the draft."""
    r, seen, _ = door_turn("CARD: lander.md\nTASK: draft the lamp's one line\nWHY: day one", board, tmp_path,
                           door_lines="thinking  template\n")
    assert r.returncode == 0, r.stdout + r.stderr
    assert len(seen) == 2
    for body in seen:
        assert body["model"] == "vendor/some-model"
        assert body["chat_template_kwargs"] == {"enable_thinking": False}, body
        assert "reasoning" not in body


@pytest.mark.skipif(_landlock_abi() < 4 or not Path("/usr/bin/python3").exists(),
                    reason="the kept turn needs Landlock ABI 4 and a system python3 for keep")
def test_a_tools_turn_holds_the_digest_back_and_the_mind_reads_the_board_under_keep_inside_a_kept_turn(board, tmp_path):
    """card:session-program.md §"13:18" (2026-09-04): the live kept turn had
    no C: line because the digest was in the prompt.  `--tools` rides the
    pick on the courier with the door's tools and no digest: the first
    request carries tools and no card's because, the mind's `ls board/`
    runs under keep — inside a turn that is itself under keep — and the
    account carries the C: line; the draft follows as before."""
    r, seen, _ = door_turn("CARD: lander.md\nTASK: one line\nWHY: w", board, tmp_path, stub=_tool_stub,
                           door_lines="tools  ls read\ncalls 4\n", TEND_LEAD_KEPT="1", TEND_LEAD_TOOLS="1",
                           TEND_KEPT_PROBE=str(board / "lander.md"))
    assert r.returncode == 0, r.stdout + r.stderr
    first = seen[0]
    assert first.get("tools") and first["tools"][0]["function"]["name"] in ("ls", "read"), first
    sys_text = "\n".join(m["content"] for m in first["messages"] if m["role"] == "system")
    assert "a commit waits on a hand" not in sys_text, "the digest was held back"
    assert "board/*.md" in sys_text, sys_text
    # the pick's own text names no card: six live turns picked tools.md five times with "tools" in the ask
    pick_text = next(m["content"] for m in first["messages"] if m["role"] == "system" and "board/*.md" in m["content"])
    cards = [p.stem for p in (ROOT / "board").glob("*.md") if p.stem != "README"]
    named = [c for c in cards if c in pick_text.lower()]
    assert not named, f"the pick text names a card: {named}"
    assert "three" in pick_text, pick_text
    assert len(seen) == 3, "the pick's two rounds and the draft"   # call round, reply round, propose
    assert "probe: refused" in r.stdout + r.stderr, r.stdout + r.stderr
    accounts = list((tmp_path / "proposals" / "lead").glob("*.md"))
    assert len(accounts) == 1, accounts
    acc = accounts[0].read_text()
    assert "arm      tools" in acc and "C: ls board/" in acc, acc
    assert "picked   lander.md" in acc, acc
    assert list((tmp_path / "proposals").glob("*.md")), "the tools turn still drafts"
    # the flag with no door is refused before anything is sent
    r2, seen2 = lead("CARD: lander.md\nTASK: x\nWHY: y", board, tmp_path, TEND_LEAD_TOOLS="1")
    assert r2.returncode == 2 and "needs a door" in r2.stderr, r2.stderr
    assert seen2 == []


def test_a_handed_card_is_the_turns_input_and_the_mind_writes_the_task_not_the_pick(board, tmp_path):
    """--card (2026-09-04, Henri: "en antaisi kummankaan johtaa … asettelu
    voi olla pielessä"): the card is handed, as ask/ is handed a question.
    The ask carries that card's because whole and no other card's, the
    reply has no CARD line and the account says `given`; a card not on
    the shelf, and --seed with --card, are refused before anything is
    sent."""
    r, seen = lead("TASK: one line for the lamp\nWHY: w", board, tmp_path, TEND_LEAD_CARD="lander.md")
    assert r.returncode == 0, r.stdout + r.stderr
    sys_text = seen[0]["messages"][0]["content"]
    assert "a commit waits on a hand" in sys_text and "the cord needs a row" not in sys_text, sys_text
    assert "handed to you" in sys_text and "CARD:" not in sys_text, sys_text
    user_text = seen[0]["messages"][-1]["content"]
    assert "in hand" in user_text and "Pick." not in user_text, user_text   # the user line asks for the task, not the pick
    acc = next((tmp_path / "proposals" / "lead").glob("*.md")).read_text()
    assert "given    lander.md — by the person, not picked" in acc and "picked" not in acc.split("given")[0], acc
    assert list((tmp_path / "proposals").glob("*.md")), "the handed card still drafts"
    r2, seen2 = lead("TASK: x\nWHY: y", board, tmp_path, TEND_LEAD_CARD="nowhere.md")
    assert r2.returncode == 2 and "not on the open board" in r2.stderr, r2.stderr
    assert seen2 == []
    r3, seen3 = lead("TASK: x\nWHY: y", board, tmp_path, TEND_LEAD_CARD="lander.md", TEND_LEAD_TOOLS="1", TEND_LEAD_SEED="1")
    assert r3.returncode == 2 and "the card is the seed" in r3.stderr, r3.stderr
    assert seen3 == []


def test_a_task_that_echoes_the_prompts_placeholder_is_no_task(board, tmp_path):
    """2026-09-04 17:20: hy3 answered `TASK: the one small thing, in one
    line` — the ask's own placeholder — and the turn drafted a built
    thing.  The placeholder's words are no task: the cord is pulled."""
    r, seen = lead("CARD: lander.md\nTASK: The one small thing, in one line\nWHY: w", board, tmp_path)
    assert r.returncode == 0, r.stdout + r.stderr
    assert len(seen) == 1, "no draft was asked for"
    assert "andon:" in r.stdout and "no CARD/TASK shape" in r.stdout, r.stdout
    assert not list((tmp_path / "proposals").glob("*.md")), "nothing was drafted"


def test_a_seeded_tools_turn_carries_the_digest_and_the_tools_and_seed_alone_is_refused(board, tmp_path):
    """--seed (2026-09-04): compare.py's third arm on the node's loop — the
    digest in the ask AND the door's tools in the request, unkept here so
    the test is the request's shape and not keep's."""
    r, seen, _ = door_turn("CARD: lander.md\nTASK: one line\nWHY: w", board, tmp_path, stub=_tool_stub,
                           door_lines="tools  ls read\ncalls 4\n", TEND_LEAD_TOOLS="1", TEND_LEAD_SEED="1")
    assert r.returncode == 0, r.stdout + r.stderr
    first = seen[0]
    assert first.get("tools"), "the tools ride the seeded request"
    sys_text = "\n".join(m["content"] for m in first["messages"] if m["role"] == "system")
    assert "a commit waits on a hand" in sys_text, "the digest rides the seeded ask"
    acc = next((tmp_path / "proposals" / "lead").glob("*.md")).read_text()
    assert "arm      tools, seeded" in acc and "C: ls board/" in acc, acc
    r2, seen2 = lead("CARD: lander.md\nTASK: x\nWHY: y", board, tmp_path, TEND_LEAD_SEED="1")
    assert r2.returncode == 2 and "needs --tools" in r2.stderr, r2.stderr
    assert seen2 == []


@pytest.mark.skipif(_landlock_abi() < 4 or not Path("/usr/bin/python3").exists(),
                    reason="the kept turn needs Landlock ABI 4 and a system python3 for keep")
def test_a_kept_turn_through_a_loopback_door_runs_under_keep_and_one_that_calls_out_is_refused(board, tmp_path):
    """card:session-program.md, Henri 2026-09-02: "in practice the commands
    should probably be possible to run kept by the model's decision.  It's
    the mechanism to limit blast radius".  A door at 127.0.0.1 is a node at
    its own port, which keep's one --connect reaches: the turn runs under
    keep, both asks go through the door, the board stays unwritable.  A
    door that calls out is refused under --kept before anything is sent."""
    r, seen, _ = door_turn("CARD: lander.md\nTASK: one line\nWHY: w", board, tmp_path,
                           TEND_LEAD_KEPT="1", TEND_KEPT_PROBE=str(board / "lander.md"))
    assert r.returncode == 0, r.stdout + r.stderr
    assert len(seen) == 2, "the pick and the draft both went through the loopback door, under keep"
    assert "probe: refused" in r.stdout + r.stderr, r.stdout + r.stderr
    assert list((tmp_path / "proposals").glob("*.md")), "the kept door turn still drafts"
    assert (board / "lander.md").read_text().startswith("# lander"), "the board is untouched under keep"
    # the same turn through a door that calls out: refused, nothing sent
    out = tmp_path / "doors2" / "outward"; out.mkdir(parents=True)
    key = tmp_path / "keys" / "openrouter.key"
    (out / "door").write_text(f"url  http://door.invalid/v1/chat/completions\nmodel  vendor/some-model\nkey  {key}\n"
                              "admitted  the test, for the refusal\n")
    env = {"PATH": "/usr/bin:/bin", "HOME": str(tmp_path), "TEND_DOOR_DIR": str(tmp_path / "doors2"),
           "TEND_DOOR": "outward", "TEND_LEAD_KEPT": "1", "TEND_PROPOSAL_DIR": str(tmp_path / "proposals2"),
           "TEND_ANDON_STATE": str(tmp_path / "andon"), "TEND_BOARD_DIR": str(board),
           "TEND_STATE_DIR": str(tmp_path / "state")}
    r2 = subprocess.run(["sh", str(LEAD), str(NODE)], capture_output=True, text=True, env=env, timeout=60)
    assert r2.returncode != 0 and "calls out" in r2.stderr, r2.stdout + r2.stderr
    assert not (tmp_path / "proposals2").exists(), "nothing was drafted through the outward door"


def test_a_door_key_others_can_read_is_refused_before_anything_is_sent(board, tmp_path):
    r, seen, _ = door_turn("CARD: lander.md\nTASK: x\nWHY: y", board, tmp_path, key_mode=0o644)
    assert r.returncode == 2 and "readable by others" in r.stderr, r.stderr
    assert seen == []


def test_a_door_key_inside_the_tree_is_refused(board, tmp_path):
    r, seen, _ = door_turn("CARD: lander.md\nTASK: x\nWHY: y", board, tmp_path, key_path=ROOT / "doors" / "no-such.key")
    assert r.returncode == 2 and "inside the tree" in r.stderr, r.stderr
    assert seen == []


def test_a_door_that_does_not_exist_is_refused(board, tmp_path):
    r, seen, _ = door_turn("CARD: lander.md\nTASK: x\nWHY: y", board, tmp_path, door="nowhere")
    assert r.returncode == 2 and "no door named nowhere" in r.stderr, r.stderr
    assert seen == []


def test_the_trees_own_doors_read_and_name_a_key_outside_the_tree():
    """Every door checked into doors/ parses, names a key under the person's
    home and not the tree, and says who admitted it (card:model-acceptance.md)."""
    doors = sorted((ROOT / "doors").glob("*/door"))
    assert doors, "doors/ carries at least one door"
    for d in doors:
        text = d.read_text()
        fields = dict(line.split("  ", 1) for line in text.splitlines() if "  " in line and not line.startswith("#"))
        # a key crosses the wire, so https — except the node's own loopback
        # port, which checks no key and is the one door where http is the
        # honest scheme (doors/llm, 2026-09-02, card:session-program.md)
        url = fields["url"]
        assert url.startswith("https://") or url.startswith("http://127.0.0.1:"), \
            f"{d}: https, or http to 127.0.0.1 only"
        assert fields["model"], d
        assert fields["key"].startswith("~/"), f"{d}: the key lives under the person's home, never the tree"
        assert "admitted" in fields, f"{d}: a door says who admitted the model"


# ── F008: the digest's cap is a gate, and a gate says what it stopped ────
# 2026-08-31 the digest was cut at 5000 bytes by `head -c` with nothing
# said, carrying 9 of 13 open cards and dropping the priority-1 one; the
# node had never seen its last cards.  Henri picked shapes (d) and (a) on
# 2026-09-01: a cap sized to the window the node actually has, and a cut
# that names every card it dropped.

def _node_ctx_tokens():
    """the `-c N` on llm/grant's program line — the window the digest is for."""
    m = re.search(r"^program .*?-c[ =]+([0-9]+)", (NODE / "grant").read_text(), re.M)
    assert m, "llm/grant's program line names its context with -c"
    return int(m.group(1))


def _default_ctxchars():
    m = re.search(r'ctxchars="\$\{TEND_CTXCHARS:-([0-9]+)\}"', LEAD.read_text())
    assert m, "lead.sh names its digest cap as a default"
    return int(m.group(1))


def test_the_whole_open_board_reaches_the_model(tmp_path):
    """(d).  Every card on the *real* open shelf is in the prompt — the cap
    is sized to the board and the window, not to a number left behind by an
    older one.  Goes red the day the board outgrows the cap, which is the
    day someone must choose again."""
    real = ROOT / "board"
    r, seen = lead("ANDON: which is mine?", real, tmp_path)
    assert r.returncode == 0, r.stdout + r.stderr
    prompt = seen[0]["messages"][0]["content"]
    cards = sorted(p.name for p in real.glob("*.md") if p.name != "README.md")
    missing = [c for c in cards if f"=== {c} ===" not in prompt]
    assert not missing, f"the digest dropped {len(missing)} of {len(cards)} open cards: {missing}"
    assert "did not fit" not in prompt, "nothing was dropped, so nothing is announced"


def test_a_cap_too_small_drops_whole_cards_and_names_every_one(board, tmp_path):
    """(a).  A cut card is not a shortened card — it is a card that does not
    exist for the mind being asked to choose.  So the cut falls on a card
    boundary and the digest says which cards are missing, the way readchars
    says where it cut."""
    r, seen = lead("ANDON: x", board, tmp_path, TEND_CTXCHARS="120")
    assert r.returncode == 0, r.stdout + r.stderr
    prompt = seen[0]["messages"][0]["content"]
    assert "lander.md" in prompt, "the cards that fit are whole"
    assert "1 card did not fit: silent-cord.md" in prompt, \
        f"the cut names what it dropped; prompt tail was: {prompt[-300:]!r}"
    assert "=== silent-cord.md ===" not in prompt, "a dropped card is dropped whole, not half"


def test_the_cap_fits_the_window_the_node_actually_has(tmp_path):
    """F008's cause, gated: TEND_CTXCHARS was 5000 for a node at `-c 2048`
    and stayed 5000 when 37092d7 took the node to 8192 — a number that fitted
    one mechanism and was silently wrong for the next.  This binds the two:
    the digest, the prompt's framing and the reply must fit the node's own
    window, at a deliberately pessimistic 3 characters per token."""
    ctx = _node_ctx_tokens()
    chars = _default_ctxchars()
    reply, framing = 160, 700 // 3
    assert chars / 3 + reply + framing < ctx, (
        f"the digest cap ({chars} chars) does not fit the node's -c {ctx}: "
        f"{chars / 3:.0f} + {reply} + {framing} tokens")
    assert chars > 12000, (
        f"the cap is {chars}: a window of {ctx} tokens holds far more board "
        "than that, and a cap well under the window is how F008 happened")


def test_a_because_cut_at_eight_lines_says_how_many_it_left(tmp_path):
    """F009.  The eight-line keep is a *summary* of the `because`, and until
    2026-09-01 it was an unmarked one: 9 of the 13 open cards ended
    mid-sentence with nothing said.  A `because` that stops mid-sentence
    names a smaller problem than the card's, and the mind has no way to
    know."""
    b = tmp_path / "board"; b.mkdir()
    (b / "README.md").write_text("# board\n")
    long_because = "\n".join(f"             line {i}" for i in range(2, 14))
    (b / "big.md").write_text(
        "# big — a long problem\n\n    status   open\n"
        f"    because  line 1\n{long_because}\n    asked    Henri\n")
    (b / "small.md").write_text(
        "# small — a short one\n\n    status   open\n    because  one line\n    asked    Henri\n")
    r, seen = lead("ANDON: x", b, tmp_path)
    assert r.returncode == 0, r.stdout + r.stderr
    prompt = seen[0]["messages"][0]["content"]
    # 13 because-lines + the title = 14 kept lines, 8 shown, 6 left
    assert "[… 6 more lines of this because" in prompt, \
        f"the cut says how many it left; got: {prompt[-400:]!r}"
    assert "line 7" in prompt and "line 9" not in prompt, "eight lines are still eight"
    assert "small.md" in prompt and "more lines of this because" not in prompt.split("=== small.md ===")[1], \
        "a because that fits is not marked"
