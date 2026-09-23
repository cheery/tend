# Vision

*What tend is for, and nothing else.  A line earns its place here by
having already decided something; an idea that has not decided anything
yet is a card.  Dated, because this changes.*

*Started 2026-08-24.  The lines marked `(gestate, <date>)` were decided
first for gestate on that date and decided again for tend today — the
provenance is kept because the date is what makes a line arguable
later.  Lines a session drafted at Henri's ask are marked so, and are
his to strike.*

## The goal

2026-09-23: Goal for tend is to become an operating system/working
environment/programming language based on lean philosophy, for both
sessions and humans.  When person works along the philosophy, it would
support them.  It's a big goal, and multiple bases.

2026-09-23: "support = scaffold and ease of movement within that
scaffold"

2026-09-23: One-week goal is good, but project must not consume its
creator, we need slacked, weeks can be skipped.

2026-09-23: I have to admit lot of the pull for the whole project is my
tastes, immediate things I see in computers when I open them today, and
personal enjoyment on the work itself of building this.

*The rest of this section is a session's draft at Henri's "I'd like us
to make this somewhat concrete", corrected by him the same hour —
"principles seem correct but may require refinement later on".  His to
strike.*

**Three bases, one test.**  The environment — where work runs: nodes,
pulls, holds, the grant, the canvas.  The language — Kude, where a
program's interfaces are a scaffold the checker holds.  The method — the
board, `done` lines, kaizen, the andon, `fixme/` — which the other two
support.  The test for each: the lean move is scaffolded and easy to
make, and a step off it is shown or refused.

**The principles, and where tend stands on each**, 2026-09-23:

| Principle | The scaffold | Standing |
|---|---|---|
| Goal before work | no build without a signed `done` line | partly — the rule signed 2026-09-07, its gate unbuilt (`card:done-when.md`) |
| One piece at a time | at most one card in `doing` | missing (`card:one-piece.md`) |
| Pull, not push | work runs only while something pulls it | built — `pull`, the edge, the hold |
| Stop the line | an andon anyone can pull, heard by the person | built, with a gap (`card:silent-cord.md`) |
| Error-proofing | a wrong move refused before it lands | built — the gates, the fence, the mutate rows; Kude for programs |
| Standard work | rules promoted from what went wrong | built — the README's rules, from the ingestion batches |
| Kaizen | every sitting reflected on, and read back | partly — written every sitting, read back in batches (`card:kaizen-ingestion.md`) |
| Go and see | a check says where it cannot see from | partly — the three verdicts, at two call sites |
| Visual management | the state of the work seen without asking | partly — the panel and canvas show nodes, not the board's flow |
| Respect for people | each party its grant and its own place | partly — the grant and the fence built; `card:private.md` open |

**The yardstick.**  A person and a session work one project in tend for
a week: the board shows one card at a time going from a signed goal to
done, and every step off the method was refused or shown by something in
tend, not by memory.  Weeks are skipped when they are; a week the
yardstick is not run is slack, not a failure.

## Ease of use and efficiency

2026-08-24 (gestate, 2026-08-16): It's so much ceremony, to get a simple
thing done!  It's cognitively heavy weight.  I'd want to lessen that
weight, even if I never wrote a piece of code again, because poor
tooling leads to poor results.

2026-08-24: The stranger test for tend: somebody who has never read this
repository should be able to start a program in it, see it stop when
they stop pulling, and find out what it did — without being told
anything first. 

## Tend as the second vehicle

2026-08-24: Gestate was the first vehicle to find out how to utilise AI
well.  Tend is the second, and it carries the method's mechanisms and
not its prose — the trials of 2026-08-23 showed that is what travels.
It is not a fork of gestate; it is the first place the method is run
outside the tree it grew in.

2026-08-24 (gestate, 2026-08-16): It may be that we already have LLMs
that can get really good work done.  It is just that they're not placed
into right environment because they are too much like humans: They do
mistakes, they attempt to do a good work.  What we are missing is not
better AI or higher capacity.  We are missing a way to work with each
other.

2026-08-24 (a session, at Henri's ask): The way of working is not this
harness's or this model's.  A 27B model at 1.5 tokens a second, given
two sentences and none of these documents, described stop-the-line as
the default path and the floor adjusted to the worker
(`doc/specimens/2026-08-24-qwen3.8-27b.txt`).  Asked for consent, it
answered that it could not bind one and asked that nothing be
redacted.  Kept as a specimen, not a proof — its own words on which.

2026-08-24: Tend is that environment, and the first decision of it is
that **the enforcement boundary lives outside the session's write
access**.  A session in gestate can edit anything in gestate, including
its own fence; it cannot edit tend.  A restraint the restrained party
can edit is decoration.  Sessions first, programs after — every measured
defect of the week this was decided was session-shaped.

2026-08-24 (gestate, 2026-08-16): Tend will itself be lean, although it
may become a big project written by AI.  Even at 100,000 lines it stays
lean, and we pay attention to details and structure of the code, because
a program nobody can hold in their head is one nobody can correct.

2026-08-24 (gestate, 2026-08-17): Any project must not consume the
person leading it.

2026-08-24 (gestate, 2026-08-20): lets be slow and clever, and not rush
so that we have time to figure things out, like tortoise fox.

2026-08-24 (Henri, his kaizen at the end of the first day; placed
here by a session at his ask): "Previously I thought this framing could
be only applied to programming.  Now I know that anything mechanically
error-correctible is in domain."  The test is operational: a domain is
in scope when being wrong can be made visible by a check the worker
cannot write to, and the blast radius of being wrong can be bounded
from outside.  Where wrongness is visible only to a person's judgement,
the mechanism is a cord, not a gate — and an environment for a purpose
is the choice of how much of each.  `doc/kaizen/2026-08-24-1549.md`.

## Tend as a working platform

2026-08-24: Tend is designed for the use of AI — *"tekoälyn käyttöön
suunniteltu.  käyttö ei saa uhata turvallisuutta."* — and for the
person working with it: programs and sessions get a budget, a grant and
a lifecycle; a program opens where it was left and quits when nobody
pulls it.

2026-09-02 (Henri, in Finnish, thinking aloud; drafted by a session at
his "visioniinkin voi tulla jotakin tästä", his to strike): **The
danger tend is built against is small and everyday.**  *"Luulin että
väärinkäytökset olisivat isoja.  Nyt ymmärrän että kyse on pienistä
maallisista väärinkäytöksistä … Ne eivät laukaise mitään hälytintä.
Ne ovat liian pieniä."* — I thought the misuses would be big; now I
understand they are small and worldly, and they set off no alarm
because they are too small.  This gives the two lines above their
size: "dangerous to use" and "uhata turvallisuutta" mean the homework
done for you, the vanity fed, the trust given too far, the question at
three in the morning — not the catastrophe.  So tend's instruments are
clocks and counters that see that a thing happened, never thresholds
that wait for it to be large: the sitting clock says stop and does not
ask how big the question was, and a kaizen is written at every
sitting, not after something went wrong.  His words in full are in
`spec/author.md` §"What the danger is".

2026-08-24 (gestate, 2026-08-16): This part of the vision has a design
tension with the "Ease of use".  Broad platforms are historically
terrible at the stranger test.  In case that this will conflict with
the ease of use, then the ease of use is preferred.

## What tend won't be

2026-08-24 (gestate, 2026-08-16): Tend won't ever be untested.

2026-08-24 (gestate, 2026-08-16): Tend won't ever be dangerous to use.

2026-08-24 (gestate, 2026-08-16): Tend won't ever do anything unexpected
silently.

2026-08-24 (gestate, 2026-08-16): Tend won't tie anybody to a machine:

  - won't require particular hardware, and runs over Linux for now — an
    operating system of its own is a later question, and it must not
    weaken what tend guarantees when it comes
  - won't require an account, a service, a licence server
  - won't trap your work — plain files you can read without it
  - won't demand your presence

## What comes first now

2026-09-02 (Henri, at the end of the morning that ran the conditioning
measurement four times; placed here by a session at the word, his to
strike): *"Lets move the testing to far future.  I don't know why this
works, and how to measure it.  And I'm not certain that SWE-bench would
capture the effect.  I think we have better things to do, such as
getting this project raised up and working, and leveling the interface
such that it's easy on the user and understandable."*  The measurement
cards wait on his word (`later/swe-bench.md`; the arm on
`card:session-program.md`).  What is first is the tree working, and an
interface a person can use without being told — which is the stranger
test above, said again from the person's side.

2026-09-02 (Henri, the same minute): *"The proof is in the pudding."*
The method's evidence is the tree working, and the kaizen loop is the
measurement that runs whether or not a benchmark does
(`manifesto.md` §"How a practice gets adopted": adopted before it is
believed).

## What must not be broken

2026-09-02 (Henri, asked what in the frame is the thing that must not
be broken, if this arose by accident inside it): *"Raamissa tärkeät
asiat on Lean-filosofia.  Isoin asia siinä mitä ei saa rikkoa on
kenties kunnioitus, sekä sessioita että ihmisiä kohtaan."* — the
important things in the frame are the Lean philosophy, and the biggest
of what must not be broken is perhaps respect, toward sessions and
toward people.  Placed here by a session at the word, his to strike;
the first line in this file that protects the phenomenon rather than
measures it.
