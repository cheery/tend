# install — the boundary lives in the tree it is meant to be outside of, and developing it costs too much

    status   done — 2026-08-27
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

## 2026-08-27 — researched and built: `/usr/local/lib/tend`, root-owned, installed from HEAD

Henri: *"research which approach to install location would make most
sense, then do that."*

**Three locations weighed, one measurement each.**

* **A prefix under `$HOME`** (`~/.local/lib/tend`) — the XDG answer, no
  sudo.  Measured against the other tree: gestate's deny-list has no
  rule for `~/tend/**` or `~/.local/**`, and its fence wraps only
  `pytest` and `cargo` — so every user-owned file on this machine is
  inside a gestate session's Bash reach, and "outside the session's
  write access" would rest on the harness classifier alone, the layer
  `tools/fence.sh`'s header already declines to lean on.  (The same
  measurement says `tools/limit.sh`'s header — *"this one, a gestate
  session cannot reach"* — has been aspirational since it was written.)
  Inside tend's fence a `$HOME` prefix would be *invisible* (`$HOME` is
  a tmpfs) rather than read-only, so `--check` could not compare it from
  a session's seat.  Kept as the fallback for a machine without sudo
  (`TEND_PREFIX=`), and `--check` says it is the weaker one.
* **`chattr +i` on the tree's own files** — root-only to set, and it
  protects the files *in the tree*.  Rejected on the ask itself
  ("rather than the files in this tree"): it keeps the workbench and the
  enforcement in one directory, which is this card's `because`.
* **`/usr/local/lib/tend`, root-owned — chosen.**  Refused by the kernel
  to every uid-1000 process, fenced or not, from either tree; `/usr` is
  already ro-bound inside the fence, so the copy in force is visible
  there and unwritable by construction rather than by a bind this tree
  configures; and installing needs `sudo`, which the deny-list already
  refuses a session — the person's hand by a rule that exists, not a
  new one.  FHS puts locally-installed software there.

**Built: `tools/install.sh`**, 9 tests.  Unprotected on purpose — a
session can write it because a session cannot run it to effect: refused
inside the fence, sudo denied, `$HOME` a tmpfs.  It installs **HEAD,
never the working tree**: a change reaches the machine through a commit
and a commit through the gate, and an uncommitted edit to a restraint is
named and left behind.  `installed` beside the copies records the
commit, date, source tree and a sha256 per file (spec/os.md, properties
5 and 6).  `--check` reads it back against HEAD — absence, drift, a
copy writable by the user, and which copy each hook line runs — and is
red on any.  `--hooks` prints the settings lines as they would read;
`--hooks apply` is the person's edit, backed up, idempotent, keeping
the reach bound.  The clone-and-outside-hand tax the card names becomes
`git commit` and one sudo prompt.

**Found on the way: the installed set is larger than the protected
set.**  `tools/leash.sh` and `tools/keep.py` are `WRITABLE` inside the
fence (measured, `test -w`), and both run on the person's side: the
fence-hook rewrites every command to `leash.sh -- sandbox.sh …` and the
harness runs *that* on the host, so leash.sh is the program that execs
the fence, unfenced; the launcher confines every node through keep.py.
`test_sandbox.py` asserted leash.sh *out* of the set "because it shapes
cost" — true, and beside the point.  `done/self.md`'s own line puts
both in, and `tools/andon.sh` with them (its record is what `limit.sh`
grants a sitting on).  The install closes the gap by construction once
the hooks run the prefix; until then the branch's second commit widens
the tree's set, belt while the braces are fitted.

**What a session could not do, and where it is.**  Every protected
script derived its root from its own location and reached its siblings
through it — so an installed `kaizen.sh` would have read the prefix's
git log, and an installed fence-hook run the tree's sandbox.  The
change — `here` for a sibling, `TEND_TREE` for the tree, the fence-hook
passing it on and the sandbox unsetting it inside — touches nine
protected files, so it is the branch **`install-day1`** (three commits:
the split and the andon word; the set widened; the `audio` row
narrowed), fetched into this tree's refs from the clone, suite green
there.  Henri's lines, in order, from outside the fence:

    git merge install-day1
    sudo tools/install.sh
    tools/install.sh --hooks apply
    tools/install.sh --check
    tools/sandbox.sh --check

and a new prompt after — hooks are read at the next prompt.  If a hook
misbehaves, `cp .claude/settings.json.before-install .claude/settings.json`
is the way back.  The root-owned `--check` going green is the one
measurement this card's "what would make it wrong" asks for and a
session cannot take.

**Day two, not built.**  The "local testing" flip: once `--check` says
the installed set is in force, the tree's ro-binds and `Edit(./tools/…)`
rules can come off and the tree is the free workbench Henri asked for —
his call, after the measurement, not before it.  `hook-installer.sh`
and `resolve.sh --install` still insert tree lines and must learn the
prefix.  And the lander: `install.sh` *is* a lander for restraints, so
the unfenced lander the 0710 kaizen called card-shaped is half this
card; the other half, fast-forwarding `main` after the gates, is not.

## 2026-08-27, 16:17–16:30 — installed, and the measurement taken from both sides

**The first install failed, and the failure was the script's.**  Henri
ran the five lines; `sudo tools/install.sh` ran as root, for whom the
prefix *is* writable, so the script took the "prefix is yours" branch —
and that branch spelled the user mode as `755 - 222` in decimal: octal
533/422, `-r---w--w-`, unreadable to anyone but root.  Every hook died
`Permission denied`, `--check` fell over on `sed`, and he took the hooks
off by hand to get a prompt back — which left the session that fixed it
running **unfenced** for the fix (it touched `install.sh`, its test and
`git add`, nothing else, and says so in the kaizen).  Fixed in 4cfcb74:
uid 0 installs root-owned 755/644, a user prefix gets 555/444 spelled
out, and `--check` reports an unreadable copy as a finding with the fix
named.  The gate held the fix out until `tools/fence.sh --force` put
his settings back — the gate reading a hand-edit in progress as the
fence being down, which it was.

**The second install went green, from outside**: all twelve files at
HEAD, read-only to him; all five hooks running the installed copies;
`tools/sandbox.sh --check` 35 of 35 — the installed fence, governing
the tree it was told about by `TEND_TREE`, with the widened set
(leash.sh, keep.py, andon.sh) read-only inside.

**And from inside**, the next session's first command: `TEND_FENCED=1`
with `TEND_TREE` unset (the sandbox strips it, so a clone's suite
cannot be pointed at the wrong tree); `/usr/local/lib/tend/tools/sandbox.sh`
visible, owned by `nobody` (root, seen through the user namespace),
and `touch` refused; `tools/install.sh --check` green from a session's
seat — the comparison the `$HOME` prefix could not have offered.  The
copy in force is on the machine, outside every session's write access,
and a session can read that it is.

**Where the card stands.**  The `because` is answered in its second
half: the boundary a session cannot reach is now on the machine, not
only read-only inside a fence the tree configures.  The first half —
"protecting them and developing them are one directory pulling two
ways" — is answered in mechanism (the tree is the workbench, HEAD is
what installs) and not yet in practice: the tree's copies are still
ro-bound and `Edit`-denied, so a session still cannot edit a restraint
in place.  Taking those off is day two, and Henri's call, now that
`--check` has said the installed set is in force.

## 2026-08-27, day two — "take the tree binds off": what runs protects itself, a workbench is free

Henri: *"Lets do install day two, take the tree binds off."*

**The rule, one sentence.**  The set is bound read-only over the tree
only while the tree's copies are what runs.  `tools/sandbox.sh` knows
which copy it is (`$here` = `$root/tools`, or a prefix) and binds the
tree's set only from the tree; `tools/fence.sh` reads which side is in
force off the hook lines — every line carrying `TEND_TREE=` is the
installed side, and then the `Edit(./tools/…)` rules are not
load-bearing; a line without it is the tree side and everything is
required as before; both at once is mixed, and red.  `.claude/` stays
read-only and Edit-denied on either side: hook config is enforcement
wherever the hooks point.

**What changes for a session, once Henri has run `--free`.**  A
restraint in the tree is a file like any other — editable in place,
runnable in the suite, committed through the gate — and *nothing runs
it* until `git commit` and `sudo tools/install.sh`.  The clone-and-
outside-hand tax this card was opened on is gone for the tree; the
clone rule in `board/README.md` §"What the days taught" is corrected
below it rather than deleted.  The one thing a session still cannot do
is put a change in force, which is the boundary `card:self.md` drew
and `work-environment-ai` exists for.

**Built, on the branch `install-day2`** (the scripts were still ro-bound
when this was written — the last clone this should cost): the two
scripts above; `tools/install.sh --free` (the person's: refused inside
the fence, refused while any hook still runs the tree's copy, then lifts
exactly the set's Edit rules with a backup); `--check` notes what is
left to free and, from outside, ends by running the *installed*
sandbox's `--check` — the fence in force, where before
`tools/sandbox.sh --check` from the tree measured the tree's copy, a
gotcha found writing this; `hook-installer.sh` and `resolve.sh
--install` write the installed line when running installed.  Four
tests; the bwrap one is proposed, not declared, until the outside run.

Henri's lines, in order, from outside the fence:

    git merge install-day2
    sudo tools/install.sh
    tools/install.sh --free
    tools/install.sh --check

The last one ends with the installed fence's own `--check`, which
should say the tree's `tools/sandbox.sh` is writable and the prefix's
is not.  Then a new prompt, and the session's first act is to edit a
restraint in the tree in place and run its tests — the measurement that
day two is true in practice and not only in mechanism.


## 2026-08-27, 17:1x — day two measured in practice; recommendation: done

Henri ran the four lines ("merged, installed, freed — check output says
the fence is up").  From inside, the next session's first command:
`TEND_FENCED=1`; `tools/fence.sh` says *in force: the installed copies
at /usr/local/lib/tend — the tree's copies are the workbench*; the
tree's `tools/sandbox.sh` is **writable** and the prefix's refuses
`touch`.

**Then the first restraint edited without a clone.**  `tools/kaizen.sh`
— the lamp's baseline bug, open since 05:38 — fixed in place with
`--diff-filter=A`, a test added, committed through the gate (eea4c87),
in one command from a fenced seat.  And `tools/install.sh --check`
answered with the line this card exists for: *tools/kaizen.sh differs
from HEAD — the copy in force is not the vetted one.*  The change is
vetted and not in force; putting it in force is `sudo tools/install.sh`,
Henri's.  Both halves of the `because` are answered by execution: the
workbench and the enforcement are two directories now, and the copy in
force is on the machine outside every session's write access.

**Recommendation: done, on Henri's review** — with the move his, the
shape `fence` and `green` closed in.  What is left is not this card's:
the lander (fast-forwarding `main` after the gates, the other half of
the 0710 kaizen's card-shape) and, some day, an install on a machine
without sudo, which `TEND_PREFIX` and `--check`'s "weaker" line already
speak to.  `install.sh --check` is now the line to read first in any
session: drift between HEAD and the prefix is the one silent state
this arrangement can have.


## Done — 2026-08-27, 17:1x, on Henri's review

Henri: *"lets check that the install and cords are done, and then mark
them done if they are fully done."*  Checked: `sudo tools/install.sh`
put HEAD 4a6d353 in force; `tools/install.sh --check` from inside —
every file at HEAD, every hook on the prefix, *the tree's copies are
the workbench — no Edit rule denies them*, `in force: the installed
set, at HEAD`.  And the suite run from outside, `python3
tools/suite.py` in the venv: **346 passed, 0 skipped** — the bwrap
workbench test and `test_fence_hook.py`'s `TEND_TREE=` line, proposed
from inside, executed.  Moved to `done/` by the session, on his word.


## 2026-08-27, 17:3x — after done: each installed script is a command

Henri: *"Could we make neat symlinks into bin, eg. tend-keep
tend-reach-allow for each tend command during install?  Or something
else similar so that it's easy to call the installed versions?"*
Something similar: **wrappers, not symlinks** — the scripts find their
siblings by `dirname "$0"`, and through a symlink `$0` is the bin
directory.  `tools/install.sh` now writes `tend-<name>` for every file
in the set (`tend-fence`, `tend-keep`, `tend-reach-allow`, …) into the
bin beside the prefix's lib — `/usr/local/bin` here, `~/.local/bin` for
a user prefix — each a two-line `exec` of the installed copy that
supplies `TEND_TREE` from the tree you stand in when it is not set, so
`tend-fence` run in `~/tend` governs `~/tend`.  `--bin` lists them,
`--check` verifies each, `installed` records them.  One more
`sudo tools/install.sh` puts them on the machine.

