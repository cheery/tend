"""tools/panel.py — the person's panel; the andon's person-side half (card:andon-panel.md), then the canvas and the hand.

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
_spec = importlib.util.spec_from_file_location("panel", ROOT / "tools" / "panel.py")
panel = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(panel)
read_state = panel.read_state


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
    panel._write_tone(str(wav))
    with wave.open(str(wav)) as w:
        assert w.getnframes() > 1000 and w.getframerate() == 22050

    # _play_alert hands the wav to a player; a fake one records it was called
    marker = tmp_path / "played"
    fake = tmp_path / "player.sh"
    fake.write_text('#!/bin/sh\necho "$1" > "%s"\n' % marker)
    fake.chmod(0o755)
    assert panel._play_alert(player=str(fake)) is True
    assert marker.exists() and marker.read_text().strip().endswith(".wav")


# --- the canvas: what the person is holding, and a death on the same timeline as a ring (card:canvas.md) ---
#
# 2026-08-28, 13:27: Henri pulled the llm node and llama-server died a
# second later at the loader (libsvml.so).  `pull` said "started llm",
# `stopped` said `exited 127`, the log said why, and he saw none of it
# until `lead.sh` said "not up".  A pin is the person's "I am holding
# this" — `<name>.pin` in a canvas directory, on the person's side —
# and the panel shows one row per pin from what the runner leaves
# (run.lock, stopped, watch) and puts a non-zero stop in the log column
# beside the andon's own lines.  The fixture is the 13:27 minute.
import os
import pathlib
import pytest
import subprocess
import time

read_canvas = panel.read_canvas
read_log = panel.read_log


@pytest.fixture(autouse=True)
def _own_tree(monkeypatch, tmp_path):
    """A test builds the side it means; it never reads the live tree.  The
    panel's canvas lists every node of the tree a process is pulling
    (card:edge.md), and on 2026-09-02 the real `die`, pulled from Henri's
    shell while the suite ran, appeared as a row in five tests about
    holds — the fixture rule's face in the panel.  Every test's tree is
    an empty directory unless it passes its own."""
    monkeypatch.setattr(panel, "ROOT", str(tmp_path / "tree"))

LOADER = "llama-server: error while loading shared libraries: libsvml.so: cannot open shared object file: No such file or directory"


def dead_node(tmp_path, name="llm", stopped="exited 127: llm stopped by itself", at=1787912843):
    """A node whose runner died at once — the 13:27 shape: `stopped` names a
    non-zero exit, and the log's last real line is the loader's."""
    node = tmp_path / name; (node / "state").mkdir(parents=True)
    (node / "grant").write_text("program llama-server\n")
    st = node / "state"
    (st / "log").write_text("DeprecationWarning: something\n" + LOADER + "\n")
    (st / "stopped").write_text(stopped + "\n")
    os.utime(st / "stopped", (at, at))
    (st / "pull").write_text(f"{at - 1} \n")
    return node


def pin(canvas, name, node, state=None):
    canvas.mkdir(parents=True, exist_ok=True)
    text = f"node {node}\n" + (f"state {state}\n" if state else "")
    (canvas / f"{name}.pin").write_text(text)


def test_no_canvas_is_no_rows(tmp_path):
    assert read_canvas(tmp_path / "canvas") == []


def test_a_pinned_node_that_died_at_the_loader_is_a_row_that_says_so(tmp_path):
    """The 13:27 minute on the person's side: not running, the last stop's
    reason, and what the runner said as it died — read from the state the
    runner left, whenever it happened, not only if `pull` was watching."""
    node = dead_node(tmp_path)
    canvas = tmp_path / "canvas"; pin(canvas, "llm", node)
    rows = read_canvas(canvas)
    assert [r.name for r in rows] == ["llm"]
    r = rows[0]
    assert not r.running and not r.cut
    assert r.last_stop == 1787912843 and r.stop_reason.startswith("exited 127")
    assert r.dead, "a non-zero exit is a death, not a close"
    assert "libsvml.so" in r.said and "DeprecationWarning" not in r.said
    assert r.last_pull == 1787912842


def test_a_death_is_a_line_in_the_log_column_beside_the_andon_lines(tmp_path):
    """One timeline: a ring, an ask, an answer and a runner's non-zero stop
    are the same kind of line, in time order.  Day two (card:canvas.md,
    2026-08-29): the death is a line the runner's own stop path wrote
    into the record — `<epoch> <stamp> <name>: exited <rc> — <reason>` —
    not a merge the panel makes at view time; the who-column is the
    pin's name, read off the line's `<name>:` prefix, so it is bold the
    way a cut is."""
    node = dead_node(tmp_path, at=1787912843)
    canvas = tmp_path / "canvas"; pin(canvas, "llm", node)
    write(tmp_path,
          pending="",
          log="1787912000 2026-08-28 13:13 ask a question before\n"
              "1787912843 2026-08-28 13:27 llm: exited 127 — " + LOADER + "\n"
              "1787914724 2026-08-28 13:58 ask llm (lead): a question after\n")
    events = read_log(tmp_path, read_canvas(canvas))
    kinds = [(e.epoch, e.who) for e in events]
    assert kinds == [(1787912000, "andon"), (1787912843, "llm"), (1787914724, "andon")], kinds
    death = events[1]
    assert "exited 127" in death.text and "libsvml.so" in death.text
    assert [e for e in events if e.who == "llm"] == [death], "the death is on the timeline once, from the record"


def test_a_death_survives_the_next_clean_stop(tmp_path):
    """§17:30's open question, answered by the record: the row shows the
    *last* stop (idle, this afternoon), and the 13:27 death is still a
    line on the timeline because the runner wrote it when it died, and
    `stopped` being rewritten since does not take it back."""
    node = dead_node(tmp_path, stopped="idle: nothing has pulled llm for 60s", at=1787916000)
    canvas = tmp_path / "canvas"; pin(canvas, "llm", node)
    write(tmp_path, log="1787912843 2026-08-28 13:27 llm: exited 127 — " + LOADER + "\n")
    rows = read_canvas(canvas)
    assert rows[0].stop_reason.startswith("idle:") and not rows[0].dead
    events = read_log(tmp_path, rows)
    assert [(e.epoch, e.who) for e in events] == [(1787912843, "llm")], events


def test_a_clean_stop_is_not_a_line_in_the_log_column(tmp_path):
    """idle and the sitting are closes, exit 0 — the row shows them as the
    last stop; the log column is for what went wrong."""
    node = dead_node(tmp_path, stopped="idle: nothing has pulled llm for 60s")
    canvas = tmp_path / "canvas"; pin(canvas, "llm", node)
    rows = read_canvas(canvas)
    assert rows[0].stop_reason.startswith("idle:") and not rows[0].dead
    assert read_log(tmp_path, rows) == []


def _lock_holder(st):
    st.mkdir(parents=True, exist_ok=True)
    p = subprocess.Popen(["sh", "-c", 'exec 9>>"$1"; flock 9; exec sleep 60', "_", str(st / "run.lock")])
    for _ in range(100):
        if subprocess.run(["flock", "-n", str(st / "run.lock"), "true"]).returncode != 0:
            return p
        time.sleep(0.05)
    raise AssertionError("the fixture holds the lock")


def test_lock_held_reads_a_free_lock_as_free_under_a_hammer_and_a_held_one_as_held(tmp_path, hammer, hold):
    """card:lock-test.md: `_lock_held` took the lock once to test it, and one
    read collides with any other reader's — under a loop of readers a free
    lock read as held about half the time (measured, 2026-09-03).  Now it
    reads across a window: free the instant a try succeeds, held only if
    every try in the window fails.  The single read (window=0) is asserted
    wrong first, so the hammer is known to bite."""
    lock = tmp_path / "run.lock"; lock.touch()
    def single_reads(n):   # spread over many of the hammer's rounds, not a burst inside one
        wrong = 0
        for _ in range(n):
            wrong += panel._lock_held(lock, window=0); time.sleep(0.001)
        return wrong
    with hammer(lock):
        assert single_reads(200) >= 1, "the hammer did not bite: no single read collided"
        assert not any(panel._lock_held(lock) for _ in range(40)), "a free lock read as held across the window"
    with hold(lock):
        assert all(panel._lock_held(lock) for _ in range(5)), "a real holder read as free"
    assert not panel._lock_held(lock)
    assert not panel._lock_held(tmp_path / "never") and not (tmp_path / "never").exists(), "a lock that is not there is never made"


def test_a_running_pin_reads_the_lock_and_a_silent_watcher_is_the_cords_cut(tmp_path):
    node = dead_node(tmp_path)
    st = node / "state"
    canvas = tmp_path / "canvas"; pin(canvas, "llm", node)
    p = _lock_holder(st)
    try:
        (st / "watch").touch()
        r = read_canvas(canvas)[0]
        assert r.running and not r.cut
        old = time.time() - 180
        os.utime(st / "watch", (old, old))
        r = read_canvas(canvas)[0]
        assert r.running and r.cut and r.cut >= 170, "a held lock with a stale heartbeat: the cords are cut"
        assert "cords are cut" in panel.row_line(r) and "3 min" in panel.row_line(r)
    finally:
        p.kill(); p.wait()


def test_a_pin_may_name_a_state_directory_that_is_not_the_nodes_default(tmp_path):
    node = dead_node(tmp_path)
    other = tmp_path / "elsewhere"; other.mkdir()
    (other / "stopped").write_text("exited 1: llm stopped by itself\n")
    canvas = tmp_path / "canvas"; pin(canvas, "llm", node, state=other)
    r = read_canvas(canvas)[0]
    assert r.state == str(other) and r.stop_reason.startswith("exited 1")


def test_the_canvas_is_a_path_and_the_panel_reads_it_without_a_terminal(tmp_path):
    node = dead_node(tmp_path)
    canvas = tmp_path / "srv"; pin(canvas, "llm", node)
    # the runner wrote its death into the record as it died (day two)
    write(tmp_path, pending="", log="1787912843 2026-08-28 13:27 llm: exited 127 — " + LOADER + "\n")
    r = subprocess.run(["python3", str(ROOT / "tools" / "panel.py"), "--canvas", str(canvas)],
                       capture_output=True, text=True, env=dict(os.environ, TEND_ANDON_STATE=str(tmp_path)))
    assert r.returncode == 0, r.stderr
    assert "llm" in r.stdout and "exited 127" in r.stdout and "libsvml.so" in r.stdout, r.stdout


# --- the hold: the canvas's standing pull, a bit on the row (card:hold.md, 2026-08-29) ---

def test_a_held_pin_says_held_beside_its_state_and_an_unheld_one_does_not(tmp_path):
    """`<name>.hold` beside the pin, on the person's side: the row says
    `held` beside `running`/`not running`/`DEAD`, and carries who asked;
    a pin with no hold has none.  The panel reads it and never writes it."""
    node = dead_node(tmp_path, stopped="idle: nothing has pulled llm for 60s")
    canvas = tmp_path / "canvas"; pin(canvas, "llm", node)
    r = read_canvas(canvas)[0]
    assert r.held is None and "held" not in panel.row_line(r)
    (canvas / "llm.hold").write_text("held by henri, the desk\n")
    r = read_canvas(canvas)[0]
    assert r.held == "held by henri, the desk"
    line = panel.row_line(r)
    assert line.startswith("llm") and "HELD, NOT RUNNING" in line and "held — held by henri, the desk" in line, line
    assert panel.wrong(r), "a held node with no runner up is the hold not kept: bold"
    (canvas / "llm.hold").write_text("")
    assert read_canvas(canvas)[0].held == "(no words)"


def test_a_hold_is_a_row_whether_or_not_its_node_is_pinned(tmp_path):
    """Henri, 2026-08-29: "we could improve the andon-panel to show
    holds".  A held node is on the canvas: a hold with no pin is a row,
    named by its node directory (the death notice's name), with its
    words; a hold and a pin for one node and state are one row; and a
    hold that names another state of the same node is its own row."""
    node = dead_node(tmp_path, stopped="idle: nothing has pulled llm for 60s")
    canvas = tmp_path / "canvas"; canvas.mkdir()
    (canvas / "some-llm.hold").write_text(f"node {node}\nheld by henri, the desk\n")
    rows = read_canvas(canvas)
    assert [r.name for r in rows] == ["llm"] and rows[0].held == "held by henri, the desk", rows
    assert "HELD, NOT RUNNING" in panel.row_line(rows[0]) and "held — held by henri, the desk" in panel.row_line(rows[0])
    pin(canvas, "llm", node)
    rows = read_canvas(canvas)
    assert len(rows) == 1 and rows[0].held == "held by henri, the desk", rows
    other = tmp_path / "other-state"; other.mkdir()
    (canvas / "llm-other.hold").write_text(f"node {node}\nstate {other}\nthe other state\n")
    rows = read_canvas(canvas)
    assert [(r.name, r.held) for r in rows] == [("llm", "held by henri, the desk"), ("llm", "the other state")], rows
    assert panel._counts(rows) == "2 on it, 2 held"


def test_a_bare_hold_line_names_a_node_of_the_tree_and_its_state(tmp_path):
    """`llm "state"` on one line (Henri's own example): the first word a
    node of this tree, the rest — quotes off — its state, relative to
    the node; the filename is a label."""
    canvas = tmp_path / "canvas"; canvas.mkdir()
    llm = tmp_path / "tree" / "llm"; llm.mkdir(parents=True); (llm / "grant").write_text("program true\n")   # a node of *this test's* tree, not the live one
    (canvas / "mine.hold").write_text('llm "state"\nheld by henri\n')
    h = panel.read_holds(canvas)[0]
    assert h.label == "mine" and h.node == os.path.join(panel.ROOT, "llm")
    assert h.state == os.path.join(panel.ROOT, "llm", "state") and h.words == "held by henri"


def test_a_hold_that_holds_nothing_is_a_broken_row_and_a_held_death_says_which_way(tmp_path):
    """Henri, 2026-08-29: "make sure the error becomes visible on the andon
    panel".  A hold whose node is not a node, or whose state is not
    there, is a BROKEN row, bold, saying why; a held node that died with
    the hold older than the death says "touch it"; one with the hold
    newer says the resolver will restart it."""
    canvas = tmp_path / "canvas"; canvas.mkdir()
    (canvas / "ghost.hold").write_text(f"node {tmp_path}/nowhere\nheld by henri\n")
    node = dead_node(tmp_path)   # exited 127 at 13:27
    (canvas / "gone.hold").write_text(f"node {node}\nstate {tmp_path}/no-such-state\nheld too\n")
    rows = read_canvas(canvas)
    assert [r.name for r in rows] == ["ghost", "gone"], rows
    assert all(r.broken and panel.wrong(r) for r in rows)
    assert "BROKEN hold — no node at" in panel.row_line(rows[0]) and "(held by henri)" in panel.row_line(rows[0])
    assert "BROKEN hold — state" in panel.row_line(rows[1]) and "is not there" in panel.row_line(rows[1])
    assert panel._counts(rows) == "2 on it, 2 held, 2 BROKEN"
    (canvas / "ghost.hold").unlink(); (canvas / "gone.hold").unlink()
    h = canvas / "llm.hold"; h.write_text(f"node {node}\nheld by henri\n")
    os.utime(h, (1787912843 - 60, 1787912843 - 60))       # older than the 13:27 death
    r = read_canvas(canvas)[0]
    assert r.dead and "DEAD, HELD — the hold is older than the death; touch it to restart" in panel.row_line(r)
    os.utime(h, (1787912843 + 60, 1787912843 + 60))       # touched, having seen why
    r = read_canvas(canvas)[0]
    assert "DEAD, HELD — the resolver restarts it at its next visit" in panel.row_line(r)


# --- the person's hand: the panel writes the canvas and runs the resolver (card:hold.md, 2026-08-29) ---
#
# Henri: "the andon panel should have a tool to insert .pin and .hold
# files to the canvas, and allow one to remove the .hold, then ensure
# that the log flows (in case the program fails or crashes on exit) and
# that the resolver is called after the file is added.  Also, entering
# the andon panel should run the resolver."

def stub_resolver(tmp_path):
    """A resolver that only counts its visits — the hand's contract is
    "call it once after the write", measured without starting anything."""
    log = tmp_path / "resolver.calls"
    script = tmp_path / "resolve-stub.sh"
    script.write_text(f"#!/bin/sh\necho visit >> {log}\necho 'launch: stub started nothing' >&2\n")
    script.chmod(0o755)
    return script, log


def visits(log):
    return log.read_text().count("visit") if log.exists() else 0


def test_the_hand_writes_pin_shaped_files_and_runs_the_resolver_once_per_write(tmp_path, monkeypatch, capsys):
    script, log = stub_resolver(tmp_path)
    monkeypatch.setenv("TEND_RESOLVE", str(script))
    node = dead_node(tmp_path)
    canvas = tmp_path / "canvas"
    rc = panel.main(["x", "--canvas", str(canvas), "hold", "mine", str(node), "held by henri, the desk"])
    assert rc == 0 and visits(log) == 1
    assert (canvas / "mine.hold").read_text() == f"node {node}\nheld by henri, the desk\n"
    out = capsys.readouterr().out
    assert "held: " in out and "resolver: launch: stub started nothing" in out, out
    rc = panel.main(["x", "--canvas", str(canvas), "pin", "llm", str(node), "--state", str(tmp_path / "s")])
    assert rc == 0 and visits(log) == 2
    assert (canvas / "llm.pin").read_text() == f"node {node}\nstate {tmp_path / 's'}\n"
    rc = panel.main(["x", "--canvas", str(canvas), "hold", "quiet", str(node)])
    assert rc == 0 and visits(log) == 3
    assert (canvas / "quiet.hold").read_text().splitlines()[1].startswith("held by "), "a hold from the panel is never wordless"
    rc = panel.main(["x", "--canvas", str(canvas), "unhold", "mine"])
    assert rc == 0 and not (canvas / "mine.hold").exists() and visits(log) == 4
    assert "removed: " in capsys.readouterr().out


def test_the_hand_refuses_what_is_not_a_node_and_does_not_resolve(tmp_path, monkeypatch, capsys):
    script, log = stub_resolver(tmp_path)
    monkeypatch.setenv("TEND_RESOLVE", str(script))
    canvas = tmp_path / "canvas"
    rc = panel.main(["x", "--canvas", str(canvas), "hold", "ghost", str(tmp_path / "nowhere")])
    assert rc == 2 and "no node at" in capsys.readouterr().err
    assert not canvas.exists() and visits(log) == 0
    rc = panel.main(["x", "--canvas", str(canvas), "unhold", "never"])
    assert rc == 2 and "no hold named never" in capsys.readouterr().err and visits(log) == 0
    rc = panel.main(["x", "--canvas", str(canvas), "hold", "../up", str(dead_node(tmp_path))])
    assert rc == 2 and "not a name" in capsys.readouterr().err and visits(log) == 0


def test_entering_the_panel_runs_the_resolver(tmp_path, monkeypatch, capsys):
    script, log = stub_resolver(tmp_path)
    monkeypatch.setenv("TEND_RESOLVE", str(script))
    monkeypatch.setenv("TEND_ANDON_STATE", str(tmp_path))
    assert panel.main(["x", "--canvas", str(tmp_path / "canvas")]) == 0
    assert visits(log) == 1
    assert "resolver: launch: stub started nothing" in capsys.readouterr().out


@pytest.mark.skipif(not os.path.exists("/usr/bin/python3"), reason="no system python3 for keep")
def test_a_hold_written_by_the_hand_starts_the_node_and_its_death_flows_to_the_timeline(tmp_path, monkeypatch):
    """The whole flow, real: the hand writes a hold for a node whose
    program dies at once; the resolver (this tree's) starts it under the
    leash; it dies; the death notice is on the timeline as the node's
    own line, and the row says DEAD, HELD — the hold is older than the
    death; touch it — and a second visit starts nothing (rule 3)."""
    tree = tmp_path / "tree"; node = tree / "dying"; node.mkdir(parents=True)
    (node / "grant").write_text("program /bin/sh -c 'echo \"dying: error while loading shared libraries: libx.so\" >&2; exit 3'\n")
    canvas = pathlib.Path(os.environ["TEND_CANVAS"])          # conftest's: the launcher reads the same one
    monkeypatch.setenv("TEND_RESOLVE", os.path.join(panel.HERE, "resolve.sh"))
    monkeypatch.setenv("TEND_TREE", str(tree))
    monkeypatch.setenv("TEND_ANDON_STATE", str(tmp_path))
    monkeypatch.delenv("TEND_FENCED", raising=False)
    lines = panel.hand("hold", ["dying", str(node), "held by the fixture"], str(canvas))
    assert any("is held and no runner — started one" in l for l in lines), lines
    record = tmp_path / "andon.log"
    t = time.monotonic()
    while time.monotonic() - t < 10 and not record.exists():
        time.sleep(0.05)
    assert record.exists(), "the death never reached the record"
    rows = read_canvas(canvas)
    assert [r.name for r in rows] == ["dying"] and rows[0].dead and rows[0].held == "held by the fixture", rows
    events = read_log(tmp_path, rows)
    assert len(events) == 1 and events[0].who == "dying" and "exited 3 — dying: error while loading" in events[0].text, events
    assert "DEAD, HELD — the hold is older than the death; touch it to restart" in panel.row_line(rows[0])
    assert panel.resolve_once() == "", "a death is not hammered: the hold is older, nothing starts"


def test_a_hold_on_a_state_the_resolver_does_not_run_says_so_instead_of_promising(tmp_path):
    """The critical reading of "state in the hold" (2026-08-29): the
    resolver runs NODE/state only, so a hold naming another state is
    honoured by nothing yet — the row says HELD, NOT HONOURED, bold, and
    never "the resolver starts one at its next visit".  A bare path line
    is the state, as in the launcher."""
    node = dead_node(tmp_path, stopped="idle: nothing has pulled llm for 60s")
    other = tmp_path / "other-state"; other.mkdir()
    canvas = tmp_path / "canvas"; canvas.mkdir()
    (canvas / "llm-other.hold").write_text(f"node {node}\n{other}\nthe other state\n")
    h = panel.read_holds(canvas)[0]
    assert h.state == str(other) and h.words == "the other state"
    r = read_canvas(canvas)[0]
    assert r.note and panel.wrong(r)
    line = panel.row_line(r)
    assert "HELD, NOT HONOURED — state" in line and "not honoured yet" in line and "next visit" not in line, line
    (canvas / "llm.hold").write_text(f"node {node}\nthe default state\n")
    rows = read_canvas(canvas)
    assert [(r.held, r.note is None) for r in rows] == [("the other state", False), ("the default state", True)], rows


# --- the tick line: a hold is kept only while something runs the resolver (card:hold.md, 2026-08-29) ---

def test_the_tick_is_a_line_and_a_hold_with_no_tick_or_a_stale_one_is_loud(tmp_path):
    canvas = tmp_path / "canvas"; canvas.mkdir()
    assert panel.read_tick(canvas) is None
    assert "no tick" in panel.tick_line(None, held=False) and not panel.tick_loud(None, held=False)
    assert "NO TICK" in panel.tick_line(None, held=True) and panel.tick_loud(None, held=True)
    (tmp_path / "tick").write_text(f"{int(time.time()) - 12} 30\n")
    t = panel.read_tick(canvas)
    assert t.every == 30 and 10 <= t.age < 20
    assert "every 30 s" in panel.tick_line(t, held=True) and not panel.tick_loud(t, held=True)
    (tmp_path / "tick").write_text(f"{int(time.time()) - 600} 30\n")
    t = panel.read_tick(canvas)
    assert "STALE" in panel.tick_line(t, held=True) and "10 min" in panel.tick_line(t, held=True)
    assert panel.tick_loud(t, held=True) and panel.tick_loud(t, held=False), "a carrier that stopped is loud, held or not"
    (tmp_path / "tick").write_text("garbage\n")
    assert panel.read_tick(canvas) is None


def test_the_panel_without_a_terminal_says_the_tick(tmp_path):
    node = dead_node(tmp_path)
    canvas = tmp_path / "srv"; pin(canvas, "llm", node)
    (canvas / "llm.hold").write_text(f"node {node}\nheld by the test\n")
    write(tmp_path)
    env = dict(os.environ, TEND_ANDON_STATE=str(tmp_path), TEND_RESOLVE="/bin/true")
    r = subprocess.run(["python3", str(ROOT / "tools" / "panel.py"), "--canvas", str(canvas)],
                       capture_output=True, text=True, env=env)
    assert r.returncode == 0, r.stderr
    assert "NO TICK" in r.stdout, r.stdout
    (tmp_path / "tick").write_text(f"{int(time.time()) - 5} 30\n")
    r = subprocess.run(["python3", str(ROOT / "tools" / "panel.py"), "--canvas", str(canvas)],
                       capture_output=True, text=True, env=env)
    assert "NO TICK" not in r.stdout and "every 30 s" in r.stdout, r.stdout


# --- talk and unpin (2026-08-30 — Henri: "I'd like if the .hold node could deploy some sort of
# user interface for node in the tools/panel.py, maybe text input with prompt, so that I can
# truly talk with the model, also would like a way to unpin nodes") ---
import http.server
import inspect
import json
import socket
import threading

REPLIES = """2026-08-30 06:10 Q: what is jidoka
2026-08-30 06:10 A: stop the line.
It means the machine stops itself.

2026-08-30 06:12 Q: and kanban
2026-08-30 06:12 V: openrouter vendor/big
2026-08-30 06:12 T: the user asks about kanban.
It is a pull signal.
2026-08-30 06:12 A: a card.

"""


def test_the_replies_record_reads_back_as_exchanges(tmp_path):
    (tmp_path / "replies").write_text(REPLIES)
    ex = panel.read_replies(str(tmp_path))
    assert [(e.question, e.answer) for e in ex] == [
        ("what is jidoka", "stop the line.\nIt means the machine stops itself."), ("and kanban", "a card.")]
    assert ex[0].stamp == "2026-08-30 06:10"
    assert ex[0].thinking == "" and ex[1].thinking == "the user asks about kanban.\nIt is a pull signal."
    assert ex[0].via == "" and ex[1].via == "openrouter vendor/big"
    assert panel.read_replies(str(tmp_path / "none")) == []
    assert panel.history(ex, turns=1) == [{"role": "user", "content": "and kanban"},
                                          {"role": "assistant", "content": "a card."}]
    assert panel.history(ex, turns=0) == []


class _Model(http.server.BaseHTTPRequestHandler):
    """A model at a port: echoes the last message, keeps every request."""
    bodies = []
    heads = []

    def log_message(self, *a): pass

    def do_GET(self):
        self.send_response(200); self.end_headers(); self.wfile.write(b"ok")

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        _Model.bodies.append(body)
        asked = body["messages"][-1]["content"]
        deltas = []
        if body.get("chat_template_kwargs", {}).get("enable_thinking"):
            deltas.append({"reasoning_content": "think<" + asked + ">"})
        deltas += [{"content": "echo<"}, {"content": asked + ">"}]
        _Model.heads.append(self.headers.get("Authorization"))
        self.send_response(200); self.send_header("Content-Type", "text/event-stream"); self.end_headers()
        for d in deltas:
            self.wfile.write(("data: " + json.dumps({"choices": [{"delta": d}]}) + "\n\n").encode()); self.wfile.flush()
        self.wfile.write(b"data: [DONE]\n\n")


@pytest.fixture
def model(monkeypatch):
    srv = http.server.HTTPServer(("127.0.0.1", 0), _Model)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{srv.server_address[1]}"
    monkeypatch.setenv("TEND_LLM_URL", base + "/v1/chat/completions")
    monkeypatch.setenv("TEND_LLM_HEALTH", base + "/health")
    monkeypatch.setenv("TEND_NO_START", "1")   # the model is the stub; deliver must not start llama-server
    monkeypatch.delenv("TEND_FENCED", raising=False)
    monkeypatch.delenv("TEND_THINK", raising=False)
    monkeypatch.delenv("TEND_DOOR", raising=False)
    _Model.bodies.clear(); _Model.heads.clear()
    yield _Model.bodies
    srv.shutdown()


def test_talk_carries_a_line_to_the_named_node_with_the_conversation_as_history(tmp_path, model, capsys):
    """One turn is one pull line and one `replies` entry — the node's own
    record, which the panel reads back as the conversation; the next turn
    carries the exchanges so far, so the model answers in the conversation."""
    node = dead_node(tmp_path); canvas = tmp_path / "canvas"; canvas.mkdir()
    (canvas / "llm.pin").write_text(f"node {node}\n")
    assert panel.talk("llm", "what is jidoka", str(canvas)) == "echo<what is jidoka>"
    assert model[-1]["messages"] == [{"role": "user", "content": "what is jidoka"}]
    assert panel.talk("llm", "and   kanban", str(canvas)) == "echo<and kanban>"
    assert model[-1]["messages"] == [{"role": "user", "content": "what is jidoka"},
                                     {"role": "assistant", "content": "echo<what is jidoka>"},
                                     {"role": "user", "content": "and kanban"}]
    ex = panel.read_replies(str(node / "state"))
    assert [(e.question, e.answer) for e in ex] == [("what is jidoka", "echo<what is jidoka>"), ("and kanban", "echo<and kanban>")]
    assert "what is jidoka" in (node / "state" / "pull").read_text(), "the ask is a pull line"
    # from a shell, the same turn
    rc = panel.main(["x", "--canvas", str(canvas), "talk", "llm", "a", "third"])
    assert rc == 0 and capsys.readouterr().out.strip() == "echo<a third>"
    assert len(model) == 3 and len(model[-1]["messages"]) == 5


def test_talk_refuses_a_name_not_on_the_canvas_and_sends_nothing(tmp_path, model, capsys):
    canvas = tmp_path / "canvas"; canvas.mkdir()
    (canvas / "llm.pin").write_text(f"node {dead_node(tmp_path)}\n")
    with pytest.raises(ValueError, match="nothing named ghost"):
        panel.talk("ghost", "hello", str(canvas))
    rc = panel.main(["x", "--canvas", str(canvas), "talk", "ghost", "hello"])
    assert rc == 2 and "nothing named ghost" in capsys.readouterr().err
    with pytest.raises(ValueError, match="nothing to say"):
        panel.talk("llm", "   ", str(canvas))
    assert panel.main(["x", "--canvas", str(canvas), "talk", "llm"]) == 2
    assert model == []


def test_talk_says_delivers_words_when_no_reply_lands(tmp_path, monkeypatch):
    """The node is down and would not start (TEND_NO_START, a closed port):
    deliver says so, and the talk raises its words rather than an empty
    answer — a turn with no reply is loud, not blank."""
    node = dead_node(tmp_path); canvas = tmp_path / "canvas"; canvas.mkdir()
    (canvas / "llm.pin").write_text(f"node {node}\n")
    s = socket.socket(); s.bind(("127.0.0.1", 0)); port = s.getsockname()[1]; s.close()
    monkeypatch.setenv("TEND_LLM_URL", f"http://127.0.0.1:{port}/v1/chat/completions")
    monkeypatch.setenv("TEND_LLM_HEALTH", f"http://127.0.0.1:{port}/health")
    monkeypatch.setenv("TEND_NO_START", "1")
    monkeypatch.delenv("TEND_FENCED", raising=False)
    with pytest.raises(ValueError, match="did not answer"):
        panel.talk("llm", "hello", str(canvas))
    assert panel.read_replies(str(node / "state")) == []


def test_the_hand_unpins(tmp_path, monkeypatch, capsys):
    script, log = stub_resolver(tmp_path)
    monkeypatch.setenv("TEND_RESOLVE", str(script))
    node = dead_node(tmp_path); canvas = tmp_path / "canvas"
    assert panel.main(["x", "--canvas", str(canvas), "pin", "llm", str(node)]) == 0
    assert (canvas / "llm.pin").exists()
    assert panel.main(["x", "--canvas", str(canvas), "unpin", "llm"]) == 0
    assert not (canvas / "llm.pin").exists() and visits(log) == 2
    assert "removed: " in capsys.readouterr().out
    assert panel.main(["x", "--canvas", str(canvas), "unpin", "llm"]) == 2
    assert "no pin named llm" in capsys.readouterr().err and visits(log) == 2


def test_talk_can_ask_the_model_to_think_and_shows_the_thinking_beside_the_answer(tmp_path, model, capsys, monkeypatch):
    """`think=True` (the [k] toggle, `--think`, TEND_THINK) asks for the
    template's thinking; the reasoning is a T line in the record, read
    back on the exchange, never sent as history; off, none is asked for."""
    node = dead_node(tmp_path); canvas = tmp_path / "canvas"; canvas.mkdir()
    (canvas / "llm.pin").write_text(f"node {node}\n")
    assert panel.talk("llm", "why", str(canvas), think=True) == "echo<why>"
    assert model[-1]["chat_template_kwargs"] == {"enable_thinking": True}
    ex = panel.read_replies(str(node / "state"))
    assert ex[-1].thinking == "think<why>" and ex[-1].answer == "echo<why>"
    assert panel.talk("llm", "and", str(canvas)) == "echo<and>"
    assert model[-1]["chat_template_kwargs"] == {"enable_thinking": False}
    assert model[-1]["messages"] == [{"role": "user", "content": "why"}, {"role": "assistant", "content": "echo<why>"},
                                     {"role": "user", "content": "and"}], "the thinking is never history"
    assert panel.read_replies(str(node / "state"))[-1].thinking == ""
    # the environment's word, and the shell's flag
    monkeypatch.setenv("TEND_THINK", "1")
    assert panel.talk("llm", "env", str(canvas)) == "echo<env>" and model[-1]["chat_template_kwargs"]["enable_thinking"]
    assert panel.talk("llm", "quiet", str(canvas), think=False) == "echo<quiet>" and not model[-1]["chat_template_kwargs"]["enable_thinking"]
    monkeypatch.delenv("TEND_THINK")
    rc = panel.main(["x", "--canvas", str(canvas), "talk", "--think", "llm", "from", "a", "shell"])
    out = capsys.readouterr()
    assert rc == 0 and out.out.strip() == "echo<from a shell>" and "(thinking) think<from a shell>" in out.err


def test_talk_can_go_through_a_door_and_the_exchange_says_so(tmp_path, model, capsys, monkeypatch):
    """Henri, 2026-08-30: "I now have the openrouter available for use."
    `door="openrouter"` (the [d] cycle, `--door`, TEND_DOOR) sends the
    turn through the door: its model and key on the request, no pull
    line, the exchange's `via` naming it; "" is the node itself."""
    node = dead_node(tmp_path); canvas = tmp_path / "canvas"; canvas.mkdir()
    (canvas / "llm.pin").write_text(f"node {node}\n")
    key = tmp_path / "keys" / "openrouter.key"; key.parent.mkdir(); key.write_text("sk-test-0000\n"); key.chmod(0o600)
    d = tmp_path / "doors" / "openrouter"; d.mkdir(parents=True)
    (d / "door").write_text(f"url  {os.environ['TEND_LLM_URL']}\nmodel  vendor/big\nkey  {key}\nadmitted  the test\n")
    monkeypatch.setenv("TEND_DOOR_DIR", str(tmp_path / "doors"))
    assert panel.doors() == ["openrouter"]
    pull_before = (node / "state" / "pull").read_text()   # the fixture's own wordless line
    assert panel.talk("llm", "hello", str(canvas), door="openrouter") == "echo<hello>"
    assert model[-1]["model"] == "vendor/big" and _Model.heads[-1] == "Bearer sk-test-0000"
    assert (node / "state" / "pull").read_text() == pull_before, "a door turn is not a pull"
    ex = panel.read_replies(str(node / "state"))
    assert ex[-1].via == "openrouter vendor/big" and ex[-1].answer == "echo<hello>"
    assert panel.talk("llm", "and you", str(canvas), door="") == "echo<and you>"
    assert "model" not in model[-1] and _Model.heads[-1] is None
    assert panel.read_replies(str(node / "state"))[-1].via == ""
    assert model[-1]["messages"][:2] == [{"role": "user", "content": "hello"}, {"role": "assistant", "content": "echo<hello>"}], "one conversation, whichever mind"
    monkeypatch.setenv("TEND_DOOR", "openrouter")
    assert panel.talk("llm", "env", str(canvas)) == "echo<env>" and model[-1]["model"] == "vendor/big"
    monkeypatch.delenv("TEND_DOOR")
    rc = panel.main(["x", "--canvas", str(canvas), "talk", "--door", "openrouter", "llm", "shell"])
    assert rc == 0 and capsys.readouterr().out.strip() == "echo<shell>" and model[-1]["model"] == "vendor/big"
    with pytest.raises(ValueError, match="no door named ghost"):
        panel.talk("llm", "x", str(canvas), door="ghost")


def test_the_panels_keys_offer_talk_and_unpin():
    """The curses loop is not driven here; what is held is that the hand
    the keys offer includes the two Henri asked for, and the bar says so."""
    src = inspect.getsource(panel._tui)
    assert "[x] unpin" in src and "[t] talk" in src
    assert 'ord("x"): ("unpin"' in src and "_talk_screen(" in src
    talk_src = inspect.getsource(panel._talk_screen)
    assert "[k] think" in talk_src and 'c == ord("k")' in talk_src and "think = not think" in talk_src
    assert "read_turn(row.state)" in talk_src, "the turn in flight is shown as it arrives"
    assert "[d] door" in talk_src and 'c == ord("d")' in talk_src and "doors()" in talk_src


def test_the_turn_in_flight_is_read_from_the_live_files(tmp_path):
    assert panel.read_turn(str(tmp_path)) == ("", "")
    (tmp_path / "turn.thinking").write_text("so far")
    assert panel.read_turn(str(tmp_path)) == ("so far", "")
    (tmp_path / "turn.answer").write_text("echo<")
    assert panel.read_turn(str(tmp_path)) == ("so far", "echo<")


def test_the_calls_a_mind_made_are_read_back_on_the_exchange_and_from_the_live_file(tmp_path):
    """card:tools.md day one: a C line per call between the Q and the A,
    read back on the exchange and shown on the talk screen; the live
    `turn.calls` while the turn is in flight; never history."""
    st = tmp_path / "st"; st.mkdir()
    (st / "replies").write_text(
        "2026-08-30 14:40 Q: look\n2026-08-30 14:40 V: openrouter vendor/x\n"
        "2026-08-30 14:40 C: ls board/ → 2 entries\n2026-08-30 14:40 C: read board/x.md → 21 chars\n"
        "2026-08-30 14:41 T: so\n2026-08-30 14:41 A: found\n\n"
        "2026-08-30 14:42 Q: plain\n2026-08-30 14:42 A: echo\n\n")
    ex = panel.read_replies(str(st))
    assert ex[0].calls == ["ls board/ → 2 entries", "read board/x.md → 21 chars"]
    assert (ex[0].thinking, ex[0].answer, ex[0].via) == ("so", "found", "openrouter vendor/x")
    assert ex[1].calls == [] and ex[1].answer == "echo"
    assert panel.history(ex) == [{"role": "user", "content": "look"}, {"role": "assistant", "content": "found"},
                                 {"role": "user", "content": "plain"}, {"role": "assistant", "content": "echo"}], "the calls are never history"
    assert panel.read_calls(str(st)) == []
    (st / "turn.calls").write_text("C: ls board/ → 2 entries\n")
    assert panel.read_calls(str(st)) == ["ls board/ → 2 entries"]
    src = inspect.getsource(panel._talk_screen)
    assert "read_calls(row.state)" in src and "[call]" in src and "'acting'" in src, "the calls are shown as the turn runs"


# ── the edges as rows (card:edge.md, 2026-09-02 — Henri: "paneeli voisi näyttää reunat riveinä") ──

def take(edge):
    """The pull as the solitaire's program takes it: a shared flock on the
    edge file, held by this process's fd — closing the fd is `stop`.  (Not
    `flock -s FILE sleep`: its child inherits the fd and keeps the lock
    after flock is killed — measured here first.)"""
    import fcntl
    fd = os.open(edge, os.O_RDONLY)
    fcntl.flock(fd, fcntl.LOCK_SH)
    return fd


def edge_tree(tmp_path):
    """A scratch tree with the edge's two nodes: `solitaire` pulls `die`,
    and the edge file is where tools/launch.sh makes it."""
    tree = tmp_path / "tree"
    die = tree / "die"; (die / "state" / "pulled").mkdir(parents=True)
    (die / "grant").write_text("pulse roll\nprogram /usr/bin/python3 die.py\n")
    sol = tree / "solitaire"; (sol / "state").mkdir(parents=True)
    (sol / "grant").write_text("pull ../die\nprogram /usr/bin/python3 solitaire.py\n")
    edge = die / "state" / "pulled" / "solitaire"; edge.write_text("")
    return tree, die, sol, edge


def test_a_pulled_node_names_its_puller_and_a_puller_says_what_it_pulls(tmp_path):
    """Both ends of an edge as words on a row: the die, pulled by a process
    and not up, is bold like a held node with no runner — the same promise,
    kept at the resolver's next visit; the solitaire's row says what it
    pulls.  The lock let go, the die's row says neither."""
    tree, die, sol, edge = edge_tree(tmp_path)
    canvas = tmp_path / "canvas"; pin(canvas, "die", die); pin(canvas, "solitaire", sol)
    fd = take(edge)
    try:
        rows = {r.name: r for r in read_canvas(canvas, tree=tree)}
        d = rows["die"]
        assert d.pulled_by == ("solitaire",) and d.pulls == ()
        assert panel.wrong(d), "a pulled node with no runner is the edge's promise not kept: bold"
        line = panel.row_line(d)
        assert "PULLED, NOT RUNNING" in line and "pulled by — solitaire" in line, line
        s = rows["solitaire"]
        assert s.pulls == ("die",) and s.pulled_by == ()
        assert "pulls — die" in panel.row_line(s) and not panel.wrong(s)
        assert "1 pulled" in panel._counts(list(rows.values()))
    finally:
        os.close(fd)   # stop: the process lets go
    d = {r.name: r for r in read_canvas(canvas, tree=tree)}["die"]
    assert d.pulled_by == () and not panel.wrong(d)
    assert "pulled by" not in panel.row_line(d), "an unlocked edge file is a trace, not a pull"


def test_a_live_edge_dates_the_pull_and_shows_the_edges_own_time(tmp_path):
    """Henri, 2026-09-03: the llm row said `pulled 08:05` — yesterday's hand
    pull from state/pull, shown with no day, on a row a process's edge holds
    up today.  Two wrongs: a time with no date reads as today, and the edge's
    own time is not the one shown.  The pull time is the live edge's mtime
    when a process holds it, and any time not today carries its date."""
    import time, re
    now = int(time.time()); old = 1787916000   # 2026-08-28, well before today
    assert re.search(r"[A-Za-z]", panel._when(old)), "a time not today carries its date"
    assert not re.search(r"[A-Za-z]", panel._when(now)), "today is the bare clock"
    tree, die, sol, edge = edge_tree(tmp_path)
    (die / "state" / "pull").write_text(f"{old} 2026-08-28 08:05 pulled by hand\n")   # the stale person-pull
    canvas = tmp_path / "canvas"; pin(canvas, "die", die)
    fd = take(edge)
    try:
        os.utime(edge, (now, now))   # the edge taken now
        r = {x.name: x for x in read_canvas(canvas, tree=tree)}["die"]
        assert r.pulled_by == ("solitaire",)
        assert r.last_pull == now, (r.last_pull, now)   # the edge's time, not the file's
        line = panel.row_line(r)
        assert "pulled by — solitaire" in line and str(old) not in line, line
        assert panel._when(old) not in line, "yesterday's hand pull is not the pull that holds it"
    finally:
        os.close(fd)
    # the lock let go: no live edge, so the person-pull file's time is what there is, and it carries its date
    r = {x.name: x for x in read_canvas(canvas, tree=tree)}["die"]
    assert r.pulled_by == () and r.last_pull == old and panel._when(old) in panel.row_line(r), panel.row_line(r)


def test_a_node_a_process_pulls_is_on_the_canvas_with_no_pin(tmp_path):
    """Alive by an edge is on the canvas, as a held node is: no pin, no
    hold, one row named by the node directory."""
    tree, die, sol, edge = edge_tree(tmp_path)
    canvas = tmp_path / "canvas"; canvas.mkdir()
    assert read_canvas(canvas, tree=tree) == []
    fd = take(edge)
    try:
        rows = read_canvas(canvas, tree=tree)
        assert [r.name for r in rows] == ["die"] and rows[0].pulled_by == ("solitaire",)
    finally:
        os.close(fd)
