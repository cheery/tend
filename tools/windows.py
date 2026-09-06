#!/usr/bin/env python3
#: asked-by: Henri, 2026-09-06 — "time to start the work on windowing system? … start steamrolling the wrinkles straight" (card:canvas-windows.md)
"""tools/windows.py — the record without the manager: the shell's window list, mirrored into `canvas/*.win`.

    tools/windows.py --once [--canvas DIR]    mirror the list now, one file per window
    tools/windows.py --watch [--canvas DIR]   mirror now, and again at every change the shell signals
    tools/windows.py --install                copy the extension under ~/.local/share/gnome-shell/extensions
                                              and say what his hand does next
    tools/windows.py --check                  three verdicts: the extension installed, enabled, answering

A window is a thing held, and nothing on the person's side records it
(`card:canvas-windows.md`): the windows are state in the compositor's
memory, a crash of the shell loses the layout, and a session that could
say "you have lander.md open" has no file to say it from.  This is the
hold card's rule one shelf over — **a window's state is a file on the
person's side** — `<app>-<seq>.win` in the canvas directory, beside the
pins and holds, read by the same readers:

    # tools/windows.py — the shell's shallow row; an app's own row is another file
    app    org.gnome.Terminal
    title  llm's log — tend
    focus  yes
    frame  0 32 1280 688
    at     1788700000          the window's last change, epoch seconds
    gone   1788700900          only once the window has closed: when — and then
                               the file is `<app>-<seq>.gone`

**Presence is the claim** — a `.win` present is a window; **the file
outlives the window** and says so twice, with a `gone` line inside
and with its name: the mirror renames it `<key>.gone`, so `ls` says
gone to the cheapest reader.  The name came second: the mark was a
line inside until 2026-09-06 16:50, when hy3 through the door read
`ls canvas/`, never a row, and called a Nautilus closed fourteen
minutes open — Henri: "do the rename into .gone".  The panel reads
both names and shows GONE for either.  The first `gone` is the moment
it went; a `.gone` is never touched again.  **Who writes**: the mirror writes
the shallow row for every window and touches only files whose first
line is its own — a tend app's richer row beside it, in its own name,
is the app's, and the two never write each other's file.

**Where the list comes from.**  GNOME 50.1 refuses
`org.gnome.Shell.Introspect.GetWindows` to a caller not on its
allow-list (from Henri's shell, 2026-09-06: `AccessDenied: GetWindows
is not allowed`), so the list is read from inside the shell by
`tools/tend-windows@tend`, a thin extension that publishes it as
`org.tend.Windows` on the session bus — `List() -> s` (JSON) and a
`Changed` signal — and this program asks over `gdbus`, which is on
every GNOME desk; python's `gi` is not (it is not here).  Not from
this seat: a shell that does not answer is not a desk with no windows
— nothing is marked gone, the line says which name did not answer,
and the exit is 1.  A session inside the fence has no session bus at
all; this runs on the person's side, from his shell, and the session
sees the files.

**What it does not do.**  Move, close or focus a window: it reads the
desk and writes files.  Sweep: a `.gone` is the person's to remove
(or the app's whose window it was), and a window that returns under
an old key gets a fresh `.win` beside the old `.gone`.  Keep itself alive: `--watch` is
the loop, a carrier for it is the tick's question and not day one's.
And it does not know a window across a shell restart — the sequence
starts over, and a new window may take an old file's name; the `at`
and `gone` lines are what says which.
"""
import ast
import json
import os
import re
import select
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
EXTENSION = "tend-windows@tend"
EXT_SRC = os.path.join(HERE, EXTENSION)
BUS_NAME = "org.tend.Windows"
OBJECT_PATH = "/org/tend/Windows"
CANVAS_DEFAULT = os.path.join(os.path.expanduser("~"), ".local", "state", "tend", "canvas")
MINE = "# tools/windows.py — the shell's shallow row; an app's own row is another file"
_LABEL = re.compile(r"[^A-Za-z0-9._-]+")


def canvas_dir(d=None):
    return str(d) if d is not None else os.environ.get("TEND_CANVAS", CANVAS_DEFAULT)


def gdbus():
    return os.environ.get("TEND_GDBUS") or shutil.which("gdbus") or "gdbus"


def parse_call(text):
    """`gdbus call` prints the reply in GVariant's text form, `('…',)` for
    one string — a Python literal for what a string can hold (the quote
    flips to `"` around a `'`, `\\` and the quote are escaped, what does
    not print is `\\uXXXX`) — and the string is the extension's JSON."""
    try:
        got = ast.literal_eval(text.strip())
        if isinstance(got, tuple) and len(got) == 1 and isinstance(got[0], str):
            return json.loads(got[0])
    except (ValueError, SyntaxError) as e:
        raise ValueError(f"not a gdbus reply: {text.strip()[:80]!r} ({e})")
    raise ValueError(f"not a one-string reply: {text.strip()[:80]!r}")


def fetch():
    """The list, from the shell; ValueError with the reason when it does not answer."""
    cmd = [gdbus(), "call", "--session", "--dest", BUS_NAME, "--object-path", OBJECT_PATH,
           "--method", BUS_NAME + ".List"]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.TimeoutExpired) as e:
        raise ValueError(f"{cmd[0]}: {e}")
    if r.returncode != 0:
        raise ValueError(r.stderr.strip() or f"exit {r.returncode}")
    return parse_call(r.stdout)


def key(w):
    """`<app>-<seq>`: a canvas label — a name the panel's hand would accept."""
    app = _LABEL.sub("-", str(w.get("app") or "")).strip("-.")
    return f"{app or 'window'}-{int(w.get('seq', 0))}"


def _row(w):
    return (f"{MINE}\napp {w.get('app', '')}\ntitle {str(w.get('title', '')).replace(chr(10), ' ')}\n"
            f"focus {'yes' if w.get('focus') else 'no'}\n"
            f"frame {int(w.get('x', 0))} {int(w.get('y', 0))} {int(w.get('w', 0))} {int(w.get('h', 0))}\n"
            f"at {int(w.get('at', 0))}\n")


def _mine(path):
    try:
        with open(path) as f:
            return f.readline().rstrip("\n") == MINE
    except OSError:
        return False


def _has_gone(path):
    try:
        with open(path) as f:
            return any(line.startswith("gone ") for line in f)
    except OSError:
        return False


def mirror(rows, canvas=None, at=None):
    """Write the rows; mark every file of this mirror's own whose window is not
    in them gone, once.  Returns (windows, gone)."""
    d = canvas_dir(canvas)
    os.makedirs(d, exist_ok=True)
    present = {}
    for w in rows:
        present[key(w) + ".win"] = w
    for name, w in present.items():
        path = os.path.join(d, name)
        text = _row(w)
        try:
            with open(path) as f:
                if f.read() == text:
                    continue
        except OSError:
            pass
        tmp = path + ".tmp"
        with open(tmp, "w") as f:
            f.write(text)
        os.replace(tmp, path)
    gone = 0
    for name in sorted(os.listdir(d)):
        path = os.path.join(d, name)
        if name.endswith(".gone"):
            if _mine(path):
                gone += 1     # marked on an earlier pass; never touched again
            continue
        if not name.endswith(".win") or name in present:
            continue
        if not _mine(path):
            continue          # somebody else's row: never touched from here
        if not _has_gone(path):
            with open(path, "a") as f:
                f.write(f"gone {int(at if at is not None else time.time())}\n")
        # the mark into the name (Henri, 2026-09-06: "do the rename into .gone"): a .win present is a
        # window, and ls says gone to the cheapest reader — the one that read names and called a
        # closed Nautilus open
        os.replace(path, path[:-len(".win")] + ".gone")
        gone += 1
    return len(present), gone


def once(canvas=None):
    try:
        rows = fetch()
    except ValueError as e:
        sys.stderr.write(f"windows: {BUS_NAME} did not answer — the {EXTENSION} extension is not enabled in "
                         f"this shell, or this is not the desk's session bus; the files are left as they are.\n  {e}\n")
        return 1
    n, gone = mirror(rows, canvas)
    print(f"windows: {n} window{'s' if n != 1 else ''} on {canvas_dir(canvas)}, {gone} gone")
    return 0


def watch(canvas=None):
    """Mirror now, then on every `Changed` the shell signals, coalescing a
    burst (a drag is many) into one pass; when the monitor ends, the
    shell went away — say so and exit 1, so a carrier can restart it."""
    if once(canvas) != 0:
        return 1
    cmd = [gdbus(), "monitor", "--session", "--dest", BUS_NAME, "--object-path", OBJECT_PATH]
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    except OSError as e:
        sys.stderr.write(f"windows: {cmd[0]}: {e}\n")
        return 1
    dirty = False
    while True:
        ready, _, _ = select.select([p.stdout], [], [], 0.3)
        if ready:
            line = p.stdout.readline()
            if line == "":
                break
            dirty = True
            continue
        if dirty:
            dirty = False
            if once(canvas) != 0:
                p.terminate()
                return 1
    if dirty:
        once(canvas)
    p.wait()
    sys.stderr.write(f"windows: the monitor on {BUS_NAME} ended — the shell went away, or {EXTENSION} was disabled; "
                     f"run --watch again once it is back.\n")
    return 1


def install():
    dest = os.path.join(os.path.expanduser("~"), ".local", "share", "gnome-shell", "extensions", EXTENSION)
    os.makedirs(dest, exist_ok=True)
    for name in ("extension.js", "metadata.json"):
        shutil.copyfile(os.path.join(EXT_SRC, name), os.path.join(dest, name))
    print(f"windows: {EXTENSION} copied to {dest}")
    print("his hand, next: on Wayland the shell loads an extension at login, so log out and in, then")
    print(f"    gnome-extensions enable {EXTENSION}")
    print(f"    tools/windows.py --check")
    return 0


def check():
    """Three verdicts, each from this seat: ✓, ✗, and `·` for what cannot be seen from here."""
    dest = os.path.join(os.path.expanduser("~"), ".local", "share", "gnome-shell", "extensions", EXTENSION)
    fail = 0
    if os.path.isfile(os.path.join(dest, "extension.js")):
        same = open(os.path.join(dest, "extension.js")).read() == open(os.path.join(EXT_SRC, "extension.js")).read()
        print(f"✓ {EXTENSION} installed at {dest}" + ("" if same else " — not the tree's copy; --install again"))
    else:
        print(f"✗ {EXTENSION} not installed — tools/windows.py --install"); fail = 1
    if not os.environ.get("DBUS_SESSION_BUS_ADDRESS") and not os.path.exists(f"/run/user/{os.getuid()}/bus"):
        print("· no session bus from this seat (a fenced session has none) — enabled and answering not checked from here")
        return fail
    ge = shutil.which("gnome-extensions")
    if ge:
        r = subprocess.run([ge, "info", EXTENSION], capture_output=True, text=True)
        state = next((l.split(":", 1)[1].strip() for l in r.stdout.splitlines() if l.strip().startswith("State:")), "")
        if state == "ACTIVE":
            print(f"✓ {EXTENSION} enabled")
        else:
            print(f"✗ {EXTENSION} not enabled (state {state or 'unknown'}) — gnome-extensions enable {EXTENSION}, after a log-in"); fail = 1
    else:
        print("· no gnome-extensions here — enabled not checked from here")
    try:
        rows = fetch()
        print(f"✓ {BUS_NAME} answers: {len(rows)} windows")
    except ValueError as e:
        print(f"✗ {BUS_NAME} does not answer — {e}"); fail = 1
    return fail


def main(argv):
    canvas = None; verb = None
    args = list(argv[1:])
    while args:
        a = args.pop(0)
        if a in ("-h", "--help"):
            sys.stdout.write(__doc__); return 0
        if a == "--canvas" and args:
            canvas = args.pop(0)
        elif a.startswith("--canvas="):
            canvas = a[len("--canvas="):]
        elif a in ("--once", "--watch", "--install", "--check") and verb is None:
            verb = a
        else:
            sys.stderr.write(f"windows: unknown argument {a!r}\n"); return 2
    if verb is None:
        sys.stdout.write(__doc__); return 2
    return {"--once": lambda: once(canvas), "--watch": lambda: watch(canvas),
            "--install": install, "--check": check}[verb]()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
