#: asked-by: Henri, 2026-08-27 — "create an install script that installs this to the machine and protects those files, rather than the files in this tree" (card:install.md)
"""test/test_install.py — the restraints installed to the machine, from HEAD, read back against HEAD.

What is held: the installed set is the protected set (less the per-node
wrapper) plus what those scripts exec on the person's side, and it is
*closed* — every sibling an installed script names is installed too;
what installs is HEAD and never the working tree; the record beside the
copies names the commit; `--check` is red on absence, on drift, and on a
hook line that still runs the tree's copy — and says which; installing
and `--hooks apply` are refused inside the fence; `--hooks apply`
rewrites every tree hook line to the installed copy with the tree named
by TEND_TREE, and keeps the reach bound.

No sudo here: the prefix is a temporary directory, the weaker kind the
script names as such.  The root-owned install at /usr/local/lib/tend is
the person's hand, and its `--check` is the measurement that this test
cannot take from inside (board/README.md, "proposed, not declared").
"""
import json
import os
import pathlib
import re
import shutil
import subprocess

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
INSTALL = ROOT / "tools" / "install.sh"


def run(*args, tree=ROOT, prefix=None, settings=None, fenced="1", **kw):
    env = dict(os.environ, TEND_FENCED=fenced)
    if fenced == "":
        env.pop("TEND_FENCED", None)
    if prefix:
        env["TEND_PREFIX"] = str(prefix)
    if settings:
        env["TEND_SETTINGS"] = str(settings)
    return subprocess.run(["sh", str(tree / "tools" / "install.sh"), *args],
                          env=env, capture_output=True, text=True, **kw)


@pytest.fixture
def tree(tmp_path):
    """A clone of this tree with the working tree's tools/ and test/ committed —
    so that HEAD there is what is on disk here, and an install stages it."""
    t = tmp_path / "tree"
    subprocess.run(["git", "clone", "-q", str(ROOT), str(t)], check=True)
    for d in ("tools", "test", "node", ".claude"):
        if (ROOT / d).is_dir():
            shutil.copytree(ROOT / d, t / d, dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns("__pycache__", "state"))
    # settings.json is enforcement and git is its canonical copy (tools/fence.sh):
    # the clone keeps HEAD's, not a hand-edit in progress here.
    (t / ".claude/settings.json").write_bytes(subprocess.run(
        ["git", "-C", str(ROOT), "show", "HEAD:.claude/settings.json"], capture_output=True, check=True).stdout)
    subprocess.run(["git", "-C", str(t), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(t), "-c", "user.email=t@t", "-c", "user.name=t",
                    "commit", "-q", "-m", "working tree", "--allow-empty"], check=True)
    return t


def test_it_parses():
    assert subprocess.run(["sh", "-n", str(INSTALL)]).returncode == 0


def test_the_set_is_the_protected_set_plus_the_persons_side():
    listed = run("--list").stdout.split()
    protected = subprocess.run(["sh", str(ROOT / "tools/sandbox.sh"), "--protected"],
                               capture_output=True, text=True).stdout.split()
    for p in protected:
        if p.startswith("node/"):
            assert p not in listed, "a per-node wrapper stays in the tree"
        else:
            assert p in listed, f"{p} is protected but not installed"
    for p in ("tools/leash.sh", "tools/keep.py"):
        assert p in listed, f"{p} runs on the person's side (the hook, the launcher) and must be installed"


def test_the_set_is_closed_under_what_its_scripts_call():
    listed = set(run("--list").stdout.split())
    sibling = re.compile(r'\$(?:here|root/tools|T/tools)/([A-Za-z0-9_.-]+\.(?:sh|py))')
    for f in listed:
        for m in sibling.finditer((ROOT / f).read_text()):
            assert f"tools/{m.group(1)}" in listed, f"{f} calls tools/{m.group(1)}, which is not installed"


def test_stage_is_head_and_the_record_names_the_commit(tree, tmp_path):
    d = tmp_path / "stage"
    r = run("--stage", str(d), tree=tree)
    assert r.returncode == 0, r.stderr
    head = subprocess.run(["git", "-C", str(tree), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    rec = (d / "installed").read_text()
    assert f"commit {head}" in rec and f"source {tree}" in rec
    for f in run("--list", tree=tree).stdout.split():
        assert (d / f).read_bytes() == (tree / f).read_bytes()
        assert f in rec


def test_what_installs_is_head_not_the_working_tree(tree, tmp_path):
    (tree / "tools/leash.sh").write_text("#!/bin/sh\nexec \"$@\"\n")  # an uncommitted weakening
    d = tmp_path / "stage"
    r = run("--stage", str(d), tree=tree)
    assert r.returncode == 0, r.stderr
    assert "uncommitted change" in r.stdout and "tools/leash.sh" in r.stdout
    assert (d / "tools/leash.sh").read_text() != (tree / "tools/leash.sh").read_text()
    assert (d / "tools/leash.sh").read_bytes() == (ROOT / "tools/leash.sh").read_bytes()


def test_install_is_refused_inside_the_fence(tree, tmp_path):
    r = run(tree=tree, prefix=tmp_path / "p", fenced="1")
    assert r.returncode == 2 and "person's hand" in r.stderr
    assert not (tmp_path / "p").exists()
    r = run("--hooks", "apply", tree=tree, fenced="1")
    assert r.returncode == 2 and "person's hand" in r.stderr


def test_install_then_check_reads_back_head_and_names_the_hooks(tree, tmp_path):
    p = tmp_path / "p"
    r = run(tree=tree, prefix=p, fenced="")
    assert r.returncode == 0, r.stderr
    assert (p / "installed").exists() and (p / "tools/sandbox.sh").exists()
    mode = (p / "tools/sandbox.sh").stat().st_mode & 0o777
    assert mode == 0o555, f"a user-owned script is 555 — readable and runnable by all, writable by none — not {oct(mode)}"
    assert (p / "installed").stat().st_mode & 0o777 == 0o444
    assert (p / "tools/keep.py").stat().st_mode & 0o777 == 0o444
    r = run("--check", tree=tree, prefix=p)
    assert r.returncode == 1, "the hooks still run the tree's copies, and that is red"
    assert "✓ tools/sandbox.sh — HEAD" in r.stdout
    assert "hook runs the TREE's tools/limit.sh" in r.stdout
    assert "weaker" in r.stdout, "a prefix under $HOME says it is the weaker one"


def test_check_is_red_on_a_copy_you_cannot_read(tree, tmp_path):
    """The first root install (2026-08-27 16:17) left 533/422 — the mode
    arithmetic done in decimal — and every hook died Permission denied,
    while --check itself fell over on sed.  Unreadable is a finding."""
    p = tmp_path / "p"
    assert run(tree=tree, prefix=p, fenced="").returncode == 0
    # root's 422/533 read as "other" is 0o022/0o033 for the owner running this
    (p / "installed").chmod(0o022)
    (p / "tools/kaizen.sh").chmod(0o033)
    r = run("--check", tree=tree, prefix=p)
    assert r.returncode == 1 and "sed:" not in r.stderr, r.stderr
    assert "installed is not readable by you" in r.stdout and "sudo tools/install.sh again" in r.stdout
    (p / "installed").chmod(0o444)
    r = run("--check", tree=tree, prefix=p)
    assert "✗ tools/kaizen.sh is not readable by you" in r.stdout and "Permission denied" in r.stdout


def test_check_is_red_on_drift_and_on_absence(tree, tmp_path):
    p = tmp_path / "p"
    assert run(tree=tree, prefix=p, fenced="").returncode == 0
    f = p / "tools/limit.sh"
    f.chmod(0o755)
    f.write_text(f.read_text() + "\n# drift\n")
    r = run("--check", tree=tree, prefix=p)
    assert "✗ tools/limit.sh differs from HEAD" in r.stdout
    f.unlink()
    r = run("--check", tree=tree, prefix=p)
    assert "✗ tools/limit.sh is not installed" in r.stdout
    r = run("--check", tree=tree, prefix=tmp_path / "nowhere")
    assert r.returncode == 1 and "nothing installed" in r.stdout


def test_hooks_apply_rewrites_every_tree_line_and_keeps_the_bound(tree, tmp_path):
    p = tmp_path / "p"
    s = tmp_path / "settings.json"
    shutil.copy(tree / ".claude/settings.json", s)
    printed = run("--hooks", tree=tree, prefix=p, settings=s).stdout
    assert f'TEND_TREE="$CLAUDE_PROJECT_DIR" {p}/tools/kaizen.sh --hook' in printed
    r = run("--hooks", "apply", tree=tree, prefix=p, settings=s, fenced="")
    assert r.returncode == 0, r.stderr
    cmds = [h["command"] for ev in json.loads(s.read_text())["hooks"].values() for g in ev for h in g["hooks"]]
    for c in cmds:
        assert f'TEND_TREE="$CLAUDE_PROJECT_DIR" {p}/tools/' in c, c
        assert "$CLAUDE_PROJECT_DIR\"/tools" not in c and "/home/" not in c.split("TEND_TREE")[0], c
    bound = [c for c in cmds if "fence-hook" in c][0]
    assert bound.startswith("TEND_REACH_ALLOW="), "the reach bound is the person's and survives the rewrite"
    assert (s.with_name("settings.json.before-install")).exists()
    r = run("--check", tree=tree, prefix=p, settings=s)
    assert "hook runs the installed tools/fence-hook.sh" in r.stdout
    # and the fence's own check still finds every hook, by the names it greps for
    r2 = run("--hooks", "apply", tree=tree, prefix=p, settings=s, fenced="")
    assert json.loads(s.read_text())["hooks"]["UserPromptSubmit"][0]["hooks"][0]["command"].count("TEND_TREE") == 1, "idempotent"


def test_an_unknown_argument_is_refused_out_loud():
    assert run("--frobnicate").returncode == 2
