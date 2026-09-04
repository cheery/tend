"""`tools/meter.py` — the tree's counts by week, read from files, never from prose.

The fixture is a tree of its own: four kaizens across two ISO weeks,
an ingestion table that has read two of them, an open F-number and a
resolved one, an open card and a done one, a failure ledger with a
`shake` line that must not count, and a two-commit git so the day an
F-number's file arrived is git's word and not the entry's.  Each column
is read back once, and the seam this file exists for is the difference
between *not counted* and *zero*: a kaizen whose `Wrong, mine` opens
with prose is the footer's line, not a 0 in the table.
"""

import os
import pathlib
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
METER = ROOT / "tools" / "meter.py"


def git(root, *args, day=None):
    env = dict(os.environ)
    if day:
        env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = f"{day}T10:00:00+03:00"
    subprocess.run(["git", "-C", str(root), *args], check=True, env=env,
                   capture_output=True)


@pytest.fixture
def tree(tmp_path):
    root = tmp_path / "tree"
    kz = root / "doc" / "kaizen"
    kz.mkdir(parents=True)
    (kz / "2026-08-24-1000.md").write_text(
        "# Kaizen\n\n**Wrong, mine.**  Two.  The first was a heredoc; the\n"
        "second a tail.\n\n**Tomorrow.**  His pick.\n\nhenri: 4 — a good sitting\n")
    (kz / "2026-08-25-0900.md").write_text(
        "# Kaizen\n\n**Wrong, mine, in order of cost.**  (1) A clock read late.\n"
        "(2) A number in prose.  (3) A fixture copied live.\n")
    (kz / "2026-08-26-0900.md").write_text(
        "# Kaizen\n\n**Wrong, mine.**  The task was too easy for the question,\n"
        "and he saw it first.\n")
    (kz / "2026-09-01-0800.md").write_text(
        "# Kaizen\n\n**Wrong, mine.**  None caught by a fence.  One in judgement.\n")
    (root / "doc" / "ingested.md").write_text(
        "# Ingested\n\n| kaizen | the lesson | verdict |\n|---|---|---|\n"
        "| 2026-08-24-1000 | a heredoc again | `recurs` — [[x]] |\n"
        "| 2026-08-25-0900 | the clock | `once` |\n")
    fx = root / "fixme"
    (fx / "resolved").mkdir(parents=True)
    (fx / "F000.md").write_text(
        "# F000\n\n    status     open\n    shows      a thing\n"
        "    seen       2026-08-25, by hand\n")
    (fx / "F001.md").write_text(
        "# F001\n\n    status     open\n    shows      a thing\n"
        "    seen       2026-08-24\n")
    bd = root / "board"
    (bd / "done").mkdir(parents=True)
    (bd / "later").mkdir()
    (bd / "README.md").write_text(
        "# board\n\n**A rule.**  Sessions do this.\n"
        "*(self-shaped, 2026-08-24 — a session wrote this rule about sessions.\n"
        "henri: approved 2026-08-26)*\n\n"
        "**Another.**  Left standing.\n"
        "*(self-shaped, 2026-08-27 — a session wrote this one too.)*\n")
    (bd / "x.md").write_text(
        "# x\n\n    status   open\n    because  a problem\n"
        "    asked    Henri, 2026-08-24 — \"card it\"\n\n"
        "*(question, his call — which of the two, and why?)*\n")
    (bd / "done" / "y.md").write_text(
        "# y\n\n    status   done — 2026-08-26\n    because  a problem\n"
        "    asked    Henri, 2026-08-24 — \"card it\"\n")
    (bd / "later" / "z.md").write_text(
        "# z\n\n    status   shelved — 2026-08-27\n    because  a problem\n"
        "    asked    Henri, 2026-08-27 — \"later\"\n")
    (tmp_path / "failed.log").write_text(
        "2026-08-25 10:00  gate  test/test_a.py::test_one  load 1.0  wall 1.0s\n"
        "2026-08-26 10:00  hand  test/test_a.py::test_one  load 1.0  wall 1.0s\n"
        "2026-08-26 10:05  shake  test/test_a.py::test_one  load 9.0  wall 1.0s\n"
        "2026-09-02 10:00  gate  test/test_b.py::test_two  load 1.0  wall 1.0s\n")
    git(root, "init", "-q")
    git(root, "add", "doc", "board", "fixme/F000.md", "fixme/F001.md")
    git(root, "commit", "-q", "-m", "one", day="2026-08-24")
    # F001 resolves on 08-26 and moves shelf: its arrival stays 08-24, the
    # earliest add across both paths, which is the seam the git read is for.
    (fx / "F001.md").rename(fx / "resolved" / "F001.md")
    (fx / "resolved" / "F001.md").write_text(
        "# F001\n\n    status     resolved — 2026-08-26: gated\n    shows      a thing\n"
        "    seen       2026-08-24\n    gate       test_x.py::test_y\n")
    git(root, "add", "-A", "fixme")
    git(root, "commit", "-q", "-m", "two", day="2026-08-26")
    return root


def meter(root, *args):
    return subprocess.run([sys.executable, str(METER), "--root", str(root), *args],
                          capture_output=True, text=True)


def row(out, key):
    for line in out.splitlines():
        if line.startswith(f"| {key} |"):
            return [c.strip() for c in line.strip("|").split("|")]
    raise AssertionError(f"no row for {key} in:\n{out}")


def test_it_parses():
    assert subprocess.run([sys.executable, "-m", "py_compile", str(METER)]).returncode == 0


def test_the_first_week_reads_every_column_from_a_file(tree):
    out = meter(tree)
    print(out.stdout)   # shown whole on a red — pytest's assertion repr cuts the table
    assert out.returncode == 0, out.stderr
    week = row(out.stdout, "2026-08-24")
    assert week[1:] == [
        "3",                 # sittings: three kaizen files that week
        "2",                 # commits: both, by author date
        "5 (2 read)",        # wrong: Two + (1)(2)(3); the prose one is not read
        "1 of 2",            # recurs: two ingested, one `recurs`
        "+2 −1 (2 d)",       # F000 arrived 08-24 by git (not `seen`'s 08-25); F001 08-24 → 08-26
        "+3 −1 (2 d)",       # x and y asked 08-24, z 08-27 (a shelf is not a close); y done 08-26
        "1/1",               # one gate red, one hand red; the shake is left out
        "+3 −1 (2 d)",       # two marks by their own dates (08-24 struck 08-26, 08-27 standing) and a
                             # question with no date, placed by git's blame of its line (08-24)
        "4.0",               # his line
    ]
    assert "for him: 2 waiting for his hand, the oldest since 2026-08-24 (board/x.md:7)" in out.stdout


def test_a_paragraph_that_opens_with_prose_is_not_counted_and_not_zero(tree):
    out = meter(tree).stdout
    assert "1 of 4 kaizens have no `Wrong, mine` paragraph that opens with a count" in out
    week = row(out, "2026-08-31")
    assert week[3] == "0 (1 read)", "`None caught by a fence` is a zero, read from the first word"
    assert week[4] == "·", "nothing in that week has been ingested"
    assert week[9] == "·", "no henri line is a blank, never a number"
    assert week[8] == "+0 −0", "nothing was placed for him or struck that week"
    assert "2 of 4 kaizens have no verdict" in out


def test_the_second_week_holds_the_shelved_card_and_its_own_red(tree):
    week = row(meter(tree).stdout, "2026-08-31")
    assert week[1:3] == ["1", "0"]
    assert week[6] == "+0 −0", "a shelved card is neither opened nor done that week"
    assert week[7] == "1/0"
    day = row(meter(tree, "--by", "day").stdout, "2026-08-27")
    assert day[6] == "+1 −0", "by day, z's `asked` counts on its own date"


def test_by_day_gives_a_row_per_date(tree):
    out = meter(tree, "--by", "day").stdout
    assert row(out, "2026-08-25")[1:4] == ["1", "0", "3 (1 read)"]
    assert row(out, "2026-08-26")[7] == "0/1", "the shake line on 08-26 is not a hand red"
    assert row(out, "2026-08-24")[5] == "+2 −0", (
        "both F-numbers arrived 08-24 by git's word; F000's `seen` says 08-25 and is not asked")
    assert row(out, "2026-08-26")[5] == "+0 −1 (2 d)", "F001's move to resolved/ is not a second arrival"


def test_the_tree_itself_has_a_first_week():
    out = meter(ROOT)
    assert out.returncode == 0, out.stderr
    first = row(out.stdout, "2026-08-24")
    assert int(first[1]) >= 60, "the first week had sixty-odd sittings"
    assert "no-verify" in out.stdout
