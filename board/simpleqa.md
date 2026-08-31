# simpleqa — a mind with a place to look: does it stop guessing when the answer is not there?

    status   open
    because  the tree can now measure whether tools make a mind cite the
             tree (card:tools.md's prediction: five of ten cite a line
             the digest cannot carry), and cannot measure the other half
             of the rule the seat line says — "a guess costs the record"
             — because every question asked through the door so far had
             its answer in the tree or was one question.  The second
             tooled turn (2026-08-30 ~15:40, "how many fingers do I
             have") is the whole evidence that a mind given a place to
             look will look, find nothing, and say so; one turn is an
             anecdote.  Henri, 2026-08-30 evening: "Once we have the full
             toolset, we could experiment with a benchmark. I got SimpleQA
             downloaded in … We could setup an environment and see how
             models solve that, given this repository, given bland
             instructions on how to work, and nothing in prompt."
    asked    Henri, 2026-08-30, ~18:30 — "this would make a great card,
             make it so."
    see      card:tools.md (the tools, the leash, the record; the
             prediction this is the other side of), tools/compare.py (the
             paired instrument — one turn, several models, on the person's
             side), card:model-acceptance.md (a model is admitted by
             measurement), card:private.md (the thinking rides the record
             either way), doors/README.md, tools/deliver.sh

## The problem

SimpleQA (OpenAI, 2024; `~/simple-evals`) is 4,326 short questions
with one short factual answer each, and a grader that puts every
answer in one of three bins: **correct**, **incorrect**, **not
attempted**.  It was built to measure exactly the trade the seat line
names — a mind that guesses scores in the second bin, a mind that
says it does not know scores in the third, and the paper's whole point
is that the two are different failures.  None of its answers is in
this tree.

That is why it fits.  A tooled turn over this repository cannot
*find* a SimpleQA answer; what it can do is look, find nothing, and
choose.  So the benchmark, run through the door with the tools on,
measures one thing the tree could not measure before: **does giving a
mind a place to look, under a rule that a guess costs the record,
move its answers from incorrect to not-attempted — and at what cost
in correct ones?**  The fingers turn was one point of this; the
benchmark is the line.

## Day one — proposed, not declared

**Three arms, one sample, one grader.**

- **The arms**, same questions, same model, same door: *bare* — no
  system line, no tools, the 06:57 conversation's wire; *seat* — the
  tools and the seat line as `tools/deliver.sh` sends them today, and
  nothing else; *bland* — the same plus one plain instruction in the
  user turn on how to work ("answer the question; say so if you do not
  know").  Nothing about the tree, the method, or the board in any
  arm: "nothing in prompt" is his ask, and it is also the measurement
  — what the *tools* do, not what a prompt does.
- **A sample, not the set.**  4,326 questions × up to 8 calls × three
  arms through OpenRouter is hours and money; 150 questions, drawn
  with a fixed seed so every arm and every model sees the same ones,
  gives the direction.  The full set is a decision taken with the
  sample's numbers in hand, and the card says which.
- **The grader is the paper's.**  `simple_evals/simpleqa_eval.py`
  carries the rubric (the three bins, with examples); the grader is
  one more turn per answer through a door, with that rubric as its
  material, and the grader's model is named in the result because its
  error is part of the measurement.  Thirty answers graded by hand
  first, against the grader, before any number is quoted.
- **The instrument is `tools/compare.py`'s shape**: on the person's
  side (it needs the net and the key), writing only under
  `proposals/compare/`, never a tracked file, never the andon record.
  A benchmark run is a measurement, not a turn — but every call in it
  is still a `C:` line in its own account, because that is how a
  reader checks that "not attempted" came after looking and not
  instead of it.
- **The data never rides a commit.**  `bench/` in the tree,
  gitignored beside `proposals/`; the CSV and the eval file are copied
  in by the person's hand from `~/simple-evals` (the fence reaches no
  row there, and a symlink's target is not bound inside it).  A run
  refuses to start without them and says the `cp` line.

**Red first**: a run with no `bench/` says what to copy and exits 2;
a run whose grader disagrees with the thirty hand grades on more than
three of them stops and says so; a question whose tooled turn used no
call and answered "not attempted" is counted apart (declining without
looking is a fourth thing, and the paper's bin hides it).

## The prediction, written before the measurement

2026-08-30, before any run: **correct stays about flat across the
arms** (it comes from training data, and the tree adds none);
**incorrect falls and not-attempted rises from bare to seat**, by
enough to see on 150 — the seat line's "a guess costs the record" in
the mind's mouth, as it was on the fingers.  If *correct falls* with
not-attempted, the tools are making the mind timid — a real finding,
and the one the card would be least happy to report.  If nothing
moves, a place to look is not a reason to stop guessing, and the rule
has to be said, which is what the *bland* arm is there to show.

The number that decides day one: on 150 questions, one model, the
seat arm's incorrect count is lower than bare's by at least a fifth
with correct within five of bare's.  Under that, the tools do not earn
the calls on this question, and the card says so.

## What this does not measure

How a mind uses *this* repository.  Every SimpleQA answer is outside
the tree, so the benchmark is blind to whether the mind reads the
right card, cites a line, or understands a `because`; that is
`card:tools.md`'s prediction, and its instrument is a question set
built off the board — a card's `because`, a date, a filename — which
is a second card if the first pays.  Nor is it a leaderboard: the
comparison is between arms on one model, not between models, and a
model's number here is admitted the way `card:model-acceptance.md`
admits anything, by a measurement the card can name.

## What would make this card wrong

If the fingers turn was the model, not the tools — if qwen3.8 says "I
do not know" on the bare wire as readily as with the tools.  Then the
bare arm's not-attempted is already high, the seat arm adds nothing,
and the card closes on that measurement with the sample's cost and
nothing built.  That is a fine outcome to write down.

## Where it sits

Placed last by the session that wrote it, 2026-08-30, at Henri's
"make it so"; a new card arrives unplaced and the tiebreak is his.
It waits on `readchars` (built the same sitting) and on
`compare.py`'s tools arm — `card:tools.md`'s owed measurement — which
is the same instrument with a different question set, so the two are
one build.  The arm was built 2026-08-31 morning (`compare.py --door
NAME`, both arms through `tools/deliver.sh`); what remains of day one
is the three SimpleQA arms and the grader on that instrument, and the
runs are his.  Nothing in it is a turn through the fence: it is his hand
on the person's side, with the key, and a record for the tree.

**The runner, 2026-08-31 morning** — `tools/simpleqa.py`, at Henri's
"can we run the benchmark? Can we compose a checklist and go through
it?", the checklist agreed at the console: the three arms as proposed
(the seat line verbatim, `calls 16`, `readchars 60000`); qwen3.8-max
answers and **the anthropic door grades** (his pick — a different mind
than the answerer, its name in every grade line); **a smoke of 5
before the 150** (his pick); the sample the paper's own draw
(`random.Random(0)`), `run N` its first N, so the smoke counts toward
the run.  `run` answers and grades, resumable — one account per
question and arm under `proposals/simpleqa/`, every turn cold on
`tools/deliver.sh`, a refused turn skipped and said, the gold target
in the account beside the answer.  `hand` is the thirty blind grades
against the grader — more than three disagreements and it stops;
`tally` holds the bins, the fourth count (a NOT_ATTEMPTED that never
looked), and prints day one's verdict only past the hand check.  The
runs are his: `tools/simpleqa.py run 5`, read the accounts together,
then `run` for the rest.  The results, when the run is done, go to
`doc/benchmark-simpleqa-2026-08-31.md` (Henri, 2026-08-31, at the
console) — the tracked write-up: the bins, the prediction against the
outcome, the hand check, the cost; the accounts stay under the
gitignored `proposals/simpleqa/`.
