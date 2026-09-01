# questions — a question raised for the person has no home, and nothing gathers it

    status   open
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
