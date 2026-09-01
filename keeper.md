# keeper.md — standard work for the person, and today it is one act

*Written 2026-09-01 at Henri's ask — "I need a keeper.md -file that
describes the act of seeking the self-shaped -records and marking them
approved with date" — on the day the first four marks were written and
struck within minutes of each other.  `~/gestate/keeper.md` is the same
page in the older tree and has six acts; this one has one, because a
piece arrives when something needs it and what needs a page today is the
mark.  The other acts come when they are asked for.*

---

## Who this is for, and what it is not

**Henri.**  A session does not read this file to do its work.
`board/README.md` is what a session reads before it knows what it is
working on; this is not read before the work — it **is** the work, and
the one person who does it is the one it is addressed to.

**And it is never a demand.**  `vision.md`: *won't demand your
presence.*  Nothing on this page can fail a commit, there is no streak,
and there is no lamp for it yet on purpose.  A mark left unanswered for
a month is not a failure of anything: the rule it stands on is still a
rule the tree follows — it simply has nobody behind it, which is exactly
what the mark says out loud.  *(gestate, `keeper.md` §"Who this is for"
— borrowed whole, and the reason travels with it: a metabolism that
punishes an absence breaks the line that makes the tree safe to own.)*

---

## 1. Strike the marks

**About two minutes**, at four marks.  Do it whenever; a session should
say at the end of a sitting if it wrote one.

### Find them

    grep -rn -A2 '^\*(self-shaped' *.md board/ spec/ doc/

Every hit is a mark and nothing else is — the bracket and the anchor
were both chosen by measurement (`manifesto.md` §"How a practice gets
adopted").  The ones still waiting are those with no `henri:` line
under them.

### Read the rule, not the mark

The mark is a label; the thing to read is the **paragraph above it**.
That is the rule a session wrote about how sessions work, and the
question in front of you is not *is this well written* but:

> **Would I have drawn the boundary here, if I were not the one who has
> to live inside it?**

That is the whole reason the mark exists.  A session drafts the version
it can already comply with, optimises hard inside that boundary, and
never thinks to test the boundary — so the lean to look for is rarely
self-serving and usually a failure of imagination.  The question a
session did not ask is more often the defect than the answer it gave.

### Write one line, in your own hand

At the end of the mark, on its own line:

    henri: approved 2026-09-01

Lowercase `henri:`, and the date you read it.  The lowercase is what
makes it findable — `Henri:` capitalised is the tree's attribution form
and stands in over a hundred places, a session quoting you; `henri:` is
you speaking.

Everything after the colon is yours.  These are all fine:

    henri: approved 2026-09-01
    henri: no — the second half claims more than the kaizens showed
    henri: not yet, ask me again when there is a third face

Only a dated `approved` is read by the gate as a claim about the text.
A refusal or a question is a sentence to the next session, and it stays
on the mark until something is done about it.

### What you are not being asked to do

Delete the mark.  You wrote the answer *into* it on the day this
started, rather than removing it, and that turned out to be the better
form: the record keeps both halves — that the rule was self-shaped, and
that you stood behind it — where a deletion would have kept neither, and
a reader next month could not tell a rule you approved from a rule
nobody ever questioned.  So a mark is permanent once written.  What
changes is the line under it.

---

## What happens after you write it

`test/test_marks.py` binds the approval to the words you read.  For each
mark it takes the rule above — excluding the mark's own lines — and goes
red if that text is committed or edited after your date.

**So editing an approved rule un-approves it.**  If a session reworks a
rule you have stood behind, the commit stops, and the message names the
file, the line, your date, and the remedy: clear the verdict and put the
rule back to you.  That is the point of the date.  Without it, an
approval drifts silently onto words you never read, and rewriting an
approved rule would be the cheapest way for a session to widen its own
boundary.

Two things it deliberately does not do, so you know its edges:

- **Day granularity.**  You write a date, not a clock time, so a rule
  edited later on its own approval day passes.  Asking you to type a
  timestamp is a worse trade.
- **It reads the tree as it is.**  If you rewrite a mark yourself, that
  is the authority it defers to, not something it audits.

---

## Why this page has one act and gestate's has six

`~/gestate/keeper.md` is a weekly fire — lamps, a decisions batch, a
rule measured against the week, a pass over the pile, the journal
rotated, the pieces pushed.  None of that is carried here.  What travels
between these trees is a mechanism and the evidence that paid for it,
one at a time, named where it came from (`board/README.md`, last
paragraph) — and what paid for this page is four marks written and
struck on 2026-09-01.  When a second act is needed, it will be because
something needed it, and it will say so here.

*(self-shaped, 2026-09-01 — a session wrote the procedure by which its
own rules get approved, which is the sharpest case the mark exists for.)*
