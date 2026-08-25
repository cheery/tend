# keep — a person's data sits in the open to whatever runs here

    status   open
    because  nothing on this machine scopes what a program or a session
             may read; the fence bounds reach by directory, but the
             directory is the person's whole tree, their state and the
             tree next door, and inside it everything is ambient — a
             program tend runs gets whatever the session that launched
             it can reach, having been handed nothing.  "How are users'
             data protected from programs?" (spec/os.md), and Henri,
             widening it: "by anything really" — a session, another
             program, the environment itself.  And `vision.md` asks the
             hard half: the person must still read their data as plain
             files, so the boundary cannot be encryption alone — it must
             let the person in while keeping the program out
    asked    Henri, 2026-08-25 — "create the card for 'how are users'
             data protected from programs?', or well, by anything
             really"
    see      spec/os.md — open problems 1 and 2 ("how are users' data
             protected from programs?", "how are programs protected and
             installed?"); the `because`
             card:work-environment-ai.md §"The architecture" 3 and
             §"Answers to the original open problems" 1 — the capability
             broker and powerbox, which that card calls *not an open
             problem but the first architecture decision*; the suspected
             fix this card must not adopt on its say-so
             card:fence.md, card:grant.md — reach and budget are bounded
             already, but coarsely: by directory and by cgroup, not by
             what data a program was given
             card:pull.md (done/) — the first program reaches only its
             own state file, because it was written to; nothing stops it
             reaching the rest.  The smallest instance of the property
             this card wants made general and enforced
             vision.md — "won't trap your work — plain files you can
             read without it"; the tension the boundary must hold

## What it is

Ambient authority.  Every process here runs with the full reach of
whoever launched it: a session reads any file it can reach, and a
program the session starts inherits that reach whole.  Nothing asks
*what was this given?* — the answer is always *everything in the
directories the fence left open*.  The capability model the architecture
sketches (a node gets a handle only by explicit grant; the picker click
*is* the grant) is the opposite stance, and tend has none of it.

## Measured, 2026-08-25, from inside the fence

A process here — a "program", though today it is the session's own
shell — reading files it was never handed:

| it was never given… | can it read it? |
|---|---|
| the leash ledger, another mechanism's private log | **yes** |
| another sitting's gestate state | **yes** |
| any file in the whole tend tree | **yes** |
| the tree next door (`~/gestate`, read-only but readable) | **yes** |
| `~/.ssh`, `~/.bashrc` | no — the fence's empty home |

So the fence's win is real and **directory-coarse**: it removes the home
and the secrets that live there, and inside every directory it leaves
open, nothing is scoped.  The person's data that lives in an open
directory — the state, the ledgers, the trees — is readable by any
program that runs, in full, ambiently.  That is the problem, and it is
one bind below the fence, not beside it: the fence says *which
directories*, and this card asks *within them, what was this program
actually given*.

## The tension that makes it hard

`vision.md`: *plain files you can read without it.*  The obvious answer
to "protect data from programs" is to make the data unreadable —
encryption, a private store — but then the person cannot read it either,
and the vision's promise breaks.  So the boundary is not secrecy; it is
**authority**: the same plain file, readable by the person by default
and by a program only if the program was handed it.  That is the
powerbox's shape and the reason the fix is a grant model and not a
vault.  It is also why this is hard: the enforcement is on the
program's reach, not on the bytes.

## What would make this card wrong

If no program tend ever runs touches the person's data — if the node
and its successors only ever read what they wrote — then ambient read
authority is a hole nothing falls into, and the fence's directory
grain is enough.  But `pull`'s node already reads and writes under a
shared state directory beside the leash's ledger and the sitting clock,
and the next node will want to read another's output; the moment two
nodes share a directory, "it can read anything in it" is a program
reading another program's data, which is exactly problem 1.  The
measurement above is that moment already arrived for the session.

## What it must not become

The whole capability broker, built in one card.  `work-environment-ai`
marks the powerbox *suspected*, and the manifesto forbids adopting a
practice on another design's say-so.  This card names the problem and
owes the first small enforcement that proves the grain finer than a
directory — one program that can read only what it was handed, and is
shown, from inside the fence, unable to read the file beside it.  The
broker, the picker, the handle types are downstream cards.  A card that
tries to answer problems 1 and 2 and the language at once is the OS
phase wearing a small name, the same failure `pull` was held back from.

## Where it sits

Placed at 2 by a session, below `work-environment-ai` and above the
count-only cards, because that card calls this its *first architecture
decision* and *everything else is downstream of it* — so by its own
words this ranks above the restraints already built and observed.  The
placing is the session's; the tiebreak is Henri's, and this is his to
move.
