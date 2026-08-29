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
#     tools/install.sh --bin        the commands: tend-<name> for each installed script, in $TEND_BINDIR
#     tools/install.sh --free       day two, the person's: lift the Edit(./tools/…) rules from
#                                   settings.json once the hooks run the installed copies — the
#                                   tree's copies become the workbench
#     tools/install.sh --hook       the lander lamp (card:lander.md): as a UserPromptSubmit hook — while
#                                   the prefix is behind HEAD, one line says by how much and which
#                                   files, and logs it; dark when in force; never acts
#     tools/install.sh --tick [SECONDS]
#                                   the person's: the tick's carrier (card:hold.md) — a systemd user
#                                   timer running the INSTALLED resolver (`resolve.sh --tick`) every
#                                   SECONDS (default 30).  systemd is Ubuntu's implementation, not the
#                                   dependency: the tick is the stamp the resolver leaves, and cron
#                                   or a loop is the same carrier elsewhere; TEND_UNIT_DIR to write
#                                   the units without enabling them
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
# **Each installed script is a command, `tend-<name>`** — `tend-fence`,
# `tend-keep`, `tend-reach-allow` — a two-line wrapper in
# `/usr/local/bin` (root) or `~/.local/bin` (a user prefix), not a
# symlink: the scripts find their siblings by `dirname "$0"`, and through
# a symlink `$0` is the bin directory.  The wrapper execs the installed
# file and supplies TEND_TREE from the tree you stand in (`git rev-parse
# --show-toplevel`) when it is not set, so `tend-fence` run in ~/tend
# governs ~/tend.  Henri, 2026-08-27: "make neat symlinks into bin, eg.
# tend-keep tend-reach-allow for each tend command during install."
#
# **The lander lamp is `--hook`** (card:lander.md, day one, 2026-08-28).
# A commit through the gate is vetted and not in force until the
# person's `sudo`, and until this nothing said so between the two —
# `--check` said it only when run, and twice a session reached across
# the boundary rather than wait in silence (doc/kaizen/2026-08-27-0710.md).
# The lamp is the kaizen lamp's shape: at every prompt, if HEAD's copy
# of any installed file differs from the record's sha256, one line —
# how many commits, which files, how long the oldest has waited — and
# nothing else; dark when in force; it never installs.  Every lit prompt
# is appended to `~/.local/state/tend/lander.log` with how far behind,
# which is the count the card says would make its actor wrong: if the
# wait never outlives a sitting, the lamp is the whole card.  It runs
# on the person's side like the other lamps, so this script is in the
# installed set and the hook line names the prefix's copy.
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
# The commands go in the bin beside the prefix's lib: /usr/local/lib/tend
# → /usr/local/bin, ~/.local/lib/tend → ~/.local/bin (both on a shell's
# PATH already); a prefix of another shape gets its own bin/, and --bin
# says where.  TEND_BINDIR overrides.
case $prefix in */lib/tend) bindir=${TEND_BINDIR:-${prefix%/lib/tend}/bin} ;; *) bindir=${TEND_BINDIR:-$prefix/bin} ;; esac
cmd_of() { n=${1#tools/}; n=${n%.sh}; n=${n%.py}; printf 'tend-%s' "$n"; }
settings=${TEND_SETTINGS:-$root/.claude/settings.json}

# The set: the protected set less the per-node wrapper, plus what those
# scripts exec on the person's side.  `test/test_install.py` holds the
# closure: every `$here/tools/X` an installed script names is installed.
persons_side="tools/leash.sh tools/keep.py tools/andon.sh tools/install.sh"
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
    --check|--list|--hooks|--free|--bin|--hook) mode=${1#--} ;;
    --stage) mode=stage; stage_dir=${2:-}; [ -n "$stage_dir" ] || { echo "install: --stage DIR" >&2; exit 2; } ;;
    --tick) mode=tick; tick_every=${2:-30}
        case $tick_every in ''|*[!0-9]*) echo "install: --tick SECONDS — a count of seconds, not \`$tick_every\`" >&2; exit 2 ;; esac ;;
    -h|--help) sed -n '4,26p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "install: unknown argument \`$1\`" >&2; exit 2 ;;
esac

[ $mode = list ] && { set_list; exit 0; }
[ $mode = bin ] && { for f in $(set_list); do printf '%s/%s -> %s/%s\n' "$bindir" "$(cmd_of "$f")" "$prefix" "$f"; done; exit 0; }

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
    # The lander lamp's line is added when absent (idempotent, the
    # hook-installer's shape): a prompt hook, beside the kaizen lamp's.
    lander=$(hook_line install.sh " --hook")
    add='if ([.hooks.UserPromptSubmit[]?.hooks[]?.command] | index($h)) then . else
           .hooks.UserPromptSubmit = ((.hooks.UserPromptSubmit // []) + [{hooks: [{type: "command", command: $h}]}]) end'
    if [ "${2:-}" = apply ]; then
        [ "${TEND_FENCED:-}" = 1 ] && { echo "install: --hooks apply is the person's hand, from outside the fence (hook config is enforcement)" >&2; exit 2; }
        command -v jq >/dev/null 2>&1 || { echo "install: jq is needed to edit $settings" >&2; exit 2; }
        jq -e . "$settings" >/dev/null 2>&1 || { echo "install: $settings is missing or not valid JSON — tools/fence.sh --restore first" >&2; exit 1; }
        cp "$settings" "$settings.before-install"
        jq --arg p "$prefix" --arg h "$lander" "$prog | $add" "$settings" > "$settings.new" && mv "$settings.new" "$settings"
        echo "install: hooks now run $prefix/tools/ — the previous file is at $settings.before-install"
        jq -r '[.hooks[]?[]?.hooks[]?.command // empty] | .[]' "$settings" | sed 's/^/  /'
        exit 0
    fi
    echo "# .claude/settings.json — the hook lines as they would read with the installed copies in force ($prefix)."
    echo "# Printed only.  The edit is the person's: tools/install.sh --hooks apply, from outside the fence."
    command -v jq >/dev/null 2>&1 && [ -f "$settings" ] \
        && jq -r --arg p "$prefix" --arg h "$lander" "$prog | $add"' | [.hooks[]?[]?.hooks[]?.command // empty] | .[]' "$settings" | sed 's/^/  /'
    exit 0
fi

if [ $mode = tick ]; then
    # The tick's carrier (card:hold.md, 2026-08-29 — Henri: "do not make it
    # depend on systemd, but use systemd in implementation for ubuntu").  The
    # tick itself is `resolve.sh --tick N` and the stamp it leaves; this
    # writes the one carrier this machine has, and it runs the INSTALLED
    # resolver only — a timer that ran the tree's copy would be a session's
    # edit running on a schedule with nobody watching.
    [ "${TEND_FENCED:-}" = 1 ] && { echo "install: --tick is the person's hand, from outside the fence — a session may not schedule its own resolver" >&2; exit 2; }
    [ -f "$prefix/tools/resolve.sh" ] || { echo "install: nothing installed at $prefix — the tick runs the installed resolver, never the tree's; sudo tools/install.sh first" >&2; exit 1; }
    udir=${TEND_UNIT_DIR:-$HOME/.config/systemd/user}
    mkdir -p "$udir"
    {
        echo "[Unit]"
        echo "Description=tend tick — the installed resolver every ${tick_every}s, for the holds on the canvas (card:hold.md)"
        echo
        echo "[Service]"
        echo "Type=oneshot"
        echo "Environment=TEND_TREE=$root"
        echo "ExecStart=/bin/sh $prefix/tools/resolve.sh --tick $tick_every"
    } > "$udir/tend-tick.service"
    {
        echo "[Unit]"
        echo "Description=tend tick, every ${tick_every}s"
        echo
        echo "[Timer]"
        echo "OnBootSec=30s"
        echo "OnUnitActiveSec=${tick_every}s"
        echo "AccuracySec=5s"
        echo
        echo "[Install]"
        echo "WantedBy=timers.target"
    } > "$udir/tend-tick.timer"
    echo "install: tick — $udir/tend-tick.timer runs $prefix/tools/resolve.sh --tick $tick_every for $root"
    if [ -z "${TEND_UNIT_DIR:-}" ] && command -v systemctl >/dev/null 2>&1; then
        if systemctl --user daemon-reload && systemctl --user enable --now tend-tick.timer; then
            echo "         enabled; the panel's tick line says when it last ran (tools/panel.py)"
        else
            echo "install: the units are written but systemctl --user could not enable the timer — enable it by hand, or use the cron line below" >&2
        fi
    fi
    echo "         the same tick without systemd, as a cron line (crontab -e):"
    echo "           * * * * * TEND_TREE=$root /bin/sh $prefix/tools/resolve.sh --tick 60"
    exit 0
fi

if [ $mode = hook ]; then
    cat >/dev/null                      # the harness's JSON; nothing in it is needed
    log=${TEND_LANDER_LOG:-$HOME/.local/state/tend/lander.log}
    # Nothing installed, or a record this user cannot read, is --check's
    # finding and not a wait: the lamp is about a vetted change waiting.
    [ -r "$prefix/installed" ] || exit 0
    git -C "$root" rev-parse --verify -q HEAD >/dev/null 2>&1 || exit 0
    ic=$(sed -n 's/^commit //p' "$prefix/installed")
    behind=""
    for f in $(set_list); do
        want=$(git -C "$root" show "HEAD:$f" 2>/dev/null | sha256sum | cut -d' ' -f1)
        have=$(awk -v f="$f" '$2 == f { print $1 }' "$prefix/installed")
        [ "$want" = "$have" ] || behind="$behind $f"
    done
    [ -n "$behind" ] || exit 0
    behind=${behind# }
    # How far: commits since the installed one touching what differs, and
    # how long the oldest of them has waited.  A record whose commit is
    # not behind HEAD (a rebase, another tree) counts as `?`.
    n=$(git -C "$root" rev-list --count "$ic..HEAD" -- $behind 2>/dev/null) || n="?"
    [ "$n" = 0 ] && n="?"
    oldest=$(git -C "$root" rev-list --reverse "$ic..HEAD" -- $behind 2>/dev/null | head -1)
    now=$(date +%s)
    if [ -n "$oldest" ]; then
        at=$(git -C "$root" show -s --format=%ct "$oldest"); wait=$((now - at))
        if [ "$wait" -ge 86400 ]; then ago="$((wait / 86400))d $(( (wait % 86400) / 3600 ))h"
        elif [ "$wait" -ge 3600 ]; then ago="$((wait / 3600))h $(( (wait % 3600) / 60 ))m"
        else ago="$((wait / 60))m"; fi
        since="waiting since $(date -d "@$at" +%H:%M) ($ago)"
    else
        wait="?"; since="the installed commit is not behind HEAD (${ic%${ic#???????}})"
    fi
    mkdir -p "$(dirname "$log")" 2>/dev/null && printf '%s\t%s\tbehind=%s\twait=%s\t%s\n' "$now" "$(date -d "@$now" +%F\ %H:%M)" "$n" "$wait" "$behind" >> "$log" 2>/dev/null || true
    # The line handed to the person is one that runs: tend-install exists
    # only after the first install; before it, the tree's script.
    line="sudo tend-install"; [ -x "$bindir/tend-install" ] || line="sudo tools/install.sh"
    echo "🔴 lander: the prefix is behind HEAD — $n commit(s) touching $(echo "$behind" | sed 's/ /, /g'), $since — vetted, not in force until the person's line: $line"
    exit 0
fi

if [ $mode = free ]; then
    [ "${TEND_FENCED:-}" = 1 ] && { echo "install: --free is the person's hand, from outside the fence (the deny-list is enforcement)" >&2; exit 2; }
    command -v jq >/dev/null 2>&1 || { echo "install: jq is needed to edit $settings" >&2; exit 2; }
    jq -e . "$settings" >/dev/null 2>&1 || { echo "install: $settings is missing or not valid JSON — tools/fence.sh --restore first" >&2; exit 1; }
    cmds=$(jq -r '[.hooks[]?[]?.hooks[]?.command // empty] | .[]' "$settings")
    for h in $hooked; do
        printf '%s\n' "$cmds" | grep -F "tools/$h" | grep -qF "$prefix/tools/$h" \
            || { echo "install: the hook for tools/$h does not run $prefix — the tree's copy is still what runs, and freeing it would leave a restraint writable to the session.  tools/install.sh --hooks apply first" >&2; exit 1; }
    done
    rules=$(for f in $(sh "$root/tools/sandbox.sh" --protected 2>/dev/null); do printf 'Edit(./%s)\n' "$f"; done | jq -R . | jq -s .)
    cp "$settings" "$settings.before-free"
    jq --argjson r "$rules" '.permissions.deny |= map(select(. as $x | $r | index($x) | not))' "$settings" > "$settings.new" && mv "$settings.new" "$settings"
    echo "install: the tree's copies are the workbench — $(printf '%s' "$rules" | jq length) Edit rules lifted; the previous file is at $settings.before-free"
    sh "$root/tools/fence.sh" | tail -1
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
    mkdir -p "$d/bin"
    for f in $(set_list); do
        c=$(cmd_of "$f")
        case $f in *.py) run="exec \"\${TEND_PYTHON:-python3}\" \"$prefix/$f\" \"\$@\"" ;; *) run="exec \"$prefix/$f\" \"\$@\"" ;; esac
        {
            echo '#!/bin/sh'
            echo "# $c — the installed $f at $prefix (tools/install.sh, $(date -u +%Y-%m-%d)); the tree is TEND_TREE, else the one you stand in"
            echo '[ -n "${TEND_TREE:-}" ] || TEND_TREE=$(git rev-parse --show-toplevel 2>/dev/null) || TEND_TREE=""'
            echo '[ -n "$TEND_TREE" ] && export TEND_TREE'
            echo "$run"
        } > "$d/bin/$c"
        chmod 755 "$d/bin/$c"
    done
    {
        echo "commit $head"
        echo "date $(date -u +%Y-%m-%dT%H:%M:%SZ)"
        echo "source $root"
        echo "prefix $prefix"
        echo "bindir $bindir"
        (cd "$d" && for f in $(set_list); do sha256sum "$f"; done)
        for f in $(set_list); do echo "bin $(cmd_of "$f") -> $f"; done
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
        for f in $(set_list); do
            c=$(cmd_of "$f")
            if [ ! -e "$bindir/$c" ]; then say "✗" "$bindir/$c is not there — the command for $f (tools/install.sh installs it)"; fail=1
            elif ! grep -qF "$prefix/$f" "$bindir/$c"; then say "✗" "$bindir/$c does not run $prefix/$f"; fail=1
            elif [ -w "$bindir/$c" ]; then say "✗" "$bindir/$c is writable by you"; fail=1
            else say "✓" "$c → $f"; fi
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
        # The lander lamp is a lamp, not a restraint: absent is a note, not a fault.
        if printf '%s\n' "$cmds" | grep -F "tools/install.sh --hook" | grep -qF "$prefix/tools/install.sh"; then say "✓" "the lander lamp is on a prompt hook (tools/install.sh --hook)"
        else say "·" "the lander lamp is on no hook — a vetted change waits in silence; tools/install.sh --hooks apply adds the line (card:lander.md)"; fi
    fi
    # The tick is a want, not a restraint: absent is a note.  The stamp is the
    # measurement, whatever carrier wrote it (card:hold.md).
    tickstamp=${TEND_TICK:-${HOME:-/nonexistent}/.local/state/tend/tick}
    if [ -r "$tickstamp" ] && read -r tat tevery < "$tickstamp" 2>/dev/null && [ -n "$tevery" ]; then
        tage=$(( $(date +%s) - tat ))
        if [ "$tage" -gt $(( tevery * 3 > 90 ? tevery * 3 : 90 )) ]; then say "✗" "the tick is stale — last $((tage / 60)) min ago, every ${tevery}s: the carrier has stopped (systemctl --user status tend-tick.timer)"; fail=1
        else say "✓" "the tick runs — last ${tage}s ago, every ${tevery}s"; fi
    else say "·" "no tick — nothing runs the resolver when nobody is at the desk; tools/install.sh --tick is the carrier (card:hold.md)"; fi
    if [ -f "$settings" ] && command -v jq >/dev/null 2>&1 && [ $fail -eq 0 ]; then
        deny_now=$(jq -r '.permissions.deny[]' "$settings")
        left=0; for f in $(set_list) node/run.sh; do printf '%s\n' "$deny_now" | grep -qxF "Edit(./$f)" && left=$((left + 1)); done
        if [ "$left" -gt 0 ]; then say "·" "the tree's copies are still Edit-denied ($left rules) — tools/install.sh --free lifts them: day two, the workbench"
        else say "✓" "the tree's copies are the workbench — no Edit rule denies them"; fi
    fi
    echo
    if [ $fail -eq 0 ]; then echo "  in force: the installed set, at HEAD."; else echo "  NOT IN FORCE as installed — the lines marked ✗ say what."; fi
    # The fence in force is the installed one; the tree's --check measures
    # the tree's copy.  From outside, run the one the hooks run.
    if [ $fail -eq 0 ] && [ "${TEND_FENCED:-}" != 1 ] && [ -x "$prefix/tools/sandbox.sh" ]; then
        echo; TEND_TREE=$root sh "$prefix/tools/sandbox.sh" --check; exit $?
    fi
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
$as mkdir -p "$bindir"
for f in $(set_list); do
    c=$(cmd_of "$f")
    $as install $owner -m "$m_sh" "$tmp/bin/$c" "$bindir/$c"
    say "✓" "$bindir/$c"
done
echo
echo "install: done.  tools/install.sh --check reads it back; tools/install.sh --hooks says how the hooks reach it."
