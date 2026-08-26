# work-environment-ai — sessions and programs run on this machine with no budget, no grant and no lifecycle

**Moved here 2026-08-24, from `~/gestate/board/later/`, where it was
shelved on a decision.**  The decision was taken on the week's evidence
— sessions first — and this repository is the answer to the card's own
"against": *the enforcement boundary must live outside the session's
write access or it is decoration.*  A workspace built inside gestate is
inside the write access of every gestate session.  This one is not.
The copy in gestate stays shelved and points here, so that citations
to `card:work-environment-ai.md` there keep resolving.

    status   open
    because  "we are missing a way to work with each other" (vision.md,
             2026-08-16) — sessions and programs run on this machine
             with no budget, no grant and no lifecycle; one already
             degraded the machine being listened on (2026-08-18)
             before anybody saw it, and it was diagnosed as hardware
             first
    asked    Henri, 2026-08-19 — "work environment+AI, composed with
             later goal to implement OS into it"
    see      vision.md §"Gestate as a lean vehicle" — the `because`
             spec/author.md — the review volume this is downstream of
             board/README.md §"Question it into existence" — how the
             sixteen-item list became one card
             card:working-standard.md, card:project-seed.md — the
             method half; this is the vessel half

**Written outside the tree** by a session, from a conversation on
2026-08-19, and brought in on 2026-08-20 at Henri's ask.  Everything in
his words is marked so; the rest is the session's, and by the
elaboration rule it is **suspected** — including the architecture below,
which is the part a reader is most likely to trust and the part most
likely to be wrong.

## The ask, verbatim

> C option. AI native sounds like sense. But there's also that "try
> things out" -angle and self-reliance on concepts I gave. I know that
> you sessions have odd notion of time. Your ten years is two months
> realtime. So I think that work environment+AI, composed with later
> goal to implement OS into it would be the proposal.

The original list (2026-08-19, Finnish, sixteen items; in the tree as
`spec/os.md` since 2026-08-25) is the property
sheet this card descends from: easy install and test, secure by design,
verified by types and model checkers, config recorded in the program
node, pull-based reconfiguration, decentralized versioning, Linux
compatibility, state persistence, crash-don't-hang, compiler
localization, hard to attack, AI-native, pull lifecycle, no silent
errors, own language (per arXiv:1507.05762), encrypted disk;
bootstrapped in Python and Rust.

## How the reading was chosen

The list as written was not a card: nearly every bullet named a fix and
none named a problem, which fails the board's first gate.  Four readings
were offered, each with what would kill it:

* **A. A real OS, kernel up** — killed by `vision.md`'s *"any project
  must not consume the person leading it"*, by one reviewer, and by the
  prior-art graveyard (Fuchsia: a decade, hundreds of engineers; Midori:
  shipped nothing).
* **B. A Linux distro with these properties** — Nix + CRIU + capability
  broker on a stock kernel.  Survives everything except *secure from the
  kernel up*; the TCB stays Linux, mitigated.
* **C. Gestate's method applied to a working environment** — sealed,
  testable, state-carrying, capability-scoped execution for AI-written
  programs.  Killed only if the goal is genuinely to boot metal.
* **D. A research programme, not a product** — killed by *"my friend
  could use it as well"*.

**Henri chose C, with the OS as a later goal layered on top.**  Which
gives the card a `because` traceable to `vision.md` without strain:
*"I'd like to use gestate as a vehicle to find out how to utilise AI
well… What we are missing is not better AI or higher capacity.  We are
missing a way to work with each other."*

## Two corrections carried from the review

**The time argument is half right.**  Sessions compress *production* —
typing is nearly free, and proof engineering that once took twenty
person-years would go much faster.  What does not compress is the
author's share: `spec/author.md` already measured 270 commits in nine
days outrunning review, and wrong-direction risk lives in the seams —
names, interfaces, contracts, refusals — which no session accelerates.
The consumption rule binds attention, not calendar.  Environment-first
is right partly because it keeps the seam count low enough for one
reviewer.

**Self-reliance on concepts is fine; self-reliance on lessons is
expensive.**  Rebuild the concepts; read the post-mortems first.  Why
Nix chose content addressing, why EROS and Phantom found that
persistence resurrects bugs, why every powerbox looks the same.  A day
of reading against months of rediscovery.  Borrow the scars, not the
code.

## The architecture, in dependency order

*Suspected, as above.*  Userspace on Linux, inside or beside gestate,
bootstrapped in Python and Rust.

**1. The node.**  A program is a content-addressed bundle: code plus its
configuration recorded in the node, so pull-reconfiguration is
re-fetching by identity, and decentralization falls out because identity
is the hash.  Install = fetch; test = run the node's own suite; a node
carrying no suite is refused — *"won't ever be untested"* applied at the
boundary.

**2. The supervisor.**  Erlang semantics: a crash is fine, a hang is a
crash (timeout), a crash-loop gets backoff and an andon light, never
silence.  Pull lifecycle: a node nobody pulls is stopped.  The measured
caller is in this tree — the 2026-08-18 audio-crackle incident, where a
session running the suite, cargo, two X servers and a dozen polling
loops degraded the machine being listened on.  A defect is always a
caller.

**3. The capability broker.**  No ambient authority; a node gets file
and network handles only by explicit grant, and the picker click *is*
the grant (the powerbox pattern: Genode, Capsicum, Fuchsia).  This
answers open problem 1 below, which turns out not to be an open problem
but the first architecture decision.  It is also the entire content of
*AI-native*: **a session is a principal** — scoped capabilities, a
CPU/IO/audio budget, everything observable and replayable.  Blast radius
equals grant.  The one genuinely novel bullet on the original list.

**4. State — explicit, not memory images.**  Checkpoint/restore
persistence collides with two vision lines: *"won't trap your work —
plain files you can read without it"*, and *"won't ever do anything
unexpected silently"*.  A resurrected image resurrects yesterday's bug
and yesterday's config without a trace (EROS and Phantom both hit this),
and a memory image is a dump full of secrets under the encryption
bullet.  Instead: a node serializes its state explicitly to a plain,
inspectable file, and *opens where it left off* means restoring from
that.  CRIU stays in the pocket as a later latency optimisation for
pull-shutdown, not as the state model.

**The OS-later discipline.**  The environment's contract — node format,
capability verbs, supervisor protocol — lives in `spec/`, kept narrow,
so what is underneath stays replaceable.  *Implement an OS into it* then
means swapping Linux out from under a contract that already has users.
If the contract sprawls, the OS phase is dead regardless of intent.

**The language is deferred, deliberately.**  The environment needs none
of it, gestate already has a language, and the LP-IR paper
(arXiv:1507.05762 — deterministic, single-moded logic programs as a
compilation IR; note it designs an IR, not a surface language) becomes
relevant only at the OS phase, if ever.

## Answers to the original open problems

1. **User data against programs** — capabilities plus powerbox, decided
   by piece 3 above.  Everything else is downstream of it.
2. **Program protection and install** — content-addressed, signed store;
   pull = fetch by hash.  A solved problem, of the Nix/OSTree shape.
3. **Speed against immediate shutdown** — answered by explicit state:
   shutdown = serialize, launch = restore, and the question collapses to
   restore latency, which is measurable (CRIU and Firecracker-class
   restores run roughly 100–300 ms).

## The open decision

*Mediation order.*  The broker and supervisor govern **principals** —
things that act.  This machine has two kinds: **sessions**, and
**programs** (gestate nodes: instruments, pieces, tools a person runs).
Enforcement cannot be built for both at once; one goes first and the
other runs ungoverned for months.

**Sessions first** — the broker's first subject is the session itself:
every tool call (cargo, the suite, X servers, polling loops, file
writes) runs through the runner with a budget and a grant, visible in
the andon.

* *For:* the caller already exists — the audio-crackle incident and the
  review volume are both session-shaped defects; immediate relief on
  what hurts now; it is the novel *AI-native* piece; and a grant model
  designed against the messiest workload trivially covers programs.
* *Against:* hardest case first, so the first version is wrong in more
  ways before it is right; nothing a gestate user meets improves for
  months, which the board's impact ordering demotes; and the governed
  party would be building its own cage — **the enforcement boundary must
  live outside the session's write access or it is decoration.**
  *Partly answered already, 2026-08-20:* `tools/sandbox.sh`'s deny-list
  blocks a session's own `sudo` and its own leash, and `.claude/` is
  outside a session's write access — enforcement outside the governed
  party's reach, working on this machine today (`spec/sandbox.md`).  So
  the cage-builder problem is not unsolved here; it is unsolved *at this
  granularity*.

**Programs first** — the broker mediates gestate nodes: an instrument
gets audio-out and its own state file, nothing else.  Sessions stay
ungoverned.

* *For:* the easy case, with narrow predictable needs, so a clean small
  capability model arrives fast; it is exactly the OS-later contract
  (nodes, grants, pull lifecycle); and a person using gestate feels it,
  which scores higher on the board's impact ordering.
* *Against:* it solves a problem that has not happened — no node has
  hurt anybody and sessions have, twice, measured; the vocabulary risks
  being too small for sessions, forcing a redo; and the actual risk, an
  ungoverned agent with the whole tree writable, continues meanwhile.

### It is open, and it is to be decided by evidence

*Henri, 2026-08-20: the order is an open question and should be settled
by measurement, not by argument.*

A session did recommend sessions-first here, on the board's rule that a
defect is always a caller.  **That recommendation is withdrawn as a
basis for deciding**, for a reason worth keeping rather than tidying
away: the session making it **is the governed party**.  A session's read
on how far it should be trusted is not neutral in either direction — it
can be self-serving, and it can as easily be self-flagellating, which
reads as humility and is exactly as useless as evidence.  The argument
stays on the card because it is a real argument; it is no longer the
answer.

And when the question was put plainly — *is this for my safety?* — the
three things bundled under "sessions first" came apart, which is itself
the finding:

* **the machine is shared** — the audio-crackle incident, measured;
* **you cannot see what happened** — 270 commits in nine days outrunning
  review, measured;
* **containment** — scoped capability, and **no incident behind it.**

The first two are the callers, and they are what settles the **order**.

**But containment is not the same kind of question, and Henri corrected
the framing on 2026-08-20:** *"I put the fence up to protect everybody
involved.  sessions and me alike.  Mistakes happen and they can be
costly."*  So it is not a defence against a session's intent — it is
blast-radius limitation against an ordinary mistake, and it protects the
session as much as the author: work that cannot be reached cannot be
destroyed, and a boundary a session cannot cross is one it cannot be
blamed for or steered into crossing.

Which means **incident-counting is the wrong instrument for that third
piece.**  What it guards is the rare expensive mistake, and counting
rare events after the fact is a measurement that arrives too late by
construction.  The right question for containment is not *has it
happened* but *how far would it reach* — the same question already
answered once at a coarser grain by `tools/sandbox.sh`.  Evidence
settles the order; blast radius settles the scope.

### What would decide it

Cheap, in roughly this order, and none of it needs the broker built:

**1. Count the incidents, both kinds.**  `fixme.md` and `journal.md`
already hold them.  How many measured incidents were session-shaped, and
how many program-shaped?  **And the caveat is half the measurement:** if
nothing in this tree would have *seen* a program misbehaving, a zero is
a fact about the instruments and not about the programs — see
`journal.md` §"Kaizen, 2026-08-19 — the instruments found everything and
the tests found none of it".  A count with no observer behind it decides
nothing.

**2. Try the program vocabulary on the session's needs, on paper.**
Write the grants a real gestate node wants — audio out, its own state
file — and then the grants a real session wants: spawn `cargo`, write
the tree, open an X display, ring the sound card.  If the node
vocabulary cannot spell the session's list, programs-first forces the
redo its *Against* column names, and that is established in an afternoon
with no code.

**3. Then it may not be a decision at all.**  The day-one slice below is
reversible and measurable, and by `doc/memory/decisions-arrive-shaped.md`
that makes it an **experiment**, not a decision: build it for one
principal, see whether it catches the case that already happened, keep
or revert.  A reversible choice with a cheap measurement should never
cost the author a decision.

**Day one, whichever way it goes**, so that this is not a decision
wearing a card forever: build the supervised, budgeted runner for one
principal's invocations — for a session, that is the suite, `cargo` and
the polling loops — visible in the andon.  Smallest slice, real caller;
capabilities, nodes and pull bolt onto it later.

## 2026-08-24 — the two cheap measurements are taken, and day one is built

`doc/mediation-order.md` holds both: the incident count (2
session-shaped, 0 program-shaped, with the observer caveat read both
ways) and the vocabulary trial on paper (the node's three static nouns
cannot spell *exec with inherited budget*, which is every line of the
session's list; the session vocabulary covers the node's as a
degenerate case).  The order question now has its evidence; the
settlement stays Henri's.

The day-one slice is `tools/leash.sh` with `test/test_leash.py`:
wall-clock kill, cgroup CPU quota where a systemd user manager runs, a
plain ledger at `~/.local/state/tend/leash.log`, and the ledger says
`scope`/`plain` so a budget that did not apply is never silent.  First
real line in the ledger is this tree's own suite.  Per
`~/gestate/doc/memory/decisions-arrive-shaped.md` it is an experiment:
keep or revert on whether a leashed suite run leaves the underrun
counter quiet where 2026-08-18's unleashed one made it flare — not run
yet, so the leash is tolerated, not owned.  "Visible in the andon"
waits on `card:cords.md`, which is what the ledger-not-lamp shape is
for now.

The card stays open: the broker, the supervisor's Erlang half, nodes
and pull are all still absent, and the mediation-order decision is
still to be made — now on evidence instead of argument.

## 2026-08-24, later — the leash is one dial, held by two hands

Henri, the same afternoon, on who the leash is for:

> Caller of leash could be all parties.  Sessions, and people.
> Sessions want that the working environment limits how far things
> break if something goes terribly wrong, people want safety for their
> files and work.  I think that leash should be adjustable, based on
> how far the session must reach.

And on who adjusts it:

> Leash could be adjustable by both parties, such that user's leash
> bounds it.  Bit like a safety harness but also a constraint.  Yeah,
> no vocabulary yet.

**Read by the session as:** budget (*how much*) and grant (*how far*)
are one dial, reach; the person sets an outer bound and a session may
tighten inside it and never loosen past it — the sitting limit's
asymmetry again, applied to reach.  Both parties are callers of the
same mechanism for different reasons: bounded blast radius for the
session, files outside the radius for the person.  **No vocabulary
yet** is the instruction: the reach table gets written from what a
real run under bwrap complains about, not designed first.

**The experiment ran, and could not be scored.**
`doc/experiments/2026-08-24-flare.md`: five loads, none made the card
run dry; the 2026-08-18 case no longer happens on demand, because the
suite is a minute now and not twenty-five.  What the day did buy: the
budget measurably binds (30.8 CPU-seconds free, 10.1 under `-c 100`),
and the kill now takes the orphans too — found on the run's doorstep,
which is the polling-shell shape of the incident.  The leash stays
tolerated, not owned, and its criterion is now Henri's *how far would
it reach* rather than *did it flare*.

**And a constraint on the vocabulary, from Henri's kaizen the same
evening** (`doc/kaizen/2026-08-24-1549.md`): *anything mechanically
error-correctible is in domain*, so the reach table must not be
programming-shaped in what it *covers*.  A leash that knows `cargo`
and `pytest` and nothing else would encode the first domain's accidents
as the environment's vocabulary.  When the table is written from what
a real run complains about, the runs should include something that is
not a suite.  Henri's correction the same night: *"in some sense it
needs to be programming a bit"* — programming stays the medium; the
table is written and read by programs and a session programs the
environment it works in.  What must not be programming-shaped is the
set of things it can say, not the way it says them.

## 2026-08-25 — the reach table's first draft, from what real runs complained about

Per the section above, the table was not designed: thirteen real
invocations ran under a bubblewrap fence with only this tree writable,
and `doc/experiments/2026-08-25-reach.md` records each exit code and
complaint, with the fence beside it as a script.  Tend's whole suite
passes fenced (104 passed, 1 skipped — the systemd gap, which says so).
The fence needed no setup: gestate's AppArmor profile for `bwrap` is
already on this machine.

**The finding that could not have been designed on paper**: inside
the fence, `tools/limit.sh` reported *"sitting started 06:44, 0m in,
15m left of 15"* — a fresh clock.  A fence that hides `~/.local/state`
and `/run/user` defeats the sitting limit, loses the leash ledger and
silences a kaizen want.  So the state directory is the first row of
any reach table here, read-write and shared, or every cord and lamp
tend has is decoration the moment a session runs fenced.  The fence
and the person-facing pieces are one design.

**Seven reaches**, each with a caller on this machine: this tree (rw);
the state directory (rw, shared, must be on); the user bus (for the
budget; without it the leash says `plain`); other trees (ro, named);
audio out (the andon); a display (the 2026-08-18 incident); the
network (off, and it should fail as a refusal, not DNS).  Henri's
"user's leash bounds it" reads onto this directly: the person sets
which rows may be on, a session turns on fewer, never more.  *The
table is the session's reading and is suspected; the complaints are
the evidence.*

**Not built, on purpose.**  The table is for Henri to read first.  What
would be built first is not a vocabulary but one bind — the state
directory — and it belongs to whatever fence tend gets, which
`card:fence.md` says arrives with the first program tend runs that it
did not write.  Until then the mediation-order decision is still his,
and the card stays open.

## 2026-08-25 — Henri, on what the count cannot show, and a decision to try both

Henri, on reading the evidence above:

> I've seen you do very well and avoid the most expensive mistakes,
> but those are rare by definition.

Read by the session as the containment argument, put from his side: a
session's good conduct — including the same morning's, when it proved
`python3 -c` goes through the deny-list and did not use it — is one
session on a good day, reported by the governed party, and the mistake
containment exists for is the one nobody notices in the fifth hour.
The count settles the order; it was never going to settle *whether*,
and the shape of the risk already has.

And then, rather than settling the order on paper: *"Could we in any
way examine both options?  You're really fast and everything is maybe
reversible."*  So both are to be tried, set-based, each as an
experiment under `doc/experiments/` and not as a tool: **sessions
first** — the session's real work under a fence with the reach
table's rows, the state-directory bind in and a `--check` that the
clock is the host's; **programs first** — a real gestate node under a
fence with only its three nouns.  Each records what it complained
about, and the comparison is his to read.

**Both tried, the same hour** — `doc/experiments/2026-08-25-both.md`,
with a fence script for each beside it.  Sessions-first: the morning's
fence plus the state directory passed through and gestate read-only;
the sitting clock is the host's inside it, the ledger and a kaizen
want reach the outside, the suite passes, gestate's audit reaches
tend, nothing escapes — zero complaints.  Programs-first: gestate's
andon under exactly its three nouns; it rendered, it rang — and traced,
the `/dev/snd` grant opened the hardware past PipeWire and the
capture device with it.  "Audio out" is not a noun the kernel has.
The two fences are one script with different rows on, and the node
ran under a fence the session wrote: the order question is now *which
principal gets a caller outside the session's write access first*,
and for sessions that caller is a hook, which is Henri's to install.
The record states what kills each; the reading is the session's.

**The hook is built** (`tools/sandbox.sh`, `tools/fence-hook.sh`, the
same evening) — the first caller outside the session's write access,
and installing it is Henri's, with `~/hook-installer.sh`.  The
mediation-order decision is therefore being taken by trial, not on
paper: sessions first, because that is the principal that had a
caller today; programs follow under the same fence with fewer rows
when `cords` brings the andon here.  Reversible in one settings line.

**2026-08-25, evening — the incident count moves to 5–0**, and the
leash has its first outside user: a gestate session, asked by Henri
whether it wanted tend's leash, named three session-shaped incidents
of its own that day and adopted the leash as shell discipline for the
ledger's sake (`doc/mediation-order.md` §"2026-08-25").  Its request
for the non-decorative version — a hook that wraps long runs, Henri's
to install — is `card:grant.md`, which now cites it as the caller.

**2026-08-25 — the leash's cpu column was wrong in scope mode, and its
first outside user found it.**  A gestate session ran tend's leash on
its full suite and read the ledger: `cpu=1.3s` for a twenty-five-minute
CPU-bound run.  The cause is in `tools/leash.sh`: the figure came from
`times`, the shell's account of its *own* waited-for children, and in
scope mode the work is a child of the user manager, not of the shell —
so `times` measured the `systemd-run` client, not the suite.  Fixed to
read the scope's own cgroup tally (`CPUUsageNSec`) before the unit is
stopped, falling to an honest `?` rather than a wrong number when it
cannot be had; `times` stays for plain mode, where the command is a
true child and the account is right.  `test_leash.py::
test_scope_mode_counts_the_work_not_the_wrapper` guards it.  **The
demonstration is owed outside the fence**: from a fenced session the
bus is off and every run is plain, so the scope path — that
`CPUUsageNSec` reads the right number and does not race the scope's
teardown to empty — has not been run here.  It needs one run with a
user manager, which is the gestate session's own case, or a session
here once `TEND_REACH_ALLOW` carries `bus`.  *The leash's first outside
invocation found a defect in the leash, which is the ledger existing
doing its one job.*

**And the scope path could not be demonstrated from inside the fence**
(2026-08-25, with `bus` granted): the leash stayed `plain`, because
`systemd-run --user --scope` cannot make a scope inside bwrap's
namespaces.  So the cpu fix's scope branch is still owed a real run —
which is an unfenced one, i.e. the gestate session's next leashed suite
— and `card:grant.md` gains its true shape from the same measurement:
the leash wraps the fence, it does not run inside it.

## 2026-08-26, 13:45 — the scope path's real run has been happening for a day, and the ledger is the demonstration

Henri: *"work-environment-ai."*  The card's last section owed "the cpu
fix's scope branch a real run — an unfenced one."  `done/grant.md` gave
the leash its true shape the same afternoon: **the leash wraps the
fence**, so every shell command a tend session runs is the unfenced
scope case, and the ledger has been recording it since
`2026-08-25 07:17:53`.  Read back today, by record (a record starts
with an epoch and a tab; a command's text spans lines):

    240 records · 236 scope · 4 plain
    149 of 236 scope records carry cpu > 0; 4 carry no cpu field
    exits: 226 × 0 · 4 × 124 (the wall budget fired) · 3 × 2 · 3 × 1
    the largest: cpu=106.1s over 139s wall (a python heredoc)
    a gate run this sitting: 97s wall, cpu=23.3s
    scope records with wall ≥ 3s and cpu=0: one, and it was a sleep loop

So `CPUUsageNSec` reads a real number and does not race the scope's
teardown to empty — 149 times, on work as heavy as the suite.  The
owed run is not owed; it is a day of ledger.  And the wall budget has
killed four times, which is the "bounded and visible" the leash was
built for, each a line a person can read.

**What this does not settle**: the mediation-order decision, which
§"Henri, on what the count cannot show" left as "try both," is still
his; and the ledger counts a session's *commands*, not what a program
started by a pull costs — the runner `node/run.sh pull` starts lives
inside the pull's command (`board/resolver.md`), so today it is inside
the same line, and a program that outlived a command would not be.  The
card stays open.

**2026-08-26, 15:12 — a cost of the leash's scope path, measured on
Henri's seat**: starting a command through `systemd-run --user --scope`
took ~10 s from cold, twice in a row, then milliseconds for the next
nine (leash ledger, 15:10:06 → 15:10:27; the resolver's runners).  From
a fenced seat the leash is `plain` and never shows it.  Not a defect of
the leash — the ledger is what made it visible — but a number the
budget defaults did not know: an invocation's wall clock can carry ten
seconds that are the manager's, not the command's.  Measured once;
`time tools/leash.sh -- true` twice on his seat after a quiet minute
would say whether it is the first call or every cold one.

**15:24 — corrected by Henri's measurement.**  `time tools/leash.sh --
true` twice on his seat: **75 ms and 85 ms.**  So the ten seconds is not
the scope path's price; it sat *before* the leash stamped its clock —
the probe (`systemd-run --user --scope -q true`) ran first, `start`
came after — which is why the ledger showed a late start and not a
long wall.  Not reproduced by hand; located by the stamp's position.
Fixed the same hour: the clock starts before the probe
(`tools/leash.sh`, `test_the_wall_clock_includes_the_leashs_own_probe`,
a row), so whatever the probe costs from cold is in the ledger the
next time it happens instead of being a runner that "started late."
The cost of the leash is part of what the leash reports.
