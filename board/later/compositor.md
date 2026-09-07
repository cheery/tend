# compositor — the placing hand runs inside GNOME's process, and nothing in the tree can fence it

    status   shelved — 2026-09-07
    because  on this laptop the canvas is placed on the screen by a
             shell extension (card:canvas-windows.md): code in the
             compositor's process with the compositor's reach,
             installed by his hand, that no fence sees — a size Henri
             accepted on 2026-09-06 ("code inside compositor's process
             is ok..").  A window manager that is the canvas end to
             end — every window's state a file, legacy windows
             included, the graph drawn on the screen — is a compositor
             of the tree's own (wlroots/smithay), weeks, replacing
             GNOME; the card that measured it said "the compositor
             stays weeks and stays not first", and it was not.
    asked    Henri, 2026-08-30 — "letting you write a window manager
             that works as a 'canvas', where windows themselves record
             their state"; and 2026-09-07, at the close of
             card:canvas-windows.md, "lets do that what you recommend"
    blocked  waits on his word that the extension's size is wrong — its
             reach, or a desk that is not GNOME — or on a want the
             extension cannot serve.  Until then the chain runs on his
             desk from the extension, and this would be building what
             nothing needs (manifesto rule 1).
    see      card:canvas-windows.md (the chain, and the size question
             answered — "What is not decided, and is his"),
             spec/canvas.md (his chain; "only tend-compatible
             programs", which is why the extension is enough),
             card:canvas.md (the value stream's screen, and the graph
             handed there), spec/os.md property 1

## What it is, when it comes

The extension's five arrows as the compositor's own: the canvas
directory the only source of what is on the screen, every window a
file because there is no other way to have one, the layout rule the
compositor's, and the graph drawn as the screen and not as a window
on it.  What the extension cannot do and a compositor could: place a
window before it is mapped without the shell's own placement getting
there first (the 13:19 wrinkle), see a window that is not a terminal
with a title, and be fenced — a program of the tree's own under keep,
which a GNOME extension can never be.

## What it must not become

A rewrite for its own sake.  The extension is a few hundred lines
that run on his desk; a compositor is weeks and replaces the desk.
Nothing on this card is built until a want the extension cannot serve
is written down with the desk it was seen on.

## Where it sits

Shelved on arrival, 2026-09-07, handed here from `card:canvas-windows.md`
at its close.  When it wakes, it wakes below `canvas`, and the tiebreak
is his.
