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
