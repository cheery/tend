"""`tools/sandbox.sh` — the fence is up, the clock first.

The sessions-first trial of 2026-08-25 (`doc/experiments/2026-08-25-both.md`)
promoted to a tool.  What is checked here is what that day found: a
fence that hides the state directory defeats the sitting limit, so the
check that matters most is not that `~/.ssh` is gone but that the
sitting clock inside is the host's.  `--check` is the mechanism and
these tests are what say it still says the truth.

Everything that needs bubblewrap skips, out loud, on a machine without
it — a skipped fence test is not a passing one, and the skip reason
names the package.
"""

import os
import pathlib
import shutil
import subprocess

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
FENCE = ROOT / "tools" / "sandbox.sh"

#: Inside the fence these skip, and the pre-commit gate now runs inside
#: the fence, so at a commit the fence's own tests do not run.  They run
#: when the suite is run by a person outside, and `--check` is what a
#: person runs to see the fence is up.  Skipped, named, not hidden.
needs_bwrap = pytest.mark.skipif(
    shutil.which("bwrap") is None or os.environ.get("TEND_FENCED") == "1",
    reason="no bubblewrap here, or already inside the fence — it cannot nest")


def sandbox(*args, **kw):
    return subprocess.run(["sh", str(FENCE), *args], cwd=ROOT,
                          capture_output=True, text=True, **kw)


def test_it_parses():
    assert subprocess.run(["sh", "-n", str(FENCE)]).returncode == 0


def test_the_rows_are_the_dial():
    out = sandbox("--rows")
    assert out.returncode == 0
    names = [line.split()[1] for line in out.stdout.splitlines() if line.strip()]
    assert names == ["tree", "state", "trees", "scratch", "git", "net", "audio", "display", "bus"]
    on = [line.split()[0] for line in out.stdout.splitlines() if line.strip()]
    assert on == ["on"] * 5 + ["off"] * 4, "five on by default, four off until asked"


@needs_bwrap
def test_check_says_the_fence_is_up_here():
    out = sandbox("--check")
    assert out.returncode == 0, out.stdout + out.stderr
    assert "the fence is up" in out.stdout
    assert out.stdout.index("sitting clock") < out.stdout.index("~/.ssh"), \
        "the clock is proved before the secrets — that is the order the day taught"


@needs_bwrap
def test_inside_the_tree_is_writable_and_home_is_not_real():
    out = sandbox("sh", "-c", 'test -w "$PWD" && ! test -e "$HOME/.bashrc" && echo ok')
    assert out.stdout.strip() == "ok", out.stderr


@needs_bwrap
def test_inside_is_marked_and_cannot_nest():
    out = sandbox("sh", "-c", 'echo "$TEND_FENCED"')
    assert out.stdout.strip() == "1"
    nested = sandbox("sh", str(FENCE), "true")
    assert nested.returncode == 3 and "cannot nest" in nested.stderr


@needs_bwrap
def test_the_restraints_are_read_only_inside():
    """`board/fence.md`'s measurement: from a tend session, `python3 -c`
    rewrote `.claude/settings.json` and `mv` made it vanish.  Inside the
    fence the tree is the world — except this directory.  This is the
    demonstration the card owed: what it caught, that had gone through."""
    settings = ROOT / ".claude" / "settings.json"
    before = settings.read_bytes()
    out = sandbox("sh", "-c",
                  f"python3 -c \"open('{settings}', 'a').write('x')\" 2>&1; "
                  f"mv '{settings}' '{settings}.away' 2>&1; touch '{settings}.probe' 2>&1")
    assert settings.read_bytes() == before
    assert not settings.with_suffix(".json.away").exists()
    assert not settings.with_suffix(".json.probe").exists()
    assert out.stdout.count("Read-only file system") + out.stdout.count("Kirjoitussuojattu") >= 3, out.stdout


@needs_bwrap
def test_the_state_directory_passes_through(tmp_path):
    """The finding of `2026-08-25-reach.md`: without this, a fenced
    session gets a fresh sitting clock."""
    probe = pathlib.Path.home() / ".local" / "state" / ".test-sandbox-probe"
    try:
        sandbox("sh", "-c", f'touch "{probe}"')
        assert probe.exists(), "written inside, must be there outside"
    finally:
        probe.unlink(missing_ok=True)


@needs_bwrap
def test_the_network_is_off_and_a_row_turns_it_on():
    off = sandbox("sh", "-c", "timeout 5 getent ahostsv4 example.com")
    assert off.returncode != 0, "off by default"
    if subprocess.run(["timeout", "5", "getent", "ahostsv4", "example.com"],
                      capture_output=True).returncode != 0:
        pytest.skip("no network outside the fence either — the row cannot be shown to work")
    on = sandbox("--reach", "net", "sh", "-c", "timeout 5 getent ahostsv4 example.com")
    assert on.returncode == 0, on.stderr


def test_an_unknown_row_is_refused_out_loud():
    out = sandbox("--reach", "moon", "true")
    assert out.returncode == 2 and "no such row" in out.stderr


def test_nothing_to_run_is_refused_out_loud():
    out = sandbox()
    assert out.returncode == 2 and "nothing to run" in out.stderr
