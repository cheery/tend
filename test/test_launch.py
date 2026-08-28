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
import shutil
import subprocess
import sys
import time

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
LAUNCH = ROOT / "tools" / "launch.sh"


def launch(node, *args, state, idle="0.5", fenced=False, timeout=30):
    env = dict(os.environ, TEND_STATE_DIR=str(state), TEND_IDLE=idle)
    env.pop("TEND_FENCED", None)
    if fenced:
        env["TEND_FENCED"] = "1"
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
    other, and it needs no new word: a program burning a core is not idle."""
    n = tmp_path / "n"; n.mkdir()
    (n / "grant").write_text("pulse beat\nidle 2\nprogram /usr/bin/python3 -c 'exec(\"import time\\nt=time.time()+8\\nwhile time.time()<t: pass\")'\n")
    st = tmp_path / "st"
    t0 = time.time()
    r = launch(n, "run", state=st, idle="2", timeout=60)
    took = time.time() - t0
    assert "idle" not in (st / "stopped").read_text(), (st / "stopped").read_text() + (st / "log").read_text()
    assert took > 6, f"it was stopped at idle, {took:.1f}s"
    (n / "grant").write_text("pulse beat\nidle 2\nprogram sleep 30\n")
    t0 = time.time()
    r = launch(n, "run", state=tmp_path / "st2", idle="2", timeout=60)
    assert "idle" in (tmp_path / "st2" / "stopped").read_text() and time.time() - t0 < 10, "silent and asleep is idle"


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
