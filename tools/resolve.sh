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
# the launcher (`tools/launch.sh NODE serve`), which starts the node
# confined by keep, holding the lock, stopping on idle; under the leash, so it has a wall budget and leaves a ledger
# line (`tools/leash.sh`).  This script grants nothing and starts nothing
# by itself: it reads a count and takes a lock, and only when the ledger
# holds a pull no runner has served does it start the one runner.
#
# **Cost, measured before it was installed**: one `flock -n`, one `wc -l`,
# one `grep` per command; a leash line per runner started.  Where there
# is no state directory yet, nothing.
set -u
here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
# The tree this governs: TEND_TREE when installed (tools/install.sh), else
# the parent of this file — a tree's own copy works as it always did.
root=${TEND_TREE:-$(CDPATH= cd -- "$here/.." && pwd)}
case "${1:-}" in
--hook) cat >/dev/null ;;
--install)
    S=$root/.claude/settings.json
    H='"$CLAUDE_PROJECT_DIR"/tools/resolve.sh --hook'
    # running installed: the line names this copy, and the tree by TEND_TREE
    [ "$here" = "$root/tools" ] || H="TEND_TREE=\"\$CLAUDE_PROJECT_DIR\" $here/resolve.sh --hook"
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

# The andon's ring crosses the same seam a pull does (card:silent-cord.md,
# 2026-08-28): a fenced session's ring fails at the player and is a line in
# the record; this side, which already runs after every command, sounds
# it once.  Not a daemon; the resolver's cost, one awk when nothing failed.
sh "$here/andon.sh" relay >/dev/null 2>&1 || true

# Every node is a directory with a grant beside its program; the launcher
# knows each one's pull file and lock and makes the per-node decision
# (`launch.sh NODE serve`).  This loop is program-agnostic: it adds the
# node by finding its grant, and nothing here names the node or the
# program (board/keep.md, board/resolver.md — the grant beside the
# program, 2026-08-26).
for grant in "$root"/*/grant; do
    [ -f "$grant" ] || continue
    node=$(dirname "$grant")
    sh "$here/launch.sh" "$node" serve || true
done
exit 0
