"""`node/node.py` — the first program tend runs (board/pull.md).

The stranger test as code: start it, pull it, stop, and it stops itself;
open it again and it is where it was left.  What is checked is exactly
the three properties the card builds — pull lifecycle, opens-where-left,
may-not-hang — and that the state is plain JSON a person could read.
"""

import json
import pathlib
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
NODE = ROOT / "node" / "node.py"


def node(state, *args, timeout=15):
    return subprocess.run([sys.executable, str(NODE), "--state", str(state), *args],
                          capture_output=True, text=True, timeout=timeout)


def read(state):
    return json.loads(pathlib.Path(state).read_text())


def test_it_parses():
    assert subprocess.run([sys.executable, "-m", "py_compile", str(NODE)]).returncode == 0


def test_the_node_is_a_directory(tmp_path):
    """The card's line: no bundle format beyond a directory.  The node is
    the directory holding node.py, and nothing else is required to run."""
    assert (ROOT / "node").is_dir()
    assert list((ROOT / "node").glob("*.py")) == [NODE]


def test_a_pull_with_no_runner_is_not_served(tmp_path):
    """The lifecycle, from the empty side: a pull when nothing runs is
    recorded in the ledger and served by no one — not an error."""
    state = tmp_path / "n.state"
    node(state, "pull")
    assert (tmp_path / "n.state.pull").exists()
    st = read(state) if state.exists() else {"pulls": 0}
    assert st["pulls"] == 0, "nothing running served it"


def test_run_serves_pulls_then_stops_itself(tmp_path):
    """Start it, pull it twice, stop pulling — and it exits on its own
    within the idle window.  The whole property in one run."""
    state = tmp_path / "n.state"
    began = time.monotonic()
    p = subprocess.Popen([sys.executable, str(NODE), "--state", str(state),
                          "run", "--idle", "1.5", "--poll", "0.05"],
                         stdout=subprocess.PIPE, text=True)
    time.sleep(0.6)
    node(state, "pull")
    time.sleep(0.2)
    node(state, "pull")
    p.wait(timeout=15)
    took = time.monotonic() - began
    assert p.returncode == 0
    assert took < 10, f"the self-stop hung ({took:.1f}s)"
    st = read(state)
    assert st["pulls"] == 2, st
    assert st["generations"] == 1
    assert st["last_stop"] is not None


def test_it_opens_where_it_was_left(tmp_path):
    """Item 8.  A second generation restores the first's tally rather than
    starting over — the state file is the whole of 'where it was left'."""
    state = tmp_path / "n.state"
    node(state, "pull")
    p = subprocess.Popen([sys.executable, str(NODE), "--state", str(state),
                          "run", "--idle", "0.8", "--poll", "0.05"])
    time.sleep(0.3)
    node(state, "pull")
    p.wait(timeout=15)
    first = read(state)
    assert first["generations"] == 1 and first["pulls"] == 1
    p = subprocess.Popen([sys.executable, str(NODE), "--state", str(state),
                          "run", "--idle", "0.8", "--poll", "0.05"])
    p.wait(timeout=15)
    second = read(state)
    assert second["generations"] == 2, "it counted this as a new opening"
    assert second["pulls"] == 1, "and kept what the last generation did"
    assert second["runtime_s"] >= first["runtime_s"]


def test_a_run_nobody_pulls_stops_on_idle(tmp_path):
    """Item 13, the bare case: pulled by no one, it still shuts itself
    down — the node's default is off."""
    state = tmp_path / "n.state"
    began = time.monotonic()
    r = node(state, "run", "--idle", "0.5", "--poll", "0.05")
    assert r.returncode == 0
    assert time.monotonic() - began < 8
    assert "stopped" in r.stdout


def test_status_reads_what_it_did_without_the_node(tmp_path):
    """The stranger reads the state, not the code.  status is a
    convenience over a file that is already plain and legible."""
    state = tmp_path / "n.state"
    node(state, "pull")
    node(state, "run", "--idle", "0.4", "--poll", "0.05")
    raw = (tmp_path / "n.state").read_text()
    json.loads(raw)  # plain JSON, no framing
    r = node(state, "status")
    assert "node tally" in r.stdout and "generations" in r.stdout


def test_a_corrupt_state_is_not_silent(tmp_path):
    """Item 14: errors are brought out.  A state file that is not JSON
    stops the node loudly rather than resetting the tally to zero."""
    state = tmp_path / "n.state"
    state.write_text("{ not json\n")
    r = node(state, "status")
    assert r.returncode != 0
    assert "JSON" in r.stderr or "json" in r.stderr
