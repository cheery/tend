# resolver — a program starts only when a person types its launcher, and the grant that confines it lives in that launcher

    status   done — 2026-08-26
    because  nothing here starts a program but a hand in a shell: the
             node runs when someone types `node/run.sh run`, and a pull
             that finds no runner is recorded and served by no one.  So
             the confinement a program gets is whatever the launcher it
             was started through happens to bake in — one script, one
             program, and a session that starts a program some other way
             starts it with the session's whole reach.  Henri: the person
             "always pulls, never need to start the program themselves"
             — and today the pull cannot start anything, and the grant
             is not where the pull is
    asked    Henri, 2026-08-26 — "How does programs get their
             restrictions?  Since I think that this should work on the
             idea that user always pulls, never need to start the
             program themselves."  Then: "Do a card for the resolver."
    see      card:keep.md — the session half, open at Henri's word the
             same hour; a program's grant is built (reads, writes, TCP),
             and only a launcher applies it
             card:pull.md (done/) — "a pull with no runner is recorded
             and served by no one — the default is off"; the lifecycle
             this card would complete
             node/run.sh — the one launcher, the grant baked in as three
             flags; what this card would move
             card:work-environment-ai.md §"The architecture" — the
             broker and lifecycle; the *suspected* design this card must
             not adopt on its say-so (manifesto)
             card:cords.md — the sitting limit and the andon: the other
             things that would have to know a resolver is running
             card:grant.md (done/) — the leash wraps the fence; a
             resolver is a third thing the leash would have to wrap, or
             be

## What it is

Two halves of one gap.  **Who starts** — the pull is one line appended
to a ledger; nothing watches the ledger, so a pull with no runner is a
line and nothing else.  **Who restricts** — `keep` confines a program
from outside, which is right, but "outside" today means a shell script
a person runs, so the grant is a property of *how it was started*, not
of *the program*.  Start it another way and there is no grant.

Henri's frame closes both at once: if the person only ever pulls, then
the pull *is* the launch, and whatever serves a pull that has no runner
is the one place a program is ever started — so it is the one place the
grant has to be applied.  The grant rides the pull path.  A session
that also pulls, rather than starts, cannot launch anything unconfined
because it cannot launch anything at all — which is `keep`'s session
half by a different door.

## What the shape would be, and what it is not yet

Named so the first measurement has something to disagree with, not so
it is built:

* **A grant beside the program, not in a command.**  Today it is three
  flags in `run.sh`.  It would be something a resolver reads from the
  program's place — the program never sees it, cannot widen it, and the
  person can read it as a plain file.
* **A resolver outside the session's write access** — like the fence,
  like the protected set.  A resolver a session can edit is decoration.
* **The resolver is the first long-running thing tend would own.**
  Something has to watch the ledger — a poll, `inotify`, a hook on
  `pull` itself.  Then the leash's wall budget bounds the *resolver*, not
  the program, and the sitting limit has to know whether a running
  resolver counts as a sitting.  This is the cost, and it is the part a
  measurement should size before a line is written.

**What it must not become**: the capability broker with a picker and
handle types, built because the name "resolver" sounds like one.  The
manifesto forbids adopting a suspected design on its say-so, and
`work-environment-ai` marks the broker suspected.  This card owes one
thing: a pull that starts a program *under its grant* when nothing is
running, shown from inside the fence with `cat` of the tree refused
from the program it started.  One program, the node.  A second pulled
program is what would earn a general path.

## What would make this card wrong

If the person does start programs by hand and wants to — if the shell
line is the interface — then the grant in the launcher is exactly where
it belongs and this card is the broker wearing a small name.  Henri's
words say otherwise, and the stranger test in `vision.md` says "start a
program in it," which the day-one measurement should read again with
this card's question: is *pulling* starting?

## Day one

Measure, do not build: how a pull reaches a resolver on this machine
without a daemon that outlives the sitting (what `pull` could do
itself, first); what the leash and the sitting limit say about a
process that is not a session and not a program; and what
`work-environment-ai` already decided about the launch that this card
must not re-decide.  Then the smallest thing: the node, pulled, starts
confined.

## The news the same hour, kept beside the card

Henri, 2026-08-26: models run on his work laptop at 5–9 tokens/s
through SYCL — llama.cpp is reachable.  "We may be able to do a fully
local system."  Not this card's problem, and named here because it
changes who the *puller* might be: a session that is a local model is a
program tend runs, under a grant, pulled — the same shape this card
describes, one level up.  If it turns into work it is its own card.

## Day one, 2026-08-26, 13:29 — measured, then the smallest thing

Henri: *"do resolver's day one."*

**Read first.**  `vision.md`'s stranger test says "start a program in
it" — and the sentence is satisfied by a pull if the pull starts it;
nothing in it says a hand.  `work-environment-ai` decided the broker is
*suspected* and the leash grants nothing; it did not decide the launch,
so there was nothing here to re-decide.  The leash bounds *one
invocation* (900 s wall, a scope); the sitting limit counts prompts —
neither has a word for a process that is not a session and not the
command a session ran, which is what a resolver would be.

**Measured, from inside the fence**: a process started detached inside
a fenced command **dies with the command** — `sandbox.sh` runs
`--unshare-pid --die-with-parent`, and a `setsid -f` sleeper's marker
never appeared.  So the day-one question has a plain answer from this
seat: no daemon can outlive a fenced command at all.  A resolver started
by a session's pull lives inside that pull's command, bounded by the
leash's wall and killed by the fence's namespace; from a person's shell
the same thing survives and stops on idle.  Neither seat needs a daemon
that outlives a sitting, and the leash's "one invocation" already
bounds the session's case.  What `pull` itself could do first turned out
to be the whole of it.

**Built, the smallest thing** — in `node/run.sh`, where the grant is;
`node.py` untouched:

* `run.sh pull` — takes the lock non-blocking to learn whether a runner
  is up; if not, starts one detached under the same three-flag grant,
  waits for its generation to move (the node reads the ledger *at open*,
  so a pull written before that would be seen and not served), says
  what it did — and says, when `TEND_FENCED` is set, that the runner
  lives only as long as this command — then pulls.
* `run.sh run` — takes `<state>/run.lock` on an fd before the
  confinement; the runner inherits it through keep's exec and holds it
  for life.  A second `run` is refused, exit 75, "pull it instead."

From inside the fence, live: one pull started a runner and was served
by it; a second was served by the same generation (2 pulls, 1
generation); `run` while held exited 75; the runner stopped at idle and
the lock was free.  Three tests in `test_keep.py` hold it, four rows in
`tools/mutate.sh` break it (pull never starts, pull starts regardless of
the lock, run never takes the lock, pull does not wait for the open),
each red by name.  The root README's "Try it" now leads with `pull`.

**What this is and is not.**  The card's owed demonstration — the node,
pulled, starts confined — is done.  What it is not: a grant beside the
program that a resolver reads (the grant is still three flags in the
launcher), a resolver outside the session's write access (`node/run.sh`
is in the tree, not the protected set), or a general path.  Those are
the shape §"What the shape would be" named, and each waits for the
thing that would earn it: a second pulled program, and a decision on
whether the launcher joins the protected set, which is Henri's.  The
session half of `keep` is unmoved by this: a session can still start a
program some other way.  That is the card's remaining `because`.

## 2026-08-26, 13:50 — the session half: a hand that bypasses the launcher, measured and closed at the node

Henri: *"keep and resolver."*  The card's remaining `because`: a session
can still start a program some other way.  **Measured, by the ledger**
(`tools/ledger.py`, born this hour — the ledger's second read, and the
13:42 kaizen said the parser is a tool on the second ask): in 244
records since 08-25, `node.py` was started raw twice, both times by
this session, both times as a measurement.  Through the launcher, 9.
So the bypass is real and has not been used for work.

**What the bypass does**, run on a scratch state: two raw runners on
one state **both opened** — gen 1 and gen 2 — and each served the same
two pulls; one log had four `pull` lines, the other three, and the
state was whichever wrote last.  Silent, which item 14 forbids.

**Closed where it belongs — the node's own lock.**  `node.py run` takes
`<state>.lock` (flock, non-blocking) and a second runner is refused,
exit 75, "another runner holds … — pull it instead."  The lock is the
node's and not the launcher's: however the node was started, one state
has one runner.  `run.sh`'s lock stays — it is the launcher's runner
*detection* on a different file and does not conflict.  Rule 1 is
kept: the node does not bound its own *reach*; it refuses to be two.
`test_node.py::test_one_state_has_one_runner`; the row `node: the
runner lock never taken` is red by name.

**What stays open**: a session can still start the node raw *when no
runner is up* — unconfined, since only the launcher applies the grant.
That is the true session half, and it is `keep`'s: the fix is not in
the node or the launcher but in what a session may execute, which is a
row of the fence or keep on the session.  Named; not this slice.

## 2026-08-26, 14:35 — what the tree-row measurement says about this card

`card:keep.md`'s tree-row measurement, read from here: in 310 fenced
commands the session never wrote `node/state` by name — the node
writes it, and the session's only write there is the pull line.  So
the directory is a program's, and the session half of both cards
collapses to one shape: the state read-only to the session, the pull
line the one file it may append, and the runner started by something
**outside the fence** that reads the pull ledger — the resolver outside
the session's write access, §"What the shape would be", second bullet.
Today the runner starts inside the pull's own command and dies with it
(day one), which was right for one program and one seat; it is also
exactly why the session can still run the node raw.  The next slice,
if Henri wants it, is the resolver as a hook on the person's side of
the fence — the same place the lamp, the limit and the fence-hook
already run — started by a pull line, confined by `run.sh`, outliving
the command that pulled.  A measurement of what such a hook costs
(when it runs, what the leash says) comes before the build.

## 2026-08-26, 14:40 — the resolver outside the fence: built, and the fence half handed over

Henri: *"do the next slice."*  Cost measured first: the person-side
hooks are `UserPromptSubmit` (lamp, limit, fence check) and
`PreToolUse[Bash]` (the fence-hook); a `PostToolUse[Bash]` hook runs
unfenced, as the person, right after the command that pulled — one
`flock -n`, one `wc -l`, one `grep` per command, and a leash line per
runner started.  The leash's word for the runner is what it says for
any invocation: a wall budget and a ledger line.

**The node changed by one line, and it is the line that made the
outside resolver possible.**  A runner used to read the ledger *at
open* and serve only what followed — so a runner started after a pull
would never serve it, and day one had to start the runner *before*
pulling.  Now `seen = state.pulls`: the ledger is append-only, the
state counts what was served, and a runner opening serves the
difference first.  Item 13 — "starts by pull" — made literal.
`test_it_opens_where_it_was_left` moved with it (a pull before the
runner counts now); `node: a runner reads the ledger at open` is a red
row.

**`tools/resolve.sh`** — a look: if the ledger holds a pull no runner
has served and no runner holds the lock, start the one runner
(`node/run.sh run`, confined, under the leash, detached), wait for it
to take the lock, say one line.  Otherwise silence.  `--hook` is the
same with stdin drained; `--install` is Henri's, `jq` into
`PostToolUse[Bash]`, refused from inside the fence.  Measured on the
way: two back-to-back looks both started a runner before the
wait-for-lock existed — the second hit the lock and left with 75, so
the tally was right and the resolver's word was not.  Eight tests,
three rows red by name.

**Handed to Henri as `resolver-outside.patch`** (77 lines; `run.sh` and
`sandbox.sh` are protected): inside the fence, `run.sh pull` appends
its line and starts nothing — "the runner is the resolver's to start"
— since one started there dies with the command and was startable
unconfined; from a person's shell, as before.  `tools/resolve.sh` joins
the protected set, because it is a script a hook runs.  The test rides
in the patch.  Then his line: `tools/resolve.sh --install`.

**What this closes, and what it does not.**  With the patch and the
hook: a session's pull is one appended line; the runner is started by
the person's side, outlives the command, is confined by the launcher
and budgeted by the leash; a session cannot start the node through the
pull path at all.  It can still run `node.py` raw — the state directory
is still writable to the session — and that is the last step the
tree-row measurement named: `node/state` read-only to the session with
the pull file the one thing it may append.  That is a fence row, and it
must land *after* the hook is installed, or a session's pull is never
served.  Not this slice; the next, and it is one bind.

## 2026-08-26, 15:03 — served by a runner no session started

Henri applied `resolver-outside.patch`, `resolve-serialize.patch`, ran
`--protect` (the step this session left off his list — the fence said
so at his next prompt, which is the check doing its job) and
`tools/resolve.sh --install`.  Then, from this session's seat: one
`run.sh pull` inside the fence — "pull recorded — inside the fence the
runner is the resolver's to start" — and in the next command:

    gen 1 opened at 15:02:52 · served 1, total 1 · pull, total 2
    stopped — nobody pulled for 30.0s · lock free
    leash: 15:02:52  48s  exit 0  cpu=0.1  scope  t=900

The hook on Henri's side started the runner between two of a session's
commands; it served a pull that had sat in the ledger since 13:29 *and*
the new one; it outlived the command that pulled, stopped by itself,
and left a leash line.  **The first program tend runs that a session
did not start.**  What the leash says about it: an invocation with a
900 s wall — a node pulled for longer is exit 124, the interaction
`node.py`'s header named on day one, still left for the grant that
sizes the budget.

**A detector that flickers, on Henri's seat only.**
`test_a_second_look_while_the_runner_is_up_starts_no_other` failed
twice from his hand — first with the 3 s wait, then with the
serialized 10 s wait saying "started one, and it has not taken the lock
after 10s" — and passed under the gate on the very next run.  The
ledger shows the runner those tests started *ran and exited 0 in 1 s*;
what the look did not see was its lock.  From this seat the test has
never failed (leash `plain`); his seat runs the leash's scope path.
Not explained; measured as far as it can be from here, and handed to
`green` as a flake to count before it is reasoned about.  Named on
both cards so the next reader does not take one green run as the
answer.

**Open**: the flake's rate on Henri's seat; then `node/state`
read-only to the session with the pull file writable — the last bind,
now safe to land because the hook serves what a session pulls.

## 2026-08-26, 15:12 — the flicker counted, and two causes read off the ledger

Henri's loop, ten runs of the one test: **1 failed, 9 passed** — the
first, in 10.92 s; the nine after in ~1 s each.  The leash ledger for
that window has eleven runner records for ten tests: nine clean 1 s
runs a second apart, and at the front **one `exit 75` with 0 s wall**
that *started* at 15:10:06 — ten seconds after the test started it —
followed by one extra clean run.  (The ledger's epoch is the leash's
start: `start=$(date +%s)`, written at the end.)

Two causes, both measured, neither guessed:

* **The resolver tested the lock by taking it.**  `flock -n "$lock"
  true` holds the lock for the length of `true`; a runner whose
  `flock -n 9` lands in that moment is turned away with 75, and the
  resolver then waits for a lock nobody will take.  The same `exit 75`
  signature is in the 14:45 mutate runs.  Fix: the runner waits up to
  5 s for the lock (`flock -w 5`) — a momentary hold clears in
  microseconds, a real runner still holds it past 5 s and the second
  still leaves with 75.  Deterministic test: hold the lock 0.3 s, start
  the runner, it must run.  Red against the old `run.sh`, green with
  the patch.
* **The leash's scope path starts a runner ~10 s from cold on Henri's
  seat** — twice in a row at 15:10, then instant for nine.  From this
  seat the leash is `plain` and starts in milliseconds, which is why
  the test never failed here.  The resolver's wait is 30 s now, and
  says so if it runs out.  The latency itself is the leash's finding,
  not this card's — `card:work-environment-ai.md` has the line.

**Handed to Henri as `resolver-lock.patch`** (`run.sh` and `resolve.sh`
are protected), the test inside it.  The detector was right both
times: a 1-in-10 red was a race in the mechanism and a cost in the
leash, and neither would have been found from a seat where the test
is always green.

## 2026-08-26, 15:30 — the session half closed by the last bind

`card:keep.md`'s last bind, handed to Henri: `node/state` read-only to
the session, the pull file its one write.  With it, the sentence both
cards carried — *a session can still start the node raw when no runner
is up* — is false: the raw start fails at the node's own lock and its
state, `run.sh run` fails at the launcher's, and the pull is the only
path, from the person's side, under the grant.  The card's `because`
no longer describes the node from any seat.  What it still describes
is the general case — a second program, and a grant that lives beside
a program rather than in a launcher — and that waits for the second
program.  Whether the card is done is Henri's.

**15:37 — closed from a session's seat.**  With the last bind in: a
raw start fails at the node's lock, the launcher's `run` fails at its
own, a pull is one appended line, and a runner on Henri's side served
it within the second (`gen 3 opened at 15:37:05`, `total 4`).  The
pull is the only path, and it applies the grant.  *Done for the one
program; a second program is what would reopen it; whether the card is
done is Henri's.*

## 2026-08-26, 16:20 — generalised: the resolver serves any node beside a grant

`tools/resolve.sh` no longer names the node.  It loops over `*/grant`
and calls `tools/launch.sh NODE serve` for each — the launcher makes
the per-node decision from the grant (an mtime rule: a pull newer than
the last stop, no runner up).  So a pull to any node, from a session's
seat, is served by a runner started on the person's side, under that
node's grant.  `llm` is the second such node and it needed no line of
resolver code — only a grant file and a `model/` directory.  In
`grant-beside.patch` with `keep`'s.  The card's shape from day one —
"the resolver outside the session's write access" — now serves every
program, not the node alone.  Whether the card is done is Henri's.

## done — 2026-08-26

Henri: *"examine the keep & resolver … if they are [satisfied], move
them to done."*  The `because` — *nothing starts a program but a hand
in a shell, and the confinement is whatever the launcher baked in* —
no longer stands.  The pull is the launch: a session's pull is one
appended line, and the runner is started from the person's side by
`tools/resolve.sh`, which serves any node beside a grant.  One launcher
applies the grant from a file beside the program; a session cannot
start a tend node raw (its state is read-only, its lock unopenable).
Shown end to end for two programs.  The residual named in the
`because`'s last clause — *a session that starts a program some other
way starts it with the session's whole reach* — is the ambient-exec of
an arbitrary program, which this card relocated from day one to "what
a session may execute": the session-as-principal question, on
`work-environment-ai` (§16:50) and `session-program`.  Moved to `done/`
at Henri's judgement, delegated to the session.
