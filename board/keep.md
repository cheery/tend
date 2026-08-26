# keep — a person's data sits in the open to whatever runs here

    status   open
    because  nothing on this machine scopes what a program or a session
             may read; the fence bounds reach by directory, but the
             directory is the person's whole tree, their state and the
             tree next door, and inside it everything is ambient — a
             program tend runs gets whatever the session that launched
             it can reach, having been handed nothing.  "How are users'
             data protected from programs?" (spec/os.md), and Henri,
             widening it: "by anything really" — a session, another
             program, the environment itself.  And `vision.md` asks the
             hard half: the person must still read their data as plain
             files, so the boundary cannot be encryption alone — it must
             let the person in while keeping the program out
    asked    Henri, 2026-08-25 — "create the card for 'how are users'
             data protected from programs?', or well, by anything
             really"
    see      spec/os.md — open problems 1 and 2 ("how are users' data
             protected from programs?", "how are programs protected and
             installed?"); the `because`
             card:work-environment-ai.md §"The architecture" 3 and
             §"Answers to the original open problems" 1 — the capability
             broker and powerbox, which that card calls *not an open
             problem but the first architecture decision*; the suspected
             fix this card must not adopt on its say-so
             card:fence.md, card:grant.md — reach and budget are bounded
             already, but coarsely: by directory and by cgroup, not by
             what data a program was given
             card:pull.md (done/) — the first program reaches only its
             own state file, because it was written to; nothing stops it
             reaching the rest.  The smallest instance of the property
             this card wants made general and enforced
             vision.md — "won't trap your work — plain files you can
             read without it"; the tension the boundary must hold

## What it is

Ambient authority.  Every process here runs with the full reach of
whoever launched it: a session reads any file it can reach, and a
program the session starts inherits that reach whole.  Nothing asks
*what was this given?* — the answer is always *everything in the
directories the fence left open*.  The capability model the architecture
sketches (a node gets a handle only by explicit grant; the picker click
*is* the grant) is the opposite stance, and tend has none of it.

## Measured, 2026-08-25, from inside the fence

A process here — a "program", though today it is the session's own
shell — reading files it was never handed:

| it was never given… | can it read it? |
|---|---|
| the leash ledger, another mechanism's private log | **yes** |
| another sitting's gestate state | **yes** |
| any file in the whole tend tree | **yes** |
| the tree next door (`~/gestate`, read-only but readable) | **yes** |
| `~/.ssh`, `~/.bashrc` | no — the fence's empty home |

So the fence's win is real and **directory-coarse**: it removes the home
and the secrets that live there, and inside every directory it leaves
open, nothing is scoped.  The person's data that lives in an open
directory — the state, the ledgers, the trees — is readable by any
program that runs, in full, ambiently.  That is the problem, and it is
one bind below the fence, not beside it: the fence says *which
directories*, and this card asks *within them, what was this program
actually given*.

## The tension that makes it hard

`vision.md`: *plain files you can read without it.*  The obvious answer
to "protect data from programs" is to make the data unreadable —
encryption, a private store — but then the person cannot read it either,
and the vision's promise breaks.  So the boundary is not secrecy; it is
**authority**: the same plain file, readable by the person by default
and by a program only if the program was handed it.  That is the
powerbox's shape and the reason the fix is a grant model and not a
vault.  It is also why this is hard: the enforcement is on the
program's reach, not on the bytes.

## What would make this card wrong

If no program tend ever runs touches the person's data — if the node
and its successors only ever read what they wrote — then ambient read
authority is a hole nothing falls into, and the fence's directory
grain is enough.  But `pull`'s node already reads and writes under a
shared state directory beside the leash's ledger and the sitting clock,
and the next node will want to read another's output; the moment two
nodes share a directory, "it can read anything in it" is a program
reading another program's data, which is exactly problem 1.  The
measurement above is that moment already arrived for the session.

## What it must not become

The whole capability broker, built in one card.  `work-environment-ai`
marks the powerbox *suspected*, and the manifesto forbids adopting a
practice on another design's say-so.  This card names the problem and
owes the first small enforcement that proves the grain finer than a
directory — one program that can read only what it was handed, and is
shown, from inside the fence, unable to read the file beside it.  The
broker, the picker, the handle types are downstream cards.  A card that
tries to answer problems 1 and 2 and the language at once is the OS
phase wearing a small name, the same failure `pull` was held back from.

## Where it sits

Placed at 2 by a session, below `work-environment-ai` and above the
count-only cards, because that card calls this its *first architecture
decision* and *everything else is downstream of it* — so by its own
words this ranks above the restraints already built and observed.  The
placing is the session's; the tiebreak is Henri's, and this is his to
move.

## 2026-08-25, afternoon — the first enforcement, built: a program blind to the file beside it

Henri, on the cost/benefit of the two shapes: *"go with A"* — the
reusable launcher, the grant outside the program, not the program
confining itself (Rule 1, kept: a party may not bound itself).

**Measured first**, from inside the fence: Landlock is available at
**ABI 4**, unprivileged, no build — a process can scope its own
filesystem reads through the raw syscalls.  The header's earlier guess
that a scope "cannot be made in bwrap's namespaces" was about `bus`; the
filesystem is a different LSM and needs no namespace at all.  *One side
finding, its own line, not this card's:* a raw `bwrap` and `unshare
--user` did nest from inside the fence, which contradicts
`tools/sandbox.sh`'s "cannot nest" comment — the sandbox still refuses
by policy, so nothing is weaker, but that comment wants verifying.

**Built**: `tools/keep.py` — `keep [--allow PATH]... -- program args`.
It governs filesystem *reads*, grants read on the handed paths plus the
system roots any program needs to run, `restrict_self` (one-way, so the
program cannot widen what it was given), then execs.  The demonstration
the card owed, run and tested:

    keep --allow $D/mine -- sh -c 'cat $D/mine; cat $D/beside; cat board/README.md; cat leash.log'
    mine        → granted
    beside      → Permission denied   (same directory, not handed over)
    the tree    → Permission denied
    the ledger  → Permission denied

`test/test_keep.py` holds it: the neighbour, the tree and the ledger are
all blind; a granted directory reads beneath; a system program still
runs.  That is problem 1 enforced for the first time — a program reads
only what it was handed.

**What the build taught, named:**

* **The runtime is a grant like any other.**  The first "still runs"
  test used the *venv* python, and it failed: the confined interpreter
  could not read its own `pyvenv.cfg` in the tree.  Correct, not a bug —
  to run a program you hand it its runtime too.  System programs need
  only the roots; a venv is handed with `--allow .venv`.  The node
  retrofit will hand the node its own directory and interpreter, no more.
* **keep refuses rather than run unconfined.**  If Landlock is absent it
  does not exec the program — a grant that silently became "everything"
  is the one lie it must not tell (Rule 9).
* **Reads only, for now.**  Write and network are Landlock bits this
  does not set yet; a program under keep can still *write* where the
  fence allows.  The card's problem is reading data it was not given,
  and that is closed; write-scoping is a later turn, named so the gap is
  not silent.

**What stays open on the card**: keep exists and binds nothing until a
caller runs a program through it — the leash's shape before the hook
wrapped it.  The next step is the one the cost/benefit named: the pull
node *run through* keep (`keep --allow <the node's dir> -- node.py`), so
the real program gains the boundary, the grant still outside it.  That,
and write-scoping, are what remain before this problem is more than
demonstrated.

## 2026-08-26 — the launch path: the node runs confined by default

The card's last open half, and the one Henri pointed at.  `node/run.sh`:
the node's grant baked in — `--allow node.py` (code, read) and `--write
<state dir>` (write-scoping's first caller) — run through keep, the
boundary outside the program.  Running the node is now running it
confined; the incantation is gone.

    node/run.sh run          # opens, serves pulls, stops — blind to the tree
    node/run.sh status

**The state directory is separate from the code, on purpose**: were it
the code's own directory, "writable state" would mean "rewritable code".
So the node may change its state and nothing else — not `node.py`, not
the tree, not the ledger beside it.  A system python, not the venv (the
runtime is a grant; a venv interpreter is blind to its own `pyvenv.cfg`
inside).

**What the launcher can be gated for, and what it cannot** (measured,
`board/green.md`): dropping `--allow node.py` is red — the node cannot
read its own code and the run fails.  But **dropping `--write`, or keep
itself, is invisible through the node** — a well-behaved program that
writes only its own state behaves the same confined or not; confinement
shows only on *overreach*, which the node never makes.  So the write
boundary the launcher sets is real (an out-of-bounds write is denied)
and is gated where it *can* be — at keep, `test_write_is_scoped_when_asked`
— not through the node.  A confinement launcher for a well-behaved
program is the honest limit named, not hidden.

**What stays open**: this wires *the node's* launch, one program by its
own script.  A general "any program tend launches runs under keep by
default" would be the fence-hook's territory (it wraps shell commands)
and is not built — the tree runs one program, and one launcher is what
one program needs (manifesto rule 1).  Network is still the other unset
Landlock bit.

## 2026-08-26 — write-scoping, built: the boundary keep did not set

The card's named-open half, and the one Henri pointed at ("keep would
be cool").  `tools/keep.py` gains `--write PATH`: it grants read+write
beneath a path and turns on the write boundary, while `--allow` stays
read-only.  With at least one `--write`, a program may change only what
it was handed writable and is refused everywhere else — **including a
path it can read**.

    keep --write $D/wr --allow $D/ro -- sh -c 'echo hi > $D/wr/new; echo no > $D/ro/blocked'
    wr/new      → written
    ro/blocked  → Permission denied   (readable, not writable)

`test/test_keep.py::test_write_is_scoped_when_asked` holds it, and
`test_without_write_the_boundary_is_not_set` holds the default.

**Opt-in, and the default is stated not silent.**  With no `--write`,
keep governs reads only and a program writes where the fence allows —
which is what six days of the card said it did, and what the existing
node grant relies on, so nothing already built changed.  The write
boundary exists the moment a caller asks for it and not before; Rule 9
is about reads never silently becoming "everything", and reads are
always confined.

**What the build had to get right:**

* **The handled set follows the ABI.**  Landlock refuses a whole
  ruleset that names a bit the kernel does not know, so `TRUNCATE` (ABI
  3) is added only when `landlock_abi()` reports ≥ 3; the rest are ABI 1.
  A `restrict_self` that failed here would be the silent-everything lie
  by another door.
* **A rule may never grant past what is handled** — `allowed &= handled`
  — so a read-only grant cannot leak a write bit through a copy-paste.
* **Broken before trusted** (`board/green.md`): with `write_bits = 0`
  the writable dir collapses to read-only and the write into the
  read-only grant goes through — `test_write_is_scoped_when_asked` red.

**Still open on the card**, unchanged: nothing yet *makes* a program run
under keep — the fence-hook wraps shell commands, not program launches
— so wiring keep into the launch path (confined by default, not by
remembering the incantation) is the step this does not take.  Network
is the other unset Landlock bit.  Both named; neither silent.

## 2026-08-25, later — the next slice: the pull node runs through keep

Henri: *"do the next slice."*  The first real program now gains the
boundary, the grant still outside it:

    keep --allow node --allow <statedir> -- /usr/bin/python3 node/node.py --state <statedir>/n.state run

Handed its own code (`node/`) and a state directory and nothing else,
the node opens, runs and stops itself — and writes its state, because
keep governs *reads* and the fence allows the write.  From that same
grant, `cat board/README.md` and the leash ledger are both *Lupa evätty*.
`test_keep.py::test_the_pull_node_runs_confined_under_keep` holds it.

**The node itself did not change** — 86 lines, no ctypes, no vocabulary.
The boundary is composed around it the way the leash and the fence are
(`leash → sandbox → keep → program`), which is the whole reason shape A
was chosen: the program cannot bound itself, so something outside it
does.  The state-directory exposure the card named — the node beside the
ledger and the sitting clock — is closed for the node that asks to be
run this way.

**What is still open**, narrowed: keep governs reads, so a confined
program can still *write* where the fence allows — write-scoping is the
next Landlock bit, for when a caller needs it.  And nothing yet *makes*
the node run under keep — the fence-hook wraps shell commands, not
program launches; wiring keep into the launch path (so a program is
confined by default, not by remembering the incantation) is the step
after write-scoping.  Both are named; neither is silent.

## 2026-08-26, 13:09 — network, the last unset bit: `--no-net`, and the node its first caller

Henri: *"do keep's slices."*  Read back, the card had one slice left
that was not held back by rule 1 — write-scoping and the node's launch
path were both built earlier this day (the two sections above), and
"any program confined by default" is explicitly the fence-hook's
territory and not owed here.  What stayed named twice as open was
**network, the other unset Landlock bit**.

**Measured first**, raw from this seat, before any design: a ruleset
handling `NET_BIND_TCP | NET_CONNECT_TCP` (ABI 4) with no port rule
refuses `connect` to a loopback listener with EACCES, refuses `bind` on
a named port *and on port 0*, and leaves a UNIX-socket bind untouched.
So "handle both bits, grant nothing" is exactly "no TCP at all", which
is the bound a program that needs no network should carry.

**Built**: `tools/keep.py --no-net`.  Opt-in, on the write slice's
shape: with it, the program can neither connect nor bind a TCP socket;
without it, a program has whatever network the fence left it, and the
default is stated in the docstring, not silent.  Asked for on a kernel
below ABI 4, keep refuses rather than run the program with the network
it was told to lose — Rule 9 by the same door as the missing-Landlock
refusal.  The v4 ruleset struct (16 bytes) is used only when the flag
asks, so an older kernel never sees a size it would reject.

    keep --allow /tmp          -- python3 -c '<connect 127.0.0.1:port>'   → connected
    keep --allow /tmp --no-net -- python3 -c '<connect 127.0.0.1:port>'   → Permission denied

**The node is the first caller.**  `node/run.sh` now passes `--no-net`:
the node is a tally of pulls through a file, uses no socket, and has no
business reaching out.  Its grant reads, in full: its own code readable,
its state directory writable, no network.  It opens, serves, stops as
before — a well-behaved program shows nothing of its confinement, which
`board/green.md` already named as the launcher's honest limit; so the
boundary is gated at keep, and the launcher is gated for *asking*.

**Held**: `test_keep.py::test_no_net_refuses_tcp_when_asked` (connect
refused, bind refused, UNIX still binds; skips out loud if loopback is
unreachable from the seat, and below ABI 4), `…without_no_net_the_network_is_not_touched`
(the default), `…the_node_launcher_asks_for_no_net`.  **Broken before
trusted**, on a scratch clone and never the tree: net bits zeroed →
`connected`, red; the flag parsed but not handed to `confine()` →
`connected`, red; the launcher's line dropped → red.  Three mutations,
three catches.

**What stays open on the card**, narrowed again: per-port grants
(`LANDLOCK_RULE_NET_PORT`) are the turn after this, for the first
program that needs a port — none does.  UDP and UNIX sockets are outside
what Landlock can say, so outside what keep can promise; named so the
word "no-net" is not read wider than it is.  The general launch path is
still the fence-hook's, still not this card's.  With reads, writes and
TCP all scoped and a real program carrying all three, the card's
`because` — a program gets whatever the launching session could reach,
having been handed nothing — no longer describes the node.  Whether it
still describes *the session* is `work-environment-ai`'s question, and
whether this card is done is Henri's.

*Henri, 2026-08-26 13:17: "it stays open for the session half."  So the
card's `because` is closed for the node and open for the session, and
that is the half it now names.*

## 2026-08-26, 13:50 — the session half, first slice: the state row is two directories, not their parent

Henri: *"you could work on the keep and resolver."*  The card's
`because` for the session: a session reads everything in every
directory the fence leaves open, having been handed nothing.
`work-environment-ai` said on 08-25 what the first build would be —
"not a vocabulary but one bind — the state directory."  Measured today
from inside the fence, that bind is `~/.local/state` whole, and under
it a session can read, unhanded: **another assistant's prompt history**
(`opencode/prompt-history.jsonl`, 7.9 KB, opened from the fence), `gh`,
the sound server's routes, `Dart`, `claude/locks`.  What tend's own
mechanisms read there is two directories: `tend/` (the leash ledger,
the kaizen want) and `gestate/` (the sitting limit's `sittings.log`).

**Handed to Henri as `state-row.patch`** — `sandbox.sh` is protected:
the `state` row binds `~/.local/state/tend` and `~/.local/state/gestate`
and not the parent, the row's text says so and why, and the patch
carries its own test (`test_the_state_row_is_two_directories_not_their_parent`,
red until applied).  The probe test that wrote at the parent now writes
under `tend/`, which holds before and after.  Verified on a scratch
copy: `--rows` reads as intended, 9 pass; `sh -n` clean.  Not run under
bwrap from here — that is his unfenced run, as every fence change is.

**What this is**: the session's grant narrowed by one row, in the
fence's own grain, from what the row's purpose actually reads.  **What
it is not**: keep applied to the session.  Inside the tree a session
still reads every file; inside `gestate/` it reads the other tree's
whole state.  Those are the rows the next measurement should read the
same way — by what the purpose reads, not by directory — and the tree
row is the hard one, because the tree *is* what the session works on.
