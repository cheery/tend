#!/bin/sh
#: asked-by: Henri, 2026-08-24 — "you forget kaizen! it's big thing to do after each session."
#
# tools/kaizen.sh — the lamp for the practice that ends a sitting.
#
#     tools/kaizen.sh                commits since the last kaizen; a lamp, never a refusal
#     tools/kaizen.sh want "why"     a session says it wants a kaizen now, and why
#     tools/kaizen.sh --hook         the lamp as a UserPromptSubmit hook: its line reaches the session
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
# the last sitting that ended properly, and anything after it is work
# no kaizen covers.  A file is named `doc/kaizen/<date>-<HHMM>.md` by
# **when the session began** — the end is fuzzy, the start is a fact —
# and the start is read from the tree: the first commit since the last
# kaizen.  The lamp says the name, so two sessions cannot disagree.
#
# **A session does not judge whether it owes another.**  The first
# draft said a session that goes on after its kaizen "owes another",
# and Henri, the same night: *"you were thinking that you deserve
# another one if I push the sitting further — that's not reliable.  You
# should have a way to tell when you want another kaizen."*  So there is
# `want`: the session (or Henri) pulls the cord itself, with a reason,
# and the lamp lights with that reason until a kaizen is committed after
# it.  Wanting is a declaration, not a verdict — the same shape as the
# sitting limit's `stop`, the one direction a session may move things.
# The want lives in `~/.local/state/tend/kaizen-wanted` (override
# TEND_KAIZEN_WANT), outside the tree like the other ledgers, because
# it is about this desk now and not about the tree.
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
WANT="${TEND_KAIZEN_WANT:-$HOME/.local/state/tend/kaizen-wanted}"

case "${1:-}" in
"") ;;
--hook) cat >/dev/null ;;          # the harness's JSON; nothing in it is needed
want)
    if [ -z "${2:-}" ]; then
        echo "kaizen: say why — tools/kaizen.sh want \"the reason\"" >&2; exit 2
    fi
    mkdir -p "$(dirname "$WANT")"
    printf '%s\t%s\n' "$(date +%s)" "$2" > "$WANT"
    echo "kaizen wanted, $(date +%H:%M): $2"
    exit 0 ;;
-h|--help) sed -n '2,44p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
*) echo "kaizen: unknown argument \`$1\`" >&2; exit 2 ;;
esac

last=$(git -C "$root" log -1 --format=%H -- doc/kaizen/ 2>/dev/null || true)
if [ -n "$last" ]; then
    range="$last..HEAD"
    since="since the last kaizen ($(git -C "$root" log -1 --format=%h -- doc/kaizen/))"
    last_at=$(git -C "$root" log -1 --format=%ct -- doc/kaizen/)
else
    range="HEAD"
    since="and no kaizen yet"
    last_at=0
fi

# A want is answered by a kaizen committed after it, and then forgotten.
wanted=""
if [ -f "$WANT" ]; then
    IFS='	' read -r want_at why < "$WANT" || true
    if [ "${want_at:-0}" -lt "$last_at" ]; then
        rm -f "$WANT"
    else
        wanted="$why"
    fi
fi

n=$(git -C "$root" log --oneline "$range" 2>/dev/null | wc -l | tr -d ' ')
if [ "$n" -eq 0 ] && [ -z "$wanted" ]; then
    exit 0
fi

# The session began at its first uncovered commit; with none yet, now.
began=$(git -C "$root" log --reverse --format=%cd --date=format:%F-%H%M "$range" 2>/dev/null | head -1)
[ -n "$began" ] || began=$(date +%F-%H%M)

if [ -n "$wanted" ]; then
    echo "🔴 kaizen wanted — $wanted — the sitting is not over until doc/kaizen/$began.md is written."
else
    echo "🔴 kaizen: $n commit(s) $since — the sitting is not over until doc/kaizen/$began.md is written."
fi
exit 0
