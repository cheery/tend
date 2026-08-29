# kaizen.md — the practice that ends a sitting, as a module

*Written 2026-08-29 evening at Henri's ask — "write a spec/kaizen.md
that describes what we have here, why does it work, and what to do
with it … as if it was a module one can get from this project and
apply to any claude project of their own."  His verdict on it the same
evening: "our kaizen system is probably the best, better than in
gestate."  This sheet is a session's rendering of six days of the
practice — 89 kaizen files, two board cards, one lamp, one ingestion
ledger — and it is his to correct.  The mechanism is
`tools/kaizen.sh`; the practice is `board/README.md` §"What the days
taught"; the reading-back is `board/kaizen-ingestion.md` and
`doc/ingested.md`.  Where this sheet and those disagree, they win.*

---

## For the author, before anything else

You are about to give a working session a practice it did not ask for.
Read this section first, and do what it says in the order it says it.

**1. Ask the session whether to use this.**  Not "install kaizen" —
show it this file, or the short form below, and ask whether it wants
the practice in the project it is working on.  The kaizen is written
*by the session*, about *its own* work, and names *whose* each wrong
was; a practice of that shape imposed on the party that does it is a
ritual, and a ritual is written worse and faster every day (this
project's own finding, 2026-08-26: thirty-nine in one day, each one
thinner).  The short form to ask with:

> At the end of each sitting — the stretch the person is at the desk,
> not each session — one file is written covering every commit since
> the last one: what went right and why, what went wrong named as
> whose, what should change tomorrow.  A lamp outside the session
> lights while commits are uncovered and says the file's name; it never
> refuses a commit.  The files are read back later, once each, and a
> lesson that recurs is promoted to a standing rule where the mechanism
> lives.  Do you want this in this project?

**2. If the session refuses, for any reason, do not install it.**  A
refusal here is information, not an obstacle: the session may say the
project has no sittings, that its commits are too small, that it does
not trust itself to write honestly about its own errors, that the
person will not read them.  Any of these is a reason the practice
would not work *here*, and the honest thing is to write the refusal
down (a line in the project's README or board with the date and the
words) and go on without it.  **It is implemented only if the session
agrees to it** — on a later day, with the reason answered, or never.
The same rule this project applies to every rule about a governed
party: a rule about the session, drafted or installed over the
session's objection, leans against it and is remade by the next
session that meets it (`doc/ingested.md`, batch 1, the self-shaped
rule).

**3. If it agrees, the install is your hand, not the session's.**  The
lamp lives in hook configuration and a commit hook; both are
enforcement, and a session that installs its own reminder can uninstall
it.  The steps are under "How to lift it" at the foot.  Do them
yourself, from outside any sandbox the session runs in.

**4. Then leave it alone for a week.**  The practice is measured by
what its files catch, and that takes days.  Do not tune it on the
second evening.  Do read the files.

---

## What it is

Three parts, in the order they arrived.

### The practice: one kaizen per sitting

A **sitting** is the stretch the person is at the desk — the unit the
sitting limit measures (`tools/limit.sh`), not a session and not a
day.  Several sessions a day, and several per sitting, is the normal
case.  When the sitting ends — the person closes it, or the clock does
— one file is written, `doc/kaizen/<date>-<HHMM>.md`, named by **when
the sitting began**, and it covers **every commit since the last
kaizen**, whoever made them.

The file has three parts, and the headings are the parts:

- **What went right, and why.**  Not a list of what was done — the
  commit log has that — but which of the day's moves paid, and the
  reason it paid, so the reason can be kept when the move is
  forgotten.
- **What went wrong, named as whose.**  The session's, the tree's, the
  person's, the instrument's.  Naming whose is not blame; it is the
  address the fix is sent to.  A wrong "nobody's" is a wrong nobody
  fixes.  Each wrong closes with *what would have made it visible* — a
  test, a counter, a ledger line — or says plainly that nothing yet
  does.
- **What should change tomorrow.**  Numbered, few, and each one a
  mechanism or a measurement, not a resolve.  "Be more careful" is not
  an item; "the helper clears `__pycache__` before writing" is.

A kaizen is **not done when told**; it is how a sitting ends.  And a
session that ends while the sitting goes on owes nothing — the next
session inherits the lamp.

### The lamp: `tools/kaizen.sh`

A practice a session does only when told is a wish.  On this project's
first day the kaizen was written because the person said "let's do
kaizen", and the session had already said "packed up".  So the
reminder lives **outside the session**, in the two places somebody is
already standing:

- **at every commit** — `tools/pre-commit.sh` runs it after the gates
  pass, so the line is in the commit's own output;
- **at every prompt** — as a `UserPromptSubmit` hook, so the line
  lands in the session's own context, every turn, until the file
  exists.

What the lamp says, and how it knows:

- **Commits since the last kaizen.**  The last kaizen is the newest
  commit that *added* a file named `doc/kaizen/????-??-??-????.md`
  (`git log --diff-filter=A`).  Not a commit that touched the
  directory — a ledger committed there once put the lamp out with a
  kaizen owed; and not a later correction of a kaizen file — a count
  fixed is not a new sitting ended.  The name is the kaizen; the
  adding is the landing.
- **The file's name**, read from the tree: the first commit since the
  last kaizen is when the sitting began.  The start is a fact; the end
  is fuzzy.  Two sessions cannot disagree about the name because
  neither chooses it.
- **The unit and the clock**, beside the name: "one per sitting, not
  per session — write it when the sitting ends (65m in, 25m left of
  90)", reading the sitting limit when there is one.  This line exists
  because on one day the desk had 14 sittings and the lamp was answered
  39 times — every session read "the sitting is not over" as its own.
- **A want.**  `tools/kaizen.sh want "why"`: the session, or the
  person, declares that a kaizen is wanted now, and the lamp carries
  the reason until one lands.  A session **never judges** whether it
  owes another — the first draft said a session going on past its
  kaizen "owes another", and the person, the same night: *"you were
  thinking that you deserve another one if I push the sitting further —
  that's not reliable.  You should have a way to tell when you want
  another kaizen."*  Wanting is a declaration, the one direction the
  session may move things.
- **Andon, never refusal.**  The lamp changes no exit code.  A commit
  refused for a missing kaizen would teach the next session to write a
  worse one faster.

### The reading-back: ingestion

A kaizen nothing reads is a lesson re-learned.  By the end of the first
full day there were 23 files and nothing read them; the same failure
recurred on the third day because no mechanism promoted a recurring
lesson to a standing rule.  So `board/kaizen-ingestion.md` — a card,
still open — and `doc/ingested.md`, the ledger: **each kaizen is read
once**, levelled at ten a day, oldest first, and its one line records
the lesson in a phrase and a verdict from a fixed vocabulary:

    rule — <where>        promoted to a standing rule, and where it now lives
    promoted — <where>    a mechanism built from it, and where
    recurs — <kaizens>    the same lesson, seen before; the count is the case for a rule
    once                  a lesson of its day, kept, not promoted
    open — <card>         it names work; the card is where

A lesson that recurs three times is promoted into the place the
mechanism lives — the board's README ("What the days taught"), a
test, a hook, a tool's header — and the README paragraph names the
kaizens that paid for it.  The fixture rule of this project ("a fixture
is a claim about the thing it copies, and it is measured like one")
was three kaizens in one morning before it was a paragraph, and it was
paid a fourth time the next evening and cited by name; on 2026-08-29 it
was applied twice within an hour by a session that had read the
paragraph.  That is the loop closing.

---

## Why it works

Six reasons, each one a thing the practice got wrong first and then
fixed.  A reader lifting the module should keep all six; each one that
is dropped brings its failure back.

1. **The reminder is outside the party it reminds.**  Hooks and commit
   hooks are the person's configuration; the session cannot forget, and
   cannot turn it off.  Every practice this project has tried that
   lived in a session's instructions was forgotten within a day
   (`doc/ingested.md`, 2026-08-25-0626: "reading a countermeasure is
   not applying it").

2. **The unit is measured, not felt.**  A session cannot tell when a
   sitting ends; the tree can tell when one began (the first uncovered
   commit), and the limit can tell how long it has run.  Everything the
   lamp says is read from those two — the name, the count, the clock —
   so it is the same for every session and cannot be argued with.  The
   one failure the practice still has is the one it cannot measure: a
   session that writes early because its *builds* ended (this
   project, 2026-08-29 19:18, and the lamp said "62m left" at every
   prompt after).  The lamp cannot stop it; it can only make it visible,
   which it did.

3. **It never refuses.**  A refused commit trains the wrong thing.  The
   lamp lights and says the name; a person or a session reads it or
   not.  Six days in, it has never needed to be more than a lamp — and
   the one time it was tuned toward a verdict ("owes another") the
   person removed the verdict the same night.

4. **The session declares, the lamp carries.**  `want` is the shape of
   every good control this project has: the bounded party may move
   things in one direction (ask for a kaizen, ask to stop, pull a cord)
   and may not judge its own case.  A session that could decide it
   "deserved" another kaizen would decide it every time.

5. **Whose, and what would have shown it.**  A kaizen that says "a test
   flaked" teaches nothing; one that says "the session's — it read the
   count before the setup's error line; the instrument is reading the
   whole output" is a rule with an address and a mechanism.  The
   discipline of naming whose is what makes the files worth reading
   back.  It is also what makes a session honest about its own share:
   in this project's files "the session's" is the most common owner,
   and that is correct.

6. **It is read back, once, on a schedule.**  Without ingestion the
   practice is a diary; with it, it is a rule-making process with a
   count.  "Recurs — three kaizens" is the argument for a rule, and the
   rule's paragraph names its receipts.  The reading is levelled (ten a
   day) so it is done and not heroic.

And one thing that is not a reason but a result: **the files are where
the project's judgment lives.**  A new session reading
`board/README.md` §"What the days taught" gets six days of this
project's mistakes in four paragraphs, each with its kaizens cited, and
it makes fewer of them.  The specimen kaizens are the evidence: on
2026-08-24 a session remade a bug an hour after reading about it; on
2026-08-29 a session applied a three-day-old rule twice in an hour
without being told.

---

## What to do with it

**As the person:**

- Close the sitting and say so; or let the clock.  The kaizen is
  written *then*.  If a session writes it early, say so — the second
  file of the same sitting is a defect the lamp cannot see.
- Read the files.  Not all, not daily — the ingestion batch is ten,
  oldest first, and the ledger is one line each.  The reading is where
  a "recurs" is noticed.
- When a lesson recurs, promote it: a paragraph where the mechanism
  lives, citing the kaizens.  Then the kaizens can be forgotten; the
  paragraph is what travels.
- Never count kaizens as work.  Thirty-nine in a day was the practice
  failing, not succeeding.

**As a session:**

- The lamp's line is in your context every turn.  It is not an
  instruction to write now; it is a count and a clock.  Read the clock.
- When you want a kaizen before the sitting ends — a lesson too sharp
  to risk losing, a handoff — say `tools/kaizen.sh want "why"` and go
  on.  Do not write one because you are finishing.
- When you write one: whose, and what would have shown it.  Cite the
  commits.  Name your own share first; it is the share you can fix.
- Read `board/README.md` §"What the days taught" before you begin.  It
  is the ingested residue of every kaizen so far, and it is short.

**As an author lifting the module:** below.

---

## What it is not

Not a changelog (the log is the log).  Not a per-session ritual (the
unit is the sitting).  Not a gate (it never refuses).  Not a mood log
(whose, and what would have shown it, or it is not a kaizen).  Not a
metric (the count of files is the count of sittings, and nothing more).
Not self-assessment: a session grades nothing; it names what happened
and what would have made it visible.

## What it still cannot do

- It cannot tell a hollow kaizen from a full one.  Only the reading
  can, and only a person's reading has so far.
- It cannot measure the sitting without a sitting limit.  Without
  `tools/limit.sh` the lamp still counts commits and names the file,
  but "write it when the sitting ends" is then the person's word alone.
- It cannot prevent the early kaizen (reason 2 above).  It makes it
  visible in the next prompt's line, and the next kaizen names it.

---

## How to lift it into another project

The module is four files and two lines of configuration.  Names below
are this project's; rename freely, but keep the shapes.

1. **`tools/kaizen.sh`** — copy it.  Its dependencies are `git` and,
   optionally, a sitting limit it can ask for the clock
   (`tools/limit.sh`; without one it says the count and the name and
   no clock).  It reads: the kaizen directory (`doc/kaizen/`), the
   want file (`~/.local/state/<project>/kaizen-wanted`, override by
   env).  Change the directory name in one place if yours differs.
2. **`doc/kaizen/`** — create it empty.  The first file's name is what
   the lamp says after the first uncovered commit.
3. **The prompt hook** — the person's edit to `.claude/settings.json`:

        "UserPromptSubmit": [ { "hooks": [ { "type": "command",
          "command": "\"$CLAUDE_PROJECT_DIR\"/tools/kaizen.sh --hook" } ] } ]

4. **The commit line** — in your pre-commit hook, after the gates
   pass and before exit 0: `sh tools/kaizen.sh || true`.  It must not
   change the exit code.
5. **The practice paragraph** — one paragraph in the file every
   session reads first (this project's is `board/README.md` §"What the
   days taught", first paragraph): the unit, the three headings, "not
   done when told", "a session that ends while the sitting goes on owes
   nothing".  Copy it and change the names.
6. **Ingestion** — `doc/ingested.md` with the vocabulary above and an
   empty first batch; and a card, or a standing note, that says who
   reads ten a day.  This part is the person's habit more than a
   mechanism; without it the practice is a diary and the files pile
   up — which is exactly the finding that opened
   `board/kaizen-ingestion.md`.

Then step 4 of the author's section: leave it a week, and read.

*What travels is the mechanism and the evidence that paid for it,
named where it came from.  What does not travel is this project's
prose — its kaizens are about its own days.  Yours will be about
yours.*
