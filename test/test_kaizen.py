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

    def commit(self, path="work", when=None):
        """`when` is an epoch: the commit's date, so two commits can be a
        minute apart without waiting a minute."""
        self.n += 1
        f = self.at / path / f"f{self.n}.md" if path != "work" else self.at / f"f{self.n}"
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text("x\n")
        env = dict(os.environ)
        if when is not None:
            env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = f"@{when} {time.strftime('%z')}"
        for a in (["add", "."], ["commit", "-q", "-m", f"c{self.n}"]):
            subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *a],
                           cwd=self.at, env=env, check=True)

    def kaizen(self, when=None):
        """A real kaizen: a file named in the `<date>-<HHMM>.md` shape the
        lamp matches (board/green.md's fix), not just any file in the dir."""
        self.n += 1
        f = self.at / "doc" / "kaizen" / f"2026-08-26-{self.n:04d}.md"
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text("k\n")
        env = dict(os.environ)
        if when is not None:
            env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = f"@{when} {time.strftime('%z')}"
        for a in (["add", "."], ["commit", "-q", "-m", f"k{self.n}"]):
            subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *a],
                           cwd=self.at, env=env, check=True)

    def stray(self, name):
        """A non-kaizen file committed into doc/kaizen/ — the thing that
        must not be read as a kaizen landing."""
        self.n += 1
        f = self.at / "doc" / "kaizen" / name
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text("not a kaizen\n")
        for a in (["add", "."], ["commit", "-q", "-m", f"s{self.n}"]):
            subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *a],
                           cwd=self.at, check=True)

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


def test_a_non_kaizen_file_in_the_dir_is_not_a_kaizen(tmp_path):
    """**The defect of 2026-08-26 (board/green.md, and this session).**

    The lamp finds the last kaizen by the *directory* — the newest
    commit touching doc/kaizen/ — so a non-kaizen file committed there
    (a ledger, a README, an archive index) is read as a kaizen landing
    and the lamp goes dark with a real kaizen still owed.  It happened:
    committing doc/kaizen/ingested.md put the lamp out an hour after the
    session had broken this very lamp twelve ways in a copy.  The lamp
    must match a kaizen's *name*, not its directory.
    """
    r = Repo(tmp_path)
    r.commit(); r.kaizen()        # a real kaizen covers the first work
    r.commit()                    # new uncovered work: the lamp is lit
    r.stray("ingested.md")        # a non-kaizen file lands in doc/kaizen/
    out = r.lamp().stdout
    assert "since the last kaizen" in out, \
        "a non-kaizen file in doc/kaizen/ was read as the last kaizen"
    assert "2 commit(s)" in out, \
        "the stray is not a kaizen, so the work after the real one still owes one"


def test_the_next_session_lights_it_again(tmp_path):
    """**Several sessions in a day.**  The second session's first commit
    is work the last kaizen does not cover, whatever the date says."""
    r = Repo(tmp_path)
    r.commit(); r.kaizen()
    first = int(time.time()) - 120
    r.commit(when=first); r.commit()
    out = r.lamp().stdout
    assert "2 commit(s) since the last kaizen" in out
    began = time.strftime("%Y-%m-%d-%H%M", time.localtime(first))
    assert f"doc/kaizen/{began}.md" in out, \
        "the file is named by when the session began — its first uncovered commit"
    # Two commits, a minute apart, on purpose: with one, first and last
    # are the same commit and the lamp could name the wrong one and pass
    # — which it did, in `board/green.md`'s measurement of 2026-08-26.


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


def test_the_lamp_says_one_per_sitting_not_per_session(tmp_path):
    """**2026-08-27, doc/reading-2026-08-27.md**: 39 kaizens for 14
    sittings on 08-26, because every session read "the sitting is not
    over" as its own.  The line now says the unit, every time it lights."""
    r = Repo(tmp_path)
    r.commit()
    out = r.lamp().stdout
    assert "one per sitting, not per session" in out and "write it when the sitting ends" in out, out
    r.lamp("want", "because")
    assert "one per sitting, not per session" in r.lamp().stdout


def test_the_lamp_reads_the_desks_clock_when_there_is_one(tmp_path):
    """The clock is `tools/limit.sh`'s (its own tests are test_limit.py);
    the lamp only repeats what it says — and says *now* when it says
    closed.  Without a clock beside it the line still names the unit."""
    r = Repo(tmp_path)
    r.commit()
    clock = tmp_path / "tools" / "limit.sh"
    clock.write_text("#!/bin/sh\necho 'sitting  started 05:20, 33m in, 27m left of 60'\n")
    assert "27m left of 60" in r.lamp().stdout
    clock.write_text("#!/bin/sh\necho 'sitting  closed at 05:50 — the thing you came for is done'\n")
    out = r.lamp().stdout
    assert "the sitting is closed" in out and "write it now" in out, out
