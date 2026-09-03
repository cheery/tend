# questions — a question raised for the person has no home, and nothing gathers it

    status   shelved — 2026-09-03
    because  a session raises questions all day and each one is written
             into whichever card or F-number it arose in, so the set of
             things actually waiting on Henri exists nowhere.  On
             2026-09-01 eight were collected **by hand**, because a grep
             cannot do it: a card's prose mixes settled history with open
             decisions, and searching for "the person's call" returns
             fourteen files and mostly returns the past.  The gathering
             has to happen when a question is written, not by searching
             afterwards — and until it does, his own rule ("collect up
             the questions that appear, wherever they belong, and pass me
             the info") is a rule with no mechanism, which this tree
             already knows is a rule that gets re-learned
    asked    Henri, 2026-09-01 — the rule itself, loaned from gestate
             into `board/README.md` §"The rules, as Henri wrote them":
             "Negotiate at the start and ask questions freely.  Collect
             up the questions that appear, wherever they belong, and pass
             me the info."  Then, when the first hand-collected list was
             handed to him and five of eight came back "I don't know":
             "open up the card for questions"
    see      board/README.md §"The rules, as Henri wrote them" — the rule
             this card is the missing half of
             card:kaizen-ingestion.md — which noticed the sibling problem
             a week ago in its own `see` line: each card "carries a
             *count* a session must keep by hand … scattered across cards
             that nothing gathers either".  The two are the same shape
             pointed at different things, and whichever is built first
             should be looked at by the other
             manifesto.md §"Two rules" — rule 1, do not build what
             nothing needs: the thing that says this is needed is the
             hand-collection, not the idea

## What the first list showed, and it was not what the card expected

Eight questions were handed over on 2026-09-01.  Three came back
answered.  **Five came back "I don't know."**

That ratio is the finding, and it changes what this card is for.  A
queue for the person would treat five unanswered as a backlog.  Read
instead as a measurement of the *questions*, it says something sharper:

* **Three of the five could not be answered by anyone**, because they
  are measurements nobody has run — does a drafting prompt do better or
  worse when told its material was cut (`F010`); what should the tools
  arm be given, between a whole 40k card and a 7.5k digest; how many
  arms on one model before 1-in-6 can be told from bad luck.  Asking a
  person for an opinion where evidence is owed is not asking a question,
  it is offloading a measurement.
* **One was asked at the wrong grain** — "are commit messages too loose
  in the heredoc rule?" has no answer until a commit message is found
  corrupted, which the card already says.
* **One is genuinely his and genuinely hard** — batch 1's self-shaped
  strand, which a session may not promote, and which got "hmm…".

So the useful thing this card can do is not *hold* questions.  It is to
make a question say, when it is written, **what would answer it** — and
to make the ones whose answer is a measurement look different from the
ones that are a person's call.  A question a person cannot answer is
usually one that was not ready to be asked.

## What it must not become

A ticket queue.  The board is already the list of work and the F-ledger
is already the list of what is wrong; a third list that grows and is
never emptied would be a fourth place to look and the exact failure
`kaizen-ingestion`'s `because` describes.  If this cannot be built so
that a question *leaves* it — answered, or turned into the measurement
that answers it, or withdrawn — it should not be built.

It must also not become a way to ask more.  Henri's rule says to ask
freely; the list above says the session's problem on 2026-09-01 was not
too few questions but three that should have been measurements.  A
mechanism that made asking cheaper would have made that worse.

## Day one, unbuilt — the shapes, none picked

- **(a) A line where the question is written.**  A card or an F-entry
  gains a field — one line, naming what would answer it: `measure`, `his
  call`, or `waits on <event>`.  Cheapest, and it is the part that would
  have caught three of today's five before they were asked.
- **(b) A gathering tool.**  `tools/questions.sh` reads those lines
  across `board/` and `fixme/` and prints what is open, the way
  `tools/kaizen.sh` reads the tree for the lamp.  Only works if (a)
  exists first; without a marked line it is the grep that already
  failed.
- **(c) A lamp.**  A count at the prompt, like the kaizen and lander
  lamps: *N questions waiting on the person, oldest M days.*  The tree
  has three lamps and they work; this is the shape it already knows.
  But a lamp for a list that never empties is nagging, so this waits on
  the "questions leave" problem above being solved.

(a) is the one worth doing alone, and it is the only one that changes
what happens *before* a question is asked rather than after.

## What would make this card wrong

If the hand-collection turns out to be enough.  It took about ten
minutes on 2026-09-01 and produced eight questions that were, as far as
anyone can tell, the real eight.  A session already writes a kaizen by
hand and that has not needed automating.  If the next two or three
collections are also right and also cheap, then the honest answer is a
paragraph in `board/README.md` saying *collect them at the sitting's
end* — and this card closes unbuilt, which would be a good outcome and
not a failure.

The thing that would make it clearly *right* is the opposite evidence:
a question raised, written into a card, and then lost — nobody acting on
it because nobody saw it.  That has probably already happened and
nothing in the tree would show it, which is the honest state of this
card's `because` on the day it was opened.

## 2026-09-01 — day one (a) landed, and the shape came from the mark

Built at Henri's *"what I next would want you to work on are the
questions card"*, hours after the self-shaped mark got its form.  The
two turned out to be one mechanism seen from opposite ends, which is why
this landed in an afternoon rather than a sitting: **a mark is a session
saying "I wrote a rule, read it"; a question is a session saying "I do
not know, and here is what would settle it."**  Both are a session
addressing the person in place, and both are answered the same way — he
appends a line beginning `henri:`.  One convention, learned once.

### The form

A question is written **where it arises**, flush left, in the card or
F-entry it belongs to:

    *(question, measure — does a drafting prompt do better told its
    material was cut?  **20 turns per arm.**)*

    *(question, his call — should this paragraph carry a mark too?)*

    *(question, waits on a commit message found corrupted — is the rule
    too loose in allowing messages through?)*

Three categories and no others, taken from this card's own day-one
sketch: **`measure`**, **`his call`**, **`waits on <event>`**.  Found
with

    grep -rn -A2 '^\*(question' *.md board/ fixme/ spec/ doc/

which returned zero hits before this section existed — measured, the way
`(self-shaped` was, rather than assumed.  `test/test_questions.py`
refuses a fourth category, a question that is not a question, and a
`waits on` that does not name its event.

### The thing that does the work: only `his call` ever reaches him

This is the whole finding of the first list turned into a mechanism.
Five of eight came back *"I don't know"* and **three of those five were
measurements nobody had run** — so the failure was not that he lacked
opinions, it was that a session had routed measurements to a person.

A `measure` question is a session's to run.  It never goes on the list
that reaches him, no matter how long it sits.  A session that writes one
is not asking for anything; it is recording a debt against itself, in
the place where the debt was incurred.

That is also the answer to *"what must this not become"*.  It cannot
become a ticket queue for him, because the only queue that reaches him
is the `his call` one, and today that queue has **one** entry.

### Questions leave, and they leave differently

- **`measure`** leaves when a session runs it and writes the answer
  beside the question.  The three that came back "I don't know" on
  2026-09-01 left the same day this landed — not by being answered, but
  by being *specified*: `F010` now carries 20 turns per arm with its
  power calculation and its honest limit, and `card:tools.md` carries 24
  arms at about $1 with the reason the number is 24 and not 14.  A
  measurement with a number and a cost is no longer a question waiting
  on anybody.
- **`his call`** leaves when he writes `henri: …` under it.
- **`waits on`** leaves when the event happens, and the point of writing
  it down is that the event can then find what was waiting on it —
  which is what the commit-message question in `card:rewritten-command.md`
  is for.

A question that has left **stays where it is**, with its answer under
it, exactly as an answered mark does.  Nothing is deleted; the record
keeps what was asked and what came back.

### What this does not build, and why

**(b), the gathering tool, and (c), the lamp** — both still wait, and
the reason is stronger now than when this card was opened.  The `his
call` queue has one entry.  A tool to gather one line, and a lamp to
count to one, would be the exact failure `manifesto.md` §"Two rules"
names: building what nothing needs.  The grep above is the gathering
tool until the queue is long enough that reading it is work.

**And the honest possibility that this card still closes unbuilt.**  Its
own §"What would make this card wrong" says: if hand-collection keeps
being enough, the right answer is a paragraph in `board/README.md` and no
mechanism.  What landed here is not really a collection mechanism — it is
a **writing discipline**, and the count that decides whether it was worth
it is how many `measure` questions get written in the next fortnight that
would otherwise have been handed to Henri.  If that number is zero, the
categories were ceremony.  Worth counting, and the place for the count is
this card.

## 2026-09-01 — the first list, kept as the baseline

| # | question | what would answer it | Henri, 2026-09-01 |
|---|---|---|---|
| 1 | should a drafting prompt say "your material was cut"? (`F010`) | a measurement through `compare.py` | I don't know |
| 2 | what should the tools arm be given — 132.7k chars or a 7.5k digest? | a measurement, then a card | I don't know |
| 3 | how many arms on one model to tell 1-in-6 from bad luck? | a session proposing a number | I don't know |
| 4 | doors' `calls` back to 16 for comparability? | his call | **yes, lift it back** |
| 5 | widen `TEND_CTXCHARS` now the node is at `-c 16384`? | his call | **yes, widen further** |
| 6 | the gate came in at 2s against a 30s budget — add program tests back? | a session's judgement | 2s is ok; add any that are critically important |
| 7 | are commit messages too loose in the heredoc rule? | a corrupted message, if one ever appears | I don't know |
| 8 | batch 1's self-shaped strand — a session may not promote it | his call, and only his | hmm… |

*(6) was answered by the session and the answer was **no**, with a
reason that is structural rather than cautious: since install day two,
nothing a session commits is in force until `sudo tools/install.sh`, so
a fence or a lamp broken in the tree is not broken on the machine.  The
install boundary already stands between a bad commit and a restraint in
force, and the whole suite runs before an install.  Adding the fence's
own tests to the gate would buy an earlier red for a failure that cannot
reach the machine.*

## Shelved 2026-09-03 — waits on the queue growing

Moved to `later/` at Henri's "laita simpleqa ja questions later/
hakemistoon".  Day one (a) landed and holds: a question is written where
it arises, only `his call` reaches him, and `test/test_questions.py`
refuses the shapes that hid one.  So the `because` — a raised question
having no home — is answered.  What waits is the rest the card named
unbuilt: the gathering tool and the lamp, and both wait on an **event**,
the `his call` queue growing past the one entry that made a lamp
"nagging".  Until a sitting leaves several unanswered, hand-collection is
enough and the card says so; it is real and not being worked.
