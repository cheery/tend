"""`tools/pre-commit.sh` — the gates, at the commit that breaks them.

Borrowed from gestate's `test/test_precommit.py` on 2026-08-24
(`card:gates.md`), where the lesson was paid for twice: the audit there
scored "the gates" as backed while the hook could vanish unnoticed, and
a hook that is not checked by a test is a rule with no gate — the exact
wish `card:gates.md` was opened about.
"""

import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
HOOK = ROOT / "tools" / "pre-commit.sh"


def sh(*args, cwd=ROOT):
    return subprocess.run(["sh", str(HOOK), *args], cwd=cwd,
                          capture_output=True, text=True)


def test_the_hook_parses():
    assert subprocess.run(["sh", "-n", str(HOOK)]).returncode == 0


def test_the_hook_runs_the_suite_and_nothing_else():
    """What the hook does at a commit is `tools/suite.py` — the whole
    suite, because tend's whole suite is seconds.  When a slow test
    arrives, the split gestate made (`--gates` for the commit, the rest
    for the shift) arrives with it, and this assertion is what says so
    out loud."""
    text = HOOK.read_text(encoding="utf-8")
    assert "python3 tools/suite.py" in text


def test_the_hook_is_installed_in_this_clone():
    """Per clone, and deliberately: a copy of this tree that has not run
    `--install` has the gates only when somebody remembers, which is the
    state the hook was built to end.  So a fresh clone is red here until
    `tools/toolbox.sh` (or `tools/pre-commit.sh --install`) has run, and
    that is the finding, not a broken test."""
    r = sh("--check")
    assert r.returncode == 0, r.stdout + r.stderr


def test_an_unknown_argument_is_refused_out_loud():
    r = sh("--bogus")
    assert r.returncode == 2
    assert "unknown argument" in r.stderr


def test_install_check_uninstall_in_a_scratch_repository(tmp_path):
    """The three verbs, against a repository that is not this one."""
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / "tools").mkdir()
    copy = tmp_path / "tools" / "pre-commit.sh"
    copy.write_text(HOOK.read_text(encoding="utf-8"))
    run = lambda *a: subprocess.run(["sh", str(copy), *a], cwd=tmp_path,
                                    capture_output=True, text=True)
    assert run("--check").returncode == 1
    assert run("--install").returncode == 0
    assert run("--check").returncode == 0
    hook = tmp_path / ".git" / "hooks" / "pre-commit"
    assert "tend:tools/pre-commit.sh" in hook.read_text()
    assert run("--uninstall").returncode == 0
    assert not hook.exists()


def test_somebody_elses_hook_is_not_overwritten(tmp_path):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / "tools").mkdir()
    copy = tmp_path / "tools" / "pre-commit.sh"
    copy.write_text(HOOK.read_text(encoding="utf-8"))
    hook = tmp_path / ".git" / "hooks" / "pre-commit"
    hook.parent.mkdir(parents=True, exist_ok=True)
    hook.write_text("#!/bin/sh\necho theirs\n")
    r = subprocess.run(["sh", str(copy), "--install"], cwd=tmp_path,
                       capture_output=True, text=True)
    assert r.returncode == 3
    assert hook.read_text() == "#!/bin/sh\necho theirs\n"
