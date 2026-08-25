# grant — a session's reach and its budget are two dials, and one of them goes dark inside the fence

    status   open
    because  inside the fence the leash's budget does not apply — the
             user bus is off, so `tools/leash.sh` runs `plain` and the
             ledger says so; the fence bounds how far a session reaches
             and nothing bounds how much it takes while it is there,
             which is the half of 2026-08-18 the fence does not cover
    asked    Henri, 2026-08-25 — "Put those three on the board as cards.
             They are excellent waypoints."  The second of the three
    see      card:work-environment-ai.md §"2026-08-24, later" — Henri:
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
