# hold — a node that should be up is up only while something happens to pull it

    status   open
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

A **hold** is a file whose *presence* is a standing pull: while
`<name>.hold` exists, something pulls the node — the resolver starts a
runner for it when none is up, and the runner is not idle while the
file is there.  Its *mtime* is the person saying so again (`touch`),
and its content is the asked-by, the way a pull line carries its text
and a card carries `asked`: a hold with no words is suspect.  Removing
the file is the act that lets the node stop; idle applies again the
moment it is gone.  `.pin` stays what it is — "show me a row" — and a
hold is a different file, because presence-and-mtime is the whole
mechanism and `touch`/`rm` is the act (Henri: "pin files should pin
files, these files should be something else").

Four boundaries the tree already has, agreed on 2026-08-29, each of
which the design keeps:

1. **A hold is a lifecycle grant, so it never extends a sitting.**
   `launch.sh`'s rule stands: a node may end its sitting early and can
   never extend one.  A hold means *restart it when it stops*, not
   *never stop it*: the sitting cuts, the resolver starts a fresh one,
   the gap is honest.  Otherwise a hold is the extension the grant
   forbids, in a different dress.
2. **The runner knows it is held, or idle fights the hold.**  `serve`
   hands the runner the hold's path; the watch loop reads the file's
   presence as the pulse — not idle while it exists — one `[ -f ]` per
   tick in the loop that already ticks.  Without this a held llm node
   is a reload loop at 80 s a turn on the GPU.  (Henri: "not sure but
   it sounds right" — the first held run is its measurement.)
3. **A crash is not hammered.**  After a clean stop (the sitting),
   restart unconditionally; after a *death* (a non-zero exit, now a
   line in the andon record), restart only if the hold is newer than
   the death — the person re-asserts with a `touch`, having seen why.
   The same mtime comparison `serve` already makes between the pull and
   `stopped`.  This is item 9's crash-loop backoff, in the tree's own
   grammar, and the andon half of it is the death notice.
4. **Whose hand.**  The hold lives where the program cannot write it —
   not `$STATE` (keep grants the program its state; a node that could
   hold itself is the bounded party setting its own boundary, Rule 1)
   — and, Henri, 2026-08-29: *"canvas should be in place where access
   must be granted separately if it's to be touched."*  Today the
   canvas is under `~/.local/state/tend`, which the fence binds
   read-write for the andon and the clock, so a fenced session could
   touch a hold and the tree could not tell its hand from his.  The
   canvas moves, or is bound apart, so that writing it is a reach row
   of its own — off by default — and a session's hold is a widening a
   person granted, never a side effect of the andon's row.  Until that
   row exists, the backstop is (1): a forged hold buys at most
   restart-after-sitting, never a longer sitting.

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
sitting extension (rule 1 above).  A restart loop (rule 3).  A second
list for the resolver — it keeps its own list of nodes and honours the
holds it finds; "the resolver reads pins as its list" stays the
decision card:canvas.md marked it, and a hold makes it unnecessary.  A
process supervisor: no PID files of its own, no health checks, no
"desired state" beyond a file being there — the runner's `run.lock`,
`stopped` and `watch` are the state, as they are today.  And not
anything a session can create by default (rule 4).

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
pulled cold once.  Rule 4's separate reach row is day two, and is not
a build before day one has been held once — its shape is
card:silent-cord.md's, a row off by default with the sound on when it
is off.

## Where it sits

Placed last in the priority by the session that wrote it, 2026-08-29,
at Henri's "Lets card it"; a new card arrives unplaced and the tiebreak
is his.  It is the canvas strand's next want after day two landed the
same morning, and the first place the owed crash-loop backoff (item 9)
has somewhere to sit.
