"""`tools/leash.sh` — the budget holds, the exit code survives, the
ledger fills.

The first instrument tend builds, so `manifesto.md` §"The three ways an
instrument fails" applies in full and the hang test below is the
"break it and watch it notice" — the leash's one hard claim is exercised
by giving it a hang, before anything trusts it.

Nothing here touches the real ledger: TEND_LEASH_LOG points at a
temporary file throughout.
"""

import os
import pathlib
import subprocess
import time

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
LEASH = ROOT / "tools" / "leash.sh"


def leash(tmp_path, *args, log=None):
    env = dict(os.environ,
               TEND_LEASH_LOG=str(log or (tmp_path / "leash.log")))
    return subprocess.run(["sh", str(LEASH), *args], env=env,
                          capture_output=True, text=True)


def lines(tmp_path):
    log = tmp_path / "leash.log"
    return [l.split("\t") for l in log.read_text().splitlines()] \
        if log.exists() else []


def test_it_parses():
    assert subprocess.run(["sh", "-n", str(LEASH)]).returncode == 0


def test_the_command_and_its_exit_code_pass_through(tmp_path):
    r = leash(tmp_path, "-t", "30", "--", "echo", "hello")
    assert r.returncode == 0
    assert r.stdout.strip() == "hello"
    r = leash(tmp_path, "-t", "30", "--", "sh", "-c", "exit 7")
    assert r.returncode == 7, "a failure must arrive as itself, not as the leash's"


def test_a_hang_is_a_crash(tmp_path):
    """The claim the card makes, exercised: a command that would sit
    past its budget is killed, says so, and says so quickly."""
    began = time.monotonic()
    r = leash(tmp_path, "-t", "1", "--", "sleep", "30")
    took = time.monotonic() - began
    assert r.returncode == 124
    assert took < 20, f"the kill itself hung ({took:.0f}s)"
    assert "budget is spent" in r.stderr


def test_the_commands_own_124_is_not_the_leashs(tmp_path):
    """2026-08-25: a payload whose own `timeout 3` expired came back as
    "the 900s budget is spent".  124 is the budget only if the clock
    agrees; otherwise it is the command's code, passed through in
    silence like any other."""
    r = leash(tmp_path, "-t", "30", "--", "timeout", "0.2", "sleep", "5")
    assert r.returncode == 124
    assert "budget is spent" not in r.stderr


def test_the_kill_takes_the_orphans_too(tmp_path):
    """**Found on the first real run's doorstep**, 2026-08-24: `timeout`
    signals only the process it started.  A `suite.py` killed at its
    budget would leave the fenced pytest it spawned running on, which is
    the polling-shells shape of the very incident the leash is for.  In
    scope mode the stop reaps the cgroup; this spawns a detached sleeper
    with a marker nobody else uses and checks it did not survive."""
    marker = "31415926"
    r = leash(tmp_path, "-t", "1", "--", "sh", "-c",
              f"sleep {marker} & sleep 300")
    assert r.returncode == 124
    how = lines(tmp_path)[0][3].split()[-1]
    if how != "scope":
        pytest.skip("no systemd user manager here; plain mode has this gap and says so")
    time.sleep(0.5)
    left = subprocess.run(["pgrep", "-f", f"[s]leep {marker}"],
                          capture_output=True, text=True).stdout.split()
    for pid in left:
        subprocess.run(["kill", pid])
    assert not left, f"the orphan outlived the leash: pids {left}"


def test_every_invocation_leaves_one_ledger_line(tmp_path):
    leash(tmp_path, "-t", "30", "--", "true")
    leash(tmp_path, "-t", "30", "--", "sh", "-c", "exit 3")
    rows = lines(tmp_path)
    assert len(rows) == 2
    for row in rows:
        assert len(row) == 6, row
    assert rows[1][2] == "3", "the ledger keeps the exit code"
    assert "sh -c exit 3" in rows[1][5], "and the command"


def test_every_line_says_what_the_load_cost(tmp_path):
    """**A load is a number** — the countermeasure for believing a
    light one on 2026-08-24.  A spinner for a second shows about a
    CPU-second; `true` shows about none; both are numbers, not names."""
    leash(tmp_path, "-t", "30", "--", "sh", "-c",
          "timeout 1 sh -c 'while :; do :; done'; true")
    leash(tmp_path, "-t", "30", "--", "true")
    spun, idle = (float(r[4].removeprefix("cpu=").removesuffix("s"))
                  for r in lines(tmp_path))
    assert spun >= 0.5, f"a second of spinning cost {spun}s?"
    assert idle < 0.2


def test_scope_mode_counts_the_work_not_the_wrapper(tmp_path):
    """**The leash's first outside run found this**, 2026-08-25: the
    ledger read cpu=1.3s for a 25-minute suite.  In scope mode the work
    is a child of the user manager, so `times` — the shell's account of
    its own children — sees only the `systemd-run` client.  The fix reads
    the scope's cgroup tally instead.  A ~1.5s single-core burn must show
    ~1.5 CPU-seconds; the old code showed near zero here, which is the
    regression this guards.  Plain mode has the command as a true child
    and does not have the bug, so it skips."""
    burn = 1.5
    r = leash(tmp_path, "-t", "30", "-c", "100", "--", "sh", "-c",
              f"timeout {burn} sh -c 'while :; do :; done'; true")
    how = lines(tmp_path)[0][3].split()[-1]
    if how != "scope":
        pytest.skip("no systemd user manager here; times is correct in plain mode")
    cpu = lines(tmp_path)[0][4]
    assert cpu != "cpu=?s", "scope mode could not read the cgroup — the number is lost"
    secs = float(cpu.removeprefix("cpu=").removesuffix("s"))
    # A band, not a floor: `-c 100` is one core, so ~`burn` CPU-seconds is
    # the known amount.  The low end catches the bug this exists for — the
    # wrapper's near-zero.  The high end catches its mirror — counting a
    # subtree twice, or the whole session's cgroup instead of the scope's.
    # A sensor is suspected until a check pins both sides of it.
    assert 0.7 <= secs <= burn * 1.6, \
        f"a {burn}s single-core burn read {secs}s — outside tolerance for the work"


def test_the_ledger_says_whether_the_budget_really_applied(tmp_path):
    """`scope` or `plain`, on every line — a budget that silently did
    not apply is the one lie this instrument must not tell."""
    leash(tmp_path, "-t", "30", "--", "true")
    assert lines(tmp_path)[0][3].split()[-1] in ("scope", "plain")


def test_a_dead_ledger_does_not_take_the_work_with_it(tmp_path):
    r = leash(tmp_path, "-t", "30", "--", "echo", "still runs",
              log="/proc/nowhere/leash.log")
    assert r.returncode == 0
    assert "still runs" in r.stdout


def test_no_command_is_refused_out_loud(tmp_path):
    r = leash(tmp_path)
    assert r.returncode == 2
    assert "no command" in r.stderr


def test_an_unknown_option_is_refused_out_loud(tmp_path):
    r = leash(tmp_path, "--bogus", "true")
    assert r.returncode == 2


def test_the_wall_clock_includes_the_leashs_own_probe(tmp_path):
    """2026-08-26: a runner's ledger line started ten seconds after its
    launch, because the scope probe ran before the clock was stamped —
    the probe's cost was invisible.  A fake `systemd-run` on PATH sleeps
    one second and refuses (so the mode is plain); the line's wall must
    carry that second."""
    fake = tmp_path / "bin"; fake.mkdir()
    (fake / "systemd-run").write_text("#!/bin/sh\nsleep 1.1\nexit 1\n")
    (fake / "systemd-run").chmod(0o755)
    log = tmp_path / "leash.log"
    env = dict(os.environ, TEND_LEASH_LOG=str(log), PATH=f"{fake}:{os.environ['PATH']}")
    r = subprocess.run(["sh", str(LEASH), "--", "true"], env=env, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    line = log.read_text().strip().splitlines()[-1].split("\t")
    assert "plain" in line[3], line
    assert int(line[1]) >= 1, f"the probe's second is not in the wall: {line}"
