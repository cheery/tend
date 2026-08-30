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
