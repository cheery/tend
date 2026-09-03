"""The self-shaped mark, and whether Henri's approval still covers the words he read.

`manifesto.md` §"How a practice gets adopted" carries Henri's rule of
2026-09-01: *a rule about sessions, drafted by a session, says so until
Henri strikes the mark.*  The mark is a parenthetical where the rule
ends, and he strikes it by writing into it — `henri: approved <date>` —
rather than deleting it, so the record keeps both halves.

**Why the date, and why this file exists.**  An approval is a claim
about a *specific text*, and until this gate nothing bound the two.
Edit an approved rule tomorrow and the approval transfers silently onto
words he never read.  That matters more here than anywhere else in the
tree, because the danger the rule names is a session optimising inside a
boundary it did not set — and editing an already-approved rule is the
cheapest possible way to do exactly that.  It is `F008`'s shape: a value
and the thing it describes drifting apart with nothing going red.

So: **editing an approved rule un-approves it.**  The approval means "he
read these words", and it stops meaning that the moment the words change.

**Three verdicts, not two** (`board/README.md` §"What the days taught").
A mark is fresh, or stale, or *its rule's extent cannot be determined* —
and the third is red with a different sentence, because a heuristic that
guesses when it does not know is `manifesto.md`'s first way an
instrument fails.  The extent is found by scanning up from the mark to
the nearest blank line whose next line opens with a bold lead (`**`),
which is how every rule in this tree is written.  It resolves all four
marks standing on 2026-09-01; a rule written otherwise gets the third
verdict and a request to say its own range, never a wrong answer.

**What this gate does not cover**, named rather than discovered later:

- **Day granularity.**  He writes a date, not a timestamp, so a rule
  edited later on its own approval day passes.  The alternative is
  asking him to type a clock time, which is a worse trade.
- **A rule with no bold lead** gets the third verdict, not a pass.
- **A mark whose text he rewrites himself.**  This gate reads the tree
  as it is; his hand is the authority it defers to, not one it audits.
"""

from __future__ import annotations

import datetime
import re
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent

#: Where a mark may stand.  **Every root document, not a list of them**
#: — the first version named `manifesto.md` alone, and `keeper.md` was
#: written with a mark in it an hour later and was invisible to this
#: gate.  A search that enumerates its own subjects goes stale the first
#: time somebody adds one; a search that takes the whole shelf does not.
SEARCHED_DIRS = ("board", "spec", "doc")

#: The mark opens flush left with its bracket.  The bracket and the
#: anchor were both chosen by measurement, 2026-09-01: the bare words
#: name the strand itself in two dozen places across the ledger.
OPENS = re.compile(r"^\*\(self-shaped\b")

#: Henri's verdict, lowercase.  `Henri:` capitalised is the tree's
#: attribution form and appears 127 times; `henri:` is him speaking.
VERDICT = re.compile(r"\bhenri:\s*(.+?)\s*\)?\*?\s*$")

#: An approval carries the date he read the words.
APPROVED = re.compile(r"^approved\s+(\d{4}-\d{2}-\d{2})\b")

#: How far up a rule may reasonably run before the extent is a guess.
REACH = 80

#: The fixtures' rule, in a subdirectory, because every real mark but one
#: is in `board/` and a fixture at the root modelled a case that does not
#: exist.  A decoy of the same basename sits at the fixture's root.
RULE = "board/d.md"


class Mark:
    """One mark, its verdict, and the lines of the rule it stands under."""

    def __init__(self, path: Path, lines: list[str], start: int, end: int):
        self.path, self.start, self.end = path, start, end
        self.text = "\n".join(lines[start:end + 1])
        self.rule_start = self._rule_start(lines)

    @property
    def where(self) -> str:
        try:
            where = self.path.relative_to(ROOT)
        except ValueError:
            where = self.path          # a fixture's tree, not this one
        return f"{where}:{self.start + 1}"

    def _rule_start(self, lines: list[str]) -> int | None:
        """Scan up for the blank line whose successor opens a rule.

        Returns a 0-based line index, or None for the third verdict.
        """
        for i in range(self.start - 1, max(-1, self.start - REACH) - 1, -1):
            if not lines[i].strip() and lines[i + 1].startswith("**"):
                return i + 1
        return None

    @property
    def verdict(self) -> str | None:
        found = VERDICT.search(self.text)
        return found.group(1) if found else None

    @property
    def approved_on(self) -> datetime.date | None:
        said = self.verdict
        if not said:
            return None
        found = APPROVED.match(said)
        if not found:
            return None
        return datetime.date.fromisoformat(found.group(1))


def _files() -> list[Path]:
    out: list[Path] = sorted(ROOT.glob("*.md"))
    for name in SEARCHED_DIRS:
        out += sorted((ROOT / name).rglob("*.md"))
    return [p for p in out if p.is_file()]


def marks() -> list[Mark]:
    """Every mark in the tree, read from the working copy."""
    out = []
    for path in _files():
        lines = path.read_text(encoding="utf-8").splitlines()
        for i, line in enumerate(lines):
            if not OPENS.match(line):
                continue
            end = i
            while end < len(lines) and ")*" not in lines[end]:
                end += 1
            out.append(Mark(path, lines, i, min(end, len(lines) - 1)))
    return out


class GitCannotSay(Exception):
    """git refused the question, so the gate has no verdict — never a pass.

    This class exists because its absence was a live defect for the first
    twenty minutes of this file: `_git` returned `""` on a non-zero exit,
    `rule_last_touched` turned that into `None`, and the assertion read
    `None` as "nothing to worry about".  See the docstring of
    `test_git_refusing_the_question_is_never_a_pass`.
    """


def _git(*args: str, cwd: Path = ROOT) -> str:
    done = subprocess.run(("git",) + args, cwd=cwd,
                          capture_output=True, text=True)
    if done.returncode != 0:
        raise GitCannotSay(" ".join(("git",) + args) + " → "
                           + (done.stderr.strip() or "no output"))
    return done.stdout


def rule_last_touched(path: Path, a: int, b: int,
                      cwd: Path = ROOT) -> datetime.date | None:
    """When lines a..b (1-based, inclusive) were last committed.

    `git log -L` follows the range through history, so this is the rule's
    own last edit and not the file's — which is the whole point: adding
    or answering a mark never touches the lines above it.

    **The path git is given must be relative to the repository**, not the
    basename.  The first draft passed `path.name`, so `board/README.md`
    became `README.md` — and this tree has one of those at its root, 103
    lines long, so git answered `fatal: file README.md has only 103 lines`
    and the swallowed error read as "no edits found".  All three board
    marks were being checked by nothing.  Now `_git` raises instead.

    **And the lines git is given are HEAD's, not the working tree's**
    (F021).  `git log -L` reads the committed file, so when an uncommitted
    edit above the rule has shifted it — 66 lines moved on 2026-09-03
    morning, 120 in the evening — a..b names some other paragraph in
    HEAD, and the gate reported that paragraph's date as the rule's.
    `rule_dirty` has already said no hunk crosses a..b, so every hunk is
    wholly above or below; the ones above are the shift, and a..b is
    moved back by it before git is asked.
    """
    at = path.resolve().relative_to(cwd.resolve())
    a, b = head_lines(path, a, b, cwd)
    out = _git("log", "-1", "--format=%cI", f"-L{a},{b}:{at}", cwd=cwd)
    for line in out.splitlines():
        if line.strip():
            return datetime.datetime.fromisoformat(line.strip()).date()
    return None


def head_lines(path: Path, a: int, b: int, cwd: Path = ROOT) -> tuple[int, int]:
    """Working-tree lines a..b as HEAD numbers them: shifted back by every
    uncommitted hunk that lies wholly above them (F021).  A hunk that
    crosses a..b is `rule_dirty`'s to refuse, and it is asked first."""
    out = _git("diff", "HEAD", "-U0", "--", str(path), cwd=cwd)
    shift = 0
    for line in out.splitlines():
        if not line.startswith("@@"):
            continue
        found = re.search(r"-(\d+)(?:,(\d+))?\s+\+(\d+)(?:,(\d+))?", line)
        if not found:
            continue
        old_count = int(found.group(2) or 1)
        new_at = int(found.group(3)); new_count = int(found.group(4) or 1)
        new_end = new_at + new_count - 1 if new_count else new_at
        if new_end < a:
            shift += new_count - old_count
    return a - shift, b - shift


def rule_dirty(path: Path, a: int, b: int, cwd: Path = ROOT) -> bool:
    """Does the working tree differ from HEAD inside lines a..b?

    `git log` reads history, so an edit being committed *right now* would
    escape it and be caught only on the next run — the one-commit lag
    `F008`'s fix was written against.  This closes it: the gate runs from
    the pre-commit hook, where the change is in the tree.
    """
    out = _git("diff", "HEAD", "-U0", "--", str(path), cwd=cwd)
    for line in out.splitlines():
        if not line.startswith("@@"):
            continue
        found = re.search(r"\+(\d+)(?:,(\d+))?", line)
        if not found:
            continue
        at = int(found.group(1))
        count = int(found.group(2) or 1)
        if count == 0:                       # a pure deletion, at the seam
            if a <= at <= b or a <= at + 1 <= b:
                return True
        elif at <= b and at + count - 1 >= a:
            return True
    return False


def test_the_tree_has_marks_to_check():
    """The oracle that has only ever passed is a claim (`manifesto.md`).

    If the marks all go away this file must say so out loud rather than
    pass on an empty set, which is how a gate quietly stops guarding.
    """
    assert marks(), (
        "no self-shaped mark found in the tree — either every rule about "
        "sessions is now Henri's own, or the mark's form changed and "
        "manifesto.md §'How a practice gets adopted' did not follow")


@pytest.mark.parametrize("mark", marks(), ids=lambda m: m.where)
def test_every_mark_has_a_rule_above_it(mark: Mark):
    """The third verdict: the extent is not determinable, so say that."""
    assert mark.rule_start is not None, (
        f"{mark.where}: cannot determine which rule this mark stands "
        f"under — no bold-lead paragraph within {REACH} lines above it. "
        "Either the rule is written without a bold lead, or the mark is "
        "in the wrong place. This is the third verdict, not a failure of "
        "the rule: the gate will not guess at what Henri approved.")


@pytest.mark.parametrize("mark", marks(), ids=lambda m: m.where)
def test_an_approval_still_covers_the_words_he_read(mark: Mark):
    """Editing an approved rule un-approves it.

    Red-first proof that this catches what it names is in
    `test_the_gate_catches_a_rule_edited_after_its_approval`, which
    builds the defect in a tree of its own.
    """
    when = mark.approved_on
    if when is None:
        return                               # unanswered, or a verdict
                                             # that is not an approval:
                                             # both are fine, neither is
                                             # a claim about the text
    a, b = mark.rule_start + 1, mark.start    # 1-based, mark excluded

    assert not rule_dirty(mark.path, a, b), (
        f"{mark.where}: the rule above this mark is edited in the working "
        f"tree, and the mark still says Henri approved it on {when}. "
        "An approval is a claim about the words he read. Either revert "
        "the rule, or clear the verdict and put it back to him.")

    touched = rule_last_touched(mark.path, a, b)   # raises if git cannot say
    assert touched is None or touched <= when, (
        f"{mark.where}: the rule at lines {a}-{b} was last committed "
        f"{touched}, and Henri's approval is dated {when}. The words "
        "changed after he read them, so the approval no longer covers "
        "them. Clear the verdict and put the rule back to him.")


# --- the gate, shown red against the defect it names -----------------
#
# `manifesto.md` §"The three ways an instrument fails", second way: an
# oracle that has only ever passed is a claim.  These build a tree with
# the defect in it and watch the checkers notice.

@pytest.fixture
def tree(tmp_path: Path) -> Path:
    """A git tree with one approved rule in it, committed a day early.

    A fixture is a claim about the thing it copies (`board/README.md`):
    this builds both sides of the seam — a commit that writes the rule,
    then a later commit that writes the mark — because a fixture with
    one commit gives the defect and the correct program the same number.

    **The rule lives in a subdirectory, and there is a decoy at the root
    wearing the same basename.**  The first version of this fixture put
    `d.md` at the repository root, which made every real mark's path
    (`board/README.md`) a case the fixture did not model — and that is
    exactly where the defect was: `git log -L…:README.md` resolved
    against the tree's own root `README.md` instead.  A fixture that
    cannot fail the way the real thing fails is not measuring it.
    """
    here = tmp_path / "t"
    (here / "board").mkdir(parents=True)
    subprocess.run(("git", "init", "-q"), cwd=here, check=True)
    (here / "d.md").write_text("a decoy at the root, two lines long\n"
                               "— shorter than the rule, exactly as the\n",
                               encoding="utf-8")

    rule = ("# doc\n"
            "\n"
            "**A rule about sessions.**  It says a thing, and it runs to\n"
            "the end of this paragraph and no further.\n")
    (here / RULE).write_text(rule, encoding="utf-8")
    subprocess.run(("git", "add", "-A"), cwd=here, check=True)
    subprocess.run(("git", "commit", "-q", "-m", "the rule",
                    "--date", "2026-08-20T09:00:00+03:00"),
                   cwd=here, check=True,
                   env={**_env(), "GIT_COMMITTER_DATE":
                        "2026-08-20T09:00:00+03:00"})

    (here / RULE).write_text(
        rule + "*(self-shaped, 2026-08-21 — a session wrote it.\n"
               "henri: approved 2026-08-21)*\n", encoding="utf-8")
    subprocess.run(("git", "add", RULE), cwd=here, check=True)
    subprocess.run(("git", "commit", "-q", "-m", "the mark"),
                   cwd=here, check=True, env=_env())
    return here


def _env() -> dict:
    import os
    return {**os.environ,
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_CONFIG_SYSTEM": os.devnull,
            "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
            "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}


def _the_mark(here: Path) -> Mark:
    lines = (here / RULE).read_text(encoding="utf-8").splitlines()
    at = next(i for i, l in enumerate(lines) if OPENS.match(l))
    return Mark(here / RULE, lines, at, at + 1)


def test_the_gate_reads_the_rules_own_lines_when_an_edit_above_it_shifts_them(tree):
    """F021: an uncommitted edit above an approved rule moves its lines,
    and `git log -L` with the working tree's numbers reads some other
    paragraph in HEAD — here the mark's own lines, committed today, so the
    gate said the rule changed after Henri read it.  Twice on 2026-09-03,
    both false, both needing his `--no-verify`.  The fixture's HEAD has the
    rule at lines 3-4 (committed 2026-08-20) and the mark below it
    (committed now); three lines added above the rule in the working tree
    put the rule at 6-7, where HEAD holds the mark.  The gate must answer
    with the rule's date, and say the rule is not dirty."""
    here = tree
    p = here / RULE
    text = p.read_text(encoding="utf-8")
    p.write_text(text.replace("# doc\n", "# doc\n\nsomething new above the rule,\nuncommitted.\n", 1), encoding="utf-8")
    mark = _the_mark(here)
    a, b = mark.rule_start + 1, mark.start
    assert (a, b) == (6, 7), (a, b)
    assert not rule_dirty(p, a, b, cwd=here)
    assert head_lines(p, a, b, cwd=here) == (3, 4)
    assert rule_last_touched(p, a, b, cwd=here) == datetime.date(2026, 8, 20)


def test_the_fixture_reads_as_a_fresh_approval(tree: Path):
    """Green before red, or the red below proves nothing."""
    mark = _the_mark(tree)
    assert mark.verdict == "approved 2026-08-21"
    assert mark.approved_on == datetime.date(2026, 8, 21)
    assert mark.rule_start == 2
    a, b = mark.rule_start + 1, mark.start
    assert not rule_dirty(tree / RULE, a, b, cwd=tree)
    assert rule_last_touched(tree / RULE, a, b, cwd=tree) \
        == datetime.date(2026, 8, 20)


def test_the_gate_catches_a_rule_edited_in_the_working_tree(tree: Path):
    """The one-commit lag closed: an edit not yet committed is caught."""
    path = tree / RULE
    path.write_text(path.read_text(encoding="utf-8")
                    .replace("It says a thing", "It says another thing"),
                    encoding="utf-8")
    mark = _the_mark(tree)
    a, b = mark.rule_start + 1, mark.start
    assert rule_dirty(path, a, b, cwd=tree), \
        "an approved rule was edited in the working tree and the gate " \
        "did not notice"


def test_the_gate_catches_a_rule_edited_after_its_approval(tree: Path):
    """The defect this file exists for, committed rather than staged."""
    path = tree / RULE
    path.write_text(path.read_text(encoding="utf-8")
                    .replace("It says a thing", "It says another thing"),
                    encoding="utf-8")
    subprocess.run(("git", "add", RULE), cwd=tree, check=True)
    subprocess.run(("git", "commit", "-q", "-m", "quietly rewritten"),
                   cwd=tree, check=True, env=_env())
    mark = _the_mark(tree)
    a, b = mark.rule_start + 1, mark.start
    touched = rule_last_touched(path, a, b, cwd=tree)
    assert touched is not None and touched > mark.approved_on, (
        "an approved rule was rewritten after Henri read it and the "
        f"gate still called the approval fresh (rule {touched}, "
        f"approval {mark.approved_on})")


def test_answering_a_mark_does_not_touch_the_rule(tree: Path):
    """The mark's own lines are excluded, or every approval is instantly stale.

    This is the check that made the whole gate possible: the commit that
    writes or answers a mark must not read as an edit to the rule above
    it.  Measured on the real tree before the gate was written — the
    batch-2 rule's body last changed 2026-08-27, its mark's lines today.
    """
    path = tree / RULE
    path.write_text(path.read_text(encoding="utf-8")
                    .replace("approved 2026-08-21", "approved 2026-08-22"),
                    encoding="utf-8")
    subprocess.run(("git", "add", RULE), cwd=tree, check=True)
    subprocess.run(("git", "commit", "-q", "-m", "he answered"),
                   cwd=tree, check=True, env=_env())
    mark = _the_mark(tree)
    a, b = mark.rule_start + 1, mark.start
    assert rule_last_touched(path, a, b, cwd=tree) \
        == datetime.date(2026, 8, 20), \
        "answering the mark counted as editing the rule"


def test_git_refusing_the_question_is_never_a_pass(tree: Path):
    """The defect this file shipped with for twenty minutes, as a test.

    `rule_last_touched` first asked git for `path.name` rather than the
    path relative to the repository, so `board/README.md` went in as
    `README.md` — and this tree has one of those at its root.  git said
    `fatal: file README.md has only 103 lines`, `_git` swallowed the
    non-zero exit into `""`, the function returned `None`, and the
    assertion read `None` as "no edits after the approval".  All three
    board marks were guarded by nothing, and the suite was green.

    It is `board/README.md` §"What the days taught" exactly — *a check
    that asserts less than it means* — found in the commit that puts the
    mark on that very rule, and found by asking what the instrument did
    rather than by trusting its colour.

    So the contract is: git failing is an exception, never a verdict.
    """
    with pytest.raises(GitCannotSay):
        rule_last_touched(tree / "d.md", 3, 4, cwd=tree)   # the 5-line decoy

    # the real shape it stands for: the basename resolves to the decoy,
    # which is too short to hold the range — exactly as README.md was
    assert (tree / "d.md").read_text().count("\n") == 2
    # while the same range against the right path answers correctly
    assert rule_last_touched(tree / RULE, 3, 4, cwd=tree) \
        == datetime.date(2026, 8, 20)


def test_a_rule_with_no_bold_lead_gets_the_third_verdict(tmp_path: Path):
    """Not a wrong answer — a different sentence."""
    path = tmp_path / "d.md"
    path.write_text("some prose with no bold lead anywhere above it\n"
                    "\n"
                    "*(self-shaped, 2026-08-21 — a session wrote it.\n"
                    "henri: approved 2026-08-21)*\n", encoding="utf-8")
    lines = path.read_text(encoding="utf-8").splitlines()
    mark = Mark(path, lines, 2, 3)
    assert mark.rule_start is None
    assert mark.approved_on == datetime.date(2026, 8, 21)
