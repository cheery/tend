# Sheet 2 — The surface you work

*Everything human-facing in tend, by kind: the keys only the person may
turn, the instruments a session and the person both run, what the tree
says back unbidden, the plain files a person reads — and the one
outward cord, the andon.  Canonical text; the styled, printable version is
`tend-sheets.html`.  What keeps it honest is in [README.md](README.md).*

## Keys you hold — yours, run unfenced

These change what a session is allowed to do.  They live outside the
tree, or read-only inside it, on purpose.

- `tools/reach-allow.sh net,audio,…` — **set the fence's reach bound.**
  Writes `TEND_REACH_ALLOW` on the hook's line: the rows a session may
  ask for.  Takes only a row the fence can be asked for (`--rows` lists
  them, and marks which are allowed); any other name is refused before
  the file is touched.
- `tools/hook-installer.sh` — **install the per-command fence.**  Edits
  `.claude/settings.json`; hook config is enforcement, so the edit is
  the person's.
- `tools/fence.sh --protect` — **lock the enforcement scripts.**  Adds
  the missing deny rules and nothing else; narrows, never widens.

*The two `~/` scripts are host-side and invisible from inside the
fence; `tools/fence.sh` is in the tree but in the protected set, so a
session cannot edit it to effect.*

## Instruments you run

- `tools/sandbox.sh --check` — prove the fence is up: the sitting clock
  first, then the secrets.  Also `--rows`, `--protected`.
- `tools/fence.sh` — is the deny-list in force?  `--restore` puts a
  lost file back from git.
- `tools/leash.sh -t -c -m -- cmd` — run one thing under a wall / CPU /
  memory budget; leaves a ledger line.
- `tools/limit.sh` — where the sitting clock stands: how long in, how
  long left.
- `tools/kaizen.sh want "why"` — read the lamp, or declare a kaizen
  owed and carry the reason forward.
- `tools/toolbox.sh` — set a clone up and say what a machine is
  missing; the stranger's first command.
- `node/node.py run · pull · status` — the first program: start it,
  pull it, read what it did.

## What the tree says back — unbidden

- **Every prompt** — three lamps run before the person's words reach
  the session: the kaizen lamp (`tools/kaizen.sh`, a sitting owes its
  close), the sitting clock (`tools/limit.sh`), and the fence lamp
  (`tools/fence.sh`, red if the deny-list weakened).
- **Every command** — the fence hook (`tools/fence-hook.sh`) wraps it as
  `leash → sandbox`, or refuses a reach outside the bound with a reason.
- **Every commit** — the gate (`tools/pre-commit.sh`) runs the suite and
  refuses a red one, naming what failed and how to skip it on the record.

## Plain files you read

- `board/` — the work itself, one card per problem; the person fills
  it, a session works it down.
- `~/.local/state/tend/leash.log` — every budgeted run: when, how long,
  what it cost, whether the budget applied.
- `doc/kaizen/` — one file per sitting: what went right, what went
  wrong named as whose, what to change.
- `node/*.state` — a program's whole memory, as JSON you can read
  without the program.

## The andon — the outward cord (`card:cords.md`, done 2026-08-27)

**The andon** — `tools/andon.sh`: a session writes its question first
(`ask`), then rings the person through the PipeWire socket (`ring` —
at most three, eight seconds apart, refused within ten minutes of the
last, refused with nothing asked).  The record —
`~/.local/state/tend/andon.pending`, `andon.log` — is what `sitting N
because andon` is granted on, read by the hook, not the session.
`answered` is the person's word, refused inside the fence.  The count
of guessed questions closed at zero after four days; the cord's first
loop — ask, ring, answered — closed on 2026-08-27 at 17:05.

---

*Keys turn the bound; instruments read it; the tree speaks in lamps,
never alarms.  The one outward cord — a session reaching the person —
rings through a socket and leaves a record.*
