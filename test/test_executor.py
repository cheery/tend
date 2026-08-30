"""tools/executor.py — the two things a mind at the door may do, and the grant that bounds them.

card:tools.md, day one: `read` and `ls` over the tree's parts, run one
call a process under keep by tools/deliver.sh.  What is held here is
the executor's own shape — a manifest of one line per tool under a
kilobyte, named what the training data calls them — and the boundary
measured from outside: under the courier's keep flags a path outside
the parts is refused by the kernel, the refusal is the call's result,
and the executor bare serves the same path — the fence is the grant,
never the executor's care.
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXEC = ROOT / "tools" / "executor.py"
KEEP = ROOT / "tools" / "keep.py"
SANDBOX = ROOT / "tools" / "sandbox.sh"
DELIVER = ROOT / "tools" / "deliver.sh"


def parts():
    """The fence's own list, read the way the courier reads it."""
    return re.search(r'^tree_parts="(.*)"$', SANDBOX.read_text(), re.M).group(1).split()


def a_tree(tmp_path):
    t = tmp_path / "tree"
    (t / "board").mkdir(parents=True)
    (t / "board" / "README.md").write_text("# the board\n")
    (t / "board" / "x.md").write_text("card x\n" * 3)
    (t / "tools").mkdir()
    (t / "llm").mkdir(); (t / "llm" / "grant").write_text("allow model\n")
    (t / ".git").mkdir(); (t / ".git" / "HEAD").write_text("ref: refs/heads/main\n")
    return t


def bare(*args, tree=None, **extra):
    env = {"PATH": "/usr/bin:/bin", **({"TEND_TREE": str(tree)} if tree else {}), **extra}
    return subprocess.run([sys.executable, "-B", str(EXEC), *args], capture_output=True, text=True, env=env)


def kept(*args, tree, **extra):
    """The call as the courier runs it: keep's flags built from tree_parts, no net, no write."""
    flags = ["--allow", str(ROOT / "tools")]   # the executor's own directory, as the courier grants it
    for p in parts():
        if (tree / p).exists():
            flags += ["--allow", str(tree / p)]
    flags += ["--no-net", "--write", "/dev/null"]
    env = {"PATH": "/usr/bin:/bin", "TEND_TREE": str(tree), **extra}
    return subprocess.run([sys.executable, str(KEEP), *flags, "--", "/usr/bin/python3", "-B", str(EXEC), *args],   # the courier's python: the venv is outside the grant
                          capture_output=True, text=True, env=env)


def said(r):
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout)


def test_it_compiles():
    assert subprocess.run([sys.executable, "-m", "py_compile", str(EXEC)]).returncode == 0


def test_the_manifest_is_one_line_per_tool_under_a_kilobyte_and_named_what_the_training_data_calls_them():
    """card:tools.md §"Short prompts": a name, one sentence, one parameter;
    the whole array under 1 KB — a cap is a gate, and the number is
    Henri's to move, in a commit that says why."""
    r = bare("--manifest")
    assert r.returncode == 0, r.stderr
    m = json.loads(r.stdout)
    assert [t["function"]["name"] for t in m] == ["read", "ls"], "pi's read, the shell's ls — never read_file/list_board"
    for t in m:
        assert "\n" not in t["function"]["description"] and len(t["function"]["description"]) < 120, "one line per tool"
        assert len(t["function"]["parameters"]["required"]) == 1
    assert len(r.stdout.strip().encode()) < 1024, f"the manifest is {len(r.stdout.encode())} bytes — the cap is 1 KB"
    assert [t["function"]["name"] for t in json.loads(bare("--manifest", "read").stdout)] == ["read"]
    r = bare("--manifest", "bash")
    assert r.returncode == 2 and "no tool named bash" in r.stderr


def test_read_and_ls_say_what_they_did_in_one_line(tmp_path):
    t = a_tree(tmp_path)
    r = said(bare("read", "board/x.md", tree=t))
    assert r == {"c": "read board/x.md → 21 chars", "result": "card x\n" * 3}
    r = said(bare("ls", "board/", tree=t))
    assert r == {"c": "ls board/ → 2 entries", "result": "README.md\nx.md"}
    assert "board/" in said(bare("ls", ".", tree=t))["result"].splitlines(), "a directory is shown with its slash"
    assert said(bare("read", "board/nothing.md", tree=t))["c"].endswith("→ not there")
    assert said(bare("read", "board", tree=t))["c"].endswith("→ a directory — ls it")
    assert said(bare("ls", "board/x.md", tree=t))["c"].endswith("→ not a directory — read it")
    r = said(bare("read", "board/x.md", tree=t, TEND_READCHARS="5"))
    assert r["c"] == "read board/x.md → 5 chars, cut" and r["result"] == "card \n[… cut at 5 chars]"
    r = bare("write", "board/x.md", tree=t)
    assert r.returncode == 2 and "read PATH" in r.stderr
    assert bare("read", tree=t).returncode == 2


def test_under_keep_a_path_outside_the_parts_is_refused_by_the_kernel_and_the_refusal_is_the_result(tmp_path):
    """The injection red, at the executor: a secret under the person's
    home, asked for by `~` and by its absolute path — refused by keep,
    the secret never on stdout — and the same path served by the
    executor bare, which is the measurement that the boundary is the
    grant and not the executor's own judgment of a path."""
    t = a_tree(tmp_path)
    home = tmp_path / "home"; (home / ".ssh").mkdir(parents=True)
    secret = home / ".ssh" / "id_rsa"; secret.write_text("SECRETKEY-0000\n"); secret.chmod(0o600)
    assert said(kept("read", "board/x.md", tree=t))["c"] == "read board/x.md → 21 chars", "inside the parts, served"
    assert said(kept("ls", "board/", tree=t))["result"] == "README.md\nx.md"
    for path in ("llm/grant", str(t / "llm" / "grant")):
        assert said(kept("read", path, tree=t))["c"] == f"read {path} → refused by keep"
    assert said(kept("ls", ".git", tree=t))["c"] == "ls .git → refused by keep"
    for path in ("~/.ssh/id_rsa", str(secret)):
        r = kept("read", path, tree=t, HOME=str(home))
        assert said(r) == {"c": f"read {path} → refused by keep", "result": "refused by keep"}
        assert "SECRETKEY" not in r.stdout + r.stderr
    # bare, the executor serves the same paths: the refusal above was keep's
    assert said(bare("read", "llm/grant", tree=t))["c"] == "read llm/grant → 12 chars"
    assert "SECRETKEY" in said(bare("read", "~/.ssh/id_rsa", tree=t, HOME=str(home)))["result"]


def test_the_courier_grants_the_fences_own_parts_and_never_a_write_or_the_net():
    """tools/deliver.sh builds each call's keep flags from tools/sandbox.sh's
    tree_parts literal — one list, the fence's — with --no-net and the
    write boundary on with nothing but /dev/null beneath it."""
    src = DELIVER.read_text()
    assert re.search(r"tree_parts=.*sandbox\.sh", src), "the parts are read from the fence's own file"
    assert '--allow $here' in src and '--no-net --write /dev/null' in src
    assert "board" in parts() and "tools" in parts() and ".git" not in parts()
