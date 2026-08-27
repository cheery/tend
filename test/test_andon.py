#: asked-by: Henri, 2026-08-27 — "cords could be taken now into this batch" (card:cords.md)
"""test/test_andon.py — the cord: a question first, a capped ring, a record a program can read.

What is held: a ring with nothing asked is refused; rings cap at three;
a second ring inside the quiet window is refused and says when; `pulled`
is true only between a ring and an answer (the record `tools/limit.sh`
reads for `sitting N because andon`); a player that cannot reach the
sound card is a loud exit 1, never silence; and `answered` is refused
inside the fence.  The player is a stub here — the real ring through
the PipeWire socket was measured by hand on 2026-08-27 (card:cords.md).
"""
import os
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
ANDON = ROOT / "tools" / "andon.sh"


def andon(state, *args, player="true", quiet="600", fenced=None):
    env = dict(os.environ, TEND_ANDON_STATE=str(state), TEND_ANDON_PLAYER=player,
               TEND_ANDON_GAP="0", TEND_ANDON_QUIET=quiet)
    if fenced is not None:
        env["TEND_FENCED"] = fenced
    return subprocess.run(["sh", str(ANDON), *args], env=env, capture_output=True, text=True)


def test_it_parses():
    assert subprocess.run(["sh", "-n", str(ANDON)]).returncode == 0


def test_a_ring_with_nothing_asked_is_refused(tmp_path):
    r = andon(tmp_path, "ring")
    assert r.returncode == 2 and "nothing asked" in r.stderr
    assert not (tmp_path / "andon.log").exists() or "ring" not in (tmp_path / "andon.log").read_text()


def test_ask_then_ring_caps_at_three_and_prints_the_questions(tmp_path):
    assert andon(tmp_path, "ask", "which prefix?").returncode == 0
    assert andon(tmp_path, "ask", "leash in the set?").returncode == 0
    r = andon(tmp_path, "ring", "9")
    assert r.returncode == 0, r.stderr
    assert "ringing 3" in r.stdout and "which prefix?" in r.stdout and "leash in the set?" in r.stdout
    log = (tmp_path / "andon.log").read_text()
    assert "ring n=3 pending=2" in log


def test_a_second_ring_in_the_quiet_window_is_refused_and_says_when(tmp_path):
    andon(tmp_path, "ask", "q")
    assert andon(tmp_path, "ring").returncode == 0
    r = andon(tmp_path, "ring")
    assert r.returncode == 3 and "not ringing again" in r.stderr
    r = andon(tmp_path, "ring", quiet="0")
    assert r.returncode == 0, "the window is a number, and zero is a window"


def test_pulled_is_true_only_between_a_ring_and_an_answer(tmp_path):
    assert andon(tmp_path, "pulled").returncode == 1, "nothing asked: not pulled"
    andon(tmp_path, "ask", "q")
    assert andon(tmp_path, "pulled").returncode == 1, "asked, not rung: a draft, not a pull"
    andon(tmp_path, "ring")
    r = andon(tmp_path, "pulled")
    assert r.returncode == 0 and "unanswered" in r.stdout
    assert andon(tmp_path, "pulled", "-q").stdout == ""
    assert andon(tmp_path, "answered", fenced="").returncode == 0
    assert andon(tmp_path, "pulled").returncode == 1, "answered: the cord hangs loose again"
    assert (tmp_path / "andon.pending").read_text() == ""


def test_a_player_that_fails_is_loud_and_does_not_count_as_a_ring(tmp_path):
    andon(tmp_path, "ask", "q")
    r = andon(tmp_path, "ring", player="false")
    assert r.returncode == 1 and "could not reach the sound card" in r.stderr
    assert "REACH=audio" in r.stderr, "inside the fence the fix is the row, and the message says so"
    assert andon(tmp_path, "pulled").returncode == 1, "a ring nobody could hear is not a pull"
    assert andon(tmp_path, "ring").returncode == 0, "and it does not start the quiet window"


def test_answered_is_refused_inside_the_fence(tmp_path):
    andon(tmp_path, "ask", "q")
    r = andon(tmp_path, "answered", fenced="1")
    assert r.returncode == 2 and "person's word" in r.stderr
    assert (tmp_path / "andon.pending").read_text().strip().endswith("q")


def test_an_unknown_word_and_an_empty_ask_are_refused_out_loud(tmp_path):
    assert andon(tmp_path, "shout").returncode == 2
    assert andon(tmp_path, "ask", "").returncode == 2
    assert andon(tmp_path, "ring", "many").returncode == 2
