<!-- PROPOSAL — drafted by the tend llm node through the openrouter door (tencent/hy3) on 2026-09-04 17:26.
     NOT tree content until a person reads it and lands it by hand.
     Task: draft a `--diff PREV` flag for tools/meter.py that prints each week's delta against a kept run (doc/meter-*.md), so two runs are actually comparable
     Material: /home/henri/tend/board/meter.md
     The model proposes; the person applies (card:session-program.md, brick 3). -->

# meter-diff — two runs are not comparable until one is kept against the other

    status   open
    because  board/meter.md — the last run of gestate's audit went from
             7 pieces to 8 and could not say which, because no earlier
             run was kept; the seedaudit was kept verbatim so the next
             could be diffed, and the meter's first run lands at
             doc/meter-2026-09-04.md for the same reason.  The meter
             prints one row per week but every run is a fresh table;
             without a diff against the kept one, the audit's failure
             repeats: a number moves and no one can say which week did
    asked    a --diff PREV flag for tools/meter.py that prints each
             week's delta against a kept run, so two runs are actually
             comparable
    see      board/meter.md — Day one; the first run to doc/meter-*.md
             doc/seedaudit-2026-08-31.md — the run kept verbatim so the
             next can be diffed, the lesson the meter starts from
             test/test_meter.py — builds its own tree; reads the one row
             back

## What it is

A `--diff PREV` flag added to `tools/meter.py`, read-only like the rest.
PREV means the newest `doc/meter-*.md` by date; `--diff <path>` means
that file.  For each ISO week the plain run prints, the flag prints the
delta of every numeric column against the same week in the kept run:
sittings, commits, wrong, recurs, F opened/resolved, cards opened/done,
reds, for him, henri.  A week present in one run but not the other is
delta'd against empty, so a born week reads as +, a gone week as -.
The footer of third verdicts stays, and adds the weeks the kept run had
that this one does not, so a dropped week is not silent.

## Why PREV is the kept run and not a session's pick

The audit failed because no earlier run was kept to say which piece
moved.  PREV is the last kept, by dating, because the comparison that
was missing is exactly the one against the prior kept table.  A path is
allowed only so a run can be diffed against the seedaudit-shaped first,
not the one just before it; the session never chooses a week to compare,
it compares against what was kept.

## What would make this flag wrong

If the delta cannot be laid beside his number — a week he calls better
showing red on the columns that answer the because, a week he calls
worse showing green — then the diff carries the wrong columns and the
flag closes saying which it should have.  It is also wrong if PREV is
read as prose: every cell is read from the kept markdown table by the
program; the person writes nothing into the comparison, only reads it.

## Day one — proposed, not declared

In `tools/meter.py`: `--diff PREV` (or `--diff <path>`), parsed after the
table is built, printing a +/- per cell or a second delta table.
`test/test_meter.py` writes one tree kept to a temp `doc/meter-*.md`
and one run fresh, and reads the delta row back.  The first diff is run
against `doc/meter-2026-09-04.md` at the next week's reading, kept
verbatim next to it.
