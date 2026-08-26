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
state="${TEND_NODE_STATE_DIR:-$here/state}"

py=/usr/bin/python3
[ -x "$py" ] || py=$(command -v python3) || {
    echo "node/run.sh: no python3 to run the node." >&2; exit 127; }

mkdir -p "$state"
lock="$state/run.lock"
idle="${TEND_NODE_IDLE:-30}"

# the grant, and nothing wider; every verb runs through it
confined() {
    exec "$py" "$root/tools/keep.py" \
    --allow "$here/node.py" \
    --write "$state" \
    --no-net \
    -- "$py" "$here/node.py" --state "$state/node.state" "$@"
}

generation() {
    grep -o '"generations": *[0-9]*' "$state/node.state" 2>/dev/null | grep -o '[0-9]*$' || echo 0
}

case "${1:-}" in
run)
    shift
    # the lock is taken on an fd here, before the confinement, and the
    # runner inherits it through keep's exec — held for its whole life.
    # a short wait, not a refusal at once: the resolver tests the lock by
    # taking it for a moment (`flock -n lock true`), and a runner that
    # tried in that moment was turned away with 75 while the resolver
    # waited for a lock nobody would take (measured on Henri's seat,
    # 2026-08-26, 1 in 10).  A real runner still holds it past 2 s.
    exec 9>>"$lock"
    flock -w 2 9 || { echo "node: a runner already holds $lock — pull it instead." >&2; exit 75; }
    confined run "$@"
    ;;
pull)
    # Inside the fence a pull is one appended line and nothing more: the
    # runner is started from the person's side by tools/resolve.sh
    # (board/resolver.md, 2026-08-26), because one started here dies with
    # the command and was startable unconfined.  From a person's shell,
    # as before: start one if none is up, then pull.
    if [ -n "${TEND_FENCED:-}" ]; then
        echo "node: pull recorded — inside the fence the runner is the resolver's to start (tools/resolve.sh --hook)" >&2
    elif flock -n "$lock" true 2>/dev/null; then
        before=$(generation)
        setsid -f sh "$0" run --idle "$idle" >> "$state/run.log" 2>&1 </dev/null
        # wait for the runner to open (its generation to move), capped
        n=0
        while [ "$(generation)" -le "$before" ] && [ "$n" -lt 60 ]; do
            sleep 0.05; n=$((n + 1))
        done
        if [ "$(generation)" -le "$before" ]; then
            echo "node: started a runner but it has not opened after 3s — see $state/run.log" >&2
        elif [ -n "${TEND_FENCED:-}" ]; then
            echo "node: started a runner (idle ${idle}s) — inside the fence it lives only as long as this command" >&2
        else
            echo "node: started a runner (idle ${idle}s); it stops by itself when pulls stop" >&2
        fi
    fi
    confined pull
    ;;
*)
    confined "$@"
    ;;
esac
