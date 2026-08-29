# canvas — a pulled node's death is a line in a file nobody is looking at

    status   open
    because  on 2026-08-28 at 13:27 Henri pulled the llm node and the
             runner died a second later at the loader (libsvml.so, the
             shell had no oneAPI on its path); `pull` had said "started
             llm", `stopped` said `exited 127`, the log said why, and the
             only thing he saw was `lead.sh llm --kept` reporting "not
             up".  The fact of the death existed in the node's state
             directory and nowhere else — no place on the person's side
             shows what the person is holding: which nodes are pulled,
             whether each is running, what it last said as it stopped,
             whether its watcher still beats — and the andon record, the
             one thing that does reach the person, is a separate file
             the panel reads alone.  A death and a cord pull are events
             on the same timeline and the person sees them in two places
             or in none.  The fix that landed the same afternoon (pull
             watches for a second, `card:session-program.md` §13:45) is
             a timing window Henri named as one "we will eventually
             revert" — it catches the failure that happened and no
             slower one, and costs every healthy pull a second
    asked    Henri, 2026-08-28 — "I think that we want a canvas where
             user 'pins' the programs+state they pull.  That could be a
             directory with name.pin -files.  Along the canvas there
             would be an andon/log where errors are shown to the user
             along andon calls."  Then: "I think there could be many
             canvases the user can define, it'd be neat for say, a
             server to have one such canvas directory.  open the canvas
             card"
    see      card:andon-panel.md (done/) — the person-side watcher this
             grows: a TUI outside the fence over the andon record; closed
             2026-08-28 with "the later views are widenings awaiting a
             want", and this is the want, the same day
             card:session-program.md §13:15 — the heartbeat: `status`,
             `check` and `serve` read a held lock and a stale
             `$STATE/watch` as "the cords are cut"; §13:45 — the
             one-second watch in `pull`, and Henri's prediction
             card:node-install.md (done/) — the 07:10 face: the runner's
             loader path is the pulling shell's, which is what died at
             13:27
             card:resolver.md (done/) — the person-side loop that visits
             every node it knows; a canvas is the person saying which
             ones are *held*, and where
             tools/launch.sh — the state a runner leaves: `run.lock`,
             `stopped` (mtime the last stop, its line the reason), `log`,
             `watch`, `run.pid`; tools/andon-panel.py — `read_state`, the
             tone on a new ring
             ~/.local/state/tend — where the andon record lives on the
             person's side and passes through the fence; a canvas
             directory is the same kind of place

## What it is

A **pin** is the person's declaration "I am holding this": a file
`<name>.pin` in a canvas directory, the filename the id the way a card's
is, the content a line or two — the node directory, and the state
directory if it is not the node's default.  Pins are the person's act,
on the person's side, in a place the fence lets through untouched.

A **canvas** is a directory of pins, and there can be many: one for
this desk, one for a server, one for a batch of nodes that belong
together — the person defines them, and which canvas a program looks at
is a path.  A canvas is *not* the resolver's list of every node the tree
knows; it is the person's list of what they are holding right now, and
the same node may be pinned on one canvas and not another.

The **view** over a canvas is the panel grown: one row per pin —
running or not (`run.lock`), the last pull, the last stop and its reason
(`stopped`), the heartbeat read (`watch`: *runner up, watcher silent N
min — the cords are cut*), proposals waiting in `proposals/lead/` — and
beside the rows the **andon/log**: one timeline where a ring, an ask, an
answer and a runner's non-zero stop are the same kind of line, shown as
they happen.  This is the reach-free route for a death the way the panel
is for a ring: the runner writes the record, the view outside the fence
reads it, and the person sees it whenever it happened, not only if
`pull` was still watching.

## What would make this card wrong

If a node's death always reaches the person some other way — if `pull`'s
watch is enough and Henri's prediction is wrong — then the log column is
redundant and the canvas is a status page.  Or if one machine only ever
holds one set of nodes, so "many canvases" is a directory with one file
in it.  The 13:27 minute is evidence against the first; the second is
his own ask (a server's canvas), and the day it is measured is the day a
second canvas exists.

## What it must not become

A second andon (the panel's own rule): the canvas shows, it does not
ring.  A way for a session to pin — a pin is the person's; a session
inside the fence can pull and can read a canvas and cannot hold one.
A server, a GUI, an auto-pin from `pull`, or the resolver reading pins
as its list — each is a widening awaiting a want, and the resolver one
is a decision (`card:resolver.md`'s per-node loop is the tree's, not the
person's).  And not the whole view built before one row is red first.

## Day one

The canvas directory and the panel reading it: `~/.local/state/tend/
canvas/` as the default canvas (a path to name another), `llm.pin` in
it by Henri's hand, and `tools/andon-panel.py` showing one row per pin
from `run.lock` / `stopped` / `watch`, with a non-zero stop appearing in
the log column beside the andon lines.  Red first with a fixture pin
naming a node whose `stopped` says `exited 127` and whose log's last line
is the loader's.  When that row is on the screen, the one-second watch
in `pull` (§13:45) has its replacement and can be reverted, which is
this card's first measurement.

## Where it sits

Placed last in the priority by the session that wrote it, 2026-08-28,
at Henri's "open the canvas card"; a new card arrives unplaced and the
tiebreak is his.  It is the andon strand's next build after
`andon-panel` closed, and the thing `session-program`'s §13:45 watch
waits on to be reverted.

## 2026-08-28, 17:30 — day one built: the canvas read, one row per pin, the death in the log column

Built in the sitting after the card was opened, red first with the 13:27
minute as the fixture: a pin naming a node whose `stopped` says `exited
127: llm stopped by itself` and whose log's last real line is the
loader's (`libsvml.so: cannot open shared object file`).

**What is there.**  `tools/andon-panel.py [--canvas DIR]` — the panel
grown, not a second tool.  A canvas is a directory of `<name>.pin`
files (`--canvas DIR`, `TEND_CANVAS`, else `~/.local/state/tend/canvas`),
a pin a line or two: `node PATH`, and `state PATH` only when the state
is not `NODE/state`.  `read_canvas` gives one row per pin from what the
runner leaves and nothing else: `run.lock` taken for an instant the way
`flock -n` takes it (never created — a node that never ran has no lock);
`stopped`'s mtime the last stop and its line the reason, an `exited N`
with N ≠ 0 read as a death and not a close; `watch` under a held lock
older than `TEND_WATCH_STALE` read as *runner up, watcher silent N min
— the cords are cut*, the rule `launch.sh status` reads, now read from
outside; the pull file's last stamp.  `read_log` is the timeline: every
line of `andon.log` and every pinned death — the stop's reason and what
the program last said, filtered as `launch.sh`'s `last_said` filters —
sorted by time.  A clean stop (idle, the sitting, exit 0) is the row's
last stop and no line in the log: the column is for what went wrong.
The TUI shows the canvas block above the pending questions and the log
below, newest at the bottom, a death or a cut in bold; with no terminal
it prints the rows and the last five lines.  Seven tests.

**Measured against the real node** from inside the fence through a
scratch pin: `llm — not running — pulled 13:57 — stopped 13:59 — idle:
nothing has pulled llm for 60s`, and beneath it the afternoon's three
cord pulls and Henri's answer, one column.  The 13:27 death itself is
gone from the row — `stopped` has been rewritten by every stop since —
which is the day-one shape the card set: the row shows the *last* stop,
and the timeline shows a death only while it is the last thing the
runner wrote.  A death that a later clean run overwrote is a line in
the runner's log only; whether the timeline should keep it is the next
question, and it is a want, not a build yet.

**What it does not do**, by the card's rule: it does not ring for a
death (the row and the line are shown; the tone is the andon's), it does
not pin (`~/.local/state/tend/canvas/` does not exist on this machine —
`llm.pin` is Henri's hand, `printf 'node ~/tend/llm\n' >
~/.local/state/tend/canvas/llm.pin`), and it does not count proposals
waiting in `proposals/lead/`, which the card's view named and day one
did not need.  The one-second watch in `pull` (`card:session-program.md`
§13:45) stays until the row has been on his screen: the revert is the
card's first measurement, and the measurement is his.

## 2026-08-28, 17:55 — Henri saw it: "interesting but I am a bit mystified by it"

He made the pin and opened the panel.  His words: *"I tried the canvas,
it was interesting but I am a bit mystified by it.  Though, it'll
probably makes more sense later."*  Recorded as a measurement, not
argued with: the row he saw was the idle stop from 13:59 and beneath
it three answered cord pulls — a quiet afternoon, nothing dead, and a
view whose reason is a death that had already been overwritten.  The
canvas makes sense at the minute it was carded for and shows little on
a good one; whether that is the view's fault (say what a pin *is* on
the screen; keep a death past the next clean stop) or only the hour's
is a question for the next 13:27, and the card keeps it.

## 2026-08-28, 18:45 — the next build, named by a model that never saw the tree

`proposals/compare/2026-08-28-1835-claude-opus-5.md`: given this card's
`because` and then the card as material, Opus 5 drafted the death
notice as a line the runner appends to the andon record on the person's
side — *"so the death and a cord pull land on one timeline"* — appended
by the stop path that already writes `stopped`, by nobody else, never
for a zero exit, and it named `pull`'s one-second watch as "the thing
this replaces".  That is a write-time record where day one built a
read-time merge (`read_log` joins the stop into the timeline when the
panel looks, and loses it at the next clean stop — §17:30's open
question), and it is the card's own "reach-free route for a death the
way the panel is for a ring", stated more exactly than §"What it is"
states it.  Sonnet 5's `died` file (`…-claude-sonnet-5.md`) is the
same fact kept in the state directory instead.  **Neither is landed**:
the model proposes, the person lands (`card:session-program.md`, brick
3), and the draft is his to read.  A session's reading: Opus's line is
day two, it answers §17:30's question (a death survives the next clean
stop because the record keeps it), and it is the revert of §13:45's
watch with a replacement rather than a hope.

## 2026-08-29, 07:50 — the draft read against the tree: it lands as day two, with the record's line shape corrected

Read by a session at the 2026-08-28-1830 kaizen's item 1, each claim
of `proposals/compare/2026-08-28-1835-claude-opus-5.md` checked
against the file it names, from inside the fence.  **It lands.**  Four
things it got right from the `because` alone, two it could not have
known, and the shape of the commit — his word lands it; a session
builds it.

**Right, by the tree's own lines.**  The record is where the draft
said: `tools/andon.sh:71`, `$state/andon.log` under
`~/.local/state/tend`, and the fence binds that directory writable
(`tools/andon-panel.py:9`), so the runner's shell can append from
either seat — the launcher's stop path runs *outside* keep (keep
wraps only the program, `tools/launch.sh:265`), and it is the one
place: `:305–306`, where `stopped` is written.  A zero exit writes
nothing is exactly the launcher's own rule — its stops for idle and
the sitting set `rc=0` (`:300`), so they are closes; the loader's 127
and the leash's 124 are deaths.  And "`pull` does not write it (its
one-second watch is the thing this replaces)" is `died_at_once`
(`:138–147`, called at `:316` and `:354`): the revert is the function
and its two calls.

**Two corrections.**  (1) The draft's line is the record's *text*, not
its line: `andon.sh:101` writes `<epoch> <YYYY-MM-DD HH:MM> <text>`,
and `read_log` (`andon-panel.py:234`) drops any line whose first word
is not digits — so the notice is `<epoch> <stamp> <name>: exited <rc>
— <reason>`, and the draft's `at <HH:MM>` goes, the stamp carries it
(`event_line` prints the time).  `TEND_ANDON_STATE` must be honoured
as `andon.sh` honours it, or no test can point the record at a
fixture.  (2) Once the record keeps a death, day one's read-time merge
(`read_log` joining a pin's `stopped` into the timeline) would show
the same death twice while it is still the last stop — the landing
removes the merge, and `test_a_death_is_a_line_in_the_log_column`
becomes a test of the record's line.  Smaller: the reason is the
runner's *last* line (`last_said`, `:134`), not its first; and the
panel labels record lines `andon` in the who-column, so a death is
read as the pin's by its `<name>:` prefix or not at all — one `if`,
a want, not owed.

**The commit, as the kaizen named it, filled in.**  Red first, in
`test/test_launch.py`: a grant whose program exits 127 leaves one line
in a fixture record, and one whose program exits 0 or is stopped for
idle leaves none.  Then `launch.sh`'s stop path appends the line;
`died_at_once` and its two calls go; the panel's pin merge goes and
its test reads the record; this card's day-two section.  `launch.sh`
is in the protected set and the tree's copy is the workbench
(`fence.sh`: the installed copies are in force), so the edit is a
session's through the gate and nothing runs it until his `sudo
tools/install.sh` — which is the same commit's `lander` line.  Sonnet
5's `died` file is the same fact in the state directory and not on the
timeline; it is not taken.

**Not landed here**: the model proposes, the person lands
(`card:session-program.md`, brick 3), and §18:45 said the draft is his
to read.  His word — "land it" — and the commit above is one sitting's
work.

## 2026-08-29, 08:20 — day two built: the runner writes its death into the record, and the watch is reverted

Henri: *"I saw that I had something to review, but I didn't do it
yesterday.  Hmm.. lets 'land it'"*.  Landed as §07:50 spelled it, red
first.

**What is there.**  `tools/launch.sh`'s stop path — the one place
`stopped` is written — appends one line to the andon record when the
exit is non-zero: `<epoch> <YYYY-MM-DD HH:MM> <name>: exited <rc> —
<what it last said>`, the record's own shape (`andon.sh`'s `note`),
in `${TEND_ANDON_STATE:-~/.local/state/tend}/andon.log`, the file the
panel reads.  The runner appends and nobody else; a zero exit and the
launcher's own stops (idle, the sitting: `rc=0`) write nothing; a
record that cannot be written never fails the stop.  `died_at_once`
and its two calls (`pull`, `serve`) are gone — the §13:45 watch
reverted, with its replacement in the same commit.  `andon-panel.py`'s
`read_log` reads the death off the record like any other line and
takes the who-column from the `<name>:` prefix when the name is a pin's,
so a death is bold the way a cut is; day one's view-time merge of the
pin's `stopped` is removed — with the record keeping the death it would
have shown the same death twice while it was still the last stop.

**Red first.**  `test_launch.py`: a grant whose program dies at the
loader with 127 — `pull` returns 0 saying "started" and the record has
exactly one line, the name, the code, and `libx.so` in the reason (red
today: `pull` exited 1 through the watch); a clean run and an idle stop
leave no record at all.  `test_andon_panel.py`: the death on the
timeline once, from the record, as `llm` between two andon lines; and
§17:30's open question as a test — **a death survives the next clean
stop**: the row says `idle:` and the timeline still has 13:27.  The
one panel test that had an empty record and expected the merge now
writes the line the runner would have (a fixture builds the side it
means).  Every test in the fixture points the record at scratch
(`TEND_ANDON_STATE`), never at the person's.

**What it does not do.**  It does not ring (the panel's rule) and it
does not pin.  The reason is the program's last real line, one line,
not truncated to a row's width — the panel's column wraps or cuts it,
not the record.  Sonnet 5's `died` file is not taken.  And nothing
runs it until his `sudo tools/install.sh`: `launch.sh` is in the
installed set, the tree's copy is the workbench, and the lander lamp
says the installed set is behind HEAD until then.  **The card's first
measurement is his**: the next 13:27, on the panel, without `pull`
having watched.
