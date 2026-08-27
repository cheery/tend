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

## 2026-08-27 — taken into a batch: the cord built, rung, measured socket-only; the count closed at zero

Henri: *"cords could be taken now into this batch"* — four days into
the week, the count above still "(none yet)".  The card's own "what
would make this wrong" says a cord nobody pulls; the reason not to wait
is `session-program`'s: a node has no person watching its transcript
and needs the cord more than a hosted session does.  So the count
closes at **zero guessed questions in four days of hosted sessions**,
written here so the week's evidence is not lost under the build, and
the andon is built for the node's sake as much as the session's.

**Built: `tools/andon.sh`**, 8 tests — the three parts the 08-25
section named.

1. **The cord.**  `ask` writes the question first; `ring` prints the
   batch and rings — at most three, eight seconds apart, gestate's
   numbers kept with their reason; a second ring within ten minutes is
   refused and says when; a ring with nothing asked is refused as noise.
   `pulled` is the record a program reads: a question asked and rung
   and not yet answered.  `answered` is the person's word, refused
   inside the fence.  Gestate's synth did not travel (tend has none): a
   two-note wave from python's `wave`, through the PipeWire socket.
2. **The row, measured.**  Rung from inside the fence with `REACH=audio`,
   the player under `strace -f -e openat,connect`: one connect, to
   `$XDG_RUNTIME_DIR/pipewire-0`; **nothing opened under `/dev/snd`**.
   So `audio` can be the socket alone, and the narrowing is the third
   commit on the branch `install-day1` (`tools/sandbox.sh` is
   protected) — proposed, not declared: the sandbox tests skip inside
   the fence, and the next ring after the merge is the measurement.
3. **The count** — closed above.

**The first question went through it.**  *"install prefix:
/usr/local/lib/tend (root-owned) — the session recommends it; say if
you want the user-owned one instead"* — asked, rung once at 15:52, and
pending in `~/.local/state/tend/andon.pending` until Henri's
`tools/andon.sh answered`.  The session went on with its recommendation
rather than stop: the cord is for reaching him, not for waiting on him.

**`sitting N because andon`** now verifies against `andon.sh pulled`
(the branch's first commit, `test_limit.py` +2, green with the record
real and red with it faked), which closes the blocker
`sitting-everywhere`'s day one left on the word.  The honest hole is in
the script's header: a session can ask and ring to earn the reason —
but the ring is loud, and that is the check, and it is not a program's.

**Recommendation: done, on Henri's review after the merge** — the
shape `fence` and `green` closed in.  What the card leaves to others:
the andon on a *node* is `session-program`'s, and waits with the rest
of that card on the first node that leads work.
