# session-program — a node tend runs is a program, not a session, until it carries the cords

    status   open
    because  the grant half of "a session is a program" is built: any
             node runs under one boundary — budget, grant, lifecycle —
             and adding one is adding a directory (card:keep.md,
             card:resolver.md, the grant beside the program).  But the
             llm node, the first program that is not the node, has no
             sitting limit, no lamp, no way to reach the person — so it
             is a program, not a session, and nothing here makes a node
             into the thing a person is on the other end of.  Henri, on
             the mediation order: the session's program differs from an
             ordinary one in that it "must have certain things in it" —
             the cords — "and must be able to refine its scope while
             staying under the scope where it is" (the second half is
             built; this card is the first)
    asked    Henri, 2026-08-26 — "open the cords card for the session's
             program"
    see      card:work-environment-ai.md §"2026-08-26, 15:45" — the
             frame: one boundary, the session's program a program that
             carries the cords and attenuates; §"16:38" — the second
             node's loop, and "the model has no limit, lamp or andon, so
             it is a program, not a session"
             card:cords.md — the two cords gestate has and tend built
             for its own sessions (the sitting limit installed, the
             andon blocked until 2026-08-31); this card is where they
             become a node's, not only a hosted session's
             card:keep.md, card:resolver.md — the grant, launcher and
             resolver a node already runs under; the cords hang beside
             them in the same grant file
             ~/gestate/tools/andon.sh, ~/gestate/tools/limit.sh — the
             mechanisms; the audit calls both absent here

## What it is

A node runs under keep, the leash and the launcher: it is bounded,
budgeted and lifecycled.  What it does not have is the person-facing
half — the three things that exist because someone is on the other end
of a session and not of an ordinary program:

* **a limit** — a sitting has a length, and a node that is a session
  must stop when the person's hours are spent, the way `tools/limit.sh`
  stops a hosted session.  The llm node stops on *idle*, which is the
  lifecycle; a sitting limit is the person's clock, not the program's.
* **a lamp** — a session ends with a kaizen; a node that is a session
  owes the same account of what it did, and nothing lights when it does
  not.  `tools/kaizen.sh` is the hosted session's; a node's is unbuilt.
* **the andon** — a session that hits a question it cannot answer must
  reach the person rather than guess or stop silently (`card:cords.md`).
  A node that is a session needs the cord more than a hosted one does,
  because no person is watching its transcript.

## What would make this card wrong

If no node tend runs is ever a *session* — if every program it runs is
the node's shape, a thing with no person on the other end — then the
cords belong to the hosted session alone and a node needs none of them.
But the frame Henri named (card:work-environment-ai.md, 15:45) is that
a local model *is* a session — `claude` or `llama.cpp`, pulled, under
the same boundary — and the moment tend runs one to lead the work
rather than to answer a curl, it is a session with no cords, which is
the exact hole `cords` names for the hosted case, one level in.

## What it must not become

The whole cords built three ways at once, or the hosted session's
mechanisms copied into a node on their say-so (the manifesto forbids
it).  This card owes the first small thing: one of the three, on the
llm node, shown to hold — most likely the limit, because it exists for
tend already (`tools/limit.sh`) and a node's sitting is a measurable
thing (its pulls, its runtime, in the state the launcher already
keeps).  The lamp and the andon are downstream, and the andon leans on
`cords`, which waits until 2026-08-31.

## Where it sits

Placed by a session on 2026-08-26 at Henri's ask, below the build
cards and above the count-only ones — the grant half it completes is
`keep`/`resolver`, both closed for the one program; this is the half
those cards named and did not build.  The placing is the session's; the
tiebreak is Henri's, and this is his to move.

## Next in line — Henri, 2026-08-26, for 2026-08-27

Henri named this the next card: the cords on a node come first tomorrow.
Alongside it, "examine that session as a principal thing a bit" —
`card:work-environment-ai.md` §"the toolbox idea" holds the seed and its
flaws.  Day one stays as §"What it must not become" set it: one of the
three cords on the llm node, most likely the limit, shown to hold — not
all three, not the hosted mechanisms copied on their say-so.

## 2026-08-27 — the limit, on the llm node: a grant word, shown to hold, waiting on Henri's apply

Henri: *"start on session-program, the limit on the llm node."*  Built
and measured; not yet in the tree, because `tools/launch.sh` is in the
protected set and a session cannot write it.  **`sitting.patch` at the
tree root** carries the whole of it — the launcher, one line in
`llm/grant`, five tests — and Henri's two lines are `git apply
sitting.patch` and `python3 tools/suite.py`.  (`*.patch` is gitignored;
the patch is handoff, not tree.)

**What it is.**  A grant word: `sitting MINUTES`, beside `idle` in the
grant beside the program.  `idle` is the program's lifecycle — it
stops when nothing pulls; `sitting` is the person's clock — the
launcher stops the runner when the minutes are up, pulled or not, the
way `tools/limit.sh` ends a hosted sitting.  The reason is written
into `$STATE/stopped` (whose mtime `serve` and `status` already read)
and the log, and `status` shows it.  A node with no `sitting` line is
a program, as the card's title says; `llm/grant` gets `sitting 10`,
so the llm node is the first node that carries a cord.

**Measured**, on a patched copy of the launcher, from inside the
fence, `TEND_SITTING=0.1 TEND_IDLE=60`: the server loaded in 1 s,
answered a chat request ("I'm ready to"), and was stopped at 6 s — its
pulse fresh, idle nowhere near — exit 0, the port closed, `stopped`
reading *"sitting: the 0.1 minutes of llm are up (from 05:32; the
length is llm/grant's)"*.  The five tests pass against that copy
(17 in `test_launch.py`, 12 before); they are red against the tree's
launcher until the patch lands, which is why they travel in the patch
and not in a commit.

**The decisions, each one small.**  (1) *The door is the grant, not the
pull.*  The hosted limit takes its length from a word Henri types; a
node's pull is the one thing a session writes, so a pull's text is
never read as a grant — `pull sitting 900` is a line in the pull file
and nothing more, and a test holds it.  That is `test_limit.py`'s
asymmetry on a node: a node may end a sitting early (idle) and can
never extend one (keep hands it its model and its state; the grant is
not in its write).  (2) *A close, not a crash.*  The sitting exits 0
with a reason; the leash's wall budget exits 124 with none.  A sitting
longer than the leash's 900 s is cut by the leash first, and sizing
the budget is `grant`'s dial (doc/kaizen/2026-08-25-1436.md item 2),
not this word's — so `sitting 10` sits under it.  (3) *Ten is a number
picked in writing*, like `idle 60` and the leash's 900; the log and
`stopped` are what settle it.  (4) *The person's clock is untouched.*
"One desk, one clock" is about `~/.local/state/gestate/sittings.log`,
which is Henri's; a node's sitting is the node's own, in its state
directory.  Whether a node that leads work should *also* stop when
Henri's desk sitting closes is a question this reading did not
answer — it is his, and it would be a second word, not this one.

**What is not built**: the lamp (a node owes an account of what it
did, and nothing lights when it does not) and the andon, which leans
on `cords` and waits until 2026-08-31.  One of three, as §"What it
must not become" set it.  The card stays open.
