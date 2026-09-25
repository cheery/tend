# one-off — a task done once on a computer is a command that vanishes

    status   open
    because  Henri, 2026-09-25, reading the bound on vision.md: "We're
             thinking about processes as processes, but how does it
             work on tasks that need to be done once, on a computer?"
             A one-off task today is a command typed and run: the
             output lands somewhere, the way it was made is gone, and
             a similar output next month is made again from memory.
             Tend's model so far is the long-lived program a person
             pulls; a task that is done once has no place in it.
    done     when a task done once from the canvas leaves a kept
             process behind, and pulling it again gives the output
             again or says why it cannot.  (a session's draft,
             2026-09-25; unsigned)
    asked    Henri, 2026-09-25 — "yes, bound to vision.md and write
             the card."
    see      vision.md §"What it will be" (the bound: work from the
             canvas), card:edge.md (nodes pulling nodes, the canvas at
             the end), ask/ (a question in, an answer out, idled out),
             ask-kude-model/node.kude (a model asked for an answer that
             wrote the process instead), spec/os.md properties 5, 6
             and 15

## His words

2026-09-25: It suggests we want to change the philosophy of operation
here.  What user builds is not a command to execute, but a process that
delivers what they want.  And that process is something stored for
future in case user wants similar output..  This resembles the idea
there is in makefiles, but on a different level.

## What the tree already has — a session's reading, his to strike

- `ask/` is a one-off task run as a process: a question in, an answer
  out, and the node idles out when nobody pulls.  What it lacks is the
  keeping — nothing says the answer can be had again.
- In `card:kude.md`'s chapter 1, the model handed the task did not
  return an answer; it wrote `ask-kude-model/node.kude`, a kept process
  that gives the answer each time it runs.  The idea above, done once,
  with a session as the author.
- `card:edge.md`'s value stream — nodes pulling nodes, a directed
  acyclic graph with the canvas at its end — is a makefile's shape: a
  target, what it depends on, and a recipe.  Where it differs from
  make: the unit is a node with a grant and a state, not a file and a
  shell line, and the demand is a pull that lasts, not one invocation.
  The nearest prior art is Nix (an output as a derivation, kept and
  known by what went into it); the most successful everyday one is the
  spreadsheet, where the person builds the process and the answer comes
  with it.
- Lean says the same from its side: improve the process, not the
  inspected product.  A kept process is what standard work and kaizen
  would act on.

## Open — none decided

1. **Effects.**  "Deliver this output" fits; "send this mail", "delete
   these files" does not.  A process whose worth is what it *did* needs
   another story than one whose worth is what it *made*.
2. **Staleness.**  When is a kept output still good?  Make reads
   times, Nix hashes inputs; `spec/os.md` property 6 (a version that
   can be identified) leans to the second.
3. **"Similar output."**  A kept process for a similar output has
   holes in it — parameters — which makes it a function, and may be
   what Kude is *for* on this machine.
4. **The shell.**  Does a typed command still exist?  Perhaps a
   command is the smallest process, and one worth having again is
   promoted to a kept node.

*(question, his call — the `done` line above: sign it as it stands,
change it, or refuse it?)*
