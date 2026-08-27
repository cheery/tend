# Ingested — one line per kaizen read, levelled at ten a day

`board/kaizen-ingestion.md` §"The plan, fixed" is the schedule and
§"What one reading produces" is the vocabulary: `rule — <where>`,
`promoted — <where>`, `recurs — <kaizens>`, `once`, `open — <card>`.
A kaizen is read once; its line is its record; the day it was read is
the batch it was in.  Newest batch at the bottom.

## Batch 1 — read 2026-08-26, the ten oldest (2026-08-24-1549 → 2026-08-25-0744)

| kaizen | the lesson, in a phrase | verdict |
|---|---|---|
| 2026-08-24-1549 | the day's four errors were each closed with a mechanism a wrongness is visible to — a test, a counter, a ledger — never a resolve to be careful | `rule` — manifesto §"go and do it"; the four-countermeasure table is the practice |
| 2026-08-24-1758 | a rule about the governed party, drafted by that party, leans toward it; mark the draft self-shaped and give it to the person | `recurs` — [[2026-08-25-0626]] [[2026-08-25-0732]] (3×, no mechanism); a session promoting this into README would be the self-shaped move itself → **Henri, Fri 08-28** |
| 2026-08-25-0626 | reading a countermeasure is not applying it — the self-shaped rule was forgotten the day after the instruction | `recurs` — the reading≠applying strand [[2026-08-24-1549]] [[2026-08-25-0714]]; rule at manifesto §"go and do it" |
| 2026-08-25-0639 | a command handed to the person to type is one short line, or it is two commands | `rule` — memory: commands-for-henri-fold-in-console |
| 2026-08-25-0646 | measure, don't design — the sharpest reach row (the state dir, a cord let *through*) was one no design pass would produce | `rule` — the reach table was written from complaints; "measured, not designed" holds tree-wide |
| 2026-08-25-0703 | a cord is never a probe — five andon rings went out for the session's own evidence | `open` — cords.md; the andon must cap and batch its rings, and a measurement renders to a file rather than pulls the cord |
| 2026-08-25-0714 | a warning about a position-matching pattern, read in the morning, was remade that evening; and a restore is only a restore when HEAD holds what you mean | `recurs` — reading≠applying [[2026-08-24-1549]] [[2026-08-25-0626]]; the restore half is its own, once, no mechanism |
| 2026-08-25-0721 | show all of what a command said when it can refuse — `tail -N` hid the reason | `recurs` — the pipe-hides-the-line strand [[2026-08-25-0714]], and again this session 2026-08-26; small, no mechanism |
| 2026-08-25-0732 | asked for direction, offer what would kill each option before offering an order — the board filled at the session's pace | `recurs` — the self-shaped strand [[2026-08-24-1758]] |
| 2026-08-25-0744 | evidence from the governed party naming its own failures is the hardest kind to get, and was got — but nothing here verified it; "relayed by Henri" is the honest form | `once` — verification owed, board/work-environment-ai.md count |

**What batch 1 showed.**  Most lessons already have a home — manifesto,
a memory, the reach table — which is the tree doing its job, and is the
`because`'s own hope answered for the oldest ten.  Two strands recur.
The first, *reading a warning is not applying it* (three faces:
[[2026-08-24-1549]], [[2026-08-25-0626]], [[2026-08-25-0714]]), is
**already a standing rule** — the sessions violated it, they did not
lack it; what the rule prescribes is a mechanism, and where one was
built (`test_selfmatch.py` for the pgrep shape) the strand stops.  The
second, *self-shaped drafts lean toward the session* (three faces too),
has **no mechanism and cannot be promoted from inside a session** — a
session writing that rule into `board/README.md` would be committing
it — so it is flagged for Henri's Friday review, not promoted here.
**Zero lines were added to README this batch, on purpose**: the one
promotion the readings pointed at is the one a session may not make.

## Batch 2 — read 2026-08-27, the next ten (2026-08-25-0753 → 2026-08-25-1445)

| kaizen | the lesson, in a phrase | verdict |
|---|---|---|
| 2026-08-25-0753 | the leash's ledger caught a defect in the leash on its first outside run; and the fix a session could not run shipped with the commit saying which line had not executed | `recurs` — the claim-ahead-of-measurement strand, first face here; its batch-1 root is [[2026-08-25-0744]] ("relayed by Henri" is the honest form).  The observer half is `rule` at doc/mediation-order.md and tools/leash.sh's header |
| 2026-08-25-0803 | the bus row was written as a reach with no `--check` probe and claimed a reach it did not deliver; the ledger said `plain` at minute one and the session spent a hundred chasing it as a bug | `recurs` — [[2026-08-25-0753]].  The row half has its mechanism now: `tools/sandbox.sh --check` probes the bus's absence (:47).  The other half is manifesto §"three ways" read backwards — the instrument was right and the reader was the fault |
| 2026-08-25-0824 | a sensor's regression check is a band — a floor catches under-counting only; ask what over-counting would look like | `recurs` — [[2026-08-25-0828]] repeats it as a standing rule (2×).  The cpu band is at test/test_leash.py:134; the general form ("any measured column") has no home yet — its third face promotes it |
| 2026-08-25-0828 | a mechanism a session cannot test is proposed, not declared — "the third time in two days" by the kaizen's own count | `promoted` — board/README.md §"What the days taught", one sentence cited to [[2026-08-25-0753]] [[2026-08-25-0803]] and this: the third face in one batch, and the card's own `because` names the strand.  What closed it in practice was not a sentence but a route — the claim went to the side that could run it (a gestate session unfenced; Henri's patch) — so the sentence says that, not "be careful" |
| 2026-08-25-1404 | the sitting's clock is read at the start, not discovered at the end of the first reply | `once` — applied the very next sitting ([[2026-08-25-1412]]: "the clock was read first"); a lesson applied the next day wants no promotion.  Of its four, the one not applied — a `14:xx` placeholder committed in a card — is the card format's to refuse, and it does not yet |
| 2026-08-25-1412 | a category question is answered by a table of what is actually open, and by a count started at zero rather than a build | `rule` — manifesto §"Two rules" (1: do not build what nothing needs); the count lives at done/gates.md.  Evidence-before-leaning is the same rule applied to the order of a reply |
| 2026-08-25-1424 | a workaround in a test (`; true` after an inner `timeout`) is a bug with an alibi | `recurs` — the reading≠applying strand of batch 1 ([[2026-08-24-1549]] [[2026-08-25-0626]] [[2026-08-25-0714]]): the two `; true` this kaizen named are still at test/test_leash.py:108 and :127, without a word on whether the 124 fix made them unnecessary.  Recorded, never read back — the card's `because` in one grep.  Left for the leash's next caller, named here rather than fixed blind |
| 2026-08-25-1428 | a probe from a tool family that can act on the person's side (`xdotool`) — say in advance which commands are reads, and leave the rest out of the line | `recurs` — [[2026-08-25-0703]] (five andon rings for the session's own evidence) and tools/limit.sh's 08-24 note (`--hook` run by hand wrote a row in Henri's log): 3 faces.  **Reason not promoted**: each face is closed by its own guard — limit's JSON check exists, the andon's cap is `cords`'s work, `xdotool` has no caller here — and "a probe never reaches the person" as a sentence would be one more thing read and not applied |
| 2026-08-25-1436 | a shell is not a place for prose — an apostrophe in `printf` cost a command, the second of its class in two days | `recurs` — [[2026-08-25-0714]] [[2026-08-25-1404]] (pgrep, word-split, apostrophe: 3 faces).  **Reason not promoted**: the pgrep face has test/test_selfmatch.py and a memory; the other two are caught by the shell in seconds, and a rule cheaper than its catcher is not owed |
| 2026-08-25-1445 | a card names a problem and refuses its own answer — "what it must not become" keeps the half-designed fix out of the card | `rule` — board/README.md §"What a card is"; test/test_board.py refuses a `because` that names a fix |

**What batch 2 showed.**  Five strands, and the batch produced the
ledger's first promotion.  *A claim written ahead of its measurement*
has three faces in these ten alone ([[2026-08-25-0753]],
[[2026-08-25-0803]], [[2026-08-25-0828]]) and its root in batch 1; the
third face is the trigger and it is promoted — one sentence in
`board/README.md`, saying what actually closed the strand (a route to
the side that can run the claim), not a resolve to be careful.  *A
sensor's check is a band* is at two faces and waits for a third.  Two
strands reached three faces and are **not** promoted, each with its
reason written: *a probe that can reach the person* (closed per face by
its own guard) and *shell prose* (caught by the shell faster than a
rule would be read).  One strand **closed by being applied**: the
clock read at the start ([[2026-08-25-1404]] → [[2026-08-25-1412]]),
which is what a kaizen is for when it works.  And one line is the
card's `because` made concrete: the two `; true` that
[[2026-08-25-1424]] called "a bug with an alibi" are still in
`test/test_leash.py`, unexplained, two days on.

**Two corrections to the card, found by reading.**  The card's `see`
cites *"manifesto.md — R10 (measure, don't assert)"*; there is no R10
in tend's manifesto, nor in gestate's — the nearest is §"The three ways
an instrument fails".  And the plan's arrival rate ("five to seven a
day") was written the morning of a day that produced **37**; both are
on the card.  **Least certain line**: [[2026-08-25-0753]], which
carries two lessons and the reading had to pick one — one uncertain
verdict, not two in a row.
