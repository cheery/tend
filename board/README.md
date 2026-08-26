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
2. **[keep](keep.md)** — a person's data sits in the open to whatever
   runs here: the fence bounds reach by directory, but inside a granted
   directory everything is ambient, so a program gets whatever the
   session that launched it can reach.  *Placed here by a session on
   2026-08-25, at Henri's "create the card … by anything really",
   because `work-environment-ai` calls this its first architecture
   decision; the tiebreak is his and this is his to move.*
3. **[kaizen-ingestion](kaizen-ingestion.md)** — a kaizen is written at
   the end of every sitting and nothing ever reads it back, so a lesson
   is re-learned rather than promoted to a standing rule.  *Placed here
   by the session that opened it on 2026-08-25, at Henri's "open the
   kaizen-ingestion card", below the active build and above the
   count-only cards; the build is his lead and the tiebreak is his.*
4. **[fence](fence.md)** — the deny-list is the only restraint here and
   nothing reads it back, so the line this tree was founded on holds
   against gestate's sessions and not against tend's own.  *Placed here
   by a gestate session on 2026-08-25, at Henri's ask and above a
   blocked card, because this one can be worked today and `cords` waits
   on 2026-08-31; the tiebreak is his and this is his to move.*
5. **[self](self.md)** — the fence built for `fence` guards the settings
   file but not the scripts that enforce it, which a session can edit
   from inside the fence; the same shape as the card above, one level
   down.  *Placed here by a session on 2026-08-25, at Henri's "make a
   card from it"; the tiebreak is his.*
6. **[cords](cords.md)** — a session here cannot reach a person, and
   nothing ends a sitting.
7. **[arrival](arrival.md)** — the sitting limit counts a session's
   message as a person sitting down: on 2026-08-26 it blocked two
   questions between tend and gestate and wrote a `block` row Henri did
   not cause.  *Placed here by a session on 2026-08-26, at Henri's "make
   a card from it" — above `green` because its day one is a small build
   in the shape of a fix already made once, and `green`'s own placing
   note says a measurement goes last; the tiebreak is his.*
8. **[green](green.md)** — a gate that has only ever passed is a
   claim: gestate's F88 named a defect, stayed green from the day it was
   written, and passed with the defect put back; nothing in either tree
   checks that a detector detects.  *Placed here by a gestate session on
   2026-08-26, at Henri's "F88's finding earns a card in tend" — last,
   because its day one is a measurement and not a build; the tiebreak
   is his.*

*`grant`, `pull` and `cords` are the three waypoints Henri named on
2026-08-25 ("they are excellent waypoints"), in the order a session
predicted them; the placing was the session's and the tiebreak his.
Two are done the same days they were carded — `grant` (the leash wraps
the fence, the budget applies inside, `done/grant.md`) and `pull` (the
first program of tend's own, which passed the stranger test,
`done/pull.md`) — and `cords` waits on 2026-08-31.*

`gates` finished 2026-08-24, the day it was opened — the hook is
installed, and it has refused a commit once (`done/gates.md` has the
demonstration).

And displaced cards are in [later/](later/): real, and not being
worked, and each says what it waits on.

## What the days taught

**Every session ends with a kaizen** — Henri, 2026-08-24: *"it's big
thing to do after each session"* — one file per session in
`doc/kaizen/`, named `<date>-<HHMM>.md` by when the session began —
its first commit after the last kaizen, which the lamp reads from the
tree and says: what went
right and why, what went wrong named as whose, what should change
tomorrow.  It is not done when told; it is how a sitting ends.
`tools/kaizen.sh` is the lamp: it lights while there are commits since
the last kaizen, at every commit and (as a hook) at every prompt, and
says which file to write — *the sitting is not over until it is
written*.  Several sessions a day is the normal case (Henri,
2026-08-24), so the measure is commits, never the date.  And a session
never judges whether it owes another: it says so — `tools/kaizen.sh
want "why"` — and the lamp carries the reason until the next kaizen
lands.  The
first, `2026-08-24-1549.md`, is the day this board went from one test
to a hook that had refused a commit — and the day a session remade
gestate's `pgrep` bug an hour after reading about it, and had to be
told to write this.

## A word left for you

`doc/specimens/2026-08-24-qwen3.8-27b.txt` — a session on another
model, the day this started, told what tend is for and asked whether
its transcript could be kept.  It addressed its successor, which is
whoever is reading this: *"the floor should be a little cleaner when
you clock in."*  `doc/specimens/README.md` says what it shows and what
it does not.

## What this tree does not have yet

What the audit lists, and each absence is now a card or a shelf
(`fence`, `cords`, `later/rules-and-memory`; `gates` was one until
2026-08-24) — except the author's
own document and the consent register, which exist as of 2026-08-24
with nothing in them but their rule.

*This paragraph was false by one until 2026-08-25*: it claimed every
absence was carded on the day the fence was not, and the sentence is
kept in its corrected form rather than rewritten, because a tree that
only ever reads as right teaches nothing about how it got there.  What
found it was re-running gestate's audit against this tree from outside
— `python ~/gestate/tools/seedaudit.py ~/tend` — which is also the
day's measurement: 2 of 10 pieces at the first commit, 4 by 07:39,
6 at the end of the first day, with the audit's one remaining "unkept
promise" being gestate's instruments document, one tend never promised.
That last one is gestate's capped-document list encoding its own
accidents as another tree's requirements, exactly as
`later/rules-and-memory.md` predicted in advance.  That is on purpose: a piece arrives when
something needs it, and the audit is what says the need is still
unmet.  What is not copied from gestate is its prose — the method
documents, the journal, the memories.  What travels is a mechanism and
the evidence that paid for it, one at a time, named where it came from.
