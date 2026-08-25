# pull — tend runs nothing but its own suite, so the stranger has nothing to start

    status   open
    because  `vision.md`'s stranger test — "start a program in it, see it
             stop when they stop pulling, and find out what it did" —
             has no program to run: everything in this tree governs, and
             nothing is governed; the fence, the leash and the cords
             have had no caller of tend's own, and the properties on
             `spec/os.md` are cited and not built
    asked    Henri, 2026-08-25 — "Put those three on the board as cards.
             They are excellent waypoints."  The third of the three
    see      vision.md §"Ease of use" — the stranger test, which is this
             card's acceptance
             spec/os.md — items 8 (opens where it was left), 9 (may
             crash, may not hang), 13 (starts by pull; quits when nobody
             pulls), and the third open problem (how programs stay fast
             if closed the moment they are not needed)
             card:work-environment-ai.md §"The architecture" 1 and 4 —
             the node, and state as a plain file, not a memory image
             doc/experiments/2026-08-25-both.md — programs-first has a
             fence and no program of tend's own to put in it
             tools/leash.sh — a hang is a crash, exit 124; already the
             enforcement for item 9

## What it is

One node.  It opens where it was left — its state a plain file a
person can read without it; it runs while something pulls it and quits
by itself when nothing does; it may crash and may not hang; and a
stranger can start it, stop pulling, and read what it did.  No
language, no broker, no bundle format beyond a directory: the smallest
thing that is a program of tend's own, run under the fence and the
leash, so that every mechanism here has, for the first time, a caller
this tree wrote.

## What would make this card wrong

If the first node needs a vocabulary — a manifest, a capability list, a
scheduler — before it can run at all, then the pull lifecycle is not
separable from the broker and this card is the broker wearing a small
name.  The test is whether the node is under a hundred lines and
answers the stranger test as written.

## What it must not become

Bigger than one node.  The list on `spec/os.md` has sixteen items and
this card builds three; the temptation will be to build a fourth
because it is near.  A fourth is a card.
