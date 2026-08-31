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
#   tools/reach-allow.sh --trees          the other trees a session may read, and whether they are there
#   tools/reach-allow.sh --trees /a:/b    point it at them, colon-separated — read-only, always
#   tools/reach-allow.sh --trees ""       bind none
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
    -h|--help) sed -n '2,16p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    --rows|--trees) ;;
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

# The other trees a session may read (card:trees.md, day one, 2026-08-31).
# Not a row: a row is a session asking and this bound refusing, and this
# is the person pointing, once, at a place to read.  So it takes a path
# and not a name — and a path is refused here, before the file is
# touched, when it is not absolute, not a directory, carries a character
# a path here may not, or names somewhere that would make the fence a
# door: the tree this governs (already the session's, read-write), a
# directory holding it, the home itself, or the home's secret places.
if [ "$arg" = --trees ]; then
    now=$(printf '%s\n' "$line" | sed -n 's/.*TEND_TREES=\([^ ]*\).*/\1/p')
    if [ $# -lt 2 ]; then
        echo "reach-allow: the trees bound is ${now:-none} — read-only, and a session can neither ask for one nor widen it"
        IFS=:; for p in $now; do
            [ -n "$p" ] || continue
            if [ ! -d "$p" ]; then printf '  ?        %s  is not there — the fence binds nothing for it\n' "$p"
            elif [ -d "$p/board" ] && [ -f "$p/.claude/settings.json" ]; then printf '  bound    %s  by its parts — a method-shaped tree (board/, .claude/settings.json)\n' "$p"
            else printf '  bound    %s  whole — a plain directory\n' "$p"
            fi
        done; unset IFS
        exit 0
    fi
    val=$2
    for p in $(printf '%s' "$val" | tr ':' ' '); do
        case $p in
            /*) ;;
            *) echo "reach-allow: \`$p\` is not an absolute path — nothing changed" >&2; exit 2 ;;
        esac
        case $p in
            *[!A-Za-z0-9._/-]*) echo "reach-allow: \`$p\` holds a character a path here may not (A-Za-z0-9._/- only) — nothing changed" >&2; exit 2 ;;
        esac
        [ -d "$p" ] || { echo "reach-allow: \`$p\` is not a directory — nothing changed" >&2; exit 2; }
        rp=$(CDPATH= cd -P -- "$p" 2>/dev/null && pwd) || rp=$p
        [ "$rp" != "$HOME" ] || { echo "reach-allow: \`$p\` is the home itself — name a directory in it — nothing changed" >&2; exit 2; }
        for b in "$root" "$HOME/.ssh" "$HOME/.config" "$HOME/.local/state" "$HOME/.gnupg" "$HOME/.claude"; do
            case "$rp/" in "$b/"*) echo "reach-allow: \`$p\` is $b or inside it — nothing changed" >&2; exit 2 ;; esac
        done
        case "$root/" in "$rp/"*) echo "reach-allow: \`$p\` holds the tree this governs — nothing changed" >&2; exit 2 ;; esac
    done
    new=$(printf '%s\n' "$line" | sed -e 's/^TEND_TREES=[^ ]* //' -e 's/ TEND_TREES=[^ ]*//')
    # Always written, empty included: `--trees ""` is a bound of none, where
    # no line at all is the script's own default (tools/sandbox.sh).  It goes
    # after the rows bound when there is one — that one is read with `^`.
    case $new in
        TEND_REACH_ALLOW=*) new=$(printf '%s\n' "$new" | sed "s|^\(TEND_REACH_ALLOW=[^ ]* \)|\1TEND_TREES=$val |") ;;
        *) new="TEND_TREES=$val $new" ;;
    esac
    jq --arg c "$new" "($sel | .command) |= \$c" "$S" > "$S.new"
    mv "$S.new" "$S"
    echo "reach-allow: $(jq -r "$sel | .command" "$S")"
    "$here/fence.sh" >/dev/null && echo "fence: up"
    exit 0
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
