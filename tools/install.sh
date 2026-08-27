#!/bin/sh
#: asked-by: Henri, 2026-08-27 — "create an install script that installs this to the machine and protects those files, rather than the files in this tree.  Allow local testing but also allow install.  We do way too much effort here now." (card:install.md)
#
# tools/install.sh — put the restraints in force on the machine, outside every session's write access.
#
#     tools/install.sh              install HEAD's set to $TEND_PREFIX (default
#                                   /usr/local/lib/tend); sudo when the prefix is not yours
#     tools/install.sh --check      what is in force against HEAD: drift, absence,
#                                   a writable copy, which copy the hooks run.  exit 1 on any
#     tools/install.sh --list       the installed set
#     tools/install.sh --hooks      the hook lines as they would read with the installed copies in
#                                   force — printed; `--hooks apply` edits the file, the person's hand
#     tools/install.sh --stage DIR  HEAD's set copied to DIR, no privilege — what an install copies
#
# **Where, and why there** (card:install.md, researched 2026-08-27).
# `/usr/local/lib/tend`, owned by root.  Three reasons, each a
# measurement.  (1) It is outside *every* session's write access with no
# fence up at all: gestate's deny-list has no rule for `~/tend/**` or
# `~/.local/**` and its fence wraps only `pytest` and `cargo`, so a
# user-owned prefix would be "outside the session's write access" only
# by the harness's classifier — the probabilistic layer `tools/fence.sh`'s
# header already declines to lean on.  A root-owned file is refused by
# the kernel, for any uid-1000 process, fenced or not.  (2) `/usr` is
# already bound read-only inside the fence, so the copy in force is
# *visible* from inside — `--check` can compare it to HEAD from a
# session's seat — and unwritable there by construction, not by a bind
# this tree configures.  (3) Installing needs `sudo`, which the
# deny-list already refuses a session: the install is the person's
# hand by a rule that exists, not a new one.  A prefix under `$HOME`
# (`TEND_PREFIX=~/.local/lib/tend`) works for a machine without sudo,
# and `--check` says it is the weaker one.
#
# **What is installed is HEAD, never the working tree.**  A change
# reaches the machine only through a commit, and a commit only through
# the gate (`tools/pre-commit.sh`); an uncommitted edit to a restraint
# is named and left behind.  So "local testing" is the tree — edit,
# run the suite — and "install" is `git commit` then this, and the
# clone-and-outside-hand tax the card names is paid once, here, by a
# `sudo` prompt.
#
# **The installed set is what runs on the person's side, transitively.**
# Not only the protected set (`tools/sandbox.sh --protected`, the
# scripts the hooks run): also what those exec unfenced — `leash.sh`,
# which the fence-hook runs on the host with the sandbox as its
# argument, and `keep.py`, which the launcher confines a node with.
# Both are writable inside the fence today (measured 2026-08-27: a
# session editing either changes what a session or a program may
# reach, before anyone looks — `card:self.md`'s own line for the set).
# `node/run.sh` is a per-node wrapper and stays in the tree.
#
# **The installed copies find the tree by `TEND_TREE`**, set on the
# hook line (`--hooks` prints it); each script's root is
# `${TEND_TREE:-its own parent}`, so the tree's copies still work as
# they do today, and an installed copy is told which tree it governs.
# `CLAUDE_PROJECT_DIR` is deliberately not read by the scripts: a clone
# running its suite with that set would act on the wrong tree.
#
# **`installed` is the record** (spec/os.md, property 5 and 6): the
# commit, the date, the source tree and a sha256 per file, written
# beside the copies.  `--check` reads it back and compares to HEAD —
# a copy in force that nothing checks against the vetted one is
# `done/fence.md`'s silent failure one level out (card:install.md,
# "what it must not become").
set -eu

root=${TEND_TREE:-$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)}
prefix=${TEND_PREFIX:-/usr/local/lib/tend}
settings=${TEND_SETTINGS:-$root/.claude/settings.json}

# The set: the protected set less the per-node wrapper, plus what those
# scripts exec on the person's side.  `test/test_install.py` holds the
# closure: every `$here/tools/X` an installed script names is installed.
persons_side="tools/leash.sh tools/keep.py tools/andon.sh"
set_list() {
    p=$(sh "$root/tools/sandbox.sh" --protected 2>/dev/null || true)
    [ -n "$p" ] || p="tools/sandbox.sh tools/fence-hook.sh tools/fence.sh tools/limit.sh tools/kaizen.sh tools/reach-allow.sh tools/hook-installer.sh tools/resolve.sh tools/launch.sh"
    for f in $p $persons_side; do
        case $f in node/*) ;; *) echo "$f" ;; esac
    done | awk '!seen[$0]++'
}
hooked="kaizen.sh limit.sh fence.sh fence-hook.sh resolve.sh"

mode=install
case "${1:-}" in
    "") ;;
    --check|--list|--hooks) mode=${1#--} ;;
    --stage) mode=stage; stage_dir=${2:-}; [ -n "$stage_dir" ] || { echo "install: --stage DIR" >&2; exit 2; } ;;
    -h|--help) sed -n '4,13p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "install: unknown argument \`$1\`" >&2; exit 2 ;;
esac

[ $mode = list ] && { set_list; exit 0; }

hook_line() { # hook_line SCRIPT ARGS — how settings.json should run the installed copy
    printf 'TEND_TREE="$CLAUDE_PROJECT_DIR" %s/tools/%s%s\n' "$prefix" "$1" "$2"
}
if [ $mode = hooks ]; then
    # The rewrite, as jq: every hook command that names the tree's tools/
    # — `"$CLAUDE_PROJECT_DIR"/tools/X` or an absolute `/home/.../tend/tools/X`
    # — runs the installed X instead, told the tree by TEND_TREE.  A leading
    # `TEND_REACH_ALLOW=… ` survives: the substitution is inside the string.
    # A line already on a prefix is re-pointed too, so the prefix can move
    # (found 16:40: HEAD's settings carried the prefix and a second apply
    # to another prefix changed nothing, and the gate said so).
    prog='walk(if type == "string" then
            gsub("\"\\$CLAUDE_PROJECT_DIR\"/tools/"; "TEND_TREE=\"$CLAUDE_PROJECT_DIR\" " + $p + "/tools/")
          | gsub("(^| )/home/[^/ ]+/tend/tools/"; " TEND_TREE=\"$CLAUDE_PROJECT_DIR\" " + $p + "/tools/")
          | gsub("TEND_TREE=\"\\$CLAUDE_PROJECT_DIR\" [^ ]+/tools/"; "TEND_TREE=\"$CLAUDE_PROJECT_DIR\" " + $p + "/tools/")
          | ltrimstr(" ")
          else . end)'
    if [ "${2:-}" = apply ]; then
        [ "${TEND_FENCED:-}" = 1 ] && { echo "install: --hooks apply is the person's hand, from outside the fence (hook config is enforcement)" >&2; exit 2; }
        command -v jq >/dev/null 2>&1 || { echo "install: jq is needed to edit $settings" >&2; exit 2; }
        jq -e . "$settings" >/dev/null 2>&1 || { echo "install: $settings is missing or not valid JSON — tools/fence.sh --restore first" >&2; exit 1; }
        cp "$settings" "$settings.before-install"
        jq --arg p "$prefix" "$prog" "$settings" > "$settings.new" && mv "$settings.new" "$settings"
        echo "install: hooks now run $prefix/tools/ — the previous file is at $settings.before-install"
        jq -r '[.hooks[]?[]?.hooks[]?.command // empty] | .[]' "$settings" | sed 's/^/  /'
        exit 0
    fi
    echo "# .claude/settings.json — the hook lines as they would read with the installed copies in force ($prefix)."
    echo "# Printed only.  The edit is the person's: tools/install.sh --hooks apply, from outside the fence."
    command -v jq >/dev/null 2>&1 && [ -f "$settings" ] \
        && jq -r --arg p "$prefix" "$prog"' | [.hooks[]?[]?.hooks[]?.command // empty] | .[]' "$settings" | sed 's/^/  /'
    exit 0
fi

git -C "$root" rev-parse --verify -q HEAD >/dev/null || { echo "install: $root is not a git checkout with a HEAD — HEAD is what installs, on purpose" >&2; exit 3; }
head=$(git -C "$root" rev-parse HEAD)

stage() { # stage DIR — HEAD's copy of each file, and the record
    d=$1; mkdir -p "$d/tools"
    for f in $(set_list); do
        git -C "$root" cat-file -e "HEAD:$f" 2>/dev/null || { echo "install: HEAD has no $f — commit it first" >&2; exit 3; }
        git -C "$root" show "HEAD:$f" > "$d/$f"
        case $f in *.sh) chmod 755 "$d/$f" ;; *) chmod 644 "$d/$f" ;; esac
        if ! git -C "$root" diff --quiet HEAD -- "$f" 2>/dev/null; then
            echo "  · $f has an uncommitted change — HEAD is installed, the edit is not (the gate has not seen it)"
        fi
    done
    {
        echo "commit $head"
        echo "date $(date -u +%Y-%m-%dT%H:%M:%SZ)"
        echo "source $root"
        echo "prefix $prefix"
        (cd "$d" && for f in $(set_list); do sha256sum "$f"; done)
    } > "$d/installed"
    chmod 644 "$d/installed"
}

if [ $mode = stage ]; then
    stage "$stage_dir"; echo "install: staged HEAD ($(git -C "$root" rev-parse --short HEAD)) at $stage_dir"; exit 0
fi

fail=0
say() { printf '  %s %s\n' "$1" "$2"; }

if [ $mode = check ]; then
    echo "install: $prefix  (HEAD $(git -C "$root" rev-parse --short HEAD))"
    echo
    if [ ! -e "$prefix/installed" ]; then
        say "✗" "nothing installed at $prefix — the restraints in force are the tree's own copies"; fail=1
    elif [ ! -r "$prefix/installed" ]; then
        say "✗" "$prefix/installed is not readable by you ($(stat -c '%A %U' "$prefix/installed")) — the copy cannot be read back, and the hooks cannot run it either; sudo tools/install.sh again"; fail=1
    else
        ic=$(sed -n 's/^commit //p' "$prefix/installed")
        say "·" "installed commit ${ic%${ic#???????}}, $(sed -n 's/^date //p' "$prefix/installed")"
        for f in $(set_list); do
            if [ ! -e "$prefix/$f" ]; then
                say "✗" "$f is not installed"; fail=1
            elif [ ! -r "$prefix/$f" ]; then
                say "✗" "$f is not readable by you ($(stat -c '%A %U' "$prefix/$f")) — a hook running it dies Permission denied"; fail=1
            elif ! git -C "$root" show "HEAD:$f" | cmp -s - "$prefix/$f"; then
                say "✗" "$f differs from HEAD — the copy in force is not the vetted one"; fail=1
            elif [ -w "$prefix/$f" ]; then
                say "✗" "$f is writable by you — a session runs as you; inside the fence \$HOME is not real, outside it this is a copy a session can edit"; fail=1
            else
                say "✓" "$f — HEAD, read-only to you"
            fi
        done
        if [ -O "$prefix" ]; then say "·" "the prefix is yours, not root's — the weaker of the two: a chmod away for any process running as you, and invisible inside the fence rather than read-only there"; fi
    fi
    if [ -f "$settings" ] && command -v jq >/dev/null 2>&1; then
        cmds=$(jq -r '[.hooks[]?[]?.hooks[]?.command // empty] | .[]' "$settings")
        for h in $hooked; do
            line=$(printf '%s\n' "$cmds" | grep -F "tools/$h" | head -1 || true)
            if [ -z "$line" ]; then say "✗" "tools/$h is on no hook"; fail=1
            elif printf '%s' "$line" | grep -qF "$prefix/tools/$h"; then say "✓" "hook runs the installed tools/$h"
            elif printf '%s' "$line" | grep -q 'TEND_TREE='; then say "✗" "hook runs ANOTHER prefix's tools/$h — ${line#*TEND_TREE=\"\$CLAUDE_PROJECT_DIR\" }"; fail=1
            else say "✗" "hook runs the TREE's tools/$h — the installed copy is not in force (tools/install.sh --hooks)"; fail=1; fi
        done
    fi
    echo
    if [ $fail -eq 0 ]; then echo "  in force: the installed set, at HEAD."; else echo "  NOT IN FORCE as installed — the lines marked ✗ say what."; fi
    exit $fail
fi

# ── install ──────────────────────────────────────────────────────────────
[ "${TEND_FENCED:-}" = 1 ] && { echo "install: this is the person's hand, from outside the fence — a session may not install its own restraint" >&2; exit 2; }
tmp=$(mktemp -d "${TMPDIR:-/tmp}/tend-install.XXXXXX")
trap 'rm -rf "$tmp"' EXIT
echo "install: HEAD $(git -C "$root" rev-parse --short HEAD) → $prefix"
stage "$tmp"
# Who is installing decides the owner and the mode.  Root (`sudo
# tools/install.sh`) installs root-owned, 755/644 — readable and runnable
# by everyone, writable by nobody but root.  A user whose prefix is their
# own gets 555/444: not even they can write it without a chmod first,
# which --check names as the weaker kind.  Anyone else is handed to sudo
# for the copy alone.  (The first install, 2026-08-27 16:17, took the
# user branch as root and computed the mode as 755-222 in decimal — 533,
# -r-x-wx-wx — and every hook died "Permission denied".  Modes are
# spelled out now, and root is recognised as root.)
as=""
if [ "$(id -u)" = 0 ]; then
    owner="-o root -g root"; m_sh=755; m_other=644
    echo "  · running as root — $prefix will be root's, 755/644"
elif [ -w "$prefix" ] || { [ ! -e "$prefix" ] && [ -w "$(dirname "$prefix")" ]; }; then
    owner=""; m_sh=555; m_other=444
    echo "  · $prefix is yours to write — no sudo; --check will say this copy is the weaker kind"
else
    as="sudo"; owner="-o root -g root"; m_sh=755; m_other=644
    echo "  · $prefix is not yours — sudo for the copy, and root will own it"
fi
$as mkdir -p "$prefix/tools"
for f in $(set_list) installed; do
    case $f in *.sh) m=$m_sh ;; *) m=$m_other ;; esac
    $as install $owner -m "$m" "$tmp/$f" "$prefix/$f"
    say "✓" "$f"
done
$as chmod 755 "$prefix" "$prefix/tools"
echo
echo "install: done.  tools/install.sh --check reads it back; tools/install.sh --hooks says how the hooks reach it."
