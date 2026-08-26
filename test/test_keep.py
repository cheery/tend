"""`tools/keep.py` — a program reads only what it was handed (board/keep.md).

The card's owed demonstration, as a test: a program run under keep reads
a granted file and is refused the file beside it, the tree, and the
ledger — from inside the fence, unprivileged, no build.  Landlock is the
mechanism (measured available at ABI 4); where it is absent these skip,
out loud, because a skipped confinement test is not a passing one.
"""

import ctypes
import os
import pathlib
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
KEEP = ROOT / "tools" / "keep.py"


def _landlock_abi():
    libc = ctypes.CDLL(None, use_errno=True)
    libc.syscall.restype = ctypes.c_long
    return libc.syscall(444, None, 0, 1)  # create_ruleset(NULL, 0, VERSION)


needs_landlock = pytest.mark.skipif(
    _landlock_abi() < 1,
    reason="no Landlock here — the confinement cannot be shown to hold")


def keep(*args, **kw):
    return subprocess.run([sys.executable, str(KEEP), *args],
                          capture_output=True, text=True, **kw)


def denied(text):
    # locale-independent: EACCES surfaced by cat, in any language
    return "cat:" in text and ("mine" not in text.split("cat:")[1][:40])


def test_it_parses():
    assert subprocess.run([sys.executable, "-m", "py_compile", str(KEEP)]).returncode == 0


@needs_landlock
def test_a_program_reads_what_it_was_handed_and_not_the_file_beside_it(tmp_path):
    """The whole card in one run: grant one file, and the neighbour is
    unreadable though it sits in the same directory."""
    (tmp_path / "mine").write_text("granted\n")
    (tmp_path / "beside").write_text("secret\n")
    r = keep("--allow", str(tmp_path / "mine"), "--", "sh", "-c",
             f"cat {tmp_path/'mine'}; cat {tmp_path/'beside'}")
    assert "granted" in r.stdout, r.stderr
    assert "secret" not in r.stdout, "the file beside it was readable — keep did not hold"
    assert r.returncode != 0, "reading the ungranted file must fail"


@needs_landlock
def test_the_tree_and_the_ledger_are_blind(tmp_path):
    """A program under keep cannot read the tree it runs in, nor another
    mechanism's log, unless handed them — problem 1, enforced."""
    (tmp_path / "mine").write_text("ok\n")
    r = keep("--allow", str(tmp_path), "--", "sh", "-c",
             f"cat {ROOT/'board'/'README.md'}")
    assert r.returncode != 0
    assert "founding" not in r.stdout and "board" not in r.stdout.lower()


@needs_landlock
def test_a_granted_directory_is_readable_beneath(tmp_path):
    """Grant a directory and files under it read; a sibling directory
    does not."""
    (tmp_path / "in").mkdir()
    (tmp_path / "in" / "f").write_text("inside\n")
    (tmp_path / "out").mkdir()
    (tmp_path / "out" / "f").write_text("outside\n")
    r = keep("--allow", str(tmp_path / "in"), "--", "sh", "-c",
             f"cat {tmp_path/'in'/'f'}; cat {tmp_path/'out'/'f'}")
    assert "inside" in r.stdout
    assert "outside" not in r.stdout


@needs_landlock
def test_a_system_program_still_runs(tmp_path):
    """The system roots are granted, so a system interpreter and its
    libraries still load — a confinement that cannot run the program is
    useless.  (A *venv* interpreter reads its pyvenv.cfg in the tree, so
    it must be handed that too: keep grants what it is given, the runtime
    included — board/keep.md.  Here the system python proves the roots
    suffice for a system program.)"""
    syspy = "/usr/bin/python3"
    if not os.path.exists(syspy):
        pytest.skip("no /usr/bin/python3 to prove a system program runs")
    r = keep("--allow", str(tmp_path), "--", syspy, "-c",
             "import json, os; print('ran', json.dumps(os.getpid() > 0))")
    assert r.returncode == 0, r.stderr
    assert "ran true" in r.stdout


@needs_landlock
def test_the_pull_node_runs_confined_under_keep(tmp_path):
    """`board/keep.md`'s next slice: the first real program, run *through*
    keep — the grant outside it — gains the boundary.  Handed its own code
    and a state directory and nothing else, the node opens, runs and stops
    (it writes state where the fence allows; keep governs reads), while a
    read of the tree from the same grant is refused.  The node itself is
    unchanged — the boundary is composed around it, not built into it."""
    node = ROOT / "node" / "node.py"
    state = tmp_path / "n.state"
    syspy = "/usr/bin/python3"
    if not os.path.exists(syspy):
        pytest.skip("no system python3 to run the node confined")
    # handed: the node's own directory (its code) and the state directory.
    r = keep("--allow", str(node.parent), "--allow", str(tmp_path), "--",
             syspy, str(node), "--state", str(state),
             "run", "--idle", "0.4", "--poll", "0.05")
    assert r.returncode == 0, r.stderr
    assert state.exists(), "the node could not open where it was left"
    import json
    assert json.loads(state.read_text())["generations"] == 1

    # the same grant is blind to the tree it was not handed.
    blind = keep("--allow", str(node.parent), "--allow", str(tmp_path), "--",
                 "sh", "-c", f"cat {ROOT/'board'/'README.md'}")
    assert blind.returncode != 0
    assert "founding" not in blind.stdout


def test_the_node_launcher_confines_by_default(tmp_path):
    """`node/run.sh` — `board/keep.md`'s last open half: the node runs
    confined *without the incantation*, and it is write-scoping's first
    caller.  The grant is baked into the launcher — the node's code
    readable, its state directory writable (`--write`), nothing else —
    so `run.sh run` opens, runs, stops and writes its state under the
    state dir.  The launcher's confinement is keep's, tested above; what
    this holds is that running the node is now running it confined, and
    that the state dir must be *writable* — a read-only grant there and
    the node cannot open its own state."""
    run = ROOT / "node" / "run.sh"
    syspy = "/usr/bin/python3"
    if not os.path.exists(syspy):
        pytest.skip("no system python3 for keep to grant the node")
    state = tmp_path / "st"
    env = dict(os.environ, TEND_NODE_STATE_DIR=str(state))
    r = subprocess.run(["sh", str(run), "run", "--idle", "0.4", "--poll", "0.05"],
                       env=env, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    import json
    assert (state / "node.state").exists(), "the node's state did not land in its state dir"
    assert json.loads((state / "node.state").read_text())["generations"] == 1


def test_nothing_to_run_is_refused_out_loud():
    r = keep("--allow", "/tmp")
    assert r.returncode == 2 and "nothing to run" in r.stderr


def test_an_unknown_argument_is_refused_out_loud():
    r = keep("--bogus", "--", "true")
    assert r.returncode == 2 and "unknown argument" in r.stderr


def test_a_missing_grant_is_refused_out_loud(tmp_path):
    r = keep("--allow", str(tmp_path / "nope"), "--", "true")
    assert r.returncode != 0 and "does not exist" in r.stderr


def test_write_is_scoped_when_asked(tmp_path):
    """Write-scoping — `board/keep.md`, the slice after reads, built
    2026-08-26.  `--write PATH` grants read+write beneath a path;
    `--allow` stays read-only.  A program handed one writable dir and
    one readable dir writes the first, reads the second, and is refused
    writing the second.  Until this, keep governed reads only and a
    program wrote where the fence allowed."""
    (tmp_path / "wr").mkdir()
    (tmp_path / "ro").mkdir()
    (tmp_path / "ro" / "seed").write_text("readable\n")
    ok = keep("--write", str(tmp_path / "wr"), "--allow", str(tmp_path / "ro"),
              "--", "sh", "-c",
              f"echo hi > {tmp_path/'wr'/'new'} && cat {tmp_path/'ro'/'seed'}")
    assert ok.returncode == 0, ok.stderr
    assert (tmp_path / "wr" / "new").read_text() == "hi\n"
    denied = keep("--write", str(tmp_path / "wr"), "--allow", str(tmp_path / "ro"),
                  "--", "sh", "-c", f"echo no > {tmp_path/'ro'/'blocked'}")
    assert denied.returncode != 0, "wrote into a read-only grant"
    assert not (tmp_path / "ro" / "blocked").exists()


def test_without_write_the_boundary_is_not_set(tmp_path):
    """The opt-in, stated as a test: with no `--write`, keep governs
    reads only and a program writes where the fence allows — the
    documented default the write slice did not change."""
    (tmp_path / "d").mkdir()
    r = keep("--allow", str(tmp_path / "d"), "--", "sh", "-c",
             f"echo x > {tmp_path/'d'/'f'}")
    assert r.returncode == 0, r.stderr
    assert (tmp_path / "d" / "f").exists()


def _loopback_listener():
    """A TCP listener in the test process, bound before any confinement,
    for a confined child to try to reach.  Returns (socket, port)."""
    import socket
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    s.listen(1)
    return s, s.getsockname()[1]


_CONNECT = ("import socket, errno, sys\n"
            "s = socket.socket()\n"
            "try:\n"
            "    s.connect(('127.0.0.1', int(sys.argv[1]))); print('connected')\n"
            "except OSError as e:\n"
            "    print('refused', errno.errorcode.get(e.errno, e.errno))\n")

_BIND = ("import socket, errno\n"
         "s = socket.socket()\n"
         "try:\n"
         "    s.bind(('127.0.0.1', 0)); print('bound')\n"
         "except OSError as e:\n"
         "    print('refused', errno.errorcode.get(e.errno, e.errno))\n")


@pytest.mark.skipif(_landlock_abi() < 4,
                    reason="Landlock below ABI 4 — no network bits to hold")
def test_no_net_refuses_tcp_when_asked(tmp_path):
    """Network-scoping — `board/keep.md`, the last unset Landlock bit,
    built 2026-08-26.  `--no-net` handles both TCP bits with nothing
    granted beneath them: a program can neither connect to a listener
    that is right there on loopback nor bind a port of its own, and the
    refusal is EACCES — keep's, not the network's.  A UNIX socket is not
    TCP and still binds, so the boundary is exactly the one named."""
    srv, port = _loopback_listener()
    try:
        plain = keep("--allow", str(tmp_path), "--", "/usr/bin/python3", "-c",
                     _CONNECT, str(port))
        if "connected" not in plain.stdout:
            pytest.skip(f"loopback is unreachable from this seat: {plain.stdout!r} {plain.stderr!r}")
        r = keep("--allow", str(tmp_path), "--no-net", "--", "/usr/bin/python3",
                 "-c", _CONNECT, str(port))
        assert r.stdout.strip() == "refused EACCES", (r.stdout, r.stderr)
        b = keep("--allow", str(tmp_path), "--no-net", "--", "/usr/bin/python3",
                 "-c", _BIND)
        assert b.stdout.strip() == "refused EACCES", (b.stdout, b.stderr)
        u = keep("--write", str(tmp_path), "--no-net", "--", "/usr/bin/python3",
                 "-c", "import socket; s=socket.socket(socket.AF_UNIX); "
                       f"s.bind({str(tmp_path/'u.sock')!r}); print('unix ok')")
        assert "unix ok" in u.stdout, (u.stdout, u.stderr)
    finally:
        srv.close()


@needs_landlock
def test_without_no_net_the_network_is_not_touched(tmp_path):
    """The opt-in, stated as a test: with no `--no-net`, a program has
    whatever network the fence left it — here, at least loopback; a
    bind to port 0 succeeds under a read grant alone."""
    r = keep("--allow", str(tmp_path), "--", "/usr/bin/python3", "-c", _BIND)
    assert r.stdout.strip() == "bound", (r.stdout, r.stderr)


def test_the_node_launcher_asks_for_no_net():
    """`node/run.sh` is `--no-net`'s first caller: the node is a tally
    through a file and has no business on a socket.  The confinement is
    keep's, tested above; what this holds is that the launcher asks for
    it — the well-behaved node itself cannot show the boundary
    (board/green.md: a launcher's confinement is invisible through a
    program that never overreaches)."""
    run = (ROOT / "node" / "run.sh").read_text()
    exec_block = run[run.index("exec "):]
    assert "--no-net" in exec_block


def _state(tmp_path):
    import json
    return json.loads((tmp_path / "st" / "node.state").read_text())


def _launcher(tmp_path, *verb, idle="0.5"):
    env = dict(os.environ, TEND_NODE_STATE_DIR=str(tmp_path / "st"), TEND_NODE_IDLE=idle)
    env.pop("TEND_FENCED", None)  # a person's shell: the launcher may start a runner there
    return subprocess.run(["sh", str(ROOT / "node" / "run.sh"), *verb],
                          env=env, capture_output=True, text=True, timeout=20)


def _wait(pred, cap=4.0):
    import time
    t = time.monotonic()
    while time.monotonic() - t < cap:
        if pred():
            return True
        time.sleep(0.05)
    return pred()


@needs_landlock
def test_a_pull_with_no_runner_starts_one_confined(tmp_path):
    """`board/resolver.md`, day one: the pull is the launch.  Nothing is
    running; `run.sh pull` starts the node under its grant, waits for it
    to open, and the pull is served by it — the person never typed
    `run`.  The runner then stops by itself when pulls stop and lets go
    of the lock.  (`node.py pull` alone still serves nothing —
    `test_node.py`; the starting lives in the launcher, where the grant
    is.)"""
    if not os.path.exists("/usr/bin/python3"):
        pytest.skip("no system python3 for keep to grant the node")
    r = _launcher(tmp_path, "pull")
    assert r.returncode == 0, r.stderr
    assert "started a runner" in r.stderr, r.stderr
    assert _wait(lambda: _state(tmp_path)["pulls"] == 1), _state(tmp_path)
    assert _state(tmp_path)["generations"] == 1
    lock = tmp_path / "st" / "run.lock"
    assert _wait(lambda: subprocess.run(["flock", "-n", str(lock), "true"]).returncode == 0, cap=6), \
        "the runner did not stop and free the lock after idle"
    assert _state(tmp_path)["last_stop"] is not None


@needs_landlock
def test_a_second_pull_finds_the_runner_and_starts_no_other(tmp_path):
    """Two pulls, one runner: the second finds the lock held and only
    pulls.  One generation serves both."""
    if not os.path.exists("/usr/bin/python3"):
        pytest.skip("no system python3 for keep to grant the node")
    a = _launcher(tmp_path, "pull", idle="1.5")
    b = _launcher(tmp_path, "pull", idle="1.5")
    assert a.returncode == 0 and b.returncode == 0, (a.stderr, b.stderr)
    assert "started a runner" in a.stderr and "started a runner" not in b.stderr
    assert _wait(lambda: _state(tmp_path)["pulls"] == 2), _state(tmp_path)
    assert _state(tmp_path)["generations"] == 1


@needs_landlock
def test_run_is_refused_while_a_runner_holds_the_lock(tmp_path):
    """A hand-started `run` is not an error and not a second runner: the
    lock says one is up, and `run` leaves with 75 and a word."""
    if not os.path.exists("/usr/bin/python3"):
        pytest.skip("no system python3 for keep to grant the node")
    first = _launcher(tmp_path, "pull", idle="1.5")
    assert first.returncode == 0, first.stderr
    second = _launcher(tmp_path, "run")
    assert second.returncode == 75, (second.returncode, second.stderr)
    assert "already holds" in second.stderr
    assert _wait(lambda: _state(tmp_path)["generations"] == 1)


def test_the_launchers_grant_appears_once():
    """The grant *is* the boundary, and three copies are three places
    for it to drift — the 13:34 kaizen's own miss, where the first draft
    of `run.sh` pasted the keep invocation into every verb.  So: exactly
    one line in the launcher invokes `tools/keep.py`, and every verb
    goes through it.  A second invocation anywhere is red."""
    run = (ROOT / "node" / "run.sh").read_text()
    lines = [l for l in run.splitlines() if "tools/keep.py" in l and not l.lstrip().startswith("#")]
    assert len(lines) == 1, lines


def test_inside_the_fence_a_pull_starts_nothing(tmp_path):
    """`board/resolver.md`, the resolver outside: with `TEND_FENCED` set,
    `run.sh pull` appends its line, says the resolver will serve it, and
    starts no runner — the runner is `tools/resolve.sh`'s to start from
    the person's side.  Red until the launcher patch is applied."""
    if not os.path.exists("/usr/bin/python3"):
        pytest.skip("no system python3 for keep to grant the node")
    env = dict(os.environ, TEND_NODE_STATE_DIR=str(tmp_path / "st"), TEND_NODE_IDLE="0.5", TEND_FENCED="1")
    r = subprocess.run(["sh", str(ROOT / "node" / "run.sh"), "pull"], env=env,
                       capture_output=True, text=True, timeout=20)
    assert r.returncode == 0, r.stderr
    assert "resolver" in r.stderr and "started a runner" not in r.stderr, r.stderr
    assert (tmp_path / "st" / "node.state.pull").exists()
    assert not (tmp_path / "st" / "node.state").exists(), "a runner opened"
