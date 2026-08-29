# fixme/ — the defect ledger

**A card is work to do; an F-number is something that is wrong.**
Opened 2026-08-29 evening at Henri's "I think that we've reached a
point where we need fixme/ -ledger … bit similar design as the board
is, but this is for defects" — the evening `card:flake.md` landed a
failure ledger and its first catch was a race with nowhere to sit but
a card's prose.  The shape is gestate's `fixme.md` with its F-numbers,
in the board's form: one file per defect.

## What an entry is

A file, and the filename is its id: `F000.md`, three digits, never
reused, the next number one past the highest on either shelf.  It
opens with a block of fields, four spaces in, the name and value two
spaces apart:

    status     open | resolved — <date>
    shows      how it shows — the symptom, in whose words; never a fix
    seen       when and where: a ledger line, a test id, a log, the words
    suspected  the cause, marked suspected until it is measured
    gate       (resolved only) the test that holds it, or `none — <why>`
    see        what it leans on: card:<name>.md, a test, a kaizen

`shows` names a **symptom**.  An entry whose `shows` names the fix has
skipped the part a reader can check; the board's rule for `because`,
carried.  `suspected` is marked so because the first guess at a cause
is the part most likely to be wrong and most trusted (gestate's board,
2026-08-17: "an elaboration's mechanism guess is a guess, and should
say so").  `test/test_fixme.py` refuses an entry without `status`,
`shows` and `seen`.

Below the block, the entry's prose: what was measured, what was tried,
what was found — dated, in the words that steered it, as a card grows.

## Where an entry is

`fixme/F*.md` is open: the defect stands.  `fixme/resolved/` is
closed: the defect no longer shows, **and the entry names the gate
that holds it** — the test id that would go red if it came back — or
says `none — <why>` out loud.  This is gestate's most expensive
defect lesson (its `ungated-fixes` card: 62 repairs named by no test,
so a defect closed on a photograph could come back with nobody told),
taken here on day one: a resolution with no gate is a resolution on
trust, and the entry says so.  A move never renames.

**Cite an entry as `F000`**, the bare id, in prose, in a comment, in a
`see` line, in a commit message; it resolves on either shelf, and the
test resolves every citation in this directory and on the board.
**Another tree's number is written with its tree** — `gestate:F182` —
so the two ledgers cannot be confused.  The one bare gestate citation
older than this ledger (`board/done/green.md` cites gestate:F182 without
its tree) is carried as a baseline in `test/test_fixme.py` that may
shrink and never grow, because a done card is history and is not
rewritten.

## What goes here, and what does not

A race, a wrong rule, a harness that lies, a fixture that leaks — a
thing that is *wrong* and can be shown wrong.  Not work to do (a card,
`board/`); not a lesson (a kaizen, `doc/kaizen/`); not a want (a card's
"not built" line).  A defect found while working a card gets an entry
and the card cites it; a card whose `because` is one defect cites the
entry and says why it is a card and not just the entry (usually: the
fix is a design decision).

## Who writes

The session, as it finds them — the session is the only party in the
loop where a defect shows.  Henri names one in a sentence and the
session writes it, with his words in `shows`.  Resolving is the
session's when the gate is named; a `none —` resolution is said to
Henri before it lands.
