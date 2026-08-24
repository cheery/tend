#!/bin/sh
#: asked-by: Henri, 2026-08-24 — "you forget kaizen! it's big thing to do after each session."
#
# tools/kaizen.sh — the lamp for the practice that ends a session.
#
#     tools/kaizen.sh            commits since the last kaizen; a lamp, never a refusal
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
# **One kaizen per session, not per day.**  The first version counted
# today's commits against today's file, and Henri, the same evening:
# *"I do several sessions in a day."*  So the measure is **commits since
# the last kaizen** — the newest commit that touched `doc/kaizen/` is
# the last session that ended properly, and anything after it is work
# no kaizen covers.  A file is named `doc/kaizen/<date>-<HHMM>.md` by
# when the session ended it; a session that goes on after its kaizen
# owes another, or appends, and either puts the lamp out.
#
# **Andon, not refusal** — gestate's rule for its rules cap, carried:
# it never changes an exit code.  A commit refused for a missing kaizen
# would teach the next session to write a worse one faster.
#
# Install as a hook (Henri's edit, since hook config is enforcement):
#     "UserPromptSubmit": [ { "hooks": [ { "type": "command",
#       "command": "\"$CLAUDE_PROJECT_DIR\"/tools/kaizen.sh --hook" } ] } ]
set -eu

root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)

case "${1:-}" in
"") ;;
--hook) cat >/dev/null ;;          # the harness's JSON; nothing in it is needed
-h|--help) sed -n '2,30p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
*) echo "kaizen: unknown argument \`$1\`" >&2; exit 2 ;;
esac

last=$(git -C "$root" log -1 --format=%H -- doc/kaizen/ 2>/dev/null || true)
if [ -n "$last" ]; then
    n=$(git -C "$root" log --oneline "$last..HEAD" 2>/dev/null | wc -l | tr -d ' ')
    since="since the last kaizen ($(git -C "$root" log -1 --format=%h -- doc/kaizen/))"
else
    n=$(git -C "$root" log --oneline 2>/dev/null | wc -l | tr -d ' ')
    since="and no kaizen yet"
fi

if [ "$n" -eq 0 ]; then
    exit 0
fi
echo "🔴 kaizen: $n commit(s) $since — the session is not over until doc/kaizen/$(date +%F-%H%M).md is written."
exit 0
