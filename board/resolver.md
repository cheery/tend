# resolver — a program starts only when a person types its launcher, and the grant that confines it lives in that launcher

    status   open
    because  nothing here starts a program but a hand in a shell: the
             node runs when someone types `node/run.sh run`, and a pull
             that finds no runner is recorded and served by no one.  So
             the confinement a program gets is whatever the launcher it
             was started through happens to bake in — one script, one
             program, and a session that starts a program some other way
             starts it with the session's whole reach.  Henri: the person
             "always pulls, never need to start the program themselves"
             — and today the pull cannot start anything, and the grant
             is not where the pull is
    asked    Henri, 2026-08-26 — "How does programs get their
             restrictions?  Since I think that this should work on the
             idea that user always pulls, never need to start the
             program themselves."  Then: "Do a card for the resolver."
    see      card:keep.md — the session half, open at Henri's word the
             same hour; a program's grant is built (reads, writes, TCP),
             and only a launcher applies it
             card:pull.md (done/) — "a pull with no runner is recorded
             and served by no one — the default is off"; the lifecycle
             this card would complete
             node/run.sh — the one launcher, the grant baked in as three
             flags; what this card would move
             card:work-environment-ai.md §"The architecture" — the
             broker and lifecycle; the *suspected* design this card must
             not adopt on its say-so (manifesto)
             card:cords.md — the sitting limit and the andon: the other
             things that would have to know a resolver is running
             card:grant.md (done/) — the leash wraps the fence; a
             resolver is a third thing the leash would have to wrap, or
             be

## What it is

Two halves of one gap.  **Who starts** — the pull is one line appended
to a ledger; nothing watches the ledger, so a pull with no runner is a
line and nothing else.  **Who restricts** — `keep` confines a program
from outside, which is right, but "outside" today means a shell script
a person runs, so the grant is a property of *how it was started*, not
of *the program*.  Start it another way and there is no grant.

Henri's frame closes both at once: if the person only ever pulls, then
the pull *is* the launch, and whatever serves a pull that has no runner
is the one place a program is ever started — so it is the one place the
grant has to be applied.  The grant rides the pull path.  A session
that also pulls, rather than starts, cannot launch anything unconfined
because it cannot launch anything at all — which is `keep`'s session
half by a different door.

## What the shape would be, and what it is not yet

Named so the first measurement has something to disagree with, not so
it is built:

* **A grant beside the program, not in a command.**  Today it is three
  flags in `run.sh`.  It would be something a resolver reads from the
  program's place — the program never sees it, cannot widen it, and the
  person can read it as a plain file.
* **A resolver outside the session's write access** — like the fence,
  like the protected set.  A resolver a session can edit is decoration.
* **The resolver is the first long-running thing tend would own.**
  Something has to watch the ledger — a poll, `inotify`, a hook on
  `pull` itself.  Then the leash's wall budget bounds the *resolver*, not
  the program, and the sitting limit has to know whether a running
  resolver counts as a sitting.  This is the cost, and it is the part a
  measurement should size before a line is written.

**What it must not become**: the capability broker with a picker and
handle types, built because the name "resolver" sounds like one.  The
manifesto forbids adopting a suspected design on its say-so, and
`work-environment-ai` marks the broker suspected.  This card owes one
thing: a pull that starts a program *under its grant* when nothing is
running, shown from inside the fence with `cat` of the tree refused
from the program it started.  One program, the node.  A second pulled
program is what would earn a general path.

## What would make this card wrong

If the person does start programs by hand and wants to — if the shell
line is the interface — then the grant in the launcher is exactly where
it belongs and this card is the broker wearing a small name.  Henri's
words say otherwise, and the stranger test in `vision.md` says "start a
program in it," which the day-one measurement should read again with
this card's question: is *pulling* starting?

## Day one

Measure, do not build: how a pull reaches a resolver on this machine
without a daemon that outlives the sitting (what `pull` could do
itself, first); what the leash and the sitting limit say about a
process that is not a session and not a program; and what
`work-environment-ai` already decided about the launch that this card
must not re-decide.  Then the smallest thing: the node, pulled, starts
confined.

## The news the same hour, kept beside the card

Henri, 2026-08-26: models run on his work laptop at 5–9 tokens/s
through SYCL — llama.cpp is reachable.  "We may be able to do a fully
local system."  Not this card's problem, and named here because it
changes who the *puller* might be: a session that is a local model is a
program tend runs, under a grant, pulled — the same shape this card
describes, one level up.  If it turns into work it is its own card.

## Day one, 2026-08-26, 13:29 — measured, then the smallest thing

Henri: *"do resolver's day one."*

**Read first.**  `vision.md`'s stranger test says "start a program in
it" — and the sentence is satisfied by a pull if the pull starts it;
nothing in it says a hand.  `work-environment-ai` decided the broker is
*suspected* and the leash grants nothing; it did not decide the launch,
so there was nothing here to re-decide.  The leash bounds *one
invocation* (900 s wall, a scope); the sitting limit counts prompts —
neither has a word for a process that is not a session and not the
command a session ran, which is what a resolver would be.

**Measured, from inside the fence**: a process started detached inside
a fenced command **dies with the command** — `sandbox.sh` runs
`--unshare-pid --die-with-parent`, and a `setsid -f` sleeper's marker
never appeared.  So the day-one question has a plain answer from this
seat: no daemon can outlive a fenced command at all.  A resolver started
by a session's pull lives inside that pull's command, bounded by the
leash's wall and killed by the fence's namespace; from a person's shell
the same thing survives and stops on idle.  Neither seat needs a daemon
that outlives a sitting, and the leash's "one invocation" already
bounds the session's case.  What `pull` itself could do first turned out
to be the whole of it.

**Built, the smallest thing** — in `node/run.sh`, where the grant is;
`node.py` untouched:

* `run.sh pull` — takes the lock non-blocking to learn whether a runner
  is up; if not, starts one detached under the same three-flag grant,
  waits for its generation to move (the node reads the ledger *at open*,
  so a pull written before that would be seen and not served), says
  what it did — and says, when `TEND_FENCED` is set, that the runner
  lives only as long as this command — then pulls.
* `run.sh run` — takes `<state>/run.lock` on an fd before the
  confinement; the runner inherits it through keep's exec and holds it
  for life.  A second `run` is refused, exit 75, "pull it instead."

From inside the fence, live: one pull started a runner and was served
by it; a second was served by the same generation (2 pulls, 1
generation); `run` while held exited 75; the runner stopped at idle and
the lock was free.  Three tests in `test_keep.py` hold it, four rows in
`tools/mutate.sh` break it (pull never starts, pull starts regardless of
the lock, run never takes the lock, pull does not wait for the open),
each red by name.  The root README's "Try it" now leads with `pull`.

**What this is and is not.**  The card's owed demonstration — the node,
pulled, starts confined — is done.  What it is not: a grant beside the
program that a resolver reads (the grant is still three flags in the
launcher), a resolver outside the session's write access (`node/run.sh`
is in the tree, not the protected set), or a general path.  Those are
the shape §"What the shape would be" named, and each waits for the
thing that would earn it: a second pulled program, and a decision on
whether the launcher joins the protected set, which is Henri's.  The
session half of `keep` is unmoved by this: a session can still start a
program some other way.  That is the card's remaining `because`.

## 2026-08-26, 13:50 — the session half: a hand that bypasses the launcher, measured and closed at the node

Henri: *"keep and resolver."*  The card's remaining `because`: a session
can still start a program some other way.  **Measured, by the ledger**
(`tools/ledger.py`, born this hour — the ledger's second read, and the
13:42 kaizen said the parser is a tool on the second ask): in 244
records since 08-25, `node.py` was started raw twice, both times by
this session, both times as a measurement.  Through the launcher, 9.
So the bypass is real and has not been used for work.

**What the bypass does**, run on a scratch state: two raw runners on
one state **both opened** — gen 1 and gen 2 — and each served the same
two pulls; one log had four `pull` lines, the other three, and the
state was whichever wrote last.  Silent, which item 14 forbids.

**Closed where it belongs — the node's own lock.**  `node.py run` takes
`<state>.lock` (flock, non-blocking) and a second runner is refused,
exit 75, "another runner holds … — pull it instead."  The lock is the
node's and not the launcher's: however the node was started, one state
has one runner.  `run.sh`'s lock stays — it is the launcher's runner
*detection* on a different file and does not conflict.  Rule 1 is
kept: the node does not bound its own *reach*; it refuses to be two.
`test_node.py::test_one_state_has_one_runner`; the row `node: the
runner lock never taken` is red by name.

**What stays open**: a session can still start the node raw *when no
runner is up* — unconfined, since only the launcher applies the grant.
That is the true session half, and it is `keep`'s: the fix is not in
the node or the launcher but in what a session may execute, which is a
row of the fence or keep on the session.  Named; not this slice.
