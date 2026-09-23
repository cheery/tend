# kude — Kude writes a line filter and a two-party protocol, and nothing in this tree or on his desk uses it yet

    status   open
    because  card:protocol.md named its own failure in its last
             section: "If the `done` line runs and nothing in this
             tree, or on his desk, ever hands a program to the checker
             afterwards, the card was built for its own joy."  On
             2026-09-23 both of its cards closed at his "This works" —
             `gcd`, the Bank and Client joined by a cut, and `nl` over
             a hundred thousand lines — and the next road is not
             chosen: five are drawn (below), each a different answer
             to what Kude is for, and a session picking one would be
             deciding that.  Henri, the same minute: "Lets leave a
             card where to continue from, then we can stop."
    done     (none yet — the road is his to pick; a session drafts the
             line for the road he picks, and nothing is built before
             his `henri:` line is on it, by card:done-when.md)
    asked    Henri, 2026-09-23 — "This works.  Lets leave a card where
             to continue from, then we can stop."
    see      card:protocol.md and card:real-program.md (both done, the
             days and what each measured), kude/kude.py (its header is
             the language as built, and its "Not built"), kude/*.kude
             (the three programs), test/test_kude.py, tools/mutate.sh
             (the Kude rows), doc/notes/lineaarilogiikka-kieli-keskustelu.md
             (why), card:edge.md (this tree's untyped wires)

*(question, his call — which road next?)*

## Where it stands — 2026-09-23

Read first: the header of `kude/kude.py`, then the three programs.

    python3 kude/kude.py check kude/bank.kude
    python3 kude/kude.py run kude/gcd.kude 'gcd(1071, 462)'
    python3 kude/kude.py run kude/bank.kude 'main()'
    seq 5 | python3 kude/kude.py run kude/nl.kude 'main(io)'
    python3 -m pytest -q test/test_kude.py        # 54, all green
    grep -P '^test/test_kude\.py\t' tools/mutate.sh   # 22 rows, all red when last run

Built: deterministic clauses with modes, exactly one clause holding
(checked by walking every case of the guards); channels typed by
session types, walked through each clause; the cut, with duality from
the callee's types and the tree that makes deadlock impossible; a
runtime of coroutines and queues, one thread; the terminal as a channel
at `Console`; `Int` and `Str`; tail calls.  985 lines of Python, one
file.

Known limits, each measured or held by a test: the guard check gives
one relation per pair of terms and does not relate pairs (`a < b`,
`b < c` making `a < c` is not seen); a call that is not last is a Python
frame, so 1000 deep is a run error; a cut side is one call; one channel
from the shell; no text in the shell's call; no way to read a number
out of text.

## The roads — none chosen

1. **More of a real language.** A file as a channel (opening one is a
   cut with the file system as the other party); `num` to read a number
   out of text; a cut side of more than one goal.  First step: `wc` in
   Kude over a file named on the command line.
2. **Channels over channels, and `!A`.** A server that hands each
   client its own line, and a service many clients call — the shape of
   every node in this tree that answers more than one pull.  First
   step: the bank as a `!A` service with two clients, deadlock-free by
   the same check.
3. **This tree's own wires.** `pull` and `connect` are typed by nothing
   (`card:edge.md`); the ask node's conversation written as a Kude
   type, and one end of it — the smallest — written in Kude and run
   against the real node.  This is the road that answers "What would
   make this wrong" directly.
4. **A model writes Kude.** Give a door model a session type and ask it
   for both parties; count what the checker refuses, what runs, and
   what the model fixes from the refusal's words alone.  The
   transcript's bet — "protocol as a type is one of the few things
   that scales with the amount of generated code" — measured, with
   `tools/compare.py` as the instrument.
5. **A compiler.** The runtime is an interpreter; the paper's form is a
   compiler's intermediate representation.  Compile a checked program
   to C, or to something the tree already runs.  The largest road and
   the one least asked for.

A session's reading, offered and not decided: 3 or 4 is where Kude
stops being built for its own joy — 3 makes the tree use it, 4 says
whether it matters to anyone; 1 and 2 are what either of them will
need along the way, and can be pulled in as the road asks.
