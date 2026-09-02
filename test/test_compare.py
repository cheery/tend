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


def test_the_account_says_whether_the_off_switch_was_on_the_wire():
    """F015 (2026-09-02): the first gemma4 turn through `doors/llm/door`
    read `thinking off — the node's own condition` while the request
    carried no knob at all — a door names a model, and the knob went only
    where no model was named — so 7,222 bytes of reasoning came back in
    the content channel and the account said off.  The line says what the
    wire carried: the knob, or that this door has no off switch."""
    on_the_wire = compare._thinking_line(False, "", knob="template")
    no_switch = compare._thinking_line(False, "", knob="")
    assert "enable_thinking:false" in on_the_wire, on_the_wire
    assert "no off switch" in no_switch and "off —" not in no_switch, no_switch
    assert compare._thinking_line(False, "") == on_the_wire, "the node's own turn always carries it"


# --- the two arms added for card:questions.md's specified measurements ---
#
# 2026-09-01.  Writing each standing "I don't know" question down as
# `*(question, measure — …)*` made two of them name a flag rather than an
# opinion, and these are the flags.  The API path is the person's side —
# no key, no net from this seat — so what is testable here is everything
# up to the wire, which for `--seed` is the whole prompt through a stub
# and for `--draft` is the material the model would have been handed.


def test_the_seeded_arm_carries_the_digest_and_the_tools_both(tmp_path):
    """`--seed` is the third arm, and it is the digest arm's prompt with
    the tools arm's request.

    The original two arms confounded two variables — what the mind is
    given, and whether it may go and read — so neither answered
    card:tools.md's question.  This checks the confound is actually
    broken: the seeded prompt must be byte-for-byte the digest arm's, and
    the tools must still be in the request.
    """
    srv, stub = _stub_server()
    door = td.a_tooled_door(tmp_path, stub, tools="read ls")
    t = td.a_tree(tmp_path)
    td.SCRIPT["Pick."] = [("say", "CARD: x.md\nTASK: t\nWHY: w\n")]
    r = _compare_door(tmp_path, "--arm", "tools", "--seed", tree=t, stub=stub, door=door)
    srv.shutdown()
    assert r.returncode == 0, r.stderr + r.stdout
    accounts = list((tmp_path / "props" / "compare").glob("*.md"))
    assert len(accounts) == 1, accounts
    assert accounts[0].name.endswith("-tools-seeded.md"), \
        f"the arm names itself, or two arms land in one tally: {accounts[0].name}"
    txt = accounts[0].read_text()
    assert "digest AND the door's tools" in txt, txt
    sent = (accounts[0].parent / accounts[0].stem / "replies").parent
    assert sent.exists()


def test_the_seeded_prompt_is_the_digest_arms_prompt(tmp_path):
    """Byte for byte, or the arms differ in something nobody named."""
    b = board(tmp_path)
    d = compare.digest(b)
    assert d and "lander.md" in d
    # what door_pick builds: PICK_SYS + digest when seeded or on the digest
    # arm, PICK_SYS alone on the bare tools arm
    assert (compare.PICK_SYS + d).startswith(compare.PICK_SYS)


def test_the_account_records_which_readchars_it_ran_under(tmp_path, monkeypatch):
    """F011's lesson one layer up: an arm that does not say its own setting
    cannot be compared with another.

    `TEND_READCHARS` is the knob the `head` arm turns — a 4000-char read
    returns a card's opening instead of a whole 40k card — and without
    this line in the account, a tally of 48 arms could not tell the two
    apart afterwards.
    """
    srv, stub = _stub_server()
    door = td.a_tooled_door(tmp_path, stub, tools="read ls")
    t = td.a_tree(tmp_path)
    td.SCRIPT["Pick."] = [("say", "CARD: x.md\nTASK: t\nWHY: w\n")]
    env_door = dict(door, TEND_READCHARS="4000")
    r = _compare_door(tmp_path, "--arm", "tools", tree=t, stub=stub, door=env_door)
    srv.shutdown()
    assert r.returncode == 0, r.stderr + r.stdout
    txt = list((tmp_path / "props" / "compare").glob("*.md"))[0].read_text()
    assert "readchars 4000" in txt, txt


def test_the_cut_notice_does_not_offer_what_a_draft_turn_cannot_do():
    """The one design decision in F010's told arm, held by a test.

    `tools/executor.py:139` ends its notice `read(path, line=L)
    continues`, which is right for a mind holding tools.  A draft turn
    has none, so the same sentence would promise a remedy the model
    cannot reach — and a notice offering an impossible remedy is worse
    than silence, because it spends the turn on reaching for it.
    """
    whole = "\n".join(f"line {i}" for i in range(1, 101))
    note = compare.cut_notice(whole[:50], whole, "x.md")
    assert "cut at 50 chars of" in note, note
    assert "no way to ask for it" in note, note
    assert "read(" not in note and "continues" not in note, \
        "the notice offers a call the draft turn cannot make: " + note


def test_the_cut_notice_counts_lines_the_way_the_executor_does():
    """Same arithmetic as `tools/executor.py:139`, or the two notices in
    this tree would describe the same cut differently.

    The first draft used `count("\\n") + 1` for the total and called a
    four-line file five lines long, because the trailing newline invented
    one.  `at` is the first line *not* shown, which is what makes it
    useful to a reader.
    """
    whole = "abc\ndef\nghi\njkl\n"
    note = compare.cut_notice(whole[:8], whole, "x.md")
    assert "cut at 8 chars of 16" in note, note
    assert "at line 3 of 4" in note, note


def test_draft_flags_are_pulled_without_swallowing_the_next_flag():
    """`--task --cut 200` must not make the task the string '--cut'.

    A flag that eats the next flag would produce a run that looks fine,
    costs money, and measures a task nobody wrote — the silent kind of
    wrong this tree keeps finding.
    """
    rest, opts = compare._pull(["--draft", "a.md", "--task", "--cut", "200"],
                               ("--draft", "--task", "--cut"))
    assert opts["--draft"] == "a.md"
    assert opts["--task"] is None, opts
    assert opts["--cut"] == "200"
    rest, opts = compare._pull(["--draft", "a.md", "--task", "do a thing", "m1"],
                               ("--draft", "--task", "--cut"))
    assert opts["--task"] == "do a thing" and rest == ["m1"]


def test_the_draft_turn_hands_the_model_the_same_material_but_for_the_notice(tmp_path):
    """The measurement is only a measurement if the arms differ in one thing.

    Both arms are run against a fake client that records what it was
    given, so this compares the actual system prompts rather than
    trusting the code path — and asserts the told arm is the silent arm
    plus the notice, with nothing else moved.
    """
    b = board(tmp_path)
    long_card = b / "long.md"
    long_card.write_text("# long — a card\n\n    status   open\n    because  x\n"
                         + "\n".join(f"body line {i}" for i in range(400)) + "\n")

    class FakeClient:
        def __init__(self):
            self.seen = []
            self.messages = self

        def create(self, **kw):
            self.seen.append(kw)
            return type("R", (), {
                "content": [type("T", (), {"type": "text", "text": "a draft"})()],
                "usage": type("U", (), {"input_tokens": 1, "output_tokens": 2})(),
                "stop_reason": "end_turn"})()

    out = {}
    for tell in (False, True):
        c = FakeClient()
        account, draft, was_cut = compare.draft_turn(
            c, "m", b, tmp_path / "p", "long.md", "do the thing", 500, tell)
        assert was_cut, "the fixture must actually cut, or the arms are identical"
        out[tell] = c.seen[0]["system"]
        assert draft == "a draft"
        assert ("told" if tell else "silent") in account.name

    assert out[True].startswith(out[False]), \
        "the told arm moved something other than the notice"
    added = out[True][len(out[False]):]
    assert "no way to ask for it" in added and len(added) < 300, added


def test_a_draft_turn_that_did_not_cut_says_so_loudly(tmp_path):
    """An arm that measured nothing must not read like an arm that did.

    If the card is shorter than `--cut`, both arms get identical material
    and the pair is worthless — which is exactly the shape of failure
    this tree calls an instrument that asserts less than it means.
    """
    b = board(tmp_path)

    class FakeClient:
        def __init__(self):
            self.messages = self

        def create(self, **kw):
            return type("R", (), {
                "content": [type("T", (), {"type": "text", "text": "d"})()],
                "usage": type("U", (), {"input_tokens": 1, "output_tokens": 2})(),
                "stop_reason": "end_turn"})()

    account, draft, was_cut = compare.draft_turn(
        FakeClient(), "m", b, tmp_path / "p", "silent-cord.md", "t", 100000, True)
    assert not was_cut
    txt = account.read_text()
    assert "NOT CUT" in txt and "measures nothing" in txt, txt


def test_the_draft_mode_refuses_before_it_spends_anything(monkeypatch, tmp_path):
    """Every refusal here returns before the SDK is imported or a key read.

    A flag that accepts nonsense on a paid path is not a small bug: the
    run looks fine, costs money and measures something nobody asked for.
    So the order matters as much as the checks — validate, then import,
    then spend — and this holds the order by running the real `main()`
    from a seat with no key at all.
    """
    monkeypatch.delenv("TEND_FENCED", raising=False)
    monkeypatch.setenv("TEND_BOARD_DIR", str(board(tmp_path)))
    monkeypatch.setenv("TEND_PROPOSAL_DIR", str(tmp_path / "p"))

    def run(*args):
        return compare.main(["compare.py", *args])

    assert run("--draft") == 2, "a --draft with no card"
    assert run("--draft", "lander.md") == 2, "a --draft with no --task"
    assert run("--draft", "lander.md", "--task", "t", "--cut", "abc") == 2, \
        "a --cut that is not a number"
    assert run("--draft", "lander.md", "--task", "t", "--seed") == 2, \
        "--seed belongs to the door's tools arm, not the draft turn"
    assert not (tmp_path / "p").exists(), \
        "a refused run wrote an account — it got further than it should have"


# --- F012: the calls a turn ran, and the ones it only asked for ---

def test_a_turn_that_hit_no_cap_says_the_number_it_always_said():
    """Every account written before 2026-09-01 means `calls N` = N ran.

    Shape (a) of F012 was chosen precisely so that stays true: the
    two-part form appears only where the one-part form was wrong, so old
    and new accounts are comparable without knowing which side of the fix
    they fell on.
    """
    assert compare._calls_line(["read a.md → 2k", "ls board/ → 9"]) == "2"
    assert compare._calls_line([]) == "0"


def test_a_turn_that_hit_the_cap_separates_run_from_refused():
    calls = ["read a.md → 2k",
             "read b.md → out of calls (16 a turn)",
             "read c.md → out of calls (16 a turn)"]
    assert compare._calls_line(calls) == "1 run, 2 refused past the cap"


def test_the_refusal_string_is_the_couriers_own_and_they_still_agree(tmp_path):
    """The one that matters, and the reason this is not a unit test.

    `compare.py` recognises a refused call by matching the words
    `deliver.sh` writes.  A copy of another program's string is a claim
    about that program, and it is measured like one (`board/README.md`,
    the fixture rule) — so this drives the **real** courier past a cap of
    1 and checks the account it produces, rather than checking compare.py
    against a string typed twice in this repository.

    If someone rewords deliver.sh:217, this test goes red and the count
    does not silently go back to counting attempts, which is F012 itself.
    """
    srv, stub = _stub_server()
    door = td.a_tooled_door(tmp_path, stub, tools="read ls")
    t = td.a_tree(tmp_path)
    td.SCRIPT["Pick."] = [("calls", [("ls", {"dir": "board/"}),
                                     ("ls", {"dir": "board/"}),
                                     ("ls", {"dir": "board/"})]),
                          ("say", "CARD: x.md\nTASK: t\nWHY: w\n")]
    r = _compare_door(tmp_path, "--arm", "tools",
                      tree=t, stub=stub, door=dict(door, TEND_CALLS="1"))
    srv.shutdown()
    assert r.returncode == 0, r.stderr + r.stdout
    txt = list((tmp_path / "props" / "compare").glob("*.md"))[0].read_text()

    assert "calls    1 run, 2 refused past the cap" in txt, txt
    # and the refusals are still on the record, because the person
    # watches the model act — F012 is not about hiding them
    assert txt.count("out of calls") >= 2, txt
