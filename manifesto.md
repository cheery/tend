# manifesto.md — how this project is worked

`vision.md` says what tend is for.  `board/` is what is being worked.
This file is the method they are written under — carried from
`~/gestate/manifesto.md` on 2026-08-24, the day tend started, and
carried *as rules, not as evidence*.

**Every claim here cites the thing that proves it**, and at the
carrying every citation pointed at another tree.  That was the honest
state, said out loud rather than faked: gestate's manifesto paid for
each of these with a number of its own, and tend had measured nothing.
A sentence with a citation into gestate is not unfinished — it is
*borrowed*, and it says so.  A section earns its own number here, or it
stays a citation.  The first section paid for here is §"Go and see"
(2026-08-31, F005 and F006).  What was not carried is everything that was a
number: the instruments table, the costs of visibility, the six
measured lessons, the shape of a good day.  Tend will have its own or
none.

*Drafted by a session at Henri's ask; the rules are his and gestate's,
the choosing is his to strike.*

---

## Two rules, and they are one idea

> **1. Do not build what nothing needs.**
>
> **2. What is built must be able to say when it is wrong.**

A feature earns its place by having a *caller* — a program somebody
wants to run, an unmet obligation, or a defect it fixes.  "It is in the
notes" is not a caller.  And a thing with a caller has somebody who is
hurt when it is wrong, so being wrong has to be visible — to something
that is not a person's attention, because attention is what runs out.
They meet in the one exception both share: **a defect is always a
caller.**  *(gestate, `manifesto.md` §"Two rules, and they are one
idea" — paid for there by F64 and F58; not yet paid for here)*

## The three ways an instrument fails

**It lies.**  Read a new instrument's first surprising number as a fault
in the instrument until it is not.

**It has never failed.**  An oracle that has only ever passed is a
claim.  Break the system and watch it notice, before the check is
committed.

**It was built from the implementation.**  A harness written by reading
the code can only confirm what the code does; it cannot find a missing
affordance, because it never reaches for one.  State the strongest
assertions in a vocabulary the implementation does not own.

*(gestate, `manifesto.md` §"The three ways an instrument fails" — three
incidents there, none here yet; the first instrument tend builds should
be broken on purpose before it is trusted)*

**Tend's own three, for the second way, all on 2026-08-27** — the
citation above said "none here yet" and was true when it was written.
Promoted here by `doc/ingested.md`'s batch 7, which found one lesson
wearing three faces in a single day's kaizens:

- a test asserted `"sitting" not in stdout`, and pytest's tmp path
  carries the test's own name — it failed loudly here, but the same
  assertion in a test named otherwise would have passed while checking
  nothing (`doc/kaizen/2026-08-27-0538.md`);
- a toolbox test read the runtime `✓` line for a reason dash that a
  *present* tool never prints — reasons appear when a tool is absent
  (`-0710`);
- the test guarding the installed copies' mode asserted only *not
  writable by owner*, which the defective `533` — `755 - 222` computed
  in decimal — satisfies.  So `sudo tools/install.sh` left every hook
  `Permission denied`, and it cost Henri a prompt to find (`-1602`).

Each was written by a session that had read this rule.  What the three
share is not carelessness: **an assertion is written against the
passing path, because the passing path is the state its author has in
mind.**  The check that would have caught each is the same and it is
cheap — show the check red against the defect it names before trusting
it, which `tools/mutate.sh` does for the detectors and a red-first test
does for everything else.  The sentence stops being borrowed on the day
tend paid for it three times.

## How a practice gets adopted

**A good practice is adopted before it is believed.**  There is a
stretch where it is overhead carried on somebody else's say-so, and it
has to survive that stretch to be owned.  Henri, 2026-08-17, on
gestate's suite: *"Imposed, tolerated, owned."*

Two things follow: **a practice must be cheap enough to tolerate while
it is unproven**, and **whoever introduces it owes the demonstration** —
*this is what it caught, that you would have shipped.*  A practice you
cannot demonstrate is one you are asking to be trusted on, and the
honest move is to say so.

*(gestate, `manifesto.md` §"How a practice gets adopted".  **This is the
rule tend needs first**: every mechanism arriving here from gestate is
in the tolerated stretch, and each one owes tend a demonstration of its
own before it is owned here.  The two paragraphs above are gestate's;
what follows is tend's own, and Henri's.)*

**A rule about sessions, drafted by a session, says so until Henri strikes the mark.**
A session may write one — it is closest to the work, and a standard
written by someone who does not do the work is fiction. What it cannot do
is approve its own. A session drafts the version it can already comply with,
optimises hard inside that boundary, and never thinks to test the boundary.
So the draft carries (self-shaped) where it stands, the way an F-entry's cause
carries suspected, and only Henri's hand takes it off.
**Marked, it is a rule the tree follows and nobody has yet stood behind. Unmarked, he stands behind it.**

**An example of a marked paragraph.**  The rule below is real — it is
`board/README.md` §"What the days taught"'s newest, promoted by an
ingestion batch on 2026-09-01 — and what is being shown is its tail:

    **A check has three verdicts, not two: ✓, ✗, and "not from this
    seat."** — three kaizens on 2026-08-28 … the mechanism, where it
    exists, is the third verdict printed as its own line:
    `tools/launch.sh:302` prints `· … not checked from here` instead of
    a ✗.  Two call sites; every other `--check` in the tree still has
    two verdicts.
    *(self-shaped, 2026-09-01 — a session wrote this rule about
    sessions; nobody has stood behind it.  Henri strikes the mark.)*

The mark is the last line, it goes where the rule ends, and it is
searched for **with its opening bracket**:

    grep -rn '(self-shaped' board/ manifesto.md spec/ doc/

The bracket is what makes it findable.  The bare words name the strand
itself in two dozen places across the ledger, the cards and the kaizens
— *"batch 1's self-shaped strand"* — and a search for those returns the
discussion and drowns the marks in it.  The first hit will always be this
example; every hit after it is a rule waiting on Henri.

*(The countermeasure is not new here.  A session named it on 2026-08-24
— "it marks the draft *self-shaped until Henri reads it*, in the header,
the way the elaboration rule marks a mechanism *suspected*" — and again
on 2026-08-25, where `spec/os.md` was to carry one and never did.  This
is its third naming in nine days and the first time it exists.  Which is
`card:kaizen-ingestion.md`'s `because` in one more form: the countermeasure
was written down twice and read by nobody.)*

## Set-based, not point-based

Henri, 2026-08-17: *"I intentionally didn't say directly that the button
should be made bigger, because it's not necessarily the whole answer to
it, or correct answer."*

Point-based design picks one answer early and iterates on it.
Set-based keeps several alive, states what would kill each, and
converges last.  It matters more with a model than with a team, because
a model's one fluent answer arrives already defended — the fluency *is*
the convergence — and a review cannot see what was never offered.  The
board's form of it: **a card's `because` is a problem, never a fix.**

*(gestate, `manifesto.md` §"Set-based, not point-based" — Ward, Liker,
Cristiano and Sobek, *The Second Toyota Paradox*)*

## Go and do it

Taiichi Ohno, in Henri's translation from the Finnish edition,
2026-08-18:

> There are many things one does not understand, and therefore we ask:
> why not just go ahead and take action?  **Do something.**  You will
> come to realise, in the doing, how little you knew — you will see your
> own failures, and you can correct those mistakes; and try again, and
> at the second trial find another mistake, or another thing you do not
> like, and correct that, and try once more.

Going to the actual place is worth nothing if you arrive and reason
instead of touching anything; **a hypothesis you did not test is a
hypothesis that gets written into a commit message as though it were a
finding.**  And the second half is the method, not a sign of doing it
badly: act and you will see your own failures.

*(gestate, `manifesto.md` §"Go and do it")*

## Go and see

**A diagnosis is believed when the mechanism has been made to show
it — not when the signal matches a story.**  The error message, the
pattern it fits, the first fluent explanation: none of these is the
thing.  Before a fix is written — and before any act that changes
state on a signal's say-so — go to the actual mechanism and make it
show the failure; a signal that pattern-matches a known cause may
have a different one.  This is §"Go and do it"'s other half: doing
shows you your failures, seeing is how you read them without being
lied to — the same move §"The three ways an instrument fails" makes
on instruments, pointed at diagnoses.

*Paid for here, 2026-08-30, by F005 and F006 — the first number in
this file that is tend's own; into the manifesto at Henri's ask at
that day's close.*

**F005**: a test timed out at exactly thirty seconds, in a commit
that touched nothing near it.  The story that fits is a flaky test.
The measurement — the fixture run alone, then by hand under the
test's own environment — showed exit 0 after 36 s with every state
file stamped in the pull's own second: the pull was polling 600 ×
50 ms for a lock a runner dead at the loader had already dropped.
The thirty seconds was the poll's cap, not the test's mood, and the
suite had passed the commit before only because the race had been
landing on the right side of a 50 ms window.

**F006**: a commit died on "invalid object … for tools/suite.py"
after the gates had passed — a file not in the commit, unchanged,
`fsck` clean.  The story that fits is corruption, or the hook.  The
measurement — a scratch repository whose hook prints
`GIT_INDEX_FILE`, tried under both commit forms — showed that a
pathspec commit hands its hook an *absolute* temporary index, that
the variable is honoured across repositories, and that a scratch
test's `git add -A` had filled the tree's temporary index with a
blob only the scratch store held.

Both stories were fluent, both were wrong, and both measurements
were cheap next to the fix they would have misdirected.  And the
seeing is only half: each entry's `gate` line names a test shown red
without the fix, because a diagnosis that was measured deserves a
gate that keeps it — that is rule 2 closing over rule 1's exception,
a defect being the caller.

---

## The whole method, in one sentence

> **Being wrong has to be visible, and the thing that makes it visible
> has to be checked against being wrong.**

*(gestate, `manifesto.md` §"The shape of a good day" — the sentence is
carried; the day that earned it is not)*
