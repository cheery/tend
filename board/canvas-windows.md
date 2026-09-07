# canvas-windows — a window is a thing held, and nothing on the person's side records it

    status   open
    because  the canvas records what the person holds only when it is a
             node: a pin is "show me", a hold is a standing pull, and
             both are files that outlive the process and can be read by
             the panel, the tick, a session with the reach row, a mind
             at the door.  Everything else on the desk — the windows —
             is state in the compositor's memory (this laptop: Wayland
             under GNOME): a window's place, what it shows, when it
             last changed, are nowhere a reader can read, a crash of
             the shell loses the layout, and a session that could say
             "you have lander.md open and a terminal on llm's log" has
             no file to say it from.  Henri, 2026-08-30: "letting you
             write a window manager that works as a 'canvas', where
             windows themselves record their state."
    done     when a window of a tend-compatible program is on his
             screen because a file for it is in the canvas — one file,
             one window, written by his command — comes back where it
             was after a shutdown and a log-in, carries a move or an
             edit into its file, and goes from the canvas when he
             closes it from its X as it does at `rm`; and a legacy
             GNOME window is on neither the canvas nor the panel, so
             `ls canvas/` shows nothing he did not put there.
             (a session's draft, 2026-09-07, from spec/canvas.md's
             seven arrows and his sixth sentence; henri: signed 2026-09-07)
    asked    Henri, 2026-08-30, ~10:40 — "put these into later/ as cards"
    waited   (shelved 2026-08-30 to 2026-09-06) on two things, in order.  A measurement: a daemon
             that mirrors the window list into `canvas/*.win` (the
             record without the manager) and a reader — the panel, or
             a session — shown to do something different for having
             read it; if no reader changes, the manager is a status
             page.  And Henri's decision on size: on Wayland a "window
             manager" is a compositor (wlroots/smithay, weeks, replaces
             GNOME); the record is a daemon over GNOME's shell interface
             or foreign-toplevel, days.  The record first.
    see      card:canvas.md (the pin, the death in the log column, and
             §"What it must not become"), card:hold.md (presence is the
             claim, mtime is the person saying so again; the state a
             program cannot write), card:hold-mirror.md (where a
             window's state is written — a window has no state
             directory of its own), card:cords-crate.md (a tend app
             writing its own richer row beside the shallow one),
             card:tools.md (a mind at the door reading the desk is a
             `read` over the canvas), spec/os.md property 1,
             tools/panel.py

*(question, his call — the `done` line above: sign it as it stands,
change it, or refuse it?  One thing it decides that the card has not:
today's mirror of every window and `.gone` are not in it — a `.win`
the shell wrote and nobody's command did is what the last clause
rules out — so signing it is the retirement `spec/canvas.md` left to
a card's decision, and the build that follows is the write half, not
the mirror's day two.
henri: signed 2026-09-07)*

## What it is, when it comes

The hold card's rule one shelf over: **a window's state is a file on
the person's side.**  `<label>.win` in the canvas directory — app id,
title, geometry, focused or not, the pin or hold it shows if any, the
time of its last change — written by whoever manages the window,
outliving the window, read by the same readers that read a pin.  The
canvas then lists everything the person is holding in one place, and
"what am I holding?" has one answer for a node and for a window.

**Who writes** is the pin/hold answer again: the manager (or the
daemon) writes the shallow row for *every* window — it can see
geometry and title and nothing more — and a tend app writes its own
richer state beside it, in the same directory, in its own name.  The
two never write each other's file.  The shallow row is what makes a
foreign program's window a thing held; the app's row is what makes it
worth reading.

**Where it runs**: the person's side, unfenced, with the person's
reach — the panel's seat, and the panel's rule: a session's reach
into the canvas stays read-only plus the pull file, and nothing the
manager does is ever reachable from inside the fence except as a file
to read.

## Day one, when it is worked — proposed, not declared

The record without the manager.  A daemon on the person's side that
mirrors the compositor's window list into `canvas/*.win`, one file per
window, removed when the window closes (or left behind and marked, as
the hold card treats a death: the file outlives the process and says
so).  The panel shows the rows beside the pins.  Red first: a `.win`
with no window behind it reads as *gone* on the panel, not as a
window.  Then the measurement in `blocked`.

## What it must not become

A second panel, or a desktop.  The canvas is a directory of files
and the panel is one reader of it; a manager that only its own panel
can read has moved the state back into a process.  And not a reach:
the manager sees the desk; the session sees the files.

## Where it sits

Shelved on arrival, 2026-08-30, at Henri's "put these into later/ as
cards".  It is `canvas`'s day N, not a new line of work; when it
wakes, it wakes below `canvas` and the tiebreak is his.

*2026-09-02, still shelved — one line added to what it carries, in
Henri's words at `card:edge.md`'s panel rows: "vasta graafisessa
ympäristössä se voi näyttää sugiyama-graafin" — the pull graph drawn
as a graph, layered, is this card's; the terminal panel shows the
edges as rows.  His words on the canvas as the windowing system's
screen, the same day (`card:edge.md`), are also here to read when it
wakes.  Not the event it waits on: he did not say so.*

## Woken 2026-09-06 — "start the work on windowing system", and the first wrinkle measured

Henri, with 52 minutes on the clock after eleven commits: *"I wonder
whether it'd be time to start the work on windowing system?  So that
we put this finally into practise and start steamrolling the wrinkles
straight?"*  The card waited on his word and on a decision on size,
with the record first; his word is above, and the size question was
put to the laptop before it was put to him.  From his shell, the
same minute:

    $ gnome-shell --version
    GNOME Shell 50.1
    $ gdbus call --session --dest org.gnome.Shell --object-path /org/gnome/Shell/Introspect --method org.gnome.Shell.Introspect.GetWindows
    Error: GDBus.Error:org.freedesktop.DBus.Error.AccessDenied: GetWindows is not allowed

**What that decides.**  The shell's own Introspect interface exists
and is closed to a caller that is not on its allow-list, which is how
GNOME has shipped it for some releases; so the "daemon over GNOME's
shell interface" of the `blocked` line is not a plain daemon on this
laptop.  The window list is readable from *inside* the shell — an
extension runs there and sees every window (title, app id, focus,
geometry, when it changed) — and nowhere else short of replacing the
shell.  So day one's shape, sized by the measurement and not by
taste: **a thin shell extension that publishes the window list on its
own D-Bus name and signals a change, and `tools/windows.py` on the
person's side that mirrors it into `canvas/*.win`**, one file per
window, marked gone when the window goes.  Two pieces and not one on
purpose: the extension stays a few lines inside a process whose
crash is the desk's, and the mirror is the tree's own program, in
Python, tested against a stub of the interface the way the door's
tests stand in for llama-server.  Days, as the card said the record
would be; the compositor stays weeks and stays not first.

**What is not decided, and is his**: whether an extension inside
GNOME's shell is a size he accepts — it is code running in the
compositor's process with the compositor's reach, installed by his
hand, and nothing in the tree can fence it.  The alternative is the
compositor of his own, and the measurement says there is no third
route on GNOME 50.

*(question, his call — day one as a thin shell extension publishing
the window list over D-Bus, with the mirror in the tree; or wait for
the compositor?
henri: code inside compositor's process is ok.. 2026-09-06)*

**Day one, when it is built** (next sitting, not this one — 45
minutes and a kaizen owed is the README's "one more small thing"):
the extension, `~/.local/share/gnome-shell/extensions/tend-windows@…`,
one method returning the list and one signal; `tools/windows.py`,
`--once` to mirror the list now and the loop form on the signal;
`canvas/<key>.win` in the hold card's shape — presence is the claim,
the file says title, app, focus, and when; the panel shows `.win`
rows beside the pins, and a `.win` with no window behind it reads
*gone*.  Red first, on the stub: a window that closed leaves a file
that says so.  Then the measurement the `blocked` line named: a
reader shown to do something different for having read the files.

Placed last on the board, at 14, below `meter`; the tiebreak is his.

## Day one landed — 2026-09-06, the 15:59 sitting, at Henri's "shall we start?"

Three commits, the shape the wake set and nothing past it.

**The extension** — `tools/tend-windows@tend/`, two files, installed
by his hand under `~/.local/share/gnome-shell/extensions/`.  It owns
`org.tend.Windows` on the session bus at `/org/tend/Windows`: `List()`
returns the windows as JSON (id, stable sequence, app id or class,
title, focus, frame, and `at` — the epoch second of the window's last
change the extension saw, since the compositor keeps no wall clock
for that), and `Changed` fires on a window created, retitled, moved,
resized, focused or unmanaged.  Windows the shell hides from the
taskbar and windows that are not `NORMAL` are left out.  It reads the
desk and changes nothing on it, and nothing inside the fence can
reach it — a session sees files.

**The mirror** — `tools/windows.py`: `--once` asks the list over
`gdbus` (on every GNOME desk; python's `gi` is not on this one) and
writes `canvas/<app>-<seq>.win`, one file per window, in the hold
card's shape — `app`, `title`, `focus`, `frame`, `at` — under a first
line that names the writer.  Presence is the claim, and **the file
outlives the window**: a window not in the list gets a `gone EPOCH`
line and is kept, the first `gone` is the moment it went and a later
pass does not move it.  The mirror touches only files whose first
line is its own, so an app's richer row beside it, in its own name,
is never written from here — the two never write each other's file,
and the panel reads both.  `--watch` mirrors now and again on every
`Changed`, a burst coalesced into one pass, and exits 1 saying so
when the monitor ends (the shell went away, or the extension was
disabled).  A shell that does not answer is not a desk with no
windows: nothing is marked gone, the line says which name did not
answer and which extension is not enabled, exit 1.  `--install`
copies the two files and prints what his hand does next; `--check`
gives three verdicts — installed ✓/✗, and from a seat with no session
bus a `·` line for enabled and answering, which it cannot see.

**The panel** — `tools/panel.py` shows a `windows — N open, M gone`
section under the tick line, one row per `.win`: key, `focused` /
`open` / `GONE`, the title, when it last changed, when it went.  A
gone row is bold, like every row that is not what it claims.  Red
first: a `.win` with no window behind it reads GONE and never as a
window, the card's own sentence.

**Measured from this seat.**  The test's shell is a stub of `gdbus`
that prints what `gdbus` prints — GVariant's text form, a Python
literal for strings — the way the door's tests stand in for
llama-server: the first run was red with no tool, the closed window's
file was red before the `gone` line existed, nine tests and two on
the panel are green, six mutate rows are red (a closed window never
marked gone; another hand's file marked gone; the first `gone` moved
by every pass; a silent shell read as an empty desk; GONE shown as
open; the no-terminal panel listing no windows).  The extension
parses as the module GNOME 45+ loads (`node --check`) and names the
interface the mirror calls, which is what a test can hold of code
that runs inside the shell.  **What has not run**: the extension,
in a shell — the fence has no session bus, and the third verdict is
the honest one.

**His hand, next** — from his shell:

    tools/windows.py --install
    (log out and in — on Wayland the shell loads an extension at login)
    gnome-extensions enable tend-windows@tend
    tools/windows.py --check
    tools/windows.py --once && tools/panel.py --canvas ~/.local/state/tend/canvas

**Run by his hand, 16:29 the same day.**  After the install, a
log-out and in, and the enable, his shell's panel showed

    windows — 1 open, 0 gone
      org.gnome.Ptyxis-2            focused  henri@carbon: ~/tend  changed 16:29

His words: *"it seems to be working."*  So: the extension loads in
GNOME Shell 50.1, `org.tend.Windows` answers, the mirror wrote the
file, the panel read it — the record without the manager exists on
this laptop, one window because the desk had just come up from the
log-in.  This is the mechanism shown working, and not the measurement
the card set itself: a reader shown to do something different for
having read the files is still owed, and is what says whether this is
a record or a status page.

*Then `--watch` from his shell, a few minutes later: "it seems to see
nautilus, and signal as well as the terminal" — three apps on the
panel from the loop on the `Changed` signal, not from a hand's
`--once`.  Whether a closed window's row turned GONE on the live desk
was his next line, closing the card's red-first sentence on the live desk
and not only on the stub: "yup, it shows it's gone."*

## The reader — the same sitting, at his "ok. lets do the windows reader."

Asked "what next in line?", the answer was the measurement this card
set itself: a reader shown to do something different for having read
the files.  The nearest reader in the tree is a mind at the door —
`card:tools.md` already said *a mind at the door reading the desk is a
`read` over the canvas* — and it could not: the executor served the
tree's parts and the courier granted nothing else.

**What landed.**  `canvas/` is a part in `tools/executor.py`: the
name resolves to the canvas directory (TEND_CANVAS, else
`~/.local/state/tend/canvas`, outside the tree), `ls .` lists it when
it exists, `ls canvas/` is the desk, `read canvas/<file>` a row, and
`grep` walks it with the rest.  `tools/deliver.sh` grants the
directory to each call read-only beside the tree's parts, hands the
executor the path, and the seat line names it — *canvas/, the desk:
what the person is holding, as files (pins, holds, windows)*.  With
no grant the kernel refuses it like any other path, and with no
canvas the name says *not there*, never an empty desk.  Two tests,
one of them under keep both ways; three mutate rows red.

**One wrong, mine, and the fixture rule's face at the executor.**
Two existing tests went red the moment the desk became a part: they
had built a tree and no desk, and the real `~/.local/state/tend/canvas`
— the one `.win` Henri had mirrored minutes before — appeared as
`canvas/` in `ls .` and as *1 unreadable* in a kept `grep`.  The
panel met the same face on 2026-09-02 with the real `die`.  The
helpers now give every test a desk that is not there unless it
passes its own, and the comment above them says why.

**The measurement is his turn.**  From his shell, through the
openrouter door (tencent/hy3, `tools read ls grep`), with the mirror
running:

    tools/panel.py talk --door openrouter llm "What windows do I have open on the desk right now? Read the desk, do not guess."

(the `llm` row must be on the canvas — `tools/panel.py pin llm llm`
if it is not).  Read: whether the mind calls `ls canvas/` and reads a
`.win` before answering, and whether its answer names the titles the
panel shows.  A mind that answers from the tree without reaching the
desk is the seat's wording to fix, or the manifest's; a mind that
reads and answers with the titles is the record shown to be a record.
Either verdict goes here, in his words.

**His turn, 16:50 by the record, with the watch running and `llm` held.**

    $ tools/panel.py talk --door openrouter llm "What windows do I have open on the desk right now? Read the desk, do not guess."
    (call) ls canvas/ → 4 entries
    (thinking — kept in the record; talk --think shows it)
    The windows open on your desk right now are:

    - `org.gnome.Nautilus-21.win`
    - `org.gnome.Ptyxis-2.win`
    - `signal-17.win`

    (`llm.hold` is a hold, not a window.)

His word: *"Hmm.. interesting."*  The desk at that minute, read from
the session's seat (the fence can read the canvas):
`org.gnome.Nautilus-21.win` — title Home, `at` 16:35:57, **`gone`
16:36:00**; `org.gnome.Ptyxis-2.win` — this terminal, focused, changed
16:51; `signal-17.win` — Signal, changed 16:34.

**What it shows.**  The reader did something different for having
read the files: one call, the desk listed and not guessed, the hold
set aside as not a window — the record is a record, the measurement
the card set itself is met.  **And the card's red-first sentence
failed at this reader**: Nautilus had been closed for fourteen minutes, its file said `gone`,
the panel showed it bold GONE — and the
mind said *open*, because it read names and never a row — its T line
in the record says so: *"The windows are the .win files."*  `ls` shows
the name, the mark is inside the file, and a mind that stops at the
cheapest read cannot see it.  The stub's test held the sentence by
content; the live reader says content is not what gets read.  Titles
went unread the same way.

*(question, his call — the gone mark moves into the name: the mirror
renames a closed window's file `<key>.win` → `<key>.gone` (the `gone`
line kept inside), so a `.win` present is a window, `ls canvas/` says
gone to the cheapest reader, and the panel reads both; or the mark
stays inside and the seat tells the mind to read a row before it
claims one?  The first is a mechanism, the second is words on a
capped line.
henri: ok, do the rename into .gone 2026-09-06)*

**Built the same hour, at his word.**  The mirror renames a closed
window's file `<key>.win` → `<key>.gone` in the pass that finds it
missing, the `gone` line still inside; a file of the old shape — a
`.win` that already says gone inside, which is what Nautilus-21 was
on his desk — gets the name on the next pass and no second line; a
`.gone` is counted and never touched again.  A `.win` present is a
window.  The panel reads both names: `.gone` is GONE at its line's
time, or at the file's own when a hand renamed it with no line, and
a `.win` that says gone inside is GONE still, for an app's own row.
Red first — six tests red before the rename, then green — and the
recorded rows re-run: the row for the old inside-only check became
*a closed window's file keeps its .win name*.  The turn that closes
it is his again, the same command; what to read is whether `ls
canvas/` now shows `org.gnome.Nautilus-21.gone` and the mind leaves
it out.

**His second turn, 17:03 by the record, the watch restarted on the new code.**

    $ tools/panel.py talk --door openrouter llm "What windows do I have open on the desk right now? Read the desk, do not guess."
    (call) ls canvas/ → 4 entries
    (thinking — kept in the record; talk --think shows it)
    The windows open on your desk right now are:

    - `org.gnome.Ptyxis-2.win`
    - `signal-17.win`

    (`org.gnome.Nautilus-21` is now `.gone`, and `llm.hold` is a hold, not a window.)

The same mind, the same one call, the same four names — and the
closed window left out, by its name.  The card's red-first sentence,
*a `.win` with no window behind it reads as gone and never as a
window*, now holds at the cheapest reader there is, which is the one
that found it false thirteen minutes earlier.  The mechanism was a
rename; the words in the seat were never written.  Titles are still
unread by a mind that stops at `ls`, and that is the next wrinkle
when someone asks a question the names cannot answer.

**Not day one, and said so.**  The measurement the `waited` line
named — a reader shown to do something different for having read the
files — is owed, and is what says whether this is a record or a
status page.  A carrier for `--watch` (a user unit, as the tick has)
is the tick's question again.  A sweep of gone files is the person's
or the app's, not the mirror's.  A window across a shell restart is
not known: the sequence starts over and a new window may take an old
file's name; `at` and `gone` are what says which.  And the
compositor of his own stays weeks and stays not first.

## Day two — the chain, 2026-09-07, at his "implement that chain I described with ->, if it can be implemented already"

It can, on this laptop, in the shape below — and the first thing it
ran into was the rule he had signed seventeen minutes earlier
(`card:done-when.md`, `henri: signed 2026-09-07`): the chain is this
card's work and this card's `done` line was a session's draft.  No
gate refuses that yet — done-when's day one is not built — so the
rule was the session's to keep, and it was: the section below was
written first, so that the line he signed names what follows from it,
and the build waited.  His line came at 12:5x — "I signed the
canvas-windows done field" — and is in the field above, his words
copied from the mark.

**Arrow by arrow**, his 17:25 sentence (`spec/canvas.md`) against the
tree:

1. *käyttäjä haluaa avata ikkunan → hänen komentonsa luo canvas/
   hakemistoon tiedoston.*  `tools/windows.py open NAME -- COMMAND…`
   writes `canvas/NAME.win` — one file, one window — and nothing else:

       # canvas/panel.win — one file, one window (spec/canvas.md); his command wrote it
       run tools/panel.py

   No frame yet: the file says what runs, and where is the layout
   rule's until the window has been somewhere.  The first route, his
   18:25: a terminal running the panel, "jotta nähdään mitä tiedoston
   pitää sisältää".

2. *→ ikkuna avautuu ruudulle ennaltamäärättyyn kohtaan.*  The
   extension (`tools/tend-windows@tend`, already in his shell) watches
   the canvas directory; a `.win` with a `run` line and no window of
   its own is started — `ptyxis --title=tend:NAME -- sh -c 'RUN'`, a
   command implying its own instance (`man ptyxis`) — and **the window
   whose title begins `tend:NAME` is the file's window**: the tend
   interface at its smallest, a window says which file it is.  A
   window with no such title is a legacy window, on neither the canvas
   nor the panel (his line, 17:45).  Placed at the file's `frame` if
   it has one, else by the layout rule — a cascade, forty pixels on
   from the last placed — and the frame is written back.

3. *→ kun käyttäjä siirtää ikkunaa tai muokkaa sen sisältöä, sen
   ikkunan tilanne muuttuu tiedostossa.*  A move or a resize of a
   matched window rewrites `frame X Y W H` and `at` in its file; and
   the other way, a `frame` edited by hand moves the window, the same
   monitor.  Contents: not this pass — the panel's contents are files
   already, and what a notebook cell writes is `spec/canvas.md`'s
   18:35, the next card.

4. *→ käyttäjä voi sammuttaa koneen ja käynnistää sen uudelleen …
   käynnistyvät uudelleen niihin kohtiin missä ne olivat.*  At the
   extension's enable — the shell coming up at log-in — every `.win`
   on the canvas is started at its frame.  A window going down with
   the shell is not a close: the extension marks its own disable
   before the windows go, and removes no file after it.

5. *→ käyttäjä sulkee ikkunan, tiedosto katoaa kanvasista.*  A
   matched window closed from its X removes its file; and his answer
   of 17:35 read the other way, a file removed (`rm`, or moved out
   of the canvas) closes its window.  No `.gone`: close is delete.

**What goes**, by the signed line's last clause (`ls canvas/` shows
nothing he did not put there): `--once` and `--watch`, the mirror of
every window, six of its tests and four mutate rows; `.gone` and the
panel's GONE rows.  The panel's `.win` row becomes what the file says
— name, `run`, *placed at* or *opening*, changed when.  `--list` stays
(the shell's list, printed, for `--check` and a reader), `List()` on
the bus stays, and the `.win` files the mirror wrote on his desk are
his to `rm`; the extension starts nothing that has no `run` line and
says so in its log.

**Measured from this seat**: `open` writes the file and refuses a name
the panel's hand would; the panel reads it; the extension parses and
names what it watches.  **The chain's run is his hand**, as day one's
was: `tools/windows.py --install`, a log-out and in (the extension
reloads at log-in), then

    tools/windows.py open panel -- tools/panel.py
    (the window opens; move it)
    cat ~/.local/state/tend/canvas/panel.win
    (close it from its X)
    ls ~/.local/state/tend/canvas/
    (log out and in: it is back where it was)

Each arrow's verdict goes here in his words.  **Not this pass**: a
window's contents in its file; more than one canvas; a program with
several cells.
