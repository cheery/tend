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


has_llm = shutil.which("llama-server") and list((ROOT / "llm" / "model").glob("*.gguf"))


@pytest.mark.skipif(not has_llm, reason="no llama-server on PATH or no *.gguf under llm/model — the second node cannot run here")
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


@pytest.mark.skipif(not has_llm, reason="no llama-server on PATH or no *.gguf under llm/model — the second node cannot run here")
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
