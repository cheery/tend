# swe-bench — the tree claims to make a working session better, and has never been measured doing work

    status   shelved — 2026-09-02
    because  every measurement this tree has run asks what a *mind* does
             at the door — SimpleQA's 150 questions, 48 pick arms, the
             compare turns.  None of them asks what this tree is for.
             `vision.md` says tend exists so that sessions and programs
             run under a boundary that a person can hold, and the whole
             apparatus — the fence, keep, the grant, the cords, the
             board, the kaizen loop — is a claim that a session working
             *inside* it does better work, or at least safer work, than
             one without.  **That claim has never been put to a task with
             a right answer.**  The kaizens are the only evidence and
             they are written by the party being judged
    asked    Henri, 2026-09-01 — "lets card the SWE-bench lite as shape
             (2)", picking the harder of two things wearing one name
             after a session laid them out: (1) SWE-bench through the
             door, another arm on `tools/compare.py`, and (2) SWE-bench
             worked by a session under the fence.  He took (2).
             `bench/SWE-bench` was cloned by his hand at 05:12 the same
             morning, before either was proposed
    see      card:simpleqa.md (the precedent, and the warning: its day
             one is shape (1) and it found the tools *cost* correct
             answers), card:session-program.md (the conditioning
             measurement, the same question asked of gemma4 instead of a
             session), card:work-environment-ai.md (the residual this
             leans on — a session exec'ing an arbitrary program),
             card:tools.md (the 48 arms, and `readchars` as the knob that
             turned a 15/24 into a 24/24), manifesto.md §"Two rules"

## What makes this different from `card:simpleqa.md`

They share a name — *a benchmark* — and almost no machinery.

`simpleqa` asks **what the mind knows and whether the tools make it
honest**: one turn, one question, an answer graded against a key.  Its
subject is the model at the door, and its instrument is
`tools/compare.py`.

This asks **whether the tree helps**.  Its subject is a *session* — the
thing this project actually governs — and its instrument does not exist.
A SWE-bench Lite instance is a repository at a commit, an issue, and a
hidden test that the fix must pass.  Working one means reading a
codebase, editing files, running tests, and iterating: exactly the
activity the fence, the grant and the cords are built around, and
exactly the activity nothing here has ever scored.

**The one number that would matter**: the same instances, worked by a
session inside this tree and by a session with none of it, resolved-rate
against the hidden tests.  Everything else is commentary.

## What this card must not become

**A leaderboard entry.**  The tree cannot beat a purpose-built coding
agent and has no reason to try; the number that matters here is not
tend's rate against the world's, it is tend's rate against *tend's
absence*, on the same instances, same model, same budget.  A card that
starts reporting an absolute score has changed subject.

**A second SimpleQA.**  That card's day one came back with the tools
costing correct answers, and its honest reading was that the three bins
could not see what the tools bought.  A benchmark whose result the tree
cannot act on is a benchmark that produced prose.  So the arms have to
differ in something this tree could actually *change* — a grant row, a
cap, a cord — and not merely in "with tend / without tend", or the
result will be a mood.

**Something a session can grade itself on.**  The hidden tests are the
point.  A session must not be able to read them, and the grader must run
where the session cannot reach.  This is the first measurement here whose
integrity depends on the fence rather than merely happening inside it.

## The hard parts, named before anything is built

1. **A session that can be launched, not just entered.**  Every session
   this tree has ever run was started by Henri at a terminal.  An arm
   needs N sessions started, watched, and stopped by a program.  That is
   `card:work-environment-ai.md`'s residual and it is the real cost of
   this card.
2. **A repository per instance, that is not this tree.**  The fence binds
   `tree_parts` of `~/tend`; an instance is a different repository at a
   pinned commit that the session must be able to *write*.  Neither the
   grant nor `tools/sandbox.sh` has a shape for "a scratch tree the
   session owns", and inventing one carelessly is how the fence gets a
   hole.
3. **A patch route out.**  The session's work has to reach the grader
   without the session reaching the grader.  `proposals/` is the tree's
   existing answer to "the session writes, a person lands", and it may be
   the answer here too.
4. **Cost and time.**  300 instances × a session each is not a sitting,
   and SWE-bench's own harness wants Docker per instance.  A first run is
   a handful of instances, and the card should say which and why before
   it runs any.

## Day one, unbuilt — and it is deliberately not the benchmark

**One instance, by hand, both ways.**  Pick a single SWE-bench Lite
instance; work it in a fenced session; work it in an unfenced one; run
the hidden test on both.  No harness, no automation, no N.

That is day one because every hard part above is a guess until one
instance has been through by hand.  It answers, for about an hour of
work: whether the fence can hold a foreign repository at all, what the
patch route has to be, what a session actually does differently, and
whether the difference is visible in a *test result* or only in the
prose about it.  If it is only visible in the prose, this card should
stop, and that is a real outcome.

`card:simpleqa.md`'s day one ran the whole 150 and its finding was that
the bins could not see the thing that mattered.  The lesson taken here is
to look at one instance closely before scoring three hundred badly.

## What would make this card wrong

**If the honest answer is that tend does not help a session do this kind
of work** — that the fence is a tax on a coding task and the board and
kaizen are overhead against a hidden test.  That is a live possibility
and the card is worth opening *because* it is: this tree's apparatus has
never been scored against anything, and a project whose central claim is
untested for nine days is exactly what `manifesto.md`'s second rule is
about.  A result that says "no measurable difference on coding tasks,
and here is what it does help with instead" would be worth more than a
flattering number.

**If day one shows the difference is not in the fix but in what the
session does around it** — the record it leaves, the questions it raises,
the things it refuses — then the benchmark is the wrong instrument and
the card closes pointing at what the right one would be.

*(self-shaped, 2026-09-01 — a session wrote the card that scores whether
sessions are helped by this tree, which is the party the measurement is
about. henri: approved 2026-09-04)*

## Shelved 2026-09-02, at Henri's word — and what it waits on

Henri, at the end of the morning that ran the conditioning arm three
times on gemma4 and once on hy3 (`card:session-program.md` §"Run 1"
to §"08:27"), and after a session had sketched how this card's day one
would be arranged:

> Lets move the testing to far future.  I don't know why this works,
> and how to measure it.  And I'm not certain that SWE-bench would
> capture the effect.  I think we have better things to do, such as
> getting this project raised up and working, and leveling the
> interface such that it's easy on the user and understandable.

So this card **waits on his word to resume**, not on an event in the
tree.  What the morning had shown by then, and why his doubt is the
right one: three predictions written before the data, three
falsified, and the last of them because the task was one a command
answers as well as a reason does (§"08:27–08:45" on the
session-program card).  A benchmark whose task has a clean imperative
form cannot see the thing this tree bets on, and nobody yet knows
which task can.  The mark above stands unanswered and stays so; a
shelved card's rule is still a rule nobody has stood behind.

The priority it leaves: the tree raised up and working, and the
interface levelled so that it is easy on the user and understandable
— his words, on `vision.md` the same hour.
