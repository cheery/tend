# canvas.md — the concept, in the words it was first said in

Started 2026-09-06, the 15:59 sitting, after a day that built the
windows mirror (`card:canvas-windows.md`) and Henri's "I am again a bit
mystified … do you have an idea why are we tracking windows now?  Is it
clear what the goal here is?" — and his answer to the session's reading:
*"I think the failure is on my end.  I haven't explained the concept
clearly enough."*  So this file: his words first, verbatim; a session's
reading after, marked as one; questions where two readings differ,
each waiting for his line.  A card serves a sentence here or says why
it cannot.

## His words — 2026-09-06, about 17:25

> No tämä on eräänlainen visio.  olen inspiroitunut lean-filosofian
> mukaisista arvovirroista.  Ajattelin että ne tekisivät hienon
> käyttöliittymän tietokoneeseen.  Se kaikki toimisi siten että
> käyttäjä haluaa avata ikkunan -> hänen komentonsa luo canvas/
> hakemistoon tiedoston, joka sisältää ikkunan tilanteen -> ikkuna
> avautuu ruudulle ennaltamäärättyyn kohtaan -> kun käyttäjä siirtää
> ikkunaa tai muokkaa sen sisältöä, sen ikkunan tilanne muuttuu
> tiedostossa -> Käyttäjä voi sammuttaa koneen, ja käynnistää sen
> uudelleen, ikkunat sammuvat, ja käynnistyvät uudelleen niihin kohtiin
> missä ne olivat ennen sammutusta. -> Käyttäjä sulkee ikkunan,
> tiedosto katoaa kanvasista.

The same sitting, about 17:35, with the four answers below (the fifth
line of his reply, said to no question):

> Meidän ei tarvitse kaikkia ikkunoita seurata.  Riittää että
> ominaisuudet toimivat ikkunoissa joissa on tend-rajapinta, eli
> tend-yhteensopivissa ohjelmissa.

Earlier words this file gathers, kept where they were said and cited
here: 2026-08-30, "a window manager that works as a 'canvas', where
windows themselves record their state" (`card:canvas-windows.md`);
2026-09-02, "Canvas on hakemisto, joka myös tarvittaessa tarkoittaa
ikkunointisysteemin ruutua, eli ikkunat sekä niiden dimensiot sekä
mitä niissä näkyy tulisivat canvas:ista.  Ja canvaseja olisi tavallaan
kaksi.  Käyttäjän kanvas ja systeemikanvas." (`card:edge.md`); the
same day, "vasta graafisessa ympäristössä se voi näyttää
sugiyama-graafin" (`card:canvas-windows.md`).

## A session's reading — 2026-09-06, the same minute; his to grade

*This is a kind of vision.  I am inspired by the value streams of lean
philosophy; I thought they would make a fine user interface for a
computer.  It would all work like this: the user wants to open a window
→ their command creates a file in the canvas/ directory that holds the
window's state → the window opens on the screen at a predetermined
place → when the user moves the window or edits its contents, that
window's state changes in the file → the user can shut the computer
down and start it again: the windows go down and come up again where
they were before the shutdown → the user closes the window, and the
file disappears from the canvas.*

What that decides, read against what the tree has:

1. **The file is the source and the window is its view.**  A command
   writes the file; the window appears because the file is there.
   The mirror built today (`tools/windows.py`) runs the other way —
   the compositor is the source and the file is a copy — so it is the
   read half of this and not the thing itself.  It stays as the
   record of windows this tree does not yet place.

2. **A window file is a hold.**  Presence is the claim: while the file
   is there the window is up, and after a shutdown it comes up again
   where it was — the resolver's promise (`card:hold.md`), now for a
   window.  Which means the file says enough to bring the window back:
   what runs in it, and where.

3. **Close is delete.**  The user closes the window and the file goes.
   Today's `.gone` — a closed window's file kept and renamed — is the
   opposite of this sentence; it came from the hold card's death
   notice, not from his words.  A window that goes down at shutdown is
   not closed: the file stays, and that is the whole difference.

4. **The contents are in the file.**  "muokkaa sen sisältöä … tilanne
   muuttuu tiedostossa": not only the frame, what the window shows.
   The shallow row of today (app, title, frame) is what a manager can
   see from outside; the state he means is the app's own.

5. **Value streams are what the screen shows.**  Windows are stations
   and the pull edges between nodes are the flow; the layered graph
   is the picture of it.  This is the sentence the whole card list
   under `canvas` serves, and the one nowhere written until now.

6. **Only tend-compatible programs.**  *We need not track every
   window; it is enough that the properties work in windows that have
   the tend interface, in tend-compatible programs.*  So the canvas
   is not a record of the desk, it is the desk of programs that speak
   tend — and today's mirror of every window the shell has is more
   than the concept asks for.  A foreign window is not the canvas's.
   This bears on the questions on the frame-and-contents file and on
   a window with no node behind it, below, without answering them:
   a program with the tend interface can write its own state, and a
   window with no node behind it may simply not be on the canvas.

7. **From his four answers, the same minute.**  Writing the canvas is
   the user's; a launch command may write what the file needs.  A
   layout rule places a window the first time when the file gives no
   place, and after that the file says.  A close from the window's X
   is the same act as `rm`, or as moving the file out of the canvas.
   On this laptop the placing hand is the GNOME extension reading the
   canvas; the compositor of his own is the far end.

8. **One file, one window — the rule that holds.**  From his last
   three answers, about 17:45: a file maps one window; the file, in a
   way, starts a process, and the process may draw the window — the
   mechanism is the session's to choose, the rule is not.  Legacy
   GNOME windows stay as they were, and are not on the canvas.  And
   `.gone` is "perhaps a somewhat useless concept" — interesting, and
   not the concept's; it and the mirror of every window are the read
   half of a desk the concept does not claim, and their retirement is
   a card's decision, not this file's.  Every mark below is answered.

## Where two readings differed — his call, answered the same sitting

*(question, his call — whose command creates the file: the person's
hand only (`panel.py pin`'s shape), or any program — a terminal's
`open lander.md` writing `canvas/lander.win` — with the hand as one
writer among them?
henri: canvasiin kirjoittaminen olisi käyttäjän homma, mutta sitä varten voisi olla käynnistyskomento joka kirjoittaa kanvasiin tarvittavat asiat. 2026-09-06)*

*(question, his call — "ennaltamäärättyyn kohtaan": the file names the
place and the window goes there; or a layout rule places it and the
file records where it landed?
henri: layout sääntö voisi asettaa sen ensimmäisellä kertaa, jos paikkaa ei ole annettu tiedostossa. 2026-09-06)*

*(question, his call — the frame and the contents: one file the
manager and the app both write, or two — the manager's row for the
frame and the app's own beside it, as `card:canvas-windows.md` proposed?
henri: Yksi tiedosto kartoittaa yhden ikkunan. tiedosto tavallaan käynnistää prosessin, ja prosessi voi piirtää ikkunan. Tai miten sinä sen haluatkaan toteuttaa. Kuitenkin - yksi tiedosto, yksi ikkuna, tämä sääntö kestää. 2026-09-06)*

*(question, his call — on close the file disappears: removed by the
manager at the window's close, so that closing by the window's own X
is the same act as `rm`; or only by the command, so that a window
closed from its X comes back?
henri: Kyllä, se on sama kuin jos käyttäjä kirjoittaa 'rm' ja poistaa tiedoston, tai siirtää sen ulos kanvasista. 2026-09-06)*

*(question, his call — the restart after shutdown is the resolver's:
the file says which node runs in the window, and a window with no node
behind it — a foreign program's — is placed but not started?
henri: legacy gnome-ikkunat olisivat samalla tapaa kuin ennenkin, eivät kanvasissa. 2026-09-06)*

*(question, his call — on this laptop, the placing hand is the GNOME
extension (it can move, resize and raise a window it sees) reading
the canvas; the compositor of his own stays the far end?
henri: juu, tuo sopii minulle. 2026-09-06)*

*(question, his call — today's `.gone`: dropped now, or kept until the
write half exists and the mirror is retired?
henri: .gone on kenties vähän turha konsepti. Se oli kyllä mielenkiintoista. 2026-09-06)*

## What this file is not

Not a card and not a spec of the mechanism: it holds the concept in
the words it was said in, and a session's reading beside it, so that
a card can say which sentence it serves.  When a reading here is
wrong the concept gains a sentence in his words; the reading is never
rewritten to look right.
