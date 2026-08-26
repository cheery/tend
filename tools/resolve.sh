#!/bin/sh
#: asked-by: Henri, 2026-08-26 — "do the next slice" (board/resolver.md: the resolver outside the session's write access)
#
# tools/resolve.sh — a pull with no runner gets one, started from the person's side of the fence.
#
#     tools/resolve.sh            look once: unserved pulls and no runner → start one
#     tools/resolve.sh --hook     the same, as a PostToolUse[Bash] hook: reads and
#                                 drops the hook's stdin, never blocks, exit 0
#     tools/resolve.sh --install  Henri's: put the hook line in .claude/settings.json
#
# **Why this is outside the fence** (board/resolver.md, board/keep.md — the
# tree-row measurement, 2026-08-26): a runner a session starts inside its
# own fence dies with the command that pulled (`--unshare-pid
# --die-with-parent`, measured), and a session that can start the runner
# can start it unconfined.  So the thing that starts a program lives where
# the lamp, the limit and the fence-hook live — on the person's side,
# read fresh at every command, in the protected set — and a session's
# pull is one appended line, nothing more.  The runner it starts is
# `node/run.sh run`: confined by keep, holding the lock, stopping on
# idle; under the leash, so it has a wall budget and leaves a ledger
# line (`tools/leash.sh`).  This script grants nothing and starts nothing
# by itself: it reads a count and takes a lock, and only when the ledger
# holds a pull no runner has served does it start the one runner.
#
# **Cost, measured before it was installed**: one `flock -n`, one `wc -l`,
# one `grep` per command; a leash line per runner started.  Where there
# is no state directory yet, nothing.
set -u
root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
state="${TEND_NODE_STATE_DIR:-$root/node/state}"
ledger="$state/node.state.pull"
lock="$state/run.lock"
idle="${TEND_NODE_IDLE:-30}"

case "${1:-}" in
--hook) cat >/dev/null ;;
--install)
    S=$root/.claude/settings.json
    H='"$CLAUDE_PROJECT_DIR"/tools/resolve.sh --hook'
    [ -n "${TEND_FENCED:-}" ] && { echo "resolve: --install is the person's, from outside the fence" >&2; exit 2; }
    cp "$S" "$S.before-resolve-hook"
    if jq -e --arg h "$H" '[.hooks.PostToolUse[]?.hooks[]?.command] | index($h)' "$S" >/dev/null; then
        echo "resolve: already installed"
    else
        jq --arg h "$H" '.hooks.PostToolUse = ((.hooks.PostToolUse // []) + [{matcher: "Bash", hooks: [{type: "command", command: $h}]}])' "$S" > "$S.new"
        mv "$S.new" "$S"
        echo "resolve: installed  PostToolUse[Bash] -> $H"
        echo "         the previous file is at $S.before-resolve-hook"
    fi
    exit 0 ;;
"") ;;
-h|--help) sed -n '4,9p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
*) echo "resolve: unknown argument \`$1\`" >&2; exit 2 ;;
esac

[ -s "$ledger" ] || exit 0                       # nothing has ever pulled
# looks are serialized: a hook fires at every command, and a second look
# must see what the first started — measured 2026-08-26 on Henri's seat,
# where the leash's scope path took longer than a 3 s wait and two looks
# both started a runner.  The second waits here for the first to finish.
exec 8>>"$state/resolve.lock"
flock -w 10 8 || exit 0
flock -n "$lock" true 2>/dev/null || exit 0      # a runner is up
served=$(grep -o '"pulls": *[0-9]*' "$state/node.state" 2>/dev/null | grep -o '[0-9]*$' || echo 0)
pulled=$(wc -l < "$ledger")
[ "$pulled" -gt "${served:-0}" ] || exit 0       # every pull has been served

setsid -f sh -c "exec '$root/tools/leash.sh' -- sh '$root/node/run.sh' run --idle '$idle'" >> "$state/run.log" 2>&1 </dev/null
# wait for the runner to take the lock, so the next look — a hook fires at
# every command — sees it and does not start a second (measured: two
# back-to-back looks both started one before this loop existed)
n=0; while flock -n "$lock" true 2>/dev/null && [ "$n" -lt 200 ]; do sleep 0.05; n=$((n + 1)); done
if flock -n "$lock" true 2>/dev/null; then
    echo "resolve: $((pulled - served)) unserved pull(s), no runner — started one, and it has not taken the lock after 10s; see $state/run.log" >&2
else
    echo "resolve: $((pulled - served)) unserved pull(s), no runner — started one (node/run.sh run, under the leash); $state/run.log" >&2
fi
exit 0
