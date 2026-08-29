#!/bin/sh
#: asked-by: Henri, 2026-08-26 — "do the grant beside the program" (board/keep.md, board/resolver.md: what the second program earns)
#
# tools/launch.sh — one launcher for any node; the grant is a file beside the program.
#
#     tools/launch.sh NODE run            run the program under its grant; 75 while a runner holds the lock
#     tools/launch.sh NODE pull [text]    a pull: one line appended to the pull file — inside the fence that
#                                         is all (the resolver starts the runner from the person's side);
#                                         from a person's shell a runner is started if none is up
#     tools/launch.sh NODE status         running or not, the last pull, the last stop, the log's tail —
#                                         or the grant's own `status` line, under the grant
#     tools/launch.sh NODE grant          what the grant becomes: keep's flags, and the program line
#     tools/launch.sh NODE check          is it installed?  each thing the grant names, checked against
#                                         this machine, nothing run — the program's binary, every path,
#                                         the model, the state, the port, keep's boundary; exit 1 on any ✗
#     tools/launch.sh NODE serve           start a runner IF a pull is unserved and none is up, else nothing —
#                                          what the resolver calls for each node, from the person's side
#
# NODE/grant — one word and its value per line, paths relative to NODE:
#     allow PATH        readable
#     allow-try PATH    readable where it exists; where it does not, said and not refused — a machine's
#                       runtime in a tracked grant (the fence's --ro-bind-try, as a grant word; 2026-08-28)
#     write PATH        writable (the state directory always is)
#     bind PORT         one TCP port to listen on, and no other bind, no connect anywhere
#     no-net            no TCP at all
#     idle SECONDS      stop when nothing has pulled for this long (default 30; TEND_IDLE overrides)
#     pulse FILE        a file whose mtime is the program's activity — for a program that cannot stop
#                       itself, the launcher watches this and stops it on idle
#     sitting MINUTES   a sitting has a length: the runner is stopped when it is up, however busy the
#                       program is — the person's clock, not the program's (TEND_SITTING overrides,
#                       in minutes).  Absent, the node is a program; present, it carries the first cord
#     pull FILE         the file a pull appends to (default $STATE/pull)
#     program CMD...    what runs, under the grant.  Lines may use $NODE, $STATE, $IDLE and $MODEL
#     status CMD...     what says what it did (optional; run read-only under the grant)
#     make PATH         a directory made before the program runs, under $STATE unless absolute — for a
#                       cache the program will not create for itself (the GPU driver's, 2026-08-28)
#     env NAME=VALUE    exported to the program before keep execs it; $NODE, $STATE and $MODEL expand — for a
#                       runtime's cache under $STATE, which keep already lets it write (2026-08-28)
#
# **Why a file and not a launcher per program** (2026-08-26): the first
# node's grant was three flags in `node/run.sh`, and the second node's
# day one measured that a server's whole grant is three lines too — the
# model, its state, its port.  A grant that lives beside the program is
# read by one launcher and served by one resolver, and adding a node is
# adding a directory.  The grant is still applied from outside the
# program (Rule 1) and can only narrow (keep).  The state directory is
# read-only to a session inside the fence, its pull file the one write
# (`tools/sandbox.sh`), so a session can pull and read and cannot run.
#
#     $MODEL   the first *.gguf under NODE/model, if any — a model is data the
#              person brings; its name is never in the tree
#     $STATE   NODE/state, or TEND_STATE_DIR (tests point it at a scratch dir)
#
# **The sitting** (2026-08-27, board/session-program.md — day one: one
# cord on the llm node, shown to hold).  `idle` is the program's
# lifecycle: it stops when nothing pulls.  `sitting` is the person's
# clock: it stops when the minutes are up, pulled or not, the way
# `tools/limit.sh` ends a hosted sitting — and a node with no `sitting`
# line is a program, not a session.  The length is declared at the door,
# in the grant beside the program, which the program cannot write (keep
# hands it its model and its state and nothing else); so a node may end
# its sitting early — idle — and can never extend one, the asymmetry
# `test/test_limit.py` holds for the hosted session.  A pull's text is
# never read as a grant: `pull sitting 90` is a line in the pull file
# and nothing more.  The stop is a close, not a crash — exit 0, the
# reason written into `$STATE/stopped` and the log — where the leash's
# wall budget is a crash (exit 124); a sitting longer than that budget
# is cut by the leash first, and sizing the budget is `grant`'s dial,
# not this word's (doc/kaizen/2026-08-25-1436.md, item 2).  Nothing here
# touches the person's own clock (`~/.local/state/gestate/sittings.log`):
# a node's sitting is the node's, kept in its state directory.
#
# **The heartbeat** (2026-08-28, board/session-program.md §09:37: "a
# runner can be alive and not watching").  On the work laptop a runner
# wrapped in strace overran its sitting by 25 minutes: the loop set the
# stop, `kill` could not end the tracer, and the shell hung at `wait`
# with the lock held while `status` read "running" — the cords were
# checked by nothing.  Now the watch loop touches `$STATE/watch` every
# tick and writes the program's pid to `$STATE/run.pid`; `status`,
# `check` and `serve` read a held lock with a heartbeat older than
# TEND_WATCH_STALE (default 60 s) as "the cords are cut", and `serve` —
# the resolver's side, the person's — kills the program so the runner's
# `wait` returns and the lock frees.  And the stop itself no longer
# trusts TERM: after TEND_KILL_WAIT (default 10 s) it escalates to KILL,
# says so in the log, and still closes as a sitting, exit 0.
#
# **The death notice** (2026-08-29, card:canvas.md day two — drafted by
# Opus 5 from the card's `because`, proposals/compare/2026-08-28-1835-
# claude-opus-5.md, landed at Henri's "land it").  2026-08-28, 13:27:
# `pull` said "started llm" and the runner died a second later at the
# loader, and the fact lived in `$STATE/stopped` and nowhere the person
# looks.  A non-zero exit now appends one line to the andon record on
# the person's side — `<epoch> <stamp> <name>: exited <rc> — <what it
# last said>` in `${TEND_ANDON_STATE:-~/.local/state/tend}/andon.log`,
# the file tools/andon-panel.py reads — from this stop path and nowhere
# else: the record's shape is tools/andon.sh's, `pull` does not write
# it, the panel does not, and a zero exit (idle, the sitting, a program
# that finished) writes nothing.  It replaces the one-second watch
# `pull` kept from 13:45 to 2026-08-29 (`died_at_once`: it caught the
# failure that happened and no slower one, and cost every healthy pull
# a second — the window Henri named as one "we will eventually revert").
set -u
here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
# The tree this governs: TEND_TREE when installed (tools/install.sh), else
# the parent of this file — a tree's own copy works as it always did.
root=${TEND_TREE:-$(CDPATH= cd -- "$here/.." && pwd)}
[ $# -ge 2 ] || { sed -n '4,10p' "$0" | sed 's/^# \{0,1\}//' >&2; exit 2; }
NODE=$(CDPATH= cd -- "$1" 2>/dev/null && pwd) || { echo "launch: no such node directory: $1" >&2; exit 2; }
verb=$2; shift 2
name=$(basename "$NODE")
[ -f "$NODE/grant" ] || { echo "launch: $name has no grant — $NODE/grant is the file beside the program that says what it may reach" >&2; exit 2; }
STATE="${TEND_STATE_DIR:-${TEND_NODE_STATE_DIR:-$NODE/state}}"
py=/usr/bin/python3; [ -x "$py" ] || py=$(command -v python3) || { echo "launch: no python3 for keep" >&2; exit 127; }
MODEL=""; for m in "$NODE"/model/*.gguf; do [ -e "$m" ] && { MODEL=$m; break; }; done
export NODE STATE MODEL

flags="--write $STATE"; program=""; status_cmd=""; pulse=""; pullfile=""; idle_grant=""; sitting_grant=""; paths=""; port=""; envs=""; makes=""
while IFS= read -r line || [ -n "$line" ]; do
    case "$line" in ''|'#'*) continue ;; esac
    key=${line%% *}; val=${line#* }; [ "$val" = "$line" ] && val=""
    case "$key" in
        allow|allow-try|write) case "$val" in /*) ;; *) val="$NODE/$val" ;; esac; flags="$flags --$key $val"; paths="$paths $key=$val" ;;
        bind)        flags="$flags --bind $val"; port=$val ;;
        no-net)      flags="$flags --no-net" ;;
        idle)        idle_grant=$val ;;
        pulse)       eval "pulse=\"$val\"" ;;
        sitting)     sitting_grant=$val ;;
        pull)        eval "pullfile=\"$val\"" ;;
        program)     program=$val ;;
        status)      status_cmd=$val ;;
        make)        case "$val" in /*) ;; *) val="$STATE/$val" ;; esac; makes="$makes $val" ;;
        env)         case "$val" in [A-Za-z_]*=*) envs="$envs $val" ;; *) echo "launch: $name/grant: env wants NAME=VALUE, got \`$val\`" >&2; exit 2 ;; esac ;;
        *) echo "launch: $name/grant: unknown word \`$key\`" >&2; exit 2 ;;
    esac
done < "$NODE/grant"
IDLE="${TEND_IDLE:-${TEND_NODE_IDLE:-${idle_grant:-30}}}"; export IDLE
SITTING="${TEND_SITTING:-$sitting_grant}"; sitting_s=""
case "$SITTING" in
    "") ;;
    *[!0-9.]*|.|"") echo "launch: $name/grant: sitting wants minutes, got \`$SITTING\`" >&2; exit 2 ;;
    *) sitting_s=$(awk "BEGIN { print int($SITTING * 60) }") ;;
esac
[ -n "$program" ] || { echo "launch: $name/grant has no program line" >&2; exit 2; }
# the grant's env lines, exported once here so run, status (under keep) and check all see one expansion
for e in $envs; do eval "export $e"; done
case "$pullfile" in "") pullfile="$STATE/pull" ;; /*) ;; *) pullfile="$STATE/$pullfile" ;; esac
case "$pulse" in ""|/*) ;; *) pulse="$STATE/$pulse" ;; esac
lock="$STATE/run.lock"
# the log's last line that is not warning noise — what a program said as it died
last_said() { grep -iv 'deprecationwarning\|^ *class \|^$' "$STATE/log" 2>/dev/null | tail -1; }
stale="${TEND_WATCH_STALE:-60}"
# seconds the watcher has been silent while a runner holds the lock — empty when the cords are fine
cut_for() {
    flock -n "$lock" true 2>/dev/null && return 1
    [ -f "$STATE/watch" ] || return 1
    _s=$(( $(date +%s) - $(stat -c %Y "$STATE/watch") ))
    [ "$_s" -ge "$stale" ] || return 1
    echo "$_s"
}
cut_line() { echo "$name: runner up, watcher silent $(( $1 / 60 )) min — the cords are cut (a held lock and a stale $STATE/watch; \`serve\` kills it)"; }

case "$verb" in
grant)
    echo "keep $flags"; echo "program $program"; [ -n "$pulse" ] && echo "pulse $pulse"; echo "pull $pullfile"; echo "idle $IDLE"
    for e in $envs; do echo "env $e"; done
    [ -n "$sitting_s" ] && echo "sitting $SITTING min"
    exit 0 ;;
check)
    # An install test that runs nothing (card:node-install.md): the grant
    # read as `run` reads it, and each thing it names checked against the
    # machine.  Inside the fence a session may read, so it may ask this.
    fail=0
    ok()  { printf '  ✓ %s\n' "$1"; }
    bad() { printf '  ✗ %s\n' "$1"; fail=1; }
    echo "check: $name  ($NODE)"
    ok "grant parses; $(echo "$flags" | wc -w | tr -d ' ') keep words"
    eval "set -- $program"; prog=$1
    bin=""
    case "$prog" in
        /*) if [ -x "$prog" ]; then ok "program $prog"; bin=$prog; else bad "program $prog is not there or not executable"; fi ;;
        *)  if found=$(command -v "$prog" 2>/dev/null); then ok "program $prog → $found"; bin=$found
            else bad "program \`$prog\` is not on PATH — tools/toolbox.sh says what the tree wants; this is $name's own"; fi ;;
    esac
    # Present is not loadable.  The work laptop, 2026-08-28: the check said
    # ✓ on a llama-server whose Intel-LLVM build wanted libsvml.so from a
    # oneAPI the fence cannot see, and the binary could not start.  ldd
    # reads what the binary names against the loader's view — with this
    # shell's LD_LIBRARY_PATH, which is the check's seat and may not be the
    # runner's — and none of the program runs.  A script or a static
    # binary has nothing to read and gets no line.
    if [ -n "$bin" ] && command -v ldd >/dev/null 2>&1 && deps=$(ldd "$bin" 2>/dev/null) && [ -n "$deps" ]; then
        missing=$(printf '%s\n' "$deps" | awk '/not found/ { print $1 }' | sort -u | tr '\n' ' ')
        if [ -n "$missing" ]; then bad "program $bin cannot load — not found by the loader: $missing(ldd; the library is $name's own need, not the tree's)"
        else
            # Found by the loader is not readable under keep: Landlock lets the
            # program read beneath keep's SYSTEM_READ and the grant's allow/write
            # paths and nowhere else.  The work laptop, 2026-08-28, second face:
            # the check said "loads" from a shell whose LD_LIBRARY_PATH reached
            # a oneAPI runtime in the person's home, where keep would not.
            sysread=$("$py" -c "import sys; sys.path.insert(0, '$here'); import keep; print(' '.join(keep.SYSTEM_READ))")
            grantread=""
            for kv in $paths; do v=${kv#*=}; v=$(readlink -f "$v" 2>/dev/null || echo "$v"); grantread="$grantread $v"; done
            outside=""
            for lib in $(printf '%s\n' "$deps" | awk '$3 ~ /^\// { print $3 }'); do
                real=$(readlink -f "$lib" 2>/dev/null) || real=$lib; inside=0
                for root in $sysread $grantread; do case "$real" in "$root"/*) inside=1; break ;; esac; done
                [ $inside -eq 1 ] && continue
                dir=$(dirname "$real"); case " $outside " in *" $dir "*) ;; *) outside="$outside $dir" ;; esac
            done
            outside=${outside# }; [ -z "$outside" ] || outside="$outside "
            if [ -z "$outside" ]; then ok "program loads — every shared library it names is found, where keep lets it read"
            else bad "program loads for you, and keep would refuse it — shared libraries outside the grant, under: $outside(an \`allow\` line for the directory, or the runtime where keep's SYSTEM_READ looks)"; fi
        fi
    fi
    for kv in $paths; do
        k=${kv%%=*}; v=${kv#*=}
        if [ -e "$v" ]; then ok "$k $v"
        elif [ "$k" = allow-try ]; then printf '  · %s\n' "$k $v is not here — keep grants it where it is, and this machine has not got it"
        else bad "$k $v does not exist — the grant names it and keep would hand the program a path that is not there"; fi
    done
    for e in $envs; do nm=$(printf '%s' "$e" | cut -d= -f1); v=$(printenv "$nm"); ok "env $nm=$v"; done
    for m in $makes; do if [ -d "$m" ]; then ok "make $m"; else printf '  · %s\n' "make $m is made by run"; fi; done
    case "$program $status_cmd" in
        *'$MODEL'*) if [ -n "$MODEL" ]; then ok "model $MODEL"
                    else bad "no *.gguf under $NODE/model — the program line uses \$MODEL, and the model is data the person brings (never in the tree)"; fi ;;
    esac
    # Inside the fence the state directory is read-only to a session by
    # design (tools/sandbox.sh: the pull file is the one write) and the
    # runner writes it from the person's side — found by the check's own
    # first run on the real nodes, 2026-08-28: a ✗ that was the fence.
    if [ -d "$STATE" ]; then
        if [ -w "$STATE" ]; then ok "state $STATE is writable"
        elif [ "${TEND_FENCED:-}" = 1 ]; then printf '  · %s\n' "state $STATE is read-only to a session (the fence); the runner writes it from the person's side — not checked from here"
        else bad "state $STATE is not writable by you — the runner writes its log, lock and stop there"; fi
    elif mkdir -p "$STATE" 2>/dev/null; then ok "state $STATE (created)"
    else bad "state $STATE cannot be created"; fi
    if silent=$(cut_for); then bad "$(cut_line "$silent")"; fi
    if [ -n "$port" ]; then
        if ! flock -n "$lock" true 2>/dev/null; then ok "bind $port — $name is running and the port is its"
        elif "$py" -c 'import socket,sys; s=socket.socket(); s.bind(("127.0.0.1", int(sys.argv[1])))' "$port" 2>/dev/null; then ok "bind $port is free"
        else bad "bind $port is in use by something that is not $name's runner"; fi
    fi
    # keep itself, with this grant, confining `true`: not the node's program,
    # and the one measurement of whether the boundary can be built here —
    # keep refuses rather than run unconfined, and says why (the ABI it needs).
    if why=$("$py" "$here/keep.py" $flags -- true 2>&1); then ok "keep confines with this grant here (true ran under it)"
    else bad "keep refuses this grant here — $name would not run: $(printf '%s' "$why" | tail -1)"; fi
    echo
    if [ $fail -eq 0 ]; then echo "  installed: $name can run under its grant on this machine."
    else echo "  NOT installed — the lines marked ✗ say what."; fi
    exit $fail ;;
run)
    mkdir -p "$STATE"
    # the lock is taken here and inherited through keep's exec; a short wait,
    # not a refusal at once — the resolver tests the lock by taking it for a
    # moment (card:resolver.md 15:12)
    exec 9>>"$lock"
    flock -w 2 9 || { echo "launch: a runner already holds $lock — pull $name instead." >&2; exit 75; }
    rm -f "$STATE/stopped"
    for m in $makes; do mkdir -p "$m"; done
    eval "set -- $program \"\$@\""   # the grant's program line, then whatever run was given
    began=$(date +%s); why=""
    busy=$began; prev_ticks=0; clk=$(getconf CLK_TCK 2>/dev/null || echo 100)
    if [ -n "$pulse" ] || [ -n "$sitting_s" ]; then
        # a program that cannot stop itself, or one with a sitting: run it, watch it, stop it —
        # the sitting is read first, because the person's clock outranks the program's pulse
        "$py" "$here/keep.py" $flags -- "$@" >> "$STATE/log" 2>&1 &
        pid=$!
        echo "$pid" > "$STATE/run.pid"
        while kill -0 "$pid" 2>/dev/null; do
            sleep 1
            now=$(date +%s)
            touch "$STATE/watch"   # the heartbeat: this loop is alive and watching
            if [ -n "$sitting_s" ] && [ $(( now - began )) -ge "$sitting_s" ]; then
                why="sitting: the $SITTING minutes of $name are up (from $(date -d "@$began" +%H:%M); the length is $name/grant's)"; break
            fi
            # CPU progress is activity too.  The work laptop, 2026-08-28, 07:50: llama-server
            # loaded its model, then compiled its GPU kernels for 45 s with no log line — busy on a
            # core, silent on its pulse — and was stopped for idleness mid-compile.  A program that
            # used at least half a core in the last second is busy, whatever its pulse says.
            ticks=$(awk '{ print $14 + $15 + $16 + $17 }' "/proc/$pid/stat" 2>/dev/null || echo "$prev_ticks")
            [ $(( ticks - prev_ticks )) -ge $(( clk / 2 )) ] && busy=$now
            prev_ticks=$ticks
            if [ -n "$pulse" ]; then
                last=$(stat -c %Y "$pulse" 2>/dev/null || echo "$began")
                [ "$last" -lt "$began" ] && last=$began
                if [ $(( now - last )) -ge "${IDLE%.*}" ] && [ $(( now - busy )) -ge "${IDLE%.*}" ]; then
                    why="idle: nothing has pulled $name for ${IDLE}s"; break
                fi
            fi
        done
        if [ -n "$why" ]; then
            echo "launch: $why — stopping it" >> "$STATE/log"; kill "$pid" 2>/dev/null
            # a close is asked for once; a program that does not take it is ended — the
            # tracer that would not die (2026-08-28) left this shell at wait for 25 minutes
            _w=0; while kill -0 "$pid" 2>/dev/null && [ "$_w" -lt "${TEND_KILL_WAIT:-10}" ]; do sleep 1; _w=$((_w + 1)); done
            if kill -0 "$pid" 2>/dev/null; then
                echo "launch: $name did not stop on TERM in s — killing it" >> "$STATE/log"; kill -9 "$pid" 2>/dev/null
            fi
        fi
        wait "$pid"; rc=$?; [ "$rc" -eq 143 ] && rc=0
        [ -n "$why" ] && rc=0   # the stop was the launcher's, a close: not the program's exit
        rm -f "$STATE/watch" "$STATE/run.pid"
    else
        "$py" "$here/keep.py" $flags -- "$@" >> "$STATE/log" 2>&1; rc=$?
    fi
    [ -n "$why" ] || why="exited $rc: $name stopped by itself"
    echo "$why" > "$STATE/stopped"   # its mtime is the last stop (serve, status); its line is why
    if [ "$rc" -ne 0 ]; then
        # the death notice (card:canvas.md, day two): one line in the andon record on the person's
        # side, the record's own shape (tools/andon.sh `note`), so a death and a cord pull are one
        # timeline.  The runner appends; nobody else; a clean stop writes nothing; a record that
        # cannot be written never fails the stop
        _a="${TEND_ANDON_STATE:-$HOME/.local/state/tend}"; _t=$(date +%s); _said=$(last_said)
        { mkdir -p "$_a" && printf '%s %s %s: exited %s%s\n' "$_t" "$(date -d "@$_t" '+%Y-%m-%d %H:%M')" \
            "$name" "$rc" "${_said:+ — $_said}" >> "$_a/andon.log"; } 2>/dev/null || true
    fi
    exit "$rc" ;;
pull)
    [ -d "$STATE" ] || mkdir -p "$STATE" 2>/dev/null || true
    printf '%s %s\n' "$(date +%s)" "$*" >> "$pullfile" || { echo "launch: cannot append to $pullfile" >&2; exit 1; }
    if [ -n "${TEND_FENCED:-}" ]; then
        echo "launch: pull recorded — inside the fence the runner is the resolver's to start (tools/resolve.sh --hook)" >&2
    elif flock -n "$lock" true 2>/dev/null; then
        setsid -f sh "$0" "$NODE" run >/dev/null 2>&1 </dev/null
        n=0; while flock -n "$lock" true 2>/dev/null && [ "$n" -lt 600 ]; do sleep 0.05; n=$((n + 1)); done
        echo "launch: started $name (idle ${IDLE}s); it stops by itself when pulls stop" >&2
    fi
    exit 0 ;;
status)
    if flock -n "$lock" true 2>/dev/null; then echo "$name: not running"
    elif silent=$(cut_for); then cut_line "$silent"
    else echo "$name: running"; fi
    [ -f "$pullfile" ] && echo "last pull: $(tail -1 "$pullfile" | cut -d' ' -f1 | xargs -I{} date -d @{} '+%F %T' 2>/dev/null)"
    [ -f "$STATE/stopped" ] && echo "last stop: $(date -r "$STATE/stopped" '+%F %T')$(head -1 "$STATE/stopped" | sed 's/^./ — &/')"
    if [ -n "$status_cmd" ]; then
        eval "set -- $status_cmd"; "$py" "$here/keep.py" $flags -- "$@"
    elif [ -f "$STATE/log" ]; then
        tail -5 "$STATE/log" | sed 's/^/  /'
    fi
    exit 0 ;;
serve)
    # the resolver's per-node decision, on the person's side: a pull is
    # unserved when the pull file is newer than the last stop (or there is
    # no stop yet); start one runner only then, and only if none is up.
    # An mtime rule, not a served-count, so it holds for any program — a
    # server has no tally (board/resolver.md, the grant beside the program).
    # first, a runner whose cords are cut: the person's side is free to kill it
    if silent=$(cut_for); then
        pid=$(cat "$STATE/run.pid" 2>/dev/null)
        echo "launch: $(cut_line "$silent")" >> "$STATE/log"
        if [ -n "$pid" ] && kill -9 "$pid" 2>/dev/null; then
            echo "launch: $(cut_line "$silent") — killed $pid" >&2
        else
            echo "launch: $(cut_line "$silent") — no pid to kill; the lock's holder is yours" >&2
        fi
        exit 0
    fi
    [ -f "$pullfile" ] || exit 0
    if [ -f "$STATE/stopped" ] && [ ! "$pullfile" -nt "$STATE/stopped" ]; then exit 0; fi
    flock -n "$lock" true 2>/dev/null || exit 0
    setsid -f sh -c "exec '$here/leash.sh' -- sh '$0' '$NODE' run" >> "$STATE/log" 2>&1 </dev/null
    n=0; while flock -n "$lock" true 2>/dev/null && [ "$n" -lt 600 ]; do sleep 0.05; n=$((n + 1)); done
    echo "launch: $name had an unserved pull and no runner — started one (under the leash); $STATE/log" >&2
    exit 0 ;;
*) echo "launch: unknown verb \`$verb\` — run, pull, status, grant, check, serve" >&2; exit 2 ;;
esac
