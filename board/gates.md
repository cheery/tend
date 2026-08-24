# gates — the board has a contract and nothing runs it

    status   open
    because  `test/test_board.py` refuses a malformed card, and nothing
             runs it unless somebody remembers — a rule with no gate is
             a wish, and this tree's first day already has one wish
    asked    Henri, 2026-08-24 — "add the needed cards so that the
             absent work is completed"
    see      ~/gestate/tools/seedaudit.py — what it calls absent here:
             the gates (tools/suite.py, tools/pre-commit.sh), and the
             boot surface unbacked (no test names AGENTS.md)
             ~/gestate/tools/pre-commit.sh — the shape to borrow,
             named as borrowed
             manifesto.md §"How a practice gets adopted" — whoever
             brings it owes the demonstration

## What it is

Three things, in order, each small:

1. A runner that runs the contract test and says so — `tools/suite.py`
   or smaller; tend has one test and does not need a page.
2. A pre-commit hook that runs it, installed in this clone, checked by
   a test the way gestate's `test_precommit.py` does.
3. A test that names `AGENTS.md` and refuses it longer than one line —
   the boot surface's gate.

## The demonstration owed

A commit with a card missing its `because`, refused at the hook.  Until
that has happened once here, this is a practice tend is tolerating on
gestate's say-so.
