#!/bin/sh
#: asked-by: Henri, 2026-08-25 — "lets do the next in line" (card:fence.md)
#
# tools/fence.sh — is the deny-list actually in force, and does anything say when it is not?
#
#     tools/fence.sh              check; exit 0 if the fence is up
#     tools/fence.sh --restore    put .claude/settings.json back from git if it
#                                 is missing or unparseable, then check
#     tools/fence.sh --force      put it back from git even if it parses
#     tools/fence.sh --hook       the UserPromptSubmit form: restore what is safe
#                                 to restore, say what is wrong, exit 0
#     tools/fence.sh --protect    add the load-bearing rules that are missing,
#                                 then check — the person's key (card:self.md)
#
# **The failure this exists for was measured on 2026-08-25, in a tend
# session, before this file existed.**  Six routes into
# `.claude/settings.json`: the Edit tool was refused by the deny-list's
# own `Edit(./.claude/**)`; `sed -i`, a heredoc and `jq` were refused by
# the harness's auto-mode classifier — a probabilistic layer that
# belongs to one permission mode and is not in the tree; and `python3 -c`
# rewrote the file and `mv` made it vanish, and nothing said a word.  A
# settings file that is missing, malformed or edited down does not
# announce itself: the session starts, the tools work, and every rule in
# it is simply not applied.  `manifesto.md` rule 2 — what is built must
# be able to say when it is wrong — pointed at the thing that restrains.
#
# **What this can do**: notice, within one prompt, and put a missing or
# unparseable file back.  **What it cannot do**: stop the write.  It
# runs from the very file it checks, so a session that removes the hook
# entry removes the check with it — the file is inside the session's
# write access, and a restraint the restrained party can edit is
# decoration (`vision.md`).  The bound that a session cannot widen is
# `card:work-environment-ai.md`'s, not this script's; what this buys
# until then is that the fence coming down is loud, and that a commit
# with it down is refused (`test/test_fence.py` at the pre-commit gate).
#
# **Borrowed from `~/gestate/tools/leash.sh` on 2026-08-25, and renamed
# on the way**: `leash.sh` here is the budget runner, and one name for
# two mechanisms would mislead whoever reads both trees (`card:fence.md`
# §"The name is already taken").  What is kept: invariants, not bytes —
# comparing to HEAD would flag every legitimate edit, so what is checked
# is the handful of rules that are the point of the file, with `~/` and
# `//home/you/` treated as one spelling; and git as the only canonical
# copy — no second embedded list to go stale, so `--restore` means
# `git checkout` and outside a checkout this says so.  What is changed:
# gestate runs its check once at setup (`tools/secure-init.sh`); this
# one runs at every prompt, because a session's write is noticed sooner
# that way, and jq on a two-kilobyte file costs nothing.
#
# `--restore` only acts when there is nothing to lose.  A file that is
# absent or unparseable cannot be holding work; one that parses might be
# an edit in progress, and reverting it silently would destroy that.
# `--force` is the way to say you meant it.
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
# The tree this governs: TEND_TREE when installed (tools/install.sh), else
# the parent of this file — a tree's own copy works as it always did.
root=${TEND_TREE:-$(CDPATH= cd -- "$here/.." && pwd)}
rel=.claude/settings.json
settings="$root/$rel"

mode=check
case "${1:-}" in
    "") ;;
    --restore|--force|--hook|--protect) mode=${1#--} ;;
    -h|--help) sed -n '2,13p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "fence: unknown argument \`$1\`" >&2; exit 2 ;;
esac

command -v jq >/dev/null 2>&1 || {
    echo "fence: jq is not installed — nothing here can read $rel, and tools/limit.sh needs it too." >&2
    exit 2
}

valid() { jq -e . "$settings" >/dev/null 2>&1; }

restore() {
    if ! git -C "$root" rev-parse --git-dir >/dev/null 2>&1; then
        echo "fence: not a git checkout — nothing to restore from." >&2
        echo "       git is the only canonical copy, on purpose; see the header." >&2
        return 3
    fi
    if ! git -C "$root" cat-file -e "HEAD:$rel" 2>/dev/null; then
        echo "fence: HEAD has no $rel to restore." >&2
        return 3
    fi
    git -C "$root" checkout HEAD -- "$rel"
    echo "fence: restored $rel from HEAD."
}

case $mode in
    force) restore || exit $? ;;
    restore|hook)
        if [ ! -f "$settings" ] || ! valid; then
            if [ $mode = hook ]; then restore || true; else restore || exit $?; fi
        elif [ $mode = restore ]; then
            echo "fence: $rel parses — not reverting it, in case the edit was yours."
            echo "       if you meant to discard it: tools/fence.sh --force"
        fi ;;
esac

# The rules whose absence means the fence is down.  Not the whole list —
# the load-bearing few, `Edit(./.claude/**)` first because it is the one
# that keeps the rest from being edited away with the edit tools; then
# the protected set (card:self.md) — the scripts the hooks run, which
# `tools/sandbox.sh` binds read-only against the shell and these rules
# deny to the edit tools, the same two ways `.claude/` is kept.  And the
# four hooks, because on this tree hook config is enforcement: the lamp,
# the sitting limit, this — and the fence around every shell command.
protected=$(sh "$here/sandbox.sh" --protected 2>/dev/null || true)
[ -n "$protected" ] || protected="tools/sandbox.sh tools/fence-hook.sh tools/fence.sh tools/limit.sh tools/kaizen.sh"
nl='
'
# Which copies are in force is read off the hook lines (card:install.md,
# day two, 2026-08-27): a line carrying `TEND_TREE=` runs an installed
# copy, read-only by ownership, and then the tree's copies are the
# workbench and the `Edit(./tools/…)` rules are not load-bearing — a
# session may edit a restraint in the tree, and nothing runs it until
# `git commit` and `sudo tools/install.sh`.  A line without it runs the
# tree's copy, and the rules are required, as they were.  Both at once
# is a mixed state, and red.  A file that is missing or unparseable is
# read as the tree side: require everything.
side=tree; prefix=""
if [ -f "$settings" ] && valid; then
    lines=$(jq -r '[.hooks[]?[]?.hooks[]?.command // empty] | .[]' "$settings" | grep -E 'tools/(kaizen|limit|fence|fence-hook|resolve)\.sh' || true)
    n_inst=$(printf '%s\n' "$lines" | grep -c 'TEND_TREE=' || true)
    n_tree=$(printf '%s\n' "$lines" | grep -vc 'TEND_TREE=' || true)
    if [ "$n_inst" -gt 0 ] && [ "$n_tree" -eq 0 ]; then
        side=installed
        prefix=$(printf '%s\n' "$lines" | head -1 | sed 's|.*TEND_TREE="[^"]*" ||; s|/tools/.*||')
    elif [ "$n_inst" -gt 0 ]; then side=mixed; fi
fi
rules="Edit(./.claude/**)$nl"
if [ $side != installed ]; then
    for p in $protected; do rules="${rules}Edit(./$p)$nl"; done
fi
rules="${rules}Bash(sudo:*)${nl}Bash(git push:*)${nl}Read(~/.ssh/**)"
# The rules carry spaces and `*`: one per line, and never globbed.
each_rule() { set -f; IFS=$nl; for rule in $rules; do "$@" "$rule"; done; unset IFS; set +f; }

# `--protect` only adds, and only what the list above names: a key that
# can narrow and never widen is one that is safe to keep in the tree,
# once the tree binds it read-only — which `tools/sandbox.sh` does, and
# is why this lives here and not in `~` (card:self.md).  It refuses a
# file that does not parse, because an edit to that is a guess.
if [ $mode = protect ]; then
    [ -f "$settings" ] && valid || { echo "fence: $rel is missing or not valid JSON — tools/fence.sh --restore first." >&2; exit 1; }
    add=""
    absent() {
        want=$(printf '%s' "$1" | sed "s|(~/|(/$HOME/|")
        jq -e --arg r "$1" --arg w "$want" '.permissions.deny // [] | index($r) != null or index($w) != null' "$settings" >/dev/null \
            || add="$add$1$nl"
    }
    each_rule absent
    if [ -z "$add" ]; then
        echo "fence: nothing to add — every load-bearing rule is in $rel."
    else
        printf '%s' "$add" | jq -R . | jq -s '.' > "$settings.protect" \
            && jq --slurpfile a "$settings.protect" '.permissions.deny += $a[0]' "$settings" > "$settings.new" \
            && mv "$settings.new" "$settings"
        rm -f "$settings.protect"
        printf '%s' "$add" | sed 's/^/fence: added  /'
    fi
    mode=check
fi
fail=0
out=""
say() { out="$out  $1 $2
"; }

if [ ! -f "$settings" ]; then
    say "✗" "$rel is MISSING — no rule in it is in force"; fail=1
elif ! valid; then
    say "✗" "$rel is not valid JSON — the whole file is silently ignored"; fail=1
else
    # `(~/` and `(//home/you/` are one rule in two spellings; only the
    # tilde travels between machines, so the list below is written in it
    # and both sides are normalised before comparing.
    deny=$(jq -r --arg home "$HOME" '
        .permissions.deny // []
        | map(sub("\\(~/"; "(/" + $home + "/"))
        | .[]' "$settings")
    missing=0
    in_force() {
        want=$(printf '%s' "$1" | sed "s|(~/|(/$HOME/|")
        if printf '%s\n' "$deny" | grep -qxF -- "$want"; then
            say "✓" "$1"
        else
            say "✗" "$1 — MISSING from the deny-list"; fail=1; missing=1
        fi
    }
    case $side in
        installed) say "✓" "in force: the installed copies at $prefix — the tree's copies are the workbench" ;;
        tree)      say "✓" "in force: the tree's copies — the set is read-only inside and Edit-denied" ;;
        mixed)     say "✗" "hooks run both the tree's and installed copies — one side or the other: tools/install.sh --hooks apply, or tools/fence.sh --force"; fail=1 ;;
    esac
    each_rule in_force
    if [ $missing -ne 0 ]; then
        say "→" "tools/fence.sh --protect adds what is missing and nothing else — the person's key, not a session's"
    fi

    hooks=$(jq -r '[.hooks.UserPromptSubmit[]?.hooks[]?.command // empty] | .[]' "$settings")
    for h in kaizen limit fence; do
        if printf '%s\n' "$hooks" | grep -q "tools/$h\.sh --hook"; then
            say "✓" "tools/$h.sh --hook on UserPromptSubmit"
        else
            say "✗" "tools/$h.sh --hook is not on UserPromptSubmit — it will not run"; fail=1
        fi
    done
    pre=$(jq -r '[.hooks.PreToolUse[]? | select(.matcher == "Bash") | .hooks[]?.command // empty] | .[]' "$settings")
    if printf '%s\n' "$pre" | grep -q 'tools/fence-hook\.sh'; then
        say "✓" "tools/fence-hook.sh on PreToolUse(Bash)"
    else
        say "✗" "tools/fence-hook.sh is not on PreToolUse(Bash) — every shell command runs unfenced"; fail=1
    fi
fi

if [ $mode = hook ]; then
    # stdout on UserPromptSubmit reaches the session; silence when up,
    # because a gate that talks when nothing is wrong gets waved past.
    if [ $fail -ne 0 ]; then
        printf '🔴 fence: THE FENCE IS DOWN — tools/fence.sh --restore puts the file back from git; a weakened file that parses is yours to look at first.\n%s' "$out"
    fi
    exit 0
fi

printf 'fence: %s\n\n%s\n' "$rel" "$out"
if [ $fail -eq 0 ]; then
    echo "  the fence is up."
else
    echo "  THE FENCE IS DOWN.  tools/fence.sh --restore"
fi
exit $fail
