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
             nothing and knows nothing.  **And it need not even say
             that**: the tmpfs home is writable, so the natural repair
             for that error — `mkdir -p` — makes the next write succeed,
             exit 0, and evaporate with the sandbox (measured below,
             2026-08-31, at Henri's question)
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

## Measured 2026-08-31, an hour after the card was opened

Henri, reading it: *"should the `$HOME` stay `$HOME`?  Kind of makes
sense to me."*  It should, and the reason is the clock — but the
question was worth more than its answer, because measuring it found
the card understating its own defect.

**`$HOME` should stay `$HOME`.**  The fence does `--tmpfs $HOME` and
then `--setenv HOME $HOME`: the same address, an empty room, three
things carried back in (`~/.local/state/tend` and
`~/.local/state/gestate` read-write, `~/.gitconfig` read-only).  Those
work *because the path inside equals the path outside* —
`tools/limit.sh` resolves `$HOME/.local/state/gestate/sittings.log` on
both sides and gets the same file.  That is why `sandbox.sh --check`'s
first probe is that the sitting clock inside is the host's, and why
`doc/experiments/2026-08-25-sessions-first-fence.sh` matters: a fence
that hides the state directory defeats the sitting limit.  Move
`$HOME` and every `~`-relative path means one thing inside and another
outside — the clock, the leash ledger, the kaizen want — and each
would have to be rewritten absolute to buy the property back.

**The tmpfs home is writable, so the loss can be silent.**  The
2026-08-31 face was loud only by luck: it appended to a path whose
parent did not exist, so it got `ENOENT`.  From inside the fence:

    $ touch $HOME/.probe-write
    -rw-rw-r-- 1 henri henri 0 Aug 31 14:48 /home/henri/.probe-write
    $ mkdir -p ~/.claude/projects/-home-henri-tend/memory
    mkdir OK
    $ printf 'a memory that will evaporate\n' > ~/.claude/…/memory/PROBE.md
    WRITE SUCCEEDED — exit 0, no error

and nothing of it exists outside.  `mkdir -p` is the natural repair
for the error the loud face gives, which is exactly why the memory
written that morning says *"do not retry it with `mkdir -p` — switch
tools"*; that sentence was written on instinct and is in fact the
whole trap.  So the defect is one step worse than the `because` first
recorded it: not *the write fails and may go unnoticed*, but **the
write can succeed and be lost**, with nothing to notice.

## Day one — proposed, not declared, and four shapes

**Measure first.**  Four faces in seven days is the count that
justifies a card; it is not yet the count that picks a mechanism.  The
first thing day one does is say how often a `~/.claude` path reaches
a Bash command at all — the leash ledger (`~/.local/state/tend/leash.log`)
has every fenced command this tree has run, so the number is a grep,
not an estimate.  If it is four in seven days, a hook is worth it.  If
it is four ever, the memory written on 2026-08-31 may be enough and
this card closes on that measurement.

Four shapes, kept alive on purpose (`manifesto.md` §"Set-based"), and
**(d) arrived from the measurement above and is the one to beat**:

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

- **(d) Let the kernel refuse it.**  Bind an empty **read-only**
  directory at `~/.claude` inside the fence, so every write there is
  `EROFS` — always, in every shell, with no pattern to match and no
  command to parse.  This is the shape the tree already trusts: rule 1
  says a program's reach is a grant applied from outside, and the
  fence's whole argument (`card:fence.md`) is that the kernel decides.
  It also answers this card's own objection to (a) before (a) is
  built — a heuristic with a veto is not a boundary, and this is a
  boundary.  About one line in `tools/sandbox.sh`.

  **Built 2026-08-31**, at Henri's *"defect is a caller.  yeah, you
  can fix the thing you found"* — `--tmpfs $HOME/.claude
  --remount-ro $HOME/.claude` in `tools/sandbox.sh`, one line, after
  the cords are bound and before the environment is set.  The
  `--ro-bind of an empty directory` candidate was dropped for a
  reason: every empty directory on this machine that a session could
  name is one a session could also write to, and a bind would make
  those writes appear inside `~/.claude` — a tmpfs is nobody's.

  **It ran, 2026-08-31 15:16, and this is the measurement.**  Henri:
  *"I ran the commands"* — `tools/sandbox.sh --check` on the tree's
  copy, then `sudo tend-install`.  `install.sh --check` says *in
  force: the installed set, at HEAD*, and from inside the fence, in
  the next command after his:

        $ ls -lad $HOME/.claude
        drwxr-xr-x 2 henri henri 40 Aug 31 15:16 /home/henri/.claude
        $ ls -A $HOME/.claude            → (nothing)
        $ mkdir -p $HOME/.claude/projects/x
        mkdir: Read-only file system
        $ touch $HOME/.claude/probe
        touch: cannot touch '…': Read-only file system
        $ printf x > $HOME/.claude/probe
        bash: …/probe: Read-only file system
        $ mkdir -p $HOME/.claude/projects/-home-henri-tend/memory
        mkdir: Read-only file system

  The last one is the whole point: that is the command whose silent
  success on the same morning is why this card exists, and it is now
  the loudest of the four.  The person's own memory outside is
  untouched — read back through the tool that runs there, eight lines,
  all present — and a session still sees nothing of it, which is the
  secrecy the old probe asserted, kept.

  **What has still not executed** is the *pytest* form.
  `test/test_sandbox.py::test_the_sessions_memory_directory_is_an_empty_
  read_only_mount` skips from inside the fence and runs when the suite
  is run from Henri's seat; the shell probes in `--check` did run
  there, which is the same property by the script's own instrument.
  Named rather than counted as green.

  **The line that had not executed, before his hand:**  bwrap 0.11.1 lists
  both flags (`--help`, checked), but a session cannot nest
  bubblewrap — `No permissions to create a new namespace` — so the
  mount has never been made.  `test/test_sandbox.py::test_the_sessions_
  memory_directory_is_an_empty_read_only_mount` is written and
  **skips** from inside, which is the state to fix from the person's
  seat.  **The safe order is `tools/sandbox.sh --check` on the tree's
  copy first** — `--check` builds the namespace with these exact
  flags, so a bwrap that rejects them fails there, loudly, while the
  installed fence is still the old one — and only then `sudo
  tend-install`.  Doing it the other way round would put an untried
  mount in front of every command in every session.

  **The costs, paid:** the probe that asserted `~/.claude` *does not
  exist* is now two — *is read-only* and *holds nothing* — which is
  the same secrecy said twice as precisely; and it is a restraint, so
  nothing changes until his line.

What would kill each: (a) is dead if the false positives bite — a
command may *name* `~/.claude` for good reasons (this card's own
commit message does; `git grep`, the fence's own tests, and
`tools/fence.sh` all read that path), so the rule must key on the
write and not the string, and if that cannot be done cleanly in a hook
it is the wrong shape.  (b) is dead if nothing can see the failure
without wrapping every command — and the measurement above nearly
kills it already: a silent success is not a failure anything can
watch for.  (c) is dead if the Write tool already is that path — which
it is, which is why (c) is last.  (d) is dead if bwrap will not hold a
read-only directory there, or if something a session legitimately
needs turns out to live under `~/.claude` inside the fence; nothing
does today, because the fence hides the whole directory and has since
it was built.

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

**Where this leaves the card — a verdict, and the move is Henri's.**
(d) is built, installed and measured; the `because` no longer stands.
A write into the fenced home at `~/.claude` cannot vanish, because it
cannot happen: the kernel refuses it in every shell, and the error
names itself.  (a), (b) and (c) are refused by that and the reasons
are worth keeping — **(a)** a hook parsing shell text now has nothing
left to catch, and would have been a heuristic standing where a
boundary is; **(b)** a watcher for silent losses is unnecessary when
there are no silent losses; **(c)** a supported write path is the
Write tool, which already exists and now has an unmistakable signpost
pointing at it.  The day-one rate measurement is not needed to decide
this and is not run: the fix cost one line and has no false positives,
so counting how often the defect fired would only have priced a
decision already made.  **What is not closed**, and belongs to
whatever card wants it: the same silent-evaporation shape exists for
any other path under the tmpfs home, and nothing here says a session
would notice.  No path there has a caller today.

*Recommended for `done/`; the move is his, as every close here is.*

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

*Corrected 2026-08-31, by the measurement above, before anyone acted
on it*: **counting faces in the kaizens would have been an unsound
falsifier**, and the card said to grep the ledger for the right reason
without knowing it.  A face becomes a kaizen only when it is *noticed*,
and a silent success is not noticed by anyone — so the four faces are
the loud ones, and the quiet ones leave no trace in `doc/kaizen/` at
all.  The ledger is sound because it records the command that was run,
not the outcome that was seen: `~/.local/state/tend/leash.log`, grepped
for a `~/.claude` or `$HOME/.claude` path in a write position.  This
is the same failure the card exists to fix, one level up — an
instrument that can only see the errors somebody happened to notice —
and it is worth having caught it in the falsifier rather than in the
result.

## Where it sits

Placed last by the session that wrote it, 2026-08-31, at Henri's "you
can open the card for the ~/.claude check"; a new card arrives
unplaced and the tiebreak is his.  It is the first card in this tree
opened *by an ingestion* — `card:kaizen-ingestion.md` read the pile,
found the strand at its fourth face, refused to build a mechanism from
a ledger line, and named what a card would be for; this is that card,
which is the reflective organ that card exists to be, working once,
end to end.
