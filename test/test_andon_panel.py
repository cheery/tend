"""tools/andon-panel.py — the andon's person-side half (card:andon-panel.md).

The panel runs outside the fence and only *reads* the record a session
writes (andon.pending, andon.log), so the cord reaches the person
through a channel a fenced session cannot cut.  The curses view needs a
terminal; what is tested here is `read_state`, the pure reading it polls
— the pending questions, the ring count a new ring is detected by, and
the pulled state `tools/limit.sh` shares.
"""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("andon_panel", ROOT / "tools" / "andon-panel.py")
andon_panel = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(andon_panel)
read_state = andon_panel.read_state


def write(d, pending="", log=""):
    (d / "andon.pending").write_text(pending)
    (d / "andon.log").write_text(log)


def test_no_record_is_an_empty_quiet_panel(tmp_path):
    st = read_state(tmp_path)
    assert st.pending == [] and st.rings == 0 and st.last_ring is None and not st.pulled


def test_it_reads_the_pending_questions_with_their_stamps(tmp_path):
    write(tmp_path,
          pending="2026-08-28 10:06 first question\n2026-08-28 10:10 second one\n")
    st = read_state(tmp_path)
    assert [q.text for q in st.pending] == ["first question", "second one"]
    assert st.pending[0].stamp == "2026-08-28 10:06"


def test_a_ring_makes_it_pulled_and_carries_the_ring_time(tmp_path):
    write(tmp_path,
          pending="2026-08-28 10:06 a question\n",
          log="1787894760 2026-08-28 10:06 ask a question\n"
              "1787894770 2026-08-28 10:07 ring pending=1\n")
    st = read_state(tmp_path)
    assert st.rings == 1 and st.last_ring == 1787894770 and st.pulled


def test_another_ring_increments_the_count_the_view_watches(tmp_path):
    write(tmp_path,
          pending="2026-08-28 10:06 a question\n",
          log="1 2026-08-28 10:06 ask a question\n"
              "2 2026-08-28 10:07 ring pending=1\n"
              "3 2026-08-28 10:20 ring pending=1\n")
    st = read_state(tmp_path)
    assert st.rings == 2 and st.last_ring == 3


def test_a_ring_that_could_not_sound_still_reaches_the_panel(tmp_path):
    """Inside the fence pw-play fails and tools/andon.sh logs `ring-failed`,
    not `ring` (card:silent-cord.md) — and that is precisely the pull the
    panel exists to announce: the cord reached no sound, so the person-side
    must.  read_state counts it as a ring."""
    write(tmp_path,
          pending="2026-08-28 10:06 a fenced question\n",
          log="1 2026-08-28 10:06 ask a fenced question\n"
              "2 2026-08-28 10:07 ring-failed player=pw-play pending=1\n")
    st = read_state(tmp_path)
    assert st.rings == 1 and st.last_ring == 2 and st.pulled


def test_answered_clears_the_pull(tmp_path):
    write(tmp_path,
          pending="",
          log="1 2026-08-28 10:06 ask q\n2 2026-08-28 10:07 ring pending=1\n"
              "3 2026-08-28 10:30 answered n=1\n")
    st = read_state(tmp_path)
    assert not st.pulled and st.last_ring is None, "a ring before the answer does not keep it pulled"
    assert st.answered == 1


def test_the_panel_plays_a_real_tone_not_the_terminal_bell(tmp_path):
    """The bug on the work laptop, 2026-08-28: the panel reacted but made
    no sound, because curses.beep is the terminal bell and terminals mute
    it.  The panel is outside the fence, so it plays an actual tone through
    a real player (card:andon-panel.md, card:silent-cord.md)."""
    # the tone is a valid wav
    import wave
    wav = tmp_path / "t.wav"
    andon_panel._write_tone(str(wav))
    with wave.open(str(wav)) as w:
        assert w.getnframes() > 1000 and w.getframerate() == 22050

    # _play_alert hands the wav to a player; a fake one records it was called
    marker = tmp_path / "played"
    fake = tmp_path / "player.sh"
    fake.write_text('#!/bin/sh\necho "$1" > "%s"\n' % marker)
    fake.chmod(0o755)
    assert andon_panel._play_alert(player=str(fake)) is True
    assert marker.exists() and marker.read_text().strip().endswith(".wav")
