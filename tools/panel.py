#!/usr/bin/env python3
#: asked-by: Henri, 2026-08-28 — "open the interface card and build the TUI first.  I think we need it next." (card:andon-panel.md)
"""tools/panel.py — the person's panel: the canvas, the andon record, and the person's hand on both.

(tools/panel.py until 2026-08-29 — Henri: "the andon-panel.py is growing into a panel.py".
It began as the andon's person-side half, card:andon-panel.md; the canvas and the hand grew on it.)

    tools/panel.py [--canvas DIR]   a TUI over the andon record and a canvas (needs a terminal)
    tools/panel.py hold LABEL NODE [--state DIR] [WORDS...]   write LABEL.hold on the canvas, then resolve
    tools/panel.py pin NAME NODE [--state DIR]                write NAME.pin, then resolve
    tools/panel.py unhold LABEL | unpin NAME                  remove it, then resolve

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
(the panel's rule: not a second andon).

**The person's hand** (card:hold.md, 2026-08-29 — Henri: "the andon
panel should have a tool to insert .pin and .hold files to the canvas,
and allow one to remove the .hold … and the resolver is called after the
file is added.  Also, entering the andon panel should run the
resolver").  Until then this said "it never pins — a pin is the person's
act"; it still is, and the panel is where the person's hand is: `hold`,
`pin`, `unhold`, `unpin` write the canvas and nothing else, refuse a node
that is not one (no grant beside it — a BROKEN row is for a file written
by hand), and every write, and every entry to the panel, runs the
resolver once (`tools/resolve.sh`: the installed copy, the set in force,
else the tree's; TEND_RESOLVE overrides for a test), so a hold written
here is a node started here and a death is a line on this timeline
before the person looks away.  The panel writes the canvas and calls the
resolver; it does not start a program itself — the resolver is the one
thing that does, on the person's side, as before.
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


Pin = namedtuple("Pin", "name node state running cut last_pull last_stop stop_reason dead said held held_at broken note",
                 defaults=(None, None, None, None))
Event = namedtuple("Event", "epoch who text")

CANVAS_DEFAULT = os.path.join(STATE_DEFAULT, "canvas")
STALE = 60          # seconds of silent watch under a held lock: tools/launch.sh's TEND_WATCH_STALE
_NOISE = ("deprecationwarning",)


def _canvas_dir(d=None):
    return str(d) if d is not None else os.environ.get("TEND_CANVAS", CANVAS_DEFAULT)


# --- the tick (card:hold.md, 2026-08-29 — Henri: "we do need some system-tick there") ---
# A hold is kept only while something runs the resolver.  With a hand on
# it — the hook after every command, the panel on entry and on every
# write — that is the person's presence; with nobody at the desk it is a
# tick: `tools/resolve.sh --tick N` run by a carrier (a systemd user timer
# on Ubuntu, cron elsewhere), leaving `EPOCH N` beside the canvas.  The
# panel reads the stamp and says so: no tick under a hold, or a tick that
# has stopped, is a hold nothing keeps — bold, like every other row that
# is a promise not kept.

Tick = namedtuple("Tick", "at every age")


def _tick_path(canvas=None):
    return os.environ.get("TEND_TICK") or os.path.join(os.path.dirname(os.path.abspath(_canvas_dir(canvas))), "tick")


def read_tick(canvas=None):
    """The stamp, read: when the last tick was and how often one is due; None
    when there is no stamp or it is not one."""
    import time
    try:
        with open(_tick_path(canvas)) as f:
            at, every = f.read().split()[:2]
        at, every = int(at), int(every)
    except (OSError, ValueError):
        return None
    return Tick(at, every, max(0, int(time.time()) - at))


def tick_stale(t):
    return t.age > max(90, 3 * t.every)


def tick_loud(t, held):
    """Loud when the promise is not kept: a hold with no tick at all, or a
    carrier that has stopped (stale), held or not."""
    return held if t is None else tick_stale(t)


def tick_line(t, held):
    if t is None:
        if held:
            return "NO TICK — a hold is kept only while a hand runs the resolver; nothing runs it when nobody is here (tools/install.sh --tick)"
        return "no tick — nothing runs the resolver when nobody is here (tools/install.sh --tick)"
    ago = f"{t.age} s" if t.age < 120 else f"{t.age // 60} min"
    if tick_stale(t):
        return f"TICK STALE — last {ago} ago, every {t.every} s — the carrier has stopped"
    return f"tick  last {ago} ago, every {t.every} s"


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


Hold = namedtuple("Hold", "label node state words mtime path named")
ROOT = os.environ.get("TEND_TREE") or os.path.dirname(HERE)


def _node_path(word):
    """A path as a hold or a pin writes it: `~` is the person's home, a
    bare name is a node of this tree (tools/launch.sh's expand_path)."""
    word = os.path.expanduser(word)
    return word if os.path.isabs(word) else os.path.join(ROOT, word)


def _is_node(word):
    return os.path.isfile(os.path.join(_node_path(word), "grant"))


def _read_hold(path):
    """A hold, read (card:hold.md; Henri, 2026-08-29: "I'd like to name
    what I'm holding inside the file").  Pin-shaped: `node NAME-OR-DIR`,
    `state DIR` (relative to the node), or one bare line `NAME [STATE]`
    whose first word is a node of this tree; every other line is the
    words — who is holding it, and why.  No node line: the filename's
    stem is the node (`node.hold`), so the filename is otherwise a label."""
    label = os.path.basename(path)[:-len(".hold")]
    node = state = None; words = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(None, 1)
            key, val = (parts[0], parts[1] if len(parts) == 2 else "")
            if key == "node":
                node = val
            elif key == "state":
                state = val
            elif line.startswith(("/", "~", "./")):
                state = line          # a bare path line is the state (Henri, 2026-08-29: "newline and state")
            elif node is None and _is_node(key):
                node = key
                if val:
                    state = val.strip('"')
            else:
                words.append(line)
    named = node is not None   # a hold with no node line holds the node its filename names
    node = _node_path(node or label)
    if state is not None:
        state = os.path.expanduser(state)
        if not os.path.isabs(state):
            state = os.path.join(node, state)
    return Hold(label, node, state, " ".join(words) or "(no words)", int(os.stat(path).st_mtime), path, named)


def read_holds(canvas_dir=None):
    """Every `*.hold` in the canvas, in name order; a missing canvas is none."""
    d = _canvas_dir(canvas_dir)
    holds = []
    try:
        names = sorted(n for n in os.listdir(d) if n.endswith(".hold"))
    except OSError:
        return holds
    for n in names:
        try:
            holds.append(_read_hold(os.path.join(d, n)))
        except OSError:
            continue
    return holds


def _same(a, b):
    try:
        return os.path.realpath(a) == os.path.realpath(b)
    except OSError:
        return a == b


def read_hold(canvas_dir, name, node=None, state=None):
    """What holds this node with this state (card:hold.md): the words of
    every hold that names it — a hold that names no state holds the node
    with whatever state it runs — and the newest hold's mtime (the one
    `serve` measures a death against), or (None, None) when nothing does."""
    if canvas_dir is None:
        return None, None
    # a hold with no state line holds the node with its default state, node/state — the
    # pin's own rule; tools/launch.sh reads the same hold as "whatever state I run with",
    # which differs only when the launcher is given TEND_STATE_DIR (the tests' seat)
    got = [h for h in read_holds(canvas_dir)
           if (_same(h.node, node) if h.named else h.label == name)
           and (state is None or _same(h.state or os.path.join(node, "state"), state))]
    if not got:
        return None, None
    return "; ".join(h.words for h in got), max(h.mtime for h in got)


def hold_fault(h):
    """Why a hold holds nothing: its node is not a node (no grant beside
    it), or the state it names is not there.  None when it is whole."""
    if not os.path.isfile(os.path.join(h.node, "grant")):
        return f"no node at {h.node} (no grant beside it)"
    if h.state is not None and not os.path.isdir(h.state):
        return f"state {h.state} is not there"
    return None


def read_pin_state(name, node, state, canvas_dir=None):
    """One row: what the runner left in its state directory, read — and
    whether the canvas holds it."""
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
    held, held_at = read_hold(canvas_dir, name, node, state)
    note = None
    if held is not None and not _same(state, os.path.join(node, "state")):
        # the resolver runs a node with NODE/state only (tools/resolve.sh → launch.sh NODE serve), so a
        # hold on any other state is honoured by nothing yet — said here, not promised (2026-08-29)
        note = f"state {state} is not the state the resolver runs ({os.path.join(node, 'state')}); not honoured yet"
    return Pin(name, node, state, running, cut, last_pull, last_stop, reason, dead, said, held, held_at, None, note)


def read_canvas(canvas_dir=None):
    """The canvas, read: one row per `<name>.pin`, in name order, and then
    one per node a `*.hold` holds that no pin shows (card:hold.md — a
    held node is on the canvas whether or not it is pinned; its row is
    named by the node directory, the name the runner's death notice
    uses).  A missing canvas is no rows — nothing is held."""
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
            rows.append(read_pin_state(*got, canvas_dir=d))
    for h in read_holds(d):
        state = h.state or os.path.join(h.node, "state")
        if h.named and any(_same(r.node, h.node) and _same(r.state, state) for r in rows):
            continue
        if not h.named and any(r.name == h.label for r in rows):
            continue
        fault = hold_fault(h)
        if fault:
            # a hold that holds nothing is not silence: a row that says so (Henri, 2026-08-29:
            # "make sure the error becomes visible on the andon panel")
            rows.append(Pin(h.label, h.node, state, False, None, None, None, "", False, "", h.words, h.mtime, fault))
            continue
        rows.append(read_pin_state(os.path.basename(h.node.rstrip("/")), h.node, state, canvas_dir=d))
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


INSTALLED_RESOLVE = "/usr/local/lib/tend/tools/resolve.sh"


def resolver():
    """The resolver the panel runs: TEND_RESOLVE, else the installed copy —
    the set in force (tools/install.sh) — else this tree's."""
    r = os.environ.get("TEND_RESOLVE")
    if r:
        return r
    return INSTALLED_RESOLVE if os.path.exists(INSTALLED_RESOLVE) else os.path.join(HERE, "resolve.sh")


def resolve_once():
    """One visit by the resolver: every node with an unserved pull or a
    standing hold and no runner is started, on the person's side.  Returns
    what it said (stderr: one line per runner started), never raises for
    a resolver that fails — the rows show what is up."""
    env = dict(os.environ)
    env.setdefault("TEND_TREE", ROOT)
    try:
        r = subprocess.run(["sh", resolver()], env=env, capture_output=True, text=True, timeout=120)
        return (r.stderr or "").strip()
    except (OSError, subprocess.SubprocessError) as e:
        return f"resolver: {e}"


def _label_ok(label):
    if not label or "/" in label or label.startswith(".") or label != label.strip():
        raise ValueError(f"not a name for a canvas file: {label!r}")


def _node_ok(node):
    path = _node_path(node)
    if not os.path.isfile(os.path.join(path, "grant")):
        raise ValueError(f"no node at {path} (no grant beside it) — the canvas is not written")
    return path


def write_hold(label, node, state=None, words="", canvas_dir=None):
    """`LABEL.hold` on the canvas: node, state if given, and the words —
    who is holding it and why; no words is `held by <user>, from the
    panel`, so a hold written here is never wordless."""
    _label_ok(label); _node_ok(node)
    d = _canvas_dir(canvas_dir); os.makedirs(d, exist_ok=True)
    if not words:
        import getpass
        words = f"held by {getpass.getuser()}, from the panel"
    text = f"node {node}\n" + (f"state {state}\n" if state else "") + words.strip() + "\n"
    path = os.path.join(d, label + ".hold")
    with open(path, "w") as f:
        f.write(text)
    return path


def write_pin(name, node, state=None, canvas_dir=None):
    _label_ok(name); _node_ok(node)
    d = _canvas_dir(canvas_dir); os.makedirs(d, exist_ok=True)
    path = os.path.join(d, name + ".pin")
    with open(path, "w") as f:
        f.write(f"node {node}\n" + (f"state {state}\n" if state else ""))
    return path


def remove_canvas_file(label, kind, canvas_dir=None):
    _label_ok(label)
    path = os.path.join(_canvas_dir(canvas_dir), f"{label}.{kind}")
    try:
        os.remove(path)
    except FileNotFoundError:
        raise ValueError(f"no {kind} named {label} on {_canvas_dir(canvas_dir)}")
    return path


def hand(verb, args, canvas_dir=None):
    """The person's hand on the canvas, as one call: do the verb, then
    resolve.  Returns the lines to show; raises ValueError for a refusal
    (nothing written, the resolver not run)."""
    state = None; rest = []
    i = 0
    while i < len(args):
        if args[i] == "--state" and i + 1 < len(args):
            state = args[i + 1]; i += 2
        elif args[i].startswith("--state="):
            state = args[i][len("--state="):]; i += 1
        else:
            rest.append(args[i]); i += 1
    if verb == "hold":
        if len(rest) < 2:
            raise ValueError("hold LABEL NODE [--state DIR] [WORDS...]")
        path = write_hold(rest[0], rest[1], state, " ".join(rest[2:]), canvas_dir)
        lines = [f"held: {path}"]
    elif verb == "pin":
        if len(rest) != 2:
            raise ValueError("pin NAME NODE [--state DIR]")
        path = write_pin(rest[0], rest[1], state, canvas_dir)
        lines = [f"pinned: {path}"]
    elif verb in ("unhold", "unpin"):
        if len(rest) != 1:
            raise ValueError(f"{verb} NAME")
        path = remove_canvas_file(rest[0], verb[2:], canvas_dir)
        lines = [f"removed: {path}"]
    else:
        raise ValueError(f"unknown verb {verb!r} — hold, pin, unhold, unpin")
    said = resolve_once()
    lines += [f"resolver: {l}" for l in said.splitlines()] if said else ["resolver: nothing to start"]
    return lines


VERBS = ("hold", "pin", "unhold", "unpin")


def _counts(rows):
    held = sum(1 for r in rows if r.held is not None)
    broken = sum(1 for r in rows if r.broken)
    return f"{len(rows)} on it, {held} held" + (f", {broken} BROKEN" if broken else "")


def wrong(p):
    """Is this row something gone wrong — shown bold: a death, cut cords, a
    hold that holds nothing, or a held node with no runner up (the hold's
    promise is not kept, whatever the reason)."""
    return bool(p.dead or p.cut or p.broken or p.note or (p.held is not None and not p.running))


def row_line(p):
    """A pin's row, as one line."""
    if p.broken:
        return f"{p.name.ljust(10)}BROKEN hold — {p.broken}  ({p.held})"
    if p.cut:
        state = f"runner up, watcher silent {p.cut // 60} min — the cords are cut"
    elif p.running:
        state = "running"
    elif p.note:
        state = f"HELD, NOT HONOURED — {p.note}"
    elif p.held is not None:
        # held and not up is the hold not kept (card:hold.md): say which way
        if p.dead and p.held_at is not None and p.last_stop is not None and p.held_at <= p.last_stop:
            state = "DEAD, HELD — the hold is older than the death; touch it to restart"
        elif p.dead:
            state = "DEAD, HELD — the resolver restarts it at its next visit"
        else:
            state = "HELD, NOT RUNNING — no runner up; the resolver starts one at its next visit"
    elif p.dead:
        state = "DEAD"
    else:
        state = "not running"
    bits = [p.name.ljust(10), state]
    if p.held is not None:
        bits.append(f"held — {p.held}")   # the canvas's standing pull: it is restarted when it stops (card:hold.md)
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

    def ask(prompt):
        """One line typed at the bottom; empty is a change of mind."""
        try:
            stdscr.addstr(h - 1, 0, (" " + prompt + " ").ljust(w - 1), curses.A_REVERSE)
            stdscr.refresh()
            curses.echo(); curses.curs_set(1); stdscr.timeout(-1)
            got = stdscr.getstr(h - 1, len(prompt) + 2, max(1, w - len(prompt) - 4)).decode(errors="replace").strip()
        except (curses.error, KeyboardInterrupt):
            got = ""
        finally:
            curses.noecho(); curses.curs_set(0); stdscr.timeout(1000)
        return got

    notice = ""   # what the hand last did, shown until the next keystroke

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
            put(row, 2, f"canvas {short} — {_counts(pins)}", curses.A_BOLD); row += 1
            for p in pins:
                attr = curses.A_BOLD if wrong(p) else 0
                put(row, 4, row_line(p), attr); row += 1
        else:
            put(row, 2, f"canvas {short} — nothing pinned", curses.A_DIM); row += 1
        # the tick: is anything keeping the holds when nobody is here
        held = any(p.held is not None for p in pins)
        t = read_tick(canvas_dir)
        put(row, 4, tick_line(t, held), curses.A_BOLD if tick_loud(t, held) else curses.A_DIM); row += 1
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
        if notice:
            put(h - 2, 2, notice, curses.A_BOLD)
        try:
            stdscr.addstr(h - 1, 0,
                          " [h] hold  [p] pin  [u] unhold  [a] answer all  [r] resolve  [q] quit ".ljust(w - 1),
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
        elif c in (ord("h"), ord("p"), ord("u")):
            # the person's hand: one typed line, the verb's own words, then the resolver
            verb, prompt = {ord("h"): ("hold", "hold LABEL NODE [--state DIR] [WORDS...]:"),
                            ord("p"): ("pin", "pin NAME NODE [--state DIR]:"),
                            ord("u"): ("unhold", "unhold LABEL:")}[c]
            line = ask(prompt)
            if line:
                try:
                    notice = " · ".join(hand(verb, line.split(), canvas_dir))
                except ValueError as e:
                    notice = f"refused: {e}"
            stdscr.clear()
        elif c == ord("r"):
            said = resolve_once()
            notice = "resolver: " + (said.replace("\n", " · ") if said else "nothing to start")
        elif c != -1:
            notice = ""
        # the timeout just loops and re-reads


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
        elif a in VERBS:
            # the person's hand, from a shell: write the canvas, then resolve
            try:
                for line in hand(a, args, canvas):
                    print(line)
                return 0
            except ValueError as e:
                sys.stderr.write(f"andon-panel: {e}\n")
                return 2
        else:
            sys.stderr.write(f"andon-panel: unknown argument {a!r}\n")
            return 2
    try:
        import curses
    except ImportError:
        sys.stderr.write("andon-panel: no curses available; the TUI needs a terminal\n")
        return 1
    # entering the panel runs the resolver once (Henri, 2026-08-29): a held node with no
    # runner is started before the first look, and its row says running or why not
    said = resolve_once()
    if not sys.stdout.isatty():
        st = read_state()
        pins = read_canvas(canvas)
        for line in said.splitlines():
            print(f"resolver: {line}")
        n = len(st.pending)
        print(f"andon-panel: {n} pending"
              + (f", pulled since {_hhmm(st.last_ring)}" if st.pulled else "")
              + " — run in a terminal for the live panel.")
        print(f"canvas {_canvas_dir(canvas)} — {_counts(pins)}")
        for p in pins:
            print("  " + row_line(p))
        print("  " + tick_line(read_tick(canvas), any(p.held is not None for p in pins)))
        for e in read_log(None, pins)[-5:]:
            print("  " + event_line(e))
        return 0
    curses.wrapper(_tui, canvas)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
