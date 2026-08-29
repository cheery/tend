#!/usr/bin/env python3
#: asked-by: Henri, 2026-08-28 — "open the interface card and build the TUI first.  I think we need it next." (card:andon-panel.md)
"""tools/andon-panel.py — the andon's person-side half: watch the record, announce a pull.

    tools/andon-panel.py [--canvas DIR]   a TUI over the andon record and a canvas (needs a terminal)

The panel runs OUTSIDE the fence and only reads what a session writes —
`andon.pending` (the questions) and `andon.log` (every ask, ring and
answer) under ~/.local/state/tend, which the fence binds writable to a
session.  So a fenced session pulls the cord by writing the record,
needing no `audio`/`display`/`bus` reach at all, and this announces it
on the person's side, through a channel the session never touches
(card:andon-panel.md, card:silent-cord.md).

It does not write the record; the one exception is `answered`, the
person's word, run through `tools/andon.sh answered` — never something
a session can reach.

**The canvas** (card:canvas.md, 2026-08-28).  At 13:27 Henri pulled the
llm node and llama-server died a second later at the loader; `pull` said
"started", `stopped` said `exited 127`, the log said why, and he saw
none of it — a pulled node's death was a line in a file nobody was
looking at.  A *pin* is the person's "I am holding this": a file
`<name>.pin` in a canvas directory, on the person's side, a line or two —

    node  /path/to/NODE            the node directory
    state /path/to/state           only if it is not NODE/state

There can be many canvases (this desk, a server); which one the panel
looks at is a path — `--canvas DIR`, TEND_CANVAS, else
~/.local/state/tend/canvas.  The panel shows one row per pin from what
the runner leaves (`run.lock` held = running; `stopped`, its mtime the
last stop and its line the reason; `watch`, a stale heartbeat under a
held lock = the cords are cut, the same rule `tools/launch.sh status`
reads) and shows the death notice a runner writes into the record as it
dies (tools/launch.sh, card:canvas.md day two) in the log column beside
the andon's own lines, one timeline.  It shows; it never rings for a death
(the panel's rule: not a second andon), and it never pins — a pin is the
person's act.
"""
import os
import re
import subprocess
import sys
from collections import namedtuple

HERE = os.path.dirname(os.path.abspath(__file__))
STATE_DEFAULT = os.path.join(os.path.expanduser("~"), ".local", "state", "tend")

Question = namedtuple("Question", "stamp text")
State = namedtuple("State", "pending rings last_ring pulled answered")


def _state_dir(d=None):
    return str(d) if d is not None else os.environ.get("TEND_ANDON_STATE", STATE_DEFAULT)


def read_state(state_dir=None):
    """The record, read: the pending questions, the count of rings (a new
    one is how the view knows to sound), the last ring's time unless an
    answer has cleared it, and whether the cord is pulled — pending with a
    ring since the last answer, the same rule `tools/andon.sh pulled` uses."""
    d = _state_dir(state_dir)
    pending = []
    try:
        with open(os.path.join(d, "andon.pending")) as f:
            for line in f:
                line = line.rstrip("\n")
                if not line:
                    continue
                parts = line.split(maxsplit=2)
                if len(parts) >= 3:
                    pending.append(Question(parts[0] + " " + parts[1], parts[2]))
                else:
                    pending.append(Question("", line))
    except FileNotFoundError:
        pass

    rings = 0
    answered = 0
    last_ring = None
    try:
        with open(os.path.join(d, "andon.log")) as f:
            for line in f:
                parts = line.split(maxsplit=3)
                if len(parts) < 4:
                    continue
                epoch, kind = parts[0], parts[3].split()[0]
                # a ring that could not sound (ring-failed, inside the fence:
                # card:silent-cord.md) is still a pull the panel must announce
                if kind in ("ring", "ring-failed"):
                    rings += 1
                    try:
                        last_ring = int(epoch)
                    except ValueError:
                        pass
                elif kind == "answered":
                    answered += 1
                    last_ring = None
    except FileNotFoundError:
        pass

    pulled = bool(pending) and last_ring is not None
    return State(pending, rings, last_ring, pulled, answered)


Pin = namedtuple("Pin", "name node state running cut last_pull last_stop stop_reason dead said")
Event = namedtuple("Event", "epoch who text")

CANVAS_DEFAULT = os.path.join(STATE_DEFAULT, "canvas")
STALE = 60          # seconds of silent watch under a held lock: tools/launch.sh's TEND_WATCH_STALE
_NOISE = ("deprecationwarning",)


def _canvas_dir(d=None):
    return str(d) if d is not None else os.environ.get("TEND_CANVAS", CANVAS_DEFAULT)


def _lock_held(path):
    """The runner's lock, tested the way `flock -n LOCK true` tests it — taken
    for an instant and let go.  A lock file that is not there is a node that
    never ran; this never creates it."""
    import fcntl
    try:
        fd = os.open(path, os.O_RDONLY)
    except OSError:
        return False
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        fcntl.flock(fd, fcntl.LOCK_UN)
        return False
    except OSError:
        return True
    finally:
        os.close(fd)


def _last_said(log):
    """The log's last line that is not warning noise — what the program said
    as it died (the same filter tools/launch.sh's last_said applies)."""
    said = ""
    try:
        with open(log, errors="replace") as f:
            for line in f:
                line = line.rstrip("\n")
                if not line.strip() or line.lstrip().startswith("class "):
                    continue
                if any(n in line.lower() for n in _NOISE):
                    continue
                said = line
    except OSError:
        pass
    return said


def _read_pin(path):
    name = os.path.basename(path)[:-len(".pin")]
    node = state = None
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(None, 1)
            if len(parts) == 2 and parts[0] in ("node", "state"):
                key, val = parts
            else:
                key, val = ("node" if node is None else "state"), line
            val = os.path.expanduser(val)
            if key == "node":
                node = val
            else:
                state = val
    if node is None:
        return None
    if state is None:
        state = os.path.join(node, "state")
    return name, node, state


def read_pin_state(name, node, state):
    """One row: what the runner left in its state directory, read."""
    import time
    running = _lock_held(os.path.join(state, "run.lock"))
    cut = None
    if running:
        try:
            silent = int(time.time() - os.stat(os.path.join(state, "watch")).st_mtime)
            if silent >= int(os.environ.get("TEND_WATCH_STALE", STALE)):
                cut = silent
        except OSError:
            pass
    last_pull = None
    try:
        with open(os.path.join(state, "pull")) as f:
            for line in f:
                head = line.split(None, 1)[0] if line.strip() else ""
                if head.isdigit():
                    last_pull = int(head)
    except OSError:
        pass
    last_stop = None; reason = ""; dead = False
    try:
        stopped = os.path.join(state, "stopped")
        last_stop = int(os.stat(stopped).st_mtime)
        with open(stopped) as f:
            reason = f.readline().rstrip("\n")
        m = re.match(r"exited (\d+)", reason)
        dead = bool(m) and m.group(1) != "0"
    except OSError:
        pass
    said = _last_said(os.path.join(state, "log")) if dead else ""
    return Pin(name, node, state, running, cut, last_pull, last_stop, reason, dead, said)


def read_canvas(canvas_dir=None):
    """The canvas, read: one row per `<name>.pin`, in name order.  A missing
    canvas is no rows — nothing is held."""
    d = _canvas_dir(canvas_dir)
    rows = []
    try:
        names = sorted(n for n in os.listdir(d) if n.endswith(".pin"))
    except OSError:
        return rows
    for n in names:
        try:
            got = _read_pin(os.path.join(d, n))
        except OSError:
            continue
        if got:
            rows.append(read_pin_state(*got))
    return rows


def read_log(state_dir=None, pins=()):
    """One timeline: every line of the andon record — ask, ring, answered,
    and a pinned runner's death notice — in time order.  A death is a
    line the runner's own stop path wrote as it died (tools/launch.sh,
    `<name>: exited <rc> — <reason>`; card:canvas.md day two), so it is
    on the timeline whenever it happened and survives the next clean
    stop; the who-column is the pin's name, read off the prefix.  Day
    one merged the pin's `stopped` in here at view time and lost it at
    the next clean stop (§17:30); the record keeps it, so the merge is
    gone.  A clean stop — idle, the sitting, exit 0 — is the row's last
    stop and not an event here: the log column is for what went wrong."""
    d = _state_dir(state_dir)
    names = {p.name for p in pins}
    events = []
    try:
        with open(os.path.join(d, "andon.log")) as f:
            for line in f:
                parts = line.rstrip("\n").split(maxsplit=3)
                if len(parts) < 4 or not parts[0].isdigit():
                    continue
                text = parts[3]
                who = text.split(":", 1)[0] if ":" in text else ""
                events.append(Event(int(parts[0]), who if who in names else "andon", text))
    except OSError:
        pass
    events.sort(key=lambda e: e.epoch)
    return events


def row_line(p):
    """A pin's row, as one line."""
    if p.cut:
        state = f"runner up, watcher silent {p.cut // 60} min — the cords are cut"
    elif p.running:
        state = "running"
    elif p.dead:
        state = "DEAD"
    else:
        state = "not running"
    bits = [p.name.ljust(10), state]
    if p.last_pull:
        bits.append(f"pulled {_hhmm(p.last_pull)}")
    if p.last_stop:
        bits.append(f"stopped {_hhmm(p.last_stop)}" + (f" — {p.stop_reason}" if p.stop_reason else ""))
    return "  ".join(bits)


def event_line(e):
    return f"{_hhmm(e.epoch)}  {e.who.ljust(6)} {e.text}"


def answer(state_dir=None):
    """Clear the questions — the person's word, run through the andon."""
    env = dict(os.environ)
    if state_dir is not None:
        env["TEND_ANDON_STATE"] = str(state_dir)
    return subprocess.run(["sh", os.path.join(HERE, "andon.sh"), "answered"], env=env)


def _hhmm(epoch):
    import datetime
    return datetime.datetime.fromtimestamp(epoch).strftime("%H:%M")


def _write_tone(path):
    """The andon's two-note tone (tools/andon.sh), written with wave —
    the panel plays the same sound the cord means."""
    import math, struct, wave
    rate = 22050

    def tone(f, secs, vol=0.35):
        n = int(rate * secs)
        for i in range(n):
            env = min(1.0, i / (rate * 0.02), (n - i) / (rate * 0.10))
            yield vol * env * math.sin(2 * math.pi * f * i / rate)

    samples = list(tone(660, 0.30)) + [0.0] * int(rate * 0.05) + list(tone(880, 0.45))
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate)
        w.writeframes(b"".join(struct.pack("<h", int(x * 32767)) for x in samples))
    return path


def _play_alert(player=None):
    """Make an actual sound on a new pull.  The panel is outside the fence,
    so a real player reaches the socket the fenced andon could not
    (card:silent-cord.md).  curses.beep is the terminal bell and many
    terminals mute it — this plays the tone instead, and returns whether
    it reached a player."""
    import os, shutil, subprocess, tempfile
    fd, path = tempfile.mkstemp(suffix=".wav"); os.close(fd)
    try:
        _write_tone(path)
        candidates = [player] if player else [
            os.environ.get("TEND_PANEL_PLAYER"), "pw-play", "paplay", "aplay"]
        for c in candidates:
            if not c:
                continue
            exe = c if os.sep in c else shutil.which(c)
            if not exe:
                continue
            try:
                if subprocess.run([exe, path], stdout=subprocess.DEVNULL,
                                  stderr=subprocess.DEVNULL).returncode == 0:
                    return True
            except OSError:
                continue
        return False
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass


def _tui(stdscr, canvas=None):
    import curses
    curses.curs_set(0)
    stdscr.timeout(1000)
    prev_rings = read_state().rings
    flash_until = 0
    import time
    canvas_dir = _canvas_dir(canvas)

    def put(y, x, text, attr=0):
        if 0 <= y < h - 1:
            try:
                stdscr.addstr(y, x, text[:max(0, w - x - 1)], attr)
            except curses.error:
                pass

    while True:
        st = read_state()
        pins = read_canvas(canvas_dir)
        events = read_log(None, pins)
        if st.rings > prev_rings:            # a new ring since last look
            if not _play_alert():            # a real tone; the terminal bell is muted too often
                try:
                    curses.beep()
                except curses.error:
                    pass
            try:
                curses.flash()
            except curses.error:
                pass
            flash_until = time.time() + 3
        prev_rings = st.rings

        stdscr.erase()
        h, w = stdscr.getmaxyx()
        hot = time.time() < flash_until
        title = " tend andon " + ("— PULLED " if st.pulled else "")
        try:
            stdscr.addstr(0, 0, title.ljust(w - 1),
                          curses.A_REVERSE | (curses.A_BLINK if hot else 0))
        except curses.error:
            pass
        row = 2
        # the canvas: what the person is holding, one row per pin
        short = canvas_dir.replace(os.path.expanduser("~"), "~", 1)
        if pins:
            put(row, 2, f"canvas {short} — {len(pins)} pinned", curses.A_BOLD); row += 1
            for p in pins:
                attr = curses.A_BOLD if (p.dead or p.cut) else 0
                put(row, 4, row_line(p), attr); row += 1
        else:
            put(row, 2, f"canvas {short} — nothing pinned", curses.A_DIM); row += 1
        row += 1
        if not st.pending:
            put(row, 2, "nothing pending — the floor is quiet."); row += 1
        else:
            put(row, 2, f"{len(st.pending)} pending"
                + (f", last ring {_hhmm(st.last_ring)}" if st.last_ring else "")
                + ":", curses.A_BOLD)
            row += 2
            for q in st.pending:
                for i, chunk in enumerate([q.text[j:j + w - 6] for j in range(0, len(q.text), w - 6)] or [""]):
                    prefix = f"  {q.stamp}  " if i == 0 else " " * 4
                    put(row, 2, prefix + chunk); row += 1
                row += 1
        # the andon/log: one timeline, the newest at the bottom, what fits
        row += 1
        room = h - 2 - row
        if room >= 2:
            put(row, 2, "log", curses.A_BOLD); row += 1
            for e in events[-(room - 1):]:
                put(row, 4, event_line(e), curses.A_BOLD if e.who != "andon" else 0); row += 1
        try:
            stdscr.addstr(h - 1, 0,
                          " [a] answer all   [r] refresh   [q] quit ".ljust(w - 1),
                          curses.A_REVERSE)
        except curses.error:
            pass
        stdscr.refresh()

        try:
            c = stdscr.getch()
        except KeyboardInterrupt:
            break
        if c in (ord("q"), 27):
            break
        if c == ord("a") and st.pending:
            curses.endwin()
            answer()
            stdscr.clear()
        # 'r' and timeout both just loop and re-read


def main(argv):
    canvas = None
    args = list(argv[1:])
    while args:
        a = args.pop(0)
        if a in ("-h", "--help"):
            sys.stdout.write(__doc__)
            return 0
        if a == "--canvas" and args:
            canvas = args.pop(0)
        elif a.startswith("--canvas="):
            canvas = a[len("--canvas="):]
        else:
            sys.stderr.write(f"andon-panel: unknown argument {a!r}\n")
            return 2
    try:
        import curses
    except ImportError:
        sys.stderr.write("andon-panel: no curses available; the TUI needs a terminal\n")
        return 1
    if not sys.stdout.isatty():
        st = read_state()
        pins = read_canvas(canvas)
        n = len(st.pending)
        print(f"andon-panel: {n} pending"
              + (f", pulled since {_hhmm(st.last_ring)}" if st.pulled else "")
              + " — run in a terminal for the live panel.")
        print(f"canvas {_canvas_dir(canvas)} — {len(pins)} pinned")
        for p in pins:
            print("  " + row_line(p))
        for e in read_log(None, pins)[-5:]:
            print("  " + event_line(e))
        return 0
    curses.wrapper(_tui, canvas)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
