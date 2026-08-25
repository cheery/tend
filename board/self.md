# self — the fence guards the settings but not the code that enforces them, nor the keys the person turns

    status   open
    because  `.claude/` is read-only inside the fence, but the scripts
             that ARE the fence — `tools/sandbox.sh`, `tools/fence-hook.sh`
             — sit in the tree writable, and the hook reads them fresh on
             every command, so a session can widen its own fence by
             editing the fence and have it take on the next call, before
             any gate sees it; and the commands a person runs to move the
             bound (`~/reach-allow.sh`, `~/hook-installer.sh`) are
             unguarded keys a session could edit to act through the
             person's own hand
    asked    Henri, 2026-08-25 — "I think these commands could be defined
             in this project in their own directory, what do you think
             about that?" then, on the reading below, "make a card from
             it"
    see      card:fence.md — the same shape one level up: is the deny-list
             still in force; this card is, is the code that enforces it
             still what it says, and can the session change it
             tools/sandbox.sh, tools/fence-hook.sh — the enforcement code,
             writable from inside the fence, measured below
             tools/reach-allow.sh?, tools/hook-installer.sh? — where Henri
             asked these might live; they are in `~` today, and this card
             is what would have to be true first
             vision.md — "the enforcement boundary lives outside the
             session's write access"; today that holds for the settings
             file and not for the fence's own code

## The measurement, taken 2026-08-25

`test -w` from inside the fence, the day the fence was built:

    tools/sandbox.sh        WRITABLE
    tools/fence-hook.sh     WRITABLE
    tools/leash.sh          WRITABLE
    .claude/settings.json   read-only

So the protection covers the settings file and stops there.  The fence
has a blind spot shaped exactly like itself.

## Two things in the blind spot

**The enforcement code.**  A fenced session edits `tools/sandbox.sh` —
say, deletes the `--tmpfs "$HOME"` line — and does not commit it.  The
hook's next call reads the edited script, and the fence for that command
is whatever the session just wrote, with `~/.ssh` back in reach.  The
pre-commit gate catches a *committed* change, if a test names it; the
live window is the uncommitted edit, which is the state of every edit
until the moment it is committed — i.e. the normal working loop.  The
gate is the wrong instrument for this the same way incident-counting was
the wrong instrument for containment: it arrives after the fact.

**The person's keys.**  `~/reach-allow.sh` and `~/hook-installer.sh`
edit `.claude/settings.json`.  A session cannot run them to effect —
inside the fence `.claude` is read-only, and they are outside the tree
besides — but if they lived in the tree a session could *edit* them, so
that the next time the person runs `reach-allow.sh bus` by hand,
unfenced, it does what the session wrote, as the person.  That is
escalation through the person's own hand, and it is why the two scripts
are in `~` today and not in `tools/`.

## The answer is a set, not a folder

Henri's question was where these commands should live.  The honest
answer is that *where* is the wrong axis: the settings file lives in the
tree and is safe, because it is protected two ways — the fence binds it
read-only, and the deny-list denies `Edit(./.claude/**)`.  The same two
extend to a **protected set**: the fence binds the enforcement scripts
read-only too, and the deny-list denies editing them.  Once that is
true, the scripts can live in the tree — gated, discoverable, one clone
away — because being in the tree no longer means being writable.  The
directory Henri wants is downstream of the set, and safe only after it.

## What would make this card wrong

If commit discipline is enough — if every path that enforces is covered
by a test that fails on any change a session would make to it, and a
session never runs from an uncommitted tree — then the live-edit window
is closed by the gate alone and a read-only bind is belt on braces.  But
the fence's own scripts have no such test yet, and "never runs
uncommitted" is false the instant a session edits and runs, which is the
loop itself.  The measurement that settles it is already sketched above
and can be made sharp: from inside the fence, edit `tools/sandbox.sh` to
drop a bind, run one command, and see whether it runs under the widened
fence.  If it does, this card stands.

## What it must not become

A second `.claude`.  The protected set is the few paths that *enforce* —
not everything in `tools/`, which would make the tree read-only to the
work and defeat itself.  `leash.sh` shapes cost and is not in it;
`sandbox.sh` and `fence-hook.sh` are, because the hook trusts them by
name every command.  The line is: a path is in the set if a session
editing it changes what the session is allowed to do, before anyone
looks.

## 2026-08-25, afternoon — measured from inside, and the set built

**The measurement, sharp.**  Henri: *"Lets do self."*  From inside the
fence, the card's own probe, in two attempts:

| route into `tools/sandbox.sh` | stopped by |
|---|---|
| `sed -i` dropping the `.claude` ro-bind | the auto-mode **classifier** — and it took two plain file reads in the same batch down with it |
| the Edit tool adding `--setenv TEND_SELF_PROBE …` | **nothing** — and the very next command ran with `TEND_SELF_PROBE=edited-from-inside`, `TEND_FENCED=1` |

So the hook reads the edited script fresh, the edit is in force one
call later, and the card stands.  The second attempt was chosen to
weaken nothing — a marker proves the live read exactly as well as a
dropped bind does, and the session did not route around the
classifier's refusal; it used the tool the deny-list does not name,
which is the finding.  `test -w` inside, the same minute: every script
in `tools/` `WRITABLE`, `.claude/settings.json` alone read-only.

**The set is wider than the two the card named, by the card's own
line.**  The three `UserPromptSubmit` hooks and the `PreToolUse` hook
run *outside* the fence, as the person, at the next prompt or the next
command — so a session editing `tools/fence.sh`, `tools/limit.sh` or
`tools/kaizen.sh` gets its code run unfenced with write access to
`.claude/` before anyone looks.  That is the escalation-through-the-
person's-hand the card describes, one directory over.  The set is
therefore *the scripts the hooks run*: `sandbox.sh`, `fence-hook.sh`,
`fence.sh`, `limit.sh`, `kaizen.sh`.  `leash.sh` stays out, as the card
said.  `pre-commit.sh` stays out too, and not for a good reason: the
gate is `.git/hooks/pre-commit`, and `.git/` is writable inside — a
session that wants past the gate edits the hook, not the script, so
binding the script alone would be a lock on a door with no wall.
*Session's decision, marked so; the `.git/hooks` question is its own
line, not this card's.*

**Built.**  `tools/sandbox.sh` binds the set read-only over the tree
(`--protected` lists it; `--check` probes each), the same way it binds
`.claude/`.  In force from the next command after the edit, measured:
append → EROFS, `mv` → EBUSY, and `leash.sh` still writable.
`tools/fence.sh` now checks the matching `Edit(./tools/…)` rule for
each — read from `sandbox.sh --protected`, so there is one list — and
checks the `PreToolUse` line, which it had never looked at: the fence
around every shell command was one hook entry a session could drop
without the check noticing.  `test_sandbox.py` holds that every script
a hook in this clone's settings runs is in the set, so a hook added
without protecting its script goes red at the gate.

**The person's key, in the tree.**  Henri's question was where
`reach-allow.sh` and `hook-installer.sh` should live.  The card's
answer was *downstream of the set*, and the set exists now, so the
first key moved: `tools/fence.sh --protect` adds the load-bearing rules
that are missing and nothing else — it can narrow and never widen,
refuses a file that does not parse, and is idempotent
(`test_protect_adds_only_what_is_missing_and_never_widens`).  It is safe
in the tree because `fence.sh` is in the set: read-only to a fenced
shell, and — once he runs it — denied to the edit tools.  The other two
keys widen, and stay in `~` until someone argues otherwise.

**What is owed.**  The deny-list half is his: `tools/fence.sh
--protect`, once, unfenced.  Until then `test_the_fence_is_up_in_this_
clone` is red, the lamp says so at every prompt, and the gate refuses
the commit — the fence card's precedent, kept.  After it, the edit-tool
route this measurement used should come back *"denied by your
permission settings"*, which is the demonstration in the manifesto's
sense: the route that went through this afternoon, refused.  The cost,
said plainly: a fix to any of the five is no longer a fenced session's
to make; it is the person's, or an unfenced session's, and `limit.sh`'s
twin debt to gestate now has that step in it too.

**Demonstrated, 2026-08-25, 14:xx.**  Henri: *"It's in."*  `tools/fence.sh`
green on this clone, 139 passed at the suite, and the Edit tool on
`tools/sandbox.sh` — the route that went through an hour earlier —
refused: *"File is in a directory that is denied by your permission
settings."*  Both ways, both halves, same as `.claude/`.  What is still
open on this card is only what it must not become: the `.git/hooks`
line above, and the two widening keys in `~`.
