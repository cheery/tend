# arrival — the sitting limit cannot tell a person sitting down from a session's message

    status   blocked
    blocked  gestate's twin, ~/gestate/tools/limit.sh — the copy the
             block happened in, and Henri's to say there (gestate-50
             put it to him on 2026-08-26 with the F-number question).
             Tend's copy is fixed as of 2026-08-26; until the twin has
             it, a message *to* a gestate session past its limit is
             still not delivered
    because  the limit's whole subject is a person's hours, and it counts
             as an arrival anything that comes through the prompt hook —
             on 2026-08-26 at 07:20 a message from a tend session to a
             gestate session was blocked as if Henri had sat down past
             his limit, wrote a `block` row he did not cause into his own
             ledger, and held back two questions for twenty minutes
    asked    Henri, 2026-08-26 — "The questions were blocked by the
             sitting limiter" … "make a card from it"
    see      tools/limit.sh — the wake exemption of 2026-08-23, the same
             defect for `<task-notification>`, and the shape of the fix
             test/test_limit.py — test_a_finished_background_task_is_not_an_arrival
             and its twin, the tests that fix would be held by
             card:cords.md — a session reaching a session is the cord's
             other end, and this is the first time one was pulled here
             card:green.md — the message that was blocked

## What happened, in numbers

At 07:20 a tend session sent a gestate session the day-one numbers of
`green` and two questions.  The harness delivers a cross-session
message to the receiving session as a prompt, wrapped
`<cross-session-message from="…">`, so it reached gestate's
`limit.sh --hook` as though Henri had typed it; his sitting there was
ten minutes old of a ten-minute grant, and the hook did what it is for
— `block gap=9 elapsed=10 limit=10`, the ledger's row at 07:20:29.  The
questions were not delivered.  Henri saw the block, told the tend
session at 07:41, and the message was sent again into a fresh grant.

Reproduced on a temporary desk before this card was written: a
15-minute grant, the start moved back twenty minutes, a
`<cross-session-message>` on stdin — **exit 2, "The 15 minutes are
up", and a `block` row.**  Same script, same branch, same words as the
2026-08-23 defect for `<task-notification>`, whose fix is twelve lines
above the block.

## What it is, and what it is not

**It is the wake defect's twin, and the fix it wants is the same
shape**: log it under its own name and never block.  A session's
message is not a person at the desk; refusing it protects nobody's
evening and hides a question somebody already asked.  Deliberately
before the state write, for the same reason the wake is: a message
landing in a silence must not open a sitting nobody sat for.

**It is not a case for the limit knowing who is talking.**  The hook
reads a prompt and cannot know; what it can know is the literal tag
the harness wraps a session's message in, exactly as it knows the
notification's.  The match is on the tag, not the words — Henri asking
*"why was the cross-session message blocked?"* is a person at the desk.

**It is not tend's copy alone.**  The block happened in gestate's
`limit.sh`, the twin that Henri keeps intact on purpose; tend's copy
has the same lines.  The header of both says a fix in one is owed to
the other by hand.

## What a session does on day one

Build, and small: the tag added beside `<task-notification>` in
`tools/limit.sh`, logged as its own event so `tools/sittings.py` can
filter it; two tests in `test/test_limit.py` in the shape of the wake's
— it passes even past the limit, it leaves the state untouched, and a
prompt that merely mentions the tag is still an arrival — each shown
red before it is trusted (`tools/mutate.sh` is there for that).  Then
the debt to gestate's twin, written where its header says.

## What would make this card wrong

If Henri decides a session's message *should* wait for the person —
that a sitting closed is closed to sessions too, and a question held
twenty minutes is the limit working — then this is a feature, the row
in the ledger wants a name rather than an exemption, and the card
closes on that decision.  That is his call: it is his ledger and his
hours.

## Day one, 2026-08-26 — built, through the person's hand

Henri: *"arrival needs a fix.  it's not a feature in my eyes that
limit.sh blocks the messages from others."*  So the last section's
question is answered and the fix is the wake's shape.

`tools/limit.sh` is in the protected set — read-only against the shell,
denied to the edit tools — so the sixteen lines went to Henri as
`arrival.patch` and his hand applied them (`git apply arrival.patch`,
then the file was removed): after the wake block and before the state
write, a prompt carrying the harness's `<cross-session-message` tag is
logged as `message` and passes, exit 0.  The match is on the tag, not
the words.

**Red before trusted**, in both directions.  The three tests in
`test/test_limit.py` were written first and run on the unfixed script:
the two that should fail failed (`…is_not_an_arrival`,
`…delivered_even_past_the_limit`), and the guard that a prompt merely
*mentioning* a message is still an arrival passed, as it should on
either script.  Then, with the fix in, three rows in `tools/mutate.sh`:

    red  limit: the message block removed        …is_not_an_arrival, …delivered_even_past_the_limit
    red  limit: a message writes the state       the same two
    red  limit: a message is logged as a prompt  …is_not_an_arrival

Suite: 20 of 20 in `test_limit.py`.

**What is not done, and why the card is `blocked` rather than
`done`**: the block happened in gestate's copy, which runs
`~/gestate/tools/limit.sh` from its own settings, and that copy is
Henri's to change — the twins' header says a fix in one is owed to the
other by hand, and the debt is now written in tend's copy beside the
fix.  Until it is paid, a message from tend to a gestate session past
its limit is still not delivered; the reverse direction is.
