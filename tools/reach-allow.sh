#!/bin/sh
# tools/reach-allow.sh — set which fence rows a session may ask for.
#
# This is Henri's bound (card:grant.md, card:fence.md): a session may
# turn a row on inside it and never widen past it.  It lives on the
# fence hook's own command line in .claude/settings.json, which is
# enforcement, so this is run by the person and not by a session.
#
#   tools/reach-allow.sh bus         allow the bus row (the leash's budget)
#   tools/reach-allow.sh bus,audio   allow several, comma-separated
#   tools/reach-allow.sh          clear it — no row may be asked for
#
# Takes effect on the next prompt, not the next session (the sitting
# limit hook did the same when it was installed).  Idempotent.
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
# The tree this governs: TEND_TREE when installed (tools/install.sh), else
# the parent of this file — a tree's own copy works as it always did.
root=${TEND_TREE:-$(CDPATH= cd -- "$here/.." && pwd)}
S="$root/.claude/settings.json"
sel='.hooks.PreToolUse[].hooks[] | select(.command | test("fence-hook"))'
rows="${1:-}"

if [ -n "$rows" ]; then
    jq --arg r "$rows" "($sel | .command) |= (sub(\"^TEND_REACH_ALLOW=[^ ]* \"; \"\") | \"TEND_REACH_ALLOW=\" + \$r + \" \" + .)" "$S" > "$S.new"
else
    jq "($sel | .command) |= sub(\"^TEND_REACH_ALLOW=[^ ]* \"; \"\")" "$S" > "$S.new"
fi
mv "$S.new" "$S"
echo "reach-allow: $(jq -r "$sel | .command" "$S")"
"$here/fence.sh" >/dev/null && echo "fence: up"
