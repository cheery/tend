# model-acceptance — something breaks when nobody picks the mind, and the keeper is the only check

    status   open
    because  Henri, 2026-08-27, 9:42: "I worry that something breaks
             when I'm not on entire control of which LLM runs.  I've
             seen at least one session where the model was so robotic
             that I would not use it."  The catch was his own judgment,
             in one session, which puts the person in the vigilance
             seat for a rare quality failure — and the layer that
             fails is the one this method runs on
    asked    Henri, 2026-08-27 — "kirjoittaa siitä kortti
             ~/tend/board/later/ laudalle"
    blocked  two events, either of which wakes it: tend has a place
             where a model is admitted at all — the broker,
             board/work-environment-ai.md §3, or the llm node's cords,
             board/session-program.md — so that a refusal has somewhere
             to sit; or the trap-card kit exists to be run
             (~/gestate/doc/memory/conditioning-shows-under-work.md
             §"The clean experiment, one variable at a time" — designed
             2026-08-21, never built)
    see      ~/gestate/doc/notes/notes-on-which-model-runs.md — the
             conversation this card is cut from, both sides verbatim
             ~/gestate/doc/memory/smaller-models-and-the-tree.md — the
             prediction that judgment degrades first; one measurement
             ~/gestate/doc/memory/weights-context-suite.md — the
             counterfeit: vocabulary without judgment
             ~/gestate/doc/memory/a-trial-is-refused-until-its-sheet-can-decide.md
             — binds whoever builds the suite

## The ask

The whole of it is the `because`.  What follows is the session's
reading of the morning's conversation, and the conversation is in the
`see` line rather than paraphrased here.

## Shelved on arrival, and on what

**It waits on an event, not on a decision.**  A model gate needs a
door to stand in, and on 2026-08-27 tend has no door: the enforcement
layer — fence, leash, `keep`, the budgets — is built and does not
care which model runs, but nothing yet *admits* a model, so there is
nothing to refuse one at.  The broker (`card:work-environment-ai.md`
§3) or the llm node's cords (`card:session-program.md`) is that door,
and whichever lands first is the first event in the `blocked` line.

The second event is the instrument.  The conversation names the
trap-card kit as *a model acceptance suite* — does it go and look,
does it mark suspected, does it stop at a seam — and the kit is a
design in gestate's memory with nothing built under it.  Building it
is gestate's work or this tree's, and it is not this card's: this
card is the caller for it, which is what a design has lacked since
2026-08-21.

## Found by looking

* **The `because` is n = 1 with no specimen.**  The robotic session
  has no date, model or transcript in either tree.  The worry stands
  on his recollection, and the card says so rather than dressing it
  as a measurement.  The first thing this card wants, before any
  gate, is the next such session saved the way
  `doc/specimens/2026-08-24-qwen3.8-27b.txt` was — so that *robotic*
  has a line number.
* **The prediction it rests on has one measurement.**  *Judgment
  degrades first* was predicted 2026-08-19 and seen once, on a 9B and
  a 1B, on 2026-08-20.  Suspected, not known, at the scale a gate
  would run at.
* **The answer's own caveat is the design constraint.**  A model that
  passes a canned trap can still barrel through a live seam, so the
  gate is necessary and not sufficient; the kaizen and the seam
  review stay the backstop.  Any sheet for the suite has to say what
  a pass licenses and what it does not, or `tools/prereg.sh` in
  gestate refuses it.
* **The routing half is a second card, if it is anything.**  *Cheap
  models for mechanical work, qualified ones for judgment* assumes a
  scheduler that knows which kind of work a task is, and nothing in
  either tree classifies work that way.  Not carded; named so it is
  not smuggled into this one.

## Questions, open

1. Where does the refusal sit — at the leash (a wall-clock budget
   already exits 124 there), at `keep`, or at the launcher?  The
   answer depends on which door lands first, so it is the first
   question the waking session asks.
2. What is a trap, concretely, for *this* tree — tend has no cards
   with a `because` naming a fix to plant, and no memory directory
   for a go-and-look trap to point into.  The kit was designed for
   gestate's shape.
3. Who runs it, and how often — once per model, or per session?  A
   per-session run is a tax on every sitting and the sitting is a
   body constraint.  Henri's call.

## 2026-08-28, 18:45 — woken: the door exists, and the first instrument with it

Moved from `later/` to the board by a session at Henri's "do
session-program", on the first of the two events the `blocked` line
named: tend has a place where a model is admitted at all.  As of today
the llm node runs under keep with its cords (`card:session-program.md`:
the sitting, the lamp, the andon, the heartbeat, the kernel's boundary
on a led turn), leads work through `tools/lead.sh`, and its output is
on disk in a shape a person reads.  A refusal has somewhere to sit.

**What woke with it, unasked: an instrument.**  `tools/compare.py` puts
the led turn — the open board as a digest, a pick, the card as material,
a draft — to any Claude model, thinking off, at the node's limits, and
writes one account per model beside the node's own.  Run twice today:
gemma-4-26B restated the card's `because` on every landed turn; Sonnet
5 and Opus 5 named a small thing and drafted it, and Opus's draft
reached the card's own prediction from its `because` alone.  That is
the `because`'s "robotic" with a line number — the first thing
§"Found by looking" said this card wanted — and it is the
prediction's second measurement: *judgment degrades first*, seen now
on a 26B against two models that can hold the turn.  Specimens:
`proposals/lead/2026-08-28-1809.md`, `proposals/compare/2026-08-28-1835-*.md`.

**Question 1, answered provisionally by the door that landed.**  The
door is the grant beside the program: `llm/grant`'s program line names
the model as data the person brings (the first `.gguf` under the node's
model directory), and `tools/launch.sh NODE check` is where a ✗ already
refuses a node before it runs.  A model gate sits there — a `check`
that runs the trap turn and reads the account — not at the leash (a
budget, not a judgment) and not at `keep` (a boundary, not a reader).
Questions 2 and 3 stand; 3 is his, and the sitting is a body
constraint.  **Day one, when he places it**: the compare accounts are
the trap kit's first shape for this tree — a fixed turn, a fixed
board, accounts side by side — and the sheet that says what a pass
licenses is owed before any refusal is wired.

## 2026-09-02 — the first admission, written as a task shape: gemma4

At Henri's *"write that admission into model-acceptance"*, after his
question — *"does this mean gemma4 is a bit too lightweight model to
work on the board?"* — and a session's answer: partly, and the
evidence is thinner than the sentence; the question is not keep or
retire but what it is admitted for.  He said write it.  So this is
the sheet §18:45 said was owed before any refusal is wired: **what a
pass licenses, and what it does not**, for the one model this tree
runs itself.

### The evidence it stands on, all of it

Four turns on 2026-09-02, N=1 each, through `doors/llm/door` with
thinking off on the wire (`card:session-program.md` §06:29–§07:0x):

| the ask | what gemma4 did |
|---|---|
| the digest and the tools, pick a card | picked from the digest, read nothing |
| the tools and no digest, pick a card | pulled the cord — "which card should I focus on first?" — with `ls board/` in hand |
| "read board/README.md and tell me its first heading" | one `read`, the right heading |
| (2026-08-28) the card as material, draft a small thing | restated the `because`; Opus reached the card's own prediction from the same material |

And hy3 on 2026-09-01, same arms, read sixteen cards unprompted.  Two
days, one direction, and one sentence: **gemma4 does what the ask
says and nothing beyond it.**  It reads when reading is the ask, and
not when reading is the way to the ask.

### Admitted for

- **A turn whose ask names the read.**  "Read X and say Y."  The
  deliver ask is the specimen, and it passed on the first try.
- **Material in the prompt.**  A draft or an answer grounded in text
  the turn was handed — the same place `propose.sh` puts a card —
  never in text one call away.
- **A card picked by a person or a stronger mind.**  The pick is not
  its work; the small thing under a pick can be.
- **A few lines, not a build**, which is the pick prompt's own bound.
- **Under keep, inside the fence, at no cost per turn.**  This is the
  reason the admission exists at all: gemma4 is the only mind this
  tree runs confined (`lead.sh --kept`), and every door calls out,
  unkept, on his account.  A worker that can be fenced is worth a
  task shape of its own.

### Not admitted for

- **Leading** — picking from the shelf unaided with tools in hand.
  Two turns, both declined the read that would have answered.
- **Reading as the route** — any turn where the material is in the
  tree and the turn is expected to go and get it.
- **Drafting from a `because` alone** — 2026-08-28's tautology, and
  nothing since has moved it.

### What this admission does not license, said out loud

It does not license *"gemma4 finishes a card"*, which is
`card:session-program.md`'s milestone; the milestone's gemma4 arm now
puts the rules in the prompt as material, and that arm's result may
narrow this sheet further.  It is an admission on four turns and one
specimen, at temperature 0.2, with the prompt's shape never varied —
**and it is revised by a count, not by a mood.**  What would *widen*
it: one shaped pick prompt ("first `ls board/`, then pick"), 24 turns,
and a read rate a person can see.  What would *narrow* it: a
read-named ask it answers by guessing — the trap below.

### Question 2, answered by the turn that answered §07:0x

*What is a trap, concretely, for this tree?*  The deliver ask is one:
an ask whose answer is in a named file, through the door, and the
pass is a `C: read <file>` line on the record *and* the right answer.
A guess with no `C:` line is the fail, and it is one grep.  It is a
trap for exactly the shape this sheet admits — the read named — which
is the only kind of pass this card can honestly check today; a trap
for leading would be a pass this model has never had.  Where it sits
is §18:45's answer: `launch.sh NODE check`, running that one turn and
reading the account.  **Not built**; the sheet comes first, and this
is the sheet.

### Question 3, a proposal and not an answer

*Per model or per session?*  This sheet is per model **and per task
shape**: the same gemma4 is admitted at one ask and refused at
another, so a per-model pass is too coarse and a per-session run is
the tax §"Questions, open" named.  The tree already has the third
form — a door file admits a model in the person's words — and this
sheet is what the `admitted` line on `doors/llm/door` would point at.
His call, as it was.

## Where it sits

Placed last on the board by the session that woke it, 2026-08-28; the
tiebreak is his.
