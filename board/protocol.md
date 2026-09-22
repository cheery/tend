# protocol — a program a model writes carries its why nowhere a machine checks, and the places it goes wrong are the interfaces

    status   doing — day one landed 2026-09-22
    because  Henri, 2026-09-21, to a general session (the transcript is
             `doc/notes/lineaarilogiikka-kieli-keskustelu.md`, copied here
             verbatim at his "it'd be tend's project"): "Minulla on
             toistuvaa halua tehdä tietokoneen käyttöliittymistä, niin
             sisäisistä kuin ulkoisistakin, parempia.  Mutta olen
             alkanut miettiä mitä se tarkoittaisi?  Toisena mietin mikä
             siitä on tarpeen?"  The talk before it had said where the
             want comes from: when a session writes a program, the
             program keeps running after the session is gone, its
             *why* was in the conversation and is now nowhere, and the
             comments in it are the model's claim about the model's
             work; an interface — between a person and a machine or
             between two parts of one — is a protocol, what may be
             sent, in what order, and what is possible after, and that
             is where errors are actually made; and nothing a machine
             checks says what the protocol is.  This tree has the same
             gap in its own shape: a node pulls a node and connects to
             a port (`card:edge.md`), and what passes on the wire is
             typed by nothing.  And the transcript names the trap the
             want has fallen into before: "ilo ilman määriteltyä
             valmista on ikuista suunnittelua."  Henri: "Ok.  Tehdään
             jotakin valmiiksi sitten."
    done     when the paper's `gcd` and a two-party protocol — the
             transcript's Bank and Client, or a pair of his own — run
             from his shell as clauses whose arguments are typed by
             session types, checked before they run; a clause that
             would leave a channel unused, use it twice, or offer a
             choice with a branch missing is refused at the check with
             the type and the clause named; and the two parties run
             with no lock and no deadlock because the check said so,
             not because the run was lucky.  (a session's draft,
             2026-09-22, from the because and the transcript's
             milestones 1 and 2 — "jos virstanpylväs 2 ei toteudu,
             koko juttu on jäänyt teoriaksi"; unsigned)
    asked    Henri, 2026-09-22, ~08:30 — "I haven't opened a tend
             session for a long while, also I have a new idea to bring
             forward" and "I started discussing it with general session
             and then thought, it'd be tend's project:
             ~/misc/lineaarilogiikka-kieli-keskustelu.md"
    see      doc/notes/lineaarilogiikka-kieli-keskustelu.md (the four
             sections: the program as a hand that keeps moving; five
             designs and why the second; the LPVM paper as the machine
             under it; the decision), Gange, Navas, Schachte,
             Søndergaard, Stuckey — *Horn Clauses as an Intermediate
             Representation for Program Analysis and Transformation*,
             https://jorgenavas.github.io/papers/lpvm.pdf (the
             clauses, the in/out modes, the `st → st'` thread that is
             a linear resource kept linear by convention alone),
             card:edge.md (this tree's wires: `pull` and `connect`,
             untyped), card:done-when.md (the line above waits for his
             hand; nothing under `tools/` lands before it), F029 (the
             morning this was carded: the file could not be read
             because the person's bound never crossed the hook)

*(question, his call — the `done` line above: sign it as it stands,
change it, or refuse it?  henri: approved 2026-09-22)*

*(question, his call — is `protocol` the name?  It is a session's pick,
from the transcript's own sentence that an interface is a protocol; the
file is never renamed once it is on a shelf, so this is the moment.
henri: I do not know about the name 'protocol'.  It's a bit odd choice
for the name of a programming language, fine name for a card.
2026-09-22)*

So the card is `protocol`, named for what is missing, and the language
is not named yet.  A session does not pick that one: a language's name
is on every file written in it.

*(question, his call — what is the language called?  Nothing on this
card needs the answer before day one, which is a checker and a runner
for the paper's `gcd`; the first file in the language is the moment.
henri: Kude it is, write it in and start day one. 2026-09-22)*

**Kude** — Finnish for weft, the thread that passes through the warp:
the warp is fixed before weaving begins and says where every pass must
go (the session type), the weft is the program, one pass at a time,
each consumed exactly once and in the order the warp says, and a
dropped or doubled pass is a fault the loom refuses.  A session's
proposal at his "I'm out of ideas.  How would you name the language?",
checked within his net bound: no command of that name on this machine,
no language of that name on GitHub; `weft` had three repositories,
`cut` is coreutils, `seam` taken several times.  Not checked: the wider
web.

*(question, his call — where on the priority?  A session places a new
card last; the transcript's "omaksi ilokseni" says it may belong
there, and "tehdään jotakin valmiiksi" says it should not stay there
unworked.  henri: we start on it once we've decided the name 2026-09-22)*

## What the transcript decided, read from this seat

Design 2 of five: classical linear logic read as protocols — `⊗` send,
`⅋` receive, `⊕` I choose, `&` you choose, `!` a replicable service,
`1` close — with the LPVM paper's form underneath: deterministic Horn
clauses, arguments split into inputs and outputs, guards per clause
that must be complementary and exhaustive so that exactly one clause
succeeds and nothing backtracks, side effects as a state thread.  The
transcript's own reading of the join: the paper's mode is a
degenerate session type, one message one way, and a session type is
a mode with a history; generalise the modes and the clauses are
processes, the arguments channel ends, and the paper's demand that
guards be exhaustive is `&`'s demand that every branch be offered.
The prior work it says to know before building is listed there —
Janus, Lolli and Forum, CP and GV, Caires–Pfenning, Lafont — and the
sentence that matters for a card: *the work is to glue, not to
invent.*

The minimal path, its five steps: classical linear logic with
recursive session types and no polymorphism; source as LP clauses
with session-typed arguments, the paper's `st` one channel among
others; the determinism requirement kept, exactly one clause per
branch of a `&`; a runtime of coroutines and two-ended queues; then
the paper's `gcd` running.  Milestone 2, the two-party protocol, is
the `done` line's second half, and the transcript's own test of
whether anything was built at all.

## Day one, proposed

Milestone 1 and nothing past it: the paper's `gcd` as clauses in a
file, a checker that reads the modes and refuses a clause set whose
guards are not complementary and exhaustive, and a runner that runs
the one clause that succeeds.  Session types are *not* in day one:
`gcd` has one channel one way, and a checker for types nothing yet
exercises is the thing this tree's manifesto says not to build.  Day
one is real when the check refuses a `gcd` with its `b = 0` clause
removed, naming the missing case, and runs the whole one — red first,
on the checker.

Where it lives is a question for the card, not for day one: a
directory of its own beside `die/` and `solitaire/`, or a node
(`card:edge.md`) whose pull is a program to check and whose answer is
the verdict — the second is how the tree would use it for its own
wires, and the first is smaller.

## Day one, landed — 2026-09-22, the same sitting

`kude/kude.py`, `check FILE` and `run FILE 'name(1, 2)'`; `kude/gcd.kude`,
the paper's `gcd` as two clauses and the first file in the language;
`test/test_kude.py`, eighteen tests, all red before the program existed
and green on its first run.  By hand: the check accepts `gcd` naming its
signature and its two clauses, `gcd(1071, 462)` answers 21, and `gcd`
with its `b = 0` clause removed is refused at the check with the words
*no clause of gcd(a, b; ret) holds when b = 0* — the day-one line above,
seen.

What the check is: the guards of a predicate are comparisons whose
operands are head inputs or numbers; each pair of terms compared is an
atom, each atom takes one of `<`, `=`, `>`, and every combination is
walked — none holding is refused with the case named, two holding is
refused naming both.  Modes: inputs bound before a call, outputs bound
by it, a variable bound once, every head output bound at the end, and a
comparison on a value the body computed refused, because a failed test
there has no clause to fall to.  **Its limit is written into it**: one
relation per atom, no relation between atoms, so a program exhaustive
only because `a < b` and `b < c` make `a < c` is refused, and the
refusal says the check did not relate the atoms; a test holds that
case.  The runner asserts what the check proved and says so if it ever
finds two clauses holding.

Four mutate rows.  One survived on its first run — the refusal of a
test after a call, disabled, and eighteen green — because the test used
`=`, which the bound-twice branch refuses first; the test grew the
other comparison and the row went red.  Kept on the card as the day's
one lesson: a refusal with two branches needs a test on each.

Not built, and said so in the file's own header: session types, the
paper's state thread, any builtin but `mod`, any term but a variable
or an integer, and the paper's own spelling beyond the five signs it
reads (`←`, `∧`, `≠`, `≤`, `≥`).  Where it lives: a directory of its
own, the smaller of the two the card named; the node shape waits on
something in this tree handing a program to the checker.

## Day two, landed — 2026-09-22, the same sitting, at his "Ok, do day two then"

Asked whether the milestone was steep, the answer was: one real piece
and three of glue, so two days and not a leap — day two one party
checked against its type and run against a scripted partner, day three
the cut.  Day two is that.  `kude/bank.kude`, the transcript's Bank and
Client as Kude writes them: `type Bank = &{deposit: ?Int . Bank,
withdraw: ?Int . !Int . Bank, quit: end}.`, the client on `~Bank` in one
clause, the bank on `Bank` in three, one per branch offered.  A head
input `c: T` is a channel; `c ! t` sends, `c ? x` receives, `c . l`
chooses or, where the type offers, names the branch the clause is.

The checker walks each clause's actions on a channel through the
type: an action the type does not allow is refused naming the state
the channel is at (*`c ? got` — c is at !Int . ~Bank, which does not
receive*); a channel is used to its `end` or passed on in a call at the
type the callee expects, and a use after passing is refused; a branch
on an offering channel is a guard, so it comes before any action, and
the exhaustiveness check walks labels as it walks comparisons — the
bank without its `quit` clause is refused with *no clause of bank(c:
Bank, bal; ) holds when c . quit*.  Duality is mechanical (`~Bank`
flips every sign) and recursion is by name, compared coinductively.
The runner plays one party: sends and choices go to stdout one line
each, receives and the partner's choices come from stdin, so a
scripted partner is a file piped in and a partner closing early is a
run error naming the action it closed on.  By hand: the bank at 100
told *deposit, 50, withdraw, 30, quit* answers `c ! 120`; the client
told *120* prints its five actions and `got = 120`.  `add` and `sub`
are builtins now because the bank needed them.

Thirteen tests, red before the program and green after two fixture
fixes: a one-clause bank in two fixtures was refused for its missing
branches before the refusal on trial — the checker right about the
test.  Five mutate rows on the walk, beside the four of day one.  Not
built, said in the header: the cut, a message type but `Int`, a channel
sent over a channel, `!A`, polymorphism, the state thread.

## What would make this wrong

The transcript says it: "Sinulle ei mikään.  Alalle vähän."  If the
`done` line runs and nothing in this tree, or on his desk, ever hands
a program to the checker afterwards, the card was built for its own
joy — which the transcript allows, and which the board should then
say out loud rather than dress as a need.  The second half of the
`done` line is the guard against the other failure: a checker with
no protocol ever checked is a theory with a test suite.
