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
"""
import os
import pytest


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
