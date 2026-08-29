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
on.  Moving between shelves never renames the file.  **Cite a card as
`card:<name>.md`**, never by shelf path: the notation resolves on
whichever shelf the card is, so a move to `done/` breaks nothing — the
form gestate's board uses, taken here on 2026-08-27 when closing two
cards broke the summaries' path citations ("it starts to matter
slowly" — Henri).  `test_board.py` resolves every citation in the
board and the summaries; `test_summary.py` resolves the sheets'.

## The priority

Priority, not order: the list says what matters most, and the tiebreak
between two workable cards is Henri's.

1. **[work-environment-ai](work-environment-ai.md)** — sessions and
   programs run on this machine with no budget, no grant and no
   lifecycle; the enforcement boundary must live outside the session's
   write access, which is why this tree exists at all.
2. **[session-program](session-program.md)** — a node tend runs is a
   program, not a session, until it carries the cords: a limit, a lamp,
   a way to reach the person.  The grant half of "a session is a
   program" is built; this is the half `keep` and `resolver` named and
   did not build.  *Placed here by a session on 2026-08-26, at Henri's
   "open the cords card for the session's program", below the build
   cards and above the count-only ones; the tiebreak is his and this is
   his to move.*  Unblocked 2026-08-28 at Henri's "I think that 'not yet'
   lifts now": the first node may lead work.  The substrate is built —
   the llm node answers under keep (`card:node-install.md`) — and the
   card carries the road from there (delivery, a minimal work loop, the
   node's own cords; ~2–4 sittings to gemma4 working the board next to
   gemma4 cold, the conditioning measurement).  *On 2026-08-29 evening,
   asked which model leads, Henri said "both": a door (`doors/`,
   `tools/door.sh`, `lead.sh NODE --door NAME`) sends the same turn
   through OpenRouter or Anthropic's chat wire, unkept, and the node
   with no door is the loop as it was; a kept turn through a door is
   not built and says so.*
3. **[kaizen-ingestion](kaizen-ingestion.md)** — a kaizen is written at
   the end of every sitting and nothing ever reads it back, so a lesson
   is re-learned rather than promoted to a standing rule.  *Placed here
   by the session that opened it on 2026-08-25, at Henri's "open the
   kaizen-ingestion card", below the active build and above the
   count-only cards; the build is his lead and the tiebreak is his.*
4. **[sitting-everywhere](sitting-everywhere.md)** — the sitting limit
   holds only for sessions started in two directories, and the grant it
   offers has no shape: on 2026-08-26 the desk was retaken within
   minutes after 8 of 9 blocks, by hand.  *Placed last by a gestate
   session on 2026-08-27, as a new card arrives; the tiebreak is his.*
5. **[lander](lander.md)** — a commit that passed the gates is not in
   force until a person runs one line, and nothing but the person's
   memory carries it there.  *Placed last by the session that wrote it
   on 2026-08-27 at Henri's "Write the lander card"; its day one is a
   lamp, which is also the count that would make the rest of it wrong;
   the tiebreak is his.*
6. **[silent-cord](silent-cord.md)** — the andon sounds only through a
   reach row the session must be allowed, so narrowing reach cuts the
   cord.  *Placed last by the session that wrote it on 2026-08-28 at
   Henri's "andon card"; day one is the sound on the person's side, red
   first with the row off; the tiebreak is his.*
7. **[canvas](canvas.md)** — a pulled node's death is a line in a file
   nobody is looking at: nothing on the person's side shows what they
   are holding, and a death and a cord pull are events on one timeline
   seen in two places or in none.  *Placed last by the session that
   wrote it on 2026-08-28 at Henri's "open the canvas card"; day one is
   a canvas directory of `name.pin` files and the panel showing a row
   per pin with the stop's reason in the log column; the tiebreak is
   his.*
8. **[model-acceptance](model-acceptance.md)** — something breaks when
   nobody picks the mind, and the keeper is the only check.  *Woken
   from `later/` on 2026-08-28 by a session at Henri's "do
   session-program", on the event it waited for — a door where a
   model is admitted (the llm node's cords) — with `tools/compare.py`
   as its first instrument; placed last; the tiebreak is his.*
9. **[hold](hold.md)** — a node that should be up is up only while
   something happens to pull it: the llm node idles out 60 s after the
   last pull and reloads for 80 s on the next, and nowhere on the
   person's side says "keep this alive".  *Placed last by the session
   that wrote it on 2026-08-29 at Henri's "Lets card it"; its day one is
   a `<name>.hold` file beside the pin whose presence is a standing pull
   and whose mtime re-asserts it after a death; the tiebreak is his.
   Day one landed the same day at his "do the hold", and its second
   pass at his review — the hold names its node inside the file, the
   panel shows holds as rows, and a hold not kept is loud; its third
   pass put the person's hand in the panel — hold, pin, unhold, and the
   resolver run on every write and on entry — and the hold-to-death flow
   test found `serve` silent on a node with no state directory yet.
   The evening landed the tick — the resolver with no hand on it:
   `resolve.sh --tick` leaves a stamp the panel reads (`NO TICK` /
   `TICK STALE` under a hold), and `install.sh --tick` is Ubuntu's
   carrier, a user timer running the installed copy; systemd is the
   implementation, never the dependency (Henri's words).*

*`grant`, `pull` and `cords` are the three waypoints Henri named on
2026-08-25 ("they are excellent waypoints"), in the order a session
predicted them; the placing was the session's and the tiebreak his.
Two are done the same days they were carded — `grant` (the leash wraps
the fence, the budget applies inside, `done/grant.md`) and `pull` (the
first program of tend's own, which passed the stranger test,
`done/pull.md`) — and `cords` waits on 2026-08-31.  `arrival` was opened and
finished on 2026-08-26, in both trees, through Henri's hand twice
(`done/arrival.md`).*

`keep` and `resolver` finished 2026-08-26 — the grant beside the program, closed for every program tend runs (`done/keep.md`, `done/resolver.md`); the residual, a session exec'ing an arbitrary program, is `work-environment-ai`'s and `session-program`'s.

`gates` finished 2026-08-24, the day it was opened — the hook is
installed, and it has refused a commit once (`done/gates.md` has the
demonstration).

`fence` and `green` finished 2026-08-27, closed in a batch on a
session's verdict and Henri's review — both were built and demonstrated
and had no build left, only a decision (`done/fence.md`, `done/green.md`).
`fence` is up (integrity + blast-radius, both counted); its one open
item, the `display` row, is a widening awaiting a caller, not a debt.
`green` answered its `because` — tend's detectors are sound at the rule
level, and the blindness the sweep found lived only in the wiring
between a detector and what runs it, never in a rule; the standing sweep
is `tools/mutate.sh`, and the two proofs that need an unfenced seat ride
to `done/` as measurement owed to the next outside run.

`install` and `cords` finished 2026-08-27, the same evening, on Henri's
"check that the install and cords are done, and then mark them done if
they are fully done" — checked from both sides first.  `install`
(`done/install.md`): the restraints in force live at
`/usr/local/lib/tend`, root-owned, installed from HEAD and read back by
`tools/install.sh --check`; the tree's copies are the workbench, and a
change to a restraint is an edit in place, a commit through the gate,
and his `sudo tools/install.sh`.  `cords` (`done/cords.md`):
`tools/andon.sh` — ask, ring, be answered — closed its first loop at
17:05, the `audio` row is the socket alone, and `sitting N because
andon` reads the cord's own record.  The outside suite ran 346 with
none skipped.  The residue is `lander` (not yet a card) and the andon
on a node (`session-program`).

`node-install` finished 2026-08-28, the day after it was opened, on the
work laptop it was written for (`done/node-install.md`): `launch.sh NODE
check` said ✗ five times in one morning — the model, the loader, keep's
read boundary, `/opt`, `/sys` — each true from its seat, and the third
run under keep loaded the model, listened, and stopped on idle as the
grant said.  It left `allow-try` in the grant's vocabulary and CPU
progress in the launcher's idea of idle.

`andon-panel` finished 2026-08-28, the day it was opened, on Henri's
"Move andon-panel to done" (`done/andon-panel.md`): the andon's
person-side half, `tools/andon-panel.py` (renamed `tools/panel.py` on 2026-08-29 as the canvas and the hand grew on it), a TUI outside the fence that
watches the record a fenced session writes with no reach row and plays
the andon's own two-note tone through a real player — rung from inside
the fence at 11:03, heard in the next room ("yes, I heard it").  Its
first tone was `curses.beep()`, which terminals mute; that is why the
panel lives outside the fence.  The later views (server, GUI tray) are
widenings awaiting a want; the `audio` row's fix stays `silent-cord`'s.

And displaced cards are in [later/](later/): real, and not being
worked, and each says what it waits on.

## What the days taught

**Every sitting ends with a kaizen — one per sitting, not per
session** — Henri, 2026-08-24: *"it's big thing to do after each
session"*; and 2026-08-27, after 2026-08-26 had 39 kaizens for 14
sittings (`doc/reading-2026-08-27.md`, point 1), the unit is the
**sitting**: the stretch Henri is at the desk, the thing
`tools/limit.sh` measures.  One file per sitting in `doc/kaizen/`,
named `<date>-<HHMM>.md` by when the sitting began — its first commit
after the last kaizen, which the lamp reads from the tree and says —
written when the sitting ends (when Henri closes it, or the clock
does) and covering every commit since the last kaizen, whoever made
them: what went right and why, what went wrong named as whose, what
should change tomorrow.  It is not done when told; it is how a sitting
ends.  **A session that ends while the sitting goes on owes nothing**:
the lamp stays lit and the next session inherits it.  `tools/kaizen.sh`
is the lamp: it lights while there are commits since the last kaizen,
at every commit and (as a hook) at every prompt, says which file to
write — *the sitting is not over until it is written* — and, since
2026-08-27, says the unit and the desk's clock beside the name.
Several sessions a day, and several per sitting, is the normal case
(Henri, 2026-08-24), so the measure is commits, never the date.  And a
session never judges whether it owes another: it says so —
`tools/kaizen.sh want "why"` — and the lamp carries the reason until
the next kaizen lands.  The first, `2026-08-24-1549.md`, is the day
this board went from one test to a hook that had refused a commit —
and the day a session remade gestate's `pgrep` bug an hour after
reading about it, and had to be told to write this.  *Until
2026-08-27 this paragraph said "every session ends with a kaizen"*,
and on 2026-08-26 thirty-nine sessions each wrote one; kept as a
correction rather than rewritten, because the surplus is what
`kaizen-ingestion` is reading.

**A mechanism a session cannot test is proposed, not declared** —
three kaizens on 2026-08-25 (`07:53`, `08:03`, `08:28`, the last
counting itself "the third time in two days"), promoted by the second
ingestion batch (`doc/ingested.md`, 2026-08-27).  What closed the
strand was not this sentence but a route: a claim that cannot be run
from where the session sits goes to the side that can run it — a
gestate session unfenced, or Henri's hand — and until it comes back
the commit says which line has not executed.

**A fixture is a claim about the thing it copies, and it is measured
like one** — three kaizens in one morning, 2026-08-26 (`07:21`, `07:28`,
`07:39`, the last naming itself "the day's one lesson in three faces"
and asking `kaizen-ingestion` to hand it up), promoted by the third
ingestion batch (`doc/ingested.md`, 2026-08-28).  A harness reported a
self-deleting `sed` as GREEN; a `write_text` of a script dropped its
mode and the shim's `exec` was what refused; a fixture of one commit,
or of a grant and a read in the same second, gave the defect and the
correct program the same number.  What closed each was a mechanism,
not care: `tools/mutate.sh` reads the intact copy before any row and
refuses to read below a red one; the scratch copy of an executable is
a copy (`test/test_precommit.py`'s `_scratch` chmods); and a fixture is
built with something on both sides of the seam — two commits, two
seconds — and tried against the defect before its green is trusted.
It was paid a fourth time the next evening (`2026-08-27-1650`: three
fixtures copied a live `.claude/settings.json` and modelled whatever
state Henri had left it in), which is the same rule in its plainest
form: **a test builds the side it means; it never copies the live
thing as it is.**

**To try a change to a protected script, clone the tree — never a
worktree.**  A session cannot edit the protected set (`card:self.md`):
those files are read-only inside the fence.  On 2026-08-27 a session
reached for `git worktree` to get a writable copy and it broke the
tree twice — a git write *inside* a linked worktree rewrites the
shared `.git/config` and flips `core.bare` to `true`, after which
every worktree, the main one included, reports all its tracked files
deleted; and a backgrounded `git rebase` that was killed at its
timeout leaked its change into the main working tree, into
`tools/kaizen.sh`, which the fence binds read-only — so it could not
be reverted from inside at all (`git checkout` on a read-only bind is
"Device or resource busy").  A **clone** has none of this: `git clone
~/tend <scratch>` gets its own `.git`, leaves the original's
`core.bare` untouched, and its copy of a protected file is writable
(the fence binds `~/tend/tools/*`, not the clone).  Edit and run the
suite there with the tree's own venv
(`~/tend/.venv/bin/python -m pytest <scratch>/test/…`) — measured
2026-08-27, the clone's tests pass and the original is never touched.
Landing is the one part the clone does not change: the original can
`git fetch <clone>` from inside the fence (objects only, no
working-tree write), but the `checkout`/`merge`/`pull` that writes a
protected file is still Henri's hand outside the fence — the same
boundary `card:self.md` drew, reached by a pull now instead of a patch
file.  *Corrected the same evening, 2026-08-27, by `install` day two*:
once the hooks run the installed copies at `/usr/local/lib/tend` and
Henri has run `tools/install.sh --free`, the tree's copies are the
workbench — edit a restraint in place, run the suite, commit through
the gate; nothing runs it until his `sudo tools/install.sh`.  The
clone is then for a change to the *installed* mechanism's tests only
if the tree itself is what runs (a fresh clone with no install), which
`tools/fence.sh` says on every prompt.  The paragraph above is kept:
it is the day the tax was measured, and the reason the install exists.

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
6 at the end of the first day — and 7 on 2026-08-26, run by Henri from
inside the fence after the `trees` row was narrowed to the other
tree's documents and tools, which is the row's named purpose shown by
execution.  The audit's one remaining "unkept promise" is gestate's
instruments document, one tend never promised; and its "the fence —
no test names it" is the audit looking for gestate's own gate file
(`test/test_safety.py`) where tend's fence is held by four test files
that name `tools/sandbox.sh` — a fact about the instrument, not the
fence.  The two honest "unbacked" are the consent register and the
author's own document, which exist with nothing in them but their
rule.
That last one is gestate's capped-document list encoding its own
accidents as another tree's requirements, exactly as
`later/rules-and-memory.md` predicted in advance.  That is on purpose: a piece arrives when
something needs it, and the audit is what says the need is still
unmet.  What is not copied from gestate is its prose — the method
documents, the journal, the memories.  What travels is a mechanism and
the evidence that paid for it, one at a time, named where it came from.
