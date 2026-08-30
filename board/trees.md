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

## What it must not become

A second write path.  The reach rows are a session asking and the
person's bound refusing; this is the person pointing, once.  If a
session can put a path here — through the settings file, through a
row it asks for, through a symlink inside its own tree that resolves
outside — the fence has a door in it that `card:self.md` closed.
`test/test_sandbox.py` already holds that the other tree's `.git`
and source are not inside; it holds the same for whatever this binds.
