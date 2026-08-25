# cords — a session in tend cannot reach a person, and nothing ends a sitting

    status   blocked
    because  a session that hits a question it cannot answer has two
             bad moves — guess, or stop silently — and this tree offers
             it nothing else; and the person's hours are governed here
             by nothing at all
    asked    Henri, 2026-08-24 — "add the needed cards so that the
             absent work is completed"
    blocked  the andon's week: it waits on 2026-08-31 and the count of
             guessed questions, per this card's own last section.  The
             sitting limit no longer waits on anything — installed for
             tend on 2026-08-24, and gestate keeps its own copy by
             Henri's decision (below)
    see      ~/gestate/tools/andon.sh, ~/gestate/tools/limit.sh — the
             two cords gestate has; the audit calls both absent here
             card:work-environment-ai.md — the budget, grant and
             lifecycle these two are the person-facing half of
             vision.md — "won't demand your presence", "any project must
             not consume the person leading it"

## What it is

Two cords, and they are the two pieces most about people:

* **The andon** — a way for a session to ring a person, capped, with
  the questions batched first.  Gestate rings a sound card because it
  has one; tend needs *a* cord, not that cord — what transfers is that
  a session must be able to reach the author and be answered.
* **The sitting limit** — one-way: a session may end a sitting and may
  never extend one.  Gestate's is a `UserPromptSubmit` hook; when it
  moves here it moves *out* of gestate's write access, which is what
  this tree is for.

## What would make this card wrong

If the sessions that run here never have a question a person must
answer — then the andon is a cord nobody pulls.  Run without it for a
week first and count the questions that got guessed.

## 2026-08-24 — the sitting limit moved; the andon's week started

**The sitting limit is here**: `tools/limit.sh`, gestate's mechanism
byte-for-byte with a new header saying why it moved, checked by
`test/test_limit.py` (also carried whole — the asymmetry it holds did
not change by moving).  The GESTATE_* names and the log at
`~/.local/state/gestate/sittings.log` stay, so the GAP_MIN evidence and
gestate's `gapcheck.py` keep working.

**Installed for tend the same day**: Henri ran the jq edit himself —
hook config is enforcement, so the edit was his — and tend's
`.claude/settings.json` now runs `tools/limit.sh --hook` on every
prompt, from the next session on.

**And gestate keeps its copy**, which resolves the card's "moves out"
sentence into something better said as *tend has its own*.  Henri,
2026-08-24: *"I think it's better to keep gestate's limit intact for
now.  So that it can be tried on different machines."*  Gestate stays
portable as one piece; on this machine both hooks read one state file
and one log, so it is still one desk and one clock.  The cost accepted
with it: the copies are twins, and a fix in either is owed to the other
by hand — `tools/limit.sh`'s header carries that debt.

**The andon deliberately waits**, per the section above: the week runs
2026-08-24 → 2026-08-31.  The count lives here — a session that
guesses where it should have asked appends one dated line below, and
what the line says is the question, not the guess:

* (none yet)

## 2026-08-25 — the first of three waypoints, and where the andon will run

Henri, having read the direction: *"Put those three on the board as
cards.  They are excellent waypoints."*  The first waypoint is this
card, so it is written here rather than on a duplicate.

When the andon arrives on 2026-08-31 it arrives into a tree that now
has a fence (`tools/sandbox.sh`, `tools/fence-hook.sh`, installed
2026-08-25), and that changes what it is: **the first program tend did
not write, running under the fence**, and the first row Henri will
ever put in `TEND_REACH_ALLOW` — `audio`.  So the card's work now has
three parts: the cord itself (a session rings, capped, batched); the
row measured properly — a socket-only ring, so that `audio` stops
meaning the whole card, microphone included
(`doc/experiments/2026-08-25-both.md`); and the count above, closed
on the day.  The fence is a cage with no bell until this lands.
