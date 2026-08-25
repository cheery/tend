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
