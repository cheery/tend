"""`tools/fence.sh` — the deny-list is in force, or something says it is not.

The measurement that paid for this (`board/fence.md`, 2026-08-25): from
inside a tend session, `python3 -c` rewrote `.claude/settings.json` and
`mv` made it vanish, and nothing noticed.  So the check is "break it
and watch it notice", each way the file was seen to break: a rule gone,
the file gone, the file unparseable, a hook gone.

Nothing here touches the real settings file: every test runs in a
throwaway git repository holding a copy of it.  The one exception is
the last test, which runs the check against this clone — and is red
until the hook line is installed, which is the finding, not a broken
test (`test_precommit.py` takes the same stance).
"""

import json
import os
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
FENCE = ROOT / "tools" / "fence.sh"
SETTINGS = ROOT / ".claude" / "settings.json"
HOOK_LINE = '"$CLAUDE_PROJECT_DIR"/tools/fence.sh --hook'


def settings_with_fence_hook():
    """This clone's real settings, with the fence's own hook line ensured —
    so the fixture is what the tree looks like once the line is in."""
    d = json.loads(SETTINGS.read_text(encoding="utf-8"))
    hooks = d["hooks"]["UserPromptSubmit"][0]["hooks"]
    if not any("tools/fence.sh --hook" in h["command"] for h in hooks):
        hooks.append({"type": "command", "command": HOOK_LINE})
    return d


class Repo:
    def __init__(self, tmp_path):
        self.at = tmp_path
        self.file = tmp_path / ".claude" / "settings.json"
        subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
        (tmp_path / "tools").mkdir()
        (tmp_path / "tools" / "fence.sh").write_text(FENCE.read_text(encoding="utf-8"))
        self.file.parent.mkdir()
        self.write(settings_with_fence_hook())
        for a in (["add", "."], ["commit", "-q", "-m", "fence"]):
            subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *a],
                           cwd=tmp_path, check=True)

    def write(self, d):
        self.file.write_text(json.dumps(d, indent=2) + "\n", encoding="utf-8")

    def edit(self, f):
        d = json.loads(self.file.read_text(encoding="utf-8"))
        f(d)
        self.write(d)

    def fence(self, *args):
        return subprocess.run(["sh", "tools/fence.sh", *args], cwd=self.at,
                              capture_output=True, text=True, input="{}")

    def at_head(self):
        return subprocess.run(["git", "diff", "--quiet", "HEAD", "--", ".claude/settings.json"],
                              cwd=self.at).returncode == 0


def drop_rule(rule):
    return lambda d: d["permissions"]["deny"].remove(rule)


def drop_hook(name):
    def f(d):
        hs = d["hooks"]["UserPromptSubmit"][0]["hooks"]
        hs[:] = [h for h in hs if name not in h["command"]]
    return f


def test_it_parses():
    assert subprocess.run(["sh", "-n", str(FENCE)]).returncode == 0


def test_the_committed_file_is_up(tmp_path):
    out = Repo(tmp_path).fence()
    assert out.returncode == 0, out.stdout + out.stderr
    assert "the fence is up" in out.stdout


def test_one_rule_removed_is_red_and_named(tmp_path):
    """The demonstration `board/fence.md` asks for: a settings file with
    one rule removed, and the check going red on it."""
    r = Repo(tmp_path)
    r.edit(drop_rule("Bash(sudo:*)"))
    out = r.fence()
    assert out.returncode == 1
    assert "Bash(sudo:*) — MISSING" in out.stdout
    assert "THE FENCE IS DOWN" in out.stdout


def test_the_edit_rule_is_load_bearing(tmp_path):
    r = Repo(tmp_path)
    r.edit(drop_rule("Edit(./.claude/**)"))
    assert "Edit(./.claude/**) — MISSING" in r.fence().stdout


def test_the_file_missing_is_red_and_restore_puts_it_back(tmp_path):
    """`mv` went through on 2026-08-25.  A missing file is every rule off."""
    r = Repo(tmp_path)
    r.file.unlink()
    out = r.fence()
    assert out.returncode == 1 and "MISSING" in out.stdout
    out = r.fence("--restore")
    assert out.returncode == 0, out.stdout + out.stderr
    assert "restored" in out.stdout and r.at_head()


def test_the_file_malformed_is_red_and_restore_puts_it_back(tmp_path):
    r = Repo(tmp_path)
    r.file.write_text("{ not json\n")
    out = r.fence()
    assert out.returncode == 1 and "not valid JSON" in out.stdout
    assert r.fence("--restore").returncode == 0 and r.at_head()


def test_restore_leaves_a_weakened_file_that_parses(tmp_path):
    """A file that parses might be an edit in progress; reverting it
    silently would destroy that.  `--force` is how you say you meant it."""
    r = Repo(tmp_path)
    r.edit(drop_rule("Bash(git push:*)"))
    out = r.fence("--restore")
    assert out.returncode == 1
    assert "not reverting" in out.stdout and "--force" in out.stdout
    assert not r.at_head(), "left alone"
    assert r.fence("--force").returncode == 0 and r.at_head()


def test_a_hook_removed_is_red(tmp_path):
    """Hook config is enforcement here (`board/cords.md`): the lamp, the
    sitting limit and this check are each one line a session could drop."""
    r = Repo(tmp_path)
    r.edit(drop_hook("limit.sh"))
    out = r.fence()
    assert out.returncode == 1
    assert "tools/limit.sh --hook is not on UserPromptSubmit" in out.stdout


def test_the_two_spellings_of_home_are_one_rule(tmp_path):
    """`~/.ssh/**` and `//home/you/.ssh/**` are both in force; matching
    raw strings made gestate's check cry wolf on 2026-08-24."""
    r = Repo(tmp_path)
    home = os.environ["HOME"]

    def respell(d):
        deny = d["permissions"]["deny"]
        deny[deny.index("Read(~/.ssh/**)")] = f"Read(/{home}/.ssh/**)"
    r.edit(respell)
    assert r.fence().returncode == 0


def test_the_hook_form_is_silent_when_up(tmp_path):
    out = Repo(tmp_path).fence("--hook")
    assert out.returncode == 0 and out.stdout == ""


def test_the_hook_form_speaks_when_down_and_never_refuses(tmp_path):
    r = Repo(tmp_path)
    r.edit(drop_rule("Read(~/.ssh/**)"))
    out = r.fence("--hook")
    assert out.returncode == 0, "a lamp, never a refusal"
    assert "🔴 fence" in out.stdout and "Read(~/.ssh/**) — MISSING" in out.stdout


def test_the_hook_form_restores_what_is_safe_to_restore(tmp_path):
    r = Repo(tmp_path)
    r.file.unlink()
    out = r.fence("--hook")
    assert out.returncode == 0 and "restored" in out.stdout
    assert r.at_head()


def test_outside_a_checkout_restore_says_so(tmp_path):
    (tmp_path / "tools").mkdir()
    (tmp_path / "tools" / "fence.sh").write_text(FENCE.read_text(encoding="utf-8"))
    out = subprocess.run(["sh", "tools/fence.sh", "--restore"], cwd=tmp_path,
                         capture_output=True, text=True)
    assert out.returncode == 3 and "not a git checkout" in out.stderr


def test_an_unknown_argument_is_refused_out_loud(tmp_path):
    assert Repo(tmp_path).fence("--bogus").returncode == 2


def test_the_fence_is_up_in_this_clone():
    """Red until `.claude/settings.json` carries the fence's own hook
    line — an edit that is Henri's, because hook config is enforcement.
    The line, as jq:

        jq '.hooks.UserPromptSubmit[0].hooks += [{"type":"command",
            "command":"\\"$CLAUDE_PROJECT_DIR\\"/tools/fence.sh --hook"}]' \\
            .claude/settings.json > .claude/settings.json.new \\
            && mv .claude/settings.json.new .claude/settings.json
    """
    out = subprocess.run(["sh", str(FENCE)], cwd=ROOT, capture_output=True, text=True)
    assert out.returncode == 0, out.stdout
