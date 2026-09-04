# meter — the trees are getting better, and the only instrument that says so is a feeling

    status   open
    because  Henri, 2026-09-04 05:07: "Huomaan muuten että nämä puut
             kehittyvät paremmiksi.  Mutta se on tällä hetkellä vain minun
             tunteeni joka tämän näkee.  Me tarvittaisiin numeroita
             mittaamaan että kehitystä tapahtuu."  The tree writes down
             nearly everything a number would be made of — a kaizen per
             sitting, an F-number per defect, a date on every card, a
             line per red in the failure ledger, a verdict per ingested
             kaizen — and nothing reads any of it back over time.  The
             last run of the one instrument that did (gestate's audit)
             went from 7 pieces to 8 and could not say which, because no
             earlier run was kept
    asked    Henri, 2026-09-04 — "tehdään tästä kortti ja sitten
             toteutetaan se, laitetaan mittari keeper.md -dokumenttiin",
             at a session's list of what could be counted
    see      card:kaizen-ingestion.md — the `recurs` / `once` verdicts
             per kaizen, the one classification already written down
             card:flake.md — the failure ledger the suite writes
             (`~/.local/state/tend/failed.log`, `tools/suite.py`)
             fixme/README.md — an F-number's `status` date; git says when
             its file arrived
             doc/seedaudit-2026-08-31.md — the run kept verbatim so the
             next can be diffed, the lesson this card starts from
             keeper.md — where the person reads the meter and writes his
             own number; act 3
             board/README.md §"What the days taught" — the self-shaped
             mark, which a meter of sessions written by a session wears

## What it is

Counts, by week, read from files the tree already keeps and never
written by a session in prose (a session memory, *count before you
write it*, is four faces of the same lesson).  `tools/meter.py` prints
one row per ISO week — the tree's first commit was a Monday — and says
underneath what it could not count from where it sits:

| column | read from | what it says |
|---|---|---|
| sittings | `doc/kaizen/<date>-*.md` | how often the desk was taken |
| commits | `git log` | the work, per sitting when divided |
| wrong | the `**Wrong, mine.**` paragraph's first word | what a sitting named as its own |
| recurs | `doc/ingested.md`'s verdict per kaizen | how many of the week's lessons were old ones |
| F opened / resolved | the `fixme/` file's first commit; its `status` date | defects found, and closed, and how long that took |
| cards opened / done | the `asked` date; the `status` date | lead time |
| reds | `failed.log`, `gate` and `hand` lines | what the suite refused, and what a hand ran red |
| henri | a `henri: N` line in the sitting's kaizen | his own number, 1–5, blind to the rest |

The **recurs** share is the one that answers the `because` directly:
a tree that teaches has fewer of last week's lessons in this week's
kaizens.  It is also the least trustworthy column, because the verdict
is a session's and a session is the party that would rather call its
own wrong new.  The **henri** column is the person's feeling made a
series, written before the meter is run, so that later the two can be
laid side by side and the mechanical column that moves with his can be
found — or none does, which is a finding too.

The first run is kept verbatim in `doc/`, dated, as the audit's now is.

## What would make this card wrong

If the rows do not move when he says the tree got better — a week he
calls good and a week he calls bad with the same numbers — then these
are the wrong columns, and the card closes saying which he would have
counted.  It is also wrong if a column starts moving on its own: a
`wrong` count that falls because paragraphs stop opening with a number,
a `recurs` share that falls because the ingestion stops saying so.
That is the meter being gamed by the party it measures, and the answer
is not a better parser but the column struck from the table.

## What it must not become

A target.  `tools/mutate.sh`'s header has the sentence: *a quota is
answered by inventing tests that pass.*  Nothing here fails a commit,
lights a lamp, or names a number a session must reach.  Not a dashboard
that grows a column per idea — a column arrives when a week's reading
needed it.  Not a session's report of itself: every column is read from
a file by a program, and the one column the person writes is the one
the person reads.

## Day one — proposed, not declared

`tools/meter.py`, read-only, `--by week` (default) or `--by day`, a
markdown table and a footer of third verdicts — the kaizens it could
not read, and that `--no-verify` leaves no line the tree can count.
`test/test_meter.py` builds its own tree in a temporary directory —
kaizens, F-numbers, cards, a ledger, a two-commit git — and reads the
one row back.  Act 3 in `keeper.md`: run it, read it, write your number
under the sitting's kaizen.  The first run to `doc/meter-2026-09-04.md`.

## Where it sits

Placed last by the session that wrote it, at his "tehdään tästä
kortti"; the tiebreak is his.
