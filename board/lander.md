# lander — a vetted change waits, silently, between the gate and the machine

    status   open
    because  a commit that passed the gates is not in force until a
             person runs one line, and nothing but the person's memory
             carries it there.  On 2026-08-27 the lamp's fix was
             committed through the gate at 17:0x and "installed" had
             not happened when the cards were checked for done —
             `tools/install.sh --check` found the drift, the session
             asked, a second sudo landed it.  Before the install existed
             the same wait was a branch waiting on a merge, and twice
             that day a session reached across the boundary rather than
             wait (doc/kaizen/2026-08-27-0710.md, item 2).  The wait is
             the one silent state the install arrangement has, and the
             reaching is what a silent wait does to a session
    asked    Henri, 2026-08-27 — "Write the lander card"; the shape was
             called card-shaped by the 0710 kaizen ("an unfenced actor
             that fast-forwards main after the gates pass"), and
             card:install.md named it as the residue when it closed
    see      card:install.md — the mechanism this waits behind, and its
             own line: "the install is the person's hand, or a lander
             outside the fence — never the restrained party installing
             its own restraint"
             tools/install.sh — `--check` is where the drift is read
             today, from either side of the fence
             tools/resolve.sh — the unfenced-actor shape that already
             exists: a hook on the person's side that starts what a
             session may not, on the session's prompt, never as a daemon
             tools/kaizen.sh — the lamp shape: lights while something is
             owed, says what, never acts
             card:work-environment-ai.md — the boundary a lander must not
             become a door through
             doc/kaizen/2026-08-27-0710.md, doc/kaizen/2026-08-27-1650.md
             — the reaching and the drift, measured

## What it is

Two waits, and `install` dissolved one of them.

1. **Branch → `main`.**  Until 2026-08-27 a change to a restraint went
   clone → branch → Henri's merge, and the wait for the merge is where
   sessions reached across.  Since `install` day two a session edits a
   restraint in the tree and commits to `main` through the gate; the
   branch path remains only for a tree whose own copies are what runs.
   This half is mostly gone, and this card does not rebuild it.
2. **`HEAD` → the prefix.**  A commit on `main` is vetted and not in
   force until `sudo tools/install.sh`.  Nothing lights; `--check` says
   so only when run.  This is the wait the card is about.

What a lander would be is *an actor outside the fence that notices
`HEAD ≠ prefix` and does something about it* — and "something" is the
decision this card exists to hold open until the count is in:

* **A lamp** — the kaizen lamp's shape: at every prompt, if the prefix
  is behind `HEAD`, say so and which files; act never.  The person still
  turns the key, and the silence is gone.  Cheapest; may be the whole
  card.
* **The andon** — ring when the drift has waited longer than a sitting.
  Loud, and only once the lamp has shown that drift outlives sittings.
* **An actor that installs HEAD when the gates are green** — the 0710
  shape.  `card:install.md` permits it by the letter ("or a lander
  outside the fence") and forbids it by the sentence after: the gates
  are tests, tests are session-writable, and a commit that weakens a
  test and a restraint together passes its own gate.  The person's
  review is what stands between a session's commit and the machine;
  an actor that removes it is a door, however many tests it runs.
* **An actor that installs only what the person has marked** — a
  signed tag, a note, a commit made by his hand.  One line of his per
  change either way, so it buys nothing over `sudo tools/install.sh`
  unless the marking is cheaper than the sudo, which it is not.

## What would make this card wrong

If the drift never outlives a sitting — if `installed`'s date is never
more than a sitting behind `HEAD`'s commit time — then the lamp is the
whole card and an actor is building what nothing needs (manifesto rule
1).  **That is a count, and the lamp is what takes it**: every prompt
at which the prefix is behind, logged with how far behind, for a week.
The card's day one is therefore the measurement and not the actor.

## What it must not become

* **A session's install.**  Any path by which a session's commit
  reaches the prefix with no person between is the door
  `card:work-environment-ai.md` was opened to close.  The actor, if it
  ever exists, is run by the person or by a hook on the person's side
  on the person's prompt — the resolver's shape — never a daemon that
  holds root and reads a session-writable tree.
* **A second gate.**  The gate is `tools/pre-commit.sh` and the suite;
  the lander does not re-decide what is vetted, only whether what is
  vetted is in force.
* **A nag.**  The lamp says the prefix is behind and which files; it
  does not say what to do about it at every prompt beyond the one
  line.

## Where it sits

Placed last, unplaced, by the session that wrote it at Henri's word;
the tiebreak is his.  Its day one is the lamp — which is also the
count that would make the rest of the card wrong — and the lamp is a
slice of `tools/install.sh --check` with a `--hook` form, on the
person's side like the other lamps.  Not built with the card: a card
that arrives with its own solution has already decided.
