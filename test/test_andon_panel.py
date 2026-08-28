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


def test_answered_clears_the_pull(tmp_path):
    write(tmp_path,
          pending="",
          log="1 2026-08-28 10:06 ask q\n2 2026-08-28 10:07 ring pending=1\n"
              "3 2026-08-28 10:30 answered n=1\n")
    st = read_state(tmp_path)
    assert not st.pulled and st.last_ring is None, "a ring before the answer does not keep it pulled"
    assert st.answered == 1
