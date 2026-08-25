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

import json
import os
import pathlib
import re
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
    assert names == ["tree", "state", "trees", "scratch", "git", "net", "audio", "display"]
    on = [line.split()[0] for line in out.stdout.splitlines() if line.strip()]
    assert on == ["on"] * 5 + ["off"] * 3, "five on by default, three off until asked"


def test_the_bus_is_not_a_row():
    """Measured 2026-08-25 (`board/done/grant.md`): with the user bus inside,
    `systemd-run --user --wait` ran a command on the host — home, PATH
    and no fence — because the manager spawns it, not the caller.  The
    row's one caller, the leash, now wraps the fence from outside.  A
    row with no caller that is also an escape is not a row."""
    out = sandbox("--reach", "bus", "true")
    assert out.returncode == 2 and "no such row" in out.stderr


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


def test_the_protected_set_is_the_scripts_the_hooks_run():
    """`board/self.md`'s line: a path is in the set if a session editing it
    changes what the session is allowed to do before anyone looks.  That
    is every script a hook runs — read fresh, unfenced, as the person —
    and not `leash.sh`, which shapes cost.  The set is read from this
    clone's settings, so a hook added without its script being protected
    is caught here."""
    out = sandbox("--protected")
    assert out.returncode == 0
    protected = set(out.stdout.split())
    settings = json.loads((ROOT / ".claude" / "settings.json").read_text(encoding="utf-8"))
    hooked = set()
    for event in settings["hooks"].values():
        for group in event:
            for h in group["hooks"]:
                m = re.search(r"tools/([\w-]+\.sh)", h["command"])
                assert m, h["command"]
                hooked.add("tools/" + m.group(1))
    assert hooked <= protected, f"a hook runs a script outside the protected set: {hooked - protected}"
    assert "tools/leash.sh" not in protected, "leash.sh shapes cost; it is not in the set"
    for p in protected:
        assert (ROOT / p).is_file(), p


@needs_bwrap
def test_the_fences_own_code_is_read_only_inside():
    """`board/self.md`'s measurement, 2026-08-25: an edit to this script
    from inside the fence was in force on the very next command.  Now the
    set is bound read-only: a write is EROFS and the mountpoint cannot be
    renamed or removed."""
    protected = sandbox("--protected").stdout.split()
    before = {p: (ROOT / p).read_bytes() for p in protected}
    for p in protected:
        f = ROOT / p
        out = sandbox("sh", "-c",
                      f"echo x >> '{f}' 2>&1; mv '{f}' '{f}.away' 2>&1; rm -f '{f}' 2>&1; echo rc=$?")
        assert (ROOT / p).read_bytes() == before[p], p
        assert not f.with_name(f.name + ".away").exists(), p
        assert "Read-only file system" in out.stdout or "Kirjoitussuojattu" in out.stdout, (p, out.stdout)


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
