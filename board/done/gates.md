# gates — the board has a contract and nothing runs it

    status   done — 2026-08-24
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

## Done, 2026-08-24, all three and the demonstration

1. `tools/suite.py` — runs everything under `test/` and says so; no
   page, on purpose, until a slow test exists to need one.
2. `tools/pre-commit.sh` — gestate's shape, marker `tend:`, installed
   here by `tools/toolbox.sh` and checked by `test/test_precommit.py`
   (which is why a fresh clone is red until toolbox runs — that is the
   finding, not a broken test).
3. `test/test_rules.py` — the boot surface's gate: `AGENTS.md` and
   `CLAUDE.md`, one line each, pointing at `board/README.md`, agreeing
   with each other.  It wears the audit's declared name so
   `~/gestate/tools/seedaudit.py` finds it.

**And the demonstration happened.**  `board/demonstration-dud.md` — a
card with `status` and `asked` and no `because` — was staged and
committed; the hook ran the suite, two gates named it
(`test_every_card_says_why_it_exists[demonstration-dud]` and the
priority check, which also caught that the card was unplaced), and the
commit was refused with HEAD unmoved.  The dud was then deleted; it
never reached the tree.  The practice is no longer tolerated on
gestate's say-so — it has caught something here.
