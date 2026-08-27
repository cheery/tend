# install — the boundary lives in the tree it is meant to be outside of, and developing it costs too much

    status   open
    because  the files that enforce the boundary are the tree's own, so
             protecting them and developing them are one directory
             pulling two ways.  A session cannot edit a restraint here —
             the fence binds `tools/*.sh` read-only — and landing a
             vetted change to one costs a clone, a hand outside the
             fence, and git operations that have twice moved `main` by
             accident (2026-08-27); "we do way too much effort here now"
             (Henri, 2026-08-27).  And the copy actually in force still
             lives in the tree, so the boundary a session cannot reach
             is not truly on the machine — only read-only inside one
             fence, which the same session configures
    asked    Henri, 2026-08-27 — "I think that we maybe need to create
             an install script that installs this to the machine and
             protects those files, rather than the files in this tree.
             Allow local testing but also allow install.  We do way too
             much effort here now."
    see      card:self.md — the protected set, the five-plus scripts the
             hooks run; the files this card is about
             board/done/fence.md — the ro-bind that makes them read-only
             in the tree, and its own "what it cannot do: stop the write"
             card:work-environment-ai.md — "the enforcement boundary
             must live outside the session's write access"; this card is
             *where* that outside is, machine vs tree
             tools/toolbox.sh — `--install` already puts the pre-commit
             hook on the machine's side; this extends that idea to the
             restraints themselves
             spec/os.md — property 2 (install testing not hard) and
             property 5 (an install's configuration is recorded in the
             program's node, reconfigured by pull)
             the clone-not-worktree lesson (board/README.md §"What the
             days taught", 2026-08-27) — the effort this names, written
             down the same day it grew too large

## What Henri proposed — the solution, kept out of the `because`

An install script that installs tend **to the machine** and protects
the installed files there, rather than protecting the files in this
working tree.  Two modes, both kept:

* **local testing** — the tree stays a free workbench: a session edits
  and runs anything, including the restraints, because the tree is not
  what is in force.
* **install** — the vetted restraints are put in force at a machine
  location outside any session's write access, the way `limit.sh` and
  the fence are meant to be — installed, not merely read-only inside a
  fence the session's own settings configure.

## What it is, at the level a card may name

Today one copy of each restraint is both the thing developed and the
thing enforced, and the fence resolves the conflict by binding the
tree's copy read-only inside itself.  That is why a change to a
restraint is expensive (the clone, the outside hand) and why the
enforcement is still only as strong as the tree it lives in.  The card's
problem is that conflation.  A resolution separates the two copies — a
workbench copy that is free, and an installed copy that is in force and
out of reach — and an install step is what moves a vetted change from
the first to the second.  Which machine location, how the installed copy
is kept honest (`done/fence.md`'s integrity check, one level out), and
how an update is applied without a session doing the applying (the
unfenced-lander shape `resolve.sh` has) are the card's to work, not to
decide here.

## What would make this card wrong

If installing to the machine only moves the same problem — a session
that can run the install script can install a weakened copy, so the
boundary is no better and the effort is worse — then the card is a
relocation, not a resolution, and it should say so and shelve.  **That
is a measurement, not an opinion**: the install path must be shown to
be one a session cannot drive (the same property `limit.sh reset` and
the settings edit already have — the person's, from outside the fence),
or the card has moved the boundary without keeping it.

## What it must not become

* **A second place the restraints can drift.**  Two copies is the
  point, but a copy in force that nothing checks against the vetted one
  is `done/fence.md`'s silent-failure a level out.  The installed copy
  owes an integrity check that reads it back, or it is a mood.
* **A session's own install.**  If a session can run the install and
  choose what it installs, the machine copy is inside the session's
  reach after all.  The install is the person's hand, or a lander
  outside the fence — never the restrained party installing its own
  restraint.
* **A rewrite of what works.**  The tree, the fence, the leash, keep and
  the launcher stay; this card changes *where the authoritative copy
  lives and how a change reaches it*, not what the restraints are.

## Where it sits

Placed at 2 by the session that wrote it, below `work-environment-ai`
and above `session-program` — because it advances that card's own
principle (the boundary outside the session's write access) and because
the effort it names is a tax on every other card that touches a
protected file, paid twice already on 2026-08-27.  That reasoning is the
session's; ranking a fresh, unbuilt card above the build cards is a
stretch a session should not make quietly, so the placing is marked and
the tiebreak is Henri's, and this is his to move.
