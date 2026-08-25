"""`tools/fence-hook.sh` — every shell command is wrapped, and the dial is
the person's.

Fed the JSON Claude Code hands a `PreToolUse` hook, and checked on what
comes back: nothing (pass through), a rewritten command under
`tools/sandbox.sh`, or a refusal with a reason.  The quoting round-trip
is checked by running the rewritten command and comparing its output to
the plain one — the bug gestate paid for was escapes arriving doubled,
and only running the result shows that.
"""

import json
import os
import pathlib
import shutil
import subprocess

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
HOOK = ROOT / "tools" / "fence-hook.sh"

needs_bwrap = pytest.mark.skipif(
    shutil.which("bwrap") is None or os.environ.get("TEND_FENCED") == "1",
    reason="no bubblewrap here, or already inside the fence — the rewritten command cannot run")


def hook(command, allow=None):
    env = {"PATH": "/usr/bin:/bin", "HOME": str(pathlib.Path.home())}
    if allow is not None:
        env["TEND_REACH_ALLOW"] = allow
    payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": command}})
    out = subprocess.run(["bash", str(HOOK)], input=payload, capture_output=True,
                         text=True, env=env, cwd=ROOT)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout) if out.stdout.strip() else None


def rewritten(command, allow=None):
    return hook(command, allow)["hookSpecificOutput"]["updatedInput"]["command"]


def test_it_parses():
    assert subprocess.run(["bash", "-n", str(HOOK)]).returncode == 0


def test_an_empty_command_passes_through():
    assert hook("") is None


def test_only_the_fences_two_read_only_forms_pass_through():
    assert hook("tools/sandbox.sh --check") is None
    assert hook(f"  {ROOT}/tools/sandbox.sh --rows ") is None


@pytest.mark.parametrize("command", [
    "sh -n tools/sandbox.sh; cat .claude/settings.json",
    "tools/sandbox.sh --check; ls",
    "tools/sandbox.sh --reach net,audio bash -c 'curl example.com'",
    f"{ROOT}/tools/sandbox.sh bash -c 'ls'",
    "echo tools/sandbox.sh",
])
def test_merely_naming_the_fence_does_not_escape_it(command):
    """The first command a session ran under the hook, on 2026-08-25, was
    `sh -n tools/sandbox.sh; ...` and it ran unfenced, because the first
    version skipped anything *containing* the fence's name.  A session
    choosing its own rows by calling the fence directly is the same hole
    from the other side.  All of these are wrapped; the ones that then
    nest fail out loud, which is the right failure."""
    assert rewritten(command).startswith(f"{ROOT}/tools/leash.sh -- {ROOT}/tools/sandbox.sh bash -c ")


def test_everything_else_is_wrapped():
    cmd = rewritten("ls -la")
    assert cmd.startswith(f"{ROOT}/tools/leash.sh -- {ROOT}/tools/sandbox.sh bash -c ")
    assert "--reach" not in cmd


def test_the_leash_wraps_the_fence_and_not_the_other_way(tmp_path):
    """`board/grant.md`, measured 2026-08-25: the budget is a cgroup made
    by the user manager, and a `bus` socket handed *inside* the fence
    lets a fenced session run anything unfenced through that manager —
    an escape, not a dial.  So the scope is made outside, by the hook,
    and the fence runs within it: `leash → sandbox → command`.  The
    ledger's `plain` for every fenced run was the other order."""
    cmd = rewritten("true")
    assert cmd.index("tools/leash.sh") < cmd.index("tools/sandbox.sh")
    assert "bus" not in cmd


@needs_bwrap
@pytest.mark.parametrize("command", [
    "echo hello",
    "printf '%s\\n' \"it's\" '\"q\"' | awk '{print}'",
    "ps -eo args= | awk '/suite\\.py|pytest/ {print \"seen\"}' | head -1; echo done",
    "cd /home/cheery/tend && git log --oneline -1 | cut -d' ' -f1",
])
def test_the_rewritten_command_says_what_the_plain_one_says(command):
    """Quoting survives the round trip, or the fence breaks working
    commands — the failure gestate's first version had."""
    plain = subprocess.run(["bash", "-c", command], capture_output=True, text=True, cwd=ROOT)
    fenced = subprocess.run(["bash", "-c", rewritten(command)], capture_output=True, text=True, cwd=ROOT)
    assert fenced.returncode == plain.returncode
    assert fenced.stdout == plain.stdout


def test_a_row_outside_the_bound_is_refused_with_a_reason():
    out = hook("REACH=net curl https://example.com")["hookSpecificOutput"]
    assert out["permissionDecision"] == "deny"
    assert "`net`" in out["permissionDecisionReason"]
    assert "allowed: none" in out["permissionDecisionReason"]
    assert "updatedInput" not in out, "refused, never silently narrowed"


def test_a_row_inside_the_bound_is_granted_and_named():
    cmd = rewritten("REACH=net getent ahostsv4 example.com", allow="net,audio")
    assert cmd.startswith(f"{ROOT}/tools/leash.sh -- {ROOT}/tools/sandbox.sh --reach net bash -c ")
    assert "REACH=" not in cmd, "the prefix is consumed, not passed into the fence"


def test_every_requested_row_must_be_in_the_bound():
    out = hook("REACH=net,audio tools/andon.sh", allow="net")["hookSpecificOutput"]
    assert out["permissionDecision"] == "deny" and "`audio`" in out["permissionDecisionReason"]


def test_there_is_no_nofence():
    assert "NOFENCE" not in HOOK.read_text(encoding="utf-8").split("set -euo pipefail")[1]
    assert rewritten("NOFENCE=1 ls").startswith(f"{ROOT}/tools/leash.sh -- {ROOT}/tools/sandbox.sh")
