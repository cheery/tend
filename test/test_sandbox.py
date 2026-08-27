"""`tools/sandbox.sh` — the fence is up, the clock first.

The sessions-first trial of 2026-08-25 (`doc/experiments/2026-08-25-both.md`)
promoted to a tool.  What is checked here is what that day found: a
fence that hides the state directory defeats the sitting limit, so the
check that matters most is not that `~/.ssh` is gone but that the
sitting clock inside is the host's.  `--check` is the mechanism and
these tests are what say it still says the truth.

Everything that needs bubblewrap skips, out loud, on a machine without
it — a skipped fence test is not a passing one, and the skip reason
names the package.
"""

import json
import os
import pathlib
import re
import shutil
import subprocess

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
FENCE = ROOT / "tools" / "sandbox.sh"

#: Inside the fence these skip, and the pre-commit gate now runs inside
#: the fence, so at a commit the fence's own tests do not run.  They run
#: when the suite is run by a person outside, and `--check` is what a
#: person runs to see the fence is up.  Skipped, named, not hidden.
needs_bwrap = pytest.mark.skipif(
    shutil.which("bwrap") is None or os.environ.get("TEND_FENCED") == "1",
    reason="no bubblewrap here, or already inside the fence — it cannot nest")


def sandbox(*args, **kw):
    return subprocess.run(["sh", str(FENCE), *args], cwd=ROOT,
                          capture_output=True, text=True, **kw)


def test_it_parses():
    assert subprocess.run(["sh", "-n", str(FENCE)]).returncode == 0


def test_the_rows_are_the_dial():
    out = sandbox("--rows")
    assert out.returncode == 0
    names = [line.split()[1] for line in out.stdout.splitlines() if line.strip()]
    assert names == ["tree", "state", "trees", "scratch", "git", "net", "audio", "display"]
    on = [line.split()[0] for line in out.stdout.splitlines() if line.strip()]
    assert on == ["on"] * 5 + ["off"] * 3, "five on by default, three off until asked"


def test_the_bus_is_not_a_row():
    """Measured 2026-08-25 (`board/done/grant.md`): with the user bus inside,
    `systemd-run --user --wait` ran a command on the host — home, PATH
    and no fence — because the manager spawns it, not the caller.  The
    row's one caller, the leash, now wraps the fence from outside.  A
    row with no caller that is also an escape is not a row."""
    out = sandbox("--reach", "bus", "true")
    assert out.returncode == 2 and "no such row" in out.stderr


@needs_bwrap
def test_check_says_the_fence_is_up_here():
    out = sandbox("--check")
    assert out.returncode == 0, out.stdout + out.stderr
    assert "the fence is up" in out.stdout
    assert out.stdout.index("sitting clock") < out.stdout.index("~/.ssh"), \
        "the clock is proved before the secrets — that is the order the day taught"


@needs_bwrap
def test_inside_the_tree_is_writable_and_home_is_not_real():
    out = sandbox("sh", "-c", 'test -w "$PWD" && ! test -e "$HOME/.bashrc" && echo ok')
    assert out.stdout.strip() == "ok", out.stderr


@needs_bwrap
def test_inside_is_marked_and_cannot_nest():
    out = sandbox("sh", "-c", 'echo "$TEND_FENCED"')
    assert out.stdout.strip() == "1"
    nested = sandbox("sh", str(FENCE), "true")
    assert nested.returncode == 3 and "cannot nest" in nested.stderr


@needs_bwrap
def test_the_restraints_are_read_only_inside():
    """`board/fence.md`'s measurement: from a tend session, `python3 -c`
    rewrote `.claude/settings.json` and `mv` made it vanish.  Inside the
    fence the tree is the world — except this directory.  This is the
    demonstration the card owed: what it caught, that had gone through."""
    settings = ROOT / ".claude" / "settings.json"
    before = settings.read_bytes()
    out = sandbox("env", "LC_ALL=C", "sh", "-c",
                  f"python3 -c \"open('{settings}', 'a').write('x')\"; "
                  f"mv '{settings}' '{settings}.away'; touch '{settings}.probe'")
    combined = out.stdout + out.stderr
    assert settings.read_bytes() == before, combined
    assert not settings.with_suffix(".json.away").exists()
    assert not settings.with_suffix(".json.probe").exists()
    # As above: the write is refused read-only (EROFS), read across both
    # streams and with LC_ALL=C; mv/touch not happening is carried by the
    # asserts above, whose errno is binding-dependent (the >=3 count this
    # replaced assumed all three were EROFS, which holds only when the
    # whole directory is bound read-only, not the file-bind shape).
    assert ("Read-only file system" in combined
            or "Kirjoitussuojattu" in combined), combined


def test_the_protected_set_is_the_scripts_the_hooks_run():
    """`board/self.md`'s line: a path is in the set if a session editing it
    changes what the session is allowed to do before anyone looks.  That
    is every script a hook runs — read fresh, unfenced, as the person —
    and what those exec on the person's side, `leash.sh` first: it shapes
    cost *and* it is the program the hook runs the fence through.  The set is read from this
    clone's settings, so a hook added without its script being protected
    is caught here."""
    out = sandbox("--protected")
    assert out.returncode == 0
    protected = set(out.stdout.split())
    settings = json.loads((ROOT / ".claude" / "settings.json").read_text(encoding="utf-8"))
    hooked = set()
    for event in settings["hooks"].values():
        for group in event:
            for h in group["hooks"]:
                m = re.search(r"tools/([\w-]+\.sh)", h["command"])
                assert m, h["command"]
                hooked.add("tools/" + m.group(1))
    assert hooked <= protected, f"a hook runs a script outside the protected set: {hooked - protected}"
    for p in ("tools/leash.sh", "tools/keep.py", "tools/andon.sh"):
        assert p in protected, (f"{p} runs on the person's side (the hook execs leash.sh unfenced with the "
                                "sandbox as its argument; the launcher confines a node with keep.py; limit.sh "
                                "grants on andon.sh's record) — card:install.md, 2026-08-27")
    for p in protected:
        assert (ROOT / p).is_file(), p


def test_the_persons_keys_are_in_the_protected_set():
    """`board/self.md`, 2026-08-26: `reach-allow.sh` and
    `hook-installer.sh` moved from `~` into `tools/` and must join the
    set — a session editing either changes what the session is allowed
    to do, through the person's next run of it (the reach bound, the
    fence install).  No bwrap: this reads `--protected`, which is a
    listing.  Red until `sandbox.sh` lists them and `fence.sh --protect`
    has added their `Edit` rules."""
    protected = set(sandbox("--protected").stdout.split())
    for key in ("tools/reach-allow.sh", "tools/hook-installer.sh"):
        assert key in protected, (
            f"{key} is in tools/ but not the protected set — apply "
            "keys-into-set.patch and run tools/fence.sh --protect")


@needs_bwrap
def test_the_fences_own_code_is_read_only_inside():
    """`board/self.md`'s measurement, 2026-08-25: an edit to this script
    from inside the fence was in force on the very next command.  Now the
    set is bound read-only: a write is EROFS and the mountpoint cannot be
    renamed or removed.

    Verifying this by mutation — dropping a `--ro-bind` from the
    protected loop — is *destructive* when the fence is then down: the
    probe's `mv` succeeds and renames the real script.  Run that on a
    clone, never the tree (measured from outside, 2026-08-26)."""
    protected = sandbox("--protected").stdout.split()
    before = {p: (ROOT / p).read_bytes() for p in protected}
    for p in protected:
        f = ROOT / p
        out = sandbox("env", "LC_ALL=C", "sh", "-c",
                      f"echo x >> '{f}'; mv '{f}' '{f}.away'; rm -f '{f}'; echo rc=$?")
        combined = out.stdout + out.stderr
        assert (ROOT / p).read_bytes() == before[p], (p, combined)
        assert not f.with_name(f.name + ".away").exists(), (p, combined)
        # The write is refused read-only, and that EROFS is the invariant.
        # Read stdout AND stderr together: dash prints a failed `>>`
        # redirection to its own stderr *before* a `2>&1` would apply, so
        # the write's "Read-only file system" lands on stderr, never
        # stdout (gestate-50, 2026-08-26, from Henri's unfenced run).  The
        # mv/rm refusal is carried by the two asserts above — its errno is
        # EROFS or the mountpoint's own EBUSY depending on whether tools/
        # around the file is writable, so it is not asserted on here.
        # LC_ALL=C keeps the words off whoever's locale ran the suite.
        assert ("Read-only file system" in combined
                or "Kirjoitussuojattu" in combined), (p, combined)


@needs_bwrap
def test_the_state_directory_passes_through(tmp_path):
    """The finding of `2026-08-25-reach.md`: without this, a fenced
    session gets a fresh sitting clock."""
    probe = pathlib.Path.home() / ".local" / "state" / "tend" / ".test-sandbox-probe"
    try:
        sandbox("sh", "-c", f'touch "{probe}"')
        assert probe.exists(), "written inside, must be there outside"
    finally:
        probe.unlink(missing_ok=True)


@needs_bwrap
def test_the_network_is_off_and_a_row_turns_it_on():
    off = sandbox("sh", "-c", "timeout 5 getent ahostsv4 example.com")
    assert off.returncode != 0, "off by default"
    if subprocess.run(["timeout", "5", "getent", "ahostsv4", "example.com"],
                      capture_output=True).returncode != 0:
        pytest.skip("no network outside the fence either — the row cannot be shown to work")
    on = sandbox("--reach", "net", "sh", "-c", "timeout 5 getent ahostsv4 example.com")
    assert on.returncode == 0, on.stderr


def test_an_unknown_row_is_refused_out_loud():
    out = sandbox("--reach", "moon", "true")
    assert out.returncode == 2 and "no such row" in out.stderr


def test_nothing_to_run_is_refused_out_loud():
    out = sandbox()
    assert out.returncode == 2 and "nothing to run" in out.stderr


def test_the_launcher_is_in_the_protected_set():
    """`board/resolver.md`, day one, 2026-08-26: the pull is the launch,
    so `node/run.sh` is the one file that applies every program's grant
    — a session editing it changes what a program may reach, which is
    the set's own line one floor down.  Henri: "add node/run.sh to the
    protected set".  No bwrap: this reads `--protected`, a listing.  Red
    until `sandbox.sh` lists it and `fence.sh --protect` has added its
    `Edit` rule."""
    protected = set(sandbox("--protected").stdout.split())
    assert "node/run.sh" in protected, (
        "node/run.sh is the launch path and not in the protected set — apply "
        "protect-run.patch and run tools/fence.sh --protect")


def test_the_state_row_is_two_directories_not_their_parent():
    """`board/keep.md`, the session half, 2026-08-26: measured from the
    fence, a session could read every other tool's state under
    `~/.local/state` — another assistant's prompt history among them —
    though the sitting clock, the ledger and the want live in two
    directories.  The row names those two and not the parent.  No
    bwrap: `--rows` is a listing.  Red until `sandbox.sh` binds
    tend/ and gestate/ instead of the parent — apply state-row.patch."""
    rows = sandbox("--rows").stdout
    state = [l for l in rows.splitlines() if l.split()[1:2] == ["state"]][0]
    assert "~/.local/state/tend" in state and "~/.local/state/gestate" in state, state
    assert "~/.local/state," not in state, "the parent is still the row"


def test_the_trees_row_is_the_other_trees_documents_and_tools():
    """`board/keep.md`, the session half, 2026-08-26: read by purpose,
    a tend session opens the other tree's board, tools, documents — and
    never its source, tests, 3 GB of builds, or .git.  The row names
    the parts and not the tree.  No bwrap: `--rows` is a listing."""
    rows = sandbox("--rows").stdout
    trees = [l for l in rows.splitlines() if l.split()[1:2] == ["trees"]][0]
    assert "board" in trees and "tools" in trees and ".git" in trees, trees
    assert "/gestate  read-only" not in trees, "the whole tree is still the row"


def test_the_tree_row_names_what_it_holds_back():
    """`board/keep.md`, the last bind generalised to any node beside its
    grant (2026-08-26): every node's state and .venv are read-only inside;
    each node's pull file alone passes through.  The row says so.  No
    bwrap: `--rows` is a listing."""
    rows = sandbox("--rows").stdout
    tree = [l for l in rows.splitlines() if l.split()[1:2] == ["tree"]][0]
    assert "every node's state" in tree and ".venv" in tree, tree


def test_the_launcher_is_in_the_protected_set_too():
    """`board/keep.md`/`resolver.md`, the grant beside the program: one
    launcher (`tools/launch.sh`) applies every node's grant, so a session
    editing it changes what any program may reach — the same line as
    node/run.sh.  Red until grant-beside.patch adds it and its Edit rule."""
    assert "tools/launch.sh" in set(sandbox("--protected").stdout.split())


@needs_bwrap
def test_the_node_state_is_read_only_inside_and_the_pull_file_is_not():
    """A session may append a pull and nothing else under node/state; it
    cannot take the runner's lock, so it cannot run the node raw."""
    r = sandbox("sh", "-c", f"touch {ROOT}/node/state/.probe")
    assert r.returncode != 0, "node/state is writable inside"
    r = sandbox("sh", "-c", f": >> {ROOT}/node/state/node.state.pull")
    assert r.returncode == 0, r.stderr
    r = sandbox("sh", "-c", f"exec 9>>{ROOT}/node/state/run.lock")
    assert r.returncode != 0, "the runner's lock is writable inside"
    if (ROOT / ".venv").is_dir():
        r = sandbox("sh", "-c", f"touch {ROOT}/.venv/.probe")
        assert r.returncode != 0, ".venv is writable inside"
