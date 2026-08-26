#!/bin/sh
#: asked-by: Henri, 2026-08-26 — "look at keep ... do the next sensible thing" (board/keep.md: nothing yet makes the node run under keep)
#
# node/run.sh — run the node confined, without the incantation.
#
#     node/run.sh [run|pull|status] [args...]
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
state="${TEND_NODE_STATE_DIR:-$here/state}"

py=/usr/bin/python3
[ -x "$py" ] || py=$(command -v python3) || {
    echo "node/run.sh: no python3 to run the node." >&2; exit 127; }

mkdir -p "$state"
exec "$py" "$root/tools/keep.py" \
    --allow "$here/node.py" \
    --write "$state" \
    --no-net \
    -- "$py" "$here/node.py" --state "$state/node.state" "$@"
