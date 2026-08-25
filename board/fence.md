# fence — the deny-list is the only restraint here, and nothing notices when it is gone

    status   open
    because  a session started in tend is restrained by one file it can
             rewrite: `.claude/settings.json` is the whole of it, no
             check reads it back, no test names it, and nothing bounds
             what a program run here can reach — so "the enforcement
             boundary lives outside the session's write access"
             (vision.md, 2026-08-24) is true of gestate sessions and
             not of tend's own
    asked    Henri, 2026-08-25 — "add the fence card to tend", after the
             audit was re-run and this was the one absence on no card
    see      ~/gestate/tools/leash.sh — is the deny-list actually in
             force; the mechanism for the first half
             ~/gestate/tools/sandbox.sh, ~/gestate/spec/sandbox.md —
             the namespace fence, and the two threats kept apart
             ~/gestate/tools/seedaudit.py — calls this piece ABSENT:
             *a session cannot edit its own restraints*
             board/README.md §"What this tree does not have yet" — which
             claimed every absence was carded, and was false by this one
             card:work-environment-ai.md — the budget, grant and
             lifecycle; this is the same problem seen from the restraint
             side rather than the resource side

## Written from outside, 2026-08-25

**A gestate session wrote this card, not a tend one.**  That is worth
saying on the card about the boundary: `~/tend` is outside a gestate
session's write access by construction, and the only reason this file
exists is that Henri asked for it in words, on 2026-08-25, after
reading the audit.  The boundary was crossed the way it is meant to be
— a person opened it for one named thing — and nothing else in this
tree was touched.  Whoever picks the card up should treat the framing
below as a gestate session's reading of tend, borrowed like everything
else here and owed its own demonstration.

## What it is, and it is two halves with different callers

**The integrity half has a caller today.**  `.claude/settings.json`
carries the deny-list — package managers, `sudo`, `ssh`, the credential
paths, `Edit(./.claude/**)` — and the harness enforces it.  What is
missing is the check that the file still says that.  The failure is
silent by construction: a settings file edited down, malformed or
missing does not announce itself; the session starts, the tools work,
and every rule in it is simply not applied.  Gestate answers this with
`tools/leash.sh` on `SessionStart`, checking invariants rather than
bytes, restoring from git and never from a second embedded copy.  Tend
has the file and no reader of it.

**The blast-radius half does not have a caller yet.**  Nothing here
bounds what a program run in this tree can reach — no namespace fence,
no `--check` that proves one is up.  By `manifesto.md` rule 1 that is
not yet work: tend runs its own suite and nothing else, and gestate's
`sandbox.sh` exists because `cargo` executes build scripts and `pytest`
imports what is importable.  **The caller arrives with the first
program tend launches that it did not write** — which is what
`card:work-environment-ai.md` is about, so this half is that card's
neighbour and should be built when it is, not before.

Tend needs *a* fence, not that fence.  What transfers is the property:
a restraint that can say when it is off, and a bound on reach that a
session cannot widen for itself.

## The name is already taken

`tools/leash.sh` means two different things in the two trees: in
gestate it is the restraint-integrity check, here it is the
per-invocation budget runner (`-t`, `-c`, `-m`).  Whoever moves the
integrity check across cannot bring its name with it, and a person
reading both trees will be misled until one of them is renamed.  Decide
that before the mechanism travels, not after it has been cited.

## What would make this card wrong

If the harness's deny-list turns out to be unbypassable from inside a
session — including by a shell command that rewrites the file — then
the integrity half has no failure to catch, and this card is one
`SessionStart` line away from being a nuisance rather than a
protection.  **That is a measurement, not an opinion**, and it is the
first thing the card owes: try to edit the deny-list from inside a tend
session by each route (the edit tools, `sed`, a heredoc, `jq`), and
write down which ones the harness stops.  **Gestate has not measured
that either**, and it is worth being exact about what its answer
actually is: `leash.sh` exists there because the *file* failing is
silent — missing, malformed, edited down — which is a different failure
from a session rewriting it on purpose, and the deny-list's own
`Edit(./.claude/**)` rule covers the edit tools and says nothing about
a shell.  Borrowing that conclusion instead of running the check is
exactly what `manifesto.md` §"How a practice gets adopted" says this
tree may not do, and the check is cheap: it is one session and five
attempts.

## The demonstration owed

Per `manifesto.md`: whoever brings a practice owes *this is what it
caught, that you would have shipped.*  For this card that is a leash
that goes red on a settings file with one rule removed, shown once
before the check is trusted — the same shape as `card:gates.md`'s hook
refusing a commit on the day it was installed.
