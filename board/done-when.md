# done-when — work was done on a spec nobody had written, and the card form has no place for what done looks like

    status   open
    because  on 2026-09-06 a card's `because` said "nothing on the
             person's side records a window", a session sized day one
             by its own taste, and fifteen commits landed — a mirror
             of every window, a reader, a rename — before Henri's
             concept was written down (`spec/canvas.md`) and showed
             the mirror to be the read half of a thing that runs the
             other way.  The card form asks for the problem and for
             nothing about what would be true, from his shell, when
             the problem no longer stands; so a session decides that,
             and his hand is asked at the end, when a no costs a day.
             Henri, 17:5x: "Miten me voitaisiin saada se aikaiseksi
             että epämääräisin speksein ei tehtäisi työtä lainkaan?"
    done     when no change to the tree's programs can land on a card
             whose definition of done Henri has not signed, and this
             card's own build was the first one refused for it.
             (a session's draft, 2026-09-06, naming no function —
             gestate's rule for the line; henri: signed 2026-09-07)
    asked    Henri, 2026-09-06, ~17:55 — "Hmm.. tee sille kortti. Ja
             kortti itse noudattaa omaa sääntöänsä."
    see      card:canvas-windows.md (the day), spec/canvas.md (the
             concept, written after), test/test_board.py (refuses a
             card without a `because` — the same gate one step
             earlier), tools/pre-commit.sh, board/README.md (the marks
             and the rule that his answer goes where the mark reads
             it), tools/meter.py --waiting (the queue for his hand),
             ~/gestate/board/README.md §"The postcondition, before
             anything is built" (the same rule, adopted there
             2026-08-17, and never carried here)

*(question, his call — the `done` line above: sign it as it stands,
change it, or refuse it?  Nothing on this card is built until a
`henri:` line is here, which is the card keeping its own rule.
henri: signed 2026-09-07)*

## Where it came from

Henri, the minute the card was written: *"muistaakseni gestatessa on
ihan täysin sama sääntö muuten. siellä me puhutaan
postconditioneista."*  It is.  gestate's board, adopted 2026-08-17:
**before building, state the postcondition in one sentence, derived
from the card's `because` and naming no function** — then Henri
corrects it in a line, or does not, and the work has a definition of
done that was not written by the code.  Two rules under it: a
postcondition that cannot be written without naming a function is the
sign the change is not user-facing; and one written after the build
is a description of what was built.  The rule was one tree over the
whole time, and this tree's README loaned only "The rules, as Henri
wrote them" — so the `because` above is also this: a rule that lived
in prose in one tree did not travel to the next.  What travels here
is the sentence, its name, and a difference: in gestate silence
passes ("or does not"); here the line is signed or the build does not
land, because 2026-09-06 is what silence costs.

## What it is

A gate, not care — the tree's shape since `gates` day one: a card
without a `because` cannot be committed, and a mark waits for his
line before it counts.  The same two pieces, one step earlier.

* **The field.**  `done` on a card: what is observable from his shell
  when the problem no longer stands, in his words or signed by him —
  the line ends `henri: <words> <date>`.  A session may draft it; a
  draft says *unsigned* and the meter counts it as waiting for his
  hand.  You cannot write one without walking the thing through, the
  way the 17:25 arrows of `spec/canvas.md` did; if a line will not
  come, the card is not ready, and that is the answer and not a
  fault.

* **The gate.**  The pre-commit hook refuses a commit that changes
  `tools/` or `test/` unless its message cites a `card:` whose `done`
  line is signed, or cites an F-number — a defect has its own ledger
  and its own red.  A commit on cards, specs, kaizens and the journal
  is not gated: that is the work that should have come first today,
  and did not.

* **What it cannot catch.**  Vagueness itself.  A gate reads presence,
  not clarity.  And "do X" said in talk with no card: the session's
  first reply is the spec in three lines — what will exist, what will
  not, how it is measured from his shell — and waits one round.  That
  is a ceremony and not a mechanism (Henri, 18:1x: "mekanismit toimivat
  joka kerta kun seremonia voi pettää") — it failed today and is
  not proposed as a rule; where it fails again it becomes a gate or an
  F-number.  No hook can see it.

## Day one — proposed, not built until the line above is his

`test/test_board.py` reads the `done` field and refuses a card at
`doing` whose line is unsigned (a card at `open` may carry a draft);
`tools/pre-commit.sh` reads the commit message for `card:` and `F`
citations and refuses a change under `tools/` or `test/` with neither,
or with a card whose line is unsigned — red first on this card, at
`doing`, with the draft above.  `tools/meter.py --waiting` lists
unsigned `done` lines beside the marks.  The cost: his hand on every
card before any build, one line each, and one exchange at the head of
every card — the exchange that was missing on 2026-09-06.

## What would make this card wrong

If the signed lines turn out to be written by him to get past the gate
rather than to say what done is — a quota answered by inventing the
thing that passes it (`card:green.md`'s lesson).  The measure is the
next card built under a signed line whose build he then calls the
wrong shape; one such is a note, the second is this card reopened.

## What it must not become

A form nobody fills, or a gate that judges words.  The hook checks a
signature and a citation, never the sentence; the sentence is his.

## Where it sits

Placed last, 15, by the session that wrote it at his word; the
tiebreak is his.  Its own `done` line is a draft and unsigned, so by
its own rule nothing on it is built — the first card the rule applies
to is the card that carries it.
