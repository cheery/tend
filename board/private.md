# private — a mind's thinking is on display, and it has no place of its own to write

    status   open
    because  the talk screen shows the model's thinking as the turn runs
             (tools/deliver.sh streams the reasoning; tools/panel.py
             `talk --think` prints it), so the mind's working is on
             display beside its answer — a half-thought reads as a
             claim, and a mind whose scratch is watched writes for the
             watcher.  And a session, or a mind at the door, has no
             private place at all: everything it writes is the record,
             the tree, or a proposal, each public by construction, so a
             working note has no home — it goes into the record as
             noise or is lost, which is card:kaizen-ingestion.md's
             problem at the scale of one sitting.  (A hosted session
             has such a place already — the harness keeps a memory
             directory per working tree, outside the tree, unseen by
             it; nothing tend runs has one.)  Henri, 2026-08-30: "the
             thinking box should not show the user anything else except
             that the session is thinking, not the thinking text
             itself.  Likewise, the session should have a private space
             where it can write memories, and that should associate
             with the directory where it works in.  Those recordings
             should be readable, but it should be out of sight by
             default.  private is private!"
    asked    Henri, 2026-08-30, ~10:50 — "also make a card:private.md …
             Do not commit that yet though."
    see      tools/deliver.sh (the reasoning stream), tools/panel.py
             (`talk`, `--think`, the thinking shown as the turn runs),
             card:hold.md §"Talk" (the conversation this happens in),
             card:tools.md (the `C:` line — an *act* is always shown;
             this card is about words and notes, never acts),
             card:kaizen-ingestion.md (a lesson nothing reads back),
             card:trees.md (a session's reach is a directory — the
             private place is keyed by the same directory),
             tools/sandbox.sh (what a session may write outside the
             tree), spec/os.md property 3

## The rule, in his words

**Private is private.**  Two things follow, and one line that does
not move:

- **Thinking is shown as a state, not as text.**  The talk screen
  says *thinking…* while the mind thinks, and nothing else; the
  thinking text is kept — it is part of the record's truth — and
  read on ask (`--think`, a key in the panel), never by default.
- **A mind has a private place, keyed by the tree it works in.**  A
  session in `~/tend`, a node of `~/tend`, a mind at a door talking
  about `~/tend` — each may write notes there that nothing shows.
  Readable by the person on ask; out of sight otherwise; never in the
  record, never in the tree, never in a proposal unless the mind puts
  it there itself.
- **Acts are never private.**  A tool call, a pull, a write, a ring on
  the andon: the `C:` line and the record show every one, as
  `card:tools.md` says.  Privacy is for words and notes; a reach the
  person cannot see is still a turn that did not happen on this
  tree's terms.  The line between the two is the whole card.

## Two rooms, not one — the scratchpad

Henri, 2026-08-30 afternoon, watching the tools sitting work out of the
harness's scratch directory (patch scripts, commit messages, two copies
of the README, the kaizen's draft): *"That reminds me that a session
also needs a scratchpad that is also private to it."*  It is a second
room, and it differs from the private place above in both its
lifetime and its reader:

- **The scratchpad** is working space.  It is the session's own for
  the session's length and then it is gone; nothing reads it, not the
  person, not the record, not the next session.  The harness gives a
  hosted session one (a directory per session, outside the tree);
  nothing tend runs has one — the executor's grant is `--write
  /dev/null`, and a node's state directory is the runner's, not the
  mind's.
- **The private place** is notes.  Keyed by the tree, outliving the
  session, readable by the person on ask.

A mind's grant names both: `write $SCRATCH` — a directory made for the
turn or the sitting and removed after it, the way the fence gives a
session an empty `/tmp` — beside the private place, and neither is
the record.  Day one below is the private place; the scratchpad is
the smaller build and may come first, since a grant word and a
`mktemp -d` are all it is.  What must not blur: a scratchpad is not
where a note goes to survive (it will not), and the private place is
not where a working file goes to be forgotten (it will be read on
ask).

## Day one — proposed, not declared

- **The thinking box**: `tools/panel.py talk` shows *thinking… (N s)*
  and the answer; the thinking text goes to the exchange's record as
  it does now, and `--think` (or a key on the talk screen) shows it.
  `tools/deliver.sh` is unchanged: it streams what the wire gives; the
  panel decides what to show.  Red first: a talk without `--think`
  prints no line of the reasoning.
- **The private place**: `~/.local/state/tend/private/<tree-key>/`,
  the key the tree's absolute path made a name (as the harness keys
  its memory directory by the working directory), one file per note,
  written by whoever works in that tree — a session through a reach
  row that opens this directory and no other (`tools/sandbox.sh`),
  a node under a grant word, a door mind through the executor's one
  write (day two of `card:tools.md`, the same gate).  The panel does
  not list it; `tools/panel.py private [TREE]` prints it on ask.
  Red first: a fresh tree has an empty private place and the panel
  shows nothing of it; a note written there appears nowhere else.
- **What is written there is the mind's**: no shape is imposed on a
  note beyond a filename; the tree's memory rules (`MEMORY.md`,
  frontmatter) are the harness's and are not carried here unless a
  mind wants them.

## What would make this card wrong

If the thinking shown is what the person reads the mind *by* — if
Henri, given the state and not the text, asks for the text on most
turns.  Then the default was the wrong way round and the card's first
half closes on that count.  And if nothing tend runs ever writes a
private note — if the place stays empty for a week of sittings — the
second half is a room nobody entered, and closes.

## What it must not become

A hiding place for acts.  Nothing that reaches — a call, a write
outside the private place, the network — is ever private; the record
shows it and the fence bounds it, this card notwithstanding.  Not a
second memory system for the harness's session: the harness has one;
this is for what tend runs.  And not secret from the person: readable
on ask, always — *out of sight* is a default, not a lock.

## Where it sits

Written 2026-08-30 at Henri's "also make a card:private.md", uncommitted
at his "Do not commit that yet though"; a new card arrives unplaced
and the tiebreak is his.

## 2026-09-06 — day one's first bullet landed: the thinking is a state

At Henri's "let's land hy3's change. that private.md's day one", after
twelve led turns on this card the same hour (`card:session-program.md`
§"2026-09-06, 13:18–13:26"): hy3 proposed this change six of six, two
turns naming the lines, once as a card; gemma4 made no call and
proposed a spec that puts the private place in the tree.  Landed by a
session's hand from those drafts, brick 3's route, the second time in
a day.

**What is built.**  `tools/panel.py talk` from a shell prints the
answer, and on stderr either the reasoning text — only when `--think`
was given — or one line, `(thinking — kept in the record; talk --think
shows it)`, when the model thought unasked (the environment's
`TEND_THINK`).  The talk screen's two `(thinking)` blocks — past
exchanges and the turn in flight — render the text only while `[k]`
is on; off, a past exchange that had thinking shows `(thinking — [k]
shows it)` and the turn in flight shows what it already showed, `… is
thinking (N s)`.  `tools/deliver.sh` is unchanged and the record keeps
the T line whole, as the rule says.  Red first: the CLI test ran with
the model thinking by the environment and no `--think`, and read the
text on stderr before the guard; one mutate row.  The screen's two
guards are held by a source assertion, not a render — the curses loop
is not driven by any test in the file, which is the file's standing
limit and not this bullet's.

**What is not built**: the private place and the scratchpad, day one's
second and third bullets — untouched, and the card stays open on them.
