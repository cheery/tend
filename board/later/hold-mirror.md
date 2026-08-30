# hold-mirror — a hold has nowhere of its own to be written about

    status   shelved — 2026-08-30
    because  a hold is the person's claim, and the program cannot write
             it (card:hold.md rule 5: the state is the runner's, under
             keep; the hold is where the program cannot write).  So
             what the person's side *learns* about a held thing — the
             tick that last saw it, the death it saw, how many times it
             restarted, that its state line names a state nothing runs
             — has only the node's `$STATE` to go to, and a node held
             before it ever ran has no state directory (card:hold.md,
             third pass: `serve` read a missing `run.lock` as "a runner
             is up", silent), a hold whose state line is not
             `NODE/state` names a place the resolver never writes
             (fourth pass: `HELD, NOT HONOURED`), and a window
             (card:canvas-windows.md) has no state directory at all.
             The tick already writes `EPOCH N` beside the canvas
             because it had nowhere else.  Henri, 2026-08-30: "I think
             the canvas should have internal state files that mirror
             the .hold -files, so that there is always a place where to
             write the state, even if the internal state is removed
             after the .hold file is removed."
    asked    Henri, 2026-08-30, ~10:40 — "put these into later/ as cards"
    blocked  waits on the first writer with nowhere to write: the
             canvas-windows daemon (a `.win` has no `$STATE`), or the
             resolver wanting to record its visit to a hold with no
             state directory, or the *instance* want (card:hold.md,
             fourth pass — a (node, state) the resolver serves) needing
             a place per hold rather than per node.  Any of the three
             wakes it; until one does, `$STATE` and the tick's stamp
             are enough and the card would be building for nothing.
    see      card:hold.md (rule 5; the third and fourth passes; the
             tick), card:canvas.md (the canvas directory, the panel as
             its reader), card:canvas-windows.md, card:cords-crate.md
             (a tend app writing its own row: the same place, the app's
             hand), tools/panel.py (`read_canvas`, the hand: hold, pin,
             unhold), tools/resolve.sh (`--tick`), tools/launch.sh
             (`holds_for`)

## What it is, when it comes — Henri's shape

**For every `<label>.hold` the canvas keeps a mirror the person's side
writes** — `<label>.state` beside it, or `canvas/state/<label>` — with
the same name, made when the hold appears and removed *after* the
hold is removed, never before.  Presence follows the hold; content is
the person's side's own knowledge of it: last visited (the tick), last
seen alive, the death and when, restarts since the hold's mtime, and
whether the hold's state line is honoured.  So there is always a
place to write about a hold, whether or not the thing held has a
state directory, has ever run, or is a node at all.

Three rules it carries from the hold card so it does not undo them:

1. **The mirror is never the state.**  `$STATE` is the runner's, under
   keep, and stays so; the mirror is what the person's side observed,
   written from the person's side (the resolver, the panel, the tick)
   and never by the program.  Two files, two hands, as the pin and the
   hold are.
2. **The hold's mtime stays the person's word.**  The mirror records a
   death; it never touches the hold, and a restart still needs the
   hold newer than the death — the mirror is where the panel reads
   "older than the death" from when there is no `stopped` to read.
3. **Removed after the hold, not with it.**  The lag is the point: the
   panel can say "unheld at T, last seen alive at T−n" for a moment
   after the hand lifts, and the resolver's visit that finds a hold
   gone finishes its own line before the mirror goes.  The removal is
   the resolver's, on a visit that finds no hold — never the panel's
   on `unhold`, so the record of the hold outlives the hand by one
   tick.

**Red first, when worked**: a hold for a node with no state directory,
never run — the mirror exists and says "never visited"; the tick
visits — "visited at T, not running"; the hold is removed — the mirror
stays one visit, says "unheld", then goes.

## What it must not become

A second state directory that the program writes to, or a cache of
`$STATE` — the resolver copying `stopped` into the mirror would make
two facts of one.  The mirror holds what only the person's side knows;
where `$STATE` has the fact, the mirror points at it and does not
repeat it.  And not a registry: nothing consults the mirror to decide
whether a node may run; the hold and the grant decide, as today.

## Where it sits

Shelved on arrival, 2026-08-30, at Henri's "put these into later/ as
cards".  When it wakes it is `hold`'s next pass, below `hold` and
beside `canvas-windows`; the tiebreak is his.
