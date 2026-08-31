# trees — the other tree a session may read is a constant naming a directory on another machine

    status   open
    because  a session inside the fence sees one tree, its own; the
             `trees` row that was meant to show it the other one is a
             constant in tools/sandbox.sh — `trees="/home/cheery/gestate"`
             — which on this laptop names nothing, so the row binds
             nothing and nothing says so.  There is no way for the
             person to say "this session may read that directory" and
             no way for a session to ask: on 2026-08-30 the attempt
             was `TEND_REACH_ALLOW=net,tree` on the hook line by hand,
             a name the fence cannot read (F004).  Henri, 2026-08-30:
             "isn't there a way to allow you to access other trees?"
    asked    Henri, 2026-08-30, 05:3x — "open the card for reaching other
             trees, or directories."
    see      card:keep.md (the session half: what of the other tree is
             bound, and why not the rest), card:fence.md (the rows are
             the dial), card:self.md (the person's keys live in the
             protected set), F004, tools/sandbox.sh, tools/reach-allow.sh

## The problem

The fence was built where two trees stood side by side — tend and
gestate, in one home — and `card:keep.md`'s session half read off 310
fenced commands what of the other tree a session actually opened: its
documents and its tools, never its source, tests, builds or `.git`.
That measurement became `tree_parts`, and the path became a literal.
Both were right for that machine.  On this one the path is another
user's home, the `[ -e ]` guard on each bind skips it silently, and
`tools/sandbox.sh --rows` still prints the row as `on` with the
foreign path — a listing that says a reach exists which does not.

So the person has one dial for reach — `tools/reach-allow.sh`, the
rows a session may *ask* for — and it cannot say this: the rows it
knows are the network, the sound socket and the display, each a
socket or a namespace, none a place on disk.  What a session needs of
another tree is not something it asks for per command; it is a
standing read, set once by the person, of a directory they name.
That is a different kind of row: one the person points, and a session
neither asks for nor widens.

## Day one — proposed, not declared

The path leaves the script and goes where the other bound lives: on
the fence hook's line, set by the person's key.

- **`TEND_TREES=/home/henri/gestate:/home/henri/notes`** on the
  fence-hook line, colon-separated, and `sandbox.sh` reads it in place
  of the literal (the literal stays as the default where the variable
  is unset, so the other machine's fence does not change under it).
- **`tools/reach-allow.sh --trees PATH:PATH`** sets it — the same key,
  the same file, the same refusal shape as the rows: a path that does
  not exist, is not absolute, or is inside the tree or the home's
  secret places (`~/.ssh`, `~/.config`, the state directory the
  session already has) is refused before the file is touched.
  `--trees` alone lists what is bound and whether each path exists.
  `--rows` shows the row's real paths, not the literal.
- **Read-only, always.**  A place the person names is a thing to read;
  a session that needs to write there is a program with a grant
  (`card:keep.md`), not a wider fence.
- **What of it is bound is the open question**, and the tiebreak is
  his.  Two honest shapes: (a) a tree of the method's shape — one with
  `board/` and `.claude/settings.json` — gets `tree_parts`, the
  by-purpose subset keep.md measured, and a plain directory gets the
  whole of itself; (b) every path gets the whole of itself, and the
  person names `~/gestate/board` if that is what they mean.  (a)
  keeps keep.md's measurement in force for the case it measured; (b)
  is one rule and no guessing about what a directory is.  The card's
  first sitting picks one and says why.

Red first: `--rows` on this laptop says the `trees` row binds nothing
(today it says `on`); a `--trees` path that is not there is refused;
a bound path is readable inside and `touch` there is EROFS; `.git`
under a method-shaped tree is not inside under shape (a).

## Day one landed — 2026-08-31

At Henri's *"I'd like to get the gestate's tree available for you soon
again"* (2026-08-31, mid-benchmark; his reason: **"this tree is
gestate's child"**).  The want splits in two, and only one half is a
build: gestate is not on this laptop at all — bringing it here is his
hand — and the mechanism to point at it was the dead literal.  Built
so that the arrival costs him one line and no code change.

- **`TEND_TREES` on the fence hook's line**, colon-separated, read by
  `tools/sandbox.sh` in place of the literal.  Set is exactly what it
  says; **set empty is a bound of none**, so the person can bind
  nothing on purpose; **unset is `~/gestate`** — Henri, the same
  sitting: *"replace /home/cheery/gestate with ~/gestate so that it
  works on both machines.  I am henri on this machine and cheery on
  another."*  So the child tree finds its parent beside it in whatever
  home it is in, and when gestate lands at `~/gestate` there is no
  line to write at all: the row binds it because it is there.  The
  literal it replaced was one machine's absolute home — the `because`
  above — and `test_sandbox.py` is red if a home is ever hardcoded
  again.
- **`tools/reach-allow.sh --trees /a:/b`** points it; `--trees` alone
  lists each path, whether it is there, and which shape it got.  A
  path is refused *before the file is touched* when it is not
  absolute, not a directory, carries a character a path here may not,
  or names somewhere that would make the fence a door: the tree this
  governs, a directory holding it, the home itself, or `~/.ssh`,
  `~/.config`, `~/.local/state`, `~/.gnupg`, `~/.claude`.  The rows
  bound and the trees bound share the line and neither loses the
  other.
- **The shape is (a), and here is why.**  A tree of the method's shape
  — `board/` and `.claude/settings.json` — is bound by `tree_parts`,
  the by-purpose subset `card:keep.md` measured off 310 fenced
  commands; any other directory is bound whole, there being no
  measurement to subset it by.  (b) would bind the other tree's
  `.git` and source, and `sandbox.sh --check` has asserted since the
  fence was built that neither is inside: a shape that turns standing
  gates red is not one to pick silently.  The tiebreak is still his,
  and (b) is one edit if he wants it.
- **The row stops lying.**  `--rows` prints each named path as
  `(parts)`, `(whole)` or `(not there)`, and `--check` says *"the
  trees row binds nothing"* instead of probing a bind that never
  happened — the card's own `because`, closed.

Measured here: the listing half, in the suite
(`test_sandbox.py`, `test_reach_allow.py`, both red before the
change).  **Not measured here**: the bind itself — a session cannot
nest bubblewrap, so `touch` being EROFS inside a bound gestate is
`sandbox.sh --check` on Henri's side, after his `sudo tend-install`,
on the day gestate is on this disk.  Until then this is a mechanism
that has never run, and says so.

**And then it ran — the same day, 13:50.**  While the kaizen was
being written Henri put gestate at `~/gestate`, pointed the line
(`TEND_TREES=/home/henri/gestate` on the fence hook, though the new
default would have bound it unasked) and ran `sudo tend-install`.
The paragraph above stood for two hours.  Measured from *inside* the
fence, which is where it counts:

    $ head -3 ~/gestate/board/README.md
    # board/ — the live board, and how to work it
    $ touch ~/gestate/tools/.probe
    touch: cannot touch '…': Read-only file system
    $ test -e ~/gestate/.git      →  not inside
    $ ls ~/gestate                →  CLAUDE.md README.md board doc fixme.md
                                     journal journal.md keeper.md manifesto.md
                                     roadmap.md spec tools vision.md

That listing is `tree_parts` exactly — its documents and its tools,
and none of its source, tests, builds or `.git`.  Shape (a) is not a
proposal any more: it is what a session sees.  `sandbox.sh --rows`
now reads `/home/henri/gestate(parts)` where this morning it read a
foreign path this machine has never had, and `install.sh --check`
says *in force, at HEAD*.

What is left of this card is a decision, not a build: whether the
`because` still stands.  It does not — the row binds, it says what it
binds, and the person has a way to point it.  Closing it is Henri's,
and it is proposed for `done/` at his review.

## What it must not become

A second write path.  The reach rows are a session asking and the
person's bound refusing; this is the person pointing, once.  If a
session can put a path here — through the settings file, through a
row it asks for, through a symlink inside its own tree that resolves
outside — the fence has a door in it that `card:self.md` closed.
`test/test_sandbox.py` already holds that the other tree's `.git`
and source are not inside; it holds the same for whatever this binds.
