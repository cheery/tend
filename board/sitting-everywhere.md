# sitting-everywhere — the sitting limit holds in two trees, and the grant it offers has no shape

    status   open
    because  "I still have the problem that I do overwork.  The solution
             to that is perhaps to make the tools we built into gestate,
             system-wide.  So that I always have them here when I work.
             I have solved this problem with gestate already." — Henri,
             2026-08-27
    asked    Henri, 2026-08-27; a gestate session questioned it in one
             batch and he answered "defaults, write the card, but I have
             a feeling we need to refine this.  We won't get it right at
             the start.  But that's ok.  Lets do and find out."
    see      ~/gestate/tools/limit.sh and tools/limit.sh — the two copies,
             58 non-comment lines apart, writing one ledger
             ~/.local/state/gestate/sittings.log — the ledger, and
             ~/gestate/tools/sittings.py, the summary that will read the
             new rows back
             ~/gestate/doc/memory/a-sitting-is-a-body-constraint.md — a
             session may call stop and never extend; the line this card
             must not cross
             doc/reading-2026-08-27.md — the reading that measured the day
             card:session-program.md — the same limit on a node, and its
             decision (1): the door is the grant, not the pull
             card:fence.md — the deny-list this card has to reach into

## The ask

Three messages, 2026-08-27, in order.

> Well.. I still have the problem that I do overwork.  The solution to
> that is perhaps to make the tools we built into gestate, system-wide.
> So that I always have them here when I work.  I have solved this
> problem with gestate already.

> I think that these improvements would be okay, but I also need a way
> to override them.  but, it is the case that I must present a reason
> for when override is done, and the session needs to verify the reason
> is real.

> defaults, write the card, but I have a feeling we need to refine
> this.  We won't get it right at the start.  But that's ok.  Lets do
> and find out.

## What this is, what it is not, and when it runs

**What it is:** the sitting limit — `limit.sh --hook` on every prompt,
the ledger, the block, the grant word — made to hold for every session
on this machine rather than for sessions started in two directories;
and the grant given a shape, so that an extension is an *override* with
a reason the machine can check, rather than a new sitting wearing the
grant word.

**What it is not:** a posture reminder, a break nagger, or anything a
session says to the person about how long they have sat.  The rule
stands: **a session may call stop and never extend.**  Nothing here
gives a session a way to lengthen a sitting, and nothing here asks a
session to judge whether a person's reason is good.

**When it runs:** on every prompt, in a hook, before the session sees
the prompt.  The check is the hook's; the session only sees its
verdict.

## Found by looking — 2026-08-27, a gestate session

**The limit is a project hook.**  `~/gestate/.claude/settings.json` and
`~/tend/.claude/settings.json` each carry `limit.sh --hook` under
`UserPromptSubmit`.  `~/.claude/settings.json` carries one hook,
`SessionStart`, gated to `$PWD = ~/gestate`.  A session started
anywhere else has no limit, no ledger row, nothing.

**The two copies drift.**  58 non-comment lines apart on 2026-08-27,
sharing one ledger whose event names are agreed by hand
(`~/gestate` commit `5c00576`).

**The grant has no shape.**  `sitting N` takes any N; nothing checks the
gap since the last block.  Ledger, 2026-08-26, in tend, where the hook
*was* installed: 9 blocks, 10 grants by hand — 15, 20, 10, 120, 120,
10, 45, 120, 60, 60 minutes — and the desk retaken within minutes after
8 of the 9 blocks; longest sitting 2h04m.  So the reach is half the
problem: a system-wide copy of today's grant reproduces yesterday in
every directory.  In gestate the sittings stayed at 10–30 minutes; in
tend `sitting 120` was typed three times.

**A session cannot grant.**  `limit.sh reset` inside a session is
refused — *"a sitting is not granted from inside a session"* — and the
grant is *the one word a session cannot forge*.  This is the property
the override must keep.

**A session asked by the person at the desk whether their reason is
real will find it real.**  That is fluency, not evidence — the pressure
that shipped gestate's auto-audition green.  So "the session verifies"
can only mean *the session runs a check whose verdict is a program's*.
Anything a session would have to judge is not verification.

## Questions — asked in one batch, 2026-08-27, answered "defaults"

**1. What can be verified?**  A closed set of reasons the machine can
check, each a check the hook runs itself and the session only reports:

| word | the check | passes when |
|---|---|---|
| `run` | a process of Henri's is alive — a suite, cargo, a render | a pid, not a claim |
| `commit` | the session's tree is dirty | `git status` says so |
| `andon` | a cord was pulled and is unanswered | the andon's own record |
| `patch` | a `*.patch` for his hand sits in a tree | the file exists |

`sitting 15 because commit` → the hook checks, honours it if true,
refuses out loud if not, and writes either way.  Anything outside the
set is not a verified override, whatever the session thinks of it.

**2. How much does an override buy?**  Fifteen minutes, and the same
reason not twice in a row — `commit` buys the time to commit, not a
second sitting.

**3. The reasons no machine can check** — a visitor, tomorrow's travel.
Honoured **once a day**, written to the ledger as `unverified`, and
counted in the weekly summary beside *"taken again straight after N of
them"*.  Not refused: the first evening this card exists is a demo to a
visitor, and a rule that fails on its first evening gets removed.  Once
a day is a number picked in writing, like `idle 60`; the ledger settles
it.

**4. Where does it live?**  Here.  One copy of `limit.sh` in tend's
protected set; the user-level hook in `~/.claude/settings.json` pointing
at it; gestate's project hook retired in the same change, or every
prompt is noted twice and the ledger lies; and the deny-list reaching
`~/.claude/**`, or the hook is decoration — the line this tree was
founded on.  The settings edits go through Henri's hand: sessions are
denied `.claude/**` on purpose.

**His answer to all four:** *"defaults … but I have a feeling we need
to refine this.  We won't get it right at the start."*  So every number
above — four words, fifteen minutes, once a day — is a first guess with
a ledger under it, and the refinement is read off the ledger, not
argued.

## The postcondition, before anything is built

> Wherever Henri starts a session on this machine, a sitting ends when
> its time is up, and it goes on only for a reason the machine could
> check — and the ledger says which.

## What a session does on day one

One thing, shown to hold: the grant row grows `reason=` and
`verified=`, and `sitting N because <word>` for the four words is
checked by the hook — red with the check faked, green with it real —
in tend's copy only.  Not the user-level move, not the fence, not the
once-a-day: those are day two and go through his hand.

## What it must not become

* **A session extending a sitting.**  If any path here lets a session's
  output lengthen the time, the card has failed at its one rule.
* **A session softening a refusal.**  When the hook says no, the
  session says what the check found, and stops.
* **A judge of reasons.**  The set is closed and the checks are
  programs.  A reason the machine cannot check is `unverified`, once a
  day, and that is the whole of what the session may say about it.
* **A nagger.**  The ledger reads back to Henri on the keeper's evening;
  no session tells him what it shows unless he asks.

## Where it sits

Unplaced — at the end, as a new card arrives; the session that wrote it
asks whether it belongs further up, and the tiebreak is his.
