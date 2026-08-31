# lost-write — a write into the fenced home vanishes, and the session believes it landed

    status   open
    because  inside the fence `$HOME` is a tmpfs, so every shell write to
             `~/.claude/…` fails — and the one thing kept there is the
             session's own memory, where the lesson not to do it lives.
             Four faces: `doc/kaizen/2026-08-25-0714.md`,
             `2026-08-26-1323.md` (whose memory write "died in the fenced
             home"), `2026-08-26-1712.md`, which wrote its own trigger —
             *"if this recurs a fourth time, it is a mechanism owed, not
             a resolve"* — and 2026-08-31, where the fourth face was
             produced **one minute after** the session read all three and
             recorded the strand as closed, in the next command it ran
             (`doc/ingested.md`, batch 7).  The countermeasure has been
             prose every time: a kaizen, then a memory, then another
             memory.  Prose has now failed four times, and the failure is
             quiet — the shell says `No such file or directory` and a
             session that does not read the exit status has written
             nothing and knows nothing
    asked    Henri, 2026-08-31 — "you can open the card for the
             ~/.claude check", after the batch-7 reading named the
             mechanism as owed and refused to build it from a ledger line
    see      card:fence.md (the tmpfs home is the fence's shape, not a
             bug in it), card:keep.md (what a program may reach is a
             grant applied from outside), card:self.md (a session cannot
             enforce against itself — the check belongs on the person's
             side, as the hooks do), card:kaizen-ingestion.md (the
             reading that found the fourth face and named this),
             doc/ingested.md batch 7, tools/fence-hook.sh (the
             PreToolUse hook a check would ride), tools/sandbox.sh

## The problem

Not that the write is refused — that is the fence working.  The
problem is **what the refusal looks like from inside**: one line on
stderr, a non-zero status, and a session that has moved on.  Nothing
downstream notices.  The memory is not there, the next session does
not have it, and no lamp, gate or test says so; the tree's whole
method is *being wrong has to be visible*, and this is a way of being
wrong that is visible only to a reader who was already looking.

What makes it worth a card rather than another note is the shape of
the recurrence.  This is not a lesson nobody wrote down — it has been
written down four times, most recently as a memory *about itself*, and
it was violated by the session that had just finished reading its own
history.  A rule that fails inside the sitting that reads it is not
under-documented.  `card:kaizen-ingestion.md`'s §"The hard part"
already says the honest limit: an ingestion can promote prose, and
prose is what has been failing.

## Day one — proposed, not declared, and three shapes

**Measure first.**  Four faces in seven days is the count that
justifies a card; it is not yet the count that picks a mechanism.  The
first thing day one does is say how often a `~/.claude` path reaches
a Bash command at all — the leash ledger (`~/.local/state/tend/leash.log`)
has every fenced command this tree has run, so the number is a grep,
not an estimate.  If it is four in seven days, a hook is worth it.  If
it is four ever, the memory written on 2026-08-31 may be enough and
this card closes on that measurement.

Three shapes, kept alive on purpose (`manifesto.md` §"Set-based"):

- **(a) Refuse the write.**  A rule on the person's side — the
  `PreToolUse` hook, beside the fence's — that refuses a Bash command
  which *writes* to a path under `~/.claude`, and says the one useful
  sentence: *use the Write tool.*  Cheap, immediate, and the same
  shape every other restraint here has: enforcement outside the party
  it binds.
- **(b) Make the loss loud.**  Leave the write refused as it is and
  add the missing half — something that notices a failed write to the
  memory directory and says so where a session will see it, the way
  the kaizen lamp says an owed file.  This treats the real defect as
  *silence*, not as the attempt.
- **(c) Give it a supported path.**  A `tools/remember.sh` that runs
  on the person's side, as `tools/deliver.sh` does for the door, so
  the write a session wants has somewhere legitimate to go and the
  refusal has an answer.  The most work, and the only one that leaves
  a session able to do the thing it was trying to do from where it
  actually sits.

What would kill each: (a) is dead if the false positives bite — a
command may *name* `~/.claude` for good reasons (this card's own
commit message does; `git grep`, the fence's own tests, and
`tools/fence.sh` all read that path), so the rule must key on the
write and not the string, and if that cannot be done cleanly in a hook
it is the wrong shape.  (b) is dead if nothing can see the failure
without wrapping every command.  (c) is dead if the Write tool already
is that path — which it is, which is why (c) is last.

## The hard part, named

**A mention is not a write.**  The naive check — refuse any command
containing `.claude` — would refuse `grep -rn claude board/`, the
fence's own `--check`, and the commit that lands this card.  A useful
rule has to see redirection (`>`, `>>`, heredocs), the tools that take
a destination (`cp`, `mv`, `tee`, `install`, `mkdir`, `touch`, `sed
-i`) and nothing else; and a shell is a language, so any such reading
is a heuristic that will be wrong at the edges.  The tree's standing
answer to that tension is `card:fence.md`'s: the *kernel* decides, and
a heuristic that guesses is worse than no heuristic — which is an
argument this card must answer before (a) is built, not after.

## What it must not become

A second enforcement layer that only *looks* like one.  The fence is
real because the kernel refuses; a hook that pattern-matches shell text
is advice with a veto, and if it is trusted as a boundary it will be
routed around by the first command it does not parse.  Whatever is
built here says plainly which of the two it is.  And it must not grow
into a general "lint the session's commands" mechanism — one refusal,
one message, or nothing.

## What would make this card wrong

If the memory written on 2026-08-31 holds.  The strand's whole history
is prose failing, but the newest prose is one day old and has not been
tested by a fifth occasion; a card that builds a hook next week
without checking whether the fifth face ever came would be building
what nothing needs.  **The measurement that decides it**: no fifth
face by 2026-09-07, with the leash ledger grepped rather than
remembered, closes this card and the memory keeps the job.

## Where it sits

Placed last by the session that wrote it, 2026-08-31, at Henri's "you
can open the card for the ~/.claude check"; a new card arrives
unplaced and the tiebreak is his.  It is the first card in this tree
opened *by an ingestion* — `card:kaizen-ingestion.md` read the pile,
found the strand at its fourth face, refused to build a mechanism from
a ledger line, and named what a card would be for; this is that card,
which is the reflective organ that card exists to be, working once,
end to end.
