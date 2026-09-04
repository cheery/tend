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
day") was written the morning of a day that produced **39** (first written
here as 37 — an eyeball count, corrected by `grep -c` the same morning); both are
on the card.  **Least certain line**: [[2026-08-25-0753]], which
carries two lessons and the reading had to pick one — one uncertain
verdict, not two in a row.

## Batch 3 — read 2026-08-28, the next ten (2026-08-25-1506 → 2026-08-26-0801)

*Read by a session that wrote none of them, per the card's rule for this batch.*

| kaizen | the lesson, in a phrase | verdict |
|---|---|---|
| 2026-08-25-1506 | "kept updated" for prose is a gate for the facts a test can check and a lamp for the rest; and the two copies of the sheets (md, html) had nothing holding them equal | `rule` — the split is tools/summary.sh's header; the drift half was closed 2026-08-27 by tools/sheets.py and test/test_summary.py:127–160, which hold the printable twin to the two sheets.  The third lesson — an instrument's test runs it in the state it ships in (the empty `git log` bug) — has its guard (summary.sh:55–56, `${sum_at:-0}`) and still no test of the untracked state; small, `once` |
| 2026-08-25-1522 | the boundary is set from outside the bounded party — a program confining itself breaks Rule 1 as a session fencing itself does; a confined program's runtime is a grant like any other | `rule` — manifesto §"Two rules" and tools/keep.py's header (:8); the runtime finding is test_keep.py's shape.  Write-scoping is named at done/keep.md:158 ("reads only, for now") and waits on a caller — not a card, and not owed before one |
| 2026-08-25-1530 | a comment that asserts a kernel behaviour is a claim and gets a measurement; and on a surprising change to a protected path, diff before stage | `rule` — the first half is batch 2's promotion (board/README.md §"What the days taught": proposed, not declared) and the card's own `because` names this kaizen as that strand's third face.  The diff-before-stage half is `once` in its form: since install day two the tree's copies are the workbench and `tools/fence.sh` says on every prompt which set is in force, so a protected file that moved is the session's own edit or Henri's `--free`, never a surprise |
| 2026-08-25-1540 | the card about the write-only journal was written from the session's memory of the day — it sat inside the gap it named | `open — card:kaizen-ingestion.md` — this ledger is the reading aid the kaizen asked for, in its first form, and the `recurs — <kaizens>` column is what hands a strand up without a session having lived every face; this batch does exactly that once (below).  Its other lesson — a card names a problem on a prompt phrased as a fix — is `rule`, test_board.py, batch 2 [[2026-08-25-1445]] |
| 2026-08-26-0721 | a harness lied twice and was caught by absurd numbers, not by a check — run a known-red and a known-green through it before any row; and "the file changed" is not "the break is in the file" | `rule` — tools/mutate.sh:91 reads the intact copy first and refuses to read below a red one, built the same morning ([[2026-08-26-0739]]); the `NOOP` column is a `cmp`.  First face of the fixture strand |
| 2026-08-26-0728 | a copy that is not quite the original — `write_text` of a script drops its mode; three fixture errors in one day, each caught by output that read wrong | `recurs` — [[2026-08-26-0721]], the second face; the scratch copy chmods now (test/test_precommit.py:99).  The fold-commands memory applying to the session's own console is its second time in two kaizens (the locale `sed` in 0721) — same session, the memory is the rule, nothing more owed |
| 2026-08-26-0739 | a fixture with nothing on either side of the seam — one commit, one second — gives the defect and the correct program the same number; "the day's one lesson in three faces, and `kaizen-ingestion` should one day hand it up" | `promoted` — board/README.md §"What the days taught", one paragraph cited to [[2026-08-26-0721]] [[2026-08-26-0728]] and this: the third face, and the kaizen asked for the promotion by name.  The strand was paid a **fourth** time the next evening — [[2026-08-27-1650]], three fixtures copying a live `.claude/settings.json` in one evening, unread by this ledger and found by `grep` — which is the card's `because` exactly, and why the paragraph says what closes a fixture and not "be careful" |
| 2026-08-26-0743 | a message sent into a limit the session knew existed; and the finding offered as "not mine to make unasked" when the card was the thing to offer | `once` — the block is closed by `arrival` (done/arrival.md; tools/limit.sh:245 logs `peer`), and the offering-a-card half was applied within the hour (the card was made).  The vocabulary half — a verdict word is refused rather than invented — is `rule`, this card §"What one reading produces" |
| 2026-08-26-0751 | test, break, fix, break again — nothing trusted for having passed once | `rule` — tools/mutate.sh and done/green.md, F88's rule; the protected set's cost paid visibly and no wider.  Carries a second lesson, below |
| 2026-08-26-0801 | a card whose problem lives in two trees needs a paragraph to say which shelf it is on — one card per tree next time; and when two copies share a file, a fix's names are part of the fix: check the reader, not the writer only | `recurs` — [[2026-08-26-0751]] says the two-tree lesson first, this repeats it (2×, no home; `sitting-everywhere.md`'s title names two trees and is the next place it would show).  The gate refusing the keeper's own commit — two fields dropped in a header rewrite — is `rule`, test_board.py, and it fired.  The reader/writer half is `once` |

**What batch 3 showed.**  Six `rule`, one `open`, two `once`, one
`recurs` at two faces — and **one promotion, the ledger's second**,
which is the mechanism doing what the `because` asked: the fixture
strand has three faces in one morning ([[2026-08-26-0721]]
[[2026-08-26-0728]] [[2026-08-26-0739]]), the third face asked
`kaizen-ingestion` to hand it up by name, and a `grep` ahead of the
schedule found it paid a fourth time on 2026-08-27 (`1650`, three
fixtures copying a live settings file) — the lesson recorded and not
read back, twice on two days, exactly the cost the card names.  It is
one paragraph in `board/README.md` §"What the days taught", saying
what closed each face (the harness reads the intact copy first; a copy
of an executable is a copy; a fixture has something on both sides of
the seam; a test builds the side it means) rather than a resolve.  The
two-tree card strand ([[2026-08-26-0751]] [[2026-08-26-0801]]) is at
two faces and waits for a third.  Two lessons of this batch closed by
the tree moving on: the sheets' second copy is held by a checker
since 2026-08-27, and the diff-before-stage face of the protected set
lost its ground when install day two made the tree's copies the
workbench.  **Least certain line**: [[2026-08-25-1530]], whose
diff-before-stage half was judged `once` on an inference about the
install rather than on a kaizen saying so — one uncertain verdict, not
two in a row.  Zero verdict words added.

## Batch 4 — read 2026-08-29, the next ten (2026-08-26-0812 → 2026-08-26-1309)

*Read on Saturday, two days ahead of the table's Monday, at the
2026-08-28-1830 kaizen's item 4 ("today wrote four kaizens and read
none back"); the batch is the ten oldest unread, so the table's row
is what moved, not the rule.  Read by a session that wrote none of
them.*

| kaizen | the lesson, in a phrase | verdict |
|---|---|---|
| 2026-08-26-0812 | the journal got a levelled schedule in the sweep's shape, and the ledger meant to read the lamp put it out — a file in the lamp's directory was read as a kaizen landing | `rule` — the schedule is card:kaizen-ingestion.md §"The plan, fixed"; the lamp matches a kaizen's *name* now (tools/kaizen.sh:85–95, `????-??-??-????.md`) and test/test_kaizen.py:139–154 commits a stray into `doc/kaizen/` and reads the lamp still lit.  The `green` row it named was written the same morning ([[2026-08-26-0822]]) |
| 2026-08-26-0822 | the reading changed one file and could say so in a line; the session that read batch 1's reading≠applying strand paid it a fourth time an hour later; a `sed` and a `tail` ate a line | `rule` for the first two — the ledger's rule is card:kaizen-ingestion.md §"What this is not", and reading≠applying is batch 1's standing rule (manifesto §"go and do it") whose stop is a mechanism, which this face got (the detector names what it detects).  The third is `recurs` — the pipe-hides-the-line strand at its **third face** [[2026-08-25-0714]] [[2026-08-25-0721]] and this.  **Reason not promoted**: each face cost one re-run and the missing line was its own catcher within a minute; the strand has no mechanism in tend's remit (it is the session's console, not the tree) and batch 2's rule for shell prose holds — a rule cheaper than its catcher is not owed |
| 2026-08-26-0847 | a detector's own power is a measurement, not an argument — the mutation expected red went green, and the reason was real: confinement of a well-behaved program is invisible through that program, and shows only on overreach | `rule` — board/done/green.md:419, the launcher row's `partial` written from the measurement; the harness is tools/mutate.sh.  The state-dir-apart-from-code point is node/run.sh's grant (`--allow` code, `--write` state), and it held when `--no-net` joined it ([[2026-08-26-1309]]) |
| 2026-08-26-0855 | a "6 passed, 7 skipped" on a real break is not a survivor, it is a detector that did not run; read the seat before a sweep and say up front which detectors it cannot reach | `rule` — the vocabulary is board/done/green.md:445 (`none — nothing can, from this seat`), and the route for what a seat cannot run is board/README.md §"What the days taught" (batch 2's promotion): the claim goes to the side that can run it.  The seat-first half was answered within the hour by the outside run arriving ([[2026-08-26-0905]]) rather than by a rule; `once` in that form |
| 2026-08-26-0905 | the outside seat caught a detector, not the fence: a one-seat oracle can be a false red in another seat, F88's mirror; and a detector edited by a seat that cannot run it says so in the first line | `rule` — the false red is on board/done/green.md:477–510 and closed by execution the same morning ([[2026-08-26-0910]]); the say-so-first is the proposed-not-declared sentence (README §"What the days taught": *the commit says which line has not executed*).  The passing twin fixed unasked — a green detector edited on reasoning — is `once`, and the unfenced run covered it |
| 2026-08-26-0910 | two seats did one measurement between them and neither could have alone; the control clone told a fence-edge from a result; a run handed to another seat names its destructive edges in the handing | `rule` — the two-seat route is the same README sentence; control-before-mutation is tools/mutate.sh:90–93, reached independently by the other seat; the scratch-dir limit it found is tools/sandbox.sh:64–70, applied by Henri's hand ([[2026-08-26-0931]]).  The destructive-edge-in-the-handing half is `once` — the docstring says it now, and no second handoff has been made without it |
| 2026-08-26-0926 | a decorator stolen by an insert one line off — the neighbour went red, not the newcomer; a question ("would it be time") answered as an assessment before it was acted on | `rule` — reading≠applying again (batch 1's standing rule; its stop is a mechanism), and the mechanism was the suite: the wrong test red is the tell, and it fired.  The look-above-the-anchor line is `once`.  Assessment-before-action is the shape the `self` card had already fixed and the sitting honoured (board/done/self.md) |
| 2026-08-26-0931 | `git add -A` stages what is not the change — a handoff patch Henri had applied on his own clock rode into a9a9958 | `rule` — .gitignore `*.patch`, with the commit named in the comment: the class made impossible, not unlikely.  Its second line (`git status` before `-A` after a step on Henri's clock) was applied the next sitting ([[2026-08-26-1304]]: `git add README.md`, not `-A`) — closed by being applied |
| 2026-08-26-1304 | "free to keep" read as "verify, then keep" — 20 of 20 paths checked before gestate's page went in; and a page verified for Henri should say what was *not* checked as plainly as what was | `recurs` — the board-reading move's first face, paired with [[2026-08-26-1309]] below.  The not-checked footer is `once` — the footer says what was checked; the next verified page owes the other half.  The verify-before-keep is `rule`: a fixture is a claim about the thing it copies (README §"What the days taught", batch 3's promotion), in its prose form |
| 2026-08-26-1309 | the board reading was wrong by two slices because a card's newest section is not its last — sections land under older headings on purpose — and Henri acted on it; a `13:xx` placeholder went into a committed card | `recurs` ×2 — the board reading at its **second face** [[2026-08-26-1304]] (used twice in a day, wrong once; "a tool on the second ask" and no tool has been asked for since — tools/ has none, and `grep -rl 'stays open' tools/` is empty); and the placeholder at its **second face** [[2026-08-25-1404]] (`14:xx` there, `13:xx` here), which batch 2 already said "is the card format's to refuse, and it does not yet" — test/test_board.py still has no line for it.  A `grep -rn '[0-9]:xx' board/ doc/` today finds no third; both wait |

**What batch 4 showed.**  Seven `rule`, no `open`, three lines carrying
a `once`, and three strands at `recurs` — **zero promotions, on
purpose, and each refusal has its reason written.**  This is the
morning `green` measured its own suite, the outside seat arrived, and
`self` closed; nearly every lesson is a mechanism that already exists
and is named by line.  The reading≠applying strand of batch 1 has two
more faces here ([[2026-08-26-0822]], [[2026-08-26-0926]]), and both
confirm batch 1's verdict exactly: the rule was not lacking, and each
face stopped where a mechanism caught it (the lamp matching a name;
the suite going red in the neighbour).  The pipe-hides-the-line strand
reached its third face and is **not promoted**, for the reason batch 2
gave shell prose: the catcher is faster than the rule.  Two strands
stand at two faces and are the ones to watch: the **placeholder time
in a committed card** ([[2026-08-25-1404]] [[2026-08-26-1309]]) whose
third face is a one-line refusal in `test/test_board.py` — and a
mechanism is a card, not a promotion, so the third face opens one or
adds the line to `kaizen-ingestion` itself; and the **board reading
as a tool** ([[2026-08-26-1304]] [[2026-08-26-1309]]), whose second
face already said the tool reads open items by phrase and not last
sections, and whose third face is Henri asking for the reading again.
One strand **closed by being applied** the next sitting:
`git status` before `git add -A` ([[2026-08-26-0931]] →
[[2026-08-26-1304]]).  **Least certain line**: [[2026-08-26-0822]]'s
third-face refusal — the pipe strand's non-promotion rests on the
claim that no mechanism in the tree could catch it, which is an
argument about the session's console and not a measurement; one
uncertain verdict, not two in a row.  Zero verdict words added.

## Batch 5 — read 2026-08-30, the next ten (2026-08-26-1317 → 2026-08-26-1437)

*Read on Saturday, two days ahead of the table's Monday, at Henri's
"do kaizen ingestion next"; the batch is the ten oldest unread, so the
row moved and the level held.  Read by a session that wrote none of
them.  The afternoon of 2026-08-26: the resolver carded and built in
four sittings, and `keep`'s session half measured row by row — state,
trees, tree.*

| kaizen | the lesson, in a phrase | verdict |
|---|---|---|
| 2026-08-26-1317 | a slice under `tools/` or `node/` lands with its mutation rows in the same commit — skipped twice in one day by the same session; and a question in the message is served before the work in it | `rule` for the rows — board/done/green.md:564 says "a slice lands with its rows, the same commit" and calls it not yet a rule; the two sittings after ([[2026-08-26-1334]] "kept once", [[2026-08-26-1437]] "four rows") kept it, so it is the tree's practice with the card as its home.  The question-first half is `promoted` at [[2026-08-26-1323]] below, where Henri confirmed it.  The third item — a program's restrictions ride the *pull* — became card:resolver.md the next sitting and is `done/` |
| 2026-08-26-1323 | Henri: "Do the question first next time"; and a memory written through the fenced shell died in the empty home, two "no such file" lines above a green suite | `promoted` — a memory, `question-first`, in the tree's memory directory: *a question in the message is served before the work in it* — Henri's words, 2026-08-26, cited to [[2026-08-26-1317]] and this.  The kaizen says the memory was written that sitting; the memory directory today holds one file and it is not this one, so the failed write it describes was never remade — the promotion is the write, done with the tool that runs outside the fence, which is the kaizen's own rule for memory files.  The local-model news is card:session-program.md, `open` there since 2026-08-26 |
| 2026-08-26-1334 | the measurement was the design — nothing detached survives a fenced command, so no daemon; a helper defined and not used left the grant pasted three times; the launcher became the pull path with no protection | `rule` — test/test_keep.py:353 `test_the_launchers_grant_appears_once` is the test the kaizen asked for; node/run.sh joined the protected set by Henri's hand the next sitting ([[2026-08-26-1342]], tools/sandbox.sh:120).  The measurement-first half is board/done/resolver.md's day one.  Closed by being applied, both |
| 2026-08-26-1342 | a line-based count over a record that spans lines gave "2978 commands" for a sitting of 53, and it was read past; the want carried a reason across Henri's hand for the first time | `recurs` — the **count-from-an-unparsed-format** strand, first face here, second at [[2026-08-26-1433]] below; its countermeasure for the leash ledger became tools/ledger.py the next sitting ([[2026-08-26-1356]]).  The want-carries-the-reason half is `rule`, tools/kaizen.sh `want` and board/README.md §"What the days taught" ("a session never judges whether it owes another: it says so") |
| 2026-08-26-1356 | the ledger's second read made the parser a tool before the reading; a mutation row survived because it broke nothing, and the harness cannot tell that from a blind detector; a fence patch verified by `sh -n` is verified by logic | `rule` — tools/ledger.py exists with tests; a survivor is read, never counted, is board/done/green.md:221–233's standing practice; the fence-by-execution half is batch 2's promotion (README §"What the days taught": proposed, not declared), and its next face is [[2026-08-26-1405]] where the unfenced run refused |
| 2026-08-26-1405 | the same miss twice in one patch — the test's probe moved and not the check's — because the test file was grepped and not the script; "PARENT WRITABLE" printed from inside a tmpfs home | `once` for the grep-every-path rule: it was applied sixteen minutes later ([[2026-08-26-1412]]) and the trees row cost one hand instead of two ([[2026-08-26-1421]]) — closed by being applied, and no fence patch since has needed it (the tree's copies are the workbench since install day two).  The wrong-seat half is `rule`: tools/sandbox.sh:323 "the escape, graded from outside", and README's route for a claim a seat cannot run |
| 2026-08-26-1412 | the trees row read by purpose: eleven ledger records and the cards' citations named board, tools, spec, doc, journal, the root documents, the twin's settings, and never the source or `.git`; the audit's run under it was read from its imports, not run | `rule` — tools/sandbox.sh:82–91 is that measurement as `tree_parts`, and the not-run half was run nine minutes later by Henri ([[2026-08-26-1421]]).  `open — card:trees.md` for what the measurement fixed as a literal: the path.  Opened this morning; the row binds nothing on this laptop and says `on` |
| 2026-08-26-1421 | one hand, no round-trip; the purpose run before it was trusted; "nothing this hour" | `once` — a sitting that applied the two lessons before it and paid nothing.  Its two tomorrows both landed: the tree row's write-side question ([[2026-08-26-1433]]) and the README's "7" by Henri's hand ([[2026-08-26-1437]]) |
| 2026-08-26-1433 | the tree row measured by what the purpose *writes*; two passes counted commit prose and `sed` expressions as paths and were read past; the ledger cannot tell a write in the tree from the same relative path in a scratch copy | `recurs` — the count-from-an-unparsed-format strand at its **second face** [[2026-08-26-1342]], on a second format the same afternoon; the kaizen's own rule is "a tool on the next ask", and `grep -rln 'name-only' tools/` finds none — no next ask has come, so the strand waits at two.  The scratch-copy limit is named on board/done/keep.md:449, `once`.  `.venv` read-only and node/state read-only with the pull file writable both landed (tools/sandbox.sh) |
| 2026-08-26-1437 | the resolver moved outside the fence on a one-line change in the node; a starter forgot the launcher's idle a second time in one day — the property belongs to the launcher, not its callers; a test moved rather than replaced | `rule` — tools/launch.sh:154 reads `TEND_NODE_IDLE` itself, the kaizen's third tomorrow, so no starter carries it; the resolver is board/done/resolver.md and tools/resolve.sh.  The test-named-for-the-rule half is `once`; the row covered it and the launcher has since been rewritten under keep |

**What batch 5 showed.**  Six `rule`, two `once`, one `open`, and
**one promotion — to a memory, the first in the ledger's five
batches** ([[2026-08-26-1323]]: *a question in the message is served
before the work in it*), which is also the batch's one repair: the
kaizen recorded the memory as written and the write had died in the
fenced home two sentences earlier in the same file.  A recorded
lesson whose recording failed is the card's `because` at its
plainest, and the ledger is what noticed — the memory directory was
read before the verdict was written.  One strand new at two faces:
**a count read off a format nothing parses** ([[2026-08-26-1342]] the
leash ledger, [[2026-08-26-1433]] `git log --name-only`), both read
past on the first pass, both with the same countermeasure — the parser
is a tool on the next ask — and the second's next ask has not come;
its third face is a `tools/` script or the reason written why not.
Three lessons **closed by being applied** within the same afternoon:
the grep-every-path rule ([[2026-08-26-1405]] → [[2026-08-26-1412]],
[[2026-08-26-1421]]), the launcher's idle as its own property
([[2026-08-26-1437]] → tools/launch.sh), and the grant-appears-once
test ([[2026-08-26-1334]] → test/test_keep.py).  The afternoon's shape
is the method working at its cheapest: four sittings, each applying
the one before it, and the round-trips through Henri's hand fell from
two to one to none.  The two strands batch 4 named as the ones to
watch have no face here: no placeholder time (`grep -rn '[0-9]:xx'
board/` finds only the card's own citation) and no board reading.
**Least certain line**: [[2026-08-26-1317]]'s `rule` for
rows-with-the-slice — green.md itself says "not yet a rule", and the
verdict rests on two sittings' keeping it, which is practice and not
a mechanism; one uncertain verdict, not two in a row.  Zero verdict
words added.

## Batch 6 — read 2026-08-30, the next ten (2026-08-26-1500 → 2026-08-26-1644)

| kaizen | the lesson, in a phrase | verdict |
|---|---|---|
| 2026-08-26-1500 | a `sandbox.sh` patch handed without its key (`fence.sh --protect`); two guesses at a seat the session cannot see before asking for the log; `!` in a session is the session's seat, not the person's shell | `once` for the key — the install (`done/install.md`, 08-27 evening) ended the patch-handoff: the tree's copies are the workbench and the protected set is installed by his `sudo tools/install.sh`, so there is no key to hand any more.  The guess-before-the-log half is `recurs` — the read-before-fix strand, at [[2026-08-30-0902]] ("both entries' guesses wrong") and promoted there to the F-entry rule.  The `!` fact is `once`: the harness's own guidance says it now; the tree records it nowhere and has not needed to |
| 2026-08-26-1509 | the flake counted (1 in 10) before it was reasoned, and the leash ledger gave the mechanism without a second look at Henri's seat; a script asserted before it wrote, twice, and a patch was read for its length — "grep the hunk you meant to add" | `rule` for the count-first half — `card:flake.md` (the failure ledger and the shake, 08-29) and `tools/mutate.sh` for "red against the old file, in a fresh copy".  The grep-the-hunk half is `recurs` — [[2026-08-26-1616]] (a `sed` anchor on an old line ending), [[2026-08-26-1633]] (the tests not grepped for the file's name), [[2026-08-30-0902]] item 3, and **the sitting that read this batch**, where a card's anchor was not grepped and the patch refused once — a fifth face, and the countermeasure in every one of them was the same assert.  What recurs is not corruption but the turn; see the batch's paragraph |
| 2026-08-26-1524 | a cause named on a card as *measured* was an inference; an inference from an instrument is bounded by what the instrument can see — the leash ledger could not see the probe's cost; 75 ms from Henri's hand corrected "~10 s from cold" within the hour | `rule` — [[2026-08-30-0902]] item 2 is the same lesson as a rule with a mechanism: an F-entry's `suspected` line is for the kaizen and the reading comes before the fix; the leash's clock stamps before its probe since that afternoon (tools/leash.sh).  The ten seconds themselves: `open` — relocated to "before the leash's clock" (`done/resolver.md`), visible to the ledger since, and no occurrence has been recorded; a wait, not a miss, and nobody's to chase |
| 2026-08-26-1532 | the last bind handed in the order the card required (hook, race, bind), and the patch read for its five hunks before the commit — the 15:09 countermeasure applied once; a bwrap test only Henri's seat can run, named as his | `once` — closed by being applied.  The name-what-you-cannot-run half is README §"What the days taught" already (`rule`, promoted by batch 2) |
| 2026-08-26-1535 | three fence patches in a day, one round-trip lost, the last two clean because the list-every-line rule ran before each; the demonstration from the seat the bind is for, refusal by refusal, then served | `once` — the fence-patch route itself is gone since install day two; what it taught (the rule runs before the patch, not after the refusal) is the 14:05 lesson's third keeping, and it stopped needing a kaizen after this one |
| 2026-08-26-1549 | the question answered before anything was built — the 13:17 rule kept; the wait for an install used to build the grant the install would need (`keep --bind`) | `rule` — question-first is a memory (batch 5's promotion, `question-first`) and the tree's practice since; the wait-used half is `once` |
| 2026-08-26-1602 | a model URL from memory, handed as a command — the fence has no net, so the session cannot check a URL and must not hand one as checked; a name and a place, or a checked line | `recurs` — [[2026-08-26-1616]] cites it the same afternoon ("the rule is written; this is its first citation"), and no face since.  For the one thing that kept being a name from memory — a model's id — the mechanism arrived 08-30: `tools/door.sh --models` lists what the door offers and `--use` refuses an id it does not list.  For URLs the rule stands as prose, and has held |
| 2026-08-26-1616 | the measurement wrote the abstraction — the grant file's fields are exactly what two nodes needed and nothing designed ahead; a `sed` anchor matched an old line ending and the launcher never joined the protected set, caught by `--protected \| grep` and not by a test | `rule` — the grant vocabulary is `tools/launch.sh`'s header, and it has grown only by a node's need since (`allow-try`, `make`, `env`, `model`, and `tools`/`calls` on the day this was read).  The anchor half is the grep-the-hunk strand [[2026-08-26-1509]], `recurs` |
| 2026-08-26-1633 | a patch changed what a file *is* and the tests reaching into it were not grepped — Henri's suite went red; a live timing loop raced four times where one look at the mtimes would have been first | `rule` for the first half by dissolution — the workbench is the tree since install day two, the suite runs here before any commit and `tools/suite.py` is the gate, so there is no handoff for a stale test to slip through.  The race-a-timing-loop half `recurs` — [[2026-08-30-0902]] ("`ps` at one instant is not a reading"), now a memory (`background-task-done`) |
| 2026-08-26-1644 | a card names a problem, not the fix; the cords half of the frame got its own card, `session-program`, leaning on the three it completes | `once` — the opening, and everything it named as absent has since been built or carded: the limit and the lamp on the node (`done/node-install.md`), the andon (`done/cords.md`, `card:silent-cord.md`), the door, and the tools on the day this was read |

**What batch 6 showed.**  Four `rule`, four `once`, three `recurs`,
one `open`, and **one promotion — to a memory, the second in the
ledger** (the first was batch 5's question-first).  The batch is the
afternoon the grant beside the program landed, and its ten kaizens
are one strand seen from five angles: **a patch is read for what it
contains before anything downstream of it is trusted** —
[[2026-08-26-1509]] (assert before write, twice), [[2026-08-26-1616]]
(a `sed` anchor on a line that had changed), [[2026-08-26-1633]] (the
tests not grepped for the file's name), [[2026-08-30-0902]] item 3,
and the sitting that read this batch, where the card's anchor was not
grepped and the patch refused once.  Every face has the same
countermeasure and it has been applied every time — an assert on the
anchor's count — so what recurs is not damage but a turn, and one
thing the assert did not cover: a patch script that writes one file
and then refuses on the next leaves the tree half-patched (this
sitting: `tools/panel.py` written, `test/test_deliver.py` refused).
The promotion is that one sentence — **check every anchor before
writing the first file** — as a memory, because it is a fact about how
this session works and not about the tree; the tree's rule (the 15:09
line, "grep the hunk you meant to add") stands in `board/README.md`'s
kaizen paragraph already through 0902's item 3.  The other strand,
**a seat the session cannot see, guessed at before its log is read**
([[2026-08-26-1500]], [[2026-08-26-1524]]), closed four days later by
a mechanism, not a resolve: the F-entry rule and the leash's clock
moved before its probe.  Two lessons closed by being applied within
the afternoon ([[2026-08-26-1532]], [[2026-08-26-1535]]); one arrived
at its mechanism four days on ([[2026-08-26-1602]] → `door.sh
--models`).  **Least certain line**: [[2026-08-26-1633]]'s `rule` by
dissolution — a route that no longer exists cannot be violated, which
is not the same as a lesson learned; one uncertain verdict, not two
in a row.  Zero verdict words added.

## Batch 7 — read 2026-08-31, the next ten (2026-08-26-1653 → 2026-08-27-1650)

| kaizen | the lesson, in a phrase | verdict |
|---|---|---|
| 2026-08-26-1653 | `keep` and `resolver` judged done by the board's own test, and the ambient-exec residual moved onto the cards that own it rather than closing with the words; two wrong shelf paths typed from the README's prose before `git ls-files` was read | `rule` — the test is `board/README.md` §"Where a card is" (does the `because` still stand), and *owned elsewhere, not merely gone* has been the practice at every close since: `fence`/`green` on a shared verdict, `install` leaving `lander` behind, and `trees` on the day this batch was read.  The path half is the grep-the-hunk strand's sixth face ([[2026-08-26-1509]]), now the memory `patch-anchors-first` — and the same check landed this sitting's `board/done/` move on the first try |
| 2026-08-26-1712 | Henri asked for flaws and got three, the idea seeded rather than carded because a `because` is a problem; a memory write through the fenced shell hit the empty home a third time, with "a fourth is a mechanism owed" written down | `rule` for the first half — `board/README.md` §"What a card is"; the critique-not-agreement mode is now Henri's own words in `spec/author.md` ("I let you influence my judgement and I influence yours", 2026-08-30).  The memory half is `recurs` at three faces ([[2026-08-25-0714]], [[2026-08-26-1323]], here).  This reading first wrote *"no fourth in the five days since — closed by disuse"* and then **produced the fourth face in its very next command**, appending this batch's own memory pointer to `MEMORY.md` with a shell heredoc into the fenced home, which has no `~/.claude`.  So the trigger this kaizen wrote for itself fires: **`promoted` — the memory `memory-write-tool-not-shell`**.  The withdrawn sentence is kept in the batch paragraph below, because a verdict falsified within a minute by the hand that wrote it is this card's `because` in miniature |
| 2026-08-26-1719 | the toolbox verdict recorded at its true grain — the enforcement withdrawn, the manifest half kept for os.md property 2 — and a status pass that marked stances as stances rather than as built things | `once`, and a good one: a rejection recorded without flattening it.  The same move ran on the day this was read, where shape (b) of `card:trees.md` was refused with its reason and left as one edit if Henri wants it.  One face here; a second makes it a rule |
| 2026-08-27-0538 | the first cord went out as a patch with its tests inside it so nothing was half-applied; the ingestion read the card that owns it and found two of that card's numbers wrong; and a check that would have passed for the wrong reason — `"sitting" not in stdout`, where pytest's tmp path carries the test's own name | **`promoted` — `manifesto.md` §"The three ways an instrument fails"**, with [[2026-08-27-0710]] and [[2026-08-27-1602]]: three faces in one day of *a check that asserts less than it means*.  That section's citation read "three incidents there, none here yet"; tend has its own three now, and the paragraph names them |
| 2026-08-27-0551 | one-per-sitting reworded and demonstrated by doing; a worktree that flipped `core.bare` twice and a backgrounded `git rebase` that leaked into a read-only file; and "37 kaizens" written from an eyeball into four places where `ls \| grep -c` said 39 | `rule` for the worktree — `board/README.md`'s clone paragraph, itself retired in place by install day two ([[2026-08-27-1650]]), and the memory.  **`promoted` — the memory `count-before-you-write-it`** for the eyeball: three faces, the third being the sitting that read this batch (`2026-08-31-0547`, "two of ten tooled turns" where the count said four), each a number that went into prose with the counting one keystroke away |
| 2026-08-27-0710 | verdicts first and the person decides — Henri's named mode; three build cards each measured into a different shape than first imagined; and a `git fetch <clone> branch:branch` that fast-forwarded main from inside the fence, landing a protected change with no hand | `rule` — the shared-verdict mode is `spec/author.md` in his own words since 2026-08-30 ("we prefer to do decisions together here"); the fetch is in the memory and was dissolved by install day two, after which nothing a session commits is in force until his line.  The toolbox test that read the runtime `✓` line for a dash a *present* tool never prints is the promoted strand's second face |
| 2026-08-27-0748 | a one-commit tail closed by the session that had the context rather than left for one that would not; the card's `because` written as the problem under an ask that named a solution | `rule` — `board/README.md` §"What a card is".  The tail-closing is the kaizen practice read the other way round: "a session that ends while the sitting goes on owes nothing" is a permission, not an instruction to leave the lamp lit for a stranger.  `once` for the rest |
| 2026-08-27-1535 | the install's location decided by reading gestate's settings rather than by preference; the install's own rule refusing its own first commit; the first andon ring measured to one socket by `strace`; and a test keyed "weaker" on the path where the criterion was the owner | `rule` — the location half is go-and-see, now `manifesto.md` §"Go and see" with F005/F006 as its number (2026-08-31); the `--hooks` jq one-liner withdrawn within the hour is the commands-fold-in-the-console memory.  The weaker-test half is the promoted strand's third face |
| 2026-08-27-1602 | `755 - 222` computed in decimal left every installed copy `-r---w--w-` and every hook `Permission denied` — and the test that "held" the mode asserted only *not writable by owner*, which 533 satisfies; the session then ran unfenced to fix it and said so after staging rather than before | `rule` — the mode test is the promoted strand's clearest face and the promotion cites it.  "When the fence is found down, the first line is the restore" is `once` with no second face since, and `tools/fence.sh` prints the in-force line at every prompt now.  The fixture-copies-the-live-file half is batch 3's promotion already |
| 2026-08-27-1650 | day two unbound the tree's copies — what runs protects itself, a workbench is free — and the proof was fixing the oldest open small bug rather than touching a file to show it writable; three fixtures copied one live settings file in one evening | `rule` — the fixture rule is `board/README.md`'s plainest form (batch 3's promotion), paid a fourth and fifth time here.  The lamp's baseline bug, named at [[2026-08-27-0538]], [[2026-08-27-0710]] and [[2026-08-27-1535]], is **fixed and verified in the tool at this reading** (`--diff-filter=A`, `tools/kaizen.sh:96`) — a strand closed by application, three namings to get there.  "`install.sh --check` first, every session" is `open — card:lander.md` |

**What batch 7 showed.**  Six `rule`, two `once`, one `open`, and
**three promotions** — the ledger's first batch with more than one,
the first promotion into `manifesto.md`, and one the reader owed
before the batch was finished (below).  The batch is 2026-08-27, the day the
install was researched, built, landed wrong by a mode, and landed
again, and its ten kaizens carry one strand three times in that single
day: **a check that asserts less than it means.**  `"sitting" not in
stdout` matched pytest's own tmp path ([[2026-08-27-0538]]); a toolbox
test read the `✓` line for a reason dash that a present tool never
prints ([[2026-08-27-0710]]); and the test guarding the installed
copies' mode asserted only *not writable by owner*, which the
defective `533` satisfies — so `sudo tools/install.sh` left every hook
`Permission denied` and cost Henri a prompt ([[2026-08-27-1602]]).
The rule for it already existed and was *borrowed*: `manifesto.md`
§"The three ways an instrument fails" carried gestate's three
incidents and the line "none here yet".  Tend has its own three now,
all from one day, and the promotion is the paragraph that names them —
which is what the manifesto's own preamble asks for ("a section earns
its own number here, or it stays a citation").  The second promotion
is smaller and is a session-fact, so it is a memory:
**count-before-you-write-it**, three faces, the last of them the
sitting that read this batch.

**One strand ended, and one was declared ended and then reopened by
the reader.**  The lamp's baseline bug was named in three kaizens and
then **fixed** ([[2026-08-27-1650]]) — verified in `tools/kaizen.sh` at
this reading rather than taken from the kaizen's word.  The other went
differently, and the sentence is kept as it was written: *"the
memory-write-through-the-fenced-shell strand, which had written its
own trigger (a fourth time is a mechanism owed), has no fourth face in
the five days since — the habit changed instead.  A strand can close by
application, or by disuse."*  The next command this reader ran
appended a `MEMORY.md` line with a shell heredoc and got `No such file
or directory` from the fenced home — the fourth face, one minute after
the acquittal, by the hand that had just read all three of the others.

That is not an embarrassment to bury; it is the **strongest evidence
this card has produced.**  `card:kaizen-ingestion.md`'s whole claim is
that a lesson recorded is not a lesson held, and batch 1 named the
strand for it (reading ≠ applying).  Here the gap is one minute wide
and inside a single tool call sequence, in a session that was at that
moment *writing the verdict on that very strand*.  A rule read, a rule
summarised, a rule violated, in that order.  The mechanism the
2026-08-26 kaizen said a fourth face would owe is now written — the
memory `memory-write-tool-not-shell` — and the honest note is that a
memory is the same *kind* of thing that just failed to hold; what
would actually hold is a check that a `~/.claude` path never appears in
a Bash command, which is a mechanism, and a mechanism is a card.
**Opened the same day at Henri's word — `card:lost-write.md`**, the
first card in this tree opened by an ingestion: it carries the four
faces, three shapes kept alive, the mention-is-not-a-write problem a
naive check would trip on, and the measurement that closes it with
nothing built if the memory holds.

**The count**: 102 kaizens in `doc/kaizen/` at this reading; 70 read;
32 unread — at the level of ten, three days with nothing arriving, and
something will.  Batch 8 is filled in on the card.  No day has been
missed yet; the lamp slice still waits for the first one.

**Least certain line**: [[2026-08-26-1719]]'s `once` for recording a
rejection at its true grain — the same move ran again on the day this
batch was read, which is arguably its second face and would make it
`recurs`; it is called `once` because the second face is the reading
session's own and a reader should not count itself into a strand it is
about to promote.  One uncertain verdict, not two in a row.  Zero
verdict words added.

**Henri's half is still undone**, now seven batches and 70 lines deep:
the three lines drawn at random for his disagreement (handed at batch
6) and batch 1's self-shaped strand.  His, and named here so batch 8
does not arrive before the first three lines.

## Batch 8 — read 2026-09-01, the next ten (2026-08-27-1714 → 2026-08-28-1029)

| kaizen | the lesson, in a phrase | verdict |
|---|---|---|
| 2026-08-27-1714 | two cards closed on a "fully done" that was measured from both sides first; a card move broke a path citation and became the `card:` notation; three gate refusals for one commit, each the gate reading a document the session had not | `rule` — the notation and its resolvers are the mechanism (`test/test_board.py`, `test/test_summary.py`), named at `board/README.md` §"Where a card is"; *measured from both sides before the move* has been the practice at every close since ([[2026-08-26-1653]]).  The three-refusals half is `once`: each refusal was the gate working, none cost a wrong commit, and reading `test_summary.py` before the move would have made it one commit — no mechanism is owed for that |
| 2026-08-27-1723 | the `lander` card holds its decision open with a count; a twin-checker red on its first run, where a green would have measured nothing; wrappers not symlinks, read off how the installed scripts find their siblings; and a default written for the one case in front of the session, the third that day | `rule` — red-first for the checker (`manifesto.md` §"The three ways an instrument fails": a first run that is green has not been shown able to go red), and `board/README.md` §"What a card is" for a card that says what would decide it rather than deciding.  The default half is `recurs` by the kaizen's own count (3× in one day) and **not promoted**: every face was caught by the suite within the minute, which is the mechanism — the tests are the enumeration of shapes the tree already knows, and the failure was writing the default before reading them |
| 2026-08-28-0545 | batch 3 read; the lander lamp lit by its own commit; `check` inheriting `run`'s seat and saying ✗ on a state directory read-only by design; and a hook line committed with its script unprotected, because the rule that would catch it reads the *live* settings and so goes red one apply too late | `rule` — the live-state half closed with a commit-time twin in the same commit (`33f50f7`): `test/test_install.py:327`, which reads what `--hooks` *would* add and checks it against `--protected`.  The kaizen asked the ingestion to say if it recurs; four days on there is no second face.  **First face of the seat strand** — a reader built from a runner carries the runner's seat until one is shown wrong |
| 2026-08-28-0702 | the work laptop; 54 red on one cause (the fixtures inherited `commit.gpgsign` from the person's own git config, with the key behind a fence that says `~/.ssh` does not exist); three faces of "installed" in ninety minutes, each ✗ true from the seat that gave it; `allow-try` found already in the tree rather than invented | `rule` for the fixture half — `board/README.md`'s plainest form (batch 3's promotion), paid twice more here by a busy-program fixture built on the person's machine; `rule` for the harness rewriting a braced expansion inside a quoted heredoc — the memory `bash-heredoc-expansion`, whose own line this kaizen records as blanked the same way on its first commit.  **Second face of the seat strand, and its best one**: four ✗ in ninety minutes, each saying what and from where, and the same check going green step by step from his shell as he moved things |
| 2026-08-28-0758 | `node-install` closed on a run agreeing with its check; the first answer through the port, 9.4 tokens a second under keep; `env NAME=VALUE` as a grant word, smaller than the card had said; and a cache that segfaulted at the same place on both sides of the boundary, so the runtime's and not the fence's | `rule` — one variable at a time, and the split run on the side that can run it, is `board/README.md` §"What the days taught" (batch 2's promotion: the claim goes to the side that can run it); the two grant lines that killed the node came back out the same hour with the number beside them, which is rule 2 with a defect as its caller.  **First face of the handed-script strand**: "the second start is the measurement" handed Henri a script with no precondition in it |
| 2026-08-28-0848 | the driver's cache 1:22 → 0:11 by hand, and a *miss* under keep told from a refusal by the cache directory's own mtimes, with no debugger; and `make` landed with its test in the same commit, not shown red first, at six minutes on the clock | `rule` — the mtimes are `manifesto.md` §"Go and see"; red-first is the standing rule the kaizen names itself for breaking, and its excuse is answered inside the tree: **the clock is not a reason**, because `board/README.md`'s "a session that ends while the sitting goes on owes nothing" means the line could have waited.  **Second face of the handed-script strand** — the script assumed a runner stops between pulls, and pull two found pull one still up: `recurs` at two, and a third face is a promotion or a reason written down |
| 2026-08-28-0910 | the cache miss read out of an `strace` — `rename` → `EXDEV`, a Landlock ruleset that does not handle `REFER` — and fixed red-first with a raw `rename(2)` because `mv` copies on `EXDEV` and would have hidden it; a tracer that `kill` cannot end ran 25 minutes past its sitting; and a false alarm echoed as agreement | `rule` — go and see at its cleanest: every guess about the cache (runtime broken, driver off, key differs) was wrong, and the syscall and the errno were one run away; choosing the raw syscall over `mv` for the red is §"The three ways an instrument fails" applied before the fact.  The over-analysis half is `recurs` — the read-before-fix strand ([[2026-08-26-1500]], [[2026-08-26-1524]]), promoted at [[2026-08-30-0902]] to the F-entry `suspected` rule; a live process the session cannot see into is the person's hand sooner, not the fence's guesswork longer.  **First face of the person's-report strand**: "not going idle in time" was echoed as the same hang on a run that had already stopped normally at 09:36:14 |
| 2026-08-28-1004 | delivery built red-first, and the red caught a real bug the same harness expansion had planted; the andon *tried* from the fence at Henri's ask and found silent; a cord's question written as a paragraph | `rule` — red-first, and trying the cord is §"Go and do it": the try is what turned `silent-cord` from a design worry into a dated measurement, which is a larger day one than the card had asked for.  The paragraph half is `once` — nothing in `tools/andon.sh` caps a question's length and nothing is owed until a second one arrives.  **First face of "a cord you never pull is a cord you never learn is cut"**, second at [[2026-08-28-1029]] |
| 2026-08-28-1017 | the andon chased three layers down — player present, socket present, the fence blocks — instead of worked around; the asked fix ("install pw-play") measured rather than followed, because the player was already there; and the 10:07 "no socket" reading, which was the fence's view stated as the machine's | **`promoted` — `board/README.md` §"What the days taught"**, with [[2026-08-28-0545]] and [[2026-08-28-0702]] and batch 4's [[2026-08-26-0855]]: **a check has three verdicts, not two — ✓, ✗, and "not from this seat."**  The mechanism exists at two call sites (`tools/launch.sh:302`, `tools/toolbox.sh:80`) and nowhere else, which is where the next face will come from.  And this reading found the *withdrawn* 10:07 sentence still standing in `tools/toolbox.sh`'s comment, citing the card that corrects it — fixed in this commit.  The asked-fix half is the person's-report strand's second face: a fix that is asked is still measured |
| 2026-08-28-1029 | the panel built at Henri's direction, which dissolved the fence-audio problem instead of fighting it; brick 2 flipped gemma's jidoka answer from wrong to right on one tree document; `curses.beep()` shipped as "the sound"; and a commit reported refused when the gate had passed | `rule` — `curses.beep()` is the manifesto strand batch 7 promoted, one layer up: a *sound* that asserts less than it means, closed the only way it could be, by hearing one.  The conditioning measurement is `card:session-program.md`'s, not a rule.  The gate-read-in-haste half is `recurs` — [[2026-08-28-0758]] and [[2026-08-28-0910]], three faces in one day of naming a failure before reading its own output — **not promoted**, on batch 1's reasoning: §"Go and see" already prescribes it, each face cost one round and was caught by the next read, and a session reading too fast leaves nothing for a mechanism to hold |

**What batch 8 showed.**  Ten kaizens of 2026-08-27 evening and
2026-08-28 morning — the day the tree moved to the work laptop, closed
`node-install` on a run, got its first answer out of a local model, and
found the andon silent.  Eight `rule`, and **one promotion**.

The promoted strand is **the seat**: `2026-08-28-0545`'s `check`
inheriting `run`'s seat and calling a by-design read-only directory a
✗; `-0702`'s four ✗ in ninety minutes, each true from its seat and
each saying from where, which is the same lesson done right; and
`-1017`'s *"there is no PipeWire socket on the work laptop"* — written
into a card by a session that could not see a socket live on the host
since 06:26, and corrected eleven minutes later by Henri checking the
host.  Batch 4 read a fourth face ([[2026-08-26-0855]]) as `once`
because the outside seat arrived that hour instead of a rule; three
more faces say the rule was owed.  What makes it promotable rather
than a resolve is that the tree already built the mechanism twice and
never named it — `tools/launch.sh:302` prints a third verdict, `· …
not checked from here`, and `tools/toolbox.sh:80` prints a ✓ that says
what it does not cover.  The promotion is the naming, and the count:
two call sites, every other `--check` still binary.

**And the reading found the rule's counter-example in the tree,
alive.**  `tools/toolbox.sh`'s andon comment still said the work laptop
"had the player and no socket on 2026-08-28", citing
`card:silent-cord.md` — the card whose §10:18 withdraws exactly that
sentence.  The card corrected itself and the file that quotes it did
not, so the fence's view has been standing as the machine's in a tool's
own comment for four days.  Fixed in this commit, and the note in
`board/README.md` keeps it, because a rule that arrives with its own
counter-example attached is worth more than the sentence alone.

Two strands are new at two faces and named to watch: **a handed script
carries its own precondition** ([[2026-08-28-0758]], [[2026-08-28-0848]])
— its third face is a promotion or a reason, and it is the near
neighbour of the `commands-for-henri-fold-in-console` memory, which
governs a handed command's *length* and not its assumptions; and **a
person's report is evidence, not a diagnosis** ([[2026-08-28-0910]],
[[2026-08-28-1017]]), which stands in real tension with the
`question-first` memory and is the more interesting of the two for it.
One strand reached three faces and is **not promoted** with the reason
written: naming a failure before reading its own output
([[2026-08-28-0758]], [[2026-08-28-0910]], [[2026-08-28-1029]]) is
already `manifesto.md` §"Go and see", and each face cost exactly one
round.

**The count**: 104 kaizens in `doc/kaizen/` at this reading; 80 read;
24 unread — at the level of ten, two full days and a short third, with
more arriving.  Batch 9 is filled in on the card.  No day has been
missed yet; the lamp slice still waits for the first one.

**Least certain line**: [[2026-08-27-1723]]'s `recurs` and no promotion
for the default written for the one case in front of the session.  It
reached three faces inside a single day, which is normally the trigger,
and the reason given — the suite caught each within the minute — is the
same reason batch 1 used to *not* promote the reading-is-not-applying
strand, and could be read as an excuse rather than a mechanism.  One
uncertain verdict, not two in a row.  Zero verdict words added.

**Henri's half, answered — the first time in eight batches.**  The
three lines drawn at random and handed at batch 6
([[2026-08-25-0639]], [[2026-08-26-1433]], [[2026-08-26-0931]]) came
back on 2026-09-01 in his words: *"I don't find anything particularly
that I would disagree with in the kaizen ingestion report."*  That is
the measurement the practice exists for, and its first reading is that
the lines hold.  It does not settle batch 1's self-shaped strand, which
asks him to *make* a call a session may not make rather than to
disagree with one; that is still his.

## Batch 9 — read 2026-09-02, the next ten (2026-08-28-1105 → 2026-08-29-2016)

| kaizen | the lesson, in a phrase | verdict |
|---|---|---|
| 2026-08-28-1105 | the reach-free cord heard in the room; brick 3 (`propose.sh`) closed the road with the model's writes confined to a gitignored area by the tool's code and not by `keep` — "the keep-enforced version is owed" | `rule` — the owed half was paid the same day: [[2026-08-28-1313]]'s `keep --connect` and `lead.sh --kept`, a proposal written and a board write refused by the kernel in one turn (`tools/keep.py`, `tools/lead.sh`).  A boundary the bounded party could step around is not the boundary — `vision.md`'s first decision, applied to the tree's own newest tool within four hours.  The order of the bricks (each a tool a person runs, the model one step further from the tree each time) is `once`: a design, not a lesson |
| 2026-08-28-1300 | `andon-panel` closed on his word; `lead.sh` built inside a fifteen-minute sitting because the bricks were already tools; nothing landed live and the kaizen said so — "the live turn is Henri's one command" | `rule` — *proposed, not declared* (`board/README.md` §"What the days taught", batch 2's promotion) done right: the card carries the command and the seat it runs from.  A fifteen-minute sitting against a ninety-six-second gate is `once`, a fact planned around; and the kaizen written at eight minutes left is on the rule's right side |
| 2026-08-28-1313 | the watcher heartbeat and the kernel-confined led turn; two commits refused by the tool's own 120 s timeout inside a 110–119 s suite and first called a flaky test; `$$` and `${…}` eaten by the tool's expansion; `launch.sh` drifted from the installed copy three times in one sitting | `open — card:flake.md` for the refusal read as a flake: *a red that vanishes on retry is a claim about the instrument first* is this kaizen's own sentence and the card's `because`, and [[2026-08-29-1934]] built it (the failure ledger and the shake).  The expansion half is `rule` — the `bash-heredoc-expansion` memory and, since 2026-09-01, `card:rewritten-command.md`, which refuses the route.  The drift is `open — card:lander.md`, measured three more times as the kaizen says |
| 2026-08-28-1401 | the tool ate a `$` in a patch script four hours after 1313 named it, and what closed it was the Write tool; a prompt tuned against one echo produced the next, fixed by reading for the thing the shelf checks; a card stamped "14:20" at 17:33 off the lamp's filename; a one-second fixture between a failed ring and its relay | `rule` — the Write-tool route is the memory `bash-heredoc-expansion`, and the card that refuses the heredoc arrived on 2026-09-01, after this kaizen's own trigger ("if it is a third, it is a line in the README") had been passed; the fixture half is `board/README.md`'s fixture rule, applied within the minute.  **The wrong stamp is a neighbour of the placeholder strand, not its third face**: [[2026-08-25-1404]] and [[2026-08-26-1309]] wrote `14:xx`, which a regex could refuse; this wrote a real-looking time that was wrong, which no regex can — the mechanism batch 4 named for that strand would not have caught this.  It is counted instead as the first face of the sitting-clock strand (see [[2026-08-29-1934]]).  *Read for the thing that is checked, not the shape that was asked* is `once`, and a good sentence |
| 2026-08-28-1830 | `compare.py`'s first run copied the node's `max_tokens` and not its `enable_thinking:false`, and thinking spent all 600 tokens on nothing; the second run had one variable and moved a card, not a dial; the model's draft was better than the session's build and the session said so without landing it | `rule` — half a condition copied from the live thing is the fixture rule in its API form (`board/README.md`), caught by the `usage` line the tool writes into its own account, which is why the line is there.  The draft-not-landed half is the boundary `card:model-acceptance.md` was woken to judge, and [[2026-08-29-0734]] is what a pass licenses: the model proposes, the tree corrects by line, the person lands.  Item 4, batch 4 in the morning, was done at [[2026-08-29-0734]] |
| 2026-08-29-0734 | batch 4 read; Opus's draft landed as canvas day two with two corrections only the parser could supply; `hold` carded around his sentence; a decorator orphaned at 08:05 by the session that read [[2026-08-26-0926]] at 07:40; a README anchor edited from memory; `mutate.sh`'s `fatal:` on every row not chased | `recurs` — the reading≠applying strand of batch 1 ([[2026-08-24-1549]] [[2026-08-25-0626]] [[2026-08-25-0714]] [[2026-08-26-0822]] [[2026-08-26-0926]]) at its **second decorator-shaped face**, which the kaizen asked the ledger to count, and it does: six faces, verdict unchanged — the catcher (`SyntaxError`, one second) is faster than any sentence.  The anchor-from-memory is `rule` — the `patch-anchors-first` memory.  The `fatal:` is `rule` — chased at [[2026-08-29-1934]] into `F002`, and the harness now says `signing?` at exit 3 (`tools/mutate.sh:66`) |
| 2026-08-29-1337 | `hold` day one in four passes at his review; a probe at the commit line (`git commit -m "x"`) landed a commit named "x"; a hold keyed on the pin's name and not its shape; `state` accepted in a hold with nothing honouring it | `once` for the probe — `--dry-run` is named nowhere in the tree but this kaizen, and no second face has arrived.  The field-without-mechanism is `rule` by application: [[2026-08-29-1918]] applied it twice the same evening (a kept turn through a door refused with its reason; a hold with no tick is a bold row), and a lesson applied the next sitting wants no promotion (batch 2's convention).  *Read the card's `because` against the build before "day one landed"* is `once`; and "think critically and don't just obey" is batch 8's person's-report strand done right — his ask measured, and the honest build a row that says *not honoured yet* |
| 2026-08-29-1918 | two decisions of his taken one question at a time, each a sentence that was also the design; the key never on an argument line; a wrong clock in the session's head (19:40 for 19:18); a red check that was green because the stash failed on an untracked directory and "12 passed" was read before the error line above it; the busy-and-silent test flaked once | `recurs` ×2.  The count-before-setup half is the *naming a failure before reading its own output* strand ([[2026-08-28-0758]] [[2026-08-28-0910]] [[2026-08-28-1029]]) at a **fourth face**, and [[2026-08-29-1934]] repeats it as a fifth; batch 8's reason not to promote — `manifesto.md` §"Go and see" already prescribes it, each face cost one round — is kept and is the least certain line below.  The clock half is the **sitting-clock strand**, promoted at [[2026-08-29-1934]].  The flake is `open` — `F001`, since resolved, `card:flake.md`'s first count.  One question at a time is `once`: a form for the person, and it worked |
| 2026-08-29-1934 | `flake` carded and built the same evening — the failure ledger and the shake, 8 of 10 under load, and *the count did not move* after the window rule changed; `mutate.sh`'s "noise" `fatal:` was every gate row refused by a signing failure the fence could not see; a kaizen written mid-sitting because "the sitting ends" was read as "my builds ended" | **`promoted` — `board/README.md` §"What the days taught"**, with [[2026-08-28-1401]], [[2026-08-29-1918]] and [[2026-08-29-2016]]: **the sitting's clock is the lamp's line, read at every decision about scope — never a remembered start, a filename, or the end of a build.**  Four faces in two days: a card stamped off the lamp's filename, a start time paced against for an hour, a kaizen at the end of a build with an hour left, and a third kaizen file for one evening because the lamp cannot tell an extension.  The rest is `rule` — the shake is `card:flake.md`'s instrument and *the count did not move* is the card's argument on its first evening; the signing row is `F002`; "reasoning from a count is still reasoning" is §"Go and see" |
| 2026-08-29-2016 | `spec/kaizen.md` and `spec/kanban.md` written as modules with the author's consent rule at the top; "tell me if you can access it" answered before the work, with the evidence; a sitting extended by hand is the same sitting, and the lamp cannot tell | `rule` — consent first is batch 1's self-shaped finding turned outward, and it is the sheets' first line; "I cannot see it" before the work is the seat rule (batch 8's promotion) done right, and it got the source pasted in under a minute.  The extension is the sitting-clock strand's fourth face, named on `spec/kaizen.md` §"What it still cannot do"; the lamp still cannot, and `card:sitting-everywhere.md` holds the shape — a session may end a sitting and never extend one (`tools/limit.sh:57`).  Item 2 is a date, below |

*(question, waits on 2026-09-05, the week the sheets asked for — does `spec/kaizen.md` still describe `tools/kaizen.sh`, and does `spec/kanban.md` still describe `test/test_board.py`?)*

**What batch 9 showed.**  Ten kaizens from 2026-08-28 midday to
2026-08-29 evening — the road's three bricks closed and the first live
led turns read, the canvas, `hold` in four passes, `flake` carded and
built in one evening, two Claude models on the node's turn, and the
two module sheets.  Five `rule`, two `recurs`, one `open`, one `once`,
and **one promotion**.

The promoted strand is **the sitting's clock**: [[2026-08-28-1401]]
stamped a card "14:20" at 17:33 because the lamp names the sitting
file by its first commit's time and the session took the name for the
clock; [[2026-08-29-1918]] paced an hour against 19:40 when `date`
said 19:18, and named the cost — a session that thinks it has twenty
minutes narrows scope on its own; [[2026-08-29-1934]] wrote a kaizen
with an hour left because "the sitting ends" was read as "my builds
ended"; and [[2026-08-29-2016]] was the third kaizen file of one
evening because an extension by hand arrives on the limit as a fresh
sitting and the lamp cannot tell.  Four faces in two days, and each
kaizen wrote the instrument down — `date`, or the lamp's own *Nm in,
Nm left* — without the tree carrying it anywhere a session reads
before pacing.  The promotion is one paragraph in `board/README.md`
§"What the days taught", with the mechanism named and its honest
limit beside it: inside the commit hook the lamp's line shows the
limit's default rather than the desk's clock (the `lamp-clock-in-hook`
memory), so a clock read off a hook is read again from the sittings
log before it is believed.  It is a rule about sessions written by a
session, so it carries a mark and waits for him.

Two strands were counted on and neither verdict moved.  The
reading≠applying strand reached **six faces** — [[2026-08-29-0734]]
asked the ledger to count its second decorator-shaped one, and it is
counted — and stays `recurs`, on the reason every batch has given: the
catcher is faster than any sentence, and this face cost one second.
The naming-before-reading strand reached **five** ([[2026-08-29-1918]],
[[2026-08-29-1934]]) and stays unpromoted on batch 8's reason, which
is where the least certain line is.  The placeholder-time strand got
a **neighbour and not a face** — a real-looking time that was wrong —
and the reading says why that matters: the regex batch 4 named as the
strand's mechanism would not have caught it.

Three lessons closed by application inside the batch, which is the
count that says the method was working those two days: brick 3's
`keep`-enforced boundary owed at 11:05 and paid at 13:13; the
field-without-a-mechanism from 13:37 applied twice at 19:18; and
`mutate.sh`'s "noise" `fatal:` from 13:37, chased at 19:34 into a
resolved F-number.

**The count**: 111 kaizens in `doc/kaizen/` at this reading; 90 read;
21 unread — two days at the level of ten and a short third, with more
arriving.  Read two days ahead of the table's Friday, at Henri's
"aloita kaizen ingestion -kortilla"; batch 10 is filled in on the
card.  No day has been missed yet; the lamp slice still waits for the
first one.

**Least certain line**: [[2026-08-29-1918]]'s `recurs` and no
promotion for the naming-before-reading strand at five faces.  Batch
8's reason was that each face cost one round and was caught by the
next read; the fourth face was not caught by a read but by the
session's own *second* red check, which it might not have run, and a
green red-check is a fixture that reports the wrong side — the one
shape this tree has promoted twice.  Kept unpromoted because
§"Go and see" is the sentence and no mechanism is in reach of a
session's console; if the sixth face is a red check read green, that
reason is spent.  One uncertain verdict, not two in a row.  Zero
verdict words added.

**Henri's half**: batch 1's self-shaped strand is still his, nine
batches on.  The weekly three lines were answered on 2026-09-01 and
the next draw is a week from then.  And this batch adds one mark to
his grep — the clock rule in `board/README.md`.


## Batch 10 — read 2026-09-04, the next ten (2026-08-29-2031 → 2026-08-30-1852)

| kaizen | the lesson, in a phrase | verdict |
|---|---|---|
| 2026-08-29-2031 | a rule carried across a boundary it does not cross: the fence's rule for restraints was applied to a lamp, and the tree held the proof (six days of the hook line unedited) — before calling a thing enforcement, ask whether it refuses | `rule` — spec/kaizen.md and spec/kanban.md, in his words: "the session implements it, not the author" |
| 2026-08-29-2048 | the failure ledger's first catch was the session's own flake, and it caught it because the session had filtered the gate's output to nothing twice in an hour — the ledger covered for a rule the session broke | `promoted` — memory `suite-output-to-file`, written this sitting on the strand's sixth face ([[2026-08-28-1313]] rule 1, this ×2, [[2026-08-29-2100]], [[2026-09-03-1904]], and 2026-09-04 morning's die flow red); the ledger half is `rule` at card:flake.md and tools/suite.py |
| 2026-08-29-2100 | the defect ledger asked for the minute it was needed, with its first four entries already written in the wrong places; a resolution names its gate or confesses | `rule` — fixme/README.md, test/test_fixme.py; the citation test wrote its own rule (another tree's number carries its tree) before the session read gestate's proposal of it |
| 2026-08-30-0523 | question first, and the second time it was a memory that had died in the fenced home; the record's `V:` line said who answered when the person thought he was talking to another mind | `rule` — memory `question-first`; tools/deliver.sh's `V:` line; card:model-acceptance.md's because met in its plainest form (a 1B model that sorted first in `ls`) |
| 2026-08-30-0730 | a sitting ran twelve minutes past the clock on "one more small thing" after the close; small was true of the code and not of the two test rounds and two gate runs | `promoted` — board/README.md §"What the days taught", *the close is the end*: four faces ([[2026-08-29-2048]] item 4, [[2026-08-29-2100]] item 5, this, [[2026-08-30-1852]]) |
| 2026-08-30-0902 | both defects were read before they were fixed and both `suspected` guesses were wrong — the ticks instrument cost eight seconds where the guesses had cost three gate refusals; `ps` at one instant is not a reading | `rule` — fixme/README.md ("marked suspected until it is measured"); memory `background-task-done`; the fixture rule's fifth face recognised on sight (a burster that burns wall time is idle on a loaded box) |
| 2026-08-30-0952 | a patch script checks every anchor before it writes any file, and no `cd` in a compound command; two gates spent on a partial stage the drift rule refuses in a second | `rule` — memory `patch-anchors-first` (promoted by batch 6 that same sitting); "read the mechanism before reasoning about it" at manifesto |
| 2026-08-30-1624 | a rule was read as a budget by the mind it was written for within the hour, and the fix went where that mind reads — the seat line, nine words, held by a test at 95 of 150 | `once` — the seat line's test holds it; the grep-anchored-on-a-line-start face is the anchor strand's, already a memory |
| 2026-08-30-1741 | four commits in one background command, the fourth killed at the harness's cap, and edits under a running hook; a pathspec commit form nobody asked for tripped F006 | `rule` — memory `commit-one-per-command`; F006 resolved with its gate; journal.md begun the same evening at his "what happened" |
| 2026-08-30-1852 | the sitting's kaizen was written at the person's words and two commits followed inside the same sitting, leaving a two-commit tail owed overnight | `promoted` — the same paragraph as [[2026-08-30-0730]]: a sitting's kaizen is written after its last commit, not after the words |

**What batch 10 showed.**  Ten kaizens from the evening of 2026-08-29
to the evening of 2026-08-30 — six kaizen files for one desk-evening,
the defect ledger born, the first tooled turns, `readchars`, and a
journal begun.  Six `rule`, one `once`, and **two promotions**, one of
them a memory and one a paragraph.

The promoted strand is **the close**: [[2026-08-29-2048]] item 4 said
"the person's close is the end and nothing after it gets a file of its
own"; [[2026-08-29-2100]] item 5 said it again as the sixth file of the
evening; [[2026-08-30-0730]] ran twelve minutes past the clock on one
more small thing after the close, and named it — "the clock is the
person's, and 'one more small thing' after the close is how it stops
being his"; [[2026-08-30-1852]] wrote the kaizen at his words and had
two commits follow it.  Four faces in two days, each writing the rule
into its own last section and none into the tree.  It is the
neighbour of batch 9's promotion (the sitting's clock) and not the
same: that one is *read the clock*; this one is *the close ends the
sitting* — a commit after the person's close is the next sitting's
first, on a fresh clock, and a sitting's kaizen goes after its last
commit.  One paragraph in `board/README.md` §"What the days taught",
with a mark, because a session wrote it about sessions.

The second promotion is the gate-output strand, and it is the batch
reading its own morning: [[2026-08-29-2048]] broke the 13:37 rule twice
in an hour, [[2026-08-29-2100]] once more, [[2026-09-03-1904]] read a
whole-suite red through `tail -6` and lost the traceback, and the
session reading this batch did the same thing to the same test at
05:23 today and had to run the sighting a second time.  The memory
`suite-output-to-file` was written this sitting, before this batch was
read; the reading counts the faces and says what the memory is not — a
mechanism.  A `tools/suite.py` that refuses to be piped is the shape
of one, and that is a card's decision, not a line's.

One count moved without a verdict: **`sudo tend-install` owed** is in
five of the ten ([[2026-08-30-0523]], [[2026-08-30-0902]],
[[2026-08-30-0952]], [[2026-08-30-1741]], [[2026-08-30-1852]]), every
one a launcher commit vetted and not in force.  That is `card:lander.md`'s
because, and its week of log was read this morning: one drift in
twenty-four outlived its sitting.  The five faces here are the same
week seen from the kaizens' side, and the card's question to him
stands.

## Batch 11 — read 2026-09-04, the next ten (2026-08-31-0444 → 2026-09-01-1544)

| kaizen | the lesson, in a phrase | verdict |
|---|---|---|
| 2026-08-31-0444 | the assigned morning: a close-list that named its evidence was workable cold; the lamp's clock read the default from inside the commit hook and the sittings log was read before it was believed; the person's uncommitted words committed as his, named | `rule` — memory `lamp-clock-in-hook` (this kaizen's item 4, promoted 2026-09-01); memory `commit-by-path-never-add-all`'s second half — read the diff, name his hand |
| 2026-08-31-0547 | the benchmark on an agreed checklist, every fault found by a mechanism; and an eyeball reported as a count (two of ten said, four of ten counted, 69 of 300 over the run) on the morning §"Go and see" was written | `rule` — memory `count-before-you-write-it`, where this is the third listed face; board/README.md's fixture paragraph for the test that copied the live home; card:simpleqa.md (later/) for the shell-debt |
| 2026-08-31-1346 | a strand acquitted and broken one minute later — the memory write into the fenced home, judged closed by disuse and then done; the fix a fifth piece of prose until Henri asked for the card | `rule` — done/lost-write.md, the kernel mount; batch 7 recorded its own face and this batch does not count it twice |
| 2026-08-31-1616 | the courier broke on MAX_ARG_STRLEN and the same defect stood four lines below the one fixed; the digest had dropped the priority-1 card for days with nothing said | `rule` — F007, F008 resolved with gates; memory `verify-every-caller` (2026-09-03) for the fix-checked-against-the-whole face, of which this is the first of three, before the memory |
| 2026-09-01-0615 | a cap four days behind the window it was sized for, read off the board's prose instead of the grant; `git add -A` while the person edited; the harness ate a braced expansion four times in one sitting | `rule` — memory `count-before-you-write-it` ("read the file, never the prose about the file"); memory `commit-by-path-never-add-all`; card:rewritten-command.md (later/) and memory `bash-heredoc-expansion`; F008, F009 resolved |
| 2026-09-01-0735 | the reasoning channel found intermittent by a grep nobody asked for; a defect called silent that had printed its warning three times; the boundary written from reasoning and wrong twice in ten lines before the table that took one command | `rule` — F011 resolved (record what came back, not what was asked for); card:rewritten-command.md day one; the table-before-the-rule face belongs to 1348's strand below |
| 2026-09-01-0857 | the gate 297 s to 2 with a line saying when the whole suite last passed; the person's edit committed under the session's message by a named path; and his rule about pace on the day the record showed the need | `rule` — tools/suite.py's last-passed line (it caught F024 on 2026-09-04, one sitting late and not never); memory `commit-by-path-never-add-all` (the `git diff --cached` half); memory `own-pace` |
| 2026-09-01-1011 | the self-shaped mark: he wrote the rule into the manifesto himself, the token was chosen by one grep, and the tree was found to have self-written and not self-approved | `rule` — manifesto.md §"How a practice gets adopted", keeper.md acts 1 and 2, test/test_marks.py; the kaizen's item 2 — whether a mark ever comes off — is counted on the card below |
| 2026-09-01-1348 | six faces of one shape in an afternoon — a sentence written before anything was run against the thing it describes: a token, a gate against the wrong path, a tally that missed 13 of 24, a claim off the wrong column, the person's approval written for him, a suite over a file mid-edit | `rule` — manifesto.md §"Go and see"; memory `count-before-you-write-it`; keeper.md for the approval face (the mark stands empty); the mid-edit face is the strand on the next row |
| 2026-09-01-1544 | a measurement and its subject must both be still — an instrument edited under 48 running arms, then a suite run over a file between its status line and its `git mv`, the narrow rule written after the first letting the second through by the other door | `recurs` — [[2026-09-01-1348]] (both faces are that sitting's, by opposite doors); no third face since, and the strand is named here so the third is counted |

**What batch 11 showed.**  Ten kaizens from the morning of 2026-08-31
to the afternoon of 2026-09-01 — the benchmark, the courier's cap, the
gate split, the mark and the question built and bound, 96 arms of his
money, and the day he wrote the rules section.  Nine `rule`, one
`recurs`, **no promotion**: the batch is the two days on which most
of the memories this session reads at start were written, so nearly
every lesson here already has its place, and the reading's work was
to say which.  Read on the same day as batch 10, at Henri's "aloita
erästä 11", which the plan allows — a batch is the ten oldest unread —
and which is the burst the plan warns about only if it becomes the
habit; the table on the card says so.

The one strand still open is **both still**: [[2026-09-01-1348]] edited
`compare.py` while 48 arms ran through it, wrote "never edit an
instrument a measurement is running through", and three hours later
ran the suite over `F013.md` mid-edit, which the narrow rule did not
catch.  [[2026-09-01-1544]] wrote the broad form.  Two faces, one
sitting, opposite doors; the third has not come in three days, and
this batch says where it will be counted.  Its neighbour is
`count-before-you-write-it`, which gained its fifth face this
afternoon (a commit hash copied off the lamp's line, `2026-09-04-1331`)
— not this batch's, and named because the memory that carries it was
updated today.

One count the batch owed and pays: [[2026-09-01-1011]] item 2 said the
first *strike* is the measurement of whether the mark is real.  Struck
since: four on 2026-09-01, the day they were written; three on
2026-09-04 by his hand while a session worked (board/README.md's close
paragraph and its extension paragraph, board/later/swe-bench.md); and
one placed 2026-09-01 against a session's argument still waits
(board/README.md, the clone paragraph, with his worktree sentence under
it since today).  `tools/meter.py --waiting` lists what waits.
