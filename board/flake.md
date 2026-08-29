# flake — a red that vanishes on retry is met with memory, and the tree keeps no count

    status   doing
    because  three times in six days a test failed once and passed on
             the re-run, and each time the session met it with "run it
             again" and its own recollection — nothing in the tree kept
             the failure, so the next session met the next one cold.
             Each was real once counted: 2026-08-26, "1 in 10" by hand
             found two defects in the resolver; 2026-08-28, two refused
             commits were the tool's 120 s timeout, not a test; 2026-08-29,
             the launcher's busy rule (half a core in the last second,
             tools/launch.sh) stopped a busy loop under the suite's own
             load, which is what it would do to llama-server on a loaded
             box.  Henri, 2026-08-29: "I see sessions have tripped to flaky
             test several times now.  Would there be a way to catch the
             flake?"
    asked    Henri, 2026-08-29, 19:29 — "lets card it, then do it."
    see      card:kaizen-ingestion.md (the same problem, in test form: a
             lesson nothing reads back), card:green.md (the detectors are
             sound; the blindness is in the wiring), card:node-install.md
             (the busy rule this card's third flake is about)

## The problem

A flake is a failure with a cause the session cannot see from one run,
and the tree's answer to it has been the session's memory: re-run,
green, move on, write a kaizen line.  The kaizens show the cost —
`2026-08-26-1500` ("the flake is not explained"), `2026-08-28-1313`
("a red that vanishes on retry is a claim about the instrument first"),
`2026-08-29-1918` (the busy rule under load, "not chased") — three
sittings that each started from nothing.  What every one of them
needed first was a **count with a signature**: how many times, which
test, under what load, how long the run was.  The 08-26 sitting made
that count by hand, ten runs, and it was enough.

## Day one

Two mechanisms, both in `tools/suite.py` — the one name for the gates:

1. **The failure ledger.**  Every run the suite makes writes one line
   per failed test to `~/.local/state/tend/failed.log`
   (`TEND_FAILED_LOG`): when, where (`gate` from the hook, `hand` from a
   terminal, `shake` from below), the test id, the load average, the
   wall.  On the person's side, not the tree — a failure is a fact
   about a run on this machine, and inside the fence the state
   directory is the one place the gate can write.  And the suite reads
   the ledger back before it speaks: a failure that has a line already
   is reported as *seen before, N times, last at …* — the count is in
   the same output as the red, so no session meets a flake cold.
2. **The shake.**  `tools/suite.py --shake TEST [N]` runs one test N
   times (default 10) while every core is burning, and says *k of N
   failed under load*; each failure is a ledger line marked `shake`.
   The 08-26 "1 in 10" as a tool, with the load half that would have
   caught the 08-29 one in one run.

Red first: a failing test in a scratch tree leaves a ledger line naming
it and the seat; a passing suite leaves nothing; the second failure of
the same test says "seen before"; a test that fails on every other run
shakes to "2 of 4".

## Rules

1. **Never a silent retry.**  The suite runs once and reports once; the
   shake is the person's or a session's deliberate act, and its count
   is the finding.  A gate that retries until green is a gate that has
   stopped measuring.
2. **A vanished failure is still a line.**  The ledger is append-only
   and nothing removes a line because the re-run passed.
3. **The count is not the cause.**  The ledger says *how often* and
   *under what*; the reasoning is the session's, from the signature, as
   on 2026-08-26.

## What it must not become

A quarantine list (a test marked flaky and skipped is a detector wired
to nothing — `card:green.md`'s exact blindness).  A retry-until-green.
A second suite runner.  Or a page: the ledger is lines a `grep` reads,
and the suite's own "seen before" is the only reader until one is
wanted.

## What would make this card wrong

If the three flakes turn out to be three unrelated accidents and no
fourth arrives, the ledger is a file nobody opens.  The evidence
against is the busy rule: a load-sensitive threshold in the launcher
will trip again on any loaded box, and the shake is how that is
measured before it trips on the GPU.
