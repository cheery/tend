# one-piece — the board works every card at once, and a card in `doing` can sit for weeks

    status   open
    because  a lean consultant, to Henri, after he explained the
             problems he has with his projects (passed on 2026-09-23):
             "Työt on hyvä jaksottaa omiin kokonaisuuksiin siten, että
             työkokonaisuudet seuraavat toisiaan kronologisesti: tällä
             tavalla työkokonaisuudet valmistuvat nopeammin verrattuna
             siihen, että kaikkia työkokonaisuuksia tehdään rinnakkain
             alusta loppuun."  The board read against it the same hour:
             fifteen open cards, three of them `doing` and untouched
             since 2026-08-30 (`hold`), 2026-08-31 (`flake`) and
             2026-09-06 (`session-program`); many more with a day one
             landed and nothing closing them; the README says
             "Priority, not order" and nothing limits `doing`.  The
             counter-example was the same two days: `protocol` and
             `real-program`, worked one after the other to their ends,
             both closed within about thirty hours.
    done     when the board cannot hold two cards in `doing` — the
             commit that would make a second is refused, naming the one
             already there — and each card that was `doing` on
             2026-09-23 has been finished, put back to `open`, or moved
             to `later/` by his word.  (a session's draft, 2026-09-23,
             naming no function; unsigned)
    asked    Henri, 2026-09-23 — "Write the goal into vision.md and card
             the two gates."
    see      vision.md §"The goal" (the principle "One piece at a
             time", and "the project must not consume its creator"),
             card:done-when.md (the other gate: goal before work),
             test/test_board.py (where the board's rules are gates),
             spec/kanban.md (the board as a module; no WIP limit in it)

*(question, his call — the `done` line above: sign it as it stands,
change it, or refuse it?)*

*(question, his call — the three cards in `doing`: for each of `hold`,
`flake`, `session-program`, finish it, put it back to `open`, or move it
to `later/`?  The gate cannot be turned on before this is answered: a
gate is turned on after the tree is clean, never as a way of announcing
that it should be.)*

## What the gate is, and is not

One card in `doing`, across the board.  It is a limit on work begun,
not a pace: it says nothing about how fast the one card moves, and a
week in which it does not move is slack, not a fault (vision.md, his
"weeks can be skipped").  A card that waits on an event or a decision
is not `doing` — it is `blocked`, naming what it waits on, or on
`later/` — so the slot is never held by something nobody can move.

Open questions for day one, not for the `done` line: whether a card
closed in the same commit that starts the next is one move or two;
whether a gestate-side card counts (this gate is this tree's board
only, unless he says otherwise); and whether the lamp says which card
is `doing` at every prompt, the way it names the kaizen owed.
