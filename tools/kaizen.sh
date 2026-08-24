#!/bin/sh
#: asked-by: Henri, 2026-08-24 — "you forget kaizen! it's big thing to do after each session."
#
# tools/kaizen.sh — the lamp for the practice that ends a session.
#
#     tools/kaizen.sh            today's commits against today's kaizen; a lamp, never a refusal
#     tools/kaizen.sh --hook     the same, as a UserPromptSubmit hook: its line reaches the session
#
# **A practice a session does only when told is a wish.**  On tend's
# first day the kaizen was written because Henri said "let's do kaizen",
# and it would not have been otherwise — the session had already said
# "packed up".  So the reminder lives outside the session, in two
# places where somebody is already standing: the commit (through
# `tools/pre-commit.sh`, after the gates pass) and the prompt (as a
# hook, so the line lands in the session's own context).
#
# **Andon, not refusal** — gestate's rule for its rules cap, carried:
# it never changes an exit code.  A commit refused for a missing kaizen
# would teach the next session to write a worse one faster.  It lights
# when the tree has commits today and `doc/kaizen/<today>.md` does not
# exist, and says nothing on a day with no commits.
#
# Install as a hook (Henri's edit, since hook config is enforcement):
#     "UserPromptSubmit": [ { "hooks": [ { "type": "command",
#       "command": "\"$CLAUDE_PROJECT_DIR\"/tools/kaizen.sh --hook" } ] } ]
set -eu

root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
today=$(date +%F)
file="doc/kaizen/$today.md"

case "${1:-}" in
"") ;;
--hook) cat >/dev/null ;;          # the harness's JSON; nothing in it is needed
-h|--help) sed -n '2,24p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
*) echo "kaizen: unknown argument \`$1\`" >&2; exit 2 ;;
esac

n=$(git -C "$root" log --since=midnight --oneline 2>/dev/null | wc -l | tr -d ' ')

if [ -f "$root/$file" ]; then
    exit 0
fi
if [ "$n" -eq 0 ]; then
    exit 0
fi
echo "🔴 kaizen: $n commit(s) today and no $file — the sitting is not over until it is written."
exit 0
