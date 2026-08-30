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
