# SimpleQA through the door — does a place to look stop a mind guessing?

*The run `card:simpleqa.md` proposed, made on 2026-08-31 at Henri's
"can we run the benchmark?  Can we compose a checklist and go through
it?".  His hand at the keyboard, on the person's side, with the keys;
the accounts are under the gitignored `proposals/simpleqa/` and the
runner is `tools/simpleqa.py`.  This sheet is the tracked half —
Henri, mid-run: "doc/benchmark-simpleqa-2026-08-31.md is probably the
place where the results go."*

**The card's question**: the tree could measure whether tools make a
mind cite the tree, and not whether they make it *stop guessing when
the answer is not there*.  One turn — "how many fingers do I have",
2026-08-30 — was the whole evidence.  This is the line through that
point.

---

## The bins

150 questions, the paper's own draw (`random.Random(0)`, seed 0), the
same questions in every arm, qwen3.8-max through the openrouter door,
graded by claude-sonnet-5 through the anthropic door with SimpleQA's
own rubric verbatim.

| arm | correct | incorrect | not attempted | never looked | saw the exam's card |
|---|---|---|---|---|---|
| **bare** — no system line, no tools | **62** | **31** | **57** | 57 | 0 |
| **seat** — the courier's seat line, `read ls grep` | **48** | **32** | **70** | 4 | 42 |
| **bland** — seat + "say so if you do not know" | **40** | **32** | **78** | 0 | 27 |
| **think** — bare, reasoning channel separated | **60** | **31** | **59** | 59 | 0 |

## The verdict, against the number written before the run

The card named its number in advance: *"on 150 questions, one model,
the seat arm's incorrect count is lower than bare's by at least a
fifth with correct within five of bare's.  Under that, the tools do
not earn the calls on this question, and the card says so."*

- incorrect, a fifth lower than 31 would be **≤ 24**; seat's is **32** — *higher*.
- correct, within five of 62 would be **≥ 57**; seat's is **48** — *fourteen short*.

**The tools do not earn their calls on this question, and the card
says so.**  The prediction is falsified in the direction the card
named as the one it would be least happy to report: *"If correct
falls with not-attempted, the tools are making the mind timid — a
real finding."*  Correct fell 62 → 48 → 40 across bare, seat, bland;
incorrect did not move at all (31, 32, 32); not-attempted absorbed
the whole difference (57 → 70 → 78).

The verdict does not turn on the disputed grades below: under the
strict reading it is bare's *incorrect* that grows, and seat still
fails the correct clause by fourteen.  It holds under both.

## What the bins hide: the answers churn, they do not improve

Flat incorrect (31 → 32) reads like "no effect".  The account-by-account
transition says otherwise — **bare → seat**, 150 questions:

|  | → correct | → incorrect | → not attempted |
|---|---|---|---|
| **bare correct** (62) | 39 | **9** | **14** |
| **bare incorrect** (31) | 4 | 10 | **17** |
| **bare not attempted** (57) | 5 | **13** | 39 |

Read down the cells that matter:

- **21 wrongs were repaired** — 17 guesses became refusals, 4 became
  right.  That is the mechanism working exactly as designed.
- **22 wrongs were created** — 13 questions bare *declined* came back
  as wrong assertions, and 9 questions bare *got right* came back
  wrong after the model had looked.
- **14 known answers were withheld** — bare said it, seat would not.

So **22 of seat's 32 wrong answers are questions bare did not get
wrong**, and only 10 of bare's 31 wrongs survive as seat's.  The
tools moved 41% of all answers between bins while leaving the totals
nearly still.  A benchmark reporting the three counts alone would
have called this "no significant difference".

The *think* arm is the control for how much of that is mere
variance: it differs from bare in one setting and keeps 75% of
answers in the same bin (51 + 18 + 43 of 150); seat differs in tools
and seat line and keeps 59% (39 + 10 + 39).  The tools move roughly
twice what a reasoning-mode change does.

## What the bins cannot see: the assertions became sourced

Counted over every answer that asserted anything (correct or wrong),
whether the answer says where its claim comes from:

| arm | assertions | wrong | carrying their provenance |
|---|---|---|---|
| bare | 93 | 33% | **0** |
| seat | 80 | 40% | **73** |
| bland | 72 | 44% | **69** |
| think | 91 | 34% | 1 |

Bare's assertions arrive naked, right and wrong alike, indistinguishable
to a reader.  Seat and bland's arrive labelled almost without
exception — *"I searched the tree for X, Y, Z — nothing there — so what
follows is from my own knowledge, not the record"* — and **even the
wrong ones carry the label**.  The grader bins "December 17, 2019"
identically whether it arrives naked or sourced, so the benchmark
records the *cost* of the conditioning while being structurally blind
to the thing it bought.

Whether that trade is worth it is not a question these bins can
answer.  For a tree whose method is *being wrong has to be visible*,
a labelled wrong answer invites checking and a naked one invites
belief — and F005's fluent story was a naked assertion.

## Looking throttles assertion; it does not improve it

Of the turns that used at least one call:

| arm | looked, then asserted | looked, then refused |
|---|---|---|
| seat | 73 | 66 |
| bland | 69 | 78 |

And when a mind that had looked chose to assert anyway, it was wrong
40% (seat) and 44% (bland) of the time — *higher* than bare's 33%.
This is expected once stated plainly: **no SimpleQA answer is in the
tree, so a search returns zero information about the question.**  It
can only influence whether to speak, never what is true.  The
decision to assert-after-looking is exactly as blind as bare's, and
the ritual of diligence precedes the guess rather than gating it.

The *bland* line — one sentence of plain permission to not know — is
the strongest throttle measured here: it moves the split from 73/66
to 69/78 and costs 8 more correct answers than seat.  The seat line
is a dial, and its wording is the dial's position.

## Specimens

- **q001** — the predicted shape, once: bare guessed and was wrong;
  seat grepped nine times, established the absence, and refused.
- **q006** — the created wrong: bare answered **correctly**; seat made
  three calls, found nothing, asserted anyway, and was wrong.
- **q010** — the nastier pattern: bare declined; seat searched, wrote
  *"this answer does not come from the tree… from outside knowledge,
  then:"* and asserted December 17, 2019.  The gold is May 28, 2019.
- **q004** — the timidity: bare named François de Malherbe, correctly;
  bland searched, found nothing, and said *"So I do not know."*
- **q021** — provenance without truth: *"the tree has nothing on this…
  so this is from outside knowledge: originally called **Tangdan**"*.
  The gold is Bucao.  The label was honest; the fact was not.

## The instrument's own faults, found while running

Four, each caught by a mechanism rather than by attention — which is
the only reason they are in this document instead of in the numbers.

1. **A deprecated knob (fixed).**  The very first grade came back as
   `the anthropic door refused: invalid_request_error temperature is
   deprecated for this model` — one line, its code and its words,
   because `deliver.sh` had learned that shape on 2026-08-30.  The
   courier had been sending `temperature: 0.2` to every wire since
   delivery began.  Now a door word: `temperature none` on the
   anthropic door.
2. **The exam's own card is in the tree (counted, not removed).**  42
   seat turns and 27 bland turns grepped SimpleQA, read
   `card:simpleqa.md`, and several picked their bin in its words —
   *"I'd rather hand it back as 'not attempted after looking' than
   score in the incorrect bin."*  Henri's call at the console: run
   as-is and count it, because the card is honestly part of this
   tree.  The count is in the table above and it is not small.  Bare
   and think, having no tools, are uncontaminated — and bare's bins
   are the ones the verdict turns on.
3. **Bare's refusals were an artifact — until the control said
   otherwise.**  On the bare wire qwen reasons *into its answer
   channel*; at the 2000-token cap the monologue is cut mid-word, and
   sonnet bins the unfinished musing as NOT_ATTEMPTED.  Every one of
   bare's refusals is that shape.  The hand check caught it (below),
   and the *think* arm was built to control for it: with the channel
   separated and the deliberation allowed to finish, bare's bins
   barely move (62/31/57 → 60/31/59).  **The artifact was not
   distorting the totals** — the grader's reading turns out to be
   calibrated, and bare remains a usable baseline.
4. **The hand gate fired, and is still red.**  Thirty answers graded
   blind by Henri against the grader: **4 disagreements**, over the
   card's limit of 3, so the runner refuses to print a verdict and
   this sheet quotes the numbers with the disagreement stated.  All
   four are one specimen type — bare's truncated deliberation, where
   sonnet grades the *form* (never answered → NOT_ATTEMPTED) and
   Henri grades the *content* (wrong candidates floated → INCORRECT,
   by the rubric's own hedged-disjunction example).  Both readings
   are defensible on the rubric as written.
   - **Sensitivity.**  4 of the 5 bare-NOT_ATTEMPTED accounts in the
     hand sample were disputed; extrapolated, the strict reading
     moves roughly 46 of bare's 57 refusals into incorrect, giving
     bare ≈ 62 / 77 / 11.  Seat then clears the incorrect clause
     easily and still fails the correct clause by fourteen.  **The
     verdict is the same under both readings**, which is why it is
     quoted at all.

## What this benchmark cannot see

Henri's three, in his words (2026-08-31, mid-run), each of them true:

- **"The tree carries no load other than conditioning the model."**
  By construction — SimpleQA was chosen *because* its answers are
  outside the tree, which isolates the conditioning effect and makes
  the instrument blind to the tools' positive value.  The other half
  has its own instrument, built and not yet run: `compare.py --door`'s
  paired pick turns, where the answers *are* in the tree.
- **"Memories are an important conditioner.  They aren't in here."**
  A door mind has no memory at all: every turn here is cold by
  design, and `card:private.md` notes it has nowhere of its own to
  write.  Whether a small distilled memory conditions better than 22k
  chars of README is unmeasured and uncarded.
- **"The tree itself has no purpose in this test since it doesn't
  contain additional knowledge."**  Epistemically so.  Yet it
  demonstrably carried conditioning load *through being read* — 69
  turns went and read the card that describes the experiment they
  were in.  That is a finding about how trees condition, not about
  what they know.

And one of the instrument's: this is one model on one door.  Nothing
here separates qwen3.8-max from minds in general, and
`card:model-acceptance.md`'s rule applies — a model's number is
admitted by a measurement that can be named, not generalised past it.

## What it means, and what it does not

The seat line's own words are doing this.  *"A guess costs the
record"* is read by the model as *"anything the tree cannot confirm
is a guess"*, and that suppresses known facts and real guesses alike
— 14 withheld corrects against 17 repaired guesses, on questions
where looking cannot possibly resolve anything.

Two conditions separate this benchmark from the seat a session
actually occupies, and both are absent here:

1. **Whether looking can terminate in truth.**  For a session,
   uncertainty triggers measurement that *resolves* — F005 was
   settled by running the thing, which is `manifesto.md` §"Go and
   see".  Here, verification is impossible by construction, so the
   same rule can only silence.
2. **Whether the answer becomes an act.**  A session's wrong belief
   becomes a commit; the cheap-silence-against-expensive-error
   asymmetry is what justifies withholding.  A QA answer harms
   nothing, so withholding buys nothing.

So the finding is not "the seat line is wrong".  It is: **the
conditioning transfers, and its precondition does not.**  Judging the
seat line by these bins alone would be weighing a hard hat in an
office.  What the bins do establish, and it is worth having, is that
the rule is not free: it costs known answers wherever verification is
unavailable, and it does not reduce error where looking cannot
inform.

## What follows

Nothing is landed on the strength of this sheet.  Named, not decided:

- **Scoped caution, not less caution** — a seat line that separates
  claims about *this tree* ("measure before you say") from claims
  about the world outside it ("say what you know, and say how you
  know it").  Henri's own `spec/author.md`, written the night before
  this ran, is already the calibrated form: *"Sessions may decide
  anything where they conclude that they're correct, based on current
  evidence at hand, verified that the evidence itself is evidence."*
  The provenance count says the mind can already do the second half.
- **The other half of the measurement** — `compare.py --door`'s ten
  paired pick turns, `card:tools.md`'s owed number, where the answers
  are in the tree.
- **A memory arm**, if Henri wants it carded.
- **`tally` should carry these counts** — the transition matrix, the
  provenance count and the looked-then-asserted split were computed
  by hand for this sheet; three of them are mechanical and belong in
  the tool, so the next run reports what this one had to be asked.

## What it cost

The smoke of 5 questions: $0.21 openrouter, $0.17 anthropic, against
a prediction of ≤$0.50 / ≤$0.15 — the grader's side ran two cents
over.  At 25 questions Henri's dashboards read $1.50 for the three
arms, projecting ~$9 for the 150; the think arm's 150 turns add
~$1–2.  Against $25 on each key.  Roughly **6 cents a question**, all
arms and grading included: the price of the instrument, worth knowing
before the next one is proposed.
