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
