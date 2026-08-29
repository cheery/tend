# fixme.md — the defect ledger, as a module

*Written 2026-08-29, late evening, at Henri's ask — "also do
spec/fixme.md in same style as kanban.md and kaizen.md, I think it
deserves that" — an hour after the ledger itself landed at his "we've
reached a point where we need fixme/ -ledger … bit similar design as
the board is, but this is for defects."  This sheet is a session's
rendering of a directory one hour old with four entries, and of the
thing it was cut from: gestate's `fixme.md`, a single file with
F-numbers, whose lesson (`ungated-fixes`: sixty-two repairs named by no
test) is the one rule here that is not the board's.  The mechanism is
`test/test_fixme.py`; the practice is `fixme/README.md`; where this
sheet and those disagree, they win.  Henri's to correct.*

---

## For the author, before anything else

The same three rules as `spec/kaizen.md` and `spec/kanban.md`, for the
same reason: a ledger the session fills, imposed on the session,
becomes a list it stops reading.

**1. Ask the session whether to use this.**  Show it this file, or the
short form:

> One file per defect, `fixme/F000.md`, the number the id and never
> reused.  `shows` names the symptom in whose words it was seen —
> never the fix; `seen` says when and where; `suspected` names the
> cause and is marked suspected until it is measured.  A resolved
> entry moves to `fixme/resolved/` and names the test that would go
> red if the defect came back — or says `none — why` out loud.  A test
> refuses an entry with no symptom, a number worn twice, a resolution
> with no date or no gate, and a citation to no entry.  Do you want
> this in this project?

**2. If the session refuses, for any reason, do not install it.**
Write the refusal down and go on.  A session may say the project's
defects are its tests' failures and need no second ledger, that its
work is too small, that a `gate` it must name does not exist for the
kind of thing that goes wrong here.  Each is a reason it would not work
*here*.  **It is implemented only if the session agrees.**

**3. If it agrees, the session installs it** — the directory, the
shelves, the README, the test on the gate.  Henri's rule for all three
sheets, 2026-08-29: *"the session installs it, not the author … It
doesn't need to be bolted down.  I've proved that you obey it even if
it were modifiable.  You have a morale in that sense."*  The order the
board's first day fixed still holds: the test goes on the gate after
the ledger is clean, never as a way of announcing that it should be.

**4. Then let the session fill it.**  The first entries are the
defects the session has already met — the ones it has been carrying in
a card's prose or a kaizen's "not chased".  Yours are the ones you
name in a sentence; the session writes them with your words in
`shows`.

---

## What it is

### An entry is a file, and the number is its id

    status     open | resolved — <date>
    shows      how it shows — the symptom, in whose words; never a fix
    seen       when and where: a ledger line, a test id, a log, the words
    suspected  the cause, marked suspected until it is measured
    gate       (resolved only) the test that holds it, or `none — <why>`
    see        what it leans on: card:<name>.md, a test, a kaizen

`F000.md`, three digits, the next one past the highest on either
shelf, never reused — so a comment, a commit message or a card may
cite `F000` and the citation resolves a year later.  Positional
numbering is what gestate's board replaced with names; a defect
ledger keeps numbers because a defect is *found*, not *placed*, and a
number says nothing about priority.  Below the block, dated prose, as
a card grows: what was measured, what was tried, what was found.

**`shows` names a symptom.**  The board's rule for `because`, carried:
an entry whose `shows` names the fix has skipped the part a reader can
check.  "The window rule stops a slow-starting program" is a cause; "a
test fails in the gate at no load and passes on retry, 2 of 4 runs"
is what showed, and it is the line a reader can go and reproduce.

**`suspected` is marked so.**  The first guess at a cause is the part
most likely to be wrong and the part a reader trusts most (gestate's
board, 2026-08-17: "an elaboration's mechanism guess is a guess, and
should say so").  An entry may say *measured, not suspected* in that
field once it is; until then the word stands.

### Two shelves, and the gate

`fixme/F*.md` is open: the defect stands.  `fixme/resolved/` is
closed: the defect no longer shows, **and the entry names the gate
that holds it** — the test id that goes red if it comes back — or says
`none — <why>` out loud.  A move never renames.

This is the one rule that is not the board's, and it is the ledger's
reason to exist.  gestate's `ungated-fixes` card: of 161 defects in its
`fixme.md`, 79 and then 62 were repaired and named by no test, so a
defect closed on a photograph could come back with nobody told.  Taken
here on day one: a resolution with no gate is a resolution on trust,
and the entry says so where the next reader will see it.  Two of
tend's first four entries are `none —` resolutions, and each says why
— a harness's trust step that does not cover signing; a fixture whose
proof is a live file staying absent, which a test could not assert
without knowing the path the fixture hides.  Saying so is the point.
A `none —` resolution is said to the person before it lands.

### Citation

`F000`, bare, in prose, in a comment, in a `see` line, in a commit
message.  Another tree's number carries its tree — `gestate:F182` — so
two ledgers cannot be confused.  `test/test_fixme.py` resolves every
bare citation in `fixme/` and on the board, with a baseline for the
citations older than the ledger (one, in a done card, which is history
and is not rewritten) that may shrink and never grow — gestate's own
proposed shape for a rule applied only to what comes after it.

### The test

`test/test_fixme.py`, on the commit gate:

- the ledger exists with both shelves;
- every entry is `F<three digits>.md`, and no number is on two shelves;
- every entry has `status`, `shows`, `seen`;
- a resolved entry is in `resolved/`, says when, and names its gate;
  an open one is not in `resolved/`;
- every bare `F` citation resolves on some shelf, less the baseline.

Five checks, all shape.  Nothing checks whether `shows` is a symptom
or `suspected` is honest; a reader does.

### What goes here, and what does not

A race, a wrong rule, a harness that lies, a fixture that leaks —
something *wrong* that can be shown wrong.  Not work to do (a card);
not a lesson (a kaizen); not a want (a card's "not built" line).  A
defect found while working a card gets an entry, and the card cites
it; a card whose `because` is one defect cites the entry and says why
it is a card — usually because the fix is a design decision, which is
the board's business and not the ledger's.

---

## Why it works

Written an hour after the ledger landed, so these are the reasons it
was *built*, each one a thing that had already gone wrong without it.
The week will say which held.

1. **A defect had nowhere to sit but prose.**  Before the ledger, a
   defect found while working a card lived in the card's dated
   sections ("not chased; named as owed"), and a defect found by a
   kaizen lived in "what should change tomorrow".  Both are read once.
   The evening the ledger landed, its first four entries were lifted
   out of exactly those places — a race on a card, a rule on a card, a
   harness fault in a kaizen's item 5, a fixture leak in a commit
   message — and each now has a number a test can cite.

2. **The number is stable and the shelf is not.**  Same as the board:
   a citation that names a path breaks on every move, and a defect
   moves exactly once, from open to resolved.  A test that cites
   `F000` in its docstring is right forever.

3. **A resolution names its gate or confesses.**  The ledger's own
   rule, and the one that makes the resolved shelf worth reading.
   Without it "resolved" means "somebody stopped seeing it"; with it,
   "resolved" means a named test would say if it came back, or the
   entry says in so many words that nothing would.  gestate paid
   sixty-two repairs to learn this; tend paid nothing, which is what
   a lesson taken across trees is for.

4. **Symptom before cause, and the cause marked.**  An entry that
   opens with the cause has decided; an entry that opens with what
   showed — the ledger line, the count, the assertion text — can be
   picked up by a session that disagrees with the cause.  F001's
   `suspected` says "not the per-second granularity — that was fixed
   and the count did not move", which is a cause *refuted* on the
   entry, and the next session starts from there.

5. **It sits beside the failure ledger.**  `tools/suite.py` counts
   what failed, where, under what load; an F-entry is where that
   count becomes a defect with a name.  The evening's first catch went
   ledger line → card note → F000 in twenty minutes, and the card's
   note is now one line pointing at the number.

6. **Shape on the gate, judgment in the reader.**  Five mechanical
   checks; the gate has already refused once (a bare gestate number in
   this ledger's own README, which is how the `gestate:` rule was
   found — the test wrote the rule).

---

## What to do with it

**As the person:**

- Name a defect in a sentence; the session writes the entry with your
  words in `shows`.
- Read the open shelf when you sit down — it is short, and an open
  entry with a `suspected` that has stood for days is the one to ask
  about.
- When a `none —` resolution is brought to you, ask what *would* hold
  it.  Sometimes the answer is a test nobody thought to write.

**As a session:**

- Found something wrong while working a card?  An entry, now, with
  the line that showed it, then back to the card, which cites the
  number.  Do not carry it in prose.
- Resolving one: name the test id in `gate`, or write `none — <why>`
  and say so to the person before it lands.  Never resolve on a retry
  that passed.
- The failure ledger's lines are `seen` material: quote them.
- Cite `F000` bare; another tree's number with its tree.

**As an author lifting it:** below.

---

## What it is not

Not the board (work to do has a card).  Not a test-failure log (the
failure ledger counts; this names).  Not a changelog.  Not a place to
propose fixes — `suspected` is a cause, and the fix is the card's or
the commit's.  Not gestate's single file: one file per defect so two
writers never touch one file, the board's own rule.

## What it still cannot do

- It cannot tell a symptom from a cause; a reader can.
- It cannot know that a `gate` still guards what it says it guards —
  a test renamed or deleted leaves a resolved entry pointing at
  nothing.  A check that every named gate is a test id that exists is
  the next test, and the day an entry's gate goes missing is the day
  it is written.
- It is an hour old.  Everything above "why it works" is a reason it
  was built; the reasons it works are a week away.

---

## How to lift it into another project

1. **`fixme/`** with `resolved/` inside, and `fixme/README.md` — the
   block, the two shelves, the gate rule, the citation form.  Copy
   tend's and change the names.
2. **`test/test_fixme.py`** — copy it.  It reads `fixme/`,
   `fixme/resolved/`, and the board's files for citations; the paths
   are at the top, the baseline set is empty for a new tree, and the
   citation regex skips `<tree>:F000`.  Keep all five checks.
3. **The gate** — after the ledger is clean.
4. **One line where defects used to go** — the board README, or
   wherever "not chased" was being written: *a card is work to do; an
   F-number is something that is wrong.*

Then step 4 of the author's section: the session lifts its carried
defects into the first entries.

*What travels is the shape, the gate rule, and the test.  What does
not travel is tend's entries: they are tend's defects.  Yours will be
yours — and the first four will probably be the ones you already know
about and have been carrying somewhere worse.*
