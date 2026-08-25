# Sheet 1 — What holds, and why

*The tend rules: fifteen invariants a session works under, each enforced
by a mechanism in the tree and not by good intentions — the whole point
is that the boundary sits where a session cannot reach it.  This file is
the canonical text; `tend-sheets.html` in this directory is the same two
sheets, styled and printable as A4.  What keeps it honest is in
[README.md](README.md).*

## The boundary

- **R1** — The enforcement boundary lives *outside* a session's write
  access, or it is decoration.  `vision.md`, the founding line.
- **R2** — A session may not widen its own reach; the bound is the
  person's, set in the hook's own line.  `tools/fence-hook.sh`,
  `TEND_REACH_ALLOW`.
- **R3** — The scripts that enforce are read-only to the session and
  denied to its edit tools.  `tools/sandbox.sh`, the protected set
  (`board/self.md`).
- **R4** — A restraint must be able to say when it is off; silence is
  the failure it exists to end.  `tools/fence.sh`, at every prompt.

## The record

- **R5** — A card names a *problem*, in the words of whoever had it —
  never a fix.  `test/test_board.py` refuses a card without one.
- **R6** — Every sitting ends with a kaizen; the measure is commits
  since the last one, not the date.  `tools/kaizen.sh`, the lamp.
- **R7** — Git is the only canonical copy: restore means *checkout*,
  never a second embedded copy.  `tools/fence.sh --restore`.
- **R8** — Every commit runs the gates first; a red gate refuses the
  commit, working tree unmoved.  `tools/pre-commit.sh`, `tools/suite.py`.

## Honesty

- **R9** — Errors are never silent; a sensor that cannot read a value
  says `?`, never a wrong number.  `tools/leash.sh`, the cpu column.
- **R10** — Measure, don't assert or borrow; a practice owes *this is
  what it caught, that you would have shipped.*  `manifesto.md`.
- **R11** — A mechanism a session cannot test, it *proposes* — it does
  not declare it done.  `doc/kaizen/`, a standing rule.
- **R12** — Nothing unexpected, silently; loud within one prompt beats
  quiet and correct-looking.  `vision.md`.

## The program

- **R13** — A hang is a crash; a wall budget bounds every run, and
  overrun is exit 124, said out loud.  `tools/leash.sh`
  (`leash → sandbox → cmd`).
- **R14** — A program opens where it was left, from a plain file a
  person can read without it.  `node/node.py`, the state file.
- **R15** — A program runs while something pulls it and quits itself
  when nothing does; the default is off.  `node/node.py`, the pull
  lifecycle.

## The mechanisms these rest on

| path | what it is |
|---|---|
| `board/` | one file per problem; open, `board/done/`, `board/later/` |
| `tools/fence.sh` | is the deny-list still in force? |
| `tools/sandbox.sh` | the tree as a session's whole world (bubblewrap) |
| `tools/fence-hook.sh` | wraps every command: leash, then fence |
| `tools/leash.sh` | one run, budgeted, with a ledger line |
| `tools/limit.sh` | a sitting has a length; ending it is one-way |
| `tools/kaizen.sh` | the lamp that ends a sitting |
| `node/node.py` | the first program tend runs, not one that governs |

*The through-line: almost every rule is the same rule — the thing that
restrains sits where the restrained party cannot reach it.  tend is the
second vehicle of the method grown in `~/gestate`; it carries the
mechanisms and not the prose.*
