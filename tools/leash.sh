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
# epoch, seconds, exit, budget, command — appended to
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
how="plain"
if systemd-run --user --scope -q true >/dev/null 2>&1; then
    how="scope"
fi

start=$(date +%s)
rc=0
if [ "$how" = "scope" ]; then
    # **The kill takes the whole scope, not the direct child.**  Found
    # while planning the first real run, 2026-08-24: `timeout` signals
    # only the process it started, so a killed `suite.py` would have
    # left its fenced pytest running on — an orphan, which is the
    # twelve-polling-shells shape of the incident this exists for.  A
    # scope is a cgroup, so stopping the unit reaps everything in it.
    unit="tend-leash-$$-$start"
    if [ -n "$m" ]; then
        systemd-run --user --scope -q --unit "$unit" -p TimeoutStopSec=10 \
            -p "CPUQuota=${c}%" -p "MemoryMax=$m" \
            timeout -k 10 "$t" "$@" || rc=$?
    else
        systemd-run --user --scope -q --unit "$unit" -p TimeoutStopSec=10 \
            -p "CPUQuota=${c}%" \
            timeout -k 10 "$t" "$@" || rc=$?
    fi
    systemctl --user stop "$unit.scope" >/dev/null 2>&1 || true
else
    # Plain mode kills only the direct child — an orphan a command
    # leaves behind outlives its budget here.  The ledger's `plain` is
    # what says this gap was in force.
    nice -n 10 timeout -k 10 "$t" "$@" || rc=$?
fi
end=$(date +%s)

# Never fatal: a ledger that can take the work down with it is worse
# than a gap in the ledger.
{ mkdir -p "$(dirname "$LOG")" &&
  printf '%s\t%s\t%s\t%s\t%s\n' \
      "$start" "$((end - start))" "$rc" "t=$t c=${c}% m=${m:--} $how" "$*" \
      >> "$LOG"; } 2>/dev/null || true

[ "$rc" -eq 124 ] && echo "leash: the ${t}s budget is spent — a hang is a crash." >&2
exit "$rc"
