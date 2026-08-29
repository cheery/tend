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
