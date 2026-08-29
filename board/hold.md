# hold — a node that should be up is up only while something happens to pull it

    status   doing
    because  a node's liveness is an accident of pull traffic: the llm
             node stops 60 s after the last pull (`idle 60` in its grant)
             and pays 80 s reloading the model on the next one, and there
             is nowhere on the person's side to say "keep this alive" —
             a pull is a line that means "something wants this once",
             `serve` starts a runner only for a pull newer than the last
             stop, and a pin (card:canvas.md) is "show me" and nothing
             more (Henri, 2026-08-29: "what does it mean for something to
             be pinned right now?" — it means a row on the panel).  So a
             server on this tree is a node that gets lucky, and the
             crash-loop half of "may crash but not hang"
             (doc/os-status-2026-08-28.md item 9) has stayed owed because
             nothing yet restarts anything
    asked    Henri, 2026-08-29 — "we could have something of the same
             style [as .pin] that actually means that the node+state is
             being pulled and stays alive while there's a corresponding
             file for it, the file would mean that something pulls the
             node" … "Lets card it."
    see      card:canvas.md — the pin: the person's "I am holding this",
             on the person's side, read by the panel only; day two (the
             death notice, 2026-08-29) is what makes a restarted death
             visible
             card:resolver.md (done/) — `launch.sh NODE serve`, the
             per-node decision as an mtime rule (pull newer than stop);
             tools/resolve.sh visits every node the tree knows
             card:keep.md (done/) — the grant beside the program; the
             program writes its state and nothing else, which is why a
             hold cannot live in `$STATE`
             tools/launch.sh — `idle`, `sitting`, `pulse`: the three
             lifecycle words; "a node may end its sitting early and can
             never extend one"
             tools/sandbox.sh `state` row — `~/.local/state/tend` bound
             read-write to a fenced session for the andon and the clock;
             the canvas lives under it today
             card:silent-cord.md, card:sitting-everywhere.md — the
             same hole seen from two other sides: a grant on the person's
             side that a session can reach
             doc/os-status-2026-08-28.md item 9 — the crash-loop backoff
             + andon, owed

## What it is

Henri, 2026-08-29: *"the way the state network works... it's that
canvas may pull nodes, and nodes may pull other nodes.  If node's
process/processes is killed or node stops pulling with separate
command, the pull stops."*  **A pull lasts exactly as long as its
puller, and the canvas is the puller that does not die.**  Everything
alive is on a canvas: a node runs because a chain of pulls reaches it
from a canvas, and when the chain breaks — a puller dies, un-pulls, or
the person removes the hold — the pull stops and idle takes the node
as it does today.  Today's `pull` (append a line; idle counts from it)
is the degenerate case: a lease that expires after `idle` seconds
whatever the puller is doing, which is why the llm node goes cold
between `lead.sh`'s turns.

Two forms of one thing:

* **The canvas's pull is a file.**  `<name>.hold` in a canvas
  directory: presence is the pull, mtime is the person saying so again
  (`touch`), the content is the asked-by (a hold with no words is
  suspect), and `rm` is the act that lets the node stop.  A person has
  no process to die with, so a file stands in.  `.pin` stays "show me a
  row"; a hold is a different file because presence-and-mtime is the
  whole mechanism (Henri: "pin files should pin files, these files
  should be something else").
* **A node's pull is a lock.**  A puller takes a shared `flock` on a
  file in the pulled node's state (`$STATE/pulled`) and keeps the fd
  open while it wants the node; un-pull closes it; killed, the kernel
  closes it — the property `launch.sh` already leans on for
  `run.lock`, no pid tracking.  The pulled runner's question is one
  line: *is anyone pulling me?* — a hold exists, or an exclusive
  non-blocking `flock` on `pulled` fails.  Under keep the pull is a
  reach, named in the puller's grant beside its program (`pull OTHER`
  — read of the other's state file is enough; `flock` needs no
  write).  It does not cross machines, and not yet: the lease-with-a-
  heartbeat form (the `watch` rule the runner has for its own cords)
  waits for a second machine to ask.

**Canvases** are where chains start, and there are several by design:
a **system canvas** for what opens when the machine starts — never as
root; every system user with processes of its own has its own — and a
**user canvas** that opens when the person logs in.  "Opens" is the
resolver visiting the canvas's holds; which canvas a resolver reads is
a path, as the panel's is.  Both are shape, not build: day one is one
canvas on one desk.

Five boundaries the tree already has, agreed on 2026-08-29, each of
which the design keeps:

1. **A hold is a lifecycle grant, so it never extends a sitting.**
   `launch.sh`'s rule stands: a node may end its sitting early and can
   never extend one.  A pull means *restart it when it stops*, not
   *never stop it*: the sitting cuts, the resolver starts a fresh one,
   the gap is honest.
2. **The runner knows it is pulled, or idle fights the pull.**  The
   watch loop reads the hold's presence and the lock's state as the
   pulse — not idle while either holds — one test per tick in the loop
   that already ticks.  Without this a held llm node is a reload loop
   at 80 s a turn on the GPU.  (Henri: "not sure but it sounds right"
   — the first held run is its measurement.)
3. **A crash is not hammered.**  After a clean stop (the sitting),
   restart unconditionally; after a *death* (a non-zero exit, a line
   in the andon record since card:canvas.md day two), restart only if
   the hold is newer than the death — the person re-asserts with a
   `touch`, having seen why.  The same mtime comparison `serve` makes
   between the pull and `stopped`.  This is doc/os-status-2026-08-28.md
   item 9's crash-loop backoff in the tree's grammar; the andon half is
   the death notice.
4. **Cycles are forbidden, at the door.**  A pulls B pulls A with no
   canvas behind them is the bounded party setting its own boundary
   (Rule 1).  Because a node's pulls are lines in its grant, the pull
   graph is declared, and `launch.sh NODE check` refuses a grant whose
   pulls reach back to the node — before anything runs.  And by
   construction liveness enters only through a canvas: a node exists
   because something pulled it, and the first pull is a hold; remove
   the hold and the chain collapses from the root.  Henri: "the idea is
   that everything alive would be on a canvas."
5. **Whose hand.**  A hold lives where the program cannot write it —
   never `$STATE` — and, Henri: *"canvas should be in place where
   access must be granted separately if it's to be touched."*  Today
   the canvas is under `~/.local/state/tend`, which the fence binds
   read-write for the andon and the clock, so a fenced session could
   touch a hold and the tree could not tell its hand from his.  The
   canvas moves, or is bound apart, so that writing it is a reach row
   of its own, off by default.  Until that row exists the backstop is
   (1): a forged hold buys at most restart-after-sitting.

## What would make this card wrong

If pull traffic is in practice enough — if the nodes that matter are
pulled often enough that idle never bites and the 80 s reload is paid
once a day — then a hold is a dial nobody turns.  The llm node's own
afternoon on 2026-08-28 (three led turns, each a cold start) is the
evidence against.  Or if a "server canvas" never exists: one desk, one
node, and a hold is `sitting 600` in the grant by another name.  His
own ask (a server's canvas, card:canvas.md) is the evidence against
that; the day it is measured is the day a second machine holds a node.

## What it must not become

A way for a program to keep itself alive (the hold is never in
`$STATE`, and never read from anywhere the program can write).  A
sitting extension (rule 1 above).  A restart loop (rule 3).  A cycle (rule
4).  A second list for the resolver — it keeps its own list of nodes and honours the
holds it finds; "the resolver reads pins as its list" stays the
decision card:canvas.md marked it, and a hold makes it unnecessary.  A
process supervisor: no PID files of its own, no health checks, no
"desired state" beyond a file being there — the runner's `run.lock`,
`stopped` and `watch` are the state, as they are today.  And not
anything a session can create by default (rule 5).

## Day one

`<name>.hold` in the canvas directory, by Henri's hand (`printf 'held
by henri, the desk\n' > ~/.local/state/tend/canvas/llm.hold`).
`launch.sh NODE serve` starts a runner for a held node with no runner
up, subject to rule 3; `run` given the hold's path is not idle while
the file exists; the panel's row says `held` beside `running`.  Red
first: a fixture hold and a program that would idle out in 0.4 s stays
up past it and stops within a tick of the file's removal; a fixture
death with a hold older than it is not restarted, and one newer is.
The first measurement is his: the llm node held across an afternoon,
pulled cold once.  A node's pull as a lock is day two, when `lead.sh` is the first node
that wants to pull another; rule 5's separate reach row is day three, and is not
a build before day one has been held once — its shape is
card:silent-cord.md's, a row off by default with the sound on when it
is off.

## Day one landed — 2026-08-29, 13:20 sitting, at Henri's "do the hold"

Built in `tools/launch.sh`, `tools/panel.py`, and their tests;
red first — the five new tests run against HEAD's launcher and panel
before the change, and five failed.

* **The hold's path** is the panel's own resolution: `TEND_CANVAS`,
  else `~/.local/state/tend/canvas`, and `<name>.hold` in it, where
  `name` is the node directory's basename (the pin's, too).  Every test
  points `TEND_CANVAS` at scratch, so a test never reads the desk's
  holds — a fixture builds the side it means.
* **`run` (rule 2)**: the watch loop's idle test is `[ ! -e "$hold" ]
  && …` — one `stat` per tick in the loop that already ticks.  Measured:
  a `sleep 60` with a pulse that never moves, `TEND_IDLE=0.4`, held, is
  up 2.5 s later; the hold removed, it stops within a tick, `stopped`
  says `idle:`, exit 0.  The sitting check runs first and is untouched
  (rule 1).
* **`serve` (rule 3)**: a pull newer than the stop is served as before;
  else a hold is a standing pull — after no stop or a clean one (`idle:`,
  `sitting:`, `exited 0`) it starts a runner unconditionally; after a
  death (`exited N`, N≠0, the same line the death notice reads) only
  when the hold is newer than `stopped` — the same `-nt` the pull uses.
  Measured both ways with a fixture death at T, a hold at T−30 (nothing
  starts, `stopped` untouched, the lock free) and the hold touched to
  T+30 (started, stderr says "the hold is newer than its death").  The
  resolver needed no change: it already visits every grant and asks
  `serve`.
* **`status` says `held: <who> (<path>)`; `check` says `✓ held — …`.**
  The panel's row carries a `held` bit beside `running`/`not running`/
  `DEAD` (`Pin.held`, the hold's first line, `(no words)` for an empty
  one — a hold with no words is suspect and still a hold).  The panel
  reads it and never writes it.

Nothing runs it until his `sudo tools/install.sh` — `launch.sh` is in
the installed set and the tree's copy is the workbench.  **The first
measurement is his**: `printf 'held by henri, the desk\n' >
~/.local/state/tend/canvas/llm.hold`, the llm node held across an
afternoon, pulled cold once; and whether rule 2's one `stat` a tick is
enough to keep idle from fighting the pull ("not sure but it sounds
right").  Not built, by the card's own order: a node's pull as a lock
(day two, `lead.sh`), the cycle check at `check` (with day two's `pull
OTHER` lines), and the canvas's own reach row (day three).  One thing
the build noticed: a node that idles *itself* (the tally node, `--idle`
in its program line, no `pulse`) is out of rule 2's reach — held, it
stops on its own clock and the resolver restarts it at its next visit,
which is correct and is a restart per command; the llm node, which the
hold is for, has a pulse and is not that.

## Day one, second pass — the same sitting, at Henri's review

Henri held `node` (the llm node "is a bit heavy") and asked three things.

**"I'd like to name what I'm holding inside the file."**  Day one keyed
the hold on its filename — `<name>.hold` "beside the pin" taken as the
pin's *name* and not the pin's *shape*, which was an oversight, not a
decision: a hold means "node+state is being pulled", so the content
should say which, the filename should be a label, and two holds of one
node with different states should be possible.  Now a hold is
pin-shaped: `node NAME-OR-DIR`, `state DIR` (relative to the node), or
one bare line `llm "state"` — his own example — whose first word is a
node of this tree and the rest, quotes off, its state; every other
line is the words, who is holding it and why.  A hold with no `node`
line holds the node its filename names, so his `node.hold` ("held by
henri, the desk") reads as it did.  `launch.sh` finds its holds by
content (`holds_for`, a scan of the canvas — one per tick in `run`'s
loop, the canvas being a handful of files), and rule 3 measures a
death against the *newest* hold that names the node.  One asymmetry,
written where it lives: a hold with no state line is, to the launcher,
"whatever state I run with", and to the panel, the node's default
`node/state` — they differ only under `TEND_STATE_DIR`, the tests'
seat.  Found on the way: `check` clobbered `$root` in its own loop
(`for root in $sysread …`), so a bare node name resolved against the
wrong tree; renamed.

**"We could improve the andon-panel to show holds."**  A held node is
on the canvas whether or not it is pinned: `read_canvas` adds a row per
hold whose node and state no pin shows, named by the node directory
(the name the death notice uses), with the hold's words — `held — held
by henri, the desk`; the header counts `N on it, M held`.

**"The canvas has a broken hold right now … make sure the error
becomes visible on the andon panel."**  What his panel showed was
`node  held  not running` — a hold standing with no runner up, the
hold's promise not kept, and the row read as calm.  Two things now:
a held node with no runner is a **bold** row that says which way —
`HELD, NOT RUNNING — no runner up; the resolver starts one at its next
visit`; `DEAD, HELD — the hold is older than the death; touch it to
restart` (rule 3, seen from the person's side); `DEAD, HELD — the
resolver restarts it at its next visit` — and a hold that holds
nothing is a **`BROKEN hold`** row of its own: no node at the path it
names (no grant beside it), or a state that is not there, with the
hold's words after it, and the header says `…, K BROKEN`.  `wrong(p)`
is the one rule for bold: a death, cut cords, a broken hold, a held
node not up.  On his canvas right now the row reads `node  HELD, NOT
RUNNING — …`: the tally node idles itself on its own 30 s and the
resolver restarts it once per command, which is the restart-per-command
the first pass named; the row is correct, and it is loud.

Red first again: both passes' tests were run against the launcher and
panel of the commit before them.  Nothing runs the launcher's half
until his `sudo tools/install.sh`; the panel runs from the tree.

## Day one, third pass — the person's hand, the same sitting

Henri, having installed and seen the row read right: *"the andon panel
should have a tool to insert .pin and .hold files to the canvas, and
allow one to remove the .hold, then ensure that the log flows (in case
the program fails or crashes on exit) and that the resolver is called
after the file is added.  Also, entering the andon panel should run
the resolver."*  And, first: *"how do I run the resolver on the
canvas?"* — the answer being `tools/resolve.sh` once, by hand, since
nothing but a hook ran it.

**Built.**  `tools/panel.py hold LABEL NODE [--state DIR]
[WORDS...]`, `pin NAME NODE [--state DIR]`, `unhold LABEL`, `unpin
NAME` — from a shell, and in the TUI as `[h] [p] [u]` with one typed
line — write the canvas and nothing else, then run the resolver once
and show what it said; `[r]` is now resolve, not just refresh.  A hold
from the panel is never wordless (`held by <user>, from the panel`
when no words are given).  The hand refuses a node that is not one (no
grant beside it), a label with a `/` in it, an `unhold` of nothing —
nothing written, the resolver not run; a BROKEN row stays for a file
written by hand.  **Entering the panel runs the resolver** before the
first look — the TUI and the non-tty print alike — so a held node with
no runner is started, and its row says running or which way it is not.
The resolver it runs is `TEND_RESOLVE`, else the installed copy (the
set in force), else the tree's; the panel still starts no program
itself.  The panel's old rule, "it never pins — a pin is the person's
act", is kept as history in its docstring: it still is the person's
act, and the panel is where the person's hand is.

**The log flows — measured, not declared.**  The one test that runs
the whole thing real: the hand writes a hold for a scratch node whose
program dies at once (`exit 3`, a loader line on stderr); the tree's
resolver, `TEND_TREE` at the scratch tree, starts it under the leash;
it dies; the death notice is on the timeline as `dying: exited 3 — …`
in the node's own name; the row reads `DEAD, HELD — the hold is older
than the death; touch it to restart`; and a second visit starts
nothing.  That test found a hole the day's earlier passes had not: **a
node held before it ever ran has no state directory**, and `serve`'s
lock test — `flock -n $STATE/run.lock` — failed to open the file and
read as "a runner is up", exit 0, silent.  A pull never met it because
`pull` makes the directory first.  `serve` now makes `$STATE` once it
has decided to start.

Still not built, by the card's order: the resolver on a timer or at
login (the "user canvas that opens" — nothing runs it when no one is
at the desk, and it is the first thing in this tree that would); a
node's pull as a lock (day two); the canvas's own reach row (day
three).

## Where it sits

Placed last in the priority by the session that wrote it, 2026-08-29,
at Henri's "Lets card it"; a new card arrives unplaced and the tiebreak
is his.  It is the canvas strand's next want after day two landed the
same morning, and the first place the owed crash-loop backoff (item 9)
has somewhere to sit.
