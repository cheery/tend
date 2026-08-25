# pull — tend runs nothing but its own suite, so the stranger has nothing to start

    status   open
    because  `vision.md`'s stranger test — "start a program in it, see it
             stop when they stop pulling, and find out what it did" —
             has no program to run: everything in this tree governs, and
             nothing is governed; the fence, the leash and the cords
             have had no caller of tend's own, and the properties on
             `spec/os.md` are cited and not built
    asked    Henri, 2026-08-25 — "Put those three on the board as cards.
             They are excellent waypoints."  The third of the three
    see      vision.md §"Ease of use" — the stranger test, which is this
             card's acceptance
             spec/os.md — items 8 (opens where it was left), 9 (may
             crash, may not hang), 13 (starts by pull; quits when nobody
             pulls), and the third open problem (how programs stay fast
             if closed the moment they are not needed)
             card:work-environment-ai.md §"The architecture" 1 and 4 —
             the node, and state as a plain file, not a memory image
             doc/experiments/2026-08-25-both.md — programs-first has a
             fence and no program of tend's own to put in it
             tools/leash.sh — a hang is a crash, exit 124; already the
             enforcement for item 9

## What it is

One node.  It opens where it was left — its state a plain file a
person can read without it; it runs while something pulls it and quits
by itself when nothing does; it may crash and may not hang; and a
stranger can start it, stop pulling, and read what it did.  No
language, no broker, no bundle format beyond a directory: the smallest
thing that is a program of tend's own, run under the fence and the
leash, so that every mechanism here has, for the first time, a caller
this tree wrote.

## What would make this card wrong

If the first node needs a vocabulary — a manifest, a capability list, a
scheduler — before it can run at all, then the pull lifecycle is not
separable from the broker and this card is the broker wearing a small
name.  The test is whether the node is under a hundred lines and
answers the stranger test as written.

## What it must not become

Bigger than one node.  The list on `spec/os.md` has sixteen items and
this card builds three; the temptation will be to build a fourth
because it is near.  A fourth is a card.

## 2026-08-25, afternoon — built: one node, and the stranger test answered

Henri: *"lets do pull."*  `node/` is the node — the directory is the
whole bundle, no manifest, no language (the card's line kept).
`node/node.py`, 86 lines of code: `run` opens where it was left and
serves pulls until they stop, then quits itself; `pull` is one pull;
`status` says what it did.  The three properties it is built to carry,
each with a test:

* **Opens where it was left** (item 8): state is one plain JSON file —
  `generations`, `pulls`, `runtime_s`, a capped log — restored on every
  `run`.  `test_it_opens_where_it_was_left`: a second generation keeps
  the first's tally.
* **May crash, may not hang** (item 9): the run loop always ends when
  the pull ledger goes quiet for `--idle` seconds; the leash's wall
  budget bounds it besides.  `test_run_serves_pulls_then_stops_itself`
  asserts the self-stop, and that it did not hang.
* **Pull lifecycle** (item 13): a pull with no runner is recorded and
  served by no one — the default is off.  `test_a_pull_with_no_runner_
  is_not_served`, `test_a_run_nobody_pulls_stops_on_idle`.

**The two writers are kept apart.** `pull` only ever appends one epoch
line to `<state>.pull`, a plain readable ledger; `run` only ever writes
the state file, reading the ledger's length.  No shared-write race, and
the ledger is itself a record a person can read.  Item 14 kept: a
corrupt state file raises, it does not reset the tally to zero.

**The demonstration, the manifesto's sense — a stranger, told nothing:**

    $ node.py run --idle 2 &
    node: gen 1, state … — pull it, or it stops after 2.0s idle
    $ node.py pull
    $ node.py pull            node: pull, total 2
    …stops pulling…           node: stopped — nobody pulled for 2.0s.
    $ node.py status          node tally: 2 pulls over 1 generations, 2.9s

It ran under `leash → sandbox` like every command here — the ledger has
its line — so the fence and the leash have, for the first time, a
caller this tree wrote.  That is the sentence the card was for.

**What it is not, held to** (the card's "what it must not become"): one
node, not four.  No content-addressed identity yet (the hash is the
store's card, not this one), no supervisor beyond the leash, no
capability broker — a node that reaches anything is `work-environment-
ai`'s piece 3, and this one reaches only its own state file.  The pull
ledger grows without compaction; that is a line for a later node, not a
vocabulary this one needs to run.

**One real tension, named:** a node genuinely pulled past the leash's
900 s wall budget is exit 124 — a crash, by item 9's own rule, but not
the crash the rule means.  That is the budget being the session's grant
applied to a program, which is `grant`'s dial pointed the other way;
the size of a program's budget is its own card when a program needs
more than a session's default.  Recorded, not solved.
