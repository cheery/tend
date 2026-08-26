# tend

*A workspace over Linux where sessions and programs get a budget, a
grant and a lifecycle — and where the thing that restrains a session is
not something the session can edit.*

**What it is.**  Tend runs things — AI sessions, and the programs they
write — under three bounds that live outside the thing bounded: a
**budget** (wall clock, CPU, memory, with a ledger line left behind), a
**grant** (a program reads only what it was handed, and writes only
where it was told), and a **lifecycle** (a program opens where it was
left, runs while something pulls it, and quits by itself when nothing
does).  Being wrong has to be visible, so every one of those has a
check that says when it is not in force, and a lamp rather than a rule
wherever a check cannot reach.

**What it is not.**  Not an operating system — that is a later
question, `spec/os.md` holds the properties it would have to keep.  Not
a fork of `~/gestate`: it is the second tree run by the method that
grew there, and it carries that method's *mechanisms* and none of its
prose, one at a time, each named where it came from.  And not a
platform that needs an account, a service, or your presence:
everything it keeps is a plain file you can read without it
(`vision.md` §"What tend won't be").

**Why it is its own repository.**  The first decision of this tree,
2026-08-24: *the enforcement boundary lives outside the session's write
access.*  A session in gestate can edit anything in gestate, including
its own fence; it cannot edit tend.  A restraint the restrained party
can edit is decoration.  Sessions and programs are being worked as
two arms at once — which bound matters most is a question the evidence
has not answered yet.

## Try it

Somebody who has never read this repository should be able to start a
program in it, see it stop when they stop pulling, and find out what it
did — without being told anything first.  That is the stranger test,
and this is it:

```sh
git clone https://github.com/cheery/tend.git && cd tend
tools/toolbox.sh                # says what this machine is missing, installs what it can

node/run.sh run --idle 3        # in one shell: the node runs while it is pulled
node/run.sh pull                # in another, a few times
                                # stop pulling; watch `run` exit on its own
node/run.sh status              # what it did — also readable as node/state/node.state
```

The node is the first program of tend's own (`board/done/pull.md`): a
tally, whose whole memory is one JSON file.  `node/run.sh` runs it
confined by `tools/keep.py` — it may read its own code and write its
own state directory, and nothing else — which needs Landlock (Linux
5.13+, no root, no build).  Where that is absent, keep refuses out loud
rather than running the program unconfined.

The suite is `python3 tools/suite.py` (pytest), and
`tools/pre-commit.sh --install` puts it on every commit.

## The pieces

| piece | what it does | where |
|---|---|---|
| **the fence** | a command runs with this tree as its whole world; a session cannot widen it | `tools/sandbox.sh`, `tools/fence.sh`, `tools/fence-hook.sh` |
| **the leash** | one invocation under a budget, and a line in `~/.local/state/tend/leash.log` | `tools/leash.sh` |
| **keep** | a program reads only what it was handed, writes only where told | `tools/keep.py` |
| **the node** | the first program: opens, serves pulls, quits when they stop | `node/` |
| **the sitting limit** | a person's hours are theirs; a session cannot extend a sitting | `tools/limit.sh` |
| **the kaizen lamp** | every sitting ends with a kaizen, and the lamp says when one is owed | `tools/kaizen.sh`, `doc/kaizen/` |
| **the gates** | the suite, at the commit that would break it | `tools/suite.py`, `tools/pre-commit.sh` |
| **the board** | one card per problem; a `because` is a problem, never a fix | `board/` |
| **the summary** | two one-page sheets — the rules, and the surface you work — with a gate and a lamp against rot | `doc/summary/` |

Three of these are **keys the person turns, not a session**:
`tools/hook-installer.sh` (put the fence on every command),
`tools/reach-allow.sh` (what the fence may be asked to reach) and
`tools/fence.sh --protect`.  Hook config is enforcement, and the
settings file is the person's.

**Not built yet:** a way for a session to reach the person mid-run —
the andon.  `board/cords.md` says why it waits, and until when.

## Read next

- `board/README.md` — how the work is worked; the first thing a session reads
- `vision.md` — what tend is for, dated line by line
- `manifesto.md` — the two rules everything here is built under
- `spec/os.md` — the properties, in the words they were first asked in
- `doc/summary/rules.md` and `doc/summary/interfaces.md` — the two sheets

---

*Written by a session of `~/gestate` on 2026-08-26, at Henri's ask —
"kirjoita tendille README" — after a search engine, asked to describe
tend, had one line to read here and invented the rest.  Left in the
tree uncommitted, for his verify.*

*Verified against the tree by a tend session on 2026-08-26 — every
path named above exists, the try-it verbs are the node's own, the three
keys are `tools/sandbox.sh`'s protected set — and committed at Henri's
"you are free to keep it or drop it".*
