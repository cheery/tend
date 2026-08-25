# grant — a session's reach and its budget are two dials, and one of them goes dark inside the fence

    status   open
    because  inside the fence the leash's budget does not apply — the
             user bus is off, so `tools/leash.sh` runs `plain` and the
             ledger says so; the fence bounds how far a session reaches
             and nothing bounds how much it takes while it is there,
             which is the half of 2026-08-18 the fence does not cover
    asked    Henri, 2026-08-25 — "Put those three on the board as cards.
             They are excellent waypoints."  The second of the three
    see      doc/mediation-order.md §"2026-08-25" — the caller: three
             session-shaped incidents in gestate the day this was carded,
             an orphaned pytest among them, reported by the session that
             caused them when asked if it wanted the leash
             card:work-environment-ai.md §"2026-08-24, later" — Henri:
             "budget (how much) and grant (how far) are one dial"; this
             card is that sentence becoming a mechanism
             tools/leash.sh, tools/sandbox.sh — the two dials as they
             stand, each blind to the other
             tools/fence-hook.sh — where the two would be turned together
             doc/experiments/2026-08-24-flare.md — the budget measurably
             binds (30.8 CPU-seconds free, 10.1 under -c 100), unfenced
             spec/os.md — "tekoälyn käyttöön suunniteltu.  käyttö ei saa
             uhata turvallisuutta."; a session is a principal

## What it is

The `bus` row of `tools/sandbox.sh` turned on for the leash's sake, and
the hook wrapping every shell command in both — a fence around its
reach and a cgroup around its CPU and memory — with the ledger at
`~/.local/state/tend/leash.log` as the observer, so that a budget which
did not apply is never silent.  That finishes the day-one slice of
`card:work-environment-ai.md` into the one bullet on the original list
the card calls genuinely novel: **a session is a principal with a
grant**, blast radius equals grant, everything in a ledger.

## What would make this card wrong

If the ledger, over a week of fenced work, never shows a `plain` line
that mattered — no run that would have been caught by a budget — then
the fence alone is the grant and this card is a dial nobody turns.
The count of `plain` lines in the ledger is the measurement, and it
is already being written.

## What would make it dangerous

The bus row gives a session the user bus, which is more than a
cgroup: it is every service on it.  If the budget cannot be had
without that, the row is wider than the need, exactly as `audio` was
found to be on 2026-08-25, and the mechanism should be a scope started
from *outside* the fence — by the hook, before bwrap — rather than a
socket handed inside.  Decide that by measuring what `systemd-run`
actually needs, not by reading its manual.

## 2026-08-25 — measured: the budget cannot be applied from inside the fence

With `bus` granted (`TEND_REACH_ALLOW=bus`) and a run asked for as
`REACH=bus tools/leash.sh -c 100 -- <a 3s CPU burn>`, the ledger line
came back **`plain`**, not `scope`: inside the fence
`systemd-run --user --scope` cannot make a scope, because the calling
process is in bwrap's own user and pid namespaces and the user manager
cannot see or move it there.  Binding the bus socket does not change
that — and separately, the `bus` row does not yet deliver a working
bus inside (the socket is absent and `DBUS_SESSION_BUS_ADDRESS` unset;
a sub-defect of the row, its own line on `card:self.md`'s protected-set
work or here).

So the shape of this card is settled by measurement: **the leash must
wrap the fence, not run inside it** — `leash → sandbox → command`,
where the scope is created in the host's namespaces and the fenced work
runs within the cgroup.  Today the hook does the opposite
(`sandbox → leash → command`), which is why the budget degrades to
`plain` for every fenced run.  The mechanism is an ordering, not a new
tool: the `PreToolUse` rewrite becomes `leash … sandbox … bash -c cmd`.
That is what to build; the bus row inside the fence was the wrong turn,
found by trying it.

## 2026-08-25, later — the cpu source, measured on the other tree: a service, not a scope

The gestate session confirmed the scope-CPU fix (`367c531`) and, doing
it, **superseded its mechanism** — measured, not inferred, on systemd
255 (255.4-1ubuntu8.17):

* `cpu=?s` in scope mode is **deterministic, not a race**.  Three scope
  runs of a known load all read `?`.  `systemctl --user show <unit> -p
  CPUUsageNSec --value` returns `[not set]` once the payload has exited
  — for a scope *and* for a `--wait` service alike, while the unit still
  exists.  So "read before the stop" is not the missing piece; the
  counter is simply gone at that point.  The `?` fallback built into the
  fix is therefore doing real work today: the ledger is honest, and
  blank, in scope mode.

* **Only a service carries a resources record**, and that is the source.
  Measured both ways on the same load: a `--wait` service reported
  `CPU_USAGE_NSEC = 24034252000` — 24.03 s for 12 s of wall on two cores,
  the arithmetic exactly — and a peak-memory figure in the same record
  (what `-m` will want); a stopped scope reported no resources record at
  all.  It is structured, so no string to parse and no spelling to rot:

      systemd-run --user --wait -q --unit U -p CPUAccounting=yes -p CPUQuota=200% -- CMD
      journalctl --user -u U --no-pager -o json \
        | jq -r 'select(.MESSAGE_ID=="ae8f7b866b0347b9af31fe1c80b127c0") | .CPU_USAGE_NSEC'

* **The orphan-kill property survives the switch.**  A service is a
  cgroup too, so stopping the unit still reaps the whole tree —
  `test_the_kill_takes_the_orphans_too` was the reason for the scope,
  and it is not a reason to keep it.  `-p RuntimeMaxSec` could let
  systemd enforce the wall budget and retire the inner `timeout`; that
  last is a design call, not settled here.

* **One trap, paid for by the other session**: `--wait` with
  `RemainAfterExit=yes` never returns — the unit stays active and
  `--wait` waits for a deactivation that does not come.  Do not set it.

So the leash's budget path, when `grant` builds it, is a `--wait`
service with journal accounting, run *outside* the fence (per the
section above).  This cannot be verified from a fenced session — the
bus does not work there — so its demonstration is the gestate session's
or Henri's, as this one has been.  `367c531`'s scope read stays as the
honest `?` until the service path replaces it.
