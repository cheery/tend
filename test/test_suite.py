"""`tools/suite.py` — one name for the gates, and it has to be able to say no.

Until 2026-08-26 nothing read this script's exit code: `board/green.md`'s
day-one measurement replaced `return r.returncode` with `return 0`, the
whole suite passed (178 of 178), and the pre-commit hook — one `if`
around this script — refused nothing.  So: a copy of the script over a
`test/` with one failing test returns non-zero and says a gate failed;
over a passing one it returns zero and says the gates hold.
"""

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SUITE = ROOT / "tools" / "suite.py"


def _tree(tmp_path, body):
    (tmp_path / "tools").mkdir()
    (tmp_path / "tools" / "suite.py").write_text(SUITE.read_text(encoding="utf-8"))
    (tmp_path / "test").mkdir()
    (tmp_path / "test" / "test_one.py").write_text(body)
    return subprocess.run([sys.executable, "tools/suite.py", "-p", "no:cacheprovider"],
                          cwd=tmp_path, capture_output=True, text=True)


def test_a_failing_test_is_a_failed_gate(tmp_path):
    r = _tree(tmp_path, "def test_no():\n    assert False\n")
    assert r.returncode != 0
    assert "a gate failed" in r.stdout


def test_a_passing_suite_holds(tmp_path):
    r = _tree(tmp_path, "def test_yes():\n    assert True\n")
    assert r.returncode == 0, r.stdout + r.stderr
    assert "the gates hold" in r.stdout
