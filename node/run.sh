#!/bin/sh
#: asked-by: Henri, 2026-08-26 — "look at keep ... do the next sensible thing" (board/keep.md: nothing yet makes the node run under keep)
#
# node/run.sh — run the node confined, without the incantation.
#
#     node/run.sh [run|pull|status] [args...]
#
#     node/run.sh pull          a pull; if nothing is running, this starts the
#                               node — confined, under the grant below — and
#                               then pulls it.  Nobody starts a program by hand.
#     node/run.sh run [--idle S] the runner itself; refused (exit 75) while
#                               another holds `<state>/run.lock`
#
# **The pull is the launch** (board/resolver.md, day one, 2026-08-26 —
# Henri: the person "always pulls, never need to start the program
# themselves").  So the one place a program is ever started is the one
# place its grant is applied: here.  `pull` takes the lock without
# blocking to learn whether a runner is up; if not, it starts one
# detached (`setsid -f`, output to `<state>/run.log`), waits for that
# runner to open — the node reads the ledger at open, so a pull written
# before that would be seen and not served — then pulls.  Two pulls at
# once may both try to start; the second `run` finds the lock held and
# leaves, exit 75, which is not an error.  `node.py` is untouched — it
# still knows nothing but its ledger and its state.
#
# **Measured, 2026-08-26, from inside the fence**: a process started
# detached inside a fenced command dies with that command (`sandbox.sh`
# runs `--unshare-pid --die-with-parent`).  So inside the fence `pull`
# starts nothing — it appends its line and says who will serve it —
# and `tools/resolve.sh`, a hook on the person's side, starts the runner
# after the command, outliving it.  From a person's shell `pull` starts
# the runner itself, which survives the shell and stops on its own when
# pulls stop (`TEND_NODE_IDLE`, default 30 s).  Nothing here is a daemon.
#
# `board/keep.md`'s last open half: keep exists, but nothing *made* the
# node run under it, so confinement was a line a session had to remember
# to type — and a boundary you have to remember is one you forget.  This
# bakes the node's grant in and runs it through keep, the boundary that
# lives outside the program (Rule 1: the node cannot bound itself).
# Running the node is now running it confined.
#
# The grant, and nothing wider: the node's **code** is readable
# (`--allow node.py`) and its **state directory** is writable
# (`--write`, the scoping built 2026-08-26 — this is its first caller),
# and no network (`--no-net`, built the same day at Henri's "do keep's
# slices" — this is its first caller too: the node is a tally of pulls
# through a file and has no business on a socket).  That is all.  So the
# node may change its own state and nothing else: not its code, not the
# tree, not the ledger beside it, and it cannot reach out.  The state
# directory is kept separate from the code for exactly that reason —
# were it the code's own directory, "writable state" would mean
# "rewritable code".  Default: `node/state`; override TEND_NODE_STATE_DIR.
#
# **A system python, not the venv** (board/keep.md, the runtime is a
# grant): keep grants the system roots, so `/usr/bin/python3` runs; a
# venv interpreter would be blind to its own `pyvenv.cfg` inside.
set -eu
here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
root=$(CDPATH= cd -- "$here/.." && pwd)
# node/run.sh is now a thin wrapper: the node runs through the one
# launcher, under the grant beside it (node/grant).  Kept as a name
# because board/done/pull.md, the README and muscle memory use it.
exec sh "$root/tools/launch.sh" "$here" "$@"
