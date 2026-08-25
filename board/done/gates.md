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

## 2026-08-25 — measured from inside the fence: the gate is not enforcement, and cannot be

Asked by Henri, after `card:self.md` left the `.git/hooks` question as
its own line: is the pre-commit hook in the protected set?  Measured
from a fenced session, every route past the gate is open:
`git commit --no-verify` (offered by the hook's own message, by design);
`.git/hooks/pre-commit` writable, so editable or deletable;
`.git/config` writable, so `core.hooksPath` moves the hook — and
`git -c core.hooksPath=…` needs no file at all; `--uninstall`, offered;
and `tools/pre-commit.sh`, `tools/suite.py` and every file under `test/`
writable — the gate is the suite, and the suite is the tree.

That last row settles it.  Binding the shim and the script read-only
would protect nothing while `test/` is writable, and `test/` is the
work; protecting the gate properly means protecting the whole suite,
which is the second `.claude` that `card:self.md` says the set must not
become.  So the gate is **not in the set, and that is a category, not
a gap**: the set bounds what a session may *do*; the gate bounds what
the tree *accepts as committed*.  Reach and consistency.  The header of
`tools/pre-commit.sh` already knows which kind it is — cheap, loud,
trivial to remove, and a skipped gate is to be said in the commit body.

The exposure that remains: a commit lands that the gates would have
refused, and the skip is not written down.  It is not silent for long —
the next honest commit by anyone runs the suite and goes red on HEAD,
and any session running `pytest` sees it.  The evidence: zero
`--no-verify` in this tree's history, every commit body read.  Gestate
asked the same question (`~/gestate/board/done/cheap-gates.md`, *"exactly
the kind of thing that gets typed reflexively"*) and answered with
evidence rather than a lock; so does this.  **Not built, on purpose.**
What would change that: a skipped gate that is found only later — count
them here, one dated line each, the way `card:cords.md` counts guessed
questions.  If the count moves, the instrument is a read-back lamp at
`SessionStart` (the suite once, 🔴 if HEAD is red), whose script would
join the protected set; it is a small card with a real `because` on
that day, and decoration before it.

* (none yet)
