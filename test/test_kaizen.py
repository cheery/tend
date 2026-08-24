"""`tools/kaizen.sh` — the lamp that says a session is not over.

Henri, 2026-08-24, after the session had said "packed up" twice:
*"you forget kaizen!  it's big thing to do after each session."*  The
session had done it once, when told.  A practice done only when told is
a wish, so the reminder is a mechanism, and this is its test.
"""

import datetime
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
LAMP = ROOT / "tools" / "kaizen.sh"


def scratch(tmp_path, commits=1):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / "tools").mkdir()
    (tmp_path / "tools" / "kaizen.sh").write_text(LAMP.read_text(encoding="utf-8"))
    for i in range(commits):
        (tmp_path / f"f{i}").write_text("x\n")
        subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t",
                        "add", "."], cwd=tmp_path, check=True)
        subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t",
                        "commit", "-q", "-m", f"c{i}"], cwd=tmp_path, check=True)
    return lambda *a: subprocess.run(["sh", "tools/kaizen.sh", *a], cwd=tmp_path,
                                     capture_output=True, text=True, input="{}")


def test_it_parses():
    assert subprocess.run(["sh", "-n", str(LAMP)]).returncode == 0


def test_commits_today_and_no_kaizen_lights_the_lamp(tmp_path):
    r = scratch(tmp_path, commits=3)()
    assert r.returncode == 0, "a lamp, never a refusal"
    assert "3 commit(s) today" in r.stdout
    assert datetime.date.today().isoformat() in r.stdout


def test_a_written_kaizen_puts_it_out(tmp_path):
    run = scratch(tmp_path, commits=2)
    today = datetime.date.today().isoformat()
    (tmp_path / "doc" / "kaizen").mkdir(parents=True)
    (tmp_path / "doc" / "kaizen" / f"{today}.md").write_text("# done\n")
    assert run().stdout == ""


def test_a_day_with_no_commits_says_nothing(tmp_path):
    assert scratch(tmp_path, commits=0)().stdout == ""


def test_the_hook_form_reaches_the_session(tmp_path):
    """On UserPromptSubmit, stdout is added to the session's context —
    so the lamp's line is what the session reads, and exit 0 is what
    keeps the prompt flowing."""
    r = scratch(tmp_path, commits=1)("--hook")
    assert r.returncode == 0
    assert "kaizen" in r.stdout


def test_an_unknown_argument_is_refused_out_loud(tmp_path):
    r = scratch(tmp_path, commits=0)("--bogus")
    assert r.returncode == 2
