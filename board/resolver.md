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
