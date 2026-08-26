# keep — a person's data sits in the open to whatever runs here

    status   done — 2026-08-26
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

**Henri's unfenced run, 14:0x — the fence was down, and the patch was
the reason.**  `--check` said `✗ ~/.local/state does NOT pass through`:
its probe writes at the *parent*, which the patch had just unbound,
while the test I moved under `tend/` passed.  The same miss twice in
one patch — one moved, one not — and exactly what "verified by logic,
not execution" meant in the 13:56 kaizen.  `state-row-2.patch` moves
the check's probe under `tend/` and adds the probe the row now needs:
one written at the parent inside must *not* be there outside.  Two
probes, the row's two halves.

## 2026-08-26, 14:10 — the session half, second slice: the `trees` row is the other tree's documents and tools

Henri: *"do the trees row."*  The row bound `~/gestate` whole,
read-only.  **Measured by purpose**, the way the state row was: the
ledger has 11 records reaching gestate since 08-25, and what they
opened is `board/`, `tools/`, `fixme.md`, `vision.md`, and twice
`.claude/settings.json` — a session comparing the twin fences.  What
the cards cite adds `spec/`, `doc/memory/`, `journal/`, `manifesto.md`.
The audit script, the row's named purpose, reads only the tree it is
pointed at.  **What nothing ever opened**: `target/` and `shell/` — 3.2
GB of builds — the source (`gestate/`, `crust/`), `test/`, `examples/`,
`.git` with the other tree's whole history, `.claude/worktrees`.

**Handed to Henri as `trees-row.patch`**: the row binds the parts —
board, tools, spec, doc, journal, the root documents, and
`.claude/settings.json` as a mechanism's config — and inside,
`~/gestate` holds those and nothing else.  This time the 14:05 rule was
run first: every line naming the path was listed before the patch, and
the check's probe was *moved* (`tools/.probe`, still blocked) *and* the
row's other half added — `.git` and the source are not inside, expected
blocked.  The patch carries its test (`--rows` names the parts, not the
tree).  `sh -n` clean, non-bwrap tests green on a scratch copy; the
bwrap run is his.

**What this is**: the second row narrowed from what the purpose reads.
**What it is not**: a judgement about gestate — its source is not
secret; it is 3 GB and a history a tend session has never needed, and a
reach nobody needs is a reach nobody should carry.  The tree row — this
tree, read-write, whole — is what remains, and it is the one where
"what the purpose reads" is "everything," because the purpose is the
work.  That is the hard one, still unbegun.

## 2026-08-26, 14:35 — the tree row, measured by what the purpose writes

Henri: *"do the tree row measurement."*  The 14:12 kaizen said the tree
row cannot be read the way the other two were — "what does the purpose
read" answers *everything*, because the purpose is the work — and
proposed the other question.  Measured, two halves.

**The committed half** — `git log --name-only`, 120 commits since
08-24, 117 carrying a session trailer, 3 a person's alone:

    board/ 102   doc/ 80   test/ 55   tools/ 51   .claude/ 8   node/ 5   spec/ 4
    root: .gitignore 5, vision.md 5, README.md, CLAUDE.md

Every file in the tree has been committed by a session-marked commit —
*which is not the same as written by a session.*  `.claude/settings.json`
is in eight such commits and the ledger has **zero** fenced writes to
it: every one was Henri's hand (the installer, his `jq` edit,
`--protect`) and a session's commit message.  The protected set the
same: sessions' commits touch every file in it; since 08-25 14:04 the
fence refuses the write (`touch tools/sandbox.sh` → EROFS, measured
today) and the path is a patch.  `spec/` was last written 08-25 06:39,
`vision.md` 08-24 17:54 — the documents were written at the tree's
start and read since.

**The runtime half** — the ledger's 310 commands, their `>`/`sed -i`/
`rm`/`mv`/`cp`/`mkdir` targets, heredoc bodies dropped: `board/` 60,
`doc/` 27, `tools/` 25, `test/` 12, `node/` 4, the root (`.gitignore`,
`CLAUDE.md`, the patches for Henri's hand).  **Never a write target**:
`.venv` (0 — pip has not run fenced), `node/state` (0 — the node writes
it, the session only through the node), `.claude` (0).  And `.git`:
zero targets by name, and written by every one of 117 commits — the
fence leaves it whole, and must, since a session's commit is a write to
it; `card:fence.md` already says the boundary for `.git/` is none by
category.  *A limit of this measurement, named*: the ledger cannot
tell `sed -i tools/fence.sh` in the tree from the same line run inside
a scratch copy after `cd`; the 50 apparent protected-set targets since
08-25 are the mutation harness and patch-building on copies, and the
fence's refusal is what says none landed.

**What the tree row is, by purpose.**  Written by the work: `board/`,
`doc/`, `test/`, the unprotected half of `tools/` and `node/`, the root
documents, `.git`.  Written by a hand and read by the session:
`.claude/`, the protected set — already read-only.  **Writable and
never written by the session**: `.venv`, and `node/state`.  Those two
are what the row can give up on the write side without touching the
work — `.venv` read-only is a bind with no caller against it, and
`node/state` read-only to the session is the sharper one, because it is
a *program's* directory: the session's one legitimate write there is
the pull line.  But a session's pull today starts the runner *inside
its own fence*, and a runner needs the state writable — so `node/state`
read-only to the session is not a bind; it is the resolver moved
outside the session's write access, which `card:resolver.md` named on
day one and did not build.  That is the tree row's finding: **the only
write the session makes that is not the work is the node's, and closing
it is the resolver's shape, not the fence's.**

**What stays**: `.venv` read-only, a patch when Henri wants it — small,
and it should wait for the resolver decision so the two rows land as
one.  The rest of the tree row is the work, and the work is what the
session is for.

*2026-08-26, 14:40 — the resolver outside the fence is built
(`card:resolver.md`), which is the shape the tree-row measurement said
closes the session's one non-work write.  Once Henri installs the hook,
the remaining bind — `node/state` read-only to the session, the pull
file writable — is this card's last slice, and it lands with `.venv`
read-only as one row.*

## 2026-08-26, 15:30 — the last bind: `node/state` read-only to the session, the pull file its one write; `.venv` read-only

Henri: *"do the last bind."*  The tree-row measurement (14:35) found
the session's one write that is not the work: the node's state, which
the session never wrote by name in 310 commands and the node writes
for it.  Since 15:03 the node is written from the person's side — the
resolver's runner — so the session no longer needs the directory
writable at all.  Its one legitimate write there is the pull line.

**Measured first**: a run of three test files wrote nothing under
`.venv`; `node/state` holds six runtime files, all the runner's or the
resolver's but the pull file.  The 14:05 rule: four lines name the two
paths — `PATH` (a read), the resolver's default, two `.gitignore`
entries — none changed by the bind.

**Handed to Henri as `last-bind.patch`** (`sandbox.sh` is protected):
after the protected set, `node/state` is bound read-only and
`node.state.pull` alone bound writable over it; `.venv` read-only when
present; the state directory and the pull file are created on the
person's side before the fence if absent, so the first pull ever can
land.  Three probes join `--check`: `node/state is read-only`, `the
pull file passes through` (`: >>`, an open for append that writes
nothing), `.venv is read-only`.  The `tree` row's text names what it
holds back.  Tests in the patch: the row's words (no bwrap), and inside
(bwrap, his run): a touch under `node/state` refused, the pull file
appendable, the runner's lock **not** openable, `.venv` refused.  No
key — the protected set is unchanged.

**What this closes.**  A session inside the fence can pull and read
the node, and cannot run it: `run.sh run` fails at the lock, and a raw
`node.py run` fails at its own lock and its state.  With the resolver
outside, the pull path is the only path, and it applies the grant.
That is the session half of this card's `because` for the one program
tend runs — *a program gets whatever the session that launched it
could reach* — closed by there being no launching session.

**What stays open**, and it is the card's last sentence: inside the
tree the session still reads and writes the work, whole, because the
work is what a session is for; and `gestate/`'s parts are read whole.
Neither is a debt.  Whether the card is done is Henri's.

**15:37 — landed, and shown from a session's seat.**  Henri: "applied
last-bind, the fence is up, suite green, committed."  From inside the
fence, the same minute: `touch node/state/.x` → *read-only file
system*; `touch .venv/.x` → the same; a raw `node.py run` → `OSError:
Read-only file system: node.state.lock`; `run.sh run` → `cannot create
run.lock`; `run.sh pull` → "pull recorded — the runner is the
resolver's to start."  Next command: `gen 3 opened at 15:37:05 · served
1, total 4`.  A session pulled, could not run, and was served from the
person's side.  The card's `because` — a program gets whatever the
session that launched it could reach — has no launching session left
to describe.  *Done for the one program, from every seat; whether the
card is done is Henri's.*

## 2026-08-26, 15:50 — a port, granted: `--bind PORT`, for the second node

The per-port turn had waited for a caller; `card:work-environment-ai.md`
15:45 named one — `llama-server` as tend's second node, whose whole
reach is one listening port.  Built while Henri installs the binary:
`keep --bind PORT` turns on the TCP boundary and adds one
`LANDLOCK_RULE_NET_PORT` rule for bind on that port.  Measured raw:
the granted port binds, any other port is EACCES, every connect is
EACCES.  `test_bind_grants_one_port_and_nothing_else`; three rows —
no rule added, connect granted instead of bind, the network left
unhandled — each red by name.  Not built: `--connect PORT`, which has
no caller; and per-host, which Landlock cannot say.

## 2026-08-26, 16:20 — the grant beside the program: one launcher, one resolver, one fence rule for any node

Henri: *"do the grant beside the program."*  The second node's day one
(15:50–16:05) measured that a server's whole grant is three lines, the
same shape as the node's three flags — so the grant became a file
beside each program and the launcher, the resolver and the fence became
node-agnostic.

**`NODE/grant`** — `allow`/`write`/`bind`/`no-net`/`idle`/`pulse`/
`pull`/`program`/`status`, one word and value per line, paths relative
to the node.  `node/grant` is `run.sh`'s three flags; `llm/grant` is
the day-one measurement (model read, state write, one port, the server
log as pulse).

**Built in the tree** (unprotected): `tools/launch.sh NODE run|pull|
status|serve|grant` reads the grant, builds keep's flags, holds the
lock, runs the program — and for a program that cannot stop itself
(`pulse FILE`) watches that file's mtime and stops it on idle.  `serve`
is the resolver's per-node decision as an **mtime rule** — a pull
newer than the last stop, no runner up — which holds for any program,
a server having no tally.  Both nodes run through it live: the node
stops on idle, `llama-server` answers over loopback and is stopped when
its log goes quiet.  Fourteen tests, four rows red by name.

**Handed to Henri as `grant-beside.patch`** (`sandbox.sh`, `resolve.sh`,
`node/run.sh` are protected; the test rides in the patch): `resolve.sh`
loops over `*/grant` calling `launch.sh NODE serve`, naming no node;
`sandbox.sh` binds every node's state read-only and its pull file
writable, and adds `tools/launch.sh` to the protected set (it applies
every grant); `node/run.sh` becomes a wrapper over the launcher, one
code path.  After `git apply`, **`tools/fence.sh --protect`** adds the
launcher's `Edit` rule (the key — a `sandbox.sh` patch that touches
`protected=` always carries it), then `--check`, suite, commit.

**What this closes on the card**: the session half was closed for the
one program; it is now closed for *any* node beside a grant, by one
mechanism, and adding a node is adding a directory.  `keep`'s `because`
is answered at the grain it asked for — what was this program given —
for every program tend runs.  Whether the card is done is Henri's.

## done — 2026-08-26

Henri: *"examine the keep & resolver, and consider whether the
conditions are satisfied for these cards.  If they are, move them to
done."*  The `because` — *nothing scopes what a program may read; a
program gets whatever the session that launched it could reach, having
been handed nothing* — no longer stands.  A program tend runs is
handed a grant (read `--allow`, write `--write`, network `--no-net`/
`--bind`), applied from outside it by one launcher from a file beside
it; it reads, writes and reaches only what the grant names, shown for
two programs (the node, `llama-server`).  The session's own ambient
reach, the `because`'s "by anything really", was narrowed to purpose
row by row — the home and secrets gone, other tools' state, gestate's
source/builds/`.git`, and every node's state closed — leaving readable
only the work tree and gestate's documents, named as the deliberate
exception (*the work is what a session is for*).  The one residual —
a session exec'ing an arbitrary program by hand, fence-bounded but not
keep-confined — is the session-as-principal question, owned by
`work-environment-ai` (§16:50) and `session-program`, not this card.
Moved to `done/` at Henri's judgement, delegated to the session.
