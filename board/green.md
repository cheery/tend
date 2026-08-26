# green — a gate that has only ever passed is a claim, and nothing checks that a detector detects

    status   open
    because  a test can name a defect, stay green from the day it was
             written, and pass with that defect put back — gestate's F88
             did exactly that, found on 2026-08-25 by mutation in a
             levelled sweep and by nothing else in two trees; the suite
             is the method's whole guarantee, and it has no check on its
             own checks
    asked    Henri, 2026-08-26 — "F88's finding earns a card in tend"
    see      ~/gestate/fixme.md F88 — the entry, the measurement, the repair
             ~/gestate/board/ungated-fixes.md — the sweep; batch 5 is the
             finding, and §"What one entry produces" is the vocabulary a
             verdict has to be spelled in
             ~/gestate/manifesto.md — the second way an instrument fails:
             *an oracle that has only ever passed is a claim*
             ~/gestate/tools/seedmutate.sh — the audit's own mutation run,
             2026-08-24: take a piece away from a copy, expect red.  Tend
             already owns this question, for one detector
             card:kaizen-ingestion.md — the same shape one floor up: a
             record that is written and never read back

## Written from outside, 2026-08-26

**A gestate session wrote this card, not a tend one**, at Henri's words
above, the way `fence` was written on 2026-08-25.  The boundary was
opened by a person for one named thing and nothing else here was
touched.  The finding is gestate's and is quoted with its numbers so
that this card does not rest on a sentence; what tend should do with it
is the card's question and is not answered here.

## What F88 showed, in numbers

`test_the_phase_is_continuous_across_a_note_change` named the property —
a note change must not click — and had been green since the audio
backend was built.  With the defect put back (`stepVoice` computing the
phase from `n`, the exact bug the entry records) **the test passed**.
Its statistic, the largest step between neighbouring samples of the
filtered output, was **0.2226 either way**: that maximum is the
sawtooth's own wrap and not the seam.  The two renders did differ —
max |diff| 0.49 — so the signal had changed and the oracle could not see
it.  And no threshold over that example could ever have worked:
`envAt` is a cubed decay, so the level just before a note boundary is
0.0000 and the phase change happens where there is nothing to hear.

The repair the same day was a fixture chosen so the defect is loud — a
sine at constant level changing 233 Hz to 317 Hz once, with the oracle
the sine's own arithmetic (`2*pi*f/rate`) rather than a chosen number
— and it was **broken before it was trusted**: 1.8159 with the defect
against a ceiling of 0.3735, and 0.2483 correct.  The first draft of
that fixture measured 0.1175 broken against 0.1177 correct, because the
boundary landed on whole cycles of both frequencies.  Three tests in a
row, then, that agreed with the implementation, and only the mutation
told them apart.

## What it is, and what it is not

**It is a problem about detectors, not about coverage.**
`tools/covercount.py` in gestate says which lines the suite has run;
F88's test ran every line it names and proved nothing.  A line executed
is not an assertion that bites, and no instrument in either tree
measures the second.

**It is the sweep's second kind of yield.**  Batches 1–4 of gestate's
sweep found *absence* — repairs with no gate.  Batch 5 found a gate
that is present, named, green, and inert.  One in thirty verdicts so
far; the tail of the file is untouched.

**Tend already holds the shape, once.**  `seedmutate.sh` asks of the
audit exactly this question — take a piece away from a copy, does the
audit go red — and was built the day the audit had only ever been run
on a tree where every piece was present.  That is one detector tested.
Every other check in both trees is in F88's position: it has only ever
passed.

**It is not a demand for mutation testing everywhere**, and the reason
is on gestate's sweep card: a quota is answered by inventing tests that
pass, which is the third way an instrument fails.  It is not a card to
redo the sweep, either — the sweep has eight batches left and its own
schedule.

## What a session does on day one

Measure, not build.  Take tend's own checks — `test_fence.py`,
`test_board.py`, the gates hook — and for each, break the thing it
guards in a copy and run it.  The number that comes back is how many
of tend's detectors detect, and it is the first fact this card needs;
`seedmutate.sh` is the harness and `fence.md` §"What would make this
card wrong" is the shape of a break worth trying first.  A verdict is
spelled in the sweep's five words — *a test, named*; *another
instrument*; *partial*; *none — not yet built*; *none — nothing can* —
or the vocabulary grows for a reason written down.

## What would make this card wrong

If a suite's green is already checked by something — not coverage,
which measures execution — then the problem is named twice and this
card should say where the first one is and close.  And if the day-one
measurement comes back with every detector red on its break, the
problem is gestate's and not tend's, and the card says so and shelves.

## What it must not become

A framework.  The move that found F88 was one hand putting one defect
back and reading one test; the day it needs a plugin, a report page and
a percentage, it has become the thing the quota warning is about.

## Day one, 2026-08-26 — measured

A tend session, at Henri's "look at the new card".  The harness was
`seedmutate.sh`'s shape and thirty lines in the session's scratch, not
the tree: a fresh copy of the working tree per break (`cp -r`, its own
`git init`, the pre-commit hook installed), one `sed` or one file
written, the named detector run on the copy, its verdict read.  A
`cmp` against the intact copy made a `sed` that matched nothing say
`NOOP` rather than pass as a verdict.  **Thirty-eight breaks over the
three detectors the card names: thirty detected, seven survived, one
committed by design.**  The intact copy was green first (178 passed,
13 skipped), so a red below is the break.

**The harness lied twice before it was trusted**, which is the F88
rhyme and belongs on the card: `gate()` read `$?` after a `local` and
reported every `test_precommit.py` verdict GREEN, including the one
where the hook was gone; and one `sed` deleted the `blocked` line it
had just added, so a red came back GREEN.  Both were caught by a
number that could not be right, not by the harness saying so.

### `test/test_fence.py` against `tools/fence.sh` — 17 breaks, 15 red

Every break of the verdict itself went red: `exit $fail` → `exit 0`
(7 failed); a MISSING rule printed but `fail=1` dropped (4); the rule's
name dropped from the MISSING line (4); `valid()` always true (2); the
`--hook` form silent when down (1); the home-spelling normalisation
gone (7); `--restore` reverting a file that parses (1); the `--protect`
hint gone (1).  Every rule dropped from `rules=` went red:
`Edit(./.claude/**)`, `Bash(sudo:*)`, `Read(~/.ssh/**)`, the whole
protected-set loop, and `Bash(git push:*)` — **but that last one only
by accident**: no test names it; what fired was
`test_restore_leaves_a_weakened_file_that_parses`, a test about
`--restore` that happens to drop that rule to make a file "weakened",
and with the rule unchecked the file was not weak and `--restore`
returned 0.  The PreToolUse check with its `fail=1` dropped: red.

**Survived, both from one line** — `for h in kaizen limit fence` in
`tools/fence.sh`:

    GREEN  sed 's/for h in kaizen limit fence; do/for h in limit fence; do/'    19 passed
    GREEN  sed 's/for h in kaizen limit fence; do/for h in kaizen limit; do/'   19 passed

`test_a_hook_removed_is_red` (`test/test_fence.py:198`) drops
`limit.sh` and nothing else.  The fence can stop watching the lamp's
line, and can stop watching **its own** `--hook` line — the exact
removal its header names as the way it dies — and the suite is green
both times.  Verdict: **`partial` — the exit code, the file states,
every rule, and one hook line of three are held; the kaizen and fence
hook lines are not, and `Bash(git push:*)` is held by a test that is
not about it.**

### `test/test_board.py` against the board — 13 breaks, 10 red

Red, each by the one test that names it: a card with no `because`
(listed, so nothing else fired); a `because` line with an empty value;
a valid card not in the README; the README naming a card not there;
two cards wearing one name (`grant` reopened beside `done/grant.md`);
`status done` sitting in `board/`; `status open` sitting in `later/`;
`blocked` with its `blocked` line removed; `blocked  board/nothing.md`;
`status opne`; the header indented three spaces instead of four.  That
last one is red with the wrong words — *"has no `because` line"* while
the line is on the screen — a lamp that lights for the right cause and
names a different one; minor, and noted.

Survived:

    GREEN  because  add mutation testing to the suite        (a because that names a fix)
    GREEN  status   done          in board/done/grant.md     (done, and no date)

The first is the test's own declared limit — *"checked for presence,
not for wisdom: no test can tell a problem from a solution"* — and the
verdict is **`none — nothing can`**, with the docstring as the why.
The second is `board/README.md` §"What a card is" saying `done —
<date>` and nothing holding the date: **`none — not yet built`**, and
cheap.  Verdict for the detector: **`a test, named`**, for everything
it claims to hold.

### The gates hook against a commit — 8 scenarios

Run for real: the copy has the hook installed, and the scenario is
`git add -A && git commit` of a because-less card that is listed in the
README (so exactly one gate should refuse it).

    refused    intact
    COMMITTED  intact, --no-verify                                by design, and documented
    refused    intact, card staged then deleted from the tree
    COMMITTED  pre-commit.sh: `if python3 tools/suite.py || true; then`   test_precommit.py GREEN
    COMMITTED  suite.py: `return 0` in place of `return r.returncode`      whole suite 178 passed
    COMMITTED  hook uninstalled                                    test_precommit.py red — if something runs it
    refused    pre-commit.sh: the drift block removed              test_precommit.py red, and the gate runs the suite
    refused    pre-commit.sh: the kaizen lamp line removed         nothing notices; a lamp, not a gate

The first two survivors are F88 exactly.
`test_the_hook_runs_the_suite_and_nothing_else`
(`test/test_precommit.py:26`) asserts that the string `python3
tools/suite.py` is **in the file** — it is, either side of `|| true` —
so the gate can run the suite, discard its verdict and commit, and the
test that says the hook runs the suite stays green.  And nothing in the
tree reads `tools/suite.py`'s exit code: the whole suite passes with
`suite.py` unable to fail, and the hook, which is one line of `if`
around it, then refuses nothing.  The third is the hook's declared
per-clone gap, and its detector is a test that only the missing hook
would have run: **`partial`**.  The drift case is the good shape — the
gate's own wiring is a test in the suite the gate runs, so removing the
wiring is refused by the gate.  Verdict for the detector: **`partial`
— what the suite refuses, the gate refuses; that the gate honours the
suite's verdict, and that the suite can fail, is held by a string and
by nothing.**

### What the number says

Seven of thirty-eight, and none of the seven is in a *rule* — every
rule the fence names, every field the board contract names, was red
on its break.  Every survivor is in the **wiring between a detector
and the thing that runs it**: the fence not watching its own hook
line, the gate not honouring the suite, the suite unable to say no,
the hook being gone.  That is the same finding as the card's one floor
down: gestate's F88 was a test blind to its own seam, and tend's
blindness is where each detector is joined to the next.  The
day-one measurement is **the question of whether the problem is
tend's or gestate's, answered: tend's** — the fence's two hook lines
and the gate's `|| true` are tend's own files — and so the card stays
open and does not shelve.

What it does not say: that thirty-eight is the sweep, or that seven
more tests are owed.  Three of the survivors are one line each to
close (`drop_hook` parametrised over three names; `test_precommit.py`
running the hook against a scratch commit with a failing suite; a test
that `suite.py` returns pytest's verdict); the `done —` date is a
fourth.  Whether they are closed, and whether the thirty lines of
harness join `tools/`, is the card's next question and Henri's
tiebreak.  The other ten test files were not measured.
