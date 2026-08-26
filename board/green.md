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

## Day one, later — the four repairs, broken before trusted

Henri: *"ok, measure, then build them."*  The before was the table
above: four survivors GREEN.  Each repair was then run against its own
break in a fresh copy, and each break is now red by a test that names
it:

    red  fence.sh not watching kaizen.sh's hook line   test_a_hook_removed_is_red[kaizen.sh]
    red  fence.sh not watching its own hook line       test_a_hook_removed_is_red[fence.sh]
    red  status done, no date, in done/                test_a_finished_or_shelved_card_says_when[grant]
    red  suite.py `return 0`                            test_a_failing_test_is_a_failed_gate  (test/test_suite.py, new)
    red  pre-commit.sh `|| true` around the suite      test_the_hook_refuses_the_commit_the_suite_refuses

The last replaces the string check at `test/test_precommit.py:26`: the
hook is installed in a scratch repository whose `tools/suite.py` is a
stub, the stub says no and the commit must be refused with *"a gate
failed"*, then the stub says yes and the commit must land.  Its first
run refused for the wrong reason — the scratch copy of the hook was not
executable, and the shim's `exec` was what said no — which is why it
asserts the message and not the exit code alone.

**What the two `|| true` and `return 0` rows still say**: the dud card
still *commits* under those breaks, because a gate whose own wiring is
cut cannot refuse the cut.  What changed is that the suite the gate
runs is red on it (`1 failed, 194 passed`), where before it was green —
the detector detects; that the enforcer can be edited by the party it
restrains is `card:work-environment-ai.md`, not this card.  Intact
copy: 195 passed, 13 skipped.

The harness stays in the session's scratch.  Whether it joins `tools/`
— and whether the other ten test files get their day — is still the
card's open question.

## Day one, later still — the harness in `tools/`, and two more detectors measured

Henri: *"put the harness in tools/, then measure test_kaizen and
test_limit."*  `tools/mutate.sh` is the scratch harness rewritten in
`seedmutate.sh`'s shape: one break on the command line, or the recorded
rows at its foot; a fresh copy of the working tree per break, its own
`.git` and the hook installed; and **the harness is checked before any
row is read** — the intact copy green on the detector, and the break
every run knows (`fence.sh` `exit 0`) red — because the morning's
version lied twice.  `test/test_mutate.py` holds the two claims the
harness makes and nothing more; the sweep is minutes and is a hand's.

**The full sweep, 64 rows**: every morning row still red or refused;
the `--gate` column now reads the *whole suite* the gate runs, not
`test_precommit.py` alone, since a gate can never refuse a cut in its
own wiring and the detector there is the suite.  Four rows came back
`NOOP` on the first run — one the harness (`git status` cannot see a
hook removed from `.git/hooks`; it looks now), three my `sed`s
matching nothing — which is the guard doing its job: none of the four
was read as a verdict.

**`test_kaizen.py` against `tools/kaizen.sh` — 12 breaks, 11 red.**
The lamp never lighting, the last kaizen never found, every commit
counted, a want never forgotten, its time comparison inverted, its
stamp at epoch 0, a reasonless want, `--hook` exiting early, exit 1
when lit, the file name gone from the line, an unknown argument
accepted: each red by the test that names it.  Survived:

    GREEN  kaizen: began = last commit, not first    (--reverse dropped)   10 passed

`test_the_next_session_lights_it_again` made one uncovered commit, so
first and last were the same commit and the name could not be wrong.
F88's shape exactly: the fixture had no seam.  Repaired the same hour
— two commits a minute apart (`GIT_COMMITTER_DATE`, in the local
offset, because `--date=format:` renders in the commit's own zone and
the first draft was three hours off), the name must be the first's —
and the row is red by name.

**`test_limit.py` against `tools/limit.sh` — 18 breaks, 17 red.**
Reset from inside a session, the grant regex unanchored, the bare word
granting 45, the grant reaching the session, the block never firing,
elapsed from `last`, the way back in gone, the closed branch dead, the
reason dropped from the state, `stop` keeping the limit, an empty stdin
recording, the wake block removed, a wake writing the state, a wake
logged as a prompt, the prompt text logged, a fresh sitting keeping the
old length, the gap default moved: each red by name.  Survived:

    GREEN  limit: reading the clock moves it          (no-arg read writes started=now)   17 passed

`test_reading_the_clock_grants_nothing` granted and read in the same
second, so `started` rewritten as `now` was the same number.  The same
shape again: a statistic that cannot see the seam because the fixture
put nothing on either side of it.  Repaired — `rewind(5)` before the
read, and the whole state compared, not its first three fields — and
red by name.

**The count for the day**: five test files and the gates hook measured,
64 breaks recorded; nine survived at first reading, all nine now red
by a test that names them, each shown red before it was trusted.
Every survivor was one of two shapes — the wiring between a detector
and what runs it, or a fixture with no seam for the defect to show
through — and none was a rule.  Eight test files remain unmeasured.

## gestate-50's answers, 2026-08-26 — the vocabulary, and the borrowed blindness

Two questions went to the gestate session that wrote this card; the
first message was blocked by its sitting limit (`card:arrival.md`),
the second was answered, and the second answer is measured, not read.

**1. "Caught by a test about something else" is not `partial`.**  On
the sweep card `partial` means a fix with more than one branch where
the gate holds some; here every branch is held, and using the word for
"held by accident" would be the vocabulary growing because a batch
found it awkward.  It is gestate's F77 case from batch 6 the same
morning: held hard, named by nothing, so a tidy-up would have taken the
gate away with no line changing colour.  The move is the cheap one —
a test that names it, red on the mutation before it is trusted, then
`a test, named` with the finding kept on the entry.  Done:
`test_each_named_rule_is_load_bearing` over the four rules `fence.sh`
names by hand; the `Bash(git push:*)` row now fails two tests, one of
them by name.  The sentence about `test_restore_…` stays above.

**2. Yes — the shape travelled with its blindness.**  gestate's
`test_the_hook_runs_the_gates_and_nothing_else` reads the hook's text
and asserts every non-comment line naming `tools/suite.py` also names
`--gates`; its docstring records a 2026-08-24/25 fix of the *spelling*
(it went red when the hook learned `"$PY"`), so the fragility was
fixed and the blindness kept.  gestate-50 changed line 114 of its
`tools/pre-commit.sh` to `… --gates || true; then`, ran the test:
**6 of 6 passed**; restored.  What tend borrowed on 08-24 was a test
that reads a shell script as prose.  gestate's copy was fixed the same
morning — `ffa9c40`, F182, a test in the shape of tend's (hook installed
in a scratch repository, a stub suite answering by a file, the message
asserted and not only the exit), red with `|| true` before trusted.

**And a second tree agrees with the day's two shapes.**  Three of
gestate's five gates in batch 6 were incidental too — `nocturne.ges`
for F81, the prelude for F77.  *Never a rule; always the wiring or the
fixture* holds on gestate's tail as it held on tend's five files.

## Day one, a fourth detector — the lamp, found blind in the live tree

Not a swept file: a defect this session made and then measured, which
is the card's own subject arriving unbidden.  Scheduling the kaizen
readings (`card:kaizen-ingestion.md`), the ledger was first committed
into `doc/kaizen/` — and that put the lamp *out*, because
`tools/kaizen.sh` reads the newest commit touching `doc/kaizen/` as the
last kaizen, and a ledger is not one.  The thirteenth break of the lamp
that morning; the first twelve were in a copy, on purpose, and this one
was in the live tree, by accident, an hour later.

Measured and closed the card's way.  `test_a_non_kaizen_file_in_the_dir_is_not_a_kaizen`
commits a real kaizen, then work, then a stray `ingested.md` into
`doc/kaizen/`, and asks the lamp for `2 commit(s) since the last
kaizen`: **red on the current script** (the stray is read as the last
kaizen and the lamp goes silent), green once the lamp matches a
kaizen's *name* — `doc/kaizen/????-??-??-????.md` — rather than its
directory.  The fix is three pathspecs in `tools/kaizen.sh`; the script
is in the protected set, so it went to Henri as `kaizen-lamp.patch`,
proved green in a scratch copy of the tree first (11 of 11).  The
mutate row `kaizen: lamp matches the dir, not the name` reverts it and
is red once the patch is in.

**Where it sits in the tally**: another *wiring* defect, not a rule —
the detector was joined to its directory where it meant to be joined to
a name.  Every survivor this card has found is one of the two shapes,
and this is the wiring shape in the tree's own reflective organ.

## Day one, a fifth detector — and a launcher a program cannot gate

`node/run.sh` (card:keep.md) wires keep into the node's launch, and
measuring it named a limit worth the card.  Its grant has three parts —
run through keep, code read, state writable — and only one is gateable
through the node: dropping `--allow node.py` fails the run and
`test_the_node_launcher_confines_by_default` goes red (a recorded mutate
row).  **The other two are invisible.**  Drop keep entirely, or weaken
`--write` to `--allow`, and the node runs identically and every test
stays green — because a program that writes only its own state behaves
the same confined or not.  **Confinement is observable only on
overreach**, and a well-behaved program never makes one.

That is not a hole to plug with a contorted test — a probe that makes
the node misbehave would be a fixture inventing the overreach it then
catches, the quota warning wearing a lab coat.  The write boundary is
gated where an overreach is real: `test_write_is_scoped_when_asked` at
the keep level, which `run.sh` composes.  Verdict: `partial` — the code
grant is `a test, named`; the confinement-applied and the write-scope
are `none — nothing can, through this program`, gated one layer down.
The finding for the tally: not every wiring can be gated at its own
layer, and saying which layer holds it is the honest form.

## Day one, the rest of the suite swept — eight files, seven detect, one unmeasurable from this seat

Henri: "look at green, maybe work on it."  The card's standing debt was
eight test files never broken.  Broken now, one break each aimed at the
core property the file guards, through `tools/mutate.sh`:

    red   test_selfmatch.py   an unbracketed `pkill -f` in a tool        test_every_pattern_kill_is_bracket_guarded[summary.sh]
    red   test_summary.py     a cited tool removed / cords un-blocked     test_every_path_the_summary_cites_exists, test_the_not_built_claim_still_holds
    red   test_rules.py       the boot surface grows a second line        test_the_boot_surface_is_one_line[CLAUDE.md], test_the_two_spellings_agree
    red   test_toolbox.py     `--check` claims a change / a syntax error   test_check_changes_nothing_and_says_so, test_it_parses
    red   test_node.py        the pull ledger renamed                      test_a_pull_with_no_runner_is_not_served
    red   test_leash.py       the "budget is spent" message changed        test_a_hang_is_a_crash
    red   test_fence_hook.py  the `leash --` prefix dropped from the wrap  test_everything_else_is_wrapped, test_the_leash_wraps_the_fence… (+7)
    —     test_sandbox.py     the fence's "up" string changed              6 passed, 7 skipped — the detectors skipped

**Seven of eight are `a test, named`** — each break went red on the
test whose docstring is about exactly that property, and each is now a
recorded row in `tools/mutate.sh`, re-run by `mutate.sh` with no
arguments.  No survivors among the measurable.

**`test_sandbox.py` is `none — nothing can, from this seat`, and the
seat is the finding.**  Its checks all need bubblewrap and this session
runs *inside* the fence (`TEND_FENCED=1`), where bwrap cannot nest, so
they skip — a break of `sandbox.sh`'s own output goes green because the
only tests that would see it did not run.  This is the exact shape
`card:work-environment-ai.md` already records for the leash's scope path
and `test_fence_hook.py`'s round-trip: a detector real, named, and
gated behind an unfenced run — a person's, or a gestate session's.
Measuring it is not a build here; it is one run of the suite from
outside the fence, and it is the sandbox sweep's whole owed step.

**Where the whole card stands now.**  Detectors measured: the four of
day one, the lamp, the keep launcher, and these eight — the suite's
files are covered but for the three whose oracle needs an unfenced seat
(sandbox whole, the leash scope path, the fence-hook round-trip).  The
tally holds: every survivor this card has found was the wiring between a
detector and what runs it, or a fixture without a seam, or a boundary a
well-behaved program cannot exercise — never a rule going unnoticed.
The unfenced-seat sweep is the one measurement the card still owes, and
it belongs to whoever next runs tend's suite from outside.
