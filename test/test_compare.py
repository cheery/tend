"""tools/compare.py — the led turn's two prompts, put to a Claude model (card:session-program.md, 2026-08-28 18:30).

Henri: "I have anthropic api key here.. you could try how sonnet or opus
fares in the task you've given to the local llm."  The seat cannot run
it (no key, no net inside the fence), so the tool runs on the person's
side; what is tested here is that it builds the same digest lead.sh
builds and reads a reply the same way — the comparison is only a
comparison if the inputs are the node's.
"""
import http.server
import importlib.util
import subprocess
import sys
import threading
from pathlib import Path

import test_deliver as td

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("compare", ROOT / "tools" / "compare.py")
compare = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(compare)


def board(tmp_path):
    b = tmp_path / "board"; b.mkdir(); (b / "done").mkdir()
    (b / "README.md").write_text("# board\n")
    (b / "lander.md").write_text("# lander — a change waits\n\n    status   open\n    because  a commit waits on a hand\n             and nobody carries it\n    asked    Henri\n\nbody\n")
    (b / "silent-cord.md").write_text("# silent-cord — quiet\n\n    status   open\n    because  the cord needs a row\n    asked    Henri\n")
    (b / "done" / "grant.md").write_text("# grant\n\n    status   done\n    because  x\n    asked    Henri\n")
    return b


def test_the_digest_is_the_open_shelfs_title_and_because_never_done(tmp_path):
    d = compare.digest(board(tmp_path))
    assert "=== lander.md ===" in d and "# lander — a change waits" in d
    assert "a commit waits on a hand" in d and "and nobody carries it" in d
    assert "asked" not in d and "grant" not in d and "README" not in d


def test_a_reply_is_read_by_the_filename_the_shelf_judges(tmp_path):
    b = board(tmp_path)
    got = compare.read_reply("CARD: `lander.md` ===\nTASK: one line\nWHY: because\n", b)
    assert got["card"] == "lander.md" and got["task"] == "one line" and got["andon"] == ""
    got = compare.read_reply("CARD: unicorn.md\nTASK: x\nWHY: y\n", b)
    assert got["card"] == "" and "unicorn.md" in got["andon"]
    got = compare.read_reply("ANDON: which?\n", b)
    assert got["andon"] == "which?"


# --- the door pair (card:tools.md's owed measurement, 2026-08-31) ---

def _stub_server():
    srv = http.server.HTTPServer(("127.0.0.1", 0), td._Stub)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{srv.server_address[1]}"
    return srv, {"TEND_LLM_URL": base + "/v1/chat/completions", "TEND_LLM_HEALTH": base + "/health"}


def _compare_door(tmp_path, *args, tree, stub, door):
    env = {"PATH": "/usr/bin:/bin", "TEND_TREE": str(tree), "TEND_BOARD_DIR": str(tree / "board"),
           "TEND_PROPOSAL_DIR": str(tmp_path / "props"), **stub, **door}
    return subprocess.run([sys.executable, str(ROOT / "tools" / "compare.py"), "--door", door["TEND_DOOR"], *args],
                          capture_output=True, text=True, env=env)


def test_the_door_pair_runs_digest_then_tools_on_the_same_courier(tmp_path):
    """--door runs the pick twice through tools/deliver.sh: the digest arm,
    the pick prompt with lead.sh's digest and TEND_TOOLS empty; the
    tools arm, the pick prompt bare and the door's own tools line, under
    the courier's seat.  Each account names its arm and the pick, both
    under the gitignored proposals dir."""
    srv, stub = _stub_server()
    door = td.a_tooled_door(tmp_path, stub, tools="read ls")
    t = td.a_tree(tmp_path)
    td.SCRIPT["Pick."] = [("say", "CARD: x.md\nTASK: cite the card\nWHY: it is there\n")]
    n0 = len(td.BODIES)
    r = _compare_door(tmp_path, tree=t, stub=stub, door=door)
    srv.shutdown()
    assert r.returncode == 0, r.stderr + r.stdout
    dig, tl = td.BODIES[n0:]
    assert "tools" not in dig and dig["messages"][0]["role"] == "system" and "=== x.md ===" in dig["messages"][0]["content"]
    assert dig["messages"][-1] == {"role": "user", "content": "Pick."}
    assert [x["function"]["name"] for x in tl["tools"]] == ["read", "ls"], "the tools arm carries the door's own line"
    assert "=== " not in tl["messages"][1]["content"], "no digest rides the tools arm"
    assert "read ls" in tl["messages"][0]["content"], "the courier's seat line, as any talk turn"
    accounts = sorted((tmp_path / "props" / "compare").glob("*.md"))
    assert [a.name.rsplit("-", 1)[1] for a in accounts] == ["digest.md", "tools.md"]
    for a in accounts:
        assert "picked   x.md" in a.read_text() and "cite the card" in a.read_text()
    assert "openrouter digest: picked x.md — cite the card" in r.stdout
    assert "openrouter tools: picked x.md — cite the card" in r.stdout


def test_the_tools_arms_account_carries_the_couriers_c_lines(tmp_path):
    srv, stub = _stub_server()
    door = td.a_tooled_door(tmp_path, stub, tools="read ls")
    t = td.a_tree(tmp_path)
    td.SCRIPT["Pick."] = [("calls", [("ls", {"dir": "board/"})]),
                          ("say", "CARD: x.md\nTASK: the shelf is README.md and x.md\nWHY: I looked\n")]
    r = _compare_door(tmp_path, "--arm", "tools", tree=t, stub=stub, door=door)
    srv.shutdown()
    assert r.returncode == 0, r.stderr + r.stdout
    accounts = list((tmp_path / "props" / "compare").glob("*.md"))
    assert len(accounts) == 1 and accounts[0].name.endswith("-tools.md"), "--arm runs one arm alone"
    txt = accounts[0].read_text()
    assert "C: ls board/ → 2 entries" in txt and "calls    1" in txt, txt
    assert (accounts[0].parent / accounts[0].stem / "replies").exists(), "the raw exchange stays beside the account"


def test_a_door_with_no_tools_line_refuses_the_pair_and_says_the_line_to_write(tmp_path):
    door = td.a_door(tmp_path, {"TEND_LLM_URL": "http://127.0.0.1:9/x"}, name="bare")
    t = td.a_tree(tmp_path)
    r = _compare_door(tmp_path, tree=t, stub={}, door=door)
    assert r.returncode == 2 and "no tools line" in r.stderr, r.stderr
    assert not (tmp_path / "props").exists(), "refused before any ask"


def test_the_two_digests_are_the_same_digest_byte_for_byte(tmp_path):
    """The docstring above says compare.py "builds the same digest lead.sh
    builds", and until 2026-09-01 nothing checked it — two copies of one
    mechanism with no gate between them, which is F008's own shape (a number
    that fitted one mechanism and was silently wrong for the next).  Both
    ends of the F008 fix live in both files, so this runs the real lead.sh
    against a stub and compares what actually reached the model, whole and
    cut."""
    import test_lead as tl
    b = board(tmp_path)
    default = compare.DIGEST_CHARS   # restored below: the module's own, never a number typed here
    try:
        for cap in (None, "120"):
            extra = {} if cap is None else {"TEND_CTXCHARS": cap}
            r, seen = tl.lead("ANDON: x", b, tmp_path / f"run{cap}", **extra)
            assert r.returncode == 0, r.stdout + r.stderr
            prompt = seen[0]["messages"][0]["content"]
            if cap is not None:
                compare.DIGEST_CHARS = int(cap)
            want = compare.digest(b)
            assert prompt.endswith(want), (
                f"cap={cap}: the two digests have drifted\n"
                f"lead.sh tail: {prompt[-400:]!r}\ncompare.py:   {want[-400:]!r}")
    finally:
        compare.DIGEST_CHARS = default


# ── F011: record what came back, never what was asked for ───────────────
# 2026-09-01: nine arms through the openrouter door with `--thinking`
# across three models, and every account said `thinking on` — including
# the five whose reasoning channel was empty.  The account recorded the
# flag.  And the presence of a reasoning channel predicted whether the
# turn produced a pick **nine times out of nine**, so the account was
# hiding the one fact that has explained anything about the turn it
# describes.

def test_the_record_carries_the_thinking_that_came_back():
    with_t = ("2026-09-01 07:30 Q: Pick.\n"
              "2026-09-01 07:30 V: openrouter tencent/hy3\n"
              "2026-09-01 07:30 T: I should look at the board.\nand keep thinking.\n"
              "2026-09-01 07:30 A: CARD: flake.md\nTASK: x\n")
    model, calls, reply, thought = compare._parse_replies(with_t)
    assert "look at the board" in thought and "keep thinking" in thought, \
        "a multi-line reasoning channel is carried whole"
    assert reply.startswith("CARD: flake.md"), "and it is not mistaken for the answer"
    assert "keep thinking" not in reply, "nor leaked into it"

    without_t = ("2026-09-01 07:30 Q: Pick.\n"
                 "2026-09-01 07:30 V: openrouter qwen/qwen3.8-max\n"
                 "2026-09-01 07:30 A: Let me look at the board.\n")
    _, _, reply2, thought2 = compare._parse_replies(without_t)
    assert thought2 == "", "no reasoning channel is an empty one, not a missing field"
    assert reply2.startswith("Let me look")


def test_the_account_says_what_came_back_not_what_was_asked_for():
    """F011's whole point.  `thinking on` was true of the request and false
    of the turn, and a reader comparing a thinking run against a
    non-thinking one had no way to tell the two apart."""
    asked_and_got = compare._thinking_line(True, "some reasoning")
    asked_and_none = compare._thinking_line(True, "")
    not_asked = compare._thinking_line(False, "")
    assert "came back" in asked_and_got
    assert "NO reasoning" in asked_and_none, asked_and_none
    assert asked_and_none != asked_and_got, "the two turns must not read the same"
    assert "off" in not_asked and "NO reasoning" not in not_asked, \
        "a turn that never asked is not a turn that asked and got nothing"
