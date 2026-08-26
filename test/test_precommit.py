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


def test_the_hook_refuses_the_commit_the_suite_refuses(tmp_path):
    """What the hook does at a commit is `tools/suite.py` — the whole
    suite, because tend's whole suite is seconds.  When a slow test
    arrives, the split gestate made (`--gates` for the commit, the rest
    for the shift) arrives with it, and this test is what says so out
    loud.

    **Measured, not read.**  Until 2026-08-26 this asserted that the
    string `python3 tools/suite.py` was in the file — and
    `board/green.md`'s day-one measurement put `|| true` after it: the
    hook ran the suite, discarded the verdict, committed a because-less
    card, and this test was green.  So now the hook is installed in a
    scratch repository whose `tools/suite.py` is a stub that says no,
    and the commit has to be refused; then the stub says yes, and the
    commit has to land.  A gate is what stands between the two."""
    git, run = _scratch(tmp_path)
    stub = tmp_path / "tools" / "suite.py"
    verdict = tmp_path / "tools" / "verdict"
    stub.write_text("import pathlib, sys\n"
                    "sys.exit(int(pathlib.Path(__file__).with_name('verdict').read_text()))\n")
    verdict.write_text("1\n")
    assert subprocess.run(["sh", "tools/pre-commit.sh", "--install"], cwd=tmp_path,
                          capture_output=True).returncode == 0
    (tmp_path / "card.md").write_text("no because\n")
    git("add", "-A")
    r = git("commit", "-qm", "dud")
    assert r.returncode != 0, "the suite said no and the commit went through"
    assert "a gate failed" in r.stderr
    assert git("rev-parse", "--verify", "-q", "HEAD").returncode != 0, "nothing was committed"
    verdict.write_text("0\n")
    git("add", "-A")
    r = git("commit", "-qm", "fine")
    assert r.returncode == 0, r.stderr
    assert git("rev-parse", "--verify", "-q", "HEAD").returncode == 0


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


def _scratch(tmp_path):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / "tools").mkdir()
    (tmp_path / "tools" / "pre-commit.sh").write_text(HOOK.read_text(encoding="utf-8"))
    (tmp_path / "tools" / "pre-commit.sh").chmod(0o755)  # the shim execs it
    git = lambda *a: subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t",
                                     *a], cwd=tmp_path, capture_output=True, text=True)
    run = lambda: subprocess.run(["sh", "tools/pre-commit.sh"], cwd=tmp_path,
                                 capture_output=True, text=True)
    return git, run


def test_a_staged_file_deleted_from_the_tree_is_refused(tmp_path):
    """**The countermeasure for 2026-08-24's polluted commit.**  The dud
    card was staged, then deleted from the working tree; the gates
    checked the tree, the commit took the index.  Now the hook refuses
    the case before it runs anything."""
    git, run = _scratch(tmp_path)
    (tmp_path / "dud.md").write_text("no because\n")
    git("add", "dud.md")
    (tmp_path / "dud.md").unlink()
    r = run()
    assert r.returncode == 1
    assert "staged content differs" in r.stderr
    assert "dud.md" in r.stderr


def test_a_staged_file_edited_since_is_refused_too(tmp_path):
    """The other direction of the same gap: the tree passed with the
    edit, the commit would carry the version without it."""
    git, run = _scratch(tmp_path)
    (tmp_path / "card.md").write_text("first\n")
    git("add", "card.md")
    (tmp_path / "card.md").write_text("second\n")
    r = run()
    assert r.returncode == 1
    assert "card.md" in r.stderr


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
