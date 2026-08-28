# kaizen-ingestion — the sittings' lessons pile up and nothing reads them back

    status   open
    because  a kaizen is written at the end of every sitting and nothing
             ever reads it again — 23 of them by the end of the first
             full day, 21 written that day — so a lesson recorded on one
             sitting is re-learned on another, and the same failure
             recurs because no mechanism promotes a recurring lesson from
             the journal to a standing rule.  The journal is write-only;
             it grows and is never gathered
    asked    Henri, 2026-08-25 — "I think that we ingest those kaizen
             bundles at some time and secrete the lessons from them.
             Maybe tomorrow I'll set that up," then "Open the
             kaizen-ingestion card"
    see      doc/kaizen/ — the bundles themselves, one per sitting, the
             raw journal this would read; `tools/kaizen.sh` is the lamp
             that writes them, and an ingestion is its first reader
             board/README.md §"What the days taught" — the practice that
             ends a sitting; this card is the practice that would learn
             from the pile of them
             manifesto.md — where a promoted lesson lands; R10
             (measure, don't assert) is already there, and the question
             this card asks is what else has earned the same promotion
             card:cords.md, card:grant.md (done/), card:keep.md — each
             carries a *count* a session must keep by hand (guessed
             questions, `plain` ledger lines); those counts are lessons
             scattered across cards that nothing gathers either
             board/later/rules-and-memory.md, ~/gestate's memories and
             journal — the shape tend deliberately did NOT copy on
             gestate's say-so (board/README.md); this card is where that
             arrives, on tend's own evidence, if it arrives at all

## What it is

A write-only journal.  Every sitting ends with a kaizen — what went
right, what went wrong named as whose, what should change — and that is
the whole of it: it is written, committed, and never read back by any
mechanism.  A person can read them, but a person does not re-read 23
files before each sitting, so in practice the lessons live once and are
gone.  What is missing is the reader: something that gathers the pile and
brings a recurring lesson forward, so the tree learns across sittings and
not only within one.

## The evidence it has already arrived

The recurrence is not hypothetical.  On 2026-08-25 alone, one lesson
appeared in three kaizens wearing three faces —

* *"a mechanism a session cannot test, it proposes, it does not declare"*
  (08:28),
* *"a workaround in a test is a bug with an alibi"* (14:24),
* *"diff before stage on a protected path — a read-only file that moved
  is a question, not a given"* (15:30).

All three are one rule: **measure the thing before you assert it.**  It
was learned three times in one day because nothing promoted it after the
first.  That is the cost the card names, paid once already, in a single
day's journal.

## What would make this card wrong

If the lessons do not actually recur — if each kaizen's "what should
change" is one-off and never seen again — then there is nothing to
promote and the journal is right to be write-only.  But the day above is
counter-evidence, and the pile only grows.  It would also be wrong if a
person genuinely holds every lesson in head; 21 kaizens in a day says no
one does.

## What it must not become

An auto-summariser that launders the kaizens into bland "lessons learned"
and lets the originals rot.  The kaizens are the primary record and must
stay it — an ingestion produces a *promotion*, cited back to the sittings
that earned it, never a replacement that reads smoother than what
happened.  And it must not become gestate's memory system copied whole on
gestate's say-so; the manifesto forbids adopting a practice that way, and
`board/later/rules-and-memory.md` predicted exactly this temptation.  The
lessons that get promoted are tend's, drawn from tend's journal.

## The hard part, named

A lesson is prose, and promoting prose cannot be fully automated — the
same honest limit the summary lamp and the kaizen lamp already live
with.  So the first slice is likely a *reading aid*, not an oracle:
surface the recurrences — a lesson that appears across N kaizens, the
scattered counts the cards ask a session to keep — and leave the
judgement of what becomes a standing rule to a person or a session.  A
machine that decided what a rule is would be the thing this tree most
distrusts, one level up.

## Where it sits

Placed at 3 by the session that opened it — below `keep`, which is an
active build, and above the count-only and blocked cards — because it is
a real build with buildable work and the tree's first reflective organ.
Henri named it as his to set up ("maybe tomorrow"), so the build is his
lead; the placing is the session's and the tiebreak is his.

## The plan, fixed — 30 kaizens, 10 a day, 2026-08-26 → 2026-08-28, then the arrivals

Henri, 2026-08-26: *"heijunka the kaizens, schedule 10 for each day."*
The shape is gestate's sweep (`~/gestate/board/ungated-fixes.md`
§"The plan, fixed"): a fixed table, equal batches, weekdays, slack
that is not spare capacity, and a missed day that moves down rather
than doubles.  Levelled reading is the reading aid this card's §"The
hard part" asked for, in its first and cheapest form — a person or a
session reads ten, and what each reading produces is one line.

| # | day | kaizens |
|---|---|---|
| 1 | Wed 2026-08-26 | 24-1549 24-1758 25-0626 25-0639 25-0646 25-0703 25-0714 25-0721 25-0732 25-0744 |
| 2 | Thu 2026-08-27 | 25-0753 25-0803 25-0824 25-0828 25-1404 25-1412 25-1424 25-1428 25-1436 25-1445 |
| 3 | Fri 2026-08-28 | 25-1506 25-1522 25-1530 25-1540 26-0721 26-0728 26-0739 26-0743 26-0751 26-0801 |
| 4 | Mon 2026-08-31 | 26-0812 26-0822 26-0847 26-0855 26-0905 26-0910 26-0926 26-0931 26-1304 26-1309 |
| 5 | Tue 2026-09-01 | 26-1317 26-1323 26-1334 26-1342 26-1356 26-1405 26-1412 26-1421 26-1433 26-1437 |
| 6… | Wed 2026-09-02 → | the ten oldest unread, whatever has arrived since |

**A batch is the ten oldest unread**, so the table is what is known
today and a session extends it the day it reads.  Kaizens arrive at
five to seven a day; ten a day absorbs the arrivals and drains the
backlog in three days, after which a batch is most days shorter than
ten and the level holds — a day with fewer than ten unread reads what
there is and does not borrow from tomorrow.

**A missed day is not made up by doubling.**  The batch moves down; the
tail moves out.  Doubling is the burst this arrangement exists to
prevent, arriving with a good excuse — and twenty kaizens in a sitting
is exactly how the journal became write-only.

**The batches get more recent as they go**, and the newest are the
ones this session wrote, which is the reader least able to see them.
Batch 3 is read by a session that did not write it, or by Henri.

### What one reading produces

One line in `doc/ingested.md`: the kaizen's name, the lesson in
a phrase, and a verdict.  Five verdicts, and the vocabulary grows only
for a reason written down after more than one batch has pushed on it
(the sweep's rule):

* **`rule — <where>`** — the lesson is already a standing rule, and
  where it lives is named: a README section, a test, a hook, a script's
  header.  The most common honest answer, if the tree has been doing
  its job.
* **`promoted — <where>`** — this reading made it one, in the same
  commit.  Small: a sentence in `board/README.md` §"What the days
  taught", a line in a script header, a memory.  Not a mechanism — a
  mechanism is a card.
* **`recurs — <kaizens>`** — seen before and not yet a rule; the earlier
  kaizens named.  Two recurrences is the trigger the card's `because`
  is about, and the third reading of one lesson is a `promoted` or a
  reason written down why not.
* **`once`** — one sitting's, no rule wanted.
* **`open — <card>`** — the lesson is a card's work, not a rule's; the
  card named, and the line goes on the card too if it is not there.

**Two uncertain verdicts in a row ends the session** — the sweep's
trip-wire, carried: uncertainty arriving twice is the andon for a
reader writing verdicts faster than reading.

**Henri's half, bounded**: once a week, three lines picked at random,
disagreed with.  Three, not thirty.  It is the only measurement either
party gets of whether the other lines are worth anything.

### What this is not

Not an oracle.  The line is written by whoever read the kaizen, and
the judgement of what becomes a rule stays with a person or a session,
per §"The hard part".  And not a lamp, yet: nothing lights when a
day's batch is unread.  That is the next slice if the schedule slips,
and it is one `ls | comm` against the ledger — cheap, and not built
before the slipping is measured.

**Measured the same hour: the ledger cannot live in `doc/kaizen/`.**
The first draft put it there, and the commit that added it put the
lamp out — `tools/kaizen.sh` reads the newest commit touching
`doc/kaizen/` as the last kaizen, and a ledger is not one.  So the
ledger is `doc/ingested.md`, one directory up, and the lamp's rule is
a `green` row waiting to be written: a file in its directory that is
not a kaizen, and the lamp goes dark.

## 2026-08-27 — batch 2 read; the arrival rate measured against the plan

Batch 2 is in `doc/ingested.md`: ten lines, the ledger's first
`promoted` (one sentence in `board/README.md` §"What the days taught",
cited to three kaizens), two strands at three faces left unpromoted
with the reason written, one strand closed by application, and one
line that is this card's `because` in a grep — a test workaround a
kaizen named two days ago is still in the tree.  Batch 4 is filled in
above; batch 3 stays Friday's and is Henri's or a session's that did
not write it.

**The arrival rate was a number picked in writing, and it was wrong
by five.**  The plan said kaizens arrive at five to seven a day and
that ten a day "drains the backlog in three days."  `ls doc/kaizen`
today: 61 files; 2026-08-26 alone wrote 39 (this section first said 37, an
eyeball count; `ls | grep -c` says 39, as does `doc/reading-2026-08-27.md`).  After Friday's batch,
31 are unread before Monday's arrivals.  The level holds at ten — the
plan's own rule, a missed forecast moves the tail out and does not
double the batch — and the drain claim is withdrawn, not the
schedule.  The lamp slice (§"What this is not": nothing lights when a
day's batch is unread) was to be built when the slipping is measured;
what is measured today is arithmetic, not a missed day.  It waits for
the first one.

**The `see` line's "manifesto.md — R10 (measure, don't assert)"
cites a rule that is not there.**  Neither tend's `manifesto.md` nor
gestate's has an R10; the nearest is §"The three ways an instrument
fails" and rule 2.  The line stays as written with this beside it
(board/README.md: a tree that only ever reads as right teaches
nothing); a reader following it will now find the correction first.

## 2026-08-28 — batch 3 read, by a session that wrote none of it

Batch 3 is in `doc/ingested.md`: ten lines, the ledger's second
`promoted` — the fixture strand, three faces in one morning
(`2026-08-26-0721`, `-0728`, `-0739`), the third of which asked this
card by name to hand it up, now one paragraph in `board/README.md`
§"What the days taught" — and a `grep` ahead of the schedule that
found the same strand paid a fourth time on 2026-08-27 (`1650`),
unread by the ledger: the `because` of this card, measured twice.
The two-tree-card strand (`-0751`, `-0801`) stands at two faces.
Batch 5 is filled in above.

**The count**: 72 kaizens in `doc/kaizen/` today; 30 read; 42 unread
before Monday's arrivals, which at the level of ten is Monday
through Thursday of next week with nothing arriving — and something
will.  No day has been missed yet, so the lamp slice still waits for
the first one.

**Henri's half is due today** — batch 1 sent the self-shaped strand
(`2026-08-24-1758`, `2026-08-25-0626`, `2026-08-25-0732`) to "Henri,
Fri 08-28" because a session may not promote it, and the weekly three
lines at random, disagreed with, have not happened once yet.  Both
are his; neither is a session's to do for him.
