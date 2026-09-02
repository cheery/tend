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
# **One kaizen per sitting — not per day, and not per session.**  The
# first version counted today's commits against today's file, and
# Henri, the same evening: *"I do several sessions in a day."*  So the
# measure is **commits since the last kaizen** — the newest commit that
# added a kaizen is the last sitting that ended properly, and anything
# after it is work no kaizen covers.  A file is named
# `doc/kaizen/<date>-<HHMM>.md` by **when the sitting began** — the end
# is fuzzy, the start is a fact — and the start is read from the tree:
# the first commit since the last kaizen.  The lamp says the name, so
# two sessions cannot disagree.
#
# **And a session is not a sitting** (2026-08-27, `doc/reading-2026-08-27.md`):
# on 2026-08-26 the desk had 14 sittings and this lamp was answered 39
# times, because every session read *"the sitting is not over"* as its
# own and wrote one before it ended.  The unit is the sitting — the
# stretch Henri is at the desk, the thing `tools/limit.sh` measures.
# A session that ends while the sitting goes on owes nothing: the lamp
# stays lit and the next session inherits it.  The kaizen is written
# when the sitting ends — when Henri closes it, or the clock does — and
# covers every uncovered commit, whoever made them.  So the line says
# the unit, and reads the desk's clock beside the name when
# `tools/limit.sh` is there to ask; reading grants nothing.
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

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
# The tree this governs: TEND_TREE when installed (tools/install.sh), else
# the parent of this file — a tree's own copy works as it always did.
root=${TEND_TREE:-$(CDPATH= cd -- "$here/.." && pwd)}
WANT="${TEND_KAIZEN_WANT:-$HOME/.local/state/tend/kaizen-wanted}"
EXT="${TEND_KAIZEN_EXTENDED:-$WANT-extended}"   # the hash of a commit that extended the sitting's kaizen, when said

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
extended)
    # **A kaizen extended is the sitting's kaizen, when said** (kaizen 1544's
    # tension, seen 2026-09-01 and 2026-09-02): a kaizen written mid-sitting at
    # Henri's ask, the sitting going on, and at its close the same file
    # extended — one sitting, one file.  The lamp cannot tell an extension from
    # a count fixed (both modify, neither adds), so, as with `want`, the
    # session says so — after the extending commit, and only if HEAD modified a
    # kaizen-named file.  The stamp is HEAD's hash, beside the want file, and
    # is forgotten when a later kaizen lands.  Saying it is a declaration in
    # the one direction `want` does not cover; a hollow extension is no more
    # checkable than a hollow kaizen, and spec/kaizen.md says so of both.
    head=$(git -C "$root" rev-parse HEAD 2>/dev/null) || { echo "kaizen: no commit to speak of" >&2; exit 2; }
    if ! git -C "$root" show --format= --name-only --diff-filter=M "$head" -- "doc/kaizen/????-??-??-????.md" | grep -q .; then
        echo "kaizen: HEAD did not modify a kaizen file — \`extended\` is said after the commit that extends one" >&2; exit 2
    fi
    mkdir -p "$(dirname "$WANT")"
    printf '%s\n' "$head" > "$EXT"
    echo "kaizen extended at $(git -C "$root" log -1 --format=%h "$head"), $(date +%H:%M): the sitting's kaizen is the one this commit extends"
    exit 0 ;;
-h|--help) sed -n '2,60p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
*) echo "kaizen: unknown argument \`$1\`" >&2; exit 2 ;;
esac

# The last kaizen is the newest commit that added a kaizen *file* — one
# named <date>-<HHMM>.md — not merely a commit that touched doc/kaizen/.
# 2026-08-26: a ledger committed into that directory (doc/kaizen/ingested.md)
# was read as a kaizen landing and put the lamp out with one owed
# (board/green.md).  The name is the kaizen; the directory is not.
# And the *adding* is the landing (--diff-filter=A): a later commit that
# corrects a kaizen file — a count fixed, a name — is not a new kaizen,
# and until 2026-08-27 it put the lamp out with one owed (noted 05:38,
# 07:10; fixed in place the evening the tree's copies became the
# workbench, card:install.md day two — the first restraint edited
# without a clone).
kzn="doc/kaizen/????-??-??-????.md"
last=$(git -C "$root" log -1 --diff-filter=A --format=%H -- "$kzn" 2>/dev/null || true)
if [ -n "$last" ]; then
    range="$last..HEAD"
    since="since the last kaizen ($(git -C "$root" log -1 --diff-filter=A --format=%h -- "$kzn"))"
    last_at=$(git -C "$root" log -1 --diff-filter=A --format=%ct -- "$kzn")
else
    range="HEAD"
    since="and no kaizen yet"
    last_at=0
fi
# An extension said with `extended` is the landing when it is newer than the
# last added kaizen and still on this branch; a later kaizen forgets it.
if [ -f "$EXT" ]; then
    ext=$(head -1 "$EXT" 2>/dev/null || true)
    if [ -n "$ext" ] && git -C "$root" merge-base --is-ancestor "$ext" HEAD 2>/dev/null; then
        ext_at=$(git -C "$root" log -1 --format=%ct "$ext" 2>/dev/null || echo 0)
        # newer by ancestry, not by clock: two commits in one second are still ordered
        if [ -z "$last" ] || { [ "$ext" != "$last" ] && git -C "$root" merge-base --is-ancestor "$last" "$ext" 2>/dev/null; }; then
            last=$ext; last_at=$ext_at; range="$ext..HEAD"
            since="since the kaizen extended at $(git -C "$root" log -1 --format=%h "$ext")"
        else
            rm -f "$EXT"
        fi
    else
        rm -f "$EXT"
    fi
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

# The desk's clock, if there is one to ask: `limit.sh` says "started
# HH:MM, Nm in, Mm left of L" or "closed at HH:MM — why".  Absent, the
# unit is still said; nothing here decides when a sitting ends.
clock=""
if [ -f "$here/limit.sh" ]; then
    clock=$(bash "$here/limit.sh" 2>/dev/null | sed -n 's/^sitting *//p' | head -1) || clock=""
fi
case "$clock" in
    closed*)  when="the sitting is closed ($clock) — write it now" ;;
    started*) when="one per sitting, not per session — write it when the sitting ends (${clock#*, })" ;;
    *)        when="one per sitting, not per session — write it when the sitting ends" ;;
esac

if [ -n "$wanted" ]; then
    echo "🔴 kaizen wanted — $wanted — the sitting is not over until doc/kaizen/$began.md is written; $when."
else
    echo "🔴 kaizen: $n commit(s) $since — the sitting is not over until doc/kaizen/$began.md is written; $when."
fi
exit 0
