#!/bin/sh
#: asked-by: Henri, 2026-08-19 — "work environment+AI, composed with later goal to implement OS into it"
#
# tools/leash.sh — run one invocation under a budget, and leave a line behind.
#
#     tools/leash.sh [-t SECONDS] [-c CPU%] [-m BYTES] [--] command args...
#
#     -t   wall-clock budget; past it the command is killed (default 900)
#     -c   CPU budget as a percentage, 100 = one core (default: half the
#          machine's cores)
#     -m   memory ceiling, systemd sizes: 2G, 500M (default: none)
#
# **The day-one slice of `card:work-environment-ai.md`**: the
# supervised, budgeted runner for one principal's invocations — a
# session's suite runs, cargo, and polling loops.  The caller is
# measured, and it is in another tree: on 2026-08-18 a session ran a
# full fenced suite, cargo, two X servers and twelve polling shells on
# the machine Henri was listening on, the audio tore, and it was
# diagnosed as hardware first (~/gestate/journal/2026-08.md §"And what a
# session costs the machine").  A defect is always a caller.
#
# **Supervised**: a hang is a crash — the wall-clock budget is enforced
# by `timeout`, and exit 124 is the leash saying so.  **Budgeted**:
# where a systemd user manager is running, the command runs in its own
# scope with CPUQuota (and MemoryMax if asked), which is a real cgroup
# limit and needs no root; where there is none it degrades to
# `nice`+`timeout` and the ledger says `plain`, because a budget that
# silently did not apply is worse than none (`vision.md`: nothing
# unexpected silently).
#
# **The ledger** is one tab-separated line per invocation —
# epoch, seconds, exit, budget, cpu, command — appended to
# `~/.local/state/tend/leash.log` (override: TEND_LEASH_LOG).  Outside
# the repository because when the machine was busy is the machine's
# business, not the tree's; plain because you must be able to read it
# without tend.  It is the observer the mediation-order measurement
# found missing: a zero incidents claim with no ledger behind it decides
# nothing (doc/mediation-order.md).
#
# **The defaults are numbers picked in the writing** — 900 s and half
# the cores — and nobody has checked them.  The ledger is what settles
# them, the same way gestate's sittings.log settles its GAP_MIN; until
# then treat a surprising kill as a fault in the default before a fault
# in the command.
#
# This is not the fence (`tools/sandbox.sh`, still absent here) and not
# the broker: it grants nothing and denies nothing.  It only makes an
# invocation's cost bounded and visible.  Capabilities bolt on later —
# `card:work-environment-ai.md` §"Day one, whichever way it goes".
set -eu

LOG="${TEND_LEASH_LOG:-$HOME/.local/state/tend/leash.log}"

# **The inner half of scope mode: the process that reads the counter is
# inside the scope, after the work and before its own exit.**  Measured
# 2026-08-25 (card:grant.md): `CPUUsageNSec` is `[not set]` the moment
# the scope's last process is gone — read from the caller, after
# `systemd-run` returns, it is always gone; read from inside, by the
# shell that ran the work, it is the number (3000085000 for a 3s burn).
# Not a race, a boundary.  So the scope runs this script again with
# `--inner`, which runs the work under `timeout`, writes the scope's own
# tally to a file the outer half is holding, and exits with the work's
# code.  Never a user-facing form; the outer half is the interface.
if [ "${1:-}" = --inner ]; then
    acct=$2; unit=$3; t=$4; shift 4
    rc=0
    timeout -k 10 "$t" "$@" || rc=$?
    systemctl --user show "$unit" -p CPUUsageNSec --value > "$acct" 2>/dev/null || true
    exit "$rc"
fi

cores=$( (command -v nproc >/dev/null 2>&1 && nproc) || echo 2 )
t=900
c=$((cores * 50))
m=""

usage() { sed -n '4,12p' "$0" | sed 's/^# \{0,1\}//' >&2; }

while [ $# -gt 0 ]; do
    case "$1" in
    -t) t="$2"; shift 2 ;;
    -c) c="$2"; shift 2 ;;
    -m) m="$2"; shift 2 ;;
    --) shift; break ;;
    -h|--help) usage; exit 0 ;;
    -*) echo "leash: unknown option \`$1\`" >&2; usage; exit 2 ;;
    *)  break ;;
    esac
done
if [ $# -eq 0 ]; then
    echo "leash: no command to run" >&2; usage; exit 2
fi

# The budget applies or the ledger says it did not — probed per
# invocation, because the user manager can be there in the morning and
# gone after a logout.
# The clock starts before the probe: on 2026-08-26 a runner's ledger line
# *started* ten seconds after the command that launched it, because the
# probe below took that long from cold and the stamp came after it — so
# the ledger's wall was the command's and not the invocation's.  What the
# leash costs is part of what the leash reports (card:resolver.md 15:12).
start=$(date +%s)
how="plain"
if systemd-run --user --scope -q true >/dev/null 2>&1; then
    how="scope"
fi

rc=0
if [ "$how" = "scope" ]; then
    # **The kill takes the whole scope, not the direct child.**  Found
    # while planning the first real run, 2026-08-24: `timeout` signals
    # only the process it started, so a killed `suite.py` would have
    # left its fenced pytest running on — an orphan, which is the
    # twelve-polling-shells shape of the incident this exists for.  A
    # scope is a cgroup, so stopping the unit reaps everything in it.
    unit="tend-leash-$$-$start"
    # **The CPU figure is the cgroup's own, read from inside the scope
    # by `--inner` (top of this file).**  `times` (below, for plain mode)
    # accounts only for this shell's waited-for children — and in scope
    # mode the work is a child of the user manager, not of this shell, so
    # `times` sees the `systemd-run` client and not the suite: cpu=1.3s
    # for a 25-minute run, found by the leash's first outside user on
    # 2026-08-25.  The first fix read the counter here, after the scope
    # returned, and got `?` every time: the counter is gone with the
    # scope's last process.  Empty or the uint64 "not set" sentinel still
    # becomes `?` below — an honest gap, never `times`'s wrong number.
    acct=$(mktemp 2>/dev/null || echo /dev/null)
    if [ -n "$m" ]; then
        systemd-run --user --scope -q --unit "$unit" -p TimeoutStopSec=10 \
            -p CPUAccounting=yes -p "CPUQuota=${c}%" -p "MemoryMax=$m" \
            sh "$0" --inner "$acct" "$unit.scope" "$t" "$@" || rc=$?
    else
        systemd-run --user --scope -q --unit "$unit" -p TimeoutStopSec=10 \
            -p CPUAccounting=yes -p "CPUQuota=${c}%" \
            sh "$0" --inner "$acct" "$unit.scope" "$t" "$@" || rc=$?
    fi
    cpu_ns=$(cat "$acct" 2>/dev/null || true)
    [ "$acct" != /dev/null ] && rm -f "$acct"
    systemctl --user stop "$unit.scope" >/dev/null 2>&1 || true
else
    # Plain mode kills only the direct child — an orphan a command
    # leaves behind outlives its budget here.  The ledger's `plain` is
    # what says this gap was in force.
    nice -n 10 timeout -k 10 "$t" "$@" || rc=$?
fi
end=$(date +%s)

# **A load is a number.**  2026-08-24: a run of gestate's suite beside
# cargo was believed heavy because it was real, and it was a minute of
# near-idle.  So every line says what the invocation cost in CPU seconds
# — and where the number comes from depends on how the budget applied,
# because the two modes put the work in different places.
cpu="?"
if [ "$how" = "scope" ]; then
    # The cgroup's own tally, read above.  `?` when it could not be had —
    # the scope torn down before the read, or accounting off — which is
    # honest where `times` here would be the 1.3s lie.
    case "${cpu_ns:-}" in
        ''|*[!0-9]*|18446744073709551615) : ;;
        *) cpu=$(awk -v n="$cpu_ns" 'BEGIN{ printf "%.1f", n/1000000000 }') ;;
    esac
else
    # Plain mode: the command is a true child, so the shell's own account
    # of waited-for children is right.  `times` to a file because a pipe
    # or `$( )` would fork, and a fork's account starts at zero.
    acct=$(mktemp 2>/dev/null || echo "")
    if [ -n "$acct" ]; then
        times > "$acct"
        cpu=$(tail -1 "$acct" | awk '{ split($1,u,"m"); split($2,s,"m");
                                       printf "%.1f", u[1]*60+u[2]+s[1]*60+s[2] }')
        rm -f "$acct"
    fi
fi

# Never fatal: a ledger that can take the work down with it is worse
# than a gap in the ledger.
{ mkdir -p "$(dirname "$LOG")" &&
  printf '%s\t%s\t%s\t%s\t%s\t%s\n' \
      "$start" "$((end - start))" "$rc" "t=$t c=${c}% m=${m:--} $how" \
      "cpu=${cpu}s" "$*" \
      >> "$LOG"; } 2>/dev/null || true

# 124 is `timeout`'s code, and the command's own `timeout` says it too:
# a 3s inner burn read as "the 900s budget is spent" on 2026-08-25.  The
# budget is spent only if the clock agrees.
[ "$rc" -eq 124 ] && [ $((end - start)) -ge "$t" ] && echo "leash: the ${t}s budget is spent — a hang is a crash." >&2
exit "$rc"
