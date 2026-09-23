# real-program — Kude checks and runs protocols, and no real program can be written in it

    status   doing — the done line signed 2026-09-23
    because  Henri, 2026-09-21, in the transcript card:protocol.md
             grew from: "Minua esimerkiksi kiehtoisi paljon juuri nyt
             'design 2' vietynä niin pitkälle että sillä voisi tuottaa
             oikeita ohjelmia."  After card:protocol.md's day three,
             2026-09-23, Kude runs the transcript's Bank and Client
             joined by a cut, and that is all it can run: a
             conversation of 1000 rounds is a run error because every
             recursion is a frame, a message is an `Int` and nothing
             else, and a program touches nothing outside itself but
             one scripted channel of numbers — no line read, no line
             written.  A language whose every program is a toy stays
             a theory with a test suite, which is the failure
             card:protocol.md names in its last section.
    done     when a Kude program that does a job he would otherwise do
             with a shell tool — numbering the lines of whatever is
             piped to it — runs from his shell over a hundred thousand
             lines without the runner running out of depth; its reads
             and writes pass through one channel whose session type the
             check walks like any other, so a program that writes after
             closing, forgets to close, or sends a number where text is
             due is refused at the check naming the type and the
             clause; and the files card:protocol.md left still check
             and run.  (a session's draft, 2026-09-23, naming no
             function; henri: signed 2026-09-23)
    asked    Henri, 2026-09-23, ~15:20 — "lets create a card that maps
             the next direction, and immediately do it.", after the
             three directions offered at card:protocol.md's day three:
             real programs, the tree's own wires, and a model writing
             Kude with the checker counting its mistakes — the first
             recommended because the other two stand on it
    see      card:protocol.md (days one to three, and "What would make
             this wrong"), kude/kude.py (its header's "Not built"),
             doc/notes/lineaarilogiikka-kieli-keskustelu.md (§3: the
             paper's `st → st'` thread, "a linear resource kept linear
             by convention alone"), card:done-when.md (the line above
             waits for his hand)

*(question, his call — the `done` line above: sign it as it stands,
change it, or refuse it?  henri: signed 2026-09-23 — "Sign as it
stands", his pick when asked in the session)*

## The map

The direction is the one card:protocol.md's day three recommended:
Kude until it writes a real program, because the tree's own wires and
the measurement of a model writing Kude both stand on it — a wire in
this tree carries text and runs for days, and a model asked to write a
program should be asked for one that does something.

**Day one — the world as a channel.**  The paper threads the world
through a program as `st → st'`, used once and replaced, linear by
convention; here it is a channel from the shell at a type the runner
knows, `Console`, and the partner at its other end is the terminal:

    type Console = +{ read: Input, write: !Str . Console, close: end }.
    type Input   = &{ line: ?Str . Console, eof: Console }.

So the linearity the paper keeps by convention is the check's: a write
after `close` has no place in the type, and a clause that ends with the
console open is refused as any channel left unfinished is.  With it:
`Str` beside `Int` as a value and a message (`!Str`, `?Str`, a string
literal, a head input `s: Str`, an output `s: Str`), checked — a number
sent where text is due is refused naming the type; the builtins a line
numberer needs (`cat`, `show`, `len`); and tail calls, so a clause whose
last goal is a call that hands back exactly the clause's outputs runs
in the frame it is in.  The program is `kude/nl.kude`.

**After that, not promised** — each its own day, and each his to pick:

- a file as a channel — opening one is a cut with the file system as
  the other party;
- a channel sent over a channel, so a server can hand a client its own
  line;
- `!A`, a service many clients call — the shape of every node in this
  tree that answers more than one pull;
- the ask node's wire (card:edge.md) written as a Kude type, checked;
- a door model writing both parties of a protocol in Kude, and the
  checker counting what it refuses — the transcript's bet measured.

The map is a list of roads, not an order; the order is his.

## Day one, landed — 2026-09-23, the same sitting, at his "immediately do it"

`kude/nl.kude` numbers the lines piped to it:
`seq 100000 | python3 kude/kude.py run kude/nl.kude 'main(io)'` ends
with `100000 100000`, in 1.1 s from this seat.  The program is four
clauses: `main` hands the console to `nl`, `nl` asks for a line, and
`line` is the answer, one clause for `line` and one for `eof`, because
a branch offered is a clause each.

What it took, each in the check and not only the run: `Console` and
`Input`, the terminal's types, which a program cannot define; `Str` as a
value, message, literal, head input and output, with every variable
given one type and a value where the other is due refused naming both
— `io ! 5` is *io is at !Str . Console, which sends Str, and 5 is Int*;
`cat`, `show` and `len`; and tail calls — a clause whose last goal is a
call handing back exactly its outputs goes round in the same frame.
Day three's measure was 400 rounds and a run error at 1000; a bank now
talks with its client for a hundred thousand rounds.  A call that is
not last is still a frame: 500 deep runs and 1000 is a run error,
measured and in the header.  One more change beneath: a choice now
travels as a tagged label, so it can never be mistaken for text.

Twelve tests.  Eleven were written before the program: ten red, and one
green on purpose — a recursion that is not a tail call, guarding the old
path through the refactor.  The twelfth, message types compared at a
cut, was written after the program, when reading the diff showed
nothing tested it; its mutate row is what says it bites.  Seven mutate
rows, and day three's wrong-kind row re-anchored to the new code; all
twenty-two Kude rows re-run after the refactor, all red.  The
protocol card's files still check and run.

The `done` line, read against this: nl over a hundred thousand lines,
refusals naming type and clause for write-after-close, left-open and a
number where text is due, the old files green — all true from a
session's seat.  "From his shell" is his; the card stays `doing` until
he has run it.
