# kude — Kude writes a line filter and a two-party protocol, and nothing in this tree or on his desk uses it yet

    status   doing
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
    done     when the conversation between a node and the llm it pulls
             — pull, wait until it answers, one question, one answer,
             let go — is written as a Kude session type, and a node
             that holds that conversation is a Kude program, run from
             his shell against the real llm and getting its answer;
             and a program that asks before the llm answers, asks
             twice, or never lets go is refused at the check naming
             the type and the clause; and a door model, given that
             session type and nothing else, writes the node too: every
             try it makes goes through the check, and the count —
             refused, fixed from the refusal's words alone, run against
             the real llm — is written into the chapter, whether or not
             a try passes.  (a session's draft, 2026-09-23, for road 3,
             his pick, and road 4 added at his "We could add into the
             chapter 1: The model writes a program"; henri: signed
             2026-09-23 — "Tend's own wire in Kude", then "Model writes
             the same node", chapter 1 of the narration in journal.md)
    asked    Henri, 2026-09-23 — "This works.  Lets leave a card where
             to continue from, then we can stop."
    see      card:protocol.md and card:real-program.md (both done, the
             days and what each measured), kude/kude.py (its header is
             the language as built, and its "Not built"), kude/*.kude
             (the three programs), test/test_kude.py, tools/mutate.sh
             (the Kude rows), doc/notes/lineaarilogiikka-kieli-keskustelu.md
             (why), card:edge.md (this tree's untyped wires)

*(question, his call — which road next?  henri: Tend's own wire in Kude
2026-09-23)*

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

## Chapter 1, day one — the plan, 2026-09-24

A session's draft, read off `kude/kude.py` and `ask/ask.py` and not yet
built; the sitting's clock ended before code.  The llm wire goes in
beside `Console`: a type the checker owns, which a program cannot
define, and a runtime party that plays it the way `ask.py` does today.
The node's side:

    type Llm   = +{ pull: Wait }.
    type Wait  = &{ up: +{ ask: !Str . ?Str . LetGo }, down: ?Str . LetGo }.
    type LetGo = +{ let_go: end }.

`pull` takes the shared flock on the edge in `$TEND_PULLS`; `up` is
`/health` answering and `down`, with its reason, is the llm's death in
`stopped` or the wait running out; `ask` and a Str is the one POST, and
the answer comes back as a Str; `let_go` closes the edge.  With that
type, the done line's three refusals need no new check: an ask before
`up` is an action `Wait` does not offer, a second ask is one `LetGo`
does not offer, and a node that never lets go ends with its channel
open, which the check already refuses.  Red first, in
`test/test_kude.py`: the three refusals, the node checking, and a run
against a stand-in llm like `test/test_launch.py`'s `_Llm`.  Then a
node directory whose program is `kude.py run`, run from his shell
against the real llm.  Open for his eye: the labels' names, and
whether `down` belongs in the type or should end the run.

## Chapter 1, day one — the wire, built, 2026-09-24

At his "I extended the time.  Continue on building the wire."  The plan
above, with its two inner names prefixed — `LlmWait`, `LlmLetGo` —
because the world's names cannot be defined by a program, and a bare
`Wait` would have taken a common word from every program:

    type Llm      = +{ pull: LlmWait }.
    type LlmWait  = &{ up: +{ ask: !Str . ?Str . LlmLetGo }, down: ?Str . LlmLetGo }.
    type LlmLetGo = +{ let_go: end }.

`kude/kude.py` carries them beside `Console`, and `LlmWire` plays the
llm's end the way `ask/ask.py` does: the shared flock on the edge,
/health, a death in the llm's `stopped`, keep's refusal of the port,
one chat completion, the edge closed at `let_go`.  Nothing in the check
learned about the llm; two refusals' words changed — a world's name says
whose it is (the terminal's, the llm wire's), and a label refusal at a
named type names it (`llm's LlmWait = &{…}`) — so each of the done
line's three refusals says the type and the clause:

    ask is not a branch of llm's LlmWait = &{up: …, down: …}      (asks early, clause main)
    ask is not a branch of llm's LlmLetGo = +{let_go: end}        (asks twice, clause asked)
    llm is at LlmLetGo when the clause ends                       (never lets go, clause asked)

The node is `ask-kude/`: `ask.kude`, three clauses, and a grant like
ask's (`pull llm`, `connect 18080`) whose program is `kude.py run
ask.kude 'main(llm)'`, with the checker read from the tree and not copied.
`tools/launch.sh ask-kude check` is green from a session's seat except
for the state, which it says it cannot see from here.

Measured: `test/test_kude.py` 64 (ten new: the node checks, the three
refusals, the world's names, a run against a stand-in llm that saw the
edge held while it was asked, `let_go` letting go before the run ends,
a death, no edge, a wait run out), red first on `no type Llm`;
`test/test_launch.py` two flow tests, the node under keep against the
stand-in and without `connect`; five mutate rows, all red.

**Run from his shell against the real llm, 2026-09-24**, the done
line's words and his hand — `tools/launch.sh ask-kude run`, the edge
taken 18:11:51, the answer in the log 18:13:49 (two minutes: the llm
loading its model because it was pulled), `stopped` saying "exited 0:
ask-kude stopped by itself".  His paste:

    answer = The word "tend" is used to describe the act of caring for something, moving in a specific direction, or having a natural inclination toward a certain behavior.

A dictionary entry, which is the cold arm `card:material.md` measured on
2026-09-04: ask-kude's grant has no `material` word, so the llm answers
about the English word and not this tree.  That is the answer to the
question it was given, and the done line asks for its answer, not a good
one.  Above it in his paste, keep's deprecation warning — F030, resolved
by his second run at 18:28:51: the same answer word for word (temperature
0), and no warning before it.  So the
done line's first half is met: the type, the node in Kude, the run
against the real llm, the three refusals at the check.  Its second half
— a door model writing the node, its tries counted — is not begun.

Also not built: the answer is only the log's line (ask/ writes
`state/answer`); a node whose llm is down exits 0, since a Kude program
chooses no exit status; the question is a literal in `ask.kude`, since
the shell's call carries no text; the token cap's cut is marked in the
answer and no test holds it; and the door model writing the node,
the chapter's second half.
