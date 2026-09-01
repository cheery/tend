"""A question written where it arises, and what would answer it.

`card:questions.md`, day one (a), 2026-09-01.  Its `because`: a session
raises questions all day and each is written into whichever card it arose
in, so the set of things actually waiting on Henri exists nowhere.  Its
*finding* is sharper than its `because` and this file exists to hold the
finding: of the first eight questions handed over, five came back "I
don't know" and **three of those five were measurements nobody had
run**.  Asking a person for an opinion where evidence is owed is not
asking a question, it is offloading a measurement.

So a question says, when it is written, what would answer it:

    *(question, measure — …)*        a session's to run; never reaches him
    *(question, his call — …)*       his, and the only kind that reaches him
    *(question, waits on <event> — …) nothing to decide until it happens

He answers by appending a line beginning `henri:`, exactly as with a
self-shaped mark (`test/test_marks.py`) — one convention, both
directions.

**What this file refuses**, and each is a way the question would be
silently lost rather than loudly wrong:

- a category that is not one of the three, including a typo of one
- a `waits on` that does not name an event
- a question that is not a question
- **a question that is not flush left**, which the search cannot find —
  the commit-message question in `card:rewritten-command.md` spent its
  first ten minutes indented inside a bullet and invisible

That last one is the same defect `test/test_marks.py` shipped with and
the same one `board/README.md` §"What the days taught" names: a check
that asserts less than it means.  A search anchored to the line start is
worth exactly as much as a rule that questions start their line.

**And one rule that is deliberately not a test.**  "Only `his call`
reaches Henri" is the mechanism this whole card is for, and the obvious
way to enforce it is to go red when a `measure` question carries a
`henri:` answer — a session offloaded a measurement after all.  That
check was written and then removed, because it goes red **at Henri's own
writing**: if he reads a measurement question and has something to say
about it, a gate would refuse him for engaging.  `keeper.md` promises
the opposite — his hand is the authority these gates defer to, not one
they audit — and a gate that punishes the person for participating is
worse than the failure it prevents.  So the division lives in the
category a session writes and in what `keeper.md` greps, and what is
tested is only that the two agree.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent

#: Every root document plus these shelves.  Not a list of files: naming
#: its own subjects is how `test_marks.py`'s first search went stale.
SEARCHED_DIRS = ("board", "fixme", "spec", "doc")

#: A question, flush left.  `grep -rn '^\\*(question'` returned zero hits
#: before this landed — measured, the way `(self-shaped` was.
OPENS = re.compile(r"^\*\(question,\s*(.+?)\s*(?:—|--)")

#: The same thing anywhere on a line, to catch one that is indented and
#: therefore invisible to the anchored search.
ANYWHERE = re.compile(r"\*\(question,")

#: The three, and no others.  `waits on` carries its event.
CATEGORIES = ("measure", "his call")
WAITS = re.compile(r"^waits on\s+(\S.*)$")

#: Henri's verdict, lowercase — `Henri:` capitalised is the tree's
#: attribution form and is a session quoting him.
VERDICT = re.compile(r"^henri:\s*(\S.*)$", re.MULTILINE)


class Question:
    def __init__(self, path: Path, lines: list[str], start: int):
        self.path, self.start = path, start
        end = start
        while end < len(lines) - 1 and ")*" not in lines[end]:
            end += 1
        self.end = end
        self.text = "\n".join(lines[start:end + 1])
        self.category = OPENS.match(lines[start]).group(1)
        # the answer, if any, is the run of lines after the question
        rest = lines[end + 1:end + 4]
        self.answer = "\n".join(rest)

    @property
    def where(self) -> str:
        try:
            at = self.path.relative_to(ROOT)
        except ValueError:
            at = self.path
        return f"{at}:{self.start + 1}"

    @property
    def waits_on(self) -> str | None:
        found = WAITS.match(self.category)
        return found.group(1) if found else None

    @property
    def answered_by_henri(self) -> str | None:
        found = VERDICT.search(self.answer)
        return found.group(1) if found else None


def _files() -> list[Path]:
    out: list[Path] = sorted(ROOT.glob("*.md"))
    for name in SEARCHED_DIRS:
        here = ROOT / name
        if here.is_dir():
            out += sorted(here.rglob("*.md"))
    return [p for p in out if p.is_file()]


def _for_henri() -> list[Question]:
    """The queue `keeper.md` act 2 reads.  `his call`, and nothing else."""
    return [q for q in questions() if q.category == "his call"]


def questions() -> list[Question]:
    out = []
    for path in _files():
        lines = path.read_text(encoding="utf-8").splitlines()
        for i, line in enumerate(lines):
            if OPENS.match(line):
                out.append(Question(path, lines, i))
    return out


def test_the_tree_has_questions_to_check():
    """An oracle that has only ever passed is a claim (`manifesto.md`)."""
    assert questions(), (
        "no question found in the tree — either nothing is open, or the "
        "form changed and card:questions.md did not follow")


@pytest.mark.parametrize("q", questions(), ids=lambda q: q.where)
def test_a_question_names_what_would_answer_it(q: Question):
    """The whole point: `measure`, `his call`, or `waits on <event>`.

    A fourth category, or a typo of one of the three, means a question
    that the collection either misroutes or drops.  The failure this
    guards is not cosmetic — a `measure` written as `measurement` would
    silently join the queue that reaches Henri, which is the exact thing
    this card was opened to stop.
    """
    if q.category in CATEGORIES:
        return
    event = q.waits_on
    assert event, (
        f"{q.where}: '{q.category}' is not one of the three. A question "
        "says what would answer it: 'measure' (a session runs it), 'his "
        "call' (Henri decides), or 'waits on <event>' — and 'waits on' "
        "must name the event, or nothing can ever notice it happened. "
        "See card:questions.md.")


@pytest.mark.parametrize("q", questions(), ids=lambda q: q.where)
def test_a_question_is_a_question(q: Question):
    """It ends in a question mark, because a statement is not a question.

    Cheap, and it catches the shape this card warns about most: a line
    that has already decided, wearing a question's clothes.
    """
    assert "?" in q.text, (
        f"{q.where}: a question with no question mark in it. If it is a "
        "decision, it belongs in the card's prose; if it is a defect, it "
        "belongs in fixme/.")


def test_no_question_is_hidden_by_indentation():
    """The defect this rule was written from, on the day it was written.

    `card:rewritten-command.md`'s commit-message question was first
    written inside a bulleted list, indented two spaces — a perfectly
    reasonable place for it, and invisible to `grep -rn '^\\*(question'`.
    An anchored search is worth exactly as much as the rule that the
    thing it searches for starts its line, so the rule is held here.

    **One to three spaces, not four or more**, and the reason is that
    `card:questions.md` has to be able to *show* the form: a four-space
    indent is a markdown code block, which is where an example lives,
    and one to three is a list item, which is where a real question gets
    lost.  The gap that leaves, named rather than discovered later: a
    question indented four spaces inside a *nested* list would read as an
    example and pass.  No such list exists in the tree today, and the
    honest alternative — no check at all — is worse.
    """
    hidden = []
    for path in _files():
        for i, line in enumerate(path.read_text(encoding="utf-8").splitlines()):
            if OPENS.match(line) or not ANYWHERE.search(line):
                continue
            indent = len(line) - len(line.lstrip())
            if line.lstrip().startswith("*(question,") and 1 <= indent <= 3:
                hidden.append(f"{path.relative_to(ROOT)}:{i + 1}")
    assert not hidden, (
        "a question is indented and the anchored search cannot find it: "
        + ", ".join(hidden)
        + ". A question starts its own line, flush left — outside the "
          "list, not inside it. card:questions.md §'The form'.")


def test_the_his_call_queue_is_the_only_one_that_reaches_him():
    """What `keeper.md` act 2 will show, checked against what it greps.

    The queue is computed here the way a person computes it — filter on
    the category — so the page and the parser cannot drift apart.  It
    asserts a property of the *filter*, never a limit on the queue's
    length: a long queue is a finding about the sessions, and a gate
    that went red on it would be nagging Henri for a session's habit.
    """
    queue = {q.where for q in _for_henri()}
    for q in questions():
        assert (q.category == "his call") == (q.where in queue), \
            f"{q.where}: the queue filter disagrees with the category"


# --- the checkers, shown red against what they name ------------------

@pytest.fixture
def doc(tmp_path: Path):
    def build(body: str) -> list[Question]:
        path = tmp_path / "d.md"
        path.write_text(body, encoding="utf-8")
        lines = body.splitlines()
        return [Question(path, lines, i) for i, l in enumerate(lines)
                if OPENS.match(l)]
    return build


def test_a_fourth_category_is_refused(doc):
    q, = doc("*(question, someday — will this ever matter?)*\n")
    assert q.category == "someday"
    assert q.waits_on is None
    with pytest.raises(AssertionError, match="is not one of the three"):
        test_a_question_names_what_would_answer_it(q)


def test_a_waits_on_with_no_event_is_refused(doc):
    q, = doc("*(question, waits on — is the rule too loose?)*\n")
    assert q.category == "waits on"
    assert q.waits_on is None
    with pytest.raises(AssertionError, match="must name the event"):
        test_a_question_names_what_would_answer_it(q)


def test_a_waits_on_with_an_event_passes(doc):
    """Green beside the red, or the red above proves nothing."""
    q, = doc("*(question, waits on a corrupted message — too loose?)*\n")
    assert q.waits_on == "a corrupted message"
    test_a_question_names_what_would_answer_it(q)


def test_a_statement_wearing_a_question_mark_is_refused(doc):
    q, = doc("*(question, his call — we should lift the calls back.)*\n")
    with pytest.raises(AssertionError, match="no question mark"):
        test_a_question_is_a_question(q)


def test_henri_answering_under_a_question_is_read(doc):
    got = doc("*(question, his call — should the calls go back to 16?)*\n"
              "henri: yes, lift it back\n")
    assert got[0].answered_by_henri == "yes, lift it back"
    assert doc("*(question, his call — anything?)*\n"
               "some prose\n")[0].answered_by_henri is None
