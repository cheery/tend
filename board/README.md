# board/ — the live board, and how to work it

**This is the first thing to read when picking the project up.**  One
file per task; Henri fills the board, a session works down it.

Started 2026-08-24 as the second tree run by the method that grew in
`~/gestate` — the first project this tree governs, and the first
directory that method's audit (`~/gestate/tools/seedaudit.py`) has ever
been pointed at that is not its own.  It was red on the first run, and
`board/README.md` in gestate says why that is the correct starting
state: *a gate is turned on after the tree is clean, never as a way of
announcing that it should be.*

## What a card is

A card is a file, and the filename is its id.  It opens with a block of
fields, four spaces in, the name and value two spaces apart:

    status   open | doing | blocked | done — <date> | shelved — <date>
    because  the problem, in the words of whoever had it — never a fix
    asked    who, when, and the words
    see      what it leans on

`because` names a **problem**.  A card whose `because` names a solution
is a card that has already decided, and the deciding is what the card
is for.  `test/test_board.py` refuses a card without one.

## Where a card is

`board/*.md` is open work.  `done/` is finished — the problem no longer
stands.  `later/` is real and not being worked: it waits on an event or
on a decision, and it says which.  A `blocked` card names what it waits
on.  Moving between shelves never renames the file.

## The priority

Priority, not order: the list says what matters most, and the tiebreak
between two workable cards is Henri's.

1. **[work-environment-ai](work-environment-ai.md)** — sessions and
   programs run on this machine with no budget, no grant and no
   lifecycle; the enforcement boundary must live outside the session's
   write access, which is why this tree exists at all.
2. **[cords](cords.md)** — a session here cannot reach a person, and
   nothing ends a sitting.

`gates` finished 2026-08-24, the day it was opened — the hook is
installed, and it has refused a commit once (`done/gates.md` has the
demonstration).

And displaced cards are in [later/](later/): real, and not being
worked, and each says what it waits on.

## What the days taught

One file per sitting that ended with a kaizen, in `doc/kaizen/`.  The
first, 2026-08-24, is the day this board went from one test to a hook
that had refused a commit — and the day a session remade gestate's
`pgrep` bug an hour after reading about it.

## A word left for you

`doc/specimens/2026-08-24-qwen3.8-27b.txt` — a session on another
model, the day this started, told what tend is for and asked whether
its transcript could be kept.  It addressed its successor, which is
whoever is reading this: *"the floor should be a little cleaner when
you clock in."*  `doc/specimens/README.md` says what it shows and what
it does not.

## What this tree does not have yet

What the audit lists, and each absence is now a card or a shelf
(`cords`, `later/rules-and-memory`; `gates` was one until 2026-08-24)
— except the author's
own document and the consent register, which exist as of 2026-08-24
with nothing in them but their rule.  That is on purpose: a piece arrives when
something needs it, and the audit is what says the need is still
unmet.  What is not copied from gestate is its prose — the method
documents, the journal, the memories.  What travels is a mechanism and
the evidence that paid for it, one at a time, named where it came from.
