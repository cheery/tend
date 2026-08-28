"""`tools/resolve.sh` — a pull with no runner gets one, from the person's
side of the fence (board/resolver.md, 2026-08-26).

The resolver reads a count and takes a lock; it starts the one runner
only when the ledger holds a pull no runner has served.  These tests run
it by hand with a scratch state directory; as a hook it is the same
script with its stdin drained.  From inside the fence the runner it
starts dies with the test's command, which is fine here — service is
checked within the test.
"""

import json
import os
import pathlib
import subprocess
import sys
import time

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
RESOLVE = ROOT / "tools" / "resolve.sh"
NODE = ROOT / "node" / "node.py"


def _env(tmp_path):
    e = dict(os.environ, TEND_NODE_STATE_DIR=str(tmp_path / "st"), TEND_NODE_IDLE="0.6")
    e.pop("TEND_FENCED", None)
    return e


def resolve(tmp_path, *args, **kw):
    return subprocess.run(["sh", str(RESOLVE), *args], env={**_env(tmp_path), **kw.pop("env", {})},
                          capture_output=True, text=True, timeout=20, **kw)


def pull(tmp_path):
    (tmp_path / "st").mkdir(exist_ok=True)
    subprocess.run(["/usr/bin/python3", str(NODE), "--state", str(tmp_path / "st" / "node.state"), "pull"],
                   check=True, capture_output=True)


def state(tmp_path):
    return json.loads((tmp_path / "st" / "node.state").read_text())


def wait(pred, cap=5.0):
    t = time.monotonic()
    while time.monotonic() - t < cap:
        if pred():
            return True
        time.sleep(0.05)
    return pred()


def test_it_parses():
    assert subprocess.run(["sh", "-n", str(RESOLVE)]).returncode == 0


def test_nothing_pulled_starts_nothing(tmp_path):
    (tmp_path / "st").mkdir()
    r = resolve(tmp_path)
    assert r.returncode == 0 and r.stderr == "", r.stderr
    assert not (tmp_path / "st" / "node.state").exists()


def test_unserved_pulls_and_no_runner_start_one_that_serves_them(tmp_path):
    """The card's owed demonstration, from outside: two pulls sit in the
    ledger with nobody running; the resolver starts the one runner and
    the runner serves the backlog it was born after."""
    if not os.path.exists("/usr/bin/python3"):
        pytest.skip("no system python3 for keep to grant the node")
    pull(tmp_path); pull(tmp_path)
    r = resolve(tmp_path)
    assert r.returncode == 0 and "started one" in r.stderr, r.stderr
    assert wait(lambda: (tmp_path / "st" / "node.state").exists() and state(tmp_path)["pulls"] == 2), \
        (tmp_path / "st" / "run.log").read_text() if (tmp_path / "st" / "run.log").exists() else "no run.log"
    assert state(tmp_path)["generations"] == 1


def test_a_second_look_while_the_runner_is_up_starts_no_other(tmp_path):
    """Back to back, as a hook fires at every command: the first look
    starts the runner and waits for its lock; the second sees it."""
    if not os.path.exists("/usr/bin/python3"):
        pytest.skip("no system python3 for keep to grant the node")
    pull(tmp_path)
    a = resolve(tmp_path); b = resolve(tmp_path)
    assert "started one" in a.stderr and b.stderr == "", (a.stderr, b.stderr)
    assert wait(lambda: (tmp_path / "st" / "node.state").exists() and state(tmp_path)["pulls"] == 1)
    assert wait(lambda: state(tmp_path)["last_stop"] is not None, cap=6)
    assert state(tmp_path)["generations"] == 1


def test_every_pull_served_means_silence(tmp_path):
    if not os.path.exists("/usr/bin/python3"):
        pytest.skip("no system python3 for keep to grant the node")
    pull(tmp_path)
    resolve(tmp_path)
    assert wait(lambda: (tmp_path / "st" / "node.state").exists() and state(tmp_path)["last_stop"] is not None, cap=6)
    r = resolve(tmp_path)
    assert r.returncode == 0 and r.stderr == "", r.stderr
    assert state(tmp_path)["generations"] == 1


def test_the_hook_drains_its_stdin_and_never_blocks(tmp_path):
    (tmp_path / "st").mkdir()
    r = resolve(tmp_path, "--hook", input='{"tool_name":"Bash","tool_input":{"command":"x"}}')
    assert r.returncode == 0 and r.stdout == "" and r.stderr == ""


def test_install_is_refused_inside_the_fence(tmp_path):
    r = resolve(tmp_path, "--install", env={"TEND_FENCED": "1"})
    assert r.returncode == 2 and "person's" in r.stderr


def test_an_unknown_argument_is_refused(tmp_path):
    r = resolve(tmp_path, "--bogus")
    assert r.returncode == 2 and "unknown argument" in r.stderr


def test_the_hook_relays_a_ring_the_fence_could_not_sound(tmp_path):
    """card:silent-cord.md day one: the resolver's hook runs on the person's
    side after every command, so it is where a fenced session's failed
    ring becomes a sound — the same seam a pull already crosses, and
    never a daemon."""
    andon_state = tmp_path / "andon"
    marker = tmp_path / "played"
    fake = tmp_path / "player.sh"
    fake.write_text('#!/bin/sh\necho x >> "%s"\n' % marker); fake.chmod(0o755)
    env = {"TEND_ANDON_STATE": str(andon_state), "TEND_ANDON_PLAYER": "false", "TEND_ANDON_GAP": "0"}
    subprocess.run(["sh", str(ROOT / "tools" / "andon.sh"), "ask", "q"], env={**os.environ, **env}, check=True, capture_output=True)
    subprocess.run(["sh", str(ROOT / "tools" / "andon.sh"), "ring"], env={**os.environ, **env}, capture_output=True)
    assert "ring-failed" in (andon_state / "andon.log").read_text()
    r = resolve(tmp_path, "--hook", env={**env, "TEND_ANDON_PLAYER": str(fake)})
    assert r.returncode == 0, r.stderr
    assert marker.exists() and marker.read_text().count("x") == 1
    assert "relayed" in (andon_state / "andon.log").read_text()
