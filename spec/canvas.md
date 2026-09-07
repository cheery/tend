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

About 18:10, at the session's three questions at the close (the
material of the value stream; the first tend-compatible program; the
kaizen's shape):

> 2. panel.py käännettynä ikkunaksi voisi olla ensimmäinen
> tend-yhteensopiva ohjelma.  Toinen voisi olla työkirja-tyylinen
> terminaali.  .ipynb -tyyliin.  Mutta tässä taas pitää olla varovainen
> mitä oikeastaan määrittelee.  Miltä nämä kuulostavat?
> 1. arvovirta on tavallaan kuin prosessikartta, mikä ohjelma riippuu
> mistäkin.  Ohjelma vetää tarvitsemansa muut ohjelmat ylös, ja ne
> sammuvat kun niitä ei enää tarvita.  Pahoittelen, tämä on mielestäni
> vielä epäselvää ja pitäisi tutkia miten tämä idea oikeastaan nyt
> toteutuu, ja mikä sen loogisesti johdonmukainen versio olisi?
> 3. Mielestäni minä olen tehnyt tässä pitkän ajan kuluessa virheen.
> En ole tarpeeksi puhunut kanssasi toteutuksesta.

*A session's reading, the same minute.*  The first tend-compatible
program is `tools/panel.py` turned into a window — the smallest, since
its state is already files (the canvas, the record).  The second is a
notebook-shaped terminal in the `.ipynb` manner, with his own caution
that what defines it is the risk — and it fits the concept's fourth
sentence exactly: a notebook is a file that *is* the window's
contents.  The value stream is "a kind of process map: which program
depends on which; a program pulls up the programs it needs, and they
go down when no longer needed" — which is `card:edge.md`'s mechanism
as built (the die and the solitaire, the lock dropped at exit, idle
taking the node), so the consistent version exists in the tree
already; what is unclear, by his word, is how it is meant and how it
looks on the screen, and that is a study before a card.  And his
third: "I have made a mistake over a long time here: I have not
talked with you enough about the implementation" — recorded as said.

About 18:25, after the kaizen, at the session's fork on the first
window — a terminal running the panel placed from a file, or the
panel drawn as its own window:

> Ensimmäinen, jotta nähdään mitä tiedoston pitää sisältää.  Ja ehkä se
> työkirja-terminaali olisi ensimmäinen osa, ja panel.py olisi sen
> terminaalin ensimmäinen yhteensopiva sovellus.  työkirja silloin
> kantaisi kahdenlaisia komentoja: komentoja jotka säilyvät, mutta ne
> ajetaan (legacy terminaalikomennot), ja komennot jotka tavallaan
> vetävät jonkin tiedon tai käyttöliittymän ruudulle.

*A session's reading, the same minute.*  The first route, to see what
the file must hold.  And the order turns: the notebook-shaped terminal
is the first part, and the panel is that terminal's first compatible
application.  The notebook carries two kinds of command: ones that
persist and are run — legacy terminal commands — and ones that pull a
piece of data or an interface onto the screen.  Read against the tree:
the second kind is the pull as a cell — `pull llm`, `connect PORT`, a
hold — and the panel would be the first interface a cell pulls up,
which makes the notebook's open cells the value stream's process map
made visible, and the notebook file the one-file-one-window rule with
its contents inside.  The reading's question, unasked and his: does a
pulling cell keep pulling while the window is open, the way a
process holds an edge, so that closing the window is what lets the
pulled thing go?  *(Written after the sitting's kaizen and left
uncommitted on his "emme ole kellon orjia"; the next sitting's first
commit.)*

About 18:35, to the reading's question — does a pulling cell keep
pulling while the window is open:

> vetävä solu työkirjassa jatkaa vetoaan kunnes se poistetaan
> työkirjasta.  Eli se olisi eräänlainen tekstipohjainen ikkuna jota
> ohjelma voi päivittää lennossa, ja ohjelmalla voisi olla useita
> tällaisia ikkunoita, joita se joko käsittelee nipussa, tai sitten
> jakaa prosesseja niille.  edge card's lock olisi silloin sen
> mekanismi, kyllä näin sen ymmärrän.

*A session's reading, the same minute.*  A pulling cell pulls until it
is removed from the notebook.  So a cell is a text window the pulled
program updates as it runs; a program may have several such cells,
handled as one batch or with a process given to each; and the edge
card's lock is the mechanism — his word.  What that fixes for the
first card: the notebook file is the window (one file, one window);
a cell is the unit a program writes, and the person writes the
command — the two writers at cell granularity, the rule the windows
card had at file granularity; removing the cell is the close that
drops the lock, and closing the window removes every cell's pull at
once.  A program with several cells is a node with several rows in
one file, which is `card:cords-crate.md`'s richer row with a place to
go.  *(On disk after the kaizen, uncommitted; the next sitting's first
commit with the rest.)*

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
