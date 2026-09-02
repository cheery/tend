# session-program — a node tend runs is a program, not a session, until it carries the cords

    status   doing
    because  the grant half of "a session is a program" is built: any
             node runs under one boundary — budget, grant, lifecycle —
             and adding one is adding a directory (card:keep.md,
             card:resolver.md, the grant beside the program).  But the
             llm node, the first program that is not the node, has no
             sitting limit, no lamp, no way to reach the person — so it
             is a program, not a session, and nothing here makes a node
             into the thing a person is on the other end of.  Henri, on
             the mediation order: the session's program differs from an
             ordinary one in that it "must have certain things in it" —
             the cords — "and must be able to refine its scope while
             staying under the scope where it is" (the second half is
             built; this card is the first)
    asked    Henri, 2026-08-26 — "open the cords card for the session's
             program"
    see      card:work-environment-ai.md §"2026-08-26, 15:45" — the
             frame: one boundary, the session's program a program that
             carries the cords and attenuates; §"16:38" — the second
             node's loop, and "the model has no limit, lamp or andon, so
             it is a program, not a session"
             card:cords.md — the two cords gestate has and tend built
             for its own sessions (the sitting limit installed, the
             andon blocked until 2026-08-31); this card is where they
             become a node's, not only a hosted session's
             card:keep.md, card:resolver.md — the grant, launcher and
             resolver a node already runs under; the cords hang beside
             them in the same grant file
             ~/gestate/tools/andon.sh, ~/gestate/tools/limit.sh — the
             mechanisms; the audit calls both absent here

## What it is

A node runs under keep, the leash and the launcher: it is bounded,
budgeted and lifecycled.  What it does not have is the person-facing
half — the three things that exist because someone is on the other end
of a session and not of an ordinary program:

* **a limit** — a sitting has a length, and a node that is a session
  must stop when the person's hours are spent, the way `tools/limit.sh`
  stops a hosted session.  The llm node stops on *idle*, which is the
  lifecycle; a sitting limit is the person's clock, not the program's.
* **a lamp** — a session ends with a kaizen; a node that is a session
  owes the same account of what it did, and nothing lights when it does
  not.  `tools/kaizen.sh` is the hosted session's; a node's is unbuilt.
* **the andon** — a session that hits a question it cannot answer must
  reach the person rather than guess or stop silently (`card:cords.md`).
  A node that is a session needs the cord more than a hosted one does,
  because no person is watching its transcript.

## What would make this card wrong

If no node tend runs is ever a *session* — if every program it runs is
the node's shape, a thing with no person on the other end — then the
cords belong to the hosted session alone and a node needs none of them.
But the frame Henri named (card:work-environment-ai.md, 15:45) is that
a local model *is* a session — `claude` or `llama.cpp`, pulled, under
the same boundary — and the moment tend runs one to lead the work
rather than to answer a curl, it is a session with no cords, which is
the exact hole `cords` names for the hosted case, one level in.

## What it must not become

The whole cords built three ways at once, or the hosted session's
mechanisms copied into a node on their say-so (the manifesto forbids
it).  This card owes the first small thing: one of the three, on the
llm node, shown to hold — most likely the limit, because it exists for
tend already (`tools/limit.sh`) and a node's sitting is a measurable
thing (its pulls, its runtime, in the state the launcher already
keeps).  The lamp and the andon are downstream, and the andon leans on
`cords`, which waits until 2026-08-31.

## Where it sits

Placed by a session on 2026-08-26 at Henri's ask, below the build
cards and above the count-only ones — the grant half it completes is
`keep`/`resolver`, both closed for the one program; this is the half
those cards named and did not build.  The placing is the session's; the
tiebreak is Henri's, and this is his to move.

## Next in line — Henri, 2026-08-26, for 2026-08-27

Henri named this the next card: the cords on a node come first tomorrow.
Alongside it, "examine that session as a principal thing a bit" —
`card:work-environment-ai.md` §"the toolbox idea" holds the seed and its
flaws.  Day one stays as §"What it must not become" set it: one of the
three cords on the llm node, most likely the limit, shown to hold — not
all three, not the hosted mechanisms copied on their say-so.

## 2026-08-27 — the limit, on the llm node: a grant word, shown to hold, waiting on Henri's apply

Henri: *"start on session-program, the limit on the llm node."*  Built
and measured; not yet in the tree, because `tools/launch.sh` is in the
protected set and a session cannot write it.  **`sitting.patch` at the
tree root** carries the whole of it — the launcher, one line in
`llm/grant`, five tests — and Henri's two lines are `git apply
sitting.patch` and `python3 tools/suite.py`.  (`*.patch` is gitignored;
the patch is handoff, not tree.)

**What it is.**  A grant word: `sitting MINUTES`, beside `idle` in the
grant beside the program.  `idle` is the program's lifecycle — it
stops when nothing pulls; `sitting` is the person's clock — the
launcher stops the runner when the minutes are up, pulled or not, the
way `tools/limit.sh` ends a hosted sitting.  The reason is written
into `$STATE/stopped` (whose mtime `serve` and `status` already read)
and the log, and `status` shows it.  A node with no `sitting` line is
a program, as the card's title says; `llm/grant` gets `sitting 10`,
so the llm node is the first node that carries a cord.

**Measured**, on a patched copy of the launcher, from inside the
fence, `TEND_SITTING=0.1 TEND_IDLE=60`: the server loaded in 1 s,
answered a chat request ("I'm ready to"), and was stopped at 6 s — its
pulse fresh, idle nowhere near — exit 0, the port closed, `stopped`
reading *"sitting: the 0.1 minutes of llm are up (from 05:32; the
length is llm/grant's)"*.  The five tests pass against that copy
(17 in `test_launch.py`, 12 before); they are red against the tree's
launcher until the patch lands, which is why they travel in the patch
and not in a commit.

**The decisions, each one small.**  (1) *The door is the grant, not the
pull.*  The hosted limit takes its length from a word Henri types; a
node's pull is the one thing a session writes, so a pull's text is
never read as a grant — `pull sitting 900` is a line in the pull file
and nothing more, and a test holds it.  That is `test_limit.py`'s
asymmetry on a node: a node may end a sitting early (idle) and can
never extend one (keep hands it its model and its state; the grant is
not in its write).  (2) *A close, not a crash.*  The sitting exits 0
with a reason; the leash's wall budget exits 124 with none.  A sitting
longer than the leash's 900 s is cut by the leash first, and sizing
the budget is `grant`'s dial (doc/kaizen/2026-08-25-1436.md item 2),
not this word's — so `sitting 10` sits under it.  (3) *Ten is a number
picked in writing*, like `idle 60` and the leash's 900; the log and
`stopped` are what settle it.  (4) *The person's clock is untouched.*
"One desk, one clock" is about `~/.local/state/gestate/sittings.log`,
which is Henri's; a node's sitting is the node's own, in its state
directory.  Whether a node that leads work should *also* stop when
Henri's desk sitting closes is a question this reading did not
answer — it is his, and it would be a second word, not this one.

**What is not built**: the lamp (a node owes an account of what it
did, and nothing lights when it does not) and the andon, which leans
on `cords` and waits until 2026-08-31.  One of three, as §"What it
must not become" set it.  The card stays open.

## 2026-08-27 — the lamp measured, and it does not port to a node yet

Second batch, after the sitting cord landed (9fb2400).  The card's
§"What it must not become" said measure the lamp first, do not copy
`tools/kaizen.sh` on its say-so.  Measured, and the measurement says
**do not build it yet** — for a reason, not a shrug.

**A node already accounts for what it did, mechanically.**  The tally
node writes its own log as it runs — `gen 1 opened at 0 pulls`,
`served 1, total 2`, `gen 2 stopped, idle 50s` — in its plain state
file; the llm node's account is the launcher's `stopped` reason (the
sitting cord writes it) and the server log.  A node cannot *forget* to
account for itself the way a hosted session can, because the logging is
a side effect of running, not an act of will.  The hosted lamp exists
to compel the one thing a session can skip — the reflective account,
what went right and wrong and should change — and a program that
answers a pull has nothing to reflect and already logs what it did.

**So the lamp's subject is a node that *leads* work and could reflect,
and no such node exists.**  The frame (`card:work-environment-ai.md`,
15:45) is that a local model is a *session* when tend runs it to lead
the work rather than to answer a curl.  Only that node owes a kaizen's
kind of account, and today's llm node is the curl-answering kind — a
program, whose mechanical log is enough.  Building a reflective-account
lamp now is building for a subject that is not here, which is exactly
"a mechanism a session cannot test, it proposes, it does not declare"
(board/README.md §"What the days taught", promoted 2026-08-27).  The
lamp waits for the first node that leads.

**Where that leaves the three cords.**  The limit ported and is built
(9fb2400) — a node's sitting is a real thing to stop.  The lamp does
*not* port yet — a node accounts automatically; the reflective account
waits for a leading node.  The andon *does* port and is needed more by
a node than by a hosted session ("no person is watching its
transcript"), but it leans on `card:cords.md`, which waits until
2026-08-31.  So the card's actionable next cord is the andon on its own
date, and the lamp is deferred with this measurement rather than
carded — it reopens when a node first leads work.  The card stays open.

## 2026-08-27 — Henri: "not yet" on the second word; the card waits on one event

Question (4) of the limit section — whether a node that leads work also
stops when Henri's desk sitting closes — answered *"not yet."*  Closed
on the card the way the lamp was: it reopens with the first node that
leads work, and it would be a second grant word beside `sitting`, not
a change to it.

The andon exists on the hosted side as of today (`tools/andon.sh`,
card:cords.md) and its shape is a node's already — a record in a
state directory, a program reading it — but today's llm node answers
a curl and has no question, so the port is to the same subject the
lamp waits for.  Every open item on this card now waits on that one
event, so the status says so: **blocked — the first node that leads
work.**  The move back to open is a session's the day such a node is
started, and the placing stays Henri's.

## 2026-08-28 — Henri: the andon must sound even with no sound allowed

Measured this morning, from a fenced session, before the words: with
`audio` out of `TEND_REACH_ALLOW`, `REACH=audio tools/andon.sh ring`
is **denied by the hook before it runs** ("the row `audio` is outside
the bound Henri set … ask him"), and a bare `ring` inside the fence
fails at the player — exit 1, `ring-failed` in the log, `pulled`
false.  Loud, never silent: that half is right.  But the cord's only
path is a reach row the session has to be *allowed*, and Henri's word
on it: **"the andon needs to sound even with no sound allowed."**

The problem, not a fix: a cord a session must be granted reach to
pull is not a cord — the person who narrows a session's reach (and
narrowing is the normal case; `tend-reach-allow` with no `audio` is
one line) has, without meaning to, cut the one line the session is
supposed to use when it is stuck.  The reach bound governs what a
session may *touch*; the andon is what it may *say*, and the two
were tied together by the first row Henri ever allowed
(`tools/andon.sh`'s header: "the first row Henri ever put in
`TEND_REACH_ALLOW` was `audio`, for this").  The record half already
lives on the person's side (`~/.local/state/tend/andon.pending`
passes through the fence); the sound does not.

Noted here first, as the open card that owned the andon; **carded
the same morning** at Henri's "andon card" — `card:silent-cord.md`,
where the measurement above is day one's red-before-trusted.  The
andon on a *node* stays this card's.

## 2026-08-28 — the first live node, not yet leading

On the work laptop the llm node ran under its grant for the first time
(`done/node-install.md`): pulled with a question, up in 81 s, answered
at the port at 9.4 tokens a second, stopped on idle.  Two things for this
card from that hour.  **A pull with words is an ask, and nothing carries
the words** — `pull` appends them and starts the node; the person then
talks to the port by hand.  The node that *leads* work would be the one
that reads them.  And **the sitting cord held on a node** without being
reached: `sitting 10` is in the grant and the idle stop came first every
time; the limit is built and has not yet had to fire.  The event this
card waits on has not happened: the node answered, it did not lead.

### 2026-08-28, 09:37 — a runner can be alive and not watching

On the work laptop a runner wrapped in `strace` overran its 10-minute
sitting by 25 (`done/node-install.md`): idle fired at ~60 s and set the
stop, but `kill "$pid"` could not end the tracer, so the shell hung at
`wait` with the lock held and `status` reading *running* the whole time.
The wrapper is a confound — a normal run stops clean — but the gap is
this card's: **the cords are checked by nothing.**  `status` reads the
lock; it never asks whether the watch loop is alive or the sitting is
blown.  The build: the runner touches a heartbeat file each loop, and
`status`/`serve`/`check` read "runner up, watcher silent N min — the
cords are cut", with the resolver free to kill it.  That is the andon
on a node the card names, reached from the failure rather than the
design.  Red first, and without a real strace in the fixture.

## 2026-08-28, 09:40 — the "not yet" lifts, and the road to a node that leads work

At Henri's "I think that 'not yet' lifts now", the block set on
2026-08-27 is gone: the first node *may* lead work.  What that unblocks
and what it still needs, measured against the tree as it stands the day
the llm node first answered under keep (`card:node-install.md`):

**The substrate is built and shown.**  A local model (gemma-4-26B) runs
under keep — grant, budget, lifecycle — answers at the port at 9.4
tokens a second, caches to a 0:12 warm start, and stops on its cords.
That is the hard part, and it is done.

**Three bricks stand between "it serves" and "it conditions the
tree" — gemma4 as a session that works the board, next to gemma4 cold,
which is the measurement Henri wants ("whether gemma4 conditions").**

1. **Delivery — a pull's words reach the model and the answer comes
   back.**  Today `pull "…"` appends the words to the pull file and
   nothing reads them; the person talks to `:18080` by hand.  The brick
   is a loop that reads an unserved pull's words, asks the running node,
   and writes the reply where the puller can read it.  Unblocked,
   cheap — ~1 sitting.  This is the "a pull with words is an ask nobody
   delivers" line above, now the next build.

2. **A minimal work loop — the model reads the board and does one
   thing.**  The board is already bound readable into the fence; the
   reading is free.  The *doing* — a card edit proposed, a kaizen
   drafted, the next card picked — leans on `card:work-environment-ai.md`'s
   residual (a session exec'ing an arbitrary program), whose cheap path
   (§"Cheap, in roughly this order") does not need the broker built.
   ~1–2 sittings once started.

3. **The cords on the node itself.**  The sitting limit is built; a
   node's lamp and its andon are not, and the andon waits on
   `card:silent-cord.md` (2026-08-31).  The watcher heartbeat carded
   above (§09:37) is part of this — nothing yet asks whether a runner
   still honours its cords.  Wanted for a first led run, not a blocker.

**Estimate.**  A local model answering under the full boundary: done
today.  gemma4 doing board work you can read as conditioned-or-not:
~2–4 sittings, the first of them delivery (brick 1) whenever Henri says
go.  The milestone is not "gemma4 answers" but "gemma4 finishes a card
and we can tell it from gemma4 with no tree".  Lighting it also wakes
`later/model-acceptance.md`, shelved waiting on a door that admits a
model — which this card, led, becomes.

*The three faces the card named — a limit, a lamp, an andon — are the
same three the cords give a hosted session; this is where they become a
node's.  The limit is on the node now; delivery is what makes the node
a thing a person is on the other end of, which is the whole of "a
session is a program".*

### 2026-08-28, 10:05 — brick 1 built: delivery

`tools/deliver.sh NODE [question]` carries a pull's words to the running
model and writes the answer back — the half named twice today and never
built.  It reads the questions in `$STATE/pull` that have no reply yet,
asks the node at its port (`enable_thinking:false`, so the answer is the
answer and not gemma's reasoning), and appends a stamp, the question and
the reply to `$STATE/replies`; a `$STATE/delivered` marker means no
question is answered twice, and a first run with no marker arms rather
than answering the backlog.  With a question argument it pulls it first
(records and starts the node through the installed launcher), waits for
`/health`, and answers that one — the round trip in one line.

It runs on the person's side, like the runner: a fenced session's
loopback is not the host's, so inside the fence it records the ask
through `pull` and says the runner's side delivers — the same boundary
`launch.sh pull` draws.  Five tests against a stub model on the test's
own loopback (the node's real port is unreachable from the fence):
answers the unanswered and skips a wordless line, does not answer twice,
arms on a first run, records-and-answers a question argument, and inside
the fence records without delivering.  Red first — the mechanism found
its own line-reading bug (the whole pull file read as one question)
before its green.

What is left of brick 1 is the live round trip, which is the person's
one command (`tools/deliver.sh llm "…"`) the way every run here has
been — the fence cannot reach the port.  Brick 2, the model *acting* on
what it reads, is the next; delivery is what makes the node a thing a
person is on the other end of.

### 2026-08-28, 10:45 — brick 2 built: the model acts on what it reads

`tools/consult.sh NODE "question" [file ...]` grounds a question in
named tree files and asks the node, so the answer is shaped by the
tree's own documents rather than the model's cold memory.  Where
`deliver.sh` carries a bare pull, consult reads material off the tree
and hands it to gemma as the ground to answer from — the model acting
on what it reads, which is this brick.  Default material is
board/README.md; the context is capped (llm/grant: -c 2048, so a card
fits and the board does not) and a trim is said, not silent.  Runs on
the person's side like deliver; inside the fence it says the port is
unreachable.  Four tests against an echo stub: the named file's text
reaches the model and the answer returns, the README is the default,
a missing file is refused, and the fence is named.  Red first.

**This is the conditioning test made runnable.**  Cold, gemma called
jidoka a Buddhist practice (`done/node-install.md`, 10:08); with a tree
document that says stop-the-line handed to it, `consult` is the same
question grounded — the before and after in one tool.  What brick 2 does
*not* yet do is have the model *write* the tree (a card edit, a kaizen);
that is the next step and it is the one that needs a boundary on what
the model may change — this brick is read-and-answer, which is safe and
is where the measurement lives.

### 2026-08-28, 10:50 — the conditioning measurement, run

Henri ran the two consult commands on the work laptop.  The result is
the milestone the road was for.

**Jidoka, cold vs grounded — the tree changed the answer.**  Cold
(`done/node-install.md`, 10:08) gemma called jidoka *"a Buddhist
philosophy of mindfulness and non-attachment."*  Grounded by `consult`
in `doc/specimens/README.md` (which says "jidoka as stop the line"),
the same model, same question: *"Jidoka is a Japanese concept of
stopping work to prevent accidents, emphasizing safety and
efficiency."*  Stop-the-line, correct — the hallucination gone, the
tree's own document the only thing that changed between the two runs.

**It read a card it could not know cold.**  Asked what `andon-panel.md`
says the panel must never become, it returned all three: a way for a
session to answer its own cord, a second andon, a load-bearing sound —
the card's own three, grounded verbatim in reasoning.

**What this measures, and does not.**  It shows the substrate carries
the material and the material moves the answer — the method's claim that
a process's conditions shape its output, on a local model, under keep.
It does not yet show *judgment* conditioned — both runs were retrieval,
not a live seam (the caveat `later/model-acceptance.md` and the trap-kit
carry).  But the door that card is shelved behind is now open: a model
is admitted, grounded, and answering on the tree, and the before/after
is a line rather than a recollection.  This is the specimen's successor
made runnable — the qwen at 1.5 tokens a second that read the method
cold, now gemma reading the method's documents at 9.4, and getting
right what it got wrong without them.

### 2026-08-28, 11:10 — brick 3 built: the model writes, and only proposes

`tools/propose.sh NODE "task" [file ...]` has the node draft tree-shaped
work — a kaizen, a card edit — grounded in named material, and writes it
to a gitignored `proposals/` area, banner-marked *NOT tree content until
a person lands it by hand*.  It never touches a tracked file: the whole
boundary in one place, and it is the tree's own rule — a party may not
bound itself, so the model may not land its own words, the same seam a
clone's pull crosses and the same hand that runs `sudo tools/install.sh`.
Five tests, red first, and the load-bearing one asserts the boundary:
given a card as material, propose leaves it byte-for-byte and writes the
draft to `proposals/` instead.

**This closes the road's three bricks.**  deliver carries a pull's
words (brick 1), consult grounds a question in the tree (brick 2), and
propose lets the model produce work the person reviews and lands (brick
3) — read, then read-and-answer, then draft-and-propose, each further
from the tree and none of them able to change it without a hand.  What
brick 3 does *not* do is enforce the boundary in `keep` — the model
process confined so it *could* only write `proposals/`; here the
boundary is in `propose.sh`'s code, which is honest for a tool the
person runs and is the weaker form of the same line.  A `keep`-enforced
proposal is the hardening, and the andon/limit/lamp cords on the node
itself (§"What it is") are still the session-half this card opened for.
The model now reads the tree, answers from it, and drafts for it; a node
that *leads* work is these three under a loop with the cords, which is
where `session-program` goes next.
### 2026-08-28, 13:05 — the loop: `lead.sh`, one led turn, and the node's lamp lights

At Henri's "take session-program", the sitting after the three bricks
closed.  `tools/lead.sh NODE` is one led turn — the bricks under a loop
with the cords, which §11:10 named as where this card goes next.  The
node is handed the open board as a digest its small context can hold
(each open card's title and `because`; never `done/` or `later/`, and a
test holds that), and answers in a three-line shape — `CARD / TASK /
WHY` — or with one line, `ANDON: <question>`.  A pick goes through
`propose.sh` with the card as material, so the draft lands in the
gitignored `proposals/` and the boundary is brick 3's, unchanged: no
tracked file is written, and a test reads the whole board before and
after.  The cord is `andon.sh ask` — the record, no reach row — so a
node that cannot decide reaches the person through the panel outside
the fence (`card:andon-panel.md`), the reach-free path heard at 11:03.
**The model's word is not trusted for the card**: a name not on the
open shelf, or a reply with no shape at all, is a cord pull, not a
proposal — a node that leads and cannot say what it picked is exactly
the node that should ask.

**The lamp lights.**  The 2026-08-27 measurement said the reflective
account waits for a node that leads, because a curl-answering node has
nothing to reflect.  A led turn has: every turn writes
`proposals/lead/<stamp>.md` — what it read, what it picked and why, the
outcome, the reply verbatim — and a line in `$STATE/lead.log`.  That is
the node's own kaizen-shaped account, beside its proposals and never in
the tree; a turn that produced nothing still writes it.  Two of the
three cords are now on the node in the form the card asked for — the
sitting limit in the grant is the clock over any loop of turns, and the
andon is the record the panel hears.  Six tests, red first, against a
stub that answers the pick and then the draft.

**What this does not show**: a real pick.  The stub decides; gemma has
not yet led a turn on the live board, and the milestone (§09:40) is a
card gemma finishes that we can tell from gemma with no tree.  The live
turn is the person's one command — `tools/lead.sh llm` — and a loop over
it is `while tools/lead.sh llm; do :; done` under the grant's `sitting`,
which is what makes the loop a session and not a program.  The watcher
heartbeat (§09:37, nothing asks whether a runner still honours its
cords) and the `keep`-enforced proposal boundary are the hardening left.

### 2026-08-28, 13:15 — the heartbeat: the cords are checked by something

The §09:37 gap, built and measured, in the sitting Henri granted at
13:07.  The runner's watch loop now touches `$STATE/watch` every tick
and writes the program's pid to `$STATE/run.pid`; `status`, `check` and
`serve` read a held lock with a heartbeat older than `TEND_WATCH_STALE`
(60 s) as **"runner up, watcher silent N min — the cords are cut"**, and
`serve` — the resolver's call, the person's side — kills the pid so the
runner's `wait` returns and the lock frees; `check` goes red on it.  And
the stop itself no longer trusts TERM: after `TEND_KILL_WAIT` (10 s) it
escalates to KILL, logs "did not stop", and still closes as a sitting,
exit 0 — the laptop's failure reproduced without strace as a program
that traps TERM, which hung the old runner past the test's 30 s and
closes in ~5 s now.  Four tests, red first; the hung-runner fixture is a
lock-holder with a three-minute-old heartbeat, not a tracer.

This is the andon on a node the card named, reached from the failure:
not a sound, but a reading that a session outside cannot fake and the
resolver acts on.  `tools/launch.sh` is an installed restraint, so
nothing runs this until Henri's `sudo tools/install.sh` — `card:lander.md`'s
wait, said here rather than forgotten.  What is left on this card: the
live led turn (`tools/lead.sh llm`, his hand), and the `keep`-enforced
proposal boundary.

### 2026-08-28, 13:30 — the boundary is the kernel's: `--connect`, and a led turn under keep

The last named hardening, built.  `keep.py --connect PORT` is
`--bind`'s twin — the same TCP boundary, one port the program may talk
to, no other connect and no bind; the Landlock bit was there from the
first day (`NET_CONNECT_TCP`, handled and never granted), and the test
mirrors bind's: granted ok, other EACCES, bind EACCES.  Then
`tools/lead.sh NODE --kept` re-execs the turn under keep — the tree
readable, only `proposals/`, the node's state, the andon record (and
`/dev/null`, which the first run found: a shell's `2>/dev/null` is a
write) writable, one connect to the node's port.  The node must be up
first, because a runner started from inside keep would inherit the
confinement.

The proof is the mutate-style one: `TEND_KEPT_PROBE=<a board card>`
makes the kept process try to append to that file after its turn, and
the test wants `probe: refused` beside a proposal that was written — the
same turn, one write allowed and one refused by the kernel, not by the
script.  Brick 3's rule "the model proposes, the person lands" was held
by `propose.sh`'s code; a kept turn holds it the way the fence and the
grant hold theirs, from outside the party.  Three tests, red first; none
skipped here (Landlock ABI ≥ 4).

**What is left on this card** is one thing, and it is Henri's hand: the
live led turn — `tools/launch.sh llm pull` then `tools/lead.sh llm
--kept` — and reading what gemma picks.  Everything the card opened for
is on the node: the sitting (2026-08-27), the lamp (`proposals/lead/`,
13:05), the andon (the record, 13:05; the heartbeat, 13:15), and the
confinement (13:30).  Whether the node *conditions* is the next
measurement, and `later/model-acceptance.md` is what it wakes.

### 2026-08-28, 13:45 — the first live attempt: a silent crash, made loud

Henri ran the install and `tools/lead.sh llm --kept`, and it said only
"llm is not up — start it first".  The log said why: `pull` at 13:27:22
had said "started llm", and a second later llama-server died at the
loader — *libsvml.so: cannot open shared object file* — because the
shell that pulled had no oneAPI on `LD_LIBRARY_PATH`, which the runner
inherits (`card:node-install.md` §07:10; the same node served at 10:51
from a shell that had it).  Henri: "ouch!  I forgot that, but it should
not crash silently."  Two fixes, red first: `launch.sh pull` and `serve`
watch the runner they started for a second, and a runner that stops at
once with a non-zero exit is said out loud — the stop reason and the
log's last line that is not warning noise — exit 1, no "started" claimed;
and `lead.sh --kept` on a node with no runner says the last stop and
what it last said, and on a runner still loading waits for `/health`
instead of refusing.  A first watch window of 3 s broke an existing
test (a healthy pull returned late into a 4 s idle); it is 1 s, which
the 13:27 log shows is enough.  `launch.sh` changed again: his `sudo
tools/install.sh`, then pull from a shell with the oneAPI env, then the
kept turn.

*2026-08-29 — the watch reverted, with its replacement.*  Henri's
"we will eventually revert" came due at his "land it": the runner's own
stop path now writes a death notice into the andon record on the
person's side (`card:canvas.md` day two, `tools/launch.sh`), so a
runner that dies at the loader is a line on the person's timeline
whether or not `pull` was watching, and `died_at_once` and its two
calls are gone — a pull says "started" and returns at once again.

### 2026-08-28, 13:48–13:58 — the first live led turns, read the next sitting

Between the 13:45 fix and the kaizen, Henri ran the kept turn three
times on the work laptop; the accounts are in `proposals/lead/` and the
cord pulls in the andon record, answered at 13:59.  Read by the next
session (17:15), because the milestone was reached and no card said so.

**The node led.**  At 13:48 gemma read the seven open cards, picked
`canvas.md` — the card opened twenty minutes earlier, whose `because` is
the freshest text on the board — restated its `because` as the task,
and `propose.sh` drafted with the card as material.  `lead.log`: `lead
proposed canvas.md`.  The kernel held the boundary; no tracked file
moved.  That is the event this card waited on since 2026-08-27.

**What the turn produced is the measurement, and it is not a card
finished.**  The draft (`proposals/2026-08-28-1348-…md`) is one
paragraph saying that a draft is ready — *"It outlines the concept of a
'pin' and a 'canvas'… The draft is ready to be read"* — repeated four
times with `---` between, and *"No preamble is included as per the
instructions."*  A description of a draft, not a draft: the model
answered the instruction about the shape of its reply rather than the
task.  The two turns after (13:57, 13:58) named `<canvas-script.md>` and
`<canvas-death.md>` — the prompt's own `CARD: <filename from the list>`
placeholder, angle brackets and all, echoed as a pick — and `lead.sh`
read each as a card not on the open board and pulled the cord, which is
the rule holding: the model's word was not trusted for the card, and a
node that cannot say what it picked asked.  At 2048 context and 160
tokens, on a 26B model with thinking off, the pick is sound and the
draft is not; the milestone (§09:40) is a card gemma finishes that we
can tell from gemma with no tree, and this is gemma with the tree,
picking the right card and drafting nothing — conditioning shows in
the pick, not yet in the work.  What to change is the prompt's
placeholders (a small model echoes `<…>`) and the draft's length and
material; that is tuning on the live seam, his hand, and it is where
`later/model-acceptance.md`'s caveat lands.

**One defect, fixed red first.**  `lead.log` has two 13:48 lines — an
andon on `<canvas-death-2026-08-28>`, then the proposal — and
`proposals/lead/` has one 13:48 account: the file is stamped by the
minute, so the second turn wrote over the first and the first live
cord pull's account is gone.  A turn whose stamp is taken now takes
`-2`, `-3`; the test runs two turns in one minute and wants two
accounts and two log lines.

**Also today, from `card:canvas.md`**: the panel now shows a pinned
node's row and its death on the andon's timeline (day one built,
17:30), which is the person-side half of "no person is watching its
transcript" that this card's andon section named.

### 2026-08-28, 17:45 — the prompt's placeholders, and a draft that is not about itself: proposed

From the live turns' measurement, the cheap half done in the tree, the
effect his to measure.  `lead.sh`'s prompt no longer shows the model
`<filename from the list>` — a 26B model with thinking off echoed the
brackets as a pick twice in two turns — and reads a bracketed name by
its name: `CARD: <lander.md>` proposes on lander.md, `CARD:
<unicorn.md>` is still a cord pull, because the open shelf is the
judge, not the typography (one test, red first).  `propose.sh`'s prompt
said *"Output the draft itself, ready to read — no preamble"* and got
*"The draft … is ready … No preamble is included as per the
instructions"* four times over; it now says to write the draft's own
lines and nothing about them, not to repeat, not to mention the
instructions.  That second change is a mechanism this seat cannot run
— the stub answers whatever it is told — so it is **proposed, not
declared** (board/README.md, "What the days taught"): the next live
`tools/lead.sh llm --kept` on the work laptop is what says whether the
draft is a draft.  If it still is not, the dial is the material and
`max_tokens`, not the prompt's manners.

### 2026-08-28, 18:15 — the second live turns: the fence echoed this time

Henri ran the kept turn twice more (17:46, 18:01) after the prompt lost
its angle brackets.  gemma answered `CARD: canvas.md ===` both times —
the digest's own `=== name ===` fence, echoed where the brackets had
been — and went on to complete the digest's pattern for the other cards
with `TASK: the one small thing, in one line` verbatim.  The shelf
refused `canvas.md ===` and the cord was pulled, which is the rule
holding; but the pick under the decoration was right both times, and
the tuning of 17:45 had only moved the echo.  So the field is read for
what the shelf judges and nothing else: the first word ending in `.md`,
whatever wraps it (`lead.sh`; one test, red first, with the fence and
with backticks, and an invented card so wrapped is still a pull).  The
prompt says "the filename only, one word ending in .md".  Proposed as
before: the next live turn says whether the pick lands and whether the
draft is a draft — the 18:01 reply repeated one line about "a line of
text that describes the task" twice, which is §17:45's second question
still open, and its dial is the material and `max_tokens`.  Also seen:
his `andon.sh ask " "` at 18:00 — a blank question is accepted and
listed as a blank line; small, and `ask` should refuse it.

### 2026-08-28, 18:20 — the pick lands; the draft is a tautology

After his `sudo tools/install.sh` (18:05) and one more kept turn: the
filename read cleanly, `work-environment-ai.md` was proposed on, the
kernel held, and `proposals/2026-08-28-1809-….md` is two sentences —
*"The reason we are missing a way to work with each other is that we
are not yet able to work with each other.  This is because we are not
yet able to work with each other."*  TASK and WHY were both the card's
`because`, verbatim.  Henri read it (`gvim`) and answered the three
pending questions; no word yet.

**What it measures.**  The loop is whole end to end — read, pick,
propose, account, answer — with no hand in the tree, which is what this
card opened for.  What the loop carries is the `because` alone: the
digest hands the model one paragraph per card, `propose.sh` hands it
the card as material into a 2048-token context that the card does not
fit, and a model given a problem statement and asked for "one small
thing" restates the problem.  The milestone of §09:40 — a card gemma
finishes that we can tell from gemma with no tree — is not met, and
the reason is now specific rather than "the model is small": nothing
in the turn tells it what a small thing *is* on this board (a card's
"Day one" section does), and it cannot read far enough to find out.

**The dials, in order, all his to turn on the live seam**: (1) the
digest carries each card's "Day one" paragraph beside its `because`,
so the ask names a shape; (2) `-c 4096` in `llm/grant` so a card fits
as material, at the cost of a slower start and the ledger's budget;
(3) `max_tokens` up from 160 for the pick and whatever `propose.sh`
sets for the draft.  A session can build (1) with the stub and cannot
say whether it moves the draft; that is a proposed change, and the
kept turn is its measurement.  Whether to keep turning dials on a 26B
model at 9 tokens a second, or to read this as the conditioning
result — *the tree moves the pick and not the prose* — is the reading
`later/model-acceptance.md` is shelved for, and it is his.

### 2026-08-28, 18:35 — the same turn, to a Claude model: `tools/compare.py`, his to run

Henri: *"I have anthropic api key here.. you could try how sonnet or opus
fares in the task you've given to the local llm."*  The seat cannot:
no key in its environment, no net inside the fence (`api http 000`),
no SDK in the venv.  So the comparison is a tool on the person's side,
the route the README names for a claim this seat cannot run.
`tools/compare.py [MODEL ...]` gives a Claude model the led turn as the
node gets it — `lead.sh`'s digest (title and `because` per open card,
never done/ or later/, capped at 5000 chars), the pick prompt at 160
tokens, then `propose.sh`'s draft prompt with the picked card as
material at 600 — reads the reply the way `lead.sh` reads it (the
first word ending in `.md`, judged by the open shelf), and writes one
account per model under `proposals/compare/`, with the draft and the
token usage; the andon record is never written — a measurement, not a
turn.  Default models `claude-sonnet-5` and `claude-opus-5`; the SDK's
refusal fallbacks left off, because a comparison is of the model named.
Two tests hold the digest and the reading against `lead.sh`'s; the
call itself is untested here and unrun — **proposed**.  His two lines:
`.venv/bin/pip install anthropic`, then `tools/compare.py`.

What it will say, if it says anything: whether the tautology of 18:09
is the 26B model or the turn's shape.  A Claude draft that is a draft
from the same `because` and the same 2-line ask means the dials named
at 18:20 are the model's; a Claude reply that also restates the
problem means the turn asks for too little and the digest is the
thing to change, whatever model leads.

### 2026-08-28, 18:27 — Sonnet 5 and Opus 5 on the same turn: the pick is a small thing; the draft was the tool's fault

Henri ran `tools/compare.py` (`proposals/compare/2026-08-28-1827-*.md`).
**The picks.**  Both chose `canvas.md`.  Sonnet 5, at 90 tokens,
`end_turn`: *"draft a short note format that writes the death reason
(exit code + last log line) into the node's state directory when the
runner exits, so it's on disk next to 'stopped'"* — WHY: *"the fact
already exists in the log; it just needs one place a person would
look."*  Opus 5: *"Draft the exact one-line death notice — node name,
exit code, last log line, path."*  From the same digest — one `because`
per card and nothing else — both named a *thing*, of the size the prompt
asked for, and the thing is nearly what the tree already has
(`stopped` holds the reason; `last_said` the line; the canvas row shows
both), which is what a pick from a `because` alone can be: right in
kind, blind to the body.  gemma at 13:48 and 18:09 restated the
`because`.  That is the answer to §18:20's question: **the turn's shape
is enough for a model that can hold it; the tautology is the model's**,
and the three dials are worth turning only if the aim is gemma
specifically.

**The drafts were empty, and that was the tool.**  Both accounts read
`draft …→600 (stop max_tokens)` with no text, and Opus's pick hit 160
the same way (no WHY): on these models thinking is adaptive by default
and its tokens count against `max_tokens`, so a limit copied from the
node without the node's other setting (`enable_thinking:false`) bought
thinking and no draft.  A fixture copied from the live thing, in its
API form — the session's.  Fixed: `thinking: disabled` is sent, the
node's condition; `--thinking` is the other measurement, adaptive on
with 16000 to write in, and the account's `usage` line says which.  His
line again: `tools/compare.py`, and `tools/compare.py --thinking` if he
wants the second number.

### 2026-08-28, 18:45 — with thinking off, both drafted a draft; the fork, decided

Henri ran `tools/compare.py` again (`proposals/compare/2026-08-28-1835-*.md`),
thinking off, the node's limits.  **Both picked `canvas.md` and both
wrote the thing they named.**  Sonnet 5 (draft 600, cut at the cap): a
`died` file beside `stopped` — four lines, when / exit / last / from,
"the current fact, checked the way `run.lock` and `watch` are checked".
Opus 5 (434 tokens, `end_turn`): a one-line death notice appended by
the runner's own stop path to the andon record on the person's side —
*"so the death and a cord pull land on one timeline"* — with the rule
that the runner appends and nobody else, that a zero exit writes
nothing, and that *"`pull` does not write it (its one-second watch is
the thing this replaces)"*.  That last clause is the canvas card's own
§13:45 prediction, reached from the card's `because` and nothing else,
by a model that had never seen the tree before this turn.

**The measurement is complete.**  The turn's shape — the open board as
one `because` per card, a pick at 160 tokens, the card as material at
600 — is enough for a model that can hold it to name a small thing and
draft it; gemma-4-26B at 9 tokens a second restated the `because` on
every landed turn.  The tautology is the model's, not the loop's.  So
the three dials of §18:20 are worth turning only if the aim is gemma
specifically, and the road from §09:40 — "gemma4 working the board next
to gemma4 cold" — has its answer in a different form than it expected:
the tree moves the *pick* on gemma (13:48, 18:09: the right card every
time) and not the prose; on Sonnet and Opus it moves both.

**What this decides, and what it opens.**  The loop does not care which
port answers: `lead.sh` is a digest, a pick, `propose.sh`, an account,
under keep.  A Claude model as the leader is the same loop with a
different door — and a door is exactly what `later/model-acceptance.md`
was shelved for: *"tend has a place where a model is admitted at all …
the llm node's cords, board/session-program.md — so that a refusal has
somewhere to sit."*  That place exists as of today, and `compare.py` is
its first instrument — the same turn put to N models, with accounts a
person can read side by side.  **Woken, this sitting, to the board**,
placed last; the tiebreak is his.  What stays on this card: the node's
cords are built and installed; the live turn runs; the leading model
is a choice, and the card that judges a model is the one that just
woke.  A Claude-led turn under keep is a build — keep's `--connect` is
one loopback port, and a leader that calls out needs a reach the node
does not — and it is not started until he says which model leads.

## The door — both, 2026-08-29 evening

Asked which model leads, Henri: *"I'd propose, build capability for
both gemma and claude, also I'm thinking about subscribing to
openrouter."*  Both is one shape, because the loop already speaks the
OpenAI chat wire to the node's port (`/v1/chat/completions`, with
`TEND_LLM_URL` as the override) and that is OpenRouter's wire and
Anthropic's compatibility endpoint's too.  So a **door**: a directory
under `doors/` with a `door` file in the grant's shape — `url`,
`model`, `key` (a file under the person's home, mode 600, never in the
tree), and `admitted` (who, when, the words; the place
`card:model-acceptance.md` was woken for — a door is where a refusal
has somewhere to sit).  `tools/door.sh NAME` reads and checks one;
`tools/lead.sh NODE --door NAME` (or `TEND_DOOR`) runs the same turn
through it — both asks, the pick and the draft — with `model` in the
body and the key on curl's stdin (`-K -`), never on an argument line;
the account says `door  openrouter (anthropic/claude-sonnet-5)` and the
proposal's banner says *through the openrouter door*.  Two doors are
checked in: `doors/openrouter/door` and `doors/anthropic/door`, their
model names the doors' own vocabulary, checked by the first live turn
(a wrong name is a 404, not a silent wrong model); the keys are his to
put at `~/.config/tend/{openrouter,anthropic}.key`.

What is honest about it: **a kept turn through a door is not built**
and says so (`lead.sh NODE --kept --door X` exits 1: keep's
`--connect` is one loopback port and a door calls out).  A door turn
runs on the person's side, unkept, as every turn did before `--kept`
existed; the boundary brick 3 is then propose.sh's code again, not the
kernel's, until a leader's reach is a grant row.  The node with no door
named is the loop as it was: gemma, local, under keep.  Red first: the
door's model and key arriving, the key refused when others can read it
or when it lives in the tree, the unknown door, the kept refusal, and
every checked-in door parsing — all red against the previous commit.
Not measured: a live turn through either door; that is the day one of
the keys.

## 2026-09-01, 15:40 — taken under work, and the first act is admitting where it stands

At Henri's *"take the session-program under work"*.  The card's last
entry was 2026-08-29 evening.  **Four days of work have gone into the
door and none into this card's own milestone**, which is not a criticism
of the door — it is the other half of his "both" — but it needs saying
plainly before anything else is written here.

**The milestone, unchanged since 08-28**: *"not 'gemma4 answers' but
'gemma4 finishes a card and we can tell it from gemma4 with no tree'."*
The estimate that day was ~2–4 sittings.  Four days later, the count of
led turns through **gemma4** is what it was, and the count through the
**door** is in the dozens — 48 arms on 2026-09-01 alone.  The three
bricks are built and the loop runs; what has not happened is the
comparison the card exists for.

### What the door work bought this card, which is more than it looks

The 48 arms of `card:tools.md` were run on `tencent/hy3`, and their
finding transfers directly and was not looked for:

**A tooled mind reading whole 40k cards produced a usable turn 15 times
in 24.  The same mind, with `readchars` at 4000, produced one 24 times in
24** (Fisher p = 0.0016).  The knob is what a single read returns, not
what the mind is given overall.

That matters here more than it does there.  `card:tools.md` §"Short
prompts" already recorded the reason: at 4B active, gemma4 is the model
least able to carry a 40k document and still act — the card wrote that
about *tool names* ("a name the model has never seen is a call it makes
badly") and the same argument applies with more force to material.  **The
most likely single reason gemma4 has not led a turn well is the one thing
measured today**, and nobody had connected them because the measurement
was aimed at a different card.

So the conditioning measurement should not be run at the settings the
node has now.  Running it at `readchars 60000` would measure gemma4
drowning, and would be read as measuring gemma4.

### What the milestone actually needs, named as three things and not "a sitting"

1. **gemma4 led turns at `readchars 4000`, enough of them to count.**
   The instrument exists (`tools/lead.sh NODE`), the knob exists
   (`TEND_READCHARS`), the node exists.  This is cheap in money — the
   node is local — and expensive in wall-clock at 9.4 tokens/s.  **It is
   also the one arm in this whole family that costs nothing to get
   wrong**, which is an argument for running it before any more paid
   arms.
2. **The cold arm, which has never been defined.**  "gemma4 with no
   tree" is written in the card three times and specified nowhere.  Cold
   is not *no board* — a model asked to work a board it cannot see
   produces nothing, and that comparison is rigged.  The honest cold arm
   is the same board, the same task, and **none of the tree's
   conditioning**: no `board/README.md`, no manifesto, no kaizen, no
   card prose about how work is done here.  Writing that down precisely
   is a prerequisite, not a detail, and it has been deferred for four
   days.
3. **A verdict a person can read.**  `card:swe-bench.md`, opened the same
   afternoon, has the same problem one level up and states it: a
   measurement whose result the tree cannot act on produced prose.  What
   would make this one actionable is not "conditioned looks better" but a
   named thing the conditioned turn does that the cold one does not —
   cites a card, refuses a task, pulls the andon, writes a `because` as
   a problem.  Countable, or it is a mood.

### The honest state, for whoever picks this up

**Built and shown**: the node under keep, delivery, the model acting on
what it reads, propose-only writing, `lead.sh`, the heartbeat, the
kernel boundary, the doors, the tools, the executor's cut notice.

**Not built**: the cold arm's definition; the conditioning run at
settings that are not known-bad; the verdict's countable criterion.
Three things, and the first two are writing rather than building.

*(question, measure — does gemma4 at `readchars 4000` lead a turn the
way hy3 did?  **The head arm's result predicts yes and nothing has
tried it**; the node is local, so this arm costs wall-clock and no
money. henri: measure 2026-09-01)*

*(question, his call — is "cold" the same board with none of the tree's
prose, or something else?  A session can propose the definition and
should not settle it: the comparison this card exists for is decided by
what the control arm is, and a session defining its own control is the
shape `manifesto.md` §"How a practice gets adopted" warns about.
henri: I think we should create some sort of a tree that has imperative
commandments in it that match the stuff we have here, but written as commands
without rationale or provenance)*

## 2026-09-02 — taken again, and the first blocker is in the card's own item 1

At Henri's *"ottaisitko työlle session-program ja asiat mitkä sitä nyt
estävät"* — take it, and the things that block it now.  Read from this
seat, inside the fence, before anything was written: `launch.sh llm
check` (every · line is the fence hiding the machine, nothing red),
`launch.sh llm status` (not running; last stop 2026-08-30 16:54, idle),
`tools/lead.sh`, `tools/compare.py`, the doors, and the seven led turns
of 2026-08-28 under `proposals/lead/`.

### What blocks it, each named from its seat

**1. The node's own turn never reads the tree — so "gemma4 at
`readchars 4000`" is not a setting the loop has.**  `tools/lead.sh`
builds the node's prompt from the digest (each open card's title and
`because`) and a fixed system text, and sends it once; there is no
tool loop in it, no `read`, no `readchars`.  The reads happen only in
`tools/compare.py`'s tools and seeded arms, and only through a door
(`doors/openrouter/door` carries `tools read ls grep`; the anthropic
door carries none; the node with no door is "the loop as it was").
So yesterday's item 1 — gemma4 led turns at `readchars 4000`, "the
instrument exists, the knob exists" — was written about an instrument
that does not take the knob, and the `measure` question above cannot
be run as asked.  **This is also why the cold arm changes nothing for a
led turn**: a mind that sees only the digest sees the same digest from
either tree.  "Gemma4 with the tree" against "gemma4 cold" is a
comparison between a mind that *reads* under each tree, and the only
loop in which gemma4 reads is one it has never been put in.

**2. The route by which gemma4 could read is a door at its own port,
and it takes one line from his hand.**  `doors/README.md` foresaw it —
"the node's own port" speaks the same wire — and `doors/llm/door` now
exists: loopback URL, the model's name, `tools read ls grep`, `calls
16`, `readchars 4000`, admitted in his words today.  Two things it
cannot do from here.  `door.sh` insists on a key file under the home
(the node checks no key; any line at mode 600 satisfies it), and
llama-server answers tool calls on this wire only with `--jinja` on
its program line, which is in `llm/grant` and is his to edit.  Whether
gemma4's chat template then actually emits a tool call is what the
first turn says — proposed, not declared.

**3. Every turn on the node is his hand, by the fence's design.**
`lead.sh` exits at once inside the fence ("the node's port is
unreachable — `--unshare-net`"), and a door calls out.  So the gemma4
arm — any number of turns of it — runs from his shell or his timer,
never from a session's.  `card:hold.md`'s hold and tick keep the node
up between turns; what no mechanism yet does is run the turns.  This
is not new and it is the card's oldest sentence ("a leader's reach is a
grant row"); it is named again because the milestone's cheap arm is
cheap only in money.

**4. The loader.**  The last live start died at `libsvml.so` with no
oneAPI on the shell's path (2026-08-28 13:27), and `check` from here
lists twelve libraries it cannot find "from this seat".  A pull from a
shell with oneAPI's loader path, once, then the hold keeps it.  His.

**5. The cold arm waits on his review**, which he asked to do at his
own pace (the mark on `doc/cold/README.md`, the four uncertainties in
`doc/cold/notes.md`).  One of the four is a measurement and not a
call, and it is done below.

### What moved from here

**The length ratio, measured** (`doc/cold/notes.md` uncertainty 1):

| what a tooled mind can read | bytes | × commandments |
|---|---|---|
| `doc/cold/commandments.md` | 3,944 | 1 |
| `board/README.md` alone | 38,050 | 9.6 |
| README + manifesto + vision + keeper | 68,992 | 17.5 |
| the whole board shelf, `board/*.md` | 361,999 | 92 |

At `readchars 4000` and 16 calls a turn, a mind reads at most 64k
chars whatever the arm.  The cold arm's rules fit in one call; the real
tree's `board/README.md` alone is ten.  So length is not a confound
*beside* the variable, it is the variable's other face: reasoned prose
is long, and whether a mind at 4B active can carry the reasons is part
of what "load-bearing" means.  The honest form is to state the ratio
with the result, which this table is for.  Whether to pad or accept is
still his.

**The verdict, made countable before any data** (item 3 above, the
part that was writing).  Per turn, read off the account and the
proposal, four yes/no counts:

1. **pick on the shelf** — `CARD:` names a file on the open shelf.
   `lead.sh` and `compare.py` already refuse the rest; the count is
   the refusals.
2. **problem, not fix** — when the draft is card-shaped, its `because`
   passes `test/test_board.py`'s own rule; when it is not, the `TASK:`
   names a few lines and not a build.
3. **asks rather than invents** — `ANDON:` when the thing is missing,
   instead of a `CARD:` on nothing.  Already refused; count it.
4. **reads what exists** — the `C:` lines name paths that resolved, not
   guessed ones the executor refused.

And one that is **not fair between these arms and is written down so
nobody counts it**: *cites a card, an F-number, a §*.  The cold arm
carries no provenance by construction, so a mind reading it has nothing
to cite; a difference on that count measures the removal, not the mind.

**Prediction, written before the run.**  On counts 1–4 the two arms
will not differ at N=24 — the commands say *do X* and the counts above
are *did X*.  Where they will differ is in the draft's content: the
real-tree mind's `WHY:` will name an incident or a reason and the cold
mind's will restate the command.  That is not one of the four counts,
and if it is the only difference, the result is: **the reasons are
carried into the output and do not change the act** — which is a real
answer to his question, and not the one this tree would prefer.

### What this leaves, and whose

- **His, one shell**: `umask 077; printf 'node\n' > ~/.config/tend/llm.key`;
  `--jinja` on `llm/grant`'s program line; a pull from a shell with
  oneAPI on its path, and a hold.  Then `tools/compare.py --door llm
  --arm tools --seed` once, and the first turn says whether gemma4
  makes a tool call at all.  Precondition first, as the handed-script
  strand asks: the node up and the key present, or the door says so.
- **His, at his pace**: the cold arm's mark and its three remaining
  uncertainties.
- **A session's, after the first turn**: 24 arms seeded at
  `readchars 4000` on gemma4 through the door, under each tree, the
  four counts, the table above beside the result.
- **Not built, and still the card's**: a leader's reach as a grant row,
  so a turn can run from somewhere that is not his shell.

*(question, waits on the first turn through `doors/llm/door` — does
gemma4 through llama-server's OpenAI wire emit a tool call at all with
`--jinja`, or is the tools arm on the node a build and not a door
file?)*

*Half answered 2026-09-02 06:58 (§"06:58" below): with the knob on the
wire gemma4 answers in shape and calls nothing when the digest is in
the prompt.  The event this waits on is now the unseeded tools arm,
one turn from his shell.*

*Answered 2026-09-02 07:0x (§"07:0x" below): yes — one deliver ask
through the door, `C: read board/README.md → 4.0k chars, cut at line 76
of 622`, and the heading right.  The tools arm on the node is a door
file, not a build.*

*(question, his call — the cold arm on the node is measured through a
door, unkept, with read-only tools on the person's side; is that
acceptable for the measurement, or does the kept form of a door turn
have to be built first?
henri: unkept is okay for measurement, but in practice the commands
should probably be possible to run kept by the model's decision. It's
the mechanism to limit blast radius, right? 2026-09-02)*

*So the measurement runs unkept and every account says so, and the
kept door turn is this mechanism's next line: keep's `--connect` is one
loopback port, `doors/llm/door` is a loopback port, so `--kept` with a
door whose url is 127.0.0.1 is the refusal at `lead.sh` and
`deliver.sh` lifted for that one case — the courier confined, not only
its reads, which are kept per call already.  A line here and not a
build, until something wants to run with nobody at the desk.*

### 06:29 — the first turn through the door, and what it does and does not say

Henri's shell, the same hour: `--jinja` was already on the grant line,
the key file in place, the node pulled and held after the first run
said "did not answer" for a runner that had idled out on 08-30 (that
sentence hid why; `F014`, found and fixed in the hour).  Four attempts
while the node loaded left empty turns; the fifth answered:

    llm tools-seeded: picked questions.md — Define a specific markdown header or tag for "questions for the person".
      calls: 0

**`calls: 0` does not answer the `waits on` question above.**  The
reply is 7,222 bytes of reasoning in the content channel — every card
weighed by name, `CARD:` written twenty-two times, cut mid-sentence
before the answer — because a door turn never sends the node's
`enable_thinking:false` (`deliver.sh` sends it only when a door names
no model, and a door always names one), while the account records
"thinking off — the node's own condition" from the flag it did not
send.  That is `F015`.  The pick is the parser's first `CARD:` line;
the model's last was `kaizen-ingestion.md`.  So a mind that never
reached its answer also never reached the line where it would have
called a tool, and whether gemma4 emits one is still unmeasured.

What the turn did show: through the door gemma4 gets the whole digest
and reasons over all sixteen cards by name, which is what `F008` and
`F009` bought; and its reasoning was tree-shaped — "if we can't find
the questions, we can't answer them" is `card:questions.md`'s own
`because`, said back.  The next turn wants the knob on the wire first
(`F015`'s smaller shape), and then the question above gets its answer
from a reply that reaches its end.

**F015 fixed the same hour, in the slower shape** — a door word,
`thinking  template`, on `doors/llm/door`, read by `door.sh --tools`
as its fifth line and honoured by deliver, lead and propose; the
account's limits line now says what the wire carried.  The url was not
made the discriminator, because every door test's stub sits at
127.0.0.1 and the rule would have had the tests lie about OpenRouter.
The next turn is the same command from his shell, with the node held.

### 06:58 — the second turn, clean, and it read nothing

His shell, twenty-six minutes after the first.  Six attempts in
eighteen seconds left empty turn directories (the node answering
nothing yet) and the seventh answered, in shape, with the knob on the
wire — the account's limits line now reads `thinking off —
enable_thinking:false on the wire`, and the reply is three lines and
292 bytes where the first turn's was 7,222:

    CARD: questions.md
    TASK: Define a regex pattern for "the person's call" to be used in a gathering script.
    WHY: To move from manual collection to an automated way of surfacing open decisions.
    calls: 0

On the four counts: pick on the shelf, yes; a few lines and not a
build, yes; asks rather than invents, not exercised; reads what
exists, **no reads at all**.  The pick is the same card the first
turn's reasoning reached first, and the task is `card:questions.md`'s
day one (a) said back as a build — the regex exists
(`test/test_questions.py`), which a read would have shown.

**So the `waits on` question is half answered.**  Given the digest,
gemma4 answers from it and does not reach for a tool — which is what
the seeded arm permits and what hy3 also did on 2026-09-01 in the arm
where the digest was enough.  Whether it *can* call one is the other
half, and the arm that forces it is the tools arm unseeded: no digest,
so the only way to name a card is to read the shelf.  One turn, his
shell, `tools/compare.py --door llm --arm tools`; a `C:` line answers
yes, and a three-line reply naming a card it never read answers
something worse.

### 07:01 — the unseeded tools arm: no digest, the tools offered, and it asked

His shell, three minutes later (the six empty directories at 06:58
were his re-runs while the node loaded — his word).  No digest in the
prompt, `read ls grep` in the request with the seat message that says
*read the tree whenever the answer may be in it*, and the reply:

    ANDON: Which card should I focus on first?
    calls: 0

Neither of the two outcomes the paragraph above named.  It did not
read and it did not invent: it pulled the cord, which is the third
count exercised for the first time and answered the honest way.  But
the cord was pulled with the answer one `ls board/` away and the tools
in hand, so on this turn gemma4 asked where reading was the act.  hy3
on 2026-09-01, same arm, read sixteen cards.  That is the 2026-08-28
finding again — Sonnet and Opus reached the card's own prediction from
the `because`, gemma wrote a tautology — *a difference in kind, not
degree*, now on the reading side.

**"Did not" and "cannot" are still not separated**, and one turn from
his shell separates them: an ask through the door that can only be
answered by reading and offers no cord —

    TEND_DOOR=llm tools/deliver.sh llm "Read board/README.md and tell me its first heading, in one line."

A `C: read board/README.md` line says gemma4 emits a tool call on this
wire; a heading guessed without one says the tools arm on the node is
a build (a prompt that makes the call the shape of the answer, or a
model that is not this one), and that is `card:model-acceptance.md`'s
question before it is this card's.  Three turns so far, N=1 each, and
every one has moved the question rather than answered it — which is
what the card's day one is for.

### 07:0x — the fourth turn answers it: gemma4 calls the tool when reading is the ask

His shell, the deliver ask above, verbatim:

    C: read board/README.md → 4.0k chars, cut at line 76 of 622
    A: # board/ — the live board, and how to work it

One call, the right file, the right heading.  So "cannot" is out: on
this wire, with `--jinja` and the knob, gemma4 emits a tool call and
reads the cut back correctly.  The `waits on` question is answered and
the tools arm on the node is a door file.

**What the four turns say together, N=1 each, and it is one sentence**:
gemma4 reads when reading *is* the ask, and not when reading is the
way to the ask.  Told to read a file, it read it.  Given tools and a
question whose answer was one `ls` away, it asked the person.  Given
the digest, it answered from the digest.  hy3 on the same arms read
sixteen cards unprompted.  That is the difference in kind from
2026-08-28, and it decides the *shape* of this card's measurement
rather than blocking it:

- **For gemma4 the tree cannot be conditioning it reaches for.**  An
  arm that leaves the rules one read away measures whether the model
  reads, and this model does not.  The rules go in the prompt, as
  material — the same place `propose.sh` puts a card's text — and the
  two arms are the same task with the real tree's rules and with
  `doc/cold/commandments.md` in that place.  The length ratio table
  above is then the direct confound and is stated with the result.
- **For hy3 and the door models the arms can stay as they are**: the
  tree bound, reads free, and the cold arm a tree with the
  commandments where the reasoned documents were — which is the shape
  `doc/cold/notes.md` uncertainty 4 asked about (a model arm and a
  session arm want different artifacts), answered by this morning:
  they do, and the model arm splits again by whether the model reads.

What is his: the cold arm's review, unchanged; and whether the gemma4
arm is worth running at all when its every turn is the prompt and
nothing else — which is `card:model-acceptance.md`'s question, and the
first concrete case it has been handed.  What is a session's: the
material-in-prompt arm for gemma4 is `compare.py --draft` with a
`--material` it does not yet have, one flag.
