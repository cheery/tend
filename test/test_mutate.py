"""`tools/mutate.sh` — the harness that asks whether a detector detects.

`board/green.md`: a gate that has only ever passed is a claim.  This
checks the harness's own two claims and nothing more — the recorded
sweep is minutes and is run by a hand, not at every commit.
"""

import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
MUTATE = ROOT / "tools" / "mutate.sh"


def run(*args):
    return subprocess.run(["bash", str(MUTATE), *args], cwd=ROOT,
                          capture_output=True, text=True)


def test_it_parses():
    assert subprocess.run(["bash", "-n", str(MUTATE)]).returncode == 0


def test_a_detected_break_is_red_and_an_empty_one_is_noop():
    """One copy each.  `suite.py` made unable to fail is the break
    `test/test_suite.py` was written for on 2026-08-26, so it is red by
    name; and a shell that changes nothing is `NOOP`, never a verdict —
    the morning's scratch harness reported one of those as GREEN."""
    r = run("test/test_suite.py", 'sed -i "s/^    return r.returncode/    return 0/" tools/suite.py')
    assert r.returncode == 0, r.stdout + r.stderr
    assert "test_a_failing_test_is_a_failed_gate" in r.stdout
    r = run("test/test_suite.py", "true")
    assert r.returncode == 3
    assert "NOOP" in r.stdout


def test_an_unknown_argument_is_refused_out_loud():
    assert run("--bogus").returncode == 2
