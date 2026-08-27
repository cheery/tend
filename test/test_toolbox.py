"""`tools/toolbox.sh` — one command from fresh clone to working clone.

Henri's ask, 2026-08-24: *"please create a tools/toolbox.sh to install
all tools you need, also those that are present."*  The property that
matters is idempotence — a setup script that is only safe on a fresh
clone is one nobody dares re-run, and then nobody knows what state a
clone is in.
"""

import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
TOOLBOX = ROOT / "tools" / "toolbox.sh"


def sh(*args):
    return subprocess.run(["sh", str(TOOLBOX), *args], cwd=ROOT,
                          capture_output=True, text=True)


def test_it_parses():
    assert subprocess.run(["sh", "-n", str(TOOLBOX)]).returncode == 0


def test_check_changes_nothing_and_says_so():
    r = sh("--check")
    assert "nothing was changed" in r.stdout


def test_a_missing_requirement_is_named_with_its_reason():
    """Every ✗ line must say why the thing is needed — a bare list of
    package names is a chore; a list of reasons is a decision the
    stranger can make."""
    r = sh("--check")
    for line in r.stdout.splitlines():
        if "✗" in line:
            assert "—" in line, f"names no reason: {line}"


def test_an_unknown_argument_is_refused_out_loud():
    r = sh("--bogus")
    assert r.returncode == 2
    assert "unknown argument" in r.stderr


def test_the_launcher_and_the_second_node_are_declared():
    """Install-testing is only not-hard if the check covers what the tree
    actually runs (spec/os.md property 2).  The launcher's run-lock
    (flock) and detached start (setsid) and the second node's program
    (llama-server) arrived after this script was first written; a clone
    that passes toolbox.sh must not then fail to run a node for a
    dependency nobody named.  card:work-environment-ai.md, 2026-08-27."""
    text = TOOLBOX.read_text()
    # declared in the source with a reason (the need/want call carries it;
    # a present tool's runtime line is just a tick, the reason shows when absent)
    for tool in ("flock", "setsid", "llama-server"):
        decl = [l for l in text.splitlines()
                if re.match(rf'\s*(need|want)\s+{re.escape(tool)}\s+"', l)]
        assert decl, f"the toolbox does not declare {tool} with a reason"
    # and the check runs clean over the new lines
    assert sh("--check").returncode in (0, 1)
