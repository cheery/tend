"""`tools/kaizen.sh` — the lamp that says a session is not over.

Henri, 2026-08-24, after the session had said "packed up" twice:
*"you forget kaizen!  it's big thing to do after each session."*  The
session had done it once, when told.  A practice done only when told is
a wish, so the reminder is a mechanism, and this is its test.

And the same evening, on the first version's per-day count: *"I do
several sessions in a day."*  So the measure is commits since the last
kaizen, which is what these check.
"""

import os
import pathlib
import subprocess
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
LAMP = ROOT / "tools" / "kaizen.sh"


class Repo:
    def __init__(self, tmp_path):
        self.at = tmp_path
        subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
        (tmp_path / "tools").mkdir()
        (tmp_path / "tools" / "kaizen.sh").write_text(LAMP.read_text(encoding="utf-8"))
        self.n = 0

    def commit(self, path="work"):
        self.n += 1
        f = self.at / path / f"f{self.n}.md" if path != "work" else self.at / f"f{self.n}"
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text("x\n")
        for a in (["add", "."], ["commit", "-q", "-m", f"c{self.n}"]):
            subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *a],
                           cwd=self.at, check=True)

    def kaizen(self):
        self.commit("doc/kaizen")

    def lamp(self, *args):
        env = dict(os.environ, TEND_KAIZEN_WANT=str(self.at / "wanted"))
        return subprocess.run(["sh", "tools/kaizen.sh", *args], cwd=self.at, env=env,
                              capture_output=True, text=True, input="{}")


def test_a_session_may_say_it_wants_one(tmp_path):
    """**Henri, 2026-08-24:** *"you should have a way to tell when you
    want another kaizen."*  Not a judgement about owing one — a
    declaration, with a reason, and the lamp carries the reason."""
    r = Repo(tmp_path)
    r.commit(); r.kaizen()                       # nothing uncovered
    assert r.lamp().stdout == ""
    assert r.lamp("want", "the leash design changed under me").returncode == 0
    out = r.lamp().stdout
    assert "kaizen wanted" in out
    assert "the leash design changed under me" in out
    assert "the sitting is not over" in out


def test_a_want_is_answered_by_the_next_kaizen(tmp_path):
    r = Repo(tmp_path)
    r.commit(); r.kaizen()
    r.lamp("want", "something to say")
    time.sleep(1.1)                               # commit time is whole seconds
    r.kaizen()
    assert r.lamp().stdout == ""
    assert not (r.at / "wanted").exists(), "and forgotten, not just muted"


def test_a_want_needs_a_reason(tmp_path):
    r = Repo(tmp_path)
    out = r.lamp("want")
    assert out.returncode == 2
    assert "say why" in out.stderr


def test_it_parses():
    assert subprocess.run(["sh", "-n", str(LAMP)]).returncode == 0


def test_commits_with_no_kaizen_ever_light_the_lamp(tmp_path):
    r = Repo(tmp_path)
    r.commit(); r.commit(); r.commit()
    out = r.lamp()
    assert out.returncode == 0, "a lamp, never a refusal"
    assert "3 commit(s) and no kaizen yet" in out.stdout


def test_a_kaizen_puts_it_out(tmp_path):
    r = Repo(tmp_path)
    r.commit(); r.commit()
    r.kaizen()
    assert r.lamp().stdout == ""


def test_the_next_session_lights_it_again(tmp_path):
    """**Several sessions in a day.**  The second session's first commit
    is work the last kaizen does not cover, whatever the date says."""
    r = Repo(tmp_path)
    r.commit(); r.kaizen()
    r.commit()
    out = r.lamp().stdout
    assert "1 commit(s) since the last kaizen" in out
    began = subprocess.run(["git", "log", "-1", "--format=%cd", "--date=format:%F-%H%M"],
                           cwd=r.at, capture_output=True, text=True).stdout.strip()
    assert f"doc/kaizen/{began}.md" in out, \
        "the file is named by when the session began — its first uncovered commit"


def test_an_empty_repository_says_nothing(tmp_path):
    assert Repo(tmp_path).lamp().stdout == ""


def test_the_hook_form_reaches_the_session(tmp_path):
    """On UserPromptSubmit, stdout is added to the session's context —
    so the lamp's line is what the session reads, and exit 0 is what
    keeps the prompt flowing."""
    r = Repo(tmp_path)
    r.commit()
    out = r.lamp("--hook")
    assert out.returncode == 0
    assert "kaizen" in out.stdout


def test_an_unknown_argument_is_refused_out_loud(tmp_path):
    assert Repo(tmp_path).lamp("--bogus").returncode == 2
