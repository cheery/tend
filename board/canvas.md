# canvas — a pulled node's death is a line in a file nobody is looking at

    status   open
    because  on 2026-08-28 at 13:27 Henri pulled the llm node and the
             runner died a second later at the loader (libsvml.so, the
             shell had no oneAPI on its path); `pull` had said "started
             llm", `stopped` said `exited 127`, the log said why, and the
             only thing he saw was `lead.sh llm --kept` reporting "not
             up".  The fact of the death existed in the node's state
             directory and nowhere else — no place on the person's side
             shows what the person is holding: which nodes are pulled,
             whether each is running, what it last said as it stopped,
             whether its watcher still beats — and the andon record, the
             one thing that does reach the person, is a separate file
             the panel reads alone.  A death and a cord pull are events
             on the same timeline and the person sees them in two places
             or in none.  The fix that landed the same afternoon (pull
             watches for a second, `card:session-program.md` §13:45) is
             a timing window Henri named as one "we will eventually
             revert" — it catches the failure that happened and no
             slower one, and costs every healthy pull a second
    asked    Henri, 2026-08-28 — "I think that we want a canvas where
             user 'pins' the programs+state they pull.  That could be a
             directory with name.pin -files.  Along the canvas there
             would be an andon/log where errors are shown to the user
             along andon calls."  Then: "I think there could be many
             canvases the user can define, it'd be neat for say, a
             server to have one such canvas directory.  open the canvas
             card"
    see      card:andon-panel.md (done/) — the person-side watcher this
             grows: a TUI outside the fence over the andon record; closed
             2026-08-28 with "the later views are widenings awaiting a
             want", and this is the want, the same day
             card:session-program.md §13:15 — the heartbeat: `status`,
             `check` and `serve` read a held lock and a stale
             `$STATE/watch` as "the cords are cut"; §13:45 — the
             one-second watch in `pull`, and Henri's prediction
             card:node-install.md (done/) — the 07:10 face: the runner's
             loader path is the pulling shell's, which is what died at
             13:27
             card:resolver.md (done/) — the person-side loop that visits
             every node it knows; a canvas is the person saying which
             ones are *held*, and where
             tools/launch.sh — the state a runner leaves: `run.lock`,
             `stopped` (mtime the last stop, its line the reason), `log`,
             `watch`, `run.pid`; tools/andon-panel.py — `read_state`, the
             tone on a new ring
             ~/.local/state/tend — where the andon record lives on the
             person's side and passes through the fence; a canvas
             directory is the same kind of place

## What it is

A **pin** is the person's declaration "I am holding this": a file
`<name>.pin` in a canvas directory, the filename the id the way a card's
is, the content a line or two — the node directory, and the state
directory if it is not the node's default.  Pins are the person's act,
on the person's side, in a place the fence lets through untouched.

A **canvas** is a directory of pins, and there can be many: one for
this desk, one for a server, one for a batch of nodes that belong
together — the person defines them, and which canvas a program looks at
is a path.  A canvas is *not* the resolver's list of every node the tree
knows; it is the person's list of what they are holding right now, and
the same node may be pinned on one canvas and not another.

The **view** over a canvas is the panel grown: one row per pin —
running or not (`run.lock`), the last pull, the last stop and its reason
(`stopped`), the heartbeat read (`watch`: *runner up, watcher silent N
min — the cords are cut*), proposals waiting in `proposals/lead/` — and
beside the rows the **andon/log**: one timeline where a ring, an ask, an
answer and a runner's non-zero stop are the same kind of line, shown as
they happen.  This is the reach-free route for a death the way the panel
is for a ring: the runner writes the record, the view outside the fence
reads it, and the person sees it whenever it happened, not only if
`pull` was still watching.

## What would make this card wrong

If a node's death always reaches the person some other way — if `pull`'s
watch is enough and Henri's prediction is wrong — then the log column is
redundant and the canvas is a status page.  Or if one machine only ever
holds one set of nodes, so "many canvases" is a directory with one file
in it.  The 13:27 minute is evidence against the first; the second is
his own ask (a server's canvas), and the day it is measured is the day a
second canvas exists.

## What it must not become

A second andon (the panel's own rule): the canvas shows, it does not
ring.  A way for a session to pin — a pin is the person's; a session
inside the fence can pull and can read a canvas and cannot hold one.
A server, a GUI, an auto-pin from `pull`, or the resolver reading pins
as its list — each is a widening awaiting a want, and the resolver one
is a decision (`card:resolver.md`'s per-node loop is the tree's, not the
person's).  And not the whole view built before one row is red first.

## Day one

The canvas directory and the panel reading it: `~/.local/state/tend/
canvas/` as the default canvas (a path to name another), `llm.pin` in
it by Henri's hand, and `tools/andon-panel.py` showing one row per pin
from `run.lock` / `stopped` / `watch`, with a non-zero stop appearing in
the log column beside the andon lines.  Red first with a fixture pin
naming a node whose `stopped` says `exited 127` and whose log's last line
is the loader's.  When that row is on the screen, the one-second watch
in `pull` (§13:45) has its replacement and can be reverted, which is
this card's first measurement.

## Where it sits

Placed last in the priority by the session that wrote it, 2026-08-28,
at Henri's "open the canvas card"; a new card arrives unplaced and the
tiebreak is his.  It is the andon strand's next build after
`andon-panel` closed, and the thing `session-program`'s §13:45 watch
waits on to be reverted.
