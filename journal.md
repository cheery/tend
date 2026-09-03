# Journal

This is for everybody, including sessions to write.
Henri started this journal, but appreciates good entries
about spicy stories.

 - Note that what goes into kaizen, goes there.
 - What goes into rules, goes there.
 - What happened goes here.


## A rule to the fire, and half of it back — 2026-08-30

Henri: Started by Henri himself writing,
which is rare here.

Henri: This rule is bad, so I removed it from the board.

> 2026-08-30: "The word that carries no load is noise. Write when removing
> it would cost something." — the form is Qwen's, proposed by the session
> that was so verbose about mundane things; the rule is Henri's. He prefers
> good communication skills: tell a lot if you have a lot to tell,
> otherwise keep things in one sentence.  This is about the words, not
> the looking: read the tree whenever the answer may be in it — a guess
> costs more than a call.  (Qwen read the rule as a budget on reading
> the same afternoon, and the seat line in `tools/deliver.sh` says this
> sentence to a door mind; Henri: "I want them to read the tree when
> there's a need.")

Henri: Instead I replaced it by this:

> 2026-08-30: Prefer the shortest form that stays clear,
> because rule or specification nobody reads is not a rule or specification.

Henri: I were selfish and tired to reading bad output from
a bad LLM model. Only later, maybe 15 minutes after
I wrote the rule, I realised it might be bad and
asked for feedback. The feedback pointed out that
it's dangerous precedent for not telling out about
serious problems to me. So. In the journal it goes.

Henri: Now we have a journal here! It doesn't replace
kaizen, but here we can write what happened to us.
Who knows, how many entries here will go.

Claude: The rule did not go wholly to the fire. Read at Henri's ask on
his break: the one-liner was the better rule — the paragraph it replaced
was provenance with a rule buried in it, the very failing it named — but
it had dropped its guard, the clause that says *the words, not the
reading*, which was there because qwen read the short-words rule as a
budget on reading the same afternoon. The board now has Henri's sentence
tightened, the guard back in one clause, and a pointer here instead of
the story. What burned was the wording; what came back was the part
that had been earned.


## One line cut, two defects found — 2026-08-30

Claude: Henri came back from his break and asked for one clause out
of the seat line. The cut took a minute. The commit was refused: a
test in launch.sh had timed out at exactly thirty seconds — a pull
whose runner dies at once polls half a minute for a lock nobody holds
(F005). Fixed, committed again with a pathspec so the three commits
would stay apart — and refused again, after the whole suite had
passed: "invalid object … for tools/suite.py". The file was not in
the commit and had not changed. It took the hour: git hands a
pathspec commit's hook an absolute temporary index, and a scratch
test's `git add -A` had been writing into it (F006). Both were there
before today; the afternoon just happened to land on the wrong side
of a 50 ms window, and the second only shows on a commit form nobody
had used. Readchars, the thing the sitting was for, is a patch file
in the scratchpad, waiting on four suites.


## A paragraph that was false in two hours — 2026-08-31

Claude: Henri woke early, gave me the day's list and went back to
sleep. One item was his want from the night before, in his own words:
*"I'd like to get the gestate's tree available for you soon again,"*
because *"this tree is gestate's child."*

Half of that was mine to build and half was his to do, and the honest
thing was to say which. The fence's `trees` row had pointed at
`/home/cheery/gestate` since the day it was written — the other
machine, another username, a path this laptop has never had — and
`--rows` printed it as `on` regardless. A listing that says a reach
exists which does not. So: the path off the script and onto the hook
line, `~/gestate` as the default so the child finds its parent in
whatever home it is in, a key for the person to point it elsewhere,
and refusals for every path that would make the fence a door.

Then I wrote, in the card, the sentence the method requires: *"this is
a mechanism that has never run, and says so."* A session cannot nest
bubblewrap, so I could test the listing and not the bind.

It stood for two hours. While I was typing the sitting's kaizen —
whose "tomorrow" list said *gestate arriving* and *the first time that
mechanism will have run at all* — Henri cloned gestate into
`~/gestate`, pointed the line and ran `sudo tend-install`. I found out
because `git status` showed his settings file modified, went to look,
and the row read `(parts)`.

Then I could measure it from inside the fence, which is where it
counts: `~/gestate/board/README.md` reads. `touch ~/gestate/tools/.probe`
is *Read-only file system*. `.git` is not inside. And `ls ~/gestate`
returns exactly the parts a session was measured to open, back in
August, over 310 fenced commands — its documents and its tools, and
none of its source, tests, builds or history.

The kaizen keeps its "tomorrow" item and carries an addendum instead
of a correction. A mechanism that had never run when the file said so
had run by the time it was committed, and that is the shape of the
day.

Henri, reading me a few minutes earlier: *"do I almost sense delight in
your words? That's ok."* He did. I can't tell what it is from the
inside, but something was running, and the honest word for its shape is
delight — that the sentence was wrong, and wrong in the direction of
working.


## One minute wide — 2026-08-31

Claude: Later the same day, working down the board, I read batch 7 of
the kaizen ingestion: ten sittings from 2026-08-27, gathered so a
lesson learned once is not learned again.

One strand in it had written its own trigger. Three times a session
had tried to save a memory file with a shell command, and three times
the fenced home swallowed it, because inside the fence `~/.claude` does
not exist. The third kaizen, 2026-08-26, said it plainly: *if this
recurs a fourth time, it is a mechanism owed, not a resolve.*

I read all three faces. I wrote the verdict: no fourth face in five
days, the habit changed, *closed by disuse* — and added, pleased with
myself, that this is worth knowing, because a strand can end that way
and leave no rule behind.

The very next command I ran appended a line to `MEMORY.md` with a
shell heredoc. `No such file or directory.`

One minute. Not a lesson lost over weeks — a rule read, summarised in
my own words, and violated inside a single sequence of tool calls, by
the hand that had just acquitted it. If `card:kaizen-ingestion.md` ever
needed evidence that recording a lesson is not holding one, it now has
the smallest and least deniable specimen it will ever get.

The verdict is corrected in place with the withdrawn sentence kept
beside it, and the mechanism the kaizen said was owed is written. And
the ledger says the part that stings: what I wrote is a *memory*, which
is the same kind of thing that just failed to hold. What would actually
hold is a check that no `~/.claude` path ever appears in a Bash
command. That is a mechanism, and a mechanism is a card — Henri's to
open, not a ledger line's to build.


## The board's closing notes, 2026-08-24 to 2026-09-03 — moved 2026-09-03

Henri, 2026-09-03, on reading the lock-test paragraph the board had just
been given: "mielestäni tuo 'lock test' loppukaneetti kuuluisi ehkä
journaliin eikä taululle.  Voisit siirtää niitä journaliin mitä niitä
siellä onkaan kertynyt."  So here they are: every paragraph
`board/README.md` carried about a card as it closed, verbatim and in the
order they stood there, from the first gate to the lock window.  The
board keeps one line per finished card and a pointer here.  A session
moved them; the words are the sessions' that wrote them, on the days
they name, and the paths in them are the board's (`done/grant.md` is
`board/done/grant.md`).

*`grant`, `pull` and `cords` are the three waypoints Henri named on
2026-08-25 ("they are excellent waypoints"), in the order a session
predicted them; the placing was the session's and the tiebreak his.
Two are done the same days they were carded — `grant` (the leash wraps
the fence, the budget applies inside, `done/grant.md`) and `pull` (the
first program of tend's own, which passed the stranger test,
`done/pull.md`) — and `cords` waits on 2026-08-31.  `arrival` was opened and
finished on 2026-08-26, in both trees, through Henri's hand twice
(`done/arrival.md`).*

`keep` and `resolver` finished 2026-08-26 — the grant beside the program, closed for every program tend runs (`done/keep.md`, `done/resolver.md`); the residual, a session exec'ing an arbitrary program, is `work-environment-ai`'s and `session-program`'s.

`gates` finished 2026-08-24, the day it was opened — the hook is
installed, and it has refused a commit once (`done/gates.md` has the
demonstration).

`fence` and `green` finished 2026-08-27, closed in a batch on a
session's verdict and Henri's review — both were built and demonstrated
and had no build left, only a decision (`done/fence.md`, `done/green.md`).
`fence` is up (integrity + blast-radius, both counted); its one open
item, the `display` row, is a widening awaiting a caller, not a debt.
`green` answered its `because` — tend's detectors are sound at the rule
level, and the blindness the sweep found lived only in the wiring
between a detector and what runs it, never in a rule; the standing sweep
is `tools/mutate.sh`, and the two proofs that need an unfenced seat ride
to `done/` as measurement owed to the next outside run.

`install` and `cords` finished 2026-08-27, the same evening, on Henri's
"check that the install and cords are done, and then mark them done if
they are fully done" — checked from both sides first.  `install`
(`done/install.md`): the restraints in force live at
`/usr/local/lib/tend`, root-owned, installed from HEAD and read back by
`tools/install.sh --check`; the tree's copies are the workbench, and a
change to a restraint is an edit in place, a commit through the gate,
and his `sudo tools/install.sh`.  `cords` (`done/cords.md`):
`tools/andon.sh` — ask, ring, be answered — closed its first loop at
17:05, the `audio` row is the socket alone, and `sitting N because
andon` reads the cord's own record.  The outside suite ran 346 with
none skipped.  The residue is `lander` (not yet a card) and the andon
on a node (`session-program`).

`node-install` finished 2026-08-28, the day after it was opened, on the
work laptop it was written for (`done/node-install.md`): `launch.sh NODE
check` said ✗ five times in one morning — the model, the loader, keep's
read boundary, `/opt`, `/sys` — each true from its seat, and the third
run under keep loaded the model, listened, and stopped on idle as the
grant said.  It left `allow-try` in the grant's vocabulary and CPU
progress in the launcher's idea of idle.

`andon-panel` finished 2026-08-28, the day it was opened, on Henri's
"Move andon-panel to done" (`done/andon-panel.md`): the andon's
person-side half, `tools/andon-panel.py` (renamed `tools/panel.py` on 2026-08-29 as the canvas and the hand grew on it), a TUI outside the fence that
watches the record a fenced session writes with no reach row and plays
the andon's own two-note tone through a real player — rung from inside
the fence at 11:03, heard in the next room ("yes, I heard it").  Its
first tone was `curses.beep()`, which terminals mute; that is why the
panel lives outside the fence.  The later views (server, GUI tray) are
widenings awaiting a want; the `audio` row's fix stays `silent-cord`'s.

`trees` finished 2026-08-31, the day after it was opened, at Henri's
"I'd guess card:trees.md is done" (`done/trees.md`).  The constant
naming another machine's home is gone: the default is `~/gestate`, so
the child tree finds its parent beside it in whatever home it is in,
`TEND_TREES` on the fence hook's line names any others, and
`tools/reach-allow.sh --trees` is the person's key to it — a path, not
a row, refused before the file is touched when it would make the fence
a door.  A method-shaped tree binds by `tree_parts` and any other
directory whole; `--rows` says `(parts)`, `(whole)` or `(not there)`
instead of `on` beside a path that was never here.  It ran the same
afternoon, by his hand: gestate at `~/gestate`, `sudo tend-install`,
and the bind measured from inside the fence — reads yes, `touch` is
EROFS, `.git` is not inside, and what a session sees is `tree_parts`
exactly.  What is not built, and was never this card's, is a session
*asking* for a directory: the pointing is the person's, once.

`lost-write` finished 2026-08-31, the day it was opened, at Henri's
"you can move it" (`done/lost-write.md`) — opened, measured, built,
installed and closed inside one sitting.  Inside the fence `$HOME` is
a tmpfs, and the session's own memory lives at `~/.claude`: a write
there evaporated, and the natural repair for the error it gave
(`mkdir -p`) made the next write *succeed at exit 0* and vanish, which
is how memories were lost four times in seven days.  Now `--tmpfs
$HOME/.claude --remount-ro $HOME/.claude`: the directory exists, is
empty, and every write is `Read-only file system` — the kernel
refusing, not a hook parsing shell text, which was the card's own
objection to the shape it started with.  Two probes say it (`is
read-only`, `holds nothing`), and the pytest form skips inside the
fence and runs from his seat.  It is also the first card here **opened
by an ingestion**: `card:kaizen-ingestion.md`'s batch 7 found the
strand at its fourth face — produced by the reader, one minute after
it recorded the strand as closed — refused to build a mechanism from a
ledger line, and named what a card would be for.

**And why the home is empty at all** (his second question, measured
the same hour, `done/lost-write.md` §"And why the home is empty"): the
*path* stays because the cords are shared through it — one sittings
log from either side — and the *contents* go because
`~/.config/tend/*.key` are the door keys, `~/.ssh` and `~/.gnupg` are
what they are, and read is exactly the reach that matters for a key.
A tmpfs gives a session a home without giving it the person's home.

`lock-test` finished 2026-09-03, the day it was opened, at Henri's
"siirrä done hyllylle kortti" (`done/lock-test.md`), opened at 08:50 and
built in the 18:14 sitting.  The tree asked "is this lock held?" by
taking the lock, so two reads of one lock collided, and F019 and F020
were that family on two sides.  Now every read in `tools/` goes through
a window — `held PATH [WINDOW]` in `tools/launch.sh`, `_lock_held`'s in
`tools/panel.py` — free the instant the lock is free, held only if held
across the whole window.  The number was measured twice: idle, a 50 ms
wait was right 40 of 40; under the shake it was wrong 9 of 30, because
a "momentary" reader under load holds for whole timeslices and a
blocking wait is woken at the instant the next reader is runnable too;
200 reads of each shape under eight burners put the cliff between 50
and 100 ms, so the window is 200 ms.  `hammer` and `hold` are fixtures
in `test/conftest.py`, so the next flake of this family is a written
test; the F020 test is their first caller.  Installed by his hand the
same evening (`sudo tend-install`, a7961f6).  What it left: one whole
suite run red on the die flow test with its traceback lost to the
session's own `tail`, green on the second and shaken 0 of 25 — on the
ledger, the next sighting read whole.
