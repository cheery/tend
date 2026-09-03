"""The suite builds every git tree it means, and none of them is the person's.

A fixture that runs `git commit` with `-c user.name=t` had still been
inheriting the rest of the person's `~/.gitconfig` — on the work laptop,
2026-08-28, `commit.gpgsign = true` with an SSH key that the fence keeps
out (`tools/sandbox.sh` probes that `~/.ssh` does not exist), and 43
tests plus 11 errors went red on "Couldn't load public key".  That is
`board/README.md`'s fixture rule in one more face: a test builds the
side it means; it never copies the live thing as it is.  So every test
runs with no global or system git config and an identity of its own,
and a fixture's commit is the fixture's, on any machine.

The same rule for the canvas (card:hold.md, 2026-08-29): a hold on the
desk's canvas is a standing pull, and the day it landed the gate caught
`test_resolve.py` reading the person's `node.hold` through the inherited
environment and starting the real node into a scratch state.  So every
test runs with TEND_CANVAS at a scratch directory of its own; a test
that means a hold writes one there.

And for the index (F006, 2026-08-30): git hands its pre-commit hook a
`GIT_INDEX_FILE`, and for a commit with a pathspec that is an absolute
temporary index; every `git add` in the suite inherited it, and
`test_precommit.py`'s scratch tree put its stub `tools/suite.py` — a
blob only the scratch repository holds — into the tree's own commit,
which died on "invalid object" after the gates had passed.  So the git
fixture drops every variable that would point a fixture's git at a
repository it did not build.

And for a lock (card:lock-test.md, 2026-09-03): the tree asks "is this
lock held?" by taking the lock, and two such tests collide — F019 and F020
were that on two sides, each reproduced from scratch harnesses over a
morning.  So the suite carries the two instruments those mornings built:
`hammer`, a loop of the readers that collide (a raw `flock -n FILE true`
read is wrong about half the time under it, measured), and `hold`, a
process that holds a lock for a window, shared or exclusive, so a test can
put a real holder or a momentary contender in front of the code it means.
"""
import contextlib
import os
import subprocess
import time
import pytest

HAMMER = 'echo hammering; while :; do flock -n "$1" true; done'
HOLDER = 'exec 9<>"$1"; flock $2 9 || exit 3; echo held; exec sleep "$3"'


@contextlib.contextmanager
def _hammer(path):
    """Readers colliding on PATH's lock: a tight loop of `flock -n PATH true`,
    the exact shape of the tree's raw lock reads, in the background until
    the block ends.  Under it a single raw read says held of a free lock
    about half the time; a read across a window does not (F019, F020).
    Yields once the loop is up and its first reader has had time to fork
    (the shell says so; 10 ms is ten forks).  A reader holds the lock for
    a fraction of each ~1 ms round, so a probe of the hammer spreads its
    reads over many rounds, never a burst inside one."""
    p = subprocess.Popen(["sh", "-c", HAMMER, "_", str(path)], stdout=subprocess.PIPE)
    try:
        assert p.stdout.readline() == b"hammering\n", f"the hammer did not start on {path}"
        time.sleep(0.01)
        yield p
    finally:
        p.kill()
        p.wait()


@contextlib.contextmanager
def _hold(path, seconds=30, shared=False):
    """A process holding PATH's lock — exclusive like a runner on run.lock,
    or `shared=True` like a puller on its edge — for SECONDS, or until the
    block ends.  Yields once the lock is held (the holder says so on its
    stdout; no lock test is made), so the code under test meets a holder
    and never a race with the fixture.  `exec sleep`, so killing the
    holder drops the lock: `flock FILE sleep` leaves the sleep holding an
    inherited fd after flock is killed (measured, F020's day one)."""
    p = subprocess.Popen(["sh", "-c", HOLDER, "_", str(path), "-s" if shared else "", str(seconds)],
                         stdout=subprocess.PIPE)
    try:
        assert p.stdout.readline() == b"held\n", f"the holder did not take {path}"
        yield p
    finally:
        if p.poll() is None:
            p.kill()
        p.wait()


@pytest.fixture
def hammer():
    return _hammer


@pytest.fixture
def hold():
    return _hold


@pytest.fixture(autouse=True)
def _the_canvas_is_the_fixtures_own(monkeypatch, tmp_path):
    monkeypatch.setenv("TEND_CANVAS", str(tmp_path / "canvas"))


@pytest.fixture(autouse=True)
def _the_failure_ledger_is_the_fixtures_own(monkeypatch, tmp_path):
    """card:flake.md, the evening it landed: test_precommit.py's scratch tree
    runs the suite over a test that must fail, and five lines of
    `test_one.py::test_no` reached the person's ~/.local/state/tend/failed.log
    before the commit was an hour old — a fixture's failure counted as the
    machine's.  The same rule as the canvas: every test's ledger is its own."""
    monkeypatch.setenv("TEND_FAILED_LOG", str(tmp_path / "failed.log"))


@pytest.fixture(autouse=True)
def _git_is_the_fixtures_own(monkeypatch):
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", os.devnull)
    monkeypatch.setenv("GIT_CONFIG_SYSTEM", os.devnull)
    for who in ("AUTHOR", "COMMITTER"):
        monkeypatch.setenv(f"GIT_{who}_NAME", "t")
        monkeypatch.setenv(f"GIT_{who}_EMAIL", "t@t")
    for var in ("GIT_INDEX_FILE", "GIT_DIR", "GIT_WORK_TREE", "GIT_OBJECT_DIRECTORY", "GIT_COMMON_DIR"):
        monkeypatch.delenv(var, raising=False)   # F006: a fixture's git never reaches the index git handed the hook
