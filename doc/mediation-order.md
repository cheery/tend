# mediation-order.md — the two cheap measurements, taken

*The evidence `card:work-environment-ai.md` §"What would decide it"
asked for, gathered 2026-08-24 by a session.  The counts are checked
against the files they cite; the reading of them is a session's and by
the elaboration rule it is suspected.  The decision stays Henri's — the
card says the order is settled by measurement, and this page is the
measurement, not the settlement.*

## 1. The incidents, counted, both kinds

Read for: incidents where the *machine or the person* was measurably
hurt, attributed to a principal.  Gestate's `fixme.md` is a defect
ledger for the code and its ~175 entries are neither kind — a compiler
bug hurts the program's output, not the machine it runs on — so they are
excluded, and that exclusion is most of the reading.

**Session-shaped, measured: 2.**

* **2026-08-18, the machine was degraded while being listened on.**
  A full fenced suite, `cargo`, two X servers and twelve accumulated
  polling shells — the audio tore, and it was diagnosed as hardware
  first.  Caught by the underrun counter, once, by luck; the polling
  shells were themselves a session's bug (`pgrep` matching its own
  watcher).  `~/gestate/journal/2026-08.md` §"And what a session costs
  the machine", `~/gestate/board/unseen-flare.md` §"Seen once".
* **270 commits in nine days outrunning review** — the person's
  attention, which is the resource `vision.md` says no project may
  consume.  `~/gestate/spec/author.md`, measured there.

**Program-shaped, measured: 0.**

**The caveat, which is half the measurement, cuts two ways here:**

* For *audio-shaped* harm the zero is partially real: the underrun
  counter in `host.c` watches the machine, not the caller — a gestate
  node taking the machine would have flared it exactly as the suite run
  did.  An observer existed and stayed quiet.
* For everything else a program could do — files, network, a quiet
  hang — gestate has no observer at all, so that part of the zero is a
  fact about the instruments and decides nothing.

**What it settles: the order.**  Both measured incidents are
session-shaped, and they are precisely the card's two callers ("the
machine is shared", "you cannot see what happened").  Containment stays
outside this count on Henri's correction — it is blast-radius
limitation, and rare-event counting arrives too late for it by
construction.

## 2. The grant vocabulary, tried on the session's needs, on paper

**The grants a real gestate node wants** (an instrument, the card's own
example): *audio-out; its own state file; read access to its own
bundle.*  Three grants, all nouns, all static — the node's list can be
written once in the node.

**The grants the session of 2026-08-18 actually used**, from the ledger
of that morning: *spawn `pytest` under an interpreter; spawn `cargo`,
which itself spawns arbitrary build scripts; spawn two X servers; spawn
polling shells that re-spawn; read and write the whole tree; run `git`;
ring the sound card; and a wall-clock/CPU footprint spanning all of it.*

**The node vocabulary cannot spell the session's list.**  It has no way
to say *spawn, with the budget inherited by the children* — and that is
not one missing verb but the session's whole shape: every item on the
session's list is an `exec` of something that execs further, where the
node's list is three static handles.  A broker whose vocabulary is
grown from nodes meets sessions as a redo, which is what the card's
*Against programs-first* column predicted; a vocabulary that can say
*exec with inherited budget* covers the node's three nouns as a
degenerate case (a node is an exec that execs nothing).

## 3. What followed on the day, and what would revert it

The day-one slice is built for the session principal: `tools/leash.sh`,
a supervised, budgeted runner — wall-clock kill, CPU quota by cgroup
where a systemd user manager runs, and a plain ledger at
`~/.local/state/tend/leash.log` that is the observer measurement 1
found missing.  Per `~/gestate/doc/memory/decisions-arrive-shaped.md`
this is an experiment, not a decision: the keep-or-revert question is
whether it catches the 2026-08-18 case — a suite run under the leash
while the machine plays audio should leave the underrun counter quiet
where the unleashed run made it flare.  That comparison was run the
same afternoon and could not be scored — no load made the card run dry;
`doc/experiments/2026-08-24-flare.md` has the table.  The leash is
tolerated, not owned, on the criterion Henri set instead: how far would
it reach.
