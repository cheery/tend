"""`tools/keep.py` — a program reads only what it was handed (board/keep.md).

The card's owed demonstration, as a test: a program run under keep reads
a granted file and is refused the file beside it, the tree, and the
ledger — from inside the fence, unprivileged, no build.  Landlock is the
mechanism (measured available at ABI 4); where it is absent these skip,
out loud, because a skipped confinement test is not a passing one.
"""

import ctypes
import os
import pathlib
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
KEEP = ROOT / "tools" / "keep.py"


def _landlock_abi():
    libc = ctypes.CDLL(None, use_errno=True)
    libc.syscall.restype = ctypes.c_long
    return libc.syscall(444, None, 0, 1)  # create_ruleset(NULL, 0, VERSION)


needs_landlock = pytest.mark.skipif(
    _landlock_abi() < 1,
    reason="no Landlock here — the confinement cannot be shown to hold")


def keep(*args, **kw):
    return subprocess.run([sys.executable, str(KEEP), *args],
                          capture_output=True, text=True, **kw)


def denied(text):
    # locale-independent: EACCES surfaced by cat, in any language
    return "cat:" in text and ("mine" not in text.split("cat:")[1][:40])


def test_it_parses():
    assert subprocess.run([sys.executable, "-m", "py_compile", str(KEEP)]).returncode == 0


@needs_landlock
def test_a_program_reads_what_it_was_handed_and_not_the_file_beside_it(tmp_path):
    """The whole card in one run: grant one file, and the neighbour is
    unreadable though it sits in the same directory."""
    (tmp_path / "mine").write_text("granted\n")
    (tmp_path / "beside").write_text("secret\n")
    r = keep("--allow", str(tmp_path / "mine"), "--", "sh", "-c",
             f"cat {tmp_path/'mine'}; cat {tmp_path/'beside'}")
    assert "granted" in r.stdout, r.stderr
    assert "secret" not in r.stdout, "the file beside it was readable — keep did not hold"
    assert r.returncode != 0, "reading the ungranted file must fail"


@needs_landlock
def test_the_tree_and_the_ledger_are_blind(tmp_path):
    """A program under keep cannot read the tree it runs in, nor another
    mechanism's log, unless handed them — problem 1, enforced."""
    (tmp_path / "mine").write_text("ok\n")
    r = keep("--allow", str(tmp_path), "--", "sh", "-c",
             f"cat {ROOT/'board'/'README.md'}")
    assert r.returncode != 0
    assert "founding" not in r.stdout and "board" not in r.stdout.lower()


@needs_landlock
def test_a_granted_directory_is_readable_beneath(tmp_path):
    """Grant a directory and files under it read; a sibling directory
    does not."""
    (tmp_path / "in").mkdir()
    (tmp_path / "in" / "f").write_text("inside\n")
    (tmp_path / "out").mkdir()
    (tmp_path / "out" / "f").write_text("outside\n")
    r = keep("--allow", str(tmp_path / "in"), "--", "sh", "-c",
             f"cat {tmp_path/'in'/'f'}; cat {tmp_path/'out'/'f'}")
    assert "inside" in r.stdout
    assert "outside" not in r.stdout


@needs_landlock
def test_a_system_program_still_runs(tmp_path):
    """The system roots are granted, so a system interpreter and its
    libraries still load — a confinement that cannot run the program is
    useless.  (A *venv* interpreter reads its pyvenv.cfg in the tree, so
    it must be handed that too: keep grants what it is given, the runtime
    included — board/keep.md.  Here the system python proves the roots
    suffice for a system program.)"""
    syspy = "/usr/bin/python3"
    if not os.path.exists(syspy):
        pytest.skip("no /usr/bin/python3 to prove a system program runs")
    r = keep("--allow", str(tmp_path), "--", syspy, "-c",
             "import json, os; print('ran', json.dumps(os.getpid() > 0))")
    assert r.returncode == 0, r.stderr
    assert "ran true" in r.stdout


@needs_landlock
def test_the_pull_node_runs_confined_under_keep(tmp_path):
    """`board/keep.md`'s next slice: the first real program, run *through*
    keep — the grant outside it — gains the boundary.  Handed its own code
    and a state directory and nothing else, the node opens, runs and stops
    (it writes state where the fence allows; keep governs reads), while a
    read of the tree from the same grant is refused.  The node itself is
    unchanged — the boundary is composed around it, not built into it."""
    node = ROOT / "node" / "node.py"
    state = tmp_path / "n.state"
    syspy = "/usr/bin/python3"
    if not os.path.exists(syspy):
        pytest.skip("no system python3 to run the node confined")
    # handed: the node's own directory (its code) and the state directory.
    r = keep("--allow", str(node.parent), "--allow", str(tmp_path), "--",
             syspy, str(node), "--state", str(state),
             "run", "--idle", "0.4", "--poll", "0.05")
    assert r.returncode == 0, r.stderr
    assert state.exists(), "the node could not open where it was left"
    import json
    assert json.loads(state.read_text())["generations"] == 1

    # the same grant is blind to the tree it was not handed.
    blind = keep("--allow", str(node.parent), "--allow", str(tmp_path), "--",
                 "sh", "-c", f"cat {ROOT/'board'/'README.md'}")
    assert blind.returncode != 0
    assert "founding" not in blind.stdout


def test_nothing_to_run_is_refused_out_loud():
    r = keep("--allow", "/tmp")
    assert r.returncode == 2 and "nothing to run" in r.stderr


def test_an_unknown_argument_is_refused_out_loud():
    r = keep("--bogus", "--", "true")
    assert r.returncode == 2 and "unknown argument" in r.stderr


def test_a_missing_grant_is_refused_out_loud(tmp_path):
    r = keep("--allow", str(tmp_path / "nope"), "--", "true")
    assert r.returncode != 0 and "does not exist" in r.stderr
