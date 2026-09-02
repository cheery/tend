# canvas-windows — a window is a thing held, and nothing on the person's side records it

    status   shelved — 2026-08-30
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
    asked    Henri, 2026-08-30, ~10:40 — "put these into later/ as cards"
    blocked  waits on two things, in order.  A measurement: a daemon
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
