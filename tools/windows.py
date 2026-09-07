#!/usr/bin/env python3
#: asked-by: Henri, 2026-09-06 — "time to start the work on windowing system? … start steamrolling the wrinkles straight" (card:canvas-windows.md)
"""tools/windows.py — a window from a file: his command writes `canvas/NAME.win`, and the shell opens the window.

    tools/windows.py open NAME -- COMMAND…    write canvas/NAME.win; the window opens on the desk
    tools/windows.py --list                   the shell's window list, printed (which file each is)
    tools/windows.py --install                copy the extension under ~/.local/share/gnome-shell/extensions
                                              and say what his hand does next
    tools/windows.py --check                  three verdicts: the extension installed, enabled, answering

Henri's chain (spec/canvas.md, 2026-09-06): *the user wants to open a
window → their command creates a file in canvas/ that holds the
window's state → the window opens on the screen at a predetermined
place → a move changes the file → after a shutdown and a start the
windows come back where they were → the user closes the window and
the file disappears from the canvas.*  This is the first arrow.  One
file, one window (his rule, "tämä sääntö kestää"):

    # canvas/panel.win — one file, one window (spec/canvas.md); his command wrote it
    run tools/panel.py            what runs in it, a shell line
    dir /home/henri/tend          where it runs
    frame 40 40 1000 700          where the window is — written back by the shell, never from here
    at 1788700000                 the last change the shell saw

**The rest of the chain is the extension**, `tools/tend-windows@tend`,
inside the shell: it watches the canvas, starts a `.win` in a terminal
whose title says which file it is (`ptyxis --title=tend:NAME -- sh -c
RUN`), places the window at `frame` or by the layout rule when the
file gives none, writes a move back, starts every file again at
log-in, removes the file when the window is closed from its X and
closes the window when the file is removed.  A window whose title
does not begin `tend:` is a legacy window, on neither the canvas nor
the panel (Henri, 2026-09-06).  **Only tend-compatible programs**: the
mirror of every window this program was on 2026-09-06 is gone by the
card's signed `done` line — `ls canvas/` shows nothing he did not put
there — and so is `.gone`: close is delete.

**Where the list comes from** (`--list`, `--check`): GNOME 50.1
refuses `org.gnome.Shell.Introspect.GetWindows` to a caller not on
its allow-list (from Henri's shell, 2026-09-06), so the extension
publishes it as `org.tend.Windows` — `List() -> s` (JSON) and a
`Changed` signal — and this program asks over `gdbus`.  A session
inside the fence has no session bus at all; `open` needs none, it
writes a file, and the shell does the rest on the person's side.
"""
import ast
import json
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EXTENSION = "tend-windows@tend"
EXT_SRC = os.path.join(HERE, EXTENSION)
BUS_NAME = "org.tend.Windows"
OBJECT_PATH = "/org/tend/Windows"
TITLE = "tend:"
CANVAS_DEFAULT = os.path.join(os.path.expanduser("~"), ".local", "state", "tend", "canvas")
_LABEL = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


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


def win_text(name, run, cwd):
    return (f"# canvas/{name}.win — one file, one window (spec/canvas.md); his command wrote it\n"
            f"run {run}\ndir {cwd}\n")


def open_window(name, command, canvas=None, cwd=None):
    """The first arrow: the file.  Refuses a name the panel's hand would,
    an empty command, and a name whose file is there — one file, one
    window, and the window is up or opening.  Returns 0, 2 or 1."""
    if not _LABEL.match(name or ""):
        sys.stderr.write(f"windows: {name!r} is not a canvas name (letters, digits, . _ -; not starting with .)\n")
        return 2
    if not command:
        sys.stderr.write("windows: open NAME -- COMMAND… — nothing to run in the window\n")
        return 2
    d = canvas_dir(canvas)
    path = os.path.join(d, name + ".win")
    if os.path.exists(path):
        sys.stderr.write(f"windows: {path} is there — one file, one window; rm it to close that one first\n")
        return 1
    os.makedirs(d, exist_ok=True)
    run = " ".join(command) if len(command) > 1 else command[0]
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        f.write(win_text(name, run, cwd or os.getcwd()))
    os.replace(tmp, path)
    print(f"windows: {path} — the shell opens it; `rm` closes it")
    return 0


def list_windows():
    try:
        rows = fetch()
    except ValueError as e:
        sys.stderr.write(f"windows: {BUS_NAME} did not answer — the {EXTENSION} extension is not enabled in "
                         f"this shell, or this is not the desk's session bus.\n  {e}\n")
        return 1
    for w in rows:
        file = w.get("file") or ""
        print(f"{(file + '.win') if file else '-':28} {'focused' if w.get('focus') else 'open':8} "
              f"{int(w.get('x', 0))} {int(w.get('y', 0))} {int(w.get('w', 0))} {int(w.get('h', 0)):<6} "
              f"{w.get('app', '')}  {w.get('title', '')}")
    on = sum(1 for w in rows if w.get("file"))
    print(f"windows: {len(rows)} on the desk, {on} on the canvas")
    return 0


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
        print(f"✓ {BUS_NAME} answers: {len(rows)} windows, {sum(1 for w in rows if w.get('file'))} on the canvas")
    except ValueError as e:
        print(f"✗ {BUS_NAME} does not answer — {e}"); fail = 1
    return fail


def main(argv):
    canvas = None; verb = None; name = None; command = []
    args = list(argv[1:])
    while args:
        a = args.pop(0)
        if a in ("-h", "--help"):
            sys.stdout.write(__doc__); return 0
        if a == "--canvas" and args:
            canvas = args.pop(0)
        elif a.startswith("--canvas="):
            canvas = a[len("--canvas="):]
        elif a in ("--list", "--install", "--check") and verb is None:
            verb = a
        elif a == "open" and verb is None:
            verb = a
            if args and not args[0].startswith("-"):
                name = args.pop(0)
            if args and args[0] == "--":
                args.pop(0)
            command, args = args, []
        else:
            sys.stderr.write(f"windows: unknown argument {a!r}\n"); return 2
    if verb is None:
        sys.stdout.write(__doc__); return 2
    if verb == "open":
        return open_window(name, command, canvas)
    return {"--list": list_windows, "--install": install, "--check": check}[verb]()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
