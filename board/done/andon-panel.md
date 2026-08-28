# andon-panel — a cord pulled while the person is away is a line in a file nobody is watching

    status   done — 2026-08-28
    because  Henri, 2026-08-28: the andon reaches the person only through
             a sound, and on 2026-08-28 that sound did not travel — the
             `audio` row allowed, the PipeWire socket present on the
             host, and a ring from inside the fence still silent, because
             a restrained session cannot bind a channel across its own
             fence (card:silent-cord.md §10:18).  A session *can* write
             the pull — `ask` and `ring` write under
             ~/.local/state/tend, which the fence binds writable, needing
             no reach at all — but nothing on the person's side
             *announces* it, so a cord pulled while he is in the next
             room is a line in a file nobody is watching.  "There should
             be an interface … that reacts to the andon, so that no audio
             required from inside the fence."
    asked    Henri, 2026-08-28 — "open the interface card and build the
             TUI first.  I think we need it next."
    see      card:silent-cord.md §"10:25" — the direction this is cut
             from, and the two tracks (this interface load-bearing; the
             audio-row fix parallel)
             tools/andon.sh — the record it watches: andon.pending (the
             questions), andon.log (every ask, ring and answer), the
             pulled-state tools/limit.sh already reads
             card:cords.md — the andon is one of the two cords; this is
             its person-side half, which gestate's synth was and tend
             never built

## What it is

A person-side interface, outside the fence, that watches the andon
record and announces a pull: the unanswered questions shown as a list,
a new ring made a sound and a flash, and the person answering there —
`tools/andon.sh answered`, the word the fence already refuses a session.
Because the session only ever *writes* the record and the interface only
ever *reads* it, the cord reaches the person through a channel a fenced
session cannot cut: it never touches it.  The reach requirement drops
away, which is the whole point.

Cheapest first, and the TUI is first (Henri, "build the TUI first"): a
program the person keeps in a spare terminal that tails the record,
rings the terminal bell and prints the question on a new pull, shows the
pending list, and answers on a keypress.  A local server with a web
panel, or a GUI tray for away/remote reach, are the same record read by
a richer view, and are later.

## What it must not become

* **A way for a session to answer its own cord.**  `answered` is the
  person's word (`tools/andon.sh` refuses it inside the fence); the
  panel runs on the person's side and owns it, and a session must never
  reach the panel to clear its own question.
* **A second andon.**  The record is `tools/andon.sh`'s; the panel reads
  it and does not write it (except `answered`, through `andon.sh`).  A
  panel that invents its own state is two cords disagreeing.
* **A load-bearing sound.**  The bell is the panel's, on the person's
  side; the cord is the *record*, and the panel announcing it must
  degrade to a printed list if the terminal cannot beep — a silent
  panel still shows the question, which is more than the fence let
  through today.

## Where it sits

Placed by the session that opened it, at Henri's "I think we need it
next" — 2026-08-28, the andon strand's active build, beside
`card:silent-cord.md`; the tiebreak is his.  Day one is the TUI:
`read_state` over the record (tested), and a curses view that polls it,
bells on a new ring, and answers on a key.

## 2026-08-28, 10:35 — day one: the TUI

Built at Henri's word.  `tools/andon-panel.py` runs on the person's
side and reads the andon record; `read_state` — the pure reading the
view polls — returns the pending questions with their stamps, the ring
count a new ring is detected by, the last ring's time (cleared by an
answer), and the pulled state `tools/limit.sh` shares.  Five tests over
`read_state`: an empty record is a quiet panel, the questions and their
stamps are read, a ring makes it pulled and carries the time, a second
ring increments the count the view watches, and an answer clears the
pull — red first (the module absent).

The view is `curses`: a reverse-video title that blinks on a fresh
pull, the pending list, and a footer — `[a] answer all  [r] refresh
[q] quit`.  On a new ring since the last look it `beep`s and `flash`es;
`a` runs `tools/andon.sh answered` (the person's word, and the panel is
on the person's side to own it).  It degrades honestly: no terminal and
it prints a one-line summary instead (`N pending, pulled since HH:MM`)
and says to run it in a terminal — a silent panel still shows the
question, which the card's §"must not become" requires.  Run it:
`python3 tools/andon-panel.py`, outside the fence, in a spare terminal.

What day one does not do: the local server and the GUI tray (later
views over the same record), and any *remote* reach — the TUI is the
terminal in the room.  The card stays `doing` until Henri has kept it
open through a real pull and said the announce is enough; the audio-row
fix (`card:silent-cord.md` §10:18) is still its own line, parallel.

## 2026-08-28, 10:52 — the panel now plays a real tone

Henri, keeping the panel open through a ring: "the TUI doesn't produce
audio when it reacts to andon."  The cause was `curses.beep()` — the
terminal bell (BEL), which terminals mute or make visual by default, so
the panel flashed and stayed silent.  Fixed: on a new ring the panel
writes the andon's own two-note tone and plays it through a real player
(`pw-play`/`paplay`/`aplay`, or `TEND_PANEL_PLAYER`), with `curses.beep`
only as the fallback when no player is found.  This is why the panel
belongs outside the fence — a real player there reaches the socket the
fenced andon could not (`card:silent-cord.md`), which Henri's host-side
ring already proved.  Tested: the tone is a valid wav, and `_play_alert`
hands it to the player.  Restart the panel to pick it up.

## 2026-08-28, 11:03 — heard

Confirmed: rung from inside the fence, the restarted panel played the
tone and Henri heard it — "yes, I heard it."  The reach-free cord is
whole end to end: a fenced session writes the record with no row, the
panel outside the fence reads it and plays the andon's own two-note tone
through `pw-play`, and it reaches the person in the next room.  The
audio line is closed; what keeps this card `doing` is only the later
views (a server, a GUI tray) and Henri's word on whether the TUI is the
whole of what he wants — the `because` is answered, and the card is his
to move to `done/`.
## 2026-08-28, 13:00 — done

Moved to `done/` at Henri's "Move andon-panel to done" — the sitting
after "yes, I heard it".  The `because` no longer stands: a cord pulled
while the person is away is a two-note tone in the next room, through
`tools/andon-panel.py` outside the fence, with no reach row in the
path.  The later views (a server, a GUI tray) are widenings awaiting a
want, not debt; the `audio` row's own fix stays `card:silent-cord.md`'s.
