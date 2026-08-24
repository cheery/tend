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
        assert len(row) == 5, row
    assert rows[1][2] == "3", "the ledger keeps the exit code"
    assert "sh -c exit 3" in rows[1][4], "and the command"


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
