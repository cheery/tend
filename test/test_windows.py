#: asked-by: Henri, 2026-09-06 — "time to start the work on windowing system? … start steamrolling the wrinkles straight" (card:canvas-windows.md)
"""test/test_windows.py — a window from a file: `tools/windows.py open` writes `canvas/NAME.win`, the shell opens the window.

His chain (spec/canvas.md, 2026-09-06) runs from a file the person's
command writes to a window the shell places; what a test can hold from
this seat is the first arrow — the file, its shape, what `open`
refuses — the list read over a stub `gdbus` the way the door's tests
stand in for llama-server, and that the extension parses as the module
GNOME 45+ loads and names what it watches.  The chain's run — the
window opening, moving, closing, coming back at log-in — is his hand:
the fence has no session bus and no shell.
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
TOOL = ROOT / "tools" / "windows.py"
EXT = ROOT / "tools" / "tend-windows@tend"

_spec = importlib.util.spec_from_file_location("windows", TOOL)
windows = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(windows)

# The stub prints what `gdbus` prints: `call` answers `('<json>',)` in
# GVariant's text form — the quote flips to `"` when the string holds a
# `'`, and the quote and `\` are escaped — from the list in $STUB_LIST.
# Every argv goes to $STUB_SEEN.
STUB = r'''#!/usr/bin/env python3
import os, sys
with open(os.environ["STUB_SEEN"], "a") as f:
    f.write(" ".join(sys.argv[1:]) + "\n")
if os.environ.get("STUB_FAIL"):
    sys.stderr.write("Error: GDBus.Error:org.freedesktop.DBus.Error.ServiceUnknown: The name org.tend.Windows was not provided by any .service files\n")
    sys.exit(1)
def variant(s):
    q = '"' if "'" in s else "'"
    out = q
    for c in s:
        if c == q or c == "\\":
            out += "\\"
        out += c if c.isprintable() else "\\u%04x" % ord(c)
    return out + q
if sys.argv[1] == "call":
    print("(" + variant(open(os.environ["STUB_LIST"]).read().strip()) + ",)")
'''

PANEL = {"id": 94551, "seq": 12, "app": "org.gnome.Ptyxis", "title": "tend:panel", "focus": True,
         "x": 40, "y": 40, "w": 1000, "h": 700, "at": 1788700000, "file": "panel"}
DOC = {"id": 94552, "seq": 13, "app": "org.gnome.TextEditor", "title": "lander.md", "focus": False,
       "x": 1280, "y": 32, "w": 640, "h": 688, "at": 1788700100, "file": ""}


@pytest.fixture
def desk(tmp_path, monkeypatch):
    """A canvas and a stub gdbus, both the test's own."""
    stub = tmp_path / "gdbus"; stub.write_text(STUB); stub.chmod(0o755)
    seen = tmp_path / "seen"; seen.write_text("")
    lst = tmp_path / "list.json"; lst.write_text(json.dumps([PANEL, DOC]))
    canvas = tmp_path / "canvas"
    monkeypatch.setenv("TEND_GDBUS", str(stub))
    monkeypatch.setenv("STUB_SEEN", str(seen))
    monkeypatch.setenv("STUB_LIST", str(lst))
    monkeypatch.setenv("TEND_CANVAS", str(canvas))
    monkeypatch.delenv("STUB_FAIL", raising=False)
    return tmp_path


def run(*args, cwd=None, **env):
    return subprocess.run([sys.executable, str(TOOL), *args], capture_output=True, text=True,
                          env=dict(os.environ, **env), timeout=30, cwd=cwd)


def fields(path):
    got = {}
    for line in path.read_text().splitlines():
        if line and not line.startswith("#"):
            k, _, v = line.partition(" ")
            got[k] = v
    return got


def test_open_writes_the_file_that_is_the_window(desk):
    """The first arrow: the command creates a file in canvas/ that holds
    what the window is — what runs and where; the frame is the shell's
    to write, never this program's."""
    r = run("open", "panel", "--", "tools/panel.py", "--canvas", "x", cwd=str(desk))
    assert r.returncode == 0, r.stderr
    path = desk / "canvas" / "panel.win"
    assert path.exists() and str(path) in r.stdout, r.stdout
    got = fields(path)
    assert got == {"run": "tools/panel.py --canvas x", "dir": str(desk)}, got
    assert path.read_text().startswith("# canvas/panel.win — one file, one window"), "the first line says what it is"
    assert "frame" not in got, "where is the layout rule's until the window has been somewhere"
    # a line the panel reads: the same file, read by the reader the desk has
    assert "rm" in r.stdout, "close is delete, and the line says so"


def test_open_refuses_a_second_file_for_a_window_that_has_one(desk):
    """One file, one window (Henri, 2026-09-06: "tämä sääntö kestää")."""
    assert run("open", "panel", "--", "tools/panel.py").returncode == 0
    first = (desk / "canvas" / "panel.win").read_text()
    r = run("open", "panel", "--", "something else")
    assert r.returncode == 1 and "one file, one window" in r.stderr and "rm" in r.stderr, r.stderr
    assert (desk / "canvas" / "panel.win").read_text() == first, "the file that is the window is not rewritten"


def test_open_refuses_a_name_the_panel_would_and_an_empty_command(desk):
    for bad in ("../x", ".hidden", "a b", ""):
        r = run("open", bad, "--", "true")
        assert r.returncode == 2 and "not a canvas name" in r.stderr, (bad, r.stderr)
    r = run("open", "panel")
    assert r.returncode == 2 and "nothing to run" in r.stderr, r.stderr
    assert not (desk / "canvas").exists(), "a refused open writes nothing, not even the directory"


def test_list_prints_the_desk_and_says_which_file_each_window_is(desk):
    r = run("--list")
    assert r.returncode == 0, r.stderr
    lines = r.stdout.splitlines()
    assert lines[0].startswith("panel.win") and "focused" in lines[0] and "40 40 1000 700" in lines[0], lines
    assert lines[1].startswith("-") and "lander.md" in lines[1], lines
    assert "2 on the desk, 1 on the canvas" in r.stdout, r.stdout
    seen = (desk / "seen").read_text()
    assert "call --session --dest org.tend.Windows --object-path /org/tend/Windows --method org.tend.Windows.List" in seen, seen


def test_a_shell_that_does_not_answer_says_so_and_names_the_extension(desk):
    """Not from this seat: a shell with no extension is not a desk with no windows."""
    r = run("--list", STUB_FAIL="1")
    assert r.returncode == 1
    assert "org.tend.Windows" in r.stderr and "tend-windows@tend" in r.stderr and "ServiceUnknown" in r.stderr, r.stderr


def test_the_gdbus_text_is_read_as_the_string_it_carries():
    """GVariant's text form is a Python literal for strings: the quote flips
    to `"` when the text holds a `'`, and `\\uXXXX` stands for what does
    not print."""
    assert windows.parse_call("('[{\"title\": \"a\"}]',)\n") == [{"title": "a"}]
    assert windows.parse_call('("[{\\"title\\": \\"llm\'s log\\"}]",)\n') == [{"title": "llm's log"}]
    assert windows.parse_call("('[{\"title\": \"tab\\\\tab \\u00e4\"}]',)") == [{"title": "tab\tab ä"}]
    with pytest.raises(ValueError):
        windows.parse_call("not a variant")


def test_the_extension_parses_and_holds_the_chains_five_arrows(tmp_path):
    """What a test can hold of code that runs inside the shell: it parses
    as the module GNOME 45+ loads, its uuid is its directory, it targets
    this shell's version, it watches the canvas the command writes to,
    starts a terminal whose title is the file's name, and its bus name
    and path are the ones `--list` asks."""
    meta = json.loads((EXT / "metadata.json").read_text())
    assert meta["uuid"] == EXT.name == "tend-windows@tend"
    assert "50" in meta["shell-version"], meta
    src = (EXT / "extension.js").read_text()
    assert windows.BUS_NAME in src and windows.OBJECT_PATH in src and 'name="List"' in src and 'name="Changed"' in src
    assert "export default class" in src and "resource:///org/gnome/shell/extensions/extension.js" in src
    # the five arrows, each a line the extension has
    assert "monitor_directory" in src, "→ the file in canvas/ is what opens the window"
    assert f"'{windows.TITLE}'" in src and "--title=" in src and "spawn_async" in src, "→ opens, in a terminal that says which file it is"
    assert "move_resize_frame" in src and "'shown'" in src and "settled" in src and "writeFrame" in src, \
        "→ placed — again once shown, past GNOME's own centring — and a move written back only after that"
    assert "_closing" in src and "EndSessionDialog" in src and "PrepareForShutdown" in src and "CLOSE_GRACE" in src, \
        "→ going down with the shell is not a close: the session's end is heard before the windows go, and a close waits"
    assert ".delete(" in src, "→ closed from its X removes the file; the file removed closes the window"
    node = shutil.which("node")
    if not node:
        pytest.skip("no node here to parse the module — not checked from this seat")
    copy = tmp_path / "extension.mjs"; copy.write_text(src)
    r = subprocess.run([node, "--check", str(copy)], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr


def test_install_copies_the_extension_under_the_persons_home_and_says_what_his_hand_does_next(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    r = run("--install")
    assert r.returncode == 0, r.stderr
    dest = tmp_path / ".local" / "share" / "gnome-shell" / "extensions" / "tend-windows@tend"
    assert (dest / "extension.js").read_text() == (EXT / "extension.js").read_text()
    assert (dest / "metadata.json").exists()
    assert "gnome-extensions enable tend-windows@tend" in r.stdout and "log out" in r.stdout, r.stdout
