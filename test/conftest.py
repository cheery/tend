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
"""
import os
import pytest


@pytest.fixture(autouse=True)
def _git_is_the_fixtures_own(monkeypatch):
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", os.devnull)
    monkeypatch.setenv("GIT_CONFIG_SYSTEM", os.devnull)
    for who in ("AUTHOR", "COMMITTER"):
        monkeypatch.setenv(f"GIT_{who}_NAME", "t")
        monkeypatch.setenv(f"GIT_{who}_EMAIL", "t@t")
