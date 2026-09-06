#: asked-by: Henri, 2026-09-06 — "time to start the work on windowing system? … start steamrolling the wrinkles straight" (card:canvas-windows.md)
"""test/test_windows.py — the record without the manager: `tools/windows.py` mirrors the shell's window list into `canvas/*.win`.

The shell's side is a stub of `gdbus`, the way the door's tests stand in
for llama-server: GNOME 50.1 refuses `Introspect.GetWindows` to a plain
caller (measured from Henri's shell, 2026-09-06, on the card), so the
list comes from a thin extension inside the shell over its own D-Bus
name, and the fence has no session bus at all — the extension's run is
his hand, and what a test can hold is the mirror, the file shape, and
that the extension parses and names the interface the mirror calls.
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
# `'`, and the quote and `\` are escaped — from the list in $STUB_LIST;
# `monitor` prints one line per signal from $STUB_SIGNALS, swapping the
# list to $STUB_LIST2 after the first, then exits like a monitor whose
# name went away.  Every argv goes to $STUB_SEEN.
STUB = r'''#!/usr/bin/env python3
import os, sys, shutil
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
elif sys.argv[1] == "monitor":
    for i, line in enumerate(open(os.environ["STUB_SIGNALS"]).read().splitlines()):
        print(line, flush=True)
        if i == 0 and os.environ.get("STUB_LIST2"):
            shutil.copy(os.environ["STUB_LIST2"], os.environ["STUB_LIST"])
    sys.exit(0)
'''

TERM = {"id": 94551, "seq": 12, "app": "org.gnome.Terminal", "title": "llm's log — tend", "focus": True,
        "x": 0, "y": 32, "w": 1280, "h": 688, "at": 1788700000}
DOC = {"id": 94552, "seq": 13, "app": "org.gnome.TextEditor", "title": "lander.md", "focus": False,
       "x": 1280, "y": 32, "w": 640, "h": 688, "at": 1788700100}


@pytest.fixture
def desk(tmp_path, monkeypatch):
    """A canvas and a stub gdbus, both the test's own."""
    stub = tmp_path / "gdbus"; stub.write_text(STUB); stub.chmod(0o755)
    seen = tmp_path / "seen"; seen.write_text("")
    lst = tmp_path / "list.json"; lst.write_text(json.dumps([TERM, DOC]))
    canvas = tmp_path / "canvas"
    monkeypatch.setenv("TEND_GDBUS", str(stub))
    monkeypatch.setenv("STUB_SEEN", str(seen))
    monkeypatch.setenv("STUB_LIST", str(lst))
    monkeypatch.setenv("TEND_CANVAS", str(canvas))
    monkeypatch.delenv("STUB_FAIL", raising=False)
    monkeypatch.delenv("STUB_LIST2", raising=False)
    return tmp_path


def run(*args, **env):
    return subprocess.run([sys.executable, str(TOOL), *args], capture_output=True, text=True,
                          env=dict(os.environ, **env), timeout=30)


def fields(path):
    got = {}
    for line in path.read_text().splitlines():
        if line and not line.startswith("#"):
            k, _, v = line.partition(" ")
            got[k] = v
    return got


def test_once_writes_one_file_per_window_in_the_holds_shape(desk):
    r = run("--once")
    assert r.returncode == 0, r.stderr
    canvas = desk / "canvas"
    assert sorted(p.name for p in canvas.iterdir()) == ["org.gnome.Terminal-12.win", "org.gnome.TextEditor-13.win"]
    t = fields(canvas / "org.gnome.Terminal-12.win")
    assert t == {"app": "org.gnome.Terminal", "title": "llm's log — tend", "focus": "yes",
                 "frame": "0 32 1280 688", "at": "1788700000"}, t
    assert fields(canvas / "org.gnome.TextEditor-13.win")["focus"] == "no"
    # the first line says who writes it: the mirror touches only its own files
    assert (canvas / "org.gnome.Terminal-12.win").read_text().startswith("# tools/windows.py")
    assert "2 windows" in r.stdout and "0 gone" in r.stdout, r.stdout
    # the interface the mirror asks is the one the extension exports
    seen = (desk / "seen").read_text()
    assert "call --session --dest org.tend.Windows --object-path /org/tend/Windows --method org.tend.Windows.List" in seen, seen


def test_a_window_that_closed_leaves_its_file_marked_gone_and_the_first_mark_is_kept(desk):
    """The card's red-first: a `.win` with no window behind it says *gone* —
    the file outlives the window, as a hold's row outlives a death."""
    run("--once")
    (desk / "list.json").write_text(json.dumps([TERM]))
    r = run("--once")
    assert r.returncode == 0, r.stderr
    doc = desk / "canvas" / "org.gnome.TextEditor-13.win"
    assert doc.exists(), "the file outlives the window"
    got = fields(doc)
    assert got["gone"].isdigit() and got["title"] == "lander.md", got
    assert "gone" not in fields(desk / "canvas" / "org.gnome.Terminal-12.win")
    assert "1 window" in r.stdout and "1 gone" in r.stdout, r.stdout
    first = doc.read_text()
    run("--once")
    assert doc.read_text() == first, "the gone line is the moment it went; a later pass does not move it"


def test_a_file_the_mirror_did_not_write_is_never_touched(desk):
    """Who writes: the shallow row is the mirror's, and a tend app's own
    row beside it is the app's — the two never write each other's file."""
    canvas = desk / "canvas"; canvas.mkdir()
    own = canvas / "lander.win"
    own.write_text("app lander\ntitle the lamp, as lander sees it\nfocus no\nat 1788600000\n")
    os.utime(own, (1788600000, 1788600000))
    run("--once")
    (desk / "list.json").write_text("[]")
    r = run("--once")
    assert r.returncode == 0, r.stderr
    assert own.read_text().startswith("app lander") and "gone" not in own.read_text()
    assert int(os.stat(own).st_mtime) == 1788600000
    assert "gone" in fields(canvas / "org.gnome.Terminal-12.win")


def test_a_shell_that_does_not_answer_leaves_the_files_alone_and_says_so(desk):
    """Not from this seat: a shell with no extension is not a desk with no
    windows.  Nothing is marked gone, and the line names the extension."""
    run("--once")
    r = run("--once", STUB_FAIL="1")
    assert r.returncode == 1
    assert "org.tend.Windows" in r.stderr and "tend-windows@tend" in r.stderr and "ServiceUnknown" in r.stderr, r.stderr
    for p in (desk / "canvas").iterdir():
        assert "gone" not in fields(p), p


def test_watch_mirrors_at_start_and_on_every_signal_and_says_when_the_shell_goes_away(desk):
    (desk / "signals").write_text("/org/tend/Windows: org.tend.Windows.Changed ()\n/org/tend/Windows: org.tend.Windows.Changed ()\n")
    (desk / "list2.json").write_text(json.dumps([DOC]))
    r = run("--watch", STUB_SIGNALS=str(desk / "signals"), STUB_LIST2=str(desk / "list2.json"))
    assert r.returncode == 1, r.stderr
    assert "went away" in r.stderr and "tend-windows@tend" in r.stderr, r.stderr
    seen = [l for l in (desk / "seen").read_text().splitlines()]
    assert any(l.startswith("monitor --session --dest org.tend.Windows --object-path /org/tend/Windows") for l in seen), seen
    assert sum(1 for l in seen if l.startswith("call ")) >= 2, seen
    canvas = desk / "canvas"
    assert "gone" in fields(canvas / "org.gnome.Terminal-12.win"), "the second list had no terminal"
    assert "gone" not in fields(canvas / "org.gnome.TextEditor-13.win")


def test_the_gdbus_text_is_read_as_the_string_it_carries():
    """GVariant's text form is a Python literal for strings: the quote flips
    to `"` when the text holds a `'`, and `\\uXXXX` stands for what does
    not print."""
    assert windows.parse_call("('[{\"title\": \"a\"}]',)\n") == [{"title": "a"}]
    assert windows.parse_call('("[{\\"title\\": \\"llm\'s log\\"}]",)\n') == [{"title": "llm's log"}]
    assert windows.parse_call("('[{\"title\": \"tab\\\\tab \\u00e4\"}]',)") == [{"title": "tab\tab ä"}]
    with pytest.raises(ValueError):
        windows.parse_call("not a variant")


def test_a_key_is_a_canvas_label():
    assert windows.key({"app": "org.gnome.Terminal", "seq": 12}) == "org.gnome.Terminal-12"
    assert windows.key({"app": "", "seq": 3}) == "window-3"
    assert windows.key({"app": "../x y/z", "seq": 3}) == "x-y-z-3"


def test_the_extension_parses_and_names_the_interface_the_mirror_calls(tmp_path):
    """What a test can hold of code that runs inside the shell: it parses
    as the module GNOME 45+ loads, its uuid is its directory, it targets
    this shell's version, and its name and path are the mirror's."""
    meta = json.loads((EXT / "metadata.json").read_text())
    assert meta["uuid"] == EXT.name == "tend-windows@tend"
    assert "50" in meta["shell-version"], meta
    src = (EXT / "extension.js").read_text()
    assert windows.BUS_NAME in src and windows.OBJECT_PATH in src and 'name="List"' in src and 'name="Changed"' in src
    assert "export default class" in src and "resource:///org/gnome/shell/extensions/extension.js" in src
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
