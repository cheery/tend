#!/usr/bin/env python3
#: asked-by: Henri, 2026-08-28 — "open the interface card and build the TUI first.  I think we need it next." (card:andon-panel.md)
"""tools/panel.py — the person's panel: the canvas, the andon record, and the person's hand on both.

(tools/panel.py until 2026-08-29 — Henri: "the andon-panel.py is growing into a panel.py".
It began as the andon's person-side half, card:andon-panel.md; the canvas and the hand grew on it.)

    tools/panel.py [--canvas DIR]   a TUI over the andon record and a canvas (needs a terminal)
    tools/panel.py hold LABEL NODE [--state DIR] [WORDS...]   write LABEL.hold on the canvas, then resolve
    tools/panel.py pin NAME NODE [--state DIR]                write NAME.pin, then resolve
    tools/panel.py unhold LABEL | unpin NAME                  remove it, then resolve
    tools/panel.py talk [--think] [--door DOOR] NAME WORDS... one turn with the node NAME names on the canvas; the reply printed

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

**Talking to a node** (2026-08-30 — Henri: "I'd like if the .hold node
could deploy some sort of user interface for node in the tools/panel.py,
maybe text input with prompt, so that I can truly talk with the model").
`[t]` on a row, or `talk NAME WORDS...` from a shell, is one turn with
the node the canvas names: the words go through `tools/deliver.sh` —
the carrier a pull's words already take — so the ask is a line in the
node's pull file and the reply an entry in its `replies`, the record the
node keeps; the panel keeps no transcript of its own and reads that one
back as the conversation.  The exchanges so far ride along as history
(`TEND_HISTORY`, the last TALK_TURNS), so the model answers in the
conversation and not cold.  A turn runs in the background and the
screen keeps time — a cold node loads for a minute — and a turn in
flight lands in the record whether or not anyone stays to watch.  The
panel is outside the fence, so it reaches the port; inside, deliver.sh
records the ask and says the runner's side delivers it, and the talk
says that back.  **Thinking** (2026-08-30 — Henri: "can I enable
thinking for the model somehow?"): `[k]` on the talk screen, `--think`
from a shell, or TEND_THINK in the panel's environment, asks the model
to reason before it answers (deliver.sh's TEND_THINK); the reasoning is
a `T:` line in `replies`, shown dim under the question and never fed
back as history.  **Streaming** (2026-08-30 — Henri: "I'd like the
model to stream it's output, so that I can see where it's going in its
work"): deliver.sh writes each token as it arrives to `turn.thinking`
and `turn.answer` beside the node's record, and the talk screen shows
them under the question while the turn is in flight — the thinking
dim, the answer as it grows — so the person watches the model work
rather than a timer.  **The calls** (2026-08-30, card:tools.md day
one): a mind with tools acts, and every act is a `C:` line — in the
record between the Q and the A, and in `turn.calls` as it happens —
shown as `[call] read board/lander.md → 8.7k chars`, on the exchange
and while the turn is in flight; the calls are never history.  **A door** (2026-08-30 — Henri: "I now have the
openrouter available for use"): `[d]` on the talk screen cycles the
turn's mind — the node, then each door under `doors/` — and `--door
NAME` from a shell, or TEND_DOOR, is the same; the turn goes through
deliver.sh's TEND_DOOR, the exchange carries the door's name and model,
and the screen labels the answer with the door.  The conversation is
still the node's record, one file, whichever mind answered each turn.
"""
import os
import re
import subprocess
import sys
import time
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


Pin = namedtuple("Pin", "name node state running cut last_pull last_stop stop_reason dead said held held_at broken note pulled_by pulls",
                 defaults=(None, None, None, None, (), ()))
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


LOCK_WINDOW = 0.1


def _lock_held(path, window=LOCK_WINDOW):
    """Is the lock held?  Tested the way `flock -n LOCK true` tests it — taken
    for an instant and let go — but across a window, not once: a test takes
    the lock to test it, so one read collides with any other reader's and
    says held of a free lock about half the time under a loop of readers
    (F019, F020, card:lock-test.md — launch.sh's `held`, polled instead of
    waited: a poll samples independent instants, where a blocking wait is
    woken at the very instant the next reader is runnable too, and 50 ms of
    polling read a hammered free lock as held 0 of 1200 times under load;
    100 ms is the margin).  A momentary reader is gone within a
    millisecond; a real holder holds for seconds.  Free the instant a try
    succeeds; held only if every try in the window fails.  A lock file that
    is not there is a node that never ran; this never creates it."""
    import fcntl
    try:
        fd = os.open(path, os.O_RDONLY)
    except OSError:
        return False
    try:
        end = time.monotonic() + window
        while True:
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                fcntl.flock(fd, fcntl.LOCK_UN)
                return False
            except OSError:
                if time.monotonic() >= end:
                    return True
                time.sleep(0.001)
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


# --- the edges (card:edge.md, 2026-09-02 — Henri: "paneeli voisi näyttää reunat riveinä.. vasta
# graafisessa ympäristössä se voi näyttää sugiyama-graafin") ---
# A node's pull is a shared flock its process holds on NODE/state/pulled/<puller>, and the
# puller's grant says `pull NODE`.  The panel reads both ends as words on a row — `pulled by`
# on the pulled node, `pulls` on the puller — and a node a process pulls is on the canvas
# whether or not it is pinned, as a held node is.  The graph drawn as a graph (layered, Sugiyama)
# is the graphical canvas's, `later/canvas-windows.md`; a terminal shows rows.

def _edge_path(word, node):
    """A `pull` value as tools/launch.sh's pull_path reads it: `./x` or `../x`
    is beside the node whose grant says it; else a bare name is a node of
    this tree and `/x` is a path."""
    if word.startswith("./") or word.startswith("../"):
        return os.path.join(node, word)
    return _node_path(word)


def read_pulls(node):
    """What this node's grant pulls: its `pull` lines whose value has a
    grant beside it, by name.  A `pull` value with no grant is the pull
    file, the word's older meaning, and is not an edge."""
    out = []
    try:
        with open(os.path.join(node, "grant")) as f:
            for line in f:
                if line.startswith("pull "):
                    p = _edge_path(line[5:].strip(), node)
                    if os.path.isfile(os.path.join(p, "grant")):
                        out.append(os.path.basename(os.path.realpath(p)))
    except OSError:
        pass
    return tuple(out)


def read_pulled_by(state):
    """Who holds an edge on this node: the files under state/pulled/ some
    process has a flock on; the filename is the puller.  An unlocked file
    is the trace of an edge that was, like `stopped`."""
    d = os.path.join(state, "pulled")
    try:
        names = sorted(os.listdir(d))
    except OSError:
        return ()
    return tuple(n for n in names if _lock_held(os.path.join(d, n)))


def pulled_nodes(tree=None):
    """Every node of the tree some process is pulling right now, with its
    default state — the resolver's (NODE/state)."""
    root = tree or ROOT
    out = []
    try:
        names = sorted(os.listdir(root))
    except OSError:
        return out
    for n in names:
        node = os.path.join(root, n)
        if os.path.isfile(os.path.join(node, "grant")) and read_pulled_by(os.path.join(node, "state")):
            out.append(node)
    return out


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
    pulled_by = read_pulled_by(state)
    if pulled_by:
        # a live edge is what holds the node up now; its time is the edge file's, not the
        # person's `pull` file, which may be an old hand pull (Henri, 2026-09-03: `pulled 08:05`
        # was yesterday's, on a row a process holds today)
        edge_at = None
        for puller in pulled_by:
            try:
                m = int(os.stat(os.path.join(state, "pulled", puller)).st_mtime)
                edge_at = m if edge_at is None else max(edge_at, m)
            except OSError:
                pass
        if edge_at is not None:
            last_pull = edge_at
    said = _last_said(os.path.join(state, "log")) if dead else ""
    held, held_at = read_hold(canvas_dir, name, node, state)
    note = None
    if held is not None and not _same(state, os.path.join(node, "state")):
        # the resolver runs a node with NODE/state only (tools/resolve.sh → launch.sh NODE serve), so a
        # hold on any other state is honoured by nothing yet — said here, not promised (2026-08-29)
        note = f"state {state} is not the state the resolver runs ({os.path.join(node, 'state')}); not honoured yet"
    return Pin(name, node, state, running, cut, last_pull, last_stop, reason, dead, said, held, held_at, None, note,
               pulled_by, read_pulls(node))


def read_canvas(canvas_dir=None, tree=None):
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
    # and one per node a process pulls that no row shows (card:edge.md): alive by an edge, on the canvas
    for node in pulled_nodes(tree):
        state = os.path.join(node, "state")
        if any(_same(r.node, node) and _same(r.state, state) for r in rows):
            continue
        rows.append(read_pin_state(os.path.basename(node), node, state, canvas_dir=d))
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


# --- talk (2026-08-30 — Henri: "so that I can truly talk with the model") ---
Exchange = namedtuple("Exchange", "stamp question answer thinking via calls")
_Q = re.compile(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}) Q: (.*)$")
_A = re.compile(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}) A: (.*)$")
_T = re.compile(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}) T: (.*)$")
_V = re.compile(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}) V: (.*)$")
_C = re.compile(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}) C: (.*)$")
TALK_TURNS = 8   # exchanges that ride along as history — the node's context is small (llm/grant)


def read_replies(state):
    """The node's `replies`, read back as exchanges, oldest first.
    tools/deliver.sh writes one as a Q line, a V line when a door
    answered (`door model`), a C line per call the mind made (the act
    and what it got), a T line when the model was asked to think,
    an A line — the thinking and the answer may run on for lines — and a
    blank; no file is no exchanges."""
    out = []
    try:
        with open(os.path.join(state, "replies")) as f:
            lines = f.read().splitlines()
    except OSError:
        return out
    q = None; a = None; t = None; v = ""; c = []

    def flush():
        out.append(Exchange(q[0], q[1], "\n".join(a or []).strip(), "\n".join(t or []).strip(), v, list(c)))

    for line in lines:
        m = _Q.match(line)
        if m:
            if q is not None:
                flush()
            q = (m.group(1), m.group(2)); a = None; t = None; v = ""; c = []
            continue
        if q is not None and a is None:
            m = _A.match(line)
            if m:
                a = [m.group(2)]
                continue
            m = _T.match(line)
            if m and t is None:
                t = [m.group(2)]
                continue
            m = _V.match(line)
            if m and t is None:
                v = m.group(2)
                continue
            m = _C.match(line)
            if m and t is None:
                c.append(m.group(2))
                continue
        if a is not None:
            a.append(line)
        elif t is not None:
            t.append(line)
    if q is not None:
        flush()
    return out


def history(exchanges, turns=TALK_TURNS):
    """The last `turns` exchanges as the messages deliver.sh prepends."""
    msgs = []
    for e in exchanges[-turns:] if turns > 0 else []:
        msgs.append({"role": "user", "content": e.question})
        msgs.append({"role": "assistant", "content": e.answer})
    return msgs


def read_turn(state):
    """The turn in flight, as far as it has come: what deliver.sh has
    written so far to the two live files; nothing when there is none."""
    out = []
    for n in ("turn.thinking", "turn.answer"):
        try:
            with open(os.path.join(state, n)) as f:
                out.append(f.read())
        except OSError:
            out.append("")
    return tuple(out)


def read_calls(state):
    """The calls the turn in flight has made so far — deliver.sh's
    `turn.calls`, one `C: ` line per call; nothing when there is none."""
    try:
        with open(os.path.join(state, "turn.calls")) as f:
            return [l[3:] if l.startswith("C: ") else l for l in f.read().splitlines() if l]
    except OSError:
        return []


def doors():
    """The doors a turn may go through: each directory under doors/
    (TEND_DOOR_DIR) with a `door` file, by name.  tools/door.sh reads one."""
    d = os.environ.get("TEND_DOOR_DIR") or os.path.join(ROOT, "doors")
    try:
        names = sorted(os.listdir(d))
    except OSError:
        return []
    return [n for n in names if os.path.isfile(os.path.join(d, n, "door"))]


def find_row(name, canvas_dir=None):
    """The row NAME names on the canvas — a pin's name, or a hold's node."""
    rows = read_canvas(canvas_dir)
    for r in rows:
        if r.name == name:
            return r
    have = ", ".join(r.name for r in rows) or "none"
    raise ValueError(f"nothing named {name} on {_canvas_dir(canvas_dir)} — the rows are: {have}")


def talk(name, words, canvas_dir=None, timeout=900, think=None, door=None):
    """One turn with the node NAME names on the canvas: the words go
    through tools/deliver.sh — a pull line, the model asked, the reply in
    `replies` — with the conversation so far as history.  `think` True
    asks the model to reason first (deliver.sh's TEND_THINK), False asks
    it not to, None leaves the environment's word.  `door` names a door
    the turn goes through instead of the node's port (deliver.sh's
    TEND_DOOR); "" is the node itself; None is the environment's word.
    Returns the answer;
    raises ValueError with deliver's own words when no reply landed (the
    node is down and would not start; inside the fence, where the ask is
    recorded and nothing delivers)."""
    import json
    words = " ".join(words.split())
    if not words:
        raise ValueError("nothing to say")
    row = find_row(name, canvas_dir)
    before = len(read_replies(row.state))
    env = dict(os.environ)
    env["TEND_STATE_DIR"] = row.state
    env["TEND_HISTORY"] = json.dumps(history(read_replies(row.state)))
    if think is True:
        env["TEND_THINK"] = "1"
    elif think is False:
        env.pop("TEND_THINK", None)
    if door is not None:
        if door:
            env["TEND_DOOR"] = door
        else:
            env.pop("TEND_DOOR", None)
    try:
        p = subprocess.run(["sh", os.path.join(HERE, "deliver.sh"), row.node, words],
                           env=env, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        raise ValueError(f"no reply from {name} in {timeout} s — the ask is in the pull file; the reply lands in replies if it comes")
    after = read_replies(row.state)
    if len(after) > before and after[-1].question == words:
        return after[-1].answer
    said = (p.stderr or p.stdout).strip().splitlines()
    raise ValueError(said[-1] if said else f"deliver exited {p.returncode} and wrote no reply")


def _start_turn(name, words, canvas_dir, think=None, door=None):
    """A turn in the background, so the screen keeps time while the model
    thinks.  The box says when it is done and what went wrong; the reply
    itself is in the record."""
    import threading, time
    box = {"words": words, "since": time.time(), "done": False, "error": None}

    def run():
        try:
            talk(name, words, canvas_dir, think=think, door=door)
        except Exception as e:   # a refusal or deliver's words — shown on the screen, never raised into curses
            box["error"] = str(e)
        box["done"] = True

    threading.Thread(target=run, daemon=True).start()
    return box


def _wrap(text, width):
    import textwrap
    out = []
    for para in text.splitlines() or [""]:
        out += textwrap.wrap(para, max(10, width)) or [""]
    return out


def _ask_line(stdscr, prompt):
    """One line typed at the bottom of the screen; empty is a change of mind."""
    import curses
    h, w = stdscr.getmaxyx()
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


def _talk_screen(stdscr, name, canvas_dir):
    """The conversation with one node: its exchanges from `replies`, the
    newest at the bottom, and a line to type.  Returns a notice for the
    panel, or nothing."""
    import curses, time
    turn = None   # the turn in flight
    last = ""     # the last refusal, shown until the next turn
    think = bool(os.environ.get("TEND_THINK"))   # the environment's word, until [k] says otherwise
    minds = [""] + doors()                       # the node, then each door; [d] cycles
    door = os.environ.get("TEND_DOOR", "")
    if door not in minds:
        minds.append(door)
    while True:
        try:
            row = find_row(name, canvas_dir)
        except ValueError as e:
            return f"refused: {e}"
        h, w = stdscr.getmaxyx()
        stdscr.erase()
        if row.running:
            state = "running"
        elif row.dead:
            state = "DEAD — a turn pulls it up again; the first reply waits for the load"
        else:
            state = "not running — a turn pulls it up; the first reply waits for the load"
        try:
            stdscr.addstr(0, 0, f" talk — {name}  {state}  think {'on' if think else 'off'}  mind {door or 'the node'} ".ljust(w - 1), curses.A_REVERSE)
        except curses.error:
            pass
        lines = []
        for e in read_replies(row.state)[-TALK_TURNS:]:
            lines += [(l, curses.A_BOLD) for l in _wrap(f"{e.stamp}  you: {e.question}", w - 4)]
            for c in e.calls:
                lines += [(l, curses.A_DIM) for l in _wrap(f"[call] {c}", w - 4)]
            if e.thinking:
                lines += [(l, curses.A_DIM) for l in _wrap(f"(thinking) {e.thinking}", w - 4)]
            lines += [(l, 0) for l in _wrap(f"{e.via.split(' ')[0] if e.via else name}: {e.answer}", w - 4)]
            lines.append(("", 0))
        if turn is not None and turn["done"]:
            if turn["error"]:
                last = "refused: " + turn["error"]
            turn = None
        if turn is not None:
            lines += [(l, curses.A_BOLD) for l in _wrap("you: " + turn["words"], w - 4)]
            thinking_so_far, answer_so_far = read_turn(row.state)
            calls_so_far = read_calls(row.state)
            for c in calls_so_far:
                lines += [(l, curses.A_DIM) for l in _wrap(f"[call] {c}", w - 4)]
            if thinking_so_far:
                lines += [(l, curses.A_DIM) for l in _wrap("(thinking) " + thinking_so_far, w - 4)]
            who = turn["door"] or name
            if answer_so_far:
                lines += [(l, 0) for l in _wrap(f"{who}: {answer_so_far}", w - 4)]
            lines.append((f"… {who} is {'answering' if answer_so_far else 'thinking' if thinking_so_far else 'acting' if calls_so_far else 'starting'}  ({int(time.time() - turn['since'])} s)", curses.A_DIM))
        if last:
            lines.append((last, curses.A_BOLD))
        room = h - 3
        y = 1
        for text, attr in (lines[-room:] if room > 0 else []):
            try:
                stdscr.addstr(y, 2, text[:max(0, w - 3)], attr)
            except curses.error:
                pass
            y += 1
        bar = (" [Enter] a line to ask  [k] think on/off  [d] door  [Esc] back " if turn is None
               else " waiting for the reply — Esc goes back; the reply still lands in replies ")
        try:
            stdscr.addstr(h - 1, 0, bar.ljust(w - 1), curses.A_REVERSE)
        except curses.error:
            pass
        stdscr.refresh()
        if turn is not None:
            stdscr.timeout(500)
            try:
                c = stdscr.getch()
            except KeyboardInterrupt:
                c = 27
            if c in (27, ord("q")):
                stdscr.timeout(1000)
                return f"talk {name}: a turn is in flight; its reply lands in {row.state}/replies"
            continue
        stdscr.timeout(1000)
        try:
            c = stdscr.getch()
        except KeyboardInterrupt:
            c = 27
        if c in (27, ord("q")):
            return ""
        if c == ord("k"):
            think = not think
            continue
        if c == ord("d"):
            door = minds[(minds.index(door) + 1) % len(minds)]
            continue
        if c in (10, 13, curses.KEY_ENTER):
            words = _ask_line(stdscr, f"{name} <")
            if words:
                last = ""
                turn = _start_turn(name, words, canvas_dir, think, door)
                turn["door"] = door


def _counts(rows):
    held = sum(1 for r in rows if r.held is not None)
    pulled = sum(1 for r in rows if r.pulled_by)
    broken = sum(1 for r in rows if r.broken)
    return f"{len(rows)} on it, {held} held" + (f", {pulled} pulled" if pulled else "") + (f", {broken} BROKEN" if broken else "")


def wrong(p):
    """Is this row something gone wrong — shown bold: a death, cut cords, a
    hold that holds nothing, or a held node with no runner up (the hold's
    promise is not kept, whatever the reason) — and a node a process
    pulls with no runner up, the same promise from an edge (card:edge.md)."""
    return bool(p.dead or p.cut or p.broken or p.note or ((p.held is not None or p.pulled_by) and not p.running))


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
    elif p.pulled_by:
        # an edge is a standing pull while a process holds it (card:edge.md): the same promise as a hold's
        if p.dead:
            state = "DEAD, PULLED — the resolver restarts it at its next visit if the edge is newer than the death"
        else:
            state = "PULLED, NOT RUNNING — a process holds its edge; the resolver starts one at its next visit"
    elif p.dead:
        state = "DEAD"
    else:
        state = "not running"
    bits = [p.name.ljust(10), state]
    if p.held is not None:
        bits.append(f"held — {p.held}")   # the canvas's standing pull: it is restarted when it stops (card:hold.md)
    if p.pulled_by:
        bits.append("pulled by — " + ", ".join(p.pulled_by))   # a process's standing pull, the edge (card:edge.md)
    if p.pulls:
        bits.append("pulls — " + ", ".join(p.pulls))
    if p.last_pull:
        bits.append(f"pulled {_when(p.last_pull)}")
    if p.last_stop:
        bits.append(f"stopped {_when(p.last_stop)}" + (f" — {p.stop_reason}" if p.stop_reason else ""))
    return "  ".join(bits)


def event_line(e):
    return f"{_when(e.epoch)}  {e.who.ljust(6)} {e.text}"


def answer(state_dir=None):
    """Clear the questions — the person's word, run through the andon."""
    env = dict(os.environ)
    if state_dir is not None:
        env["TEND_ANDON_STATE"] = str(state_dir)
    return subprocess.run(["sh", os.path.join(HERE, "andon.sh"), "answered"], env=env)


def _when(epoch):
    """A clock for today, a date for any other day — Henri, 2026-09-03: a
    bare `08:05` on a row read as this morning when it was yesterday's."""
    import datetime
    t = datetime.datetime.fromtimestamp(epoch)
    if t.date() == datetime.date.today():
        return t.strftime("%H:%M")
    return t.strftime("%b %-d %H:%M")


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
        return _ask_line(stdscr, prompt)

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
                + (f", last ring {_when(st.last_ring)}" if st.last_ring else "")
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
                          " [h] hold  [p] pin  [u] unhold  [x] unpin  [t] talk  [a] answer all  [r] resolve  [q] quit ".ljust(w - 1),
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
        elif c == ord("t"):
            # talk: the one row, or the row named; the screen is the conversation
            name = pins[0].name if len(pins) == 1 else ask("talk NAME:")
            if name:
                notice = _talk_screen(stdscr, name, canvas_dir)
            stdscr.clear()
        elif c in (ord("h"), ord("p"), ord("u"), ord("x")):
            # the person's hand: one typed line, the verb's own words, then the resolver
            verb, prompt = {ord("h"): ("hold", "hold LABEL NODE [--state DIR] [WORDS...]:"),
                            ord("p"): ("pin", "pin NAME NODE [--state DIR]:"),
                            ord("u"): ("unhold", "unhold LABEL:"),
                            ord("x"): ("unpin", "unpin NAME:")}[c]
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
        elif a == "talk":
            think = None; door = None
            while args and args[0] in ("--think", "--door"):
                if args[0] == "--think":
                    think = True; args = args[1:]
                elif len(args) > 1:
                    door = args[1]; args = args[2:]
                else:
                    args = []
            if len(args) < 2:
                sys.stderr.write("andon-panel: talk [--think] [--door DOOR] NAME WORDS...\n")
                return 2
            try:
                answer_text = talk(args[0], " ".join(args[1:]), canvas, think=think, door=door)
                ex = read_replies(find_row(args[0], canvas).state)
                for c in (ex[-1].calls if ex else []):
                    sys.stderr.write("(call) " + c + "\n")
                if ex and ex[-1].thinking:
                    # the thinking beside the answer, on stderr: a pipe gets the answer alone
                    sys.stderr.write("(thinking) " + ex[-1].thinking + "\n")
                print(answer_text)
                return 0
            except ValueError as e:
                sys.stderr.write(f"andon-panel: {e}\n")
                return 2
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
              + (f", pulled since {_when(st.last_ring)}" if st.pulled else "")
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
