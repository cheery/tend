#!/bin/sh
# tools/hook-installer.sh — put tend's fence hook on PreToolUse for Bash.
#
# Henri runs this, not a session: hook config is enforcement, and the
# settings file is his to edit (board/cords.md, 2026-08-24; board/fence.md,
# 2026-08-25).  Idempotent — a second run says "already installed".
# It refuses to touch settings until tools/fence-hook.sh exists, so it is
# inert until the hook is built.
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
T=${TEND_TREE:-$(CDPATH= cd -- "$here/.." && pwd)}
S=$T/.claude/settings.json
H='"$CLAUDE_PROJECT_DIR"/tools/fence-hook.sh'
# running installed (tools/install.sh): the line names this copy, and the tree by TEND_TREE
[ "$here" = "$T/tools" ] || H="TEND_TREE=\"\$CLAUDE_PROJECT_DIR\" $here/fence-hook.sh"

[ -x "$here/fence-hook.sh" ] || {
    echo "hook-installer: $here/fence-hook.sh is not there or not executable — nothing to install yet" >&2
    exit 1
}
cp "$S" "$S.before-fence-hook"
if jq -e --arg h "$H" '[.hooks.PreToolUse[]?.hooks[]?.command] | index($h)' "$S" >/dev/null; then
    echo "hook-installer: already installed"
else
    jq --arg h "$H" '.hooks.PreToolUse = ((.hooks.PreToolUse // []) + [{matcher: "Bash", hooks: [{type: "command", command: $h}]}])' "$S" > "$S.new"
    mv "$S.new" "$S"
    echo "hook-installer: installed  PreToolUse[Bash] -> $H"
    echo "                 the previous file is at $S.before-fence-hook"
fi
"$here/fence.sh"
