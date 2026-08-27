"""tools/limit.sh — the sitting, and the direction it may not run in.

Moved into tend with the script on 2026-08-24 (`card:cords.md`); the
tests are gestate's `test/test_limit.py`, carried whole, because the
property they hold did not change by moving: **a session may end a
sitting and may never extend one.**  That is not a promise anybody can
keep by intending to, so it is checked here — and checked *here* rather
than in gestate, because the copy that will hold the hook is this one.

Two of these are regressions gestate paid for.  The session there found
both by running the thing end to end, and `bash -n` passed on both:

* a session-closed sitting printed *"The 0 minutes are up"* instead of
  its reason, because a patch missed on indentation;
* the hook's state write dropped the reason field, so the *why* survived
  one read and vanished on the next prompt.

Nothing here touches the live sitting: `XDG_RUNTIME_DIR` and
`GESTATE_LIMIT_LOG` are pointed at a temporary directory.
"""

import json
import os
import pathlib
import subprocess
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
LIMIT = ROOT / "tools/limit.sh"


class Desk:
    """One temporary desk: its own state file, its own log."""

    def __init__(self, tmp_path, claudecode=True):
        self.tmp = tmp_path
        self.log = tmp_path / "sittings.log"
        self.env = dict(os.environ,
                        XDG_RUNTIME_DIR=str(tmp_path),
                        GESTATE_LIMIT_LOG=str(self.log))
        if claudecode:
            self.env["CLAUDECODE"] = "1"
        else:
            self.env.pop("CLAUDECODE", None)
        self.state = tmp_path / f"gestate-sitting-{os.getuid()}"

    def run(self, *args, prompt=None):
        stdin = json.dumps({"prompt": prompt}) if prompt is not None else ""
        return subprocess.run(["bash", str(LIMIT), *args], env=self.env,
                              input=stdin, capture_output=True, text=True)

    def prompt(self, text):
        return self.run("--hook", prompt=text)

    def rewind(self, minutes):
        """Move this sitting's start back, so the limit can be reached
        without waiting for it."""
        started, last, limit, *why = self.state.read_text().split()
        started = int(started) - minutes * 60
        self.state.write_text(" ".join([str(started), last, limit, *why]) + "\n")

    def lines(self):
        return [l.split("\t") for l in self.log.read_text().splitlines()] \
            if self.log.exists() else []


def test_the_hook_run_by_hand_records_nothing(tmp_path):
    """**Tend's own regression, 2026-08-24.**  A session ran `--hook`
    with an empty stdin to check a path and wrote a row into the real
    log.  Without the harness's JSON there is no prompt, so there is
    nothing to record — and the desk's clock is not touched."""
    desk = Desk(tmp_path)
    r = desk.run("--hook")                       # empty stdin
    assert r.returncode == 0
    assert "nothing recorded" in r.stderr
    assert not desk.state.exists()
    assert desk.lines() == []


def test_a_session_may_not_grant_itself_a_sitting(tmp_path):
    """The asymmetry, in the direction that matters.  `CLAUDECODE` is set
    for Henri's own `!` commands too, so this refuses him as well — which
    is why the real grant is a typed prompt and not this."""
    desk = Desk(tmp_path)
    r = desk.run("reset")
    assert r.returncode == 3
    assert "not granted from inside a session" in r.stderr
    assert not desk.state.exists()


def test_a_real_terminal_may(tmp_path):
    desk = Desk(tmp_path, claudecode=False)
    assert desk.run("reset").returncode == 0
    assert desk.state.exists()


def test_the_typed_word_grants_and_never_reaches_the_session(tmp_path):
    """Exit 2 on UserPromptSubmit discards the prompt.  `sitting 45` is a
    control word, so the session must never see it as a question."""
    desk = Desk(tmp_path)
    r = desk.prompt("sitting 45")
    assert r.returncode == 2
    assert "45 minutes" in r.stderr
    assert desk.state.read_text().split()[2] == "45"


def test_the_bare_word_is_the_short_default(tmp_path):
    desk = Desk(tmp_path)
    assert desk.prompt("sitting").returncode == 2
    assert desk.state.read_text().split()[2] == "15"


def test_a_question_that_merely_mentions_it_is_not_a_grant(tmp_path):
    """The regex is anchored on purpose.  If asking *about* the
    instrument extended the sitting, the instrument would be a
    formality — and a session can put those words in his mouth by
    quoting them back."""
    desk = Desk(tmp_path)
    desk.prompt("sitting 45")
    desk.rewind(60)
    r = desk.prompt("what does `sitting 90` do?")
    assert r.returncode == 2
    assert "minutes are up" in r.stderr


def test_a_prompt_inside_the_limit_passes(tmp_path):
    desk = Desk(tmp_path)
    desk.prompt("sitting 45")
    assert desk.prompt("a real question").returncode == 0


def test_a_prompt_past_the_limit_is_blocked(tmp_path):
    desk = Desk(tmp_path)
    desk.prompt("sitting 20")
    desk.rewind(21)
    r = desk.prompt("one more thing")
    assert r.returncode == 2
    assert "The 20 minutes are up" in r.stderr
    assert "sitting 45" in r.stderr, "the way back in has to be in the message"


def test_a_session_may_end_one(tmp_path):
    """The other direction, which is open."""
    desk = Desk(tmp_path)
    desk.prompt("sitting 45")
    assert desk.run("stop", "the thing you came for is done").returncode == 0
    assert desk.prompt("something else").returncode == 2


def test_a_closed_sitting_says_why_and_not_zero_minutes(tmp_path):
    """Regression, defect one.  The closed branch never fired, so a
    session-closed sitting reported *"The 0 minutes are up"* — true, and
    useless, and it hid the one thing the close was for."""
    desk = Desk(tmp_path)
    desk.prompt("sitting 45")
    desk.run("stop", "the export bug is fixed")
    r = desk.prompt("next")
    assert "the export bug is fixed" in r.stderr
    assert "0 minutes are up" not in r.stderr


def test_the_reason_survives_more_than_one_read(tmp_path):
    """Regression, defect two.  The hook's state write dropped the reason
    field, so the *why* was there on the first blocked prompt and gone on
    the second — the worst shape for a message whose whole job is to be
    read by somebody who came back."""
    desk = Desk(tmp_path)
    desk.prompt("sitting 45")
    desk.run("stop", "the export bug is fixed")
    desk.prompt("next")
    r = desk.prompt("and again")
    assert "the export bug is fixed" in r.stderr


def test_the_log_records_the_events_and_never_the_prompt(tmp_path):
    """The privacy claim, checked rather than promised.  The log exists
    to settle GESTATE_LIMIT_GAP; it is kept outside the repo, and what a
    person typed is not what it is for."""
    desk = Desk(tmp_path)
    desk.prompt("sitting 45")
    desk.prompt("a private question about something")
    desk.rewind(60)
    desk.prompt("blocked now")
    desk.run("stop", "done")

    events = [row[1] for row in desk.lines()]
    assert events == ["grant", "prompt", "block", "close"]
    body = desk.log.read_text()
    assert "a private question" not in body
    assert "blocked now" not in body


def test_a_gap_of_silence_starts_a_fresh_sitting(tmp_path):
    """The shape of the actual problem: logging in for one small thing.
    The number this uses is the one `tools/gapcheck.py` is measuring."""
    desk = Desk(tmp_path)
    desk.prompt("sitting 45")
    started, _, limit, *_ = desk.state.read_text().split()
    long_ago = int(time.time()) - 40 * 60
    desk.state.write_text(f"{started} {long_ago} {limit}\n")
    desk.prompt("back the next morning")
    assert desk.state.read_text().split()[2] == "15", \
        "a fresh sitting is the short default, not the length last granted"


def test_reading_the_clock_grants_nothing(tmp_path):
    """A session may read freely — the one thing it may do with the
    instrument besides ending a sitting."""
    desk = Desk(tmp_path)
    desk.prompt("sitting 20")
    desk.rewind(5)   # so `started` is not this second: a read that
                     # rewrote it as `now` passed here on 2026-08-26
                     # (`board/green.md`), because both were the same
    before = desk.state.read_text()
    r = desk.run()
    assert r.returncode == 0
    assert "20" in r.stdout
    assert desk.state.read_text() == before


def test_a_finished_background_task_is_not_an_arrival(tmp_path):
    """**The defect of 2026-08-23, and the direction it ran in.**

    A background agent's completion is delivered to the session as a
    prompt, so it arrived at this hook as though Henri had typed it.  At
    17:34 that day the limit blocked one — *withholding a result he had
    already asked for* — and every other notification that afternoon
    wrote a `prompt` row, which is a ledger claiming somebody was at the
    desk when nobody was.  Three of the last five rows were machines.

    His call, given two options: log it under its own name and never
    block.  So a wake passes (exit 0), leaves one `wake` line, and —
    the part that matters for the meter — **does not touch the state**:
    it may not open a sitting, extend one, or move `last`, or a
    notification landing in a silence starts a sitting nobody sat for.
    """
    desk = Desk(tmp_path)
    desk.prompt("sitting 45")
    before = desk.state.read_text()

    out = desk.prompt("<task-notification>\n<task-id>abc</task-id>\n"
                      "<status>completed</status>\n</task-notification>")

    assert out.returncode == 0, f"a wake must never block: {out.stderr}"
    assert desk.state.read_text() == before, \
        "a wake moved the sitting's state; it must be transparent to it"
    assert [l[1] for l in desk.lines()][-1] == "wake"


def test_a_wake_does_not_block_even_past_the_limit(tmp_path):
    """The whole point of the fix, at the moment it bit.

    Past the limit a typed prompt is refused and that is correct.  A
    finished task is not a person sitting down again, and refusing it
    does not protect anybody's evening — it only hides work that is
    already done.
    """
    desk = Desk(tmp_path)
    desk.prompt("sitting 15")
    desk.rewind(20)

    out = desk.prompt("<task-notification><status>completed</status>"
                      "</task-notification>")
    assert out.returncode == 0, "the limit held back a finished task"
    assert "minutes are up" not in out.stderr

    typed = desk.prompt("what did it say?")
    assert typed.returncode == 2, "a typed prompt past the limit must stop"


def test_a_prompt_that_merely_mentions_the_word_is_still_an_arrival(tmp_path):
    """The twin of `test_a_question_that_merely_mentions_it_is_not_a_grant`.

    Henri asking *"why did the task-notification get blocked?"* is a
    person at the desk, and must count as one.  The match is on the
    literal tag the harness wraps a notification in, not on the word.
    """
    desk = Desk(tmp_path)
    desk.prompt("sitting 45")
    desk.prompt("why did the task-notification thing get blocked?")
    assert [l[1] for l in desk.lines()][-1] == "prompt"


MESSAGE = ('<cross-session-message from="uds:/run/user/1000/cc-socks/3913.sock" '
           'from-name="tend-e8" from-mode="prompting">\ntwo questions\n'
           '</cross-session-message>')


def test_a_message_from_another_session_is_not_an_arrival(tmp_path):
    """**The defect of 2026-08-26, 07:20 (`board/arrival.md`).**

    A session's message to another session is delivered as a prompt,
    wrapped in the harness's tag, so it reached this hook as though
    Henri had typed it — and was blocked past a ten-minute grant, with
    a `block` row he did not cause.  Henri, the same morning: *"it's
    not a feature in my eyes that limit.sh blocks the messages from
    others."*  The wake's shape, then: logged under its own name, never
    blocked, and the state untouched — a message landing in a silence
    must not open a sitting nobody sat for.
    """
    desk = Desk(tmp_path)
    desk.prompt("sitting 45")
    before = desk.state.read_text()
    out = desk.prompt(MESSAGE)
    assert out.returncode == 0, f"a message must never block: {out.stderr}"
    assert desk.state.read_text() == before, \
        "a message moved the sitting's state; it must be transparent to it"
    assert [l[1] for l in desk.lines()][-1] == "peer", \
        "gestate's word: one ledger, and its reader skips `wake` and `peer` by name"


def test_a_message_is_delivered_even_past_the_limit(tmp_path):
    """The moment it bit: the sitting closed, the questions held."""
    desk = Desk(tmp_path)
    desk.prompt("sitting 15")
    desk.rewind(20)
    out = desk.prompt(MESSAGE)
    assert out.returncode == 0, "the limit held back another session's message"
    assert "minutes are up" not in out.stderr
    typed = desk.prompt("what did they ask?")
    assert typed.returncode == 2, "a typed prompt past the limit must stop"


def test_a_prompt_that_merely_mentions_a_message_is_still_an_arrival(tmp_path):
    """Henri asking *why* a message was blocked is a person at the desk.
    The match is on the harness's tag, not on the words."""
    desk = Desk(tmp_path)
    desk.prompt("sitting 45")
    desk.prompt("why was the cross-session-message blocked?")
    assert [l[1] for l in desk.lines()][-1] == "prompt"


# ── the override: sitting N because <word>, checked by the hook ──
# card:sitting-everywhere.md day one — the grant row grows reason= and
# verified=, and only a reason a program can verify grants the time.

def _git_tree(path, dirty=False, patch=False):
    path.mkdir(parents=True, exist_ok=True)
    g = ["git", "-c", "user.name=t", "-c", "user.email=t@t", "-C", str(path)]
    subprocess.run(["git", "init", "-q", str(path)], check=True)
    (path / "a.txt").write_text("x\n")
    subprocess.run(g + ["add", "."], check=True)
    subprocess.run(g + ["commit", "-qm", "base"], check=True)
    if dirty:
        (path / "a.txt").write_text("y\n")
    if patch:
        (path / "fix.patch").write_text("--- a\n+++ b\n")
    return path


def _override(tmp_path, prompt, tree):
    desk = Desk(tmp_path)
    desk.env["TEND_LIMIT_TREE"] = str(tree)
    return desk, desk.prompt(prompt)


def _last(desk, event):
    rows = [l for l in desk.lines() if len(l) > 1 and l[1] == event]
    return rows[-1] if rows else None


def test_override_commit_verifies_on_a_dirty_tree(tmp_path):
    """green with it real: the tree has uncommitted work, so `commit`
    verifies, the sitting is granted, and the ledger says verified=1."""
    tree = _git_tree(tmp_path / "tree", dirty=True)
    desk, r = _override(tmp_path, "sitting 25 because commit", tree)
    assert r.returncode == 2 and "verified" in r.stderr, r.stderr
    row = _last(desk, "grant")
    assert row and "reason=commit" in row[2] and "verified=1" in row[2], row
    assert desk.state.read_text().split()[2] == "25"


def test_override_commit_refused_on_a_clean_tree(tmp_path):
    """red with the check faked: the tree is clean, so `commit` cannot
    verify — refused, verified=0, and no new sitting granted."""
    tree = _git_tree(tmp_path / "tree", dirty=False)
    desk, r = _override(tmp_path, "sitting 25 because commit", tree)
    assert r.returncode == 2 and "refused" in r.stderr, r.stderr
    row = _last(desk, "grant-refused")
    assert row and "reason=commit" in row[2] and "verified=0" in row[2], row
    assert not desk.state.exists() or desk.state.read_text().split()[2] != "25"


def test_override_patch_verifies_when_a_patch_waits(tmp_path):
    tree = _git_tree(tmp_path / "tree", patch=True)
    desk, r = _override(tmp_path, "sitting 20 because patch", tree)
    assert r.returncode == 2 and "verified" in r.stderr, r.stderr
    assert "verified=1" in _last(desk, "grant")[2]


def test_override_patch_refused_without_one(tmp_path):
    tree = _git_tree(tmp_path / "tree")
    desk, r = _override(tmp_path, "sitting 20 because patch", tree)
    assert "refused" in r.stderr and "verified=0" in _last(desk, "grant-refused")[2]


def test_an_unwired_word_is_refused_with_its_blocker(tmp_path):
    """run is named on the card but has no record to check yet; it is
    refused with the blocker, never faked green."""
    tree = _git_tree(tmp_path / "tree", dirty=True)
    _, run = _override(tmp_path, "sitting 15 because run", tree)
    assert "refused" in run.stderr and "day two" in run.stderr, run.stderr


def _andon(tmp_path, *words):
    env = dict(os.environ, TEND_ANDON_STATE=str(tmp_path / "andon"), TEND_ANDON_PLAYER="true", TEND_ANDON_GAP="0")
    return subprocess.run(["sh", str(ROOT / "tools" / "andon.sh"), *words], env=env, capture_output=True, text=True)


def test_override_andon_verifies_while_a_ring_is_unanswered(tmp_path):
    """green with it real: a question asked and rung, nobody has answered —
    the record is the andon's own, read by the hook, not the session's word."""
    tree = _git_tree(tmp_path / "tree")
    assert _andon(tmp_path, "ask", "which prefix?").returncode == 0
    assert _andon(tmp_path, "ring").returncode == 0
    desk = Desk(tmp_path)
    desk.env["TEND_LIMIT_TREE"] = str(tree)
    desk.env["TEND_ANDON_STATE"] = str(tmp_path / "andon")
    r = desk.prompt("sitting 15 because andon")
    assert r.returncode == 2 and "verified" in r.stderr, r.stderr
    assert "reason=andon" in _last(desk, "grant")[2] and "verified=1" in _last(desk, "grant")[2]


def test_override_andon_refused_with_nothing_pulled(tmp_path):
    """red with the check faked: asked but never rung is a draft; answered is
    hung up.  Neither grants."""
    tree = _git_tree(tmp_path / "tree")
    _andon(tmp_path, "ask", "q")
    desk = Desk(tmp_path)
    desk.env["TEND_LIMIT_TREE"] = str(tree)
    desk.env["TEND_ANDON_STATE"] = str(tmp_path / "andon")
    r = desk.prompt("sitting 15 because andon")
    assert "refused" in r.stderr and "no cord is pulled" in r.stderr, r.stderr
    assert "verified=0" in _last(desk, "grant-refused")[2]


def test_an_unknown_reason_is_refused(tmp_path):
    tree = _git_tree(tmp_path / "tree", dirty=True)
    _, r = _override(tmp_path, "sitting 15 because banana", tree)
    assert r.returncode == 2 and "not a checkable reason" in r.stderr, r.stderr


def test_a_plain_sitting_still_opens_one(tmp_path):
    """the override did not break the plain word it extends."""
    desk = Desk(tmp_path)
    r = desk.prompt("sitting 30")
    assert r.returncode == 2 and "Sitting of 30" in r.stderr
    assert desk.state.read_text().split()[2] == "30"
    assert "reason=" not in (_last(desk, "grant") or ["", "", ""])[2]
