#!/bin/sh
# tools/reach-allow.sh — set which fence rows a session may ask for.
#
# This is Henri's bound (card:grant.md, card:fence.md): a session may
# turn a row on inside it and never widen past it.  It lives on the
# fence hook's own command line in .claude/settings.json, which is
# enforcement, so this is run by the person and not by a session.
#
#   tools/reach-allow.sh --rows      the rows that may be allowed, and which are
#   tools/reach-allow.sh net         allow the net row
#   tools/reach-allow.sh net,audio   allow several, comma-separated
#   tools/reach-allow.sh             clear it — no row may be asked for
#
# Takes effect on the next prompt, not the next session (the sitting
# limit hook did the same when it was installed).  Idempotent.
#
# **Only a row the fence can be asked for goes on the line** — one that
# is `off` in `tools/sandbox.sh --rows` (`net`, `audio`, `display` as of
# 2026-08-30).  The fence is the one that knows the rows, and this
# script reads them from it rather than keeping a second list to go
# stale.  Anything else is refused before the file is touched, with the
# rows named.  Until 2026-08-30 the argument went onto the line as
# written, and the hook line read `TEND_REACH_ALLOW=net,tree` — `tree`
# is a row that is always on, `--reach tree` is "no such row", and
# this script had written it without a word (F004).  Henri, that
# morning: "modify tend-reach-allow to restrict what you can insert
# into it, and list available allowances as well".
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
# The tree this governs: TEND_TREE when installed (tools/install.sh), else
# the parent of this file — a tree's own copy works as it always did.
root=${TEND_TREE:-$(CDPATH= cd -- "$here/.." && pwd)}
S="$root/.claude/settings.json"
sel='.hooks.PreToolUse[].hooks[] | select(.command | test("fence-hook"))'
arg="${1:-}"

case $arg in
    -h|--help) sed -n '2,12p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    --rows) ;;
    -*) echo "reach-allow: unknown argument \`$arg\`" >&2; exit 2 ;;
esac

# The rows, read off the fence: the ones that are off unless asked for.
# `--rows` is a listing and answers from inside the fence too.
known=$(sh "$here/sandbox.sh" --rows 2>/dev/null | awk '$1 == "off" { printf "%s ", $2 }') || true
[ -n "$known" ] || { echo "reach-allow: could not read the rows from $here/sandbox.sh --rows — nothing set" >&2; exit 2; }
# A `case` on the padded list: it reads the same whatever IFS the caller
# has set (the loops below set it to `,`).
is_row() { case " $known " in *" $1 "*) return 0 ;; *) return 1 ;; esac; }

# The bound as it stands: the hook line, and the rows on it.
line=$(jq -r "$sel | .command" "$S" 2>/dev/null || true)
[ -n "$line" ] || { echo "reach-allow: no fence-hook line in $S — tools/hook-installer.sh first" >&2; exit 2; }
current=$(printf '%s\n' "$line" | sed -n 's/^TEND_REACH_ALLOW=\([^ ]*\) .*/\1/p')

if [ "$arg" = --rows ]; then
    echo "reach-allow: the bound is ${current:-none} — a session may ask for these and no other"
    sh "$here/sandbox.sh" --rows | while IFS= read -r l; do
        case $l in
            "  off  "*)
                rest=${l#"  off  "}; r=${rest%% *}
                case ",$current," in
                    *",$r,"*) printf '  allowed  %s\n' "$rest" ;;
                    *)        printf '  -        %s\n' "$rest" ;;
                esac ;;
        esac
    done
    bad=0
    IFS=,; for r in $current; do
        [ -n "$r" ] && ! is_row "$r" && { printf '  ?        %s  is on the line and is not a row — tools/reach-allow.sh without it\n' "$r"; bad=1; }
    done; unset IFS
    exit $bad
fi

rows=$arg
if [ -n "$rows" ]; then
    # The shape first — a name is [a-z]+, a list is names joined by
    # single commas: the hook reads the line with `[^ ]*` and `,row,`,
    # so a space or an empty name would be a bound nobody can read.
    case $rows in
        *[!a-z,]*|,*|*,|*,,*)
            echo "reach-allow: \`$rows\` is not a comma-separated list of rows.  The rows: $known— tools/reach-allow.sh --rows" >&2; exit 2 ;;
    esac
    IFS=,; for r in $rows; do
        is_row "$r" || { unset IFS; echo "reach-allow: \`$r\` is not a row a session can ask for — nothing changed.  The rows: $known— tools/reach-allow.sh --rows" >&2; exit 2; }
    done; unset IFS
    jq --arg r "$rows" "($sel | .command) |= (sub(\"^TEND_REACH_ALLOW=[^ ]* \"; \"\") | \"TEND_REACH_ALLOW=\" + \$r + \" \" + .)" "$S" > "$S.new"
else
    jq "($sel | .command) |= sub(\"^TEND_REACH_ALLOW=[^ ]* \"; \"\")" "$S" > "$S.new"
fi
mv "$S.new" "$S"
echo "reach-allow: $(jq -r "$sel | .command" "$S")"
"$here/fence.sh" >/dev/null && echo "fence: up"
