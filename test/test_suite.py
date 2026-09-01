"""`tools/suite.py` — one name for the gates, and it has to be able to say no.

Until 2026-08-26 nothing read this script's exit code: `board/green.md`'s
day-one measurement replaced `return r.returncode` with `return 0`, the
whole suite passed (178 of 178), and the pre-commit hook — one `if`
around this script — refused nothing.  So: a copy of the script over a
`test/` with one failing test returns non-zero and says a gate failed;
over a passing one it returns zero and says the gates hold.
"""

import os
import pathlib
import shutil
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


# --- the failure ledger and the shake (card:flake.md, 2026-08-29 — Henri: "Would there be a way to catch the flake?") ---

def _run(tmp_path, body, *args, env=None):
    (tmp_path / "tools").mkdir(exist_ok=True)
    (tmp_path / "tools" / "suite.py").write_text(SUITE.read_text(encoding="utf-8"))
    (tmp_path / "test").mkdir(exist_ok=True)
    # two bodies of one length written in one second are one file to pytest's
    # assertion-rewrite cache (mtime + size): test_yes ran test_no's bytecode
    # until this — the 2026-08-26 fixture rule, a seam with nothing on either side
    shutil.rmtree(tmp_path / "test" / "__pycache__", ignore_errors=True)
    (tmp_path / "test" / "test_one.py").write_text(body)
    e = dict(os.environ, TEND_FAILED_LOG=str(tmp_path / "failed.log"))
    e.pop("TEND_SUITE_WHERE", None)      # the seat is the test's to name, never the gate's inherited one
    e.update(env or {})
    return subprocess.run([sys.executable, "tools/suite.py", *args, "-p", "no:cacheprovider"],
                          cwd=tmp_path, capture_output=True, text=True, env=e)


def test_a_failed_test_is_a_line_on_the_ledger_and_a_passing_suite_leaves_none(tmp_path):
    r = _run(tmp_path, "def test_no():\n    assert False\n")
    assert r.returncode != 0
    lines = (tmp_path / "failed.log").read_text().splitlines()
    assert len(lines) == 1, lines
    assert "test_one.py::test_no" in lines[0] and "  hand  " in lines[0] and "load " in lines[0] and "wall " in lines[0], lines[0]
    assert str(tmp_path / "failed.log") in r.stdout, "the report names the ledger"
    r = _run(tmp_path, "def test_yes():\n    assert True\n")
    assert r.returncode == 0, r.stdout + r.stderr
    assert len((tmp_path / "failed.log").read_text().splitlines()) == 1, "a passing run appends nothing"


def test_the_seat_is_on_the_line(tmp_path):
    r = _run(tmp_path, "def test_no():\n    assert False\n", env={"TEND_SUITE_WHERE": "gate"})
    assert "  gate  " in (tmp_path / "failed.log").read_text()


def test_a_failure_seen_before_is_counted_in_the_report(tmp_path):
    r = _run(tmp_path, "def test_no():\n    assert False\n")
    assert "seen before" not in r.stdout, r.stdout
    r = _run(tmp_path, "def test_no():\n    assert False\n")
    assert "seen before" in r.stdout and "1 time" in r.stdout, r.stdout
    r = _run(tmp_path, "def test_no():\n    assert False\n")
    assert "2 times" in r.stdout, r.stdout


def test_the_shake_runs_one_test_many_times_under_load_and_counts(tmp_path):
    """A test that fails on every other run — the fixture has both sides —
    shakes to 2 of 4, each failure a `shake` line on the ledger."""
    body = ("import pathlib\n"
            "def test_flaky():\n"
            "    p = pathlib.Path('count'); n = int(p.read_text()) if p.exists() else 0\n"
            "    p.write_text(str(n + 1)); assert n % 2 == 0\n")
    r = _run(tmp_path, body, "--shake", "test/test_one.py::test_flaky", "4")
    assert r.returncode != 0
    assert "2 of 4" in r.stdout, r.stdout + r.stderr
    lines = (tmp_path / "failed.log").read_text().splitlines()
    assert len(lines) == 2 and all("  shake  " in l for l in lines), lines
    body = "def test_steady():\n    assert True\n"
    r = _run(tmp_path, body, "--shake", "test/test_one.py::test_steady", "2")
    assert r.returncode == 0 and "0 of 2" in r.stdout, r.stdout + r.stderr


# ── the gate's half, and the line that keeps the split honest ───────────
# Henri, 2026-09-01: the gate should be a quick consistency check and the
# program tests should live in the suite.  The whole suite was 297 s on
# every commit; GATE_TARGETS is 258 tests in 2.  What is given up is that
# a program broken by a commit is no longer caught by that commit, so the
# gate has to *say* what it did not run — otherwise this is a mechanism
# that quietly stopped checking, which is F008 all over again.

def _suite_module():
    import importlib.util
    spec = importlib.util.spec_from_file_location("suite", SUITE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_every_file_the_gate_names_is_there():
    """A gate target that has been renamed away would make the gate quietly
    smaller, and pytest exits 4 on a missing path rather than saying so in
    a way anybody reads."""
    suite = _suite_module()
    missing = [t for t in suite.GATE_TARGETS if not (ROOT / t).exists()]
    assert not missing, f"the gate names files that are not there: {missing}"
    assert suite.GATE_TARGETS, "the gate is not empty"


def test_the_gate_runs_no_program_tests():
    """The split's own definition, held: the files that start processes are
    the ones that cost the 297 seconds, and none of them belongs here."""
    suite = _suite_module()
    slow = {"test/test_launch.py", "test/test_mutate.py", "test/test_deliver.py",
            "test/test_lead.py", "test/test_suite.py", "test/test_install.py",
            "test/test_keep.py", "test/test_leash.py", "test/test_node.py"}
    assert not (set(suite.GATE_TARGETS) & slow), \
        "a program test crept into the gate — it belongs in the whole suite"


def test_the_gate_says_when_the_whole_suite_last_passed(tmp_path):
    """The honesty line.  Without it this change is a gate that stopped
    checking and said nothing."""
    suite = _suite_module()
    stamp = tmp_path / "suite-passed"
    os.environ["TEND_SUITE_PASSED"] = str(stamp)
    try:
        never = suite.full_pass_line()
        assert "never been recorded passing" in never, never
        assert "tools/suite.py" in never, "and it names the way to run them"
        stamp.write_text(f"{suite._git('rev-parse', 'HEAD')}\n2026-09-01 09:30\n")
        now = suite.full_pass_line()
        assert "at this commit" in now, now
        assert "2026-09-01 09:30" in now
    finally:
        del os.environ["TEND_SUITE_PASSED"]
