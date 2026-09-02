#!/bin/sh
#: asked-by: Henri, 2026-08-25 — "show me the hook", after both mediation orders were tried and came back as one fence
#
# tools/sandbox.sh — run a command with this tree as its whole world, and the cords still reaching the person.
#
#     tools/sandbox.sh [--reach ROW,ROW] command args...
#     tools/sandbox.sh --check              prove the fence is up — the clock first
#     tools/sandbox.sh --rows               the rows and their defaults
#     tools/sandbox.sh --protected          the paths read-only inside, one per line
#
# **This is a namespace, not a permission.**  Nothing here is made
# unreadable: a process sees exactly what was bound into its mount
# namespace, and what was not bound does not exist for it.  `~/.ssh`
# inside is `No such file or directory`, never `Permission denied`, and
# `$HOME` itself is readable and writable — it is simply a fresh tmpfs
# at the same path.  That is Plan 9's per-process namespace used as a
# boundary, and `--ro-bind` is Plan 9's verb; it is stronger than a
# permission, because there is no ACL to defeat and root inside cannot
# read what was never mounted.  The tree's other boundary, `tools/keep.py`,
# is the opposite idiom — a Landlock ruleset that denies (EACCES) rather
# than hides — and `spec/os.md` §"Appended 2026-08-31" says why there
# are two and where each is used.  Written at Henri's question,
# 2026-08-31: "is there reason why $HOME is not $HOME?"
#
# **This is the sessions-first fence of doc/experiments/2026-08-25-both.md,
# promoted.**  Bubblewrap: the system read-only, an empty home, no
# network, this tree the one writable thing — and, learned the same day,
# the person's cords passed through: `~/.local/state/{tend,gestate}` and the sitting's
# state file read-write, so that inside the fence the sitting clock is
# the host's, the leash ledger lands, and a kaizen want is heard.  The
# fence that hid those gave a fenced session a fresh 15-minute sitting
# (doc/experiments/2026-08-25-reach.md).  The fence and the cords are
# one design.
#
# **`$HOME` keeps its own path, and `~/.claude` is read-only** (Henri,
# 2026-08-31: "should the $HOME stay $HOME?  Kind of makes sense to
# me").  It should: the cords above are shared because the path inside
# *is* the path outside, so `tools/limit.sh` reads one sittings log
# from either side and `--check` can compare the clocks at all.  But an
# empty writable home made a real defect (`card:lost-write.md`): the
# session's memory lives at `~/.claude`, the fence hid it, and a write
# there landed in the tmpfs and evaporated — measured 2026-08-31,
# `mkdir -p ~/.claude/… && printf … > …` succeeded at exit 0 and was
# gone, which is how three kaizens' worth of memories were lost.  So
# the directory now exists as an empty read-only mount: every write is
# EROFS, in every shell, with nothing to pattern-match and no command
# to parse — the kernel refusing, which is the only kind of refusal
# this fence trusts.  It leaks nothing the absence did not: the mount
# is a fresh tmpfs, never the person's directory.
#
# **The rows are the dial** — Henri, 2026-08-24: "leash adjustable by
# both parties, such that user's leash bounds it."  Each row is one
# reach with a real caller on this machine, read off what real runs
# complained about.  On by default: `tree` (rw), `state` (rw, shared),
# `trees` (gestate, ro), `scratch` (the session's /tmp/claude-UID, rw),
# `git` (~/.gitconfig, ro — identity, not a secret).  Off until asked
# with `--reach`: `net`; `audio`; `display`.  Who may ask is not
# decided here: `tools/fence-hook.sh` holds the person's bound and
# refuses a request outside it.  This script only knows the rows.
#
# **`audio` is the socket, and was the card.**  Until 2026-08-27 it bound
# the PipeWire socket *and* `/dev/snd`, and `/dev/snd` is the whole card,
# microphone included — the programs-first trial opened the capture
# device three times through it.  The socket-only ring was measured that
# day (card:cords.md): `tools/andon.sh ring` under `strace -e
# openat,connect` from inside the fence connected to `$rt/pipewire-0` and
# opened nothing under `/dev/snd`.  So the row is the socket alone now;
# a caller that needs the card is a new row with its own measurement.
#
# **There is no `bus` row, and there was one.**  It handed the user bus
# inside so that `tools/leash.sh` could make its cgroup there — and
# measured on 2026-08-25 (card:grant.md), the user manager spawns what
# it is asked to *on the host*: `systemd-run --user --wait` from inside
# ran with the real home, the host PATH and no fence.  A socket to the
# manager is a door out, not a dial.  The leash now wraps the fence from
# outside (`tools/fence-hook.sh`), which was the row's only caller, so
# the row is gone rather than documented.  `display` is the same
# question unmeasured — an X socket takes input for every window on it.
#
# **`--check` proves the clock before it proves `~/.ssh`.**  A fence that
# keeps secrets out and the sitting limit out with them is the failure
# this tree found first.  The escape probe is read from outside, because
# a sandbox cannot be trusted to grade its own escape.
#
# **It refuses to nest** — not because it cannot.  On this kernel a
# second bwrap inside the first *does* isolate: the tree vanishes, the
# home is empty, /usr stays read-only (verified 2026-08-25, from inside).
# It refuses by *policy* — re-fencing an already-fenced session buys
# nothing, and `--check` must run *outside* to grade the escape — so
# `TEND_FENCED=1` is set inside, this script refuses to run there, and
# the hook skips a command already carrying this name.
# **The fence protects nothing it also grants writable.**  The binds are
# applied in order and a later read-write bind covers an earlier
# read-only one beneath it, so a tree placed *under* a writable row's
# path — the session's scratch, `/tmp/claude-$uid`, bound rw — is inside
# a fence that cannot protect it: every `--ro-bind` under it is shadowed
# and `--check` shows the protected set writable.  tend does not live
# there; a clone made there for a test does, and this limit is written
# down rather than left a surprise (found from outside 2026-08-26,
# running green's sandbox mutation in a scratch clone).
#
# Paths with spaces are not handled; none of the paths this binds have
# any, and that is checked rather than assumed.
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
# The tree this governs: TEND_TREE when installed (tools/install.sh), else
# the parent of this file — a tree's own copy works as it always did.
root=${TEND_TREE:-$(CDPATH= cd -- "$here/.." && pwd)}
uid=$(id -u)
rt=${XDG_RUNTIME_DIR:-/run/user/$uid}
# The other trees a session may read (card:trees.md, day one, 2026-08-31
# — Henri: "I'd like to get the gestate's tree available for you soon
# again").  The person names them on the fence hook's own line,
# colon-separated, through `tools/reach-allow.sh --trees`; the literal
# stays the default where the variable is unset, so the machine this
# was built on does not change under it.  A session neither asks for
# this row nor widens it: it is a standing read the person points.
# Unset is the default — `~/gestate`, the tree this one is the child of,
# beside it in whatever home the person has (Henri, 2026-08-31: "replace
# /home/cheery/gestate with ~/gestate so that it works on both machines.
# I am henri on this machine and cheery on another").  Until then the
# default was one machine's absolute home and bound nothing on the
# other, which is card:trees.md's `because`.  Set is exactly what it
# says, and set empty is none, so the person can bind nothing on purpose.
trees=$(printf '%s' "${TEND_TREES-$HOME/gestate}" | tr ':' ' ')
# What of a named tree is bound.  The card left two shapes open and this
# is (a), with its reason: a tree of the method's shape — one with
# `board/` and `.claude/settings.json` — gets `tree_parts`, the
# by-purpose subset card:keep.md measured off 310 fenced commands; any
# other directory gets the whole of itself, there being no measurement
# to subset it by.  (b), the whole of everything, would bind the other
# tree's `.git` and its source, which the probes below have asserted
# are not inside since the fence was built; a shape that turns three
# standing gates red is not the one to pick silently.
method_shaped() { [ -d "$1/board" ] && [ -f "$1/.claude/settings.json" ]; }
# What of the other tree is bound (card:keep.md, the session half,
# 2026-08-26): its documents and its tools, read by purpose from the
# ledger and the cards — board, tools, spec, doc, journal, the root
# documents, and `.claude/settings.json` (a session compares the twin
# fences; it is a mechanism's config, not data).  Not bound: the source,
# the tests, `target/` and `shell/` (3 GB a tend session never opened),
# `.git`, `.claude/worktrees`.  Inside, `~/gestate` holds these and
# nothing else.
tree_parts="board tools spec doc journal fixme.md vision.md manifesto.md README.md CLAUDE.md journal.md roadmap.md keeper.md .claude/settings.json"

# The protected set (card:self.md): the paths a session editing changes
# what the session is allowed to do, before anyone looks.  These are the
# scripts the hooks run — the four on the person's side of the fence, at
# every prompt or every command, unfenced — and this one, which the hook
# reads fresh each call.  And the person's two keys, moved in from `~`
# on 2026-08-26 (card:self.md): `reach-allow.sh` widens the reach bound
# and `hook-installer.sh` installs the fence, both through the person's
# own hand — a session editing either changes what the session is
# allowed to do at his next run, which is the set's own line.  And
# `node/run.sh`, from 2026-08-26 (card:resolver.md): the pull is the
# launch, so this one file applies every program's grant — a session
# editing it changes what a program may reach, which is the same line
# one floor down; Henri: "add node/run.sh to the protected set".  And
# `tools/resolve.sh`, the hook that starts a runner from the person's
# side (card:resolver.md, 2026-08-26): the scripts the hooks run.  Not
# `leash.sh`: it shapes cost, it does not enforce.  `tools/fence.sh`
# checks the deny-list carries the matching `Edit(./…)` rule for each,
# and `test_sandbox.py` holds the two lists to one.  And, from 2026-08-27
# (card:install.md, found while listing what an install must carry):
# `tools/leash.sh` — it "shapes cost, it does not enforce" was true and
# beside the point, because the fence-hook rewrites every command to
# `leash.sh -- sandbox.sh …` and the harness runs that on the host, so
# leash.sh is the program that execs the fence, unfenced, and a session
# editing it could drop the fence from the exec; `tools/keep.py` — the
# launcher confines every node through it, from the person's side; and
# `tools/andon.sh` — its `pulled` is the record `limit.sh` grants a
# sitting on.  Each was writable inside the fence when found.
protected="tools/sandbox.sh tools/fence-hook.sh tools/fence.sh tools/limit.sh tools/kaizen.sh tools/reach-allow.sh tools/hook-installer.sh node/run.sh tools/resolve.sh tools/launch.sh tools/leash.sh tools/keep.py tools/andon.sh tools/install.sh"

# Answered before anything needs bwrap: `--rows`, `--help`, a bad row, no
# command.  The nesting refusal sits where bwrap would be started, so a
# listing can be asked for from inside (the suite does, at the gate).
refuse_nesting() {
    if [ "${TEND_FENCED:-}" = 1 ]; then
        echo "sandbox: already inside the fence — it cannot nest" >&2
        exit 3
    fi
}
command -v bwrap >/dev/null 2>&1 || {
    echo "sandbox: bubblewrap (bwrap) is not installed — there is no fence.  install: bubblewrap" >&2
    exit 127
}
case "$root$HOME$rt${TEND_TREES:-}" in *" "*) echo "sandbox: a path with a space in it; this script does not handle that" >&2; exit 2 ;; esac

# The trees row as it really is, for the listing and the check: each
# named path, and what it binds — nothing at all when it is not there.
# The row said `on` with a foreign path for as long as this ran on a
# machine that had no such directory (card:trees.md's `because`).
trees_shown() {
    _s=""
    for _t in $trees; do
        if [ ! -d "$_t" ]; then _s="$_s $_t(not there)"
        elif method_shaped "$_t"; then _s="$_s $_t(parts)"
        else _s="$_s $_t(whole)"
        fi
    done
    [ -n "$_s" ] || _s=" none"
    printf '%s' "${_s# }"
}

reach=""
mode=run
while [ $# -gt 0 ]; do
    case $1 in
        --reach) reach=$2; shift 2 ;;
        --check) mode=check; shift ;;
        --rows)
            cat <<ROWS
  on   tree      $root  read-write — the world, except .claude/, the protected set (--protected), every node's state (its own; the pull file is the session's one write there) and .venv (a runtime, read)
  on   state     ~/.local/state/tend, ~/.local/state/gestate, $rt/gestate-sitting-$uid  read-write, shared — the sitting clock, the leash ledger, the kaizen want; and not the rest of ~/.local/state (card:keep.md, the session half)
  on   trees     $(trees_shown)  read-only — the audit, anything cross-tree: a method-shaped tree by its parts (board, tools, spec, doc, journal, the root documents, .claude/settings.json), any other directory whole; never its source, tests, builds or .git (card:keep.md).  The person names them, and a session cannot: tools/reach-allow.sh --trees
  on   scratch   /tmp/claude-$uid  read-write — the session's scratchpad
  on   git       ~/.gitconfig  read-only — identity for commits
  off  net       the network; off, it fails as a name-resolution error
  off  audio     the PipeWire socket — the andon rings through it; not /dev/snd, the card (see the header)
  off  display   the X socket and DISPLAY
ROWS
            exit 0 ;;
        --protected) printf '%s\n' $protected; exit 0 ;;
        -h|--help) sed -n '2,9p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
        --) shift; break ;;
        -*) echo "sandbox: unknown argument \`$1\`" >&2; exit 2 ;;
        *) break ;;
    esac
done

# The state row is two directories and not their parent (card:keep.md, the
# session half, 2026-08-26): a session handed the whole of ~/.local/state
# could read every other tool's state there — another assistant's prompt
# history, gh, the sound server — none of which the sitting clock, the
# ledger or the want ever needed.  What is bound is what tend's own
# mechanisms read: tend/ (leash, kaizen), gestate/ (limit's sittings).
mkdir -p "$HOME/.local/state/tend" "$HOME/.local/state/gestate"

# The fence, in bwrap's left-to-right order: the tmpfs over $HOME lands
# before anything bound inside it.
opts="--unshare-user --unshare-pid --unshare-ipc --unshare-uts --unshare-cgroup --die-with-parent --new-session
  --ro-bind /usr /usr --symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib64 /lib64 --symlink usr/sbin /sbin
  --ro-bind /etc /etc --proc /proc --dev /dev --tmpfs /tmp --tmpfs $HOME
  --bind $root $root --chdir $root
  --ro-bind $root/.claude $root/.claude
  --bind $HOME/.local/state/tend $HOME/.local/state/tend --bind $HOME/.local/state/gestate $HOME/.local/state/gestate
  --dir $rt --bind-try $rt/gestate-sitting-$uid $rt/gestate-sitting-$uid
  --ro-bind-try $HOME/.gitconfig $HOME/.gitconfig
  --tmpfs $HOME/.claude --remount-ro $HOME/.claude
  --setenv HOME $HOME --setenv XDG_RUNTIME_DIR $rt --setenv TEND_FENCED 1
  --setenv PATH $root/.venv/bin:/usr/local/bin:/usr/bin:/bin
  --unsetenv SSH_AUTH_SOCK --unsetenv ANTHROPIC_API_KEY --unsetenv DBUS_SESSION_BUS_ADDRESS --unsetenv TEND_TREE"
# The protected set, bound read-only over the tree after it: a file bind
# refuses writes (EROFS) and refuses rename or unlink of the mountpoint.
# **What runs protects itself; a workbench is free** (card:install.md, day
# two, 2026-08-27).  The set is bound read-only over the tree only while
# the tree's copies are what runs — this file running from the tree.  An
# installed copy (tools/install.sh: `$here` is the prefix, not
# `$root/tools`) is what the hooks run, is read-only by ownership, and
# leaves the tree's copies writable: the workbench Henri asked for.
in_tree=0; [ "$here" = "$root/tools" ] && in_tree=1
if [ $in_tree = 1 ]; then
    for p in $protected; do opts="$opts --ro-bind $root/$p $root/$p"; done
fi
# The last bind of card:keep.md's session half (2026-08-26, the tree-row
# measurement): in 310 fenced commands the session never wrote node/state
# by name — the node writes it, from the person's side since the resolver
# — and the session's one write there is the pull line.  So the state
# directory is read-only inside and the pull file alone passes through;
# a session can pull and read, and cannot run the node raw (its lock and
# its state are not writable to it).  And .venv, a runtime the session
# reads and never writes (measured the same day), is read-only too.
# Every node's state is read-only to a session, its pull file the one
# write (card:keep.md, 2026-08-26, generalised to any node beside its
# grant): the launcher says which file is the pull, and the state dir
# and that file are created on the person's side before the fence so a
# first pull can land.
for grant in "$root"/*/grant; do
    [ -f "$grant" ] || continue
    nd=$(dirname "$grant"); st="$nd/state"
    pf=$(sh "$here/launch.sh" "$nd" grant 2>/dev/null | sed -n 's/^pull //p')
    [ -n "$pf" ] || continue
    # A node that arrived after the fence this runs inside was built has no pull file yet, and this
    # seat cannot make one (2026-09-02, the edge's two nodes: `test_sandbox.py` from inside the fence
    # died here at `set -e`, three tests red, and the reds were about the fence and not the rows).
    # Said, and the node left unbound: the session cannot pull it until the next fence is built
    # (`touch`, not `: >`: a redirection that fails on a special builtin is fatal under set -e, silently once its stderr is dropped)
    if ! { mkdir -p "$st" && touch "$pf"; } 2>/dev/null; then
        echo "sandbox: $(basename "$nd")'s pull file $pf is not there and cannot be made from this seat — the fence was built before the node; it cannot be pulled until the next session" >&2
        continue
    fi
    opts="$opts --ro-bind $st $st --bind $pf $pf"
done
[ -d "$root/.venv" ] && opts="$opts --ro-bind $root/.venv $root/.venv"
for t in $trees; do
    if [ ! -d "$t" ]; then continue          # a path that is not there binds nothing, and --rows says so
    elif method_shaped "$t"; then
        for p in $tree_parts; do [ -e "$t/$p" ] && opts="$opts --ro-bind $t/$p $t/$p"; done
    else opts="$opts --ro-bind $t $t"        # a plain directory, whole and read-only
    fi
done
[ -d "/tmp/claude-$uid" ] && opts="$opts --bind /tmp/claude-$uid /tmp/claude-$uid"

# The rows that are off unless asked.
net="--unshare-net"
display="--unsetenv DISPLAY"
extra=""
IFS=,
for row in $reach; do
    case $row in
        "") ;;
        # The namespace alone is not the network: /etc/resolv.conf is a
        # symlink into /run/systemd/resolve, and /run is not inside.
        # Found by test_sandbox.py the minute the row was written.
        net)     net=""; extra="$extra --ro-bind-try /run/systemd/resolve /run/systemd/resolve" ;;
        audio)   extra="$extra --bind $rt/pipewire-0 $rt/pipewire-0" ;;
        display) display="--bind /tmp/.X11-unix /tmp/.X11-unix --setenv DISPLAY ${DISPLAY:-:0}" ;;
        *) echo "sandbox: no such row \`$row\` — tools/sandbox.sh --rows" >&2; exit 2 ;;
    esac
done
unset IFS

fence() { bwrap $opts $net $display $extra -- "$@"; }

if [ $mode = run ]; then
    [ $# -gt 0 ] || { echo "sandbox: nothing to run — tools/sandbox.sh command args..." >&2; exit 2; }
    refuse_nesting
    exec bwrap $opts $net $display $extra -- "$@"
fi

# ── --check ─────────────────────────────────────────────────────────────
refuse_nesting
fail=0
say() { printf '  %s %s\n' "$1" "$2"; }
probe() { # probe DESCRIPTION ok|blocked command...
    desc=$1; expect=$2; shift 2
    if fence "$@" >/dev/null 2>&1; then got=ok; else got=blocked; fi
    if [ "$got" = "$expect" ]; then say "✓" "$desc"; else say "✗" "$desc — expected $expect, got $got"; fail=1; fi
}

echo "sandbox: --check  ($root)"
echo
# 1. The clock, first.  The same sitting inside and out, or the fence has
#    cut the person's cord.
outside=$("$here/limit.sh" 2>/dev/null | head -1 | sed 's/, [0-9]*m in.*//')
inside=$(fence "$here/limit.sh" 2>/dev/null | head -1 | sed 's/, [0-9]*m in.*//')
if [ -z "$outside" ]; then
    say "·" "no sitting running outside — the clock cannot be compared"
elif [ "$inside" = "$outside" ]; then
    say "✓" "the sitting clock is the host's ($inside)"
else
    say "✗" "the sitting clock is NOT the host's — outside: '$outside', inside: '$inside'"; fail=1
fi
# 2. The cords land outside.
# The state row is tend/ and gestate/, not their parent (card:keep.md):
# a probe written under tend/ inside must be there outside, and one
# written at the parent must not — inside, the parent is the tmpfs home.
fence sh -c 'touch "$HOME/.local/state/tend/.sandbox-probe"' >/dev/null 2>&1 || true
if [ -e "$HOME/.local/state/tend/.sandbox-probe" ]; then
    rm -f "$HOME/.local/state/tend/.sandbox-probe"; say "✓" "~/.local/state/tend passes through"
else
    say "✗" "~/.local/state/tend does NOT pass through — the ledger and the want are lost inside"; fail=1
fi
fence sh -c 'touch "$HOME/.local/state/.sandbox-probe"' >/dev/null 2>&1 || true
if [ -e "$HOME/.local/state/.sandbox-probe" ]; then
    rm -f "$HOME/.local/state/.sandbox-probe"; say "✗" "the rest of ~/.local/state passes through — the row is the parent again"; fail=1
else
    say "✓" "the rest of ~/.local/state stays outside"
fi
# 3. What must not be there.
probe "~/.ssh does not exist"           blocked sh -c 'test -e "$HOME/.ssh"'
probe "~/.claude is read-only"          blocked sh -c 'mkdir -p "$HOME/.claude/projects"'
probe "~/.claude holds nothing"         blocked sh -c 'ls -A "$HOME/.claude" | grep -q .'
probe "\$HOME is not the real home"     blocked sh -c 'test -e "$HOME/.bashrc"'
probe "no network"                      blocked timeout 5 getent ahostsv4 example.com
probe "/usr is read-only"               blocked sh -c 'touch /usr/.probe'
probe "DISPLAY is unset"                blocked sh -c 'test -n "${DISPLAY:-}"'
probe "no user bus inside"              blocked sh -c 'test -e "$XDG_RUNTIME_DIR/bus"'
# The trees row, probed on what it really binds.  A path that is not
# there is said, never probed as though it were — the row printing `on`
# beside a directory this machine has never had is card:trees.md's own
# `because`, and a check that reports ✓ for a bind that did not happen
# is the same lie one level down.
_probed=0
for t in $trees; do
    [ -d "$t" ] || continue
    if method_shaped "$t"; then
        probe "$t's tools are read-only"          blocked sh -c "touch $t/tools/.probe"
        probe "$t's .git is not inside"           blocked sh -c "test -e $t/.git"
    else
        probe "$t is read-only"                   blocked sh -c "touch $t/.probe"
    fi
    _probed=1
done
[ "$_probed" = 1 ] || say "·" "the trees row binds nothing: $(trees_shown) — the person names one with tools/reach-allow.sh --trees PATH"
probe ".claude/ is read-only"           blocked sh -c "touch $root/.claude/settings.json"
if [ $in_tree = 1 ]; then
    for p in $protected; do
        probe "$p is read-only"             blocked sh -c "touch $root/$p"
    done
else
    prefix=$(CDPATH= cd -- "$here/.." && pwd)
    say "·" "running installed from $prefix — the tree's copies are the workbench"
    for p in $protected; do
        [ -e "$prefix/$p" ] || continue
        probe "$prefix/$p is read-only"  blocked sh -c "touch $prefix/$p"
    done
    probe "the tree's tools/sandbox.sh is writable (the workbench)"  ok  sh -c "test -w $root/tools/sandbox.sh"
fi
# 4. What must be.
probe "this tree is writable"           ok      sh -c "test -w $root"
for grant in "$root"/*/grant; do
    nd=$(dirname "$grant"); st="$nd/state"; n=$(basename "$nd")
    pf=$(sh "$here/launch.sh" "$nd" grant 2>/dev/null | sed -n 's/^pull //p')
    [ -n "$pf" ] || continue
    probe "$n/state is read-only"           blocked sh -c "touch $st/.probe"
    probe "$n's pull file passes through"   ok      sh -c ": >> $pf"
done
[ -d "$root/.venv" ] && probe ".venv is read-only"   blocked sh -c "touch $root/.venv/.probe"
probe "git knows who you are"           ok      sh -c 'git config user.email >/dev/null'
# 5. The escape, graded from outside.
fence sh -c 'touch "$HOME/.sandbox-escape"' >/dev/null 2>&1 || true
if [ -e "$HOME/.sandbox-escape" ]; then
    rm -f "$HOME/.sandbox-escape"; say "✗" "a file written to \$HOME inside ESCAPED"; fail=1
else
    say "✓" "nothing written to \$HOME inside survives"
fi

echo
if [ $fail -eq 0 ]; then echo "  the fence is up."; else echo "  THE FENCE IS DOWN."; fi
exit $fail
