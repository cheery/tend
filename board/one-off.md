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

## Open — as written, before the talk below

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

## Talk — 2026-09-25, the answers

*A session's answers to the four, at his "Do you have ideas on the open
questions?  I think that file removal is particularly good thing to
discuss.. The standard behavior on that is to mark files for removal
before they're removed actually (moving them into trashbin -behavior)..
but how does a process show what is changing on the system?"*

1. **Effects.**  A process with effects does not perform them; its
   output is the changeset it would make — *these 214 files, 3.1 GB,
   removed* — shown on the canvas before anything happens.  Applying
   is a separate, uniform step (a courier), the one place effects
   happen.  Prior art: Terraform's plan and apply, git's staging area,
   `make -n`; in this tree, `proposals/` landed by a hand, and
   `deliver.sh` already called the courier.  keep enforces the split
   for free: a native process can write only its state directory, so
   it cannot remove your files — only write down that it would.  The
   trash is how the courier removes: before (the plan shown), during
   (only the courier acts), after (the reversible undone).  Each effect
   is marked reversible or irreversible — a removal to the trash is the
   first, a sent mail the second.  A plan carries what it saw (a hash
   per file) and a line whose file changed since refuses at apply,
   saying why.  A kept process pulled again plans afresh against
   today's state.  A guest (a Linux program) writes no changeset: it
   runs over an overlay, whose upper layer is the diff, committed or
   thrown away — from the person's side, since a namespace cannot nest
   inside the fence (`spec/os.md`, measured 2026-08-31).
2. **Staleness.**  The grant is to tend what the dependency list is to
   make: it says what a process may read.  It is an upper bound — a
   grant on a whole directory makes every edit in it stale — so it is
   the first form, and what was actually read the precise one.
3. **Similar output.**  A kept process with holes is a function; "the
   same again for this folder" is a copy with a hole filled — in Kude,
   an ordinary function with typed parameters.
4. **The shell.**  Kept: a command is the smallest process, run under a
   grant, and one wanted again is promoted to a kept node with its
   grant and inputs recorded.  The history becomes candidates.

henri: This is a good idea. and others three seem like good answers as
well. — 2026-09-25

**Auto-apply.**  Asked whether an apply ever happens without the
person: henri: Yes. reversible operations could be auto-applied.  It's
sort of an interesting idea.  The action and changeset would become a
log-item. — 2026-09-25

*A session's reading of the log-item, his to strike.*  Each apply is
one item: which process, the changeset, who applied it (the person, or
a grant for a reversible one), and the reverse changeset.  Undo is
then read off the log, not the trash's own memory, and an irreversible
item simply has no reverse.  It is the same timeline `card:canvas.md`
asks for — a death, a cord pull and now a change to the machine, seen
in one place — and "won't do anything unexpected silently" held by
construction: a change that is not a log item did not happen through
tend.

*(question, his call — the `done` line above: sign it as it stands,
change it, or refuse it?)*
