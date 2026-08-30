"""`tools/reach-allow.sh` — the person's key to the reach bound takes only
the rows the fence can be asked for, and says which they are.

Henri, 2026-08-30: "modify tend-reach-allow to restrict what you can
insert into it, and list available allowances as well" — the morning
the hook line read `TEND_REACH_ALLOW=net,tree` (F004).  `tree` is not a
row a session can ask for: `tools/sandbox.sh --reach tree` is "no such
row", and the key had written it onto the line without a word.

The fixture builds the side it means: a tree of its own holding HEAD's
`.claude/settings.json` (git is the file's canonical copy,
`tools/fence.sh`), never the working tree's — which on the day this was
written held the very bound this test refuses.  The script is run from
this tree's `tools/` with `TEND_TREE` at the fixture, the way an
installed copy governs a tree.
"""

import json
import os
import pathlib
import shutil
import subprocess

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
KEY = ROOT / "tools" / "reach-allow.sh"
SEL = '.hooks.PreToolUse[].hooks[] | select(.command | test("fence-hook")) | .command'

pytestmark = pytest.mark.skipif(shutil.which("bwrap") is None,
                                reason="no bubblewrap — sandbox.sh --rows, which the key reads, refuses before listing")


@pytest.fixture
def tree(tmp_path):
    t = tmp_path / "tree"
    (t / ".claude").mkdir(parents=True)
    (t / ".claude/settings.json").write_bytes(subprocess.run(
        ["git", "-C", str(ROOT), "show", "HEAD:.claude/settings.json"], capture_output=True, check=True).stdout)
    return t


def run(tree, *args):
    return subprocess.run(["sh", str(KEY), *args], env=dict(os.environ, TEND_TREE=str(tree)) | {"TEND_FENCED": ""},
                          capture_output=True, text=True)


def line(tree):
    return subprocess.run(["jq", "-r", SEL, str(tree / ".claude/settings.json")],
                          capture_output=True, text=True, check=True).stdout.strip()


def bound(tree):
    l = line(tree)
    return l.split(" ", 1)[0].removeprefix("TEND_REACH_ALLOW=") if l.startswith("TEND_REACH_ALLOW=") else None


def fence_rows():
    out = subprocess.run(["sh", str(ROOT / "tools/sandbox.sh"), "--rows"], capture_output=True, text=True, check=True).stdout
    return {l.split()[1]: l.split()[0] for l in out.splitlines()}


def test_it_parses():
    assert subprocess.run(["sh", "-n", str(KEY)]).returncode == 0


def test_the_rows_it_lists_are_the_fences_off_rows(tree):
    """The fence knows the rows; the key reads them and keeps no list of
    its own.  Every row `--rows` names is `off` in `sandbox.sh --rows`,
    and every `off` row is named."""
    r = run(tree, "--rows")
    assert r.returncode == 0, r.stderr
    listed = {l.split()[1] for l in r.stdout.splitlines() if l.startswith("  ")}
    assert listed == {k for k, v in fence_rows().items() if v == "off"}
    assert {"net", "audio", "display"} <= listed
    assert "tree" not in listed and "state" not in listed, "a row that is always on cannot be asked for"


def test_a_row_the_fence_knows_is_set_and_read_back(tree):
    r = run(tree, "net")
    assert r.returncode == 0, r.stderr
    assert bound(tree) == "net" and "fence: up" in r.stdout
    rows = run(tree, "--rows").stdout
    assert "  allowed  net " in rows and "  -        audio " in rows
    r = run(tree, "net,audio")
    assert r.returncode == 0 and bound(tree) == "net,audio", r.stderr
    rows = run(tree, "--rows").stdout
    assert "  allowed  net " in rows and "  allowed  audio " in rows and "  -        display " in rows
    r = run(tree, "")
    assert r.returncode == 0 and bound(tree) is None, r.stderr
    assert "the bound is none" in run(tree, "--rows").stdout


@pytest.mark.parametrize("arg", [
    "tree",             # a row that is always on — F004, the one that was on the line
    "net,tree",
    "state",
    "nofence",
    "net audio",        # a space: the hook reads the line with `[^ ]*`
    "net;ls",
    ",net", "net,", "net,,audio",
    "NET",
])
def test_a_name_that_is_not_a_row_is_refused_before_the_file_is_touched(tree, arg):
    assert run(tree, "net").returncode == 0
    before = (tree / ".claude/settings.json").read_bytes()
    r = run(tree, arg)
    assert r.returncode == 2, (r.stdout, r.stderr)
    assert "reach-allow:" in r.stderr and "tools/reach-allow.sh --rows" in r.stderr
    assert "net" in r.stderr and "audio" in r.stderr and "display" in r.stderr, "the refusal names the rows"
    assert (tree / ".claude/settings.json").read_bytes() == before, "refused, and nothing written"
    assert bound(tree) == "net"


def test_a_bound_holding_a_name_that_is_not_a_row_is_said_out_loud(tree):
    """The state the key found on 2026-08-30: a line written before it
    checked.  `--rows` says which name is not a row and exits 1 — a lamp,
    not a repair; the person's hand clears it."""
    s = tree / ".claude/settings.json"
    d = json.loads(s.read_text())
    for group in d["hooks"]["PreToolUse"]:
        for h in group["hooks"]:
            if "fence-hook" in h["command"]:
                h["command"] = "TEND_REACH_ALLOW=net,tree " + h["command"].split(" ", 1)[1]
    s.write_text(json.dumps(d))
    assert bound(tree) == "net,tree"
    r = run(tree, "--rows")
    assert r.returncode == 1
    assert "  allowed  net " in r.stdout
    assert "  ?        tree " in r.stdout and "is not a row" in r.stdout
    # and the way out is the key itself, with the row that is one
    assert run(tree, "net").returncode == 0 and bound(tree) == "net"
    assert run(tree, "--rows").returncode == 0


def test_without_a_fence_hook_line_there_is_nothing_to_set(tree):
    s = tree / ".claude/settings.json"
    d = json.loads(s.read_text())
    d["hooks"].pop("PreToolUse")
    s.write_text(json.dumps(d))
    r = run(tree, "net")
    assert r.returncode == 2 and "no fence-hook line" in r.stderr and "hook-installer" in r.stderr
    assert json.loads(s.read_text()) == d, "nothing written"


def test_an_unknown_argument_is_refused_out_loud(tree):
    r = run(tree, "--clear")
    assert r.returncode == 2 and "unknown argument" in r.stderr
    assert run(tree, "--help").returncode == 0 and "--rows" in run(tree, "--help").stdout
