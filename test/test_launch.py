"""`tools/launch.sh` — one launcher for any node; the grant is a file beside
the program (board/keep.md, board/resolver.md, 2026-08-26: what the second
program earns).

The node's grant is `node/run.sh`'s three flags as a file; the llm node's
is the day-one measurement (model, state, port).  Tests point the state
at a scratch directory with TEND_STATE_DIR and run as a person's shell
(TEND_FENCED unset) unless the test is about the fence.
"""

import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import time

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
LAUNCH = ROOT / "tools" / "launch.sh"


def launch(node, *args, state, idle="0.5", fenced=False, timeout=30, path=None):
    # the andon record is pointed at scratch too: a runner that dies writes
    # a line to it (the death notice), and a test never writes the person's;
    # and the canvas, so a test never reads the person's holds (card:hold.md)
    env = dict(os.environ, TEND_STATE_DIR=str(state), TEND_IDLE=idle,
               TEND_ANDON_STATE=str(pathlib.Path(state) / "andon"),
               TEND_CANVAS=str(pathlib.Path(state) / "canvas"))
    env.pop("TEND_FENCED", None)
    if fenced:
        env["TEND_FENCED"] = "1"
    if path:   # a directory first on PATH — a fixture's shim of a command the launcher calls (F000: `date`)
        env["PATH"] = f"{path}:{env.get('PATH', '/usr/bin:/bin')}"
    return subprocess.run(["sh", str(LAUNCH), str(node), *args], env=env,
                          capture_output=True, text=True, timeout=timeout)


def wait(pred, cap=6.0):
    t = time.monotonic()
    while time.monotonic() - t < cap:
        if pred():
            return True
        time.sleep(0.05)
    return pred()


def state_of(state):
    return json.loads((state / "node.state").read_text())


needs_syspy = pytest.mark.skipif(not os.path.exists("/usr/bin/python3"), reason="no system python3 for keep")


def test_it_parses():
    assert subprocess.run(["sh", "-n", str(LAUNCH)]).returncode == 0


def test_the_nodes_grant_is_the_launchers_three_flags(tmp_path):
    r = launch(ROOT / "node", "grant", state=tmp_path)
    assert r.returncode == 0, r.stderr
    keep = [l for l in r.stdout.splitlines() if l.startswith("keep ")][0]
    assert f"--write {tmp_path}" in keep and "--allow" in keep and "node.py" in keep and "--no-net" in keep, keep
    assert "pull " + str(tmp_path / "node.state.pull") in r.stdout


def test_a_node_without_a_grant_is_refused_out_loud(tmp_path):
    (tmp_path / "bare").mkdir()
    r = launch(tmp_path / "bare", "run", state=tmp_path / "st")
    assert r.returncode == 2 and "has no grant" in r.stderr


def test_an_unknown_word_in_a_grant_is_refused(tmp_path):
    (tmp_path / "odd").mkdir()
    (tmp_path / "odd" / "grant").write_text("allow .\nwidget 3\nprogram true\n")
    r = launch(tmp_path / "odd", "grant", state=tmp_path / "st")
    assert r.returncode == 2 and "unknown word" in r.stderr


@needs_syspy
def test_the_node_runs_under_its_grant_and_stops(tmp_path):
    st = tmp_path / "st"
    r = launch(ROOT / "node", "run", state=st, idle="0.4")
    assert r.returncode == 0, r.stderr
    assert state_of(st)["generations"] == 1
    assert (st / "stopped").exists() and (st / "log").exists()


@needs_syspy
def test_a_pull_from_a_persons_shell_starts_the_node_and_is_served(tmp_path):
    st = tmp_path / "st"
    r = launch(ROOT / "node", "pull", state=st, idle="0.6")
    assert r.returncode == 0 and "started node" in r.stderr, r.stderr
    assert wait(lambda: (st / "node.state").exists() and state_of(st)["pulls"] == 1)
    assert wait(lambda: (st / "stopped").exists(), cap=8), "the runner did not stop on idle"
    # the pull is older than the stop: nothing is owed
    assert (st / "node.state.pull").stat().st_mtime < (st / "stopped").stat().st_mtime


@needs_syspy
def test_a_pull_inside_the_fence_appends_and_starts_nothing(tmp_path):
    st = tmp_path / "st"
    r = launch(ROOT / "node", "pull", "hello", state=st, fenced=True)
    assert r.returncode == 0 and "resolver" in r.stderr, r.stderr
    assert (st / "node.state.pull").read_text().strip().endswith("hello")
    assert not (st / "node.state").exists(), "a runner opened inside the fence"


@needs_syspy
def test_run_is_refused_while_a_runner_holds_the_lock(tmp_path):
    st = tmp_path / "st"
    first = launch(ROOT / "node", "pull", state=st, idle="4.0")
    assert first.returncode == 0, first.stderr
    second = launch(ROOT / "node", "run", state=st)
    assert second.returncode == 75 and "already holds" in second.stderr, (second.returncode, second.stderr)


@needs_syspy
def test_status_uses_the_grants_own_status_line(tmp_path):
    st = tmp_path / "st"
    launch(ROOT / "node", "run", state=st, idle="0.3")
    r = launch(ROOT / "node", "status", state=st)
    assert r.returncode == 0, r.stderr
    assert "node: not running" in r.stdout and "node tally:" in r.stdout, r.stdout


# where the second node runs is what its own check says — on the work laptop, 2026-08-28,
# the binary was on PATH and the model present and llama-server could not load its oneAPI
# libraries; a guard that asked less than the check ran the node on a machine that could not
has_llm = subprocess.run(["sh", str(LAUNCH), str(ROOT / "llm"), "check"], capture_output=True).returncode == 0


@pytest.mark.skipif(not has_llm, reason="tools/launch.sh llm check says the second node cannot run here")
def test_the_llm_node_serves_a_request_and_is_stopped_on_idle_by_its_pulse(tmp_path):
    """The second node: a program that cannot stop itself, run under its
    grant (model, state, one port), answers over loopback, and is stopped
    by the launcher when its pulse — the server log — goes quiet."""
    import socket, urllib.request
    st = tmp_path / "st"
    env = dict(os.environ, TEND_STATE_DIR=str(st), TEND_IDLE="3"); env.pop("TEND_FENCED", None)
    p = subprocess.Popen(["sh", str(LAUNCH), str(ROOT / "llm"), "run"], env=env,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        def up():
            try:
                s = socket.create_connection(("127.0.0.1", 18080), timeout=0.3); s.close(); return True
            except OSError:
                return False
        def ready():  # the port answers before the model is loaded (503); /health says when it is
            try:
                return urllib.request.urlopen("http://127.0.0.1:18080/health", timeout=1).status == 200
            except Exception:
                return False
        assert wait(ready, cap=30), "the server did not become ready"
        req = urllib.request.Request("http://127.0.0.1:18080/v1/chat/completions",
                                     data=json.dumps({"messages": [{"role": "user", "content": "Say yes."}],
                                                      "max_tokens": 4, "temperature": 0}).encode(),
                                     headers={"Content-Type": "application/json"})
        r = json.load(urllib.request.urlopen(req, timeout=60))
        assert r["choices"][0]["message"]["content"]
        assert wait(lambda: (st / "stopped").exists(), cap=20), "the launcher did not stop it on idle"
        p.wait(timeout=10)
    finally:
        if p.poll() is None:
            p.kill()
    assert "stopping it" in (st / "log").read_text()
    assert not up(), "the port is still bound"


@needs_syspy
def test_serve_starts_a_runner_for_an_unserved_pull_and_is_silent_when_served(tmp_path):
    """`serve` is the resolver's per-node decision, program-agnostic: a
    pull newer than the last stop with no runner up starts one; once it
    has run and stopped, a second serve with no new pull is silent."""
    st = tmp_path / "st"; st.mkdir()
    (st / "node.state.pull").write_text(f"{int(time.time())}\n")
    a = launch(ROOT / "node", "serve", state=st, idle="0.5")
    assert a.returncode == 0 and "started one" in a.stderr, a.stderr
    assert wait(lambda: (st / "node.state").exists() and state_of(st)["pulls"] == 1)
    assert wait(lambda: (st / "stopped").exists(), cap=8)
    b = launch(ROOT / "node", "serve", state=st)
    assert b.returncode == 0 and b.stderr == "", b.stderr


def test_serve_is_silent_with_no_pull_at_all(tmp_path):
    st = tmp_path / "st"; st.mkdir()
    r = launch(ROOT / "node", "serve", state=st)
    assert r.returncode == 0 and r.stderr == "", r.stderr
    assert not (st / "node.state").exists()


# ── the sitting: the first cord on a node (board/session-program.md, 2026-08-27) ──

def sitting_line(grant_output):
    return [l for l in grant_output.splitlines() if l.startswith("sitting ")]


def sitting_node(tmp_path, grant):
    node = tmp_path / "busy"; node.mkdir()
    (node / "grant").write_text(grant)
    return node


def test_a_node_without_a_sitting_line_is_a_program_and_the_llm_node_carries_one(tmp_path):
    """The cord is a line in the grant beside the program: absent, the
    node is a program (the tally node); present, the runner has a sitting
    (the llm node, tend's first session-program)."""
    node = launch(ROOT / "node", "grant", state=tmp_path / "a")
    assert node.returncode == 0 and not sitting_line(node.stdout), node.stdout
    llm = launch(ROOT / "llm", "grant", state=tmp_path / "b")
    assert llm.returncode == 0 and "sitting 10 min" in llm.stdout, llm.stdout


def test_a_sitting_that_is_not_minutes_is_refused(tmp_path):
    node = sitting_node(tmp_path, "sitting soon\nprogram /bin/true\n")
    r = launch(node, "grant", state=tmp_path / "st")
    assert r.returncode == 2 and "sitting wants minutes" in r.stderr, (r.returncode, r.stderr)


@needs_syspy
def test_the_sitting_stops_a_program_that_would_run_on(tmp_path):
    """A program with no pulse and no idle of its own — it would sleep for
    a minute — is stopped when its sitting is up, as a close: exit 0, the
    reason in `stopped` and the log."""
    node = sitting_node(tmp_path, "sitting 1\nprogram /bin/sleep 60\n")
    st = tmp_path / "st"
    env = dict(os.environ, TEND_STATE_DIR=str(st), TEND_SITTING="0.05"); env.pop("TEND_FENCED", None)
    t = time.monotonic()
    r = subprocess.run(["sh", str(LAUNCH), str(node), "run"], env=env, capture_output=True, text=True, timeout=30)
    assert r.returncode == 0, (r.returncode, r.stderr)
    assert time.monotonic() - t < 15, "the sitting did not end it"
    assert (st / "stopped").read_text().startswith("sitting:"), (st / "stopped").read_text()
    assert "minutes of busy are up" in (st / "log").read_text()
    s = launch(node, "status", state=st)
    assert "last stop:" in s.stdout and "sitting:" in s.stdout, s.stdout


@needs_syspy
def test_a_pull_cannot_declare_a_sitting(tmp_path):
    """The direction the hosted limit holds (test_limit.py): a session may
    end a sitting and never extend one.  A pull is the one thing a
    session writes, and its text is never read as a grant."""
    st = tmp_path / "st"
    r = launch(ROOT / "node", "pull", "sitting", "900", state=st, fenced=True)
    assert r.returncode == 0, r.stderr
    assert (st / "node.state.pull").read_text().strip().endswith("sitting 900")
    g = launch(ROOT / "node", "grant", state=st)
    assert not sitting_line(g.stdout), g.stdout


@pytest.mark.skipif(not has_llm, reason="tools/launch.sh llm check says the second node cannot run here")
def test_the_llm_nodes_sitting_ends_while_it_is_still_being_asked(tmp_path):
    """The cord on the llm node, shown to hold: the server is loaded, is
    asked something — so its pulse is fresh and idle (60 s) is nowhere
    near — and is stopped anyway when the sitting is up, the port freed."""
    import socket, urllib.request
    st = tmp_path / "st"
    env = dict(os.environ, TEND_STATE_DIR=str(st), TEND_IDLE="60", TEND_SITTING="0.1"); env.pop("TEND_FENCED", None)
    p = subprocess.Popen(["sh", str(LAUNCH), str(ROOT / "llm"), "run"], env=env,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        def ready():
            try:
                return urllib.request.urlopen("http://127.0.0.1:18080/health", timeout=1).status == 200
            except Exception:
                return False
        assert wait(ready, cap=30), "the server did not become ready"
        req = urllib.request.Request("http://127.0.0.1:18080/v1/chat/completions",
                                     data=json.dumps({"messages": [{"role": "user", "content": "Say yes."}],
                                                      "max_tokens": 4, "temperature": 0}).encode(),
                                     headers={"Content-Type": "application/json"})
        assert json.load(urllib.request.urlopen(req, timeout=60))["choices"][0]["message"]["content"]
        assert wait(lambda: (st / "stopped").exists(), cap=15), "the sitting did not stop it"
        p.wait(timeout=10)
    finally:
        if p.poll() is None:
            p.kill()
    assert p.returncode == 0
    assert (st / "stopped").read_text().startswith("sitting:")
    assert "minutes of llm are up" in (st / "log").read_text()
    try:
        socket.create_connection(("127.0.0.1", 18080), timeout=0.3).close()
        assert False, "the port is still bound"
    except OSError:
        pass


# ── check: an install test that runs nothing (card:node-install.md) ──────

def test_check_says_the_first_node_is_installed_and_runs_nothing(tmp_path):
    r = launch(ROOT / "node", "check", state=tmp_path / "st")
    assert r.returncode == 0, r.stdout + r.stderr
    assert "✓ program /usr/bin/python3" in r.stdout or "✓ program" in r.stdout
    assert "✓ allow " in r.stdout and "installed: node can run" in r.stdout, r.stdout
    assert not (tmp_path / "st" / "log").exists() and not (tmp_path / "st" / "stopped").exists(), "nothing ran"


def test_check_is_red_on_a_missing_program_and_a_missing_path_and_says_which(tmp_path):
    n = tmp_path / "n"; n.mkdir()
    (n / "grant").write_text("allow data.txt\nprogram no-such-binary-xyz $NODE/data.txt\n")
    r = launch(n, "check", state=tmp_path / "st")
    assert r.returncode == 1, r.stdout
    assert "✗ program `no-such-binary-xyz` is not on PATH" in r.stdout, r.stdout
    assert f"✗ allow {n}/data.txt does not exist" in r.stdout, r.stdout
    assert "NOT installed" in r.stdout
    (n / "data.txt").write_text("x")
    (n / "grant").write_text("allow data.txt\nprogram cat $NODE/data.txt\n")
    r = launch(n, "check", state=tmp_path / "st")
    assert r.returncode == 0 and "✓ program cat" in r.stdout and f"✓ allow {n}/data.txt" in r.stdout, r.stdout


def test_check_wants_the_model_the_person_brings_when_the_program_line_uses_it(tmp_path):
    n = tmp_path / "m"; n.mkdir()
    (n / "grant").write_text("allow model\nprogram cat $MODEL\n")
    r = launch(n, "check", state=tmp_path / "st")
    assert r.returncode == 1 and "no *.gguf under" in r.stdout and "the person brings" in r.stdout, r.stdout
    (n / "model").mkdir(); (n / "model" / "tiny.gguf").write_bytes(b"GGUF")
    r = launch(n, "check", state=tmp_path / "st")
    assert r.returncode == 0 and f"✓ model {n}/model/tiny.gguf" in r.stdout, r.stdout


def test_check_says_whether_the_bound_port_is_free_and_whose_it_is(tmp_path):
    import socket
    n = tmp_path / "p"; n.mkdir()
    s = socket.socket(); s.bind(("127.0.0.1", 0)); port = s.getsockname()[1]
    (n / "grant").write_text(f"bind {port}\nprogram true\n")
    r = launch(n, "check", state=tmp_path / "st")
    assert r.returncode == 1 and f"✗ bind {port} is in use" in r.stdout, r.stdout
    s.close()
    r = launch(n, "check", state=tmp_path / "st")
    assert r.returncode == 0 and f"✓ bind {port} is free" in r.stdout, r.stdout
    assert "✓ keep confines with this grant here" in r.stdout, "keep itself, with the grant, is the last line"


def test_check_inside_the_fence_reads_and_runs_nothing(tmp_path):
    r = launch(ROOT / "node", "check", state=tmp_path / "st", fenced=True)
    assert r.returncode == 0 and "installed:" in r.stdout, r.stdout + r.stderr


def test_check_knows_a_read_only_state_is_the_fence_inside_and_a_fault_outside(tmp_path):
    """The check's first run on the real nodes (2026-08-28) said ✗ on the
    state directory from inside the fence — where it is read-only to a
    session by design, and the runner writes it from the person's side."""
    st = tmp_path / "st"; st.mkdir(); st.chmod(0o555)
    try:
        r = launch(ROOT / "node", "check", state=st, fenced=True)
        assert r.returncode == 0 and "read-only to a session (the fence)" in r.stdout and "✗" not in r.stdout, r.stdout
        r = launch(ROOT / "node", "check", state=st, fenced=False)
        assert r.returncode == 1 and f"✗ state {st} is not writable by you" in r.stdout, r.stdout
    finally:
        st.chmod(0o755)


def test_check_is_red_on_a_program_whose_shared_library_is_not_found(tmp_path):
    """The work laptop, 2026-08-28: `check` said ✓ on a llama-server the
    loader could not start — an Intel-LLVM build wanting libsvml.so from a
    oneAPI the fence cannot see.  Present is not loadable; `ldd` reads a
    binary's needs against the loader's view without running any of it."""
    cc = shutil.which("cc")
    if not cc:
        pytest.skip("no C compiler here — the fixture builds a binary that needs a library")
    d = tmp_path / "b"; d.mkdir()
    (d / "nope.c").write_text("int nope(void) { return 0; }\n")
    (d / "main.c").write_text("int nope(void); int main(void) { return nope(); }\n")
    subprocess.run([cc, "-shared", "-fPIC", "-o", str(d / "libnope.so"), str(d / "nope.c")], check=True)
    subprocess.run([cc, "-o", str(d / "prog"), str(d / "main.c"), "-L", str(d), "-lnope", f"-Wl,-rpath,{d}"], check=True)
    n = tmp_path / "n"; n.mkdir()
    # found by the loader, and outside keep's SYSTEM_READ with no allow: keep would refuse it
    (n / "grant").write_text(f"program {d}/prog\n")
    r = launch(n, "check", state=tmp_path / "st")
    assert r.returncode == 1 and "keep would refuse it" in r.stdout and f"under: {d} " in r.stdout, r.stdout
    (n / "grant").write_text(f"allow {d}\nprogram {d}/prog\n")
    r = launch(n, "check", state=tmp_path / "st")
    assert r.returncode == 0 and f"✓ program {d}/prog" in r.stdout and "loads" in r.stdout, r.stdout
    (n / "grant").write_text(f"allow-try {d}\nprogram {d}/prog\n")   # present, allow-try reads like allow
    r = launch(n, "check", state=tmp_path / "st")
    assert r.returncode == 0 and "where keep lets it read" in r.stdout, r.stdout
    (d / "libnope.so").unlink()
    r = launch(n, "check", state=tmp_path / "st")
    assert r.returncode == 1 and "✗ program" in r.stdout and "cannot load" in r.stdout and "libnope.so" in r.stdout, r.stdout
    assert "NOT installed" in r.stdout


def test_check_resolves_the_program_as_keep_would_and_says_when_keep_would_skip_it(tmp_path):
    """F018, the work laptop, 2026-09-03: a wrapper at ~/.local/bin/llama-server
    ran from Henri's shell, and `check` said ✓ program → that path; under keep
    execvp got EACCES there (the home is outside SYSTEM_READ), walked on to
    /usr/local/bin/llama-server and ran the bare binary, which died at its
    loader.  The check resolved PATH from the shell's seat and not keep's, and
    a script has no ldd line to catch it.  Now the check walks PATH as keep
    would — an entry keep cannot read is skipped, not refused — and says so."""
    name = "tend-f018-prog"
    home = tmp_path / "home" / "bin"; home.mkdir(parents=True)
    (home / name).write_text("#!/bin/sh\nexit 0\n"); (home / name).chmod(0o755)
    n = tmp_path / "n"; n.mkdir()
    (n / "grant").write_text(f"program {name}\n")
    # found by the shell, outside keep's read, and no other on PATH: keep would find nothing
    r = launch(n, "check", state=tmp_path / "st", path=str(home))
    assert r.returncode == 1 and f"✗ program {name} → {home / name} for you" in r.stdout, r.stdout
    assert "keep would find nothing" in r.stdout and "NOT installed" in r.stdout, r.stdout
    # a second copy where keep can read: keep would skip the first and run the second, and the check names it
    sys_ = tmp_path / "sys" / "bin"; sys_.mkdir(parents=True)
    shutil.copy(home / name, sys_ / name)
    (n / "grant").write_text(f"allow {sys_}\nprogram {name}\n")
    r = launch(n, "check", state=tmp_path / "st", path=f"{home}:{sys_}")
    assert r.returncode == 1 and "keep would skip it" in r.stdout and f"run {sys_ / name} instead" in r.stdout, r.stdout
    # the first copy readable too: the shell and keep agree, ✓
    (n / "grant").write_text(f"allow {home}\nprogram {name}\n")
    r = launch(n, "check", state=tmp_path / "st", path=f"{home}:{sys_}")
    assert r.returncode == 0 and f"✓ program {name} → {home / name}" in r.stdout, r.stdout
    # an absolute program outside keep's read is refused, not skipped — there is nothing to walk on to
    (n / "grant").write_text(f"program {home / name}\n")
    r = launch(n, "check", state=tmp_path / "st")
    assert r.returncode == 1 and f"✗ program {home / name} is there, and keep would refuse it" in r.stdout, r.stdout


def test_material_is_a_grant_word_that_reads_a_tree_file_and_names_it(tmp_path):
    """card:material.md day one: a node reads a tree file only through a grant
    word.  `material PATH` grants the read (keep --allow) and names the path in
    $TEND_MATERIAL, so the program knows what to put in front of the mind;
    absent, keep refuses the read.  One path per line, like allow, refused at
    parse when the file is not there.  Red first against a launcher with no
    such word — the read is denied and the word is unknown."""
    tree = tmp_path / "tree"; (tree / "board").mkdir(parents=True)
    doc = tree / "board" / "README.md"; doc.write_text("the board's rule\n")
    real = os.path.realpath(doc)
    n = tree / "node"; n.mkdir()
    prog = 'program /bin/sh -c "echo M=$TEND_MATERIAL; cat $TEND_MATERIAL 2>&1"'
    # absent file: refused at parse, like model
    (n / "grant").write_text(f"material ../board/nope.md\n{prog}\n")
    r = launch(n, "grant", state=tmp_path / "st")
    assert r.returncode == 2 and "material" in (r.stdout + r.stderr) and "is not there" in (r.stdout + r.stderr), r.stdout + r.stderr
    # the word present: grant emits --allow the resolved path, check lists it
    (n / "grant").write_text(f"material ../board/README.md\n{prog}\n")
    r = launch(n, "grant", state=tmp_path / "st")
    assert r.returncode == 0 and f"--allow {real}" in r.stdout, r.stdout
    r = launch(n, "check", state=tmp_path / "st")
    assert r.returncode == 0 and f"✓ material {real}" in r.stdout, r.stdout
    # run under keep: the program is handed the path and reads the file — the grant carried the read in
    r = launch(n, "run", state=tmp_path / "st")
    log = (tmp_path / "st" / "log").read_text()
    assert real in log and "the board's rule" in log, log
    # the control: no material word, the same read by literal path — keep refuses it (outside the grant)
    (n / "grant").write_text(f'program /bin/sh -c "cat {real} 2>&1; true"\n')
    r = launch(n, "run", state=tmp_path / "st2")
    log = (tmp_path / "st2" / "log").read_text()
    assert "the board's rule" not in log and "Permission denied" in log, log


def test_allow_try_is_a_grant_word_and_check_says_when_the_path_is_not_here(tmp_path):
    """A grant is tracked and a machine's runtime is not: `allow-try PATH`
    is readable where it exists and no refusal where it does not (the
    fence's `--ro-bind-try`, as a grant word — 2026-08-28)."""
    n = tmp_path / "n"; n.mkdir()
    (n / "grant").write_text(f"allow-try {tmp_path}/rt\nprogram true\n")
    r = launch(n, "grant", state=tmp_path / "st")
    assert r.returncode == 0 and f"--allow-try {tmp_path}/rt" in r.stdout, r.stdout + r.stderr
    r = launch(n, "check", state=tmp_path / "st")
    assert r.returncode == 0 and f"· allow-try {tmp_path}/rt is not here" in r.stdout and "installed:" in r.stdout, r.stdout + r.stderr
    (tmp_path / "rt").mkdir()
    r = launch(n, "check", state=tmp_path / "st")
    assert r.returncode == 0 and f"✓ allow-try {tmp_path}/rt" in r.stdout, r.stdout


def test_a_program_that_is_busy_and_silent_is_not_idle(tmp_path):
    """The work laptop, 2026-08-28, 07:50: llama-server loaded the model,
    then compiled its GPU kernels for 45 s with no log line — busy on a
    core, silent on its pulse — and the launcher stopped it for idleness
    mid-compile.  A pulse is one sign of activity; CPU progress is the
    other, and it needs no new word: a program burning a core is not idle.

    F001 (2026-08-30): under eight burners this loop gets ~28 ticks a
    second, and at `idle 2` the rule wants 50 in two ticks — a margin
    under one tick, so the fixture says `idle 4` now, as the burst one
    does; the other half of F001, the exit between two ticks, has its
    own gate below."""
    n = tmp_path / "n"; n.mkdir()
    (n / "grant").write_text("pulse beat\nidle 4\nprogram /usr/bin/python3 -c 'exec(\"import time\\nt=time.time()+8\\nwhile time.time()<t: pass\")'\n")
    st = tmp_path / "st"
    t0 = time.time()
    r = launch(n, "run", state=st, idle="4", timeout=60)
    took = time.time() - t0
    ticks = (st / "ticks").read_text() if (st / "ticks").exists() else "(no ticks file)"
    assert "idle" not in (st / "stopped").read_text(), (st / "stopped").read_text() + "ticks:\n" + ticks
    assert took > 6, f"it was stopped at idle, {took:.1f}s\nticks:\n{ticks}"
    (n / "grant").write_text("pulse beat\nidle 4\nprogram sleep 30\n")
    t0 = time.time()
    r = launch(n, "run", state=tmp_path / "st2", idle="4", timeout=60)
    assert "idle" in (tmp_path / "st2" / "stopped").read_text() and time.time() - t0 < 10, "silent and asleep is idle"


@needs_syspy
def test_a_program_that_exits_between_two_ticks_is_recorded_as_its_exit_and_not_as_idle(tmp_path):
    """F001 (2026-08-29, 8 of 10 under the shake; 5 of 10 after F000's
    clock fix; read from $STATE/ticks 2026-08-30 09:20: the CPU column
    *fell* on the last tick, to the window's base — the fallback).  A
    program that exits during the watch's `sleep 1` is reaped there; the
    next tick cannot read /proc/PID/stat, the fallback reads as no
    progress, and IDLE ticks after the last busy one the stop is written
    as `idle`, the exit code masked to 0 and the death notice — the line
    the panel reads — never written.  On the llm node that is a crash
    between two ticks shown as idle, with nothing on the person's side.

    The fixture exits 3 at 1.5 s with `idle 2`: alive at tick 1, gone at
    tick 2.  The old launcher says idle and exits 0; this one ends the
    watch on the unreadable stat and lets `wait` say `exited 3`."""
    n = tmp_path / "n"; n.mkdir()
    (n / "grant").write_text("pulse beat\nidle 2\nprogram /bin/sh -c 'sleep 1.5; echo \"prog: gave up\" >&2; exit 3'\n")
    st = tmp_path / "st"
    r = launch(n, "run", state=st, idle="2", timeout=60)
    stopped = (st / "stopped").read_text()
    ticks = (st / "ticks").read_text() if (st / "ticks").exists() else "(no ticks file)"
    assert stopped.startswith("exited 3"), stopped + "ticks:\n" + ticks
    assert r.returncode == 3, (r.returncode, r.stderr)
    record = st / "andon" / "andon.log"
    assert record.exists(), "no death notice for a program that died between two ticks"
    line = record.read_text().splitlines()[-1]
    assert "n: exited 3" in line and "gave up" in line, line


def test_env_is_a_grant_word_and_the_program_sees_it_with_state_expanded(tmp_path):
    """`env NAME=VALUE` — the work laptop, 2026-08-28: the llm node paid an
    81 s kernel compile on every start because the SYCL runtime's cache
    lives under ~/.cache, which keep does not grant; $STATE is writable
    already, so the runtime only needs telling.  The launcher exports the
    line before keep execs the program; $STATE, $NODE and $MODEL expand."""
    n = tmp_path / "n"; n.mkdir()
    (n / "grant").write_text("env CACHE_HOME=$STATE/cache\nprogram sh -c 'echo \"$CACHE_HOME\" > $STATE/seen'\n")
    st = tmp_path / "st"
    r = launch(n, "grant", state=st)
    assert r.returncode == 0 and "env CACHE_HOME=$STATE/cache" in r.stdout, r.stdout + r.stderr
    r = launch(n, "check", state=st)
    assert r.returncode == 0 and f"✓ env CACHE_HOME={st}/cache" in r.stdout, r.stdout + r.stderr
    r = launch(n, "run", state=st)
    assert (st / "seen").read_text().strip() == f"{st}/cache", (st / "log").read_text()


def test_make_is_a_grant_word_and_the_directory_exists_before_the_program_runs(tmp_path):
    """`make PATH` — the work laptop, 2026-08-28: the GPU driver's kernel
    cache cut the llm node's start from 82 s to 11 s by hand, and the
    driver does not create its directory; absent, it quietly caches
    nothing.  Under $STATE unless absolute; made before keep execs."""
    n = tmp_path / "n"; n.mkdir()
    (n / "grant").write_text("make neo-cache\nenv CACHE=$STATE/neo-cache\nprogram sh -c 'ls -d \"$CACHE\" > $STATE/seen'\n")
    st = tmp_path / "st"
    r = launch(n, "check", state=st)
    assert r.returncode == 0 and f"· make {st}/neo-cache is made by run" in r.stdout, r.stdout + r.stderr
    launch(n, "run", state=st)
    assert (st / "neo-cache").is_dir() and (st / "seen").read_text().strip() == f"{st}/neo-cache", (st / "log").read_text()


# --- the watcher heartbeat: the cords are checked by something (card:session-program.md §09:37) ---
#
# On the work laptop a runner wrapped in strace overran its sitting by 25
# minutes: the watch loop set the stop, `kill` could not end the tracer,
# and the shell hung at `wait` with the lock held while `status` read
# "running".  The runner now touches $STATE/watch every tick of its loop,
# and status/check/serve read a held lock with a silent watch as "the
# cords are cut" — serve, the resolver's side, kills it.  The fixture is
# a lock-holder with a stale heartbeat, not a real strace.

def _hung_runner(st):
    """A runner that holds the lock and whose watcher went silent three minutes ago."""
    st.mkdir(parents=True, exist_ok=True)
    p = subprocess.Popen(["sh", "-c", 'exec 9>>"$1"; flock 9; exec sleep 60', "_", str(st / "run.lock")])
    (st / "run.pid").write_text(f"{p.pid}\n")   # exec keeps the pid: the sleeper is the "program"
    assert wait(lambda: subprocess.run(["flock", "-n", str(st / "run.lock"), "true"]).returncode != 0), "the fixture holds the lock"
    old = time.time() - 180
    (st / "watch").touch(); os.utime(st / "watch", (old, old))
    return p


@needs_syspy
def test_a_watching_runner_leaves_a_fresh_heartbeat(tmp_path):
    node = sitting_node(tmp_path, "sitting 1\nprogram /bin/sleep 60\n")
    st = tmp_path / "st"
    env = dict(os.environ, TEND_STATE_DIR=str(st), TEND_SITTING="0.08"); env.pop("TEND_FENCED", None)
    p = subprocess.Popen(["sh", str(LAUNCH), str(node), "run"], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        assert wait(lambda: (st / "watch").exists()), "the watcher touches its heartbeat"
        assert time.time() - (st / "watch").stat().st_mtime < 5
        s = launch(node, "status", state=st)
        assert "running" in s.stdout and "cords are cut" not in s.stdout, s.stdout
    finally:
        p.wait(timeout=30)
    assert p.returncode == 0
    assert not (st / "watch").exists(), "a clean stop takes the heartbeat with it"


def test_a_held_lock_with_a_silent_watcher_is_read_as_the_cords_cut(tmp_path):
    node = sitting_node(tmp_path, "sitting 1\nprogram /bin/sleep 60\n")
    st = tmp_path / "st"
    p = _hung_runner(st)
    try:
        s = launch(node, "status", state=st)
        assert "cords are cut" in s.stdout and "3 min" in s.stdout, s.stdout
        c = launch(node, "check", state=st)
        assert "cords are cut" in c.stdout and c.returncode == 1, c.stdout
    finally:
        p.kill(); p.wait()


def test_serve_kills_a_runner_whose_cords_are_cut_and_frees_the_lock(tmp_path):
    node = sitting_node(tmp_path, "sitting 1\nprogram /bin/sleep 60\n")
    st = tmp_path / "st"
    p = _hung_runner(st)
    try:
        r = launch(node, "serve", state=st)
        assert "cords are cut" in r.stderr and "killed" in r.stderr, r.stderr
        assert wait(lambda: p.poll() is not None, cap=15), "the resolver ended it"
        assert subprocess.run(["flock", "-n", str(st / "run.lock"), "true"]).returncode == 0, "the lock is free"
        assert "cords are cut" in (st / "log").read_text()
    finally:
        if p.poll() is None:
            p.kill(); p.wait()


@needs_syspy
def test_a_program_that_ignores_term_does_not_hang_the_runner(tmp_path):
    """The failure itself, without strace: a program that shrugs off TERM.
    The runner escalates after a bounded wait and still closes as a
    sitting, exit 0 with the reason."""
    node = sitting_node(tmp_path, "sitting 1\nprogram /bin/sh -c 'trap \"\" TERM; sleep 60'\n")
    st = tmp_path / "st"
    env = dict(os.environ, TEND_STATE_DIR=str(st), TEND_SITTING="0.05", TEND_KILL_WAIT="2"); env.pop("TEND_FENCED", None)
    t = time.monotonic()
    r = subprocess.run(["sh", str(LAUNCH), str(node), "run"], env=env, capture_output=True, text=True, timeout=30)
    assert r.returncode == 0, (r.returncode, r.stderr)
    assert time.monotonic() - t < 20, "the runner hung on a program that ignored TERM"
    assert (st / "stopped").read_text().startswith("sitting:")
    assert "did not stop" in (st / "log").read_text()


DEATH = re.compile(r"^\d+ \d{4}-\d\d-\d\d \d\d:\d\d (\S+): exited (\d+)( — (.*))?$")


@needs_syspy
def test_a_runner_that_dies_writes_one_line_to_the_andon_record(tmp_path):
    """The death notice (card:canvas.md, day two — Opus 5's draft, 2026-08-28
    18:35, landed at Henri's "land it" 2026-08-29).  Henri, 2026-08-28
    13:27: `pull` said "started llm" and the runner had died a second
    later at the loader, with nothing on the person's side.  Now the
    runner's own stop path appends one line to the andon record — the
    file the panel reads, in the record's own shape — so the death and a
    cord pull land on one timeline, whether or not anyone was watching.
    The runner appends; `pull` no longer watches for a second (the window
    Henri named as one "we will eventually revert")."""
    node = tmp_path / "dead"; node.mkdir()
    (node / "grant").write_text("program /bin/sh -c 'echo \"prog: error while loading shared libraries: libx.so\" >&2; exit 127'\n")
    st = tmp_path / "st"
    r = launch(node, "pull", "hello", state=st)
    assert r.returncode == 0 and "started dead" in r.stderr, (r.returncode, r.stderr)
    record = st / "andon" / "andon.log"
    assert wait(lambda: record.exists()), "the runner's stop wrote no death notice"
    assert wait(lambda: (st / "stopped").exists())
    lines = record.read_text().splitlines()
    assert len(lines) == 1, lines
    m = DEATH.match(lines[0])
    assert m, lines[0]
    assert m.group(1) == "dead" and m.group(2) == "127", lines[0]
    assert "libx.so" in m.group(4), "the reason is what the program last said"


@needs_syspy
def test_a_clean_stop_writes_no_death_notice(tmp_path):
    """A zero exit writes nothing, and the launcher's own stops — idle, the
    sitting — are closes (rc 0): the record is for deaths that were not
    asked for; a clean stop is already in `stopped` for the row."""
    st = tmp_path / "st"
    r = launch(ROOT / "node", "run", state=st, idle="0.4")
    assert r.returncode == 0, r.stderr
    assert (st / "stopped").exists()
    assert not (st / "andon" / "andon.log").exists()
    node = tmp_path / "quiet"; node.mkdir()
    (node / "grant").write_text("program /bin/sh -c 'exit 0'\n")
    st2 = tmp_path / "st2"
    r = launch(node, "run", state=st2)
    assert r.returncode == 0 and not (st2 / "andon" / "andon.log").exists()


# ── the hold: the canvas's standing pull (card:hold.md, 2026-08-29) ──
#
# A pull is a line that means "something wants this once"; the llm node
# idled out 60 s after each of lead.sh's turns and paid 80 s reloading
# on the next.  `<name>.hold` in the canvas directory is the person's
# "keep this alive": presence is the pull, mtime is the person saying
# so again, rm lets the node stop.  Every fixture here builds its own
# canvas under the scratch state (the launch helper's TEND_CANVAS).

def hold(state, name, text="held by the fixture\n", at=None):
    canvas = pathlib.Path(state) / "canvas"; canvas.mkdir(parents=True, exist_ok=True)
    h = canvas / f"{name}.hold"; h.write_text(text)
    if at is not None:
        os.utime(h, (at, at))
    return h


@needs_syspy
def test_a_held_program_is_not_idle_while_the_hold_stands_and_stops_a_tick_after_it_goes(tmp_path):
    """Rule 2: the runner knows it is pulled.  A program whose pulse never
    moves would be stopped for idleness in 0.4 s; held, it is still up
    two seconds later; the hold removed, it stops within a tick, as idle
    — a close, exit 0 — and never as a sitting extension."""
    node = sitting_node(tmp_path, "pulse log\nprogram /bin/sleep 60\n")
    st = tmp_path / "st"; st.mkdir()
    h = hold(st, "busy")
    env = dict(os.environ, TEND_STATE_DIR=str(st), TEND_IDLE="0.4", TEND_CANVAS=str(st / "canvas"),
               TEND_ANDON_STATE=str(st / "andon")); env.pop("TEND_FENCED", None)
    p = subprocess.Popen(["sh", str(LAUNCH), str(node), "run"], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        assert wait(lambda: (st / "watch").exists(), cap=8), "the runner never started watching"
        time.sleep(2.5)
        assert p.poll() is None and not (st / "stopped").exists(), "a held program idled out"
        h.unlink()
        assert wait(lambda: (st / "stopped").exists(), cap=4), "the hold removed, it did not stop"
        assert (st / "stopped").read_text().startswith("idle:"), (st / "stopped").read_text()
        assert p.wait(timeout=15) == 0
    finally:
        if p.poll() is None:
            p.kill(); p.wait()


@needs_syspy
def test_serve_starts_a_held_node_with_no_pull_at_all_and_again_after_a_clean_stop(tmp_path):
    """A hold is a standing pull: `serve` starts a runner for a held node
    with no pull file and none up, and — the node having stopped by
    itself, clean — starts it again on the next visit, unconditionally."""
    st = tmp_path / "st"; st.mkdir()
    hold(st, "node")
    a = launch(ROOT / "node", "serve", state=st, idle="0.4")
    assert a.returncode == 0 and "is held and no runner" in a.stderr, (a.returncode, a.stderr)
    assert wait(lambda: (st / "stopped").exists(), cap=8), "the held node never ran and stopped"
    first = (st / "stopped").stat().st_mtime_ns
    b = launch(ROOT / "node", "serve", state=st, idle="0.4")
    assert b.returncode == 0 and "is held and no runner" in b.stderr, (b.returncode, b.stderr)
    assert wait(lambda: (st / "stopped").exists() and (st / "stopped").stat().st_mtime_ns > first, cap=8), \
        "a clean stop under a hold was not restarted"


@needs_syspy
def test_a_held_death_is_restarted_only_by_a_hold_newer_than_it(tmp_path):
    """Rule 3: a crash is not hammered.  The runner died (a non-zero exit
    in `stopped`) after the hold was written: `serve` starts nothing.
    The person touches the hold, having seen why: `serve` starts one."""
    st = tmp_path / "st"; st.mkdir()
    death = int(time.time()) - 60
    (st / "stopped").write_text("exited 127: node stopped by itself\n")
    os.utime(st / "stopped", (death, death))
    h = hold(st, "node", at=death - 30)
    a = launch(ROOT / "node", "serve", state=st)
    assert a.returncode == 0 and a.stderr == "", (a.returncode, a.stderr)
    time.sleep(0.3)
    assert (st / "stopped").read_text().startswith("exited 127"), "a death older than its hold was restarted"
    assert subprocess.run(["flock", "-n", str(st / "run.lock"), "true"]).returncode == 0
    os.utime(h, (death + 30, death + 30))
    b = launch(ROOT / "node", "serve", state=st, idle="0.4")
    assert b.returncode == 0 and "the hold is newer than its death" in b.stderr, (b.returncode, b.stderr)
    assert wait(lambda: (st / "stopped").exists() and not (st / "stopped").read_text().startswith("exited 127"), cap=8), \
        "the hold re-asserted, the node was not restarted"


def test_status_and_check_say_held(tmp_path):
    st = tmp_path / "st"; st.mkdir()
    hold(st, "node", "held by henri, the desk\n")
    s = launch(ROOT / "node", "status", state=st)
    assert "held: held by henri, the desk" in s.stdout, s.stdout
    c = launch(ROOT / "node", "check", state=st)
    assert "held — " in c.stdout and "held by henri" in c.stdout, c.stdout


def test_a_hold_names_its_node_inside_the_file_and_the_filename_is_a_label(tmp_path):
    """Henri, 2026-08-29: "I'd like to name what I'm holding inside the
    file".  A hold is pin-shaped: `node NAME`, `state DIR`, and the words;
    a hold that names another node, or this node with another state, is
    not this node's; and one with no node line holds the node its
    filename names, so `node.hold` still works."""
    st = tmp_path / "st"; st.mkdir()
    hold(st, "some-node", "node node\nheld by henri, for the afternoon\n")
    hold(st, "other", "node llm\nheld by henri\n")
    hold(st, "elsewhere", f"node node\nstate {tmp_path}/not-this-state\nheld by a fixture\n")
    s = launch(ROOT / "node", "status", state=st)
    assert s.stdout.count("held:") == 1 and "held: held by henri, for the afternoon (" in s.stdout, s.stdout
    hold(st, "here", f"node node\nstate {st}\nthis state exactly\n")
    hold(st, "node", "no node line: the filename names it\n")
    s = launch(ROOT / "node", "status", state=st)
    assert s.stdout.count("held:") == 3, s.stdout
    assert "held: this state exactly (" in s.stdout and "held: no node line: the filename names it (" in s.stdout, s.stdout


def test_a_bare_path_line_in_a_hold_is_its_state(tmp_path):
    """Henri, 2026-08-29: "newline and state dumped there".  A line that
    reads as a path is the state, no key needed; it is matched against
    the state the launcher runs with, and the words are the other lines."""
    st = tmp_path / "st"; st.mkdir()
    hold(st, "here", f"node node\n{st}\nthis state, on its own line\n")
    hold(st, "there", f"node node\n{tmp_path}/elsewhere\nanother state\n")
    s = launch(ROOT / "node", "status", state=st)
    assert s.stdout.count("held:") == 1 and "held: this state, on its own line (" in s.stdout, s.stdout


def test_a_program_busy_in_bursts_is_busy_over_the_idle_window(tmp_path):
    """card:flake.md, the first shake (2026-08-29, 8 of 10 under load): the
    busy rule read half a core *per second*, and a program that gets less
    than that for two seconds running — contention, or honest bursts —
    was stopped as idle.  Busy-ness is now half a core-second summed over
    the idle window: 0.3 s of burning per second is 30 % of a core, under
    the old rule idle within any window, under this one 60 ticks in two
    seconds — busy.  Silent on its pulse throughout.

    F000 (2026-08-30): this fixture burned 0.3 s of *wall* time a cycle and
    ran at `idle 2` — under eight burners it got 10 ticks a second, which
    the rule rightly reads as idle, and at no load a tick of the launcher's
    integer clock was half its window (the clock is F000's own, gated by
    the test below).  It now burns 0.3 s of CPU a cycle, so its 30 % is 30 %
    on any box, and says `idle 4`, so no tick is half the window."""
    n = tmp_path / "n"; n.mkdir()
    prog = ("exec(\"import time\\nend=time.time()+9\\nwhile time.time()<end:\\n"
            "  t=time.process_time()+0.3\\n  while time.process_time()<t: pass\\n  time.sleep(0.7)\")")
    (n / "grant").write_text(f"pulse beat\nidle 4\nprogram /usr/bin/python3 -c '{prog}'\n")
    st = tmp_path / "st"
    t0 = time.time()
    r = launch(n, "run", state=st, idle="4", timeout=60)
    took = time.time() - t0
    ticks = (st / "ticks").read_text() if (st / "ticks").exists() else "(no ticks file)"
    assert "idle" not in (st / "stopped").read_text(), (st / "stopped").read_text() + "ticks:\n" + ticks
    assert took > 7, f"it was stopped at idle, {took:.1f}s\nticks:\n{ticks}"


def test_the_idle_window_is_counted_in_ticks_of_the_watch_not_on_a_clock_that_can_skip(tmp_path):
    """F000 (2026-08-29 20:40, 20:48; 2026-08-30 07:29 — three gate runs
    refused on unrelated commits; 3 of 20 by hand at no load).  The busy
    rule's window was measured on `date +%s`, which truncates: a tick that
    straddles two second boundaries reads as two, and at `idle 2` that is
    half the window gone — a program found busy on one tick was stopped as
    idle on the next.  The window is now counted in ticks of the watch
    loop, each a `sleep 1` or longer, so it is never shorter than declared.

    The fixture builds the defect's side deterministically: a `date` on
    PATH that skips 3 s on every read.  The program sleeps a second, then
    burns; on the old rule the first tick reads as 3 s of silence and it
    is stopped before it has burned at all; on this one the third tick
    finds ~2 s of burning.  Load-proof: by tick 3 a full burn has at least
    half a core-second at a quarter of a core."""
    n = tmp_path / "n"; n.mkdir(); shim = tmp_path / "bin"; shim.mkdir()
    (shim / "date").write_text(
        "#!/bin/sh\n# a clock that skips: every read 3 s past the last, whatever the wall says (F000)\n"
        f"c={shim}/count; n=$(cat \"$c\" 2>/dev/null || echo 0); n=$((n + 1)); echo \"$n\" > \"$c\"\n"
        "case \"$1\" in +%s) echo $(( $(/bin/date +%s) + 3 * n )) ;; *) exec /bin/date \"$@\" ;; esac\n")
    (shim / "date").chmod(0o755)
    prog = "exec(\"import time\\ntime.sleep(1)\\ne=time.time()+5\\nwhile time.time()<e: pass\")"
    (n / "grant").write_text(f"pulse beat\nidle 3\nprogram /usr/bin/python3 -c '{prog}'\n")
    st = tmp_path / "st"
    t0 = time.time()
    launch(n, "run", state=st, idle="3", timeout=60, path=shim)
    took = time.time() - t0
    ticks = (st / "ticks").read_text()
    assert "idle" not in (st / "stopped").read_text(), (st / "stopped").read_text() + "ticks:\n" + ticks
    assert took > 4, f"stopped at {took:.1f}s\nticks:\n{ticks}"
    # the instrument: one line a tick, and the last column is the window in ticks — never past the grant's
    rows = [l.split() for l in ticks.splitlines()]
    assert len(rows) >= 4 and all(len(r) == 7 for r in rows), ticks
    assert max(int(r[6]) for r in rows) <= 3, ticks   # read before the tick's own update: it reaches IDLE on the tick that resets it


def test_the_grant_names_its_model_and_check_is_red_when_the_file_is_not_there(tmp_path):
    """Henri, 2026-08-30: "I'd want the bigger mind."  Until the `model`
    word, $MODEL was the first *.gguf by name — and the mind that answered
    a morning's talk was the 1B model that sorted first.  Named in the
    grant, the pick is written; absent, the first by name, as before;
    named and not there, `check` says so."""
    n = tmp_path / "n"; (n / "model").mkdir(parents=True)
    (n / "model" / "a-small.gguf").write_text(""); (n / "model" / "b-big.gguf").write_text("")
    (n / "grant").write_text("allow model\nprogram cat $MODEL\n")
    r = launch(n, "check", state=tmp_path / "st")   # `check` says which file $MODEL is; `grant` prints the line unexpanded
    assert r.returncode == 0 and f"✓ model {n}/model/a-small.gguf" in r.stdout, r.stdout
    (n / "grant").write_text("allow model\nmodel model/b-big.gguf\nprogram cat $MODEL\n")
    r = launch(n, "check", state=tmp_path / "st")
    assert r.returncode == 0 and f"✓ model {n}/model/b-big.gguf" in r.stdout and "a-small" not in r.stdout, r.stdout
    (n / "grant").write_text("allow model\nmodel model/c-gone.gguf\nprogram cat $MODEL\n")
    r = launch(n, "check", state=tmp_path / "st")
    assert r.returncode == 1 and f"✗ model {n}/model/c-gone.gguf is not there" in r.stdout, r.stdout


def test_the_llm_nodes_grant_names_its_mind():
    """The pick is in the grant, not in ls order (card:model-acceptance.md)."""
    words = [l.split()[0] for l in (ROOT / "llm" / "grant").read_text().splitlines() if l.strip() and not l.startswith("#")]
    assert "model" in words


# --- F013: the third verdict at the grant's paths -------------------
#
# board/README.md §"What the days taught": a check has three verdicts,
# not two.  That rule was promoted 2026-09-01 and its closing sentence
# named where the next face would come from — "every other --check in the
# tree still has two verdicts" — and it came from this file, eleven lines
# above the one mechanism it cited, six hours later.
#
# `tools/sandbox.sh` binds neither /sys nor /dev/dri, and llm/grant names
# both, so `launch.sh llm check` from a fenced session printed two ✗,
# then "keep refuses this grant here — llm would not run", then "NOT
# installed".  Every one false about the machine and true about the seat.

def test_check_inside_the_fence_cannot_see_a_path_and_says_so(tmp_path):
    """A path the seat cannot see is not a path that is absent.

    The fixture's path is genuinely absent, which is the point: **a
    fenced session cannot tell the two apart**, so the honest verdict is
    "I cannot see this" and never "this is fine".  Unfenced, the same
    grant is still a red — that half must not regress.
    """
    n = tmp_path / "n"; n.mkdir()
    (n / "grant").write_text("allow /sys\nprogram cat $NODE/grant\n")

    outside = launch(n, "check", state=tmp_path / "so")
    assert outside.returncode == 1, outside.stdout
    assert "✗ allow /sys does not exist" in outside.stdout, outside.stdout
    assert "NOT installed" in outside.stdout, outside.stdout

    inside = launch(n, "check", state=tmp_path / "si", fenced=True)
    assert "✗ allow /sys does not exist" not in inside.stdout, (
        "the fenced check still calls a path it cannot see absent:\n" + inside.stdout)
    assert "· allow /sys is not visible from this seat" in inside.stdout, inside.stdout


def test_the_fenced_summary_claims_neither_installed_nor_not_installed(tmp_path):
    """The roll-up must not assert what the detail withdrew.

    This is F011 and F012's shape a fourth time: a summary line that
    means something other than the lines it rolls up.  If a path went to
    the third verdict, the check has not established that the node runs
    *or* that it does not, and both summaries would be claims it cannot
    make.
    """
    n = tmp_path / "n"; n.mkdir()
    (n / "grant").write_text("allow /sys\nprogram cat $NODE/grant\n")
    r = launch(n, "check", state=tmp_path / "st", fenced=True)
    assert "NOT installed" not in r.stdout, r.stdout
    assert "installed: n can run" not in r.stdout, r.stdout
    assert "not said from this seat" in r.stdout, r.stdout
    # and three verdicts get three exit codes: 2 is not 0, because
    # test_launch.py:133 gates two live-node tests on `returncode == 0`
    # and a seat that cannot see must not read as a machine that can run
    assert r.returncode == 2, r.returncode


def test_keep_is_not_asked_to_judge_a_grant_the_seat_cannot_read(tmp_path):
    """keep refusing a path the fence hides is the fence, not the machine.

    Left as a ✗ it produced the loudest false sentence of the four:
    *"keep refuses this grant here — llm would not run"*.
    """
    n = tmp_path / "n"; n.mkdir()
    (n / "grant").write_text("allow /sys\nprogram cat $NODE/grant\n")
    r = launch(n, "check", state=tmp_path / "st", fenced=True)
    assert "✗ keep refuses this grant here" not in r.stdout, r.stdout
    assert "keep was not asked" in r.stdout, r.stdout


def test_a_fenced_check_with_nothing_hidden_still_says_installed(tmp_path):
    """The third verdict must not swallow the other two.

    A fenced session reads this check more often than anyone, and a
    summary that said "not said from this seat" whenever the fence was on
    would make it useless exactly where it is used most.  Only a path
    that could not be seen buys the third verdict.
    """
    n = tmp_path / "n"; n.mkdir()
    (n / "data.txt").write_text("x")
    (n / "grant").write_text("allow data.txt\nprogram cat $NODE/data.txt\n")
    r = launch(n, "check", state=tmp_path / "st", fenced=True)
    assert r.returncode == 0, r.stdout
    assert "installed: n can run" in r.stdout, r.stdout
    assert "not said from this seat" not in r.stdout, r.stdout


# ── the edge: a node's process pulls a node (card:edge.md, day one, 2026-09-02) ──
#
# Henri: "solmuun kuuluva prosessi voisi antaa 'pull' -käskyn, joka pysyy
# voimassa kunnes prosessi sanoo 'stop' tai lopettaa."  The puller's
# grant says `pull NODE`; the launcher makes NODE/state/pulled/<puller>
# and names it in $TEND_PULLS; the program takes a shared flock on it.
# The pulled node is not idle while the lock is held, `serve` starts it
# when it is pulled and has no runner, and the kernel drops the lock on
# exit.  Two nodes that are nothing but the edge: the tree's own `die`
# and `solitaire`, copied to scratch with the edge pointed at the copy.

def edge_nodes(tmp_path):
    die = tmp_path / "die"; sol = tmp_path / "solitaire"
    shutil.copytree(ROOT / "die", die, ignore=shutil.ignore_patterns("state", "__pycache__"))
    shutil.copytree(ROOT / "solitaire", sol, ignore=shutil.ignore_patterns("state", "__pycache__"))
    g = sol / "grant"; g.write_text(g.read_text().replace("\npull die\n", "\npull ../die\n"))
    return die, sol


def locked(path):
    return subprocess.run(["flock", "-n", str(path), "true"]).returncode != 0


def test_a_pull_word_naming_a_node_is_an_edge_and_the_grant_says_so(tmp_path):
    """`pull` with a node's path is the edge: the pulled node's state is
    readable to the program, the edge file is named, and `status` says
    what this node pulls.  `pull` with anything else is the pull file, as
    it has been since the first node (test_the_nodes_grant_is_the_launchers_three_flags)."""
    die, sol = edge_nodes(tmp_path)
    r = launch(sol, "grant", state=sol / "state")
    assert r.returncode == 0, r.stderr
    assert f"--allow {die}/state" in r.stdout, r.stdout
    assert f"edge die {die}/state/pulled/solitaire" in r.stdout, r.stdout
    assert f"pull {sol}/state/pull" in r.stdout, "the pull file is still the default"
    s = launch(sol, "status", state=sol / "state")
    assert f"pulls: die ({die})" in s.stdout, s.stdout
    c = launch(sol, "check", state=sol / "state")
    assert c.returncode == 0 and "✓ pull die →" in c.stdout, c.stdout


def test_a_pull_that_reaches_back_is_refused_at_the_door_before_anything_runs(tmp_path):
    """card:hold.md rule 4: A pulls B pulls A with no canvas behind them.
    `check` says ✗ and exits 1; `run` exits 2 from either end and takes
    no lock, writes no log."""
    die, sol = edge_nodes(tmp_path)
    with (die / "grant").open("a") as f:
        f.write("pull ../solitaire\n")
    c = launch(die, "check", state=die / "state")
    assert c.returncode == 1 and "✗ pull solitaire reaches back to die" in c.stdout, c.stdout
    for node in (die, sol):
        r = launch(node, "run", state=node / "state")
        assert r.returncode == 2 and "reaches back" in r.stderr, (r.returncode, r.stderr)
        assert not (node / "state" / "log").exists(), "the cycle ran something"


@needs_syspy
def test_without_the_word_the_edge_is_refused_by_keep_and_the_program_says_so(tmp_path):
    """Red first, from both sides of the door.  A program that reads the
    die's state with no `pull die` in its grant is refused by keep — the
    kernel's voice, Permission denied.  The solitaire's own program,
    handed no edge, says which word is missing and dies with it in the
    death notice."""
    die, sol = edge_nodes(tmp_path)
    (die / "state").mkdir(); (die / "state" / "roll").write_text("6\n")
    peek = tmp_path / "peek"; peek.mkdir()
    (peek / "grant").write_text(f"program /bin/cat {die}/state/roll\n")
    r = launch(peek, "run", state=peek / "state")
    assert r.returncode != 0 and "Permission denied" in (peek / "state" / "log").read_text(), (peek / "state" / "log").read_text()
    g = sol / "grant"; g.write_text(g.read_text().replace("pull ../die\n", ""))
    r = launch(sol, "run", state=sol / "state")
    assert r.returncode == 2, (r.returncode, r.stderr)
    notice = (sol / "state" / "andon" / "andon.log").read_text()
    assert "solitaire: exited 2" in notice and "`pull die` is the word" in notice, notice


@needs_syspy
def test_a_process_pull_brings_the_die_up_and_lets_it_idle_out_when_it_lets_go(tmp_path):
    """The flow, measured by the lock and not by the clock: the solitaire's
    process locks the edge; `status` on the die names it; `serve` (the
    tick) starts the die because it is pulled; the die rolls; the
    solitaire reads the roll, lets go, exits 0; the die, unpulled, idles
    out within a tick; `serve` starts nothing more."""
    die, sol = edge_nodes(tmp_path)
    # TEND_IDLE reaches the die too: the solitaire's runner serves it, and the die's grant says `idle 30`
    env = dict(os.environ, TEND_STATE_DIR=str(sol / "state"), TEND_ANDON_STATE=str(tmp_path / "andon"),
               TEND_CANVAS=str(tmp_path / "canvas"), TEND_IDLE="0.5"); env.pop("TEND_FENCED", None)
    p = subprocess.Popen(["sh", str(LAUNCH), str(sol), "run"], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        edge = die / "state" / "pulled" / "solitaire"
        assert wait(lambda: edge.exists() and locked(edge), cap=8), "the solitaire's process never took the edge"
        s = launch(die, "status", state=die / "state")
        assert "pulled by: solitaire" in s.stdout, s.stdout
        # the die comes up at the lock, not at the tick: the puller's runner asked `serve` once for it
        # (Henri, 2026-09-02: "pystyisikö vedetty solmu käynnistymään heti vedon jälkeen?") — so a serve
        # by hand here finds a runner up, or the die already served, and starts nothing
        assert p.wait(timeout=30) == 0, "the solitaire did not get its roll — nothing served the die at the lock"
        assert "die is pulled by solitaire and no runner — started one" in (sol / "state" / "log").read_text(), (sol / "state" / "log").read_text()
        log = (sol / "state" / "log").read_text()
        assert re.search(r"solitaire: die rolled [1-6]$", log, re.M), log
        assert wait(lambda: not locked(edge)), "the edge was not let go"   # a reader's momentary flock -n is not the puller holding it (F019)
        assert wait(lambda: (die / "state" / "stopped").exists(), cap=10), "the die did not idle out after the pull was let go"
        assert (die / "state" / "stopped").read_text().startswith("idle:"), (die / "state" / "stopped").read_text()
        again = launch(die, "serve", state=die / "state", idle="0.5")
        assert again.returncode == 0 and again.stderr == "", "an edge that was let go restarted the die"
    finally:
        if p.poll() is None:
            p.kill(); p.wait()


def test_a_pulled_death_is_restarted_only_by_an_edge_newer_than_it(tmp_path):
    """Rule 3 for the edge, the plainest form: a puller under keep cannot
    touch its edge, so after a death the die waits for an edge made after
    it.  A lock on an old edge starts nothing; the same lock on a fresh
    edge does."""
    die, _ = edge_nodes(tmp_path)
    st = die / "state"; (st / "pulled").mkdir(parents=True)
    death = int(time.time()) - 60
    (st / "stopped").write_text("exited 127: die stopped by itself\n"); os.utime(st / "stopped", (death, death))
    edge = st / "pulled" / "solitaire"; edge.write_text(""); os.utime(edge, (death - 30, death - 30))
    # the pull as the solitaire's program takes it: a shared flock on this process's fd, closed to let go
    # (not `flock -s FILE sleep`: its child inherits the fd and keeps the lock after flock is killed)
    import fcntl
    fd = os.open(edge, os.O_RDONLY); fcntl.flock(fd, fcntl.LOCK_SH)
    try:
        assert locked(edge)
        a = launch(die, "serve", state=st, idle="0.5")
        assert a.returncode == 0 and a.stderr == "", (a.returncode, a.stderr)
        assert (st / "stopped").read_text().startswith("exited 127"), "a death older than its edge was restarted"
        os.utime(edge, (death + 30, death + 30))
        b = launch(die, "serve", state=st, idle="0.5")
        assert b.returncode == 0 and "the edge is newer than its death" in b.stderr, (b.returncode, b.stderr)
        # `run` removes `stopped` as it starts and writes it again at the stop: gone or rewritten is restarted
        assert wait(lambda: not (st / "stopped").exists() or not (st / "stopped").read_text().startswith("exited 127"), cap=8), \
            "the fresh edge did not restart the die"
    finally:
        os.close(fd)
        # the die is up under the lock we held; let go and let it idle out, so no runner outlives the test
        wait(lambda: (st / "stopped").exists() and (st / "stopped").read_text().startswith("idle:"), cap=10)


def test_an_empty_pull_file_is_the_fences_precreation_and_starts_nothing(tmp_path):
    """F017: tools/sandbox.sh makes every node's pull file empty on the
    person's side so a first pull can land, and `serve` read the empty
    file with no `stopped` as an unserved pull — the edge's two nodes
    were run by the tick the minute they arrived.  A pull is a line."""
    st = tmp_path / "st"; st.mkdir()
    (st / "node.state.pull").write_text("")
    a = launch(ROOT / "node", "serve", state=st, idle="0.4")
    assert a.returncode == 0 and a.stderr == "", (a.returncode, a.stderr)
    time.sleep(0.3)
    assert not (st / "stopped").exists() and not (st / "log").exists(), "an empty pull file ran the node"
    s = launch(ROOT / "node", "status", state=st)
    assert "last pull" not in s.stdout, s.stdout
    launch(ROOT / "node", "pull", "one line", state=st, idle="0.4")   # from a person's shell: appends and starts
    assert wait(lambda: (st / "stopped").exists(), cap=8), "a real pull was not served"


# ── the conversation over the edge: `connect PORT` (card:edge.md, 2026-09-02) ──

@needs_syspy
def test_connect_is_a_grant_word_and_without_it_the_kernel_refuses_the_talk(tmp_path):
    """keep's --connect has been there since 2026-08-28 with no grant word to
    reach it.  A node whose grant says `connect PORT` talks to a listener
    on that port under keep; the same program with the word gone is
    refused by the kernel — Permission denied, not a script's care."""
    import socket
    srv = socket.socket(); srv.bind(("127.0.0.1", 0)); srv.listen(1); port = srv.getsockname()[1]
    try:
        node = tmp_path / "talker"; node.mkdir()
        prog = f"program /usr/bin/python3 -c 'import socket; socket.socket().connect((\"127.0.0.1\", {port})); print(\"connected\")'\n"
        (node / "grant").write_text(f"connect {port}\n" + prog)
        g = launch(node, "grant", state=node / "state")
        assert f"--connect {port}" in g.stdout, g.stdout
        r = launch(node, "run", state=node / "state")
        assert r.returncode == 0 and "connected" in (node / "state" / "log").read_text(), (r.stderr, (node / "state" / "log").read_text())
        c = launch(node, "check", state=node / "state")
        assert f"· connect {port}" in c.stdout and c.returncode == 0, c.stdout
        (node / "grant").write_text("bind 1\n" + prog)   # the TCP boundary on, the word gone
        r = launch(node, "run", state=node / "state")
        assert r.returncode != 0 and "Permission denied" in (node / "state" / "log").read_text(), (node / "state" / "log").read_text()
        (node / "grant").write_text("connect eighty\n" + prog)
        r = launch(node, "grant", state=node / "state")
        assert r.returncode == 2 and "connect wants a port" in r.stderr, r.stderr
    finally:
        srv.close()


# ── the first conversation over an edge: the ask node (card:edge.md, 2026-09-02) ──

class _Llm:
    """A stand-in for llama-server's two doors — /health and one chat completion —
    on a free port, in a thread.  The test builds the side it means."""
    def __init__(self):
        import http.server, threading
        class H(http.server.BaseHTTPRequestHandler):
            def log_message(self, *a): pass
            def do_GET(self):
                self.send_response(200); self.end_headers(); self.wfile.write(b"ok")
            def do_POST(self):
                body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                q = body["messages"][-1]["content"]
                if "THINK" in q:   # gemma4 under --jinja at 15:41: the cap spent on thinking, content empty
                    out = {"choices": [{"message": {"role": "assistant", "content": "", "reasoning_content": "hmm what is tend really"}}]}
                elif "CUT" in q:   # gemma4 2026-09-03: a partial answer the token cap ended, finish_reason length
                    out = {"choices": [{"finish_reason": "length", "message": {"role": "assistant", "content": "Tend on ymparisto jossa"}}]}
                else:
                    out = {"choices": [{"message": {"role": "assistant", "content": f"ANSWER to: {q}"}}]}
                self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers()
                self.wfile.write(json.dumps(out).encode())
        self.srv = http.server.HTTPServer(("127.0.0.1", 0), H)
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()
        self.port = self.srv.server_address[1]
    def close(self):
        self.srv.shutdown()


def ask_nodes(tmp_path, port, connect=True):
    """The tree's `ask`, copied, its edge pointed at a scratch `llm` and its talk at the stand-in's port."""
    llm = tmp_path / "llm"; (llm / "state").mkdir(parents=True)
    (llm / "grant").write_text("program true\n")
    ask = tmp_path / "ask"
    shutil.copytree(ROOT / "ask", ask, ignore=shutil.ignore_patterns("state", "__pycache__"))
    g = (ask / "grant").read_text().replace("\npull llm\n", "\npull ../llm\n")
    g = g.replace(f"\nconnect 18080\n", f"\nconnect {port}\n" if connect else "\nbind 1\n")
    g += f"env ASK_URL=http://127.0.0.1:{port}\nenv ASK_WAIT=4\n"
    (ask / "grant").write_text(g)
    return llm, ask


@needs_syspy
def test_the_ask_node_pulls_the_llm_talks_to_it_over_the_edge_and_lets_go(tmp_path):
    """`pull llm` for the signal, `connect PORT` for the talk: the ask node
    takes the edge, waits for /health, asks its one question, writes the
    answer beside the signal in its own state, and lets go."""
    llm_stub = _Llm()
    try:
        llm, ask = ask_nodes(tmp_path, llm_stub.port)
        r = launch(ask, "run", "Say", "hi", state=ask / "state", timeout=60)
        log = (ask / "state" / "log").read_text()
        assert r.returncode == 0, (r.stderr, log)
        assert "ask: ANSWER to: Say hi" in log, log
        assert (ask / "state" / "answer").read_text() == "Say hi\n---\nANSWER to: Say hi\n"
        edge = llm / "state" / "pulled" / "ask"
        assert edge.exists() and wait(lambda: not locked(edge)), "the edge was not let go"   # tolerate a reader's momentary flock -n (F019)
    finally:
        llm_stub.close()


@needs_syspy
def test_without_connect_the_talk_is_refused_by_the_kernel_and_the_ask_node_says_which_word(tmp_path):
    """The signal without the talk: `pull llm` and no `connect` — the edge is
    taken, the first request is Permission denied, and the program names
    the missing word instead of waiting out its clock."""
    llm_stub = _Llm()
    try:
        llm, ask = ask_nodes(tmp_path, llm_stub.port, connect=False)
        r = launch(ask, "run", state=ask / "state", timeout=60)
        log = (ask / "state" / "log").read_text()
        assert r.returncode == 2 and "connect refused by keep" in log and "`connect PORT` is the word" in log, (r.returncode, log)
    finally:
        llm_stub.close()


@needs_syspy
def test_the_ask_node_reads_the_llms_death_from_its_state_and_stops_at_once(tmp_path):
    """The pulled node's state is the interface (Henri, 2026-09-02): the
    llm dying at its loader is a `stopped` newer than the edge, readable
    to the puller, and the resolver will not restart it on that edge —
    so the ask node says so and exits, instead of waiting out its clock
    as it did at 15:26 (300 s to "never answered")."""
    llm, ask = ask_nodes(tmp_path, 1)   # a port nothing listens on; the grant's ASK_WAIT is 4 s
    g = (ask / "grant").read_text().replace("env ASK_WAIT=4\n", "env ASK_WAIT=30\n")
    (ask / "grant").write_text(g)
    env = dict(os.environ, TEND_STATE_DIR=str(ask / "state"), TEND_ANDON_STATE=str(tmp_path / "andon"),
               TEND_CANVAS=str(tmp_path / "canvas")); env.pop("TEND_FENCED", None)
    p = subprocess.Popen(["sh", str(LAUNCH), str(ask), "run"], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        edge = llm / "state" / "pulled" / "ask"
        assert wait(lambda: edge.exists() and locked(edge), cap=8), "the ask node never took the edge"
        time.sleep(1.1)   # the death must be newer than the edge, on a filesystem with second mtimes
        (llm / "state" / "stopped").write_text("exited 127: llm stopped by itself\n")
        assert p.wait(timeout=15) == 1, "the ask node did not stop on the llm's death"
        log = (ask / "state" / "log").read_text()
        assert "ask: llm died while pulled — exited 127" in log and "pull again" in log, log
        assert wait(lambda: not locked(edge))   # F019
    finally:
        if p.poll() is None:
            p.kill(); p.wait()


@needs_syspy
def test_a_partial_answer_the_token_cap_cut_is_said_and_not_passed_off_as_whole(tmp_path):
    """card:material.md, 2026-09-03: gemma4's answer was cut mid-sentence at
    the 800-token cap and ask wrote the partial content as if it were the
    whole.  A reply whose finish_reason is `length` is unfinished — ask says
    so, in the answer file and on the screen, so a cut does not read as an
    answer (the F010 family: a cut that says nothing)."""
    llm_stub = _Llm()
    try:
        llm, ask = ask_nodes(tmp_path, llm_stub.port)
        r = launch(ask, "run", "CUT", "please", state=ask / "state", timeout=60)
        log = (ask / "state" / "log").read_text()
        assert r.returncode == 0, (r.stderr, log)
        answer = (ask / "state" / "answer").read_text()
        assert "Tend on ymparisto jossa" in answer, answer
        assert "cut" in answer and "800" in answer, answer   # the file says the cap ended it, unfinished
        assert "cut" in log or "unfinished" in log, log      # and the screen does too
    finally:
        llm_stub.close()


@needs_syspy
def test_an_answer_that_is_all_thinking_is_said_as_no_answer_and_kept(tmp_path):
    """The first live answer, 15:41: 200 tokens of reasoning, an empty
    `content`, and ask said "ask: " and exited 0 as if answered.  Now the
    thinking is kept in `answer` under its own rule, the log says there
    was no answer and why, and the exit is still 0 — the llm did reply."""
    llm_stub = _Llm()
    try:
        llm, ask = ask_nodes(tmp_path, llm_stub.port)
        r = launch(ask, "run", "THINK", "about", "tend", state=ask / "state", timeout=60)
        log = (ask / "state" / "log").read_text()
        assert r.returncode == 0, (r.stderr, log)
        assert "ask: no answer — the llm thought for 5 words" in log, log
        ans = (ask / "state" / "answer").read_text()
        assert ans.startswith("THINK about tend\n---\n\n---thinking (5 words)---\nhmm what is tend really\n"), ans
    finally:
        llm_stub.close()
