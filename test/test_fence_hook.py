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
import pathlib
import shutil
import subprocess

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
HOOK = ROOT / "tools" / "fence-hook.sh"

needs_bwrap = pytest.mark.skipif(shutil.which("bwrap") is None,
                                 reason="no bubblewrap here — the rewritten command cannot run")


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


def test_a_command_already_under_the_fence_passes_through():
    assert hook("tools/sandbox.sh --check") is None
    assert hook(f"{ROOT}/tools/sandbox.sh bash -c 'ls'") is None


def test_everything_else_is_wrapped():
    cmd = rewritten("ls -la")
    assert cmd.startswith(f"{ROOT}/tools/sandbox.sh bash -c ")
    assert "--reach" not in cmd


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
    assert cmd.startswith(f"{ROOT}/tools/sandbox.sh --reach net bash -c ")
    assert "REACH=" not in cmd, "the prefix is consumed, not passed into the fence"


def test_every_requested_row_must_be_in_the_bound():
    out = hook("REACH=net,audio tools/andon.sh", allow="net")["hookSpecificOutput"]
    assert out["permissionDecision"] == "deny" and "`audio`" in out["permissionDecisionReason"]


def test_there_is_no_nofence():
    assert "NOFENCE" not in HOOK.read_text(encoding="utf-8").split("set -euo pipefail")[1]
    assert rewritten("NOFENCE=1 ls").startswith(f"{ROOT}/tools/sandbox.sh")
