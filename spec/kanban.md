# kanban.md — the board, as a module

*Written 2026-08-29 evening at Henri's ask — "write a spec/kanban.md,
describe it the same way as the kaizen.md."  This sheet is a session's
rendering of tend's board: one directory, nine open cards, thirteen
done, one shelved, seven tests, six days.  The board came to tend from
`~/gestate`, where the method grew; the session that wrote this could
not reach gestate's board from its seat (the `trees` reach row was off
for the session), so what is said here about gestate is what tend's own
README records having taken from it, and nothing more.  The mechanism
is `test/test_board.py`; the practice is `board/README.md`; where this
sheet and those disagree, they win.  Henri's to correct.*

---

## For the author, before anything else

You are about to give a working session a way of holding its work that
it did not ask for.  The same rule as `spec/kaizen.md`, for the same
reason.

**1. Ask the session whether to use this.**  Show it this file, or the
short form below, and ask whether it wants the board in the project it
is working on.  A board is written mostly by sessions — cards, moves,
the placing of a new card — and a board imposed on the party that
fills it becomes a to-do list it stops reading.  The short form:

> One file per task, in one directory.  A card opens with `status`,
> `because`, `asked`, `see`.  `because` names a **problem** in the
> words of whoever had it — never a fix.  Open cards sit in the
> directory; finished ones move to `done/`, waiting ones to `later/`
> with what they wait on; a move never renames the file, and a card is
> cited by name, not by path.  The README lists every open card in
> priority — priority, not order — and the tiebreak is the person's.  A
> test refuses a card without a `because`, a card on the wrong shelf,
> an open card the README does not list, and a citation that resolves
> to no shelf.  Do you want this in this project?

**2. If the session refuses, for any reason, do not install it.**
Write the refusal down — where, when, the words — and go on without
it.  A session may say the project has one task and needs no board,
that its work is not card-shaped, that a `because` it must write in
someone else's words has no someone.  Each is a reason the board would
not work *here*.  **It is implemented only if the session agrees** —
later, with the reason answered, or never.

**3. If it agrees, the install is yours** — the directory, the README's
first priority list, the test on the gate.  The gate is enforcement,
and a session that installs its own gate can lift it.  And one thing
this project learned on its first day (`board/README.md`, first
paragraph): **a gate is turned on after the tree is clean, never as a
way of announcing that it should be.**  Write the first cards, make the
test pass, *then* put the test on the hook.

**4. Then fill it yourself, first.**  The first cards are the person's:
the problems you have, in your words.  A session placing a card it
wrote is the normal case later; the board's first shape is yours.

---

## What it is

### A card is a file, and the filename is its id

    status   open | doing | blocked | done — <date> | shelved — <date>
    because  the problem, in the words of whoever had it — never a fix
    asked    who, when, and the words
    see      what it leans on

Four spaces in, the field name, two spaces, the value.  Below the
block, the card's prose: the problem at length, what day one would be,
the rules it must keep, what would make it wrong, what it must not
become.  A card grows as it is worked — each pass appends a section
with the date and the words that steered it — and the file is the
history of the problem, not a ticket that closes.

**`because` names a problem.**  This is the board's most expensive
lesson and the one thing the test enforces about content: a card whose
`because` names a solution has already decided, and the deciding is
what the card is for.  The card that read *"name datatypes, e.g. `type
Duration = Float`"* named a fix; the need behind it — *"I do not
figure out quickly enough which argument in lowpass filters is which"*
— turned out to have nothing to do with types.  The test checks
presence, not wisdom: no test can tell a problem from a solution.  It
can refuse a card that answers neither.

**`asked` carries the words.**  Who asked, when, and what they said —
verbatim, in quotation marks.  A card that says "Henri asked for a
hold" has lost the thing a later reader needs; one that says *"Lets
card it"* at 2026-08-29 has kept it.  Every section a session adds
opens the same way: the date, the words that steered it.

### Where a card is

`board/*.md` is open work.  `done/` is finished — **the problem no
longer stands**, which is a different thing from "the build is
merged".  `later/` is real and not being worked: it waits on an event
or on a decision, and it says which.  A `blocked` card names what it
waits on, in the block.  Moving between shelves never renames the file.

**Cite a card as `card:<name>.md`**, never by shelf path: the notation
resolves on whichever shelf the card is, so a move to `done/` breaks
nothing.  Taken from gestate's board on 2026-08-27, the day closing two
cards broke every path citation in the summaries — "it starts to
matter slowly".  The test resolves every citation in every card, the
README, and the summaries; kaizens are history and are not checked (a
kaizen may name a card that was later folded away).

### The priority

The README lists every open card, with a line each: what the problem
is, and — in italics — who placed it where, when, at whose words, and
that the tiebreak is the person's.  **Priority, not order:** what to
work on next is priority filtered by what can be worked today, and the
filter changes daily.  A new card arrives **placed last** by the
session that wrote it; moving it up is the person's act.  A session
never reorders.

Below the list, the README keeps a paragraph per finished card — what
it was, when it closed, what it left — and a section, "What the days
taught", where the kaizens' recurring lessons are promoted to
paragraphs.  The README is the first thing a session reads;
`CLAUDE.md` says so in one line.

### The test

`test/test_board.py`, on the commit gate:

- no two cards wear the same name across shelves;
- every card has `status`, `because`, `asked`;
- a `done` or `shelved` card says when;
- a card marked done is in `done/` and an open one is not;
- a `blocked` card names what it waits on;
- the README lists every open card;
- every `card:` citation resolves on some shelf.

Seven checks, all about **shape**, none about judgment.  The test has
refused a commit for a because-less card (`done/gates.md` has the
demonstration), and `tools/mutate.sh` keeps a row that commits one to
prove the refusal still fires.

---

## Why it works

Six reasons, each one a failure this board or its parent had and
fixed.  Drop one and its failure returns.

1. **The problem is separated from the fix at the door.**  A board of
   fixes is a board of decisions already taken by whoever was tired
   when they wrote the card.  Requiring `because` to name a problem —
   and keeping the words it was had in — leaves the deciding to the
   session that works it, on the day it is worked, with what is known
   then.  Tend's `hold` card was carded as "a `<name>.hold` file beside
   the pin" and built as a filename-keyed hold; the `because` said
   "node+state is being pulled", and reading it back against the build
   is what turned the second pass.  The `because` is the part that
   survives a wrong first build.

2. **The file is the history.**  A ticket closes; a card grows.  Every
   pass is a dated section in the card, with the words that steered it,
   so a session picking the card up reads the arc — day one, the
   review, what was found red first, what is still not built — and
   not a status.  This is why tend's cards are long, and why a new
   session reads one and knows what the last one knew.

3. **Shelves are facts, and moves cost nothing.**  `done/` means the
   problem no longer stands; `later/` means it waits on a named thing.
   Because a card is cited by name and never by path, a move is `git
   mv` and nothing else breaks — so cards actually move, and the open
   shelf is actually the open work.  Boards where a move breaks links
   stop moving cards, and then the open shelf lies.

4. **Priority is the person's; placing is the session's.**  A session
   that could reorder the board would reorder it toward what it wants
   to build.  A session places a new card *last*, says so in the
   README line, and names the tiebreak as the person's.  The person
   moves it up or does not.  Six days in, the line "placed last by the
   session that wrote it … the tiebreak is his" is on every card that
   arrived that way, and the person has moved two.

5. **The test holds shape and refuses wisdom.**  Seven checks, all
   mechanical, all on the gate — so a card cannot be malformed, cited
   wrongly, or forgotten from the README, and the gate has refused for
   each.  Nothing checks whether a card is worth working; that is what
   the README's prose and the person are for.  A test that tried to
   judge would be argued with; one that holds shape is obeyed.

6. **The README is read first, and it says what the days taught.**
   The board is not the directory; it is the README, which every
   session reads before anything (one line in `CLAUDE.md`).  It carries
   the priority, the finished cards' one-paragraph residue, and the
   promoted lessons with their kaizens cited.  A new session inherits
   six days of judgment in one file, and the file is short because the
   cards hold the length.

And the result these six add up to: **a session can pick the project
up cold.**  "Let's see what we have on board" on the evening of
2026-08-29 was answered from the README, the two `doing` cards' tails,
and the last kaizen — three reads — and the session knew which two
decisions the board was parked on.

---

## What to do with it

**As the person:**

- Fill the board.  Your problems, your words, in `because` and `asked`.
  A card a session writes for you should quote you.
- Move cards up.  A session places last; the priority is yours, and
  the README line records that you moved it.
- Close cards when the problem no longer stands — not when the build
  lands.  Say "move X to done" and let the session check both sides
  first (tend's `install` and `cords` were checked from both sides
  before closing, at "check that … are done, and then mark them done if
  they are fully done").
- Read the README's "What the days taught" when it grows a paragraph.
  That is the kaizens reaching the board.

**As a session:**

- Read `board/README.md` first, then the `doing` cards' tails, then
  the last kaizen.  That is the pickup.
- A new card: `because` in the person's words or the problem's own,
  never a fix; `asked` verbatim; placed last in the README with the
  italic line; `see` what it leans on.  Then the test.
- Working a card: append a dated section, open it with the words that
  steered the pass, say what was measured and what was not, name what
  is still not built.  Never rewrite an earlier section — a card that
  only ever reads as right teaches nothing.
- Cite `card:<name>.md`.  Never a shelf path.
- Never reorder the priority.  Never move a card to `done/` on your
  own verdict; say it is done and let the person say the word.

**As an author lifting it:** below.

---

## What it is not

Not a ticket system (a card grows; it does not close).  Not a plan
(priority, not order; and the filter is daily).  Not a changelog (the
finished-card paragraphs in the README are residue, not history; the
log is the log).  Not a place for fixes (a `because` that names one is
refused by the reader if not by the test).  Not a session's to-do list
(the person fills it; the session places last).

## What it still cannot do

- It cannot tell a problem from a solution; the test checks that
  `because` is there, and a reader checks what it says.
- It cannot stop a card from being worked in the wrong order; it can
  only make the order and its owner visible.
- It has no view but the directory and the README.  A board with
  thirty open cards would need one; tend's has nine.

---

## How to lift it into another project

Three things and a line.

1. **`board/`** with `done/` and `later/` inside, empty.  Write
   `board/README.md`: what a card is (the four fields, the rule for
   `because`), where a card is (the three shelves, the `card:` notation),
   and a priority list — empty is fine; the first card fills it.
2. **`test/test_board.py`** — copy it.  It reads `board/`, `board/done`,
   `board/later`, `board/README.md`, the root README, and
   `doc/summary/*.md` for citations; rename paths in one place at the
   top.  Its seven checks are named above; keep all seven.  Its
   docstrings carry the reasons and are worth keeping whole.
3. **The gate** — whatever runs your tests before a commit.  Add the
   test *after* the board is clean (author's step 3).
4. **One line in `CLAUDE.md`**: *please read board/README.md before you
   begin.*  That line is the whole pickup mechanism.

Then step 4 of the author's section: the first cards are yours.

*What travels is the shape and the test, and the reasons in the
docstrings.  What does not travel is tend's cards: they are about
tend's problems.  Yours will be about yours.*
