#!/usr/bin/env python3
#: asked-by: Henri, 2026-08-28 — "open the interface card and build the TUI first.  I think we need it next." (card:andon-panel.md)
"""tools/andon-panel.py — the andon's person-side half: watch the record, announce a pull.

    tools/andon-panel.py            a TUI over the andon record (needs a terminal)

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
"""
import os
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


def answer(state_dir=None):
    """Clear the questions — the person's word, run through the andon."""
    env = dict(os.environ)
    if state_dir is not None:
        env["TEND_ANDON_STATE"] = str(state_dir)
    return subprocess.run(["sh", os.path.join(HERE, "andon.sh"), "answered"], env=env)


def _hhmm(epoch):
    import datetime
    return datetime.datetime.fromtimestamp(epoch).strftime("%H:%M")


def _tui(stdscr):
    import curses
    curses.curs_set(0)
    stdscr.timeout(1000)
    prev_rings = read_state().rings
    flash_until = 0
    import time
    while True:
        st = read_state()
        if st.rings > prev_rings:            # a new ring since last look
            try:
                curses.beep(); curses.flash()
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
        if not st.pending:
            stdscr.addstr(row, 2, "nothing pending — the floor is quiet.")
        else:
            stdscr.addstr(row, 2, f"{len(st.pending)} pending"
                          + (f", last ring {_hhmm(st.last_ring)}" if st.last_ring else "")
                          + ":")
            row += 2
            for q in st.pending:
                for i, chunk in enumerate([q.text[j:j + w - 6] for j in range(0, len(q.text), w - 6)] or [""]):
                    prefix = f"  {q.stamp}  " if i == 0 else " " * 4
                    if row < h - 2:
                        try:
                            stdscr.addstr(row, 2, (prefix + chunk)[:w - 3])
                        except curses.error:
                            pass
                        row += 1
                row += 1
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
    if len(argv) > 1 and argv[1] in ("-h", "--help"):
        sys.stdout.write(__doc__)
        return 0
    try:
        import curses
    except ImportError:
        sys.stderr.write("andon-panel: no curses available; the TUI needs a terminal\n")
        return 1
    if not sys.stdout.isatty():
        st = read_state()
        n = len(st.pending)
        print(f"andon-panel: {n} pending"
              + (f", pulled since {_hhmm(st.last_ring)}" if st.pulled else "")
              + " — run in a terminal for the live panel.")
        return 0
    curses.wrapper(_tui)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
