# edge — a node cannot pull a node, so every pull is a person's and nothing runs as a network

    status   open
    because  Henri, 2026-09-02: "iso juttu on että solmu on (ohjelma +
             tilatallenne), kun käyttäjä 'vetää', hänen pitäisi kenties
             vetää tällaista solmua jossa on ohjelma ja sen tila
             yhdessä, ja ne pitäisi olla käyttäjän määriteltävissä
             vapaasti ja helposti" — and, asked what an edge is:
             "ajattelin että solmuun kuuluva prosessi voisi antaa 'pull'
             -käskyn, joka pysyy voimassa kunnes prosessi sanoo 'stop'
             tai lopettaa."  Today a pull is taken by a person's
             command or by the hold's resolver, never by a node's own
             process; so the only network the tree has is one person
             pulling one node, and the value stream he described —
             nodes depending on nodes, a directed acyclic graph in which
             programs start and stop as needed, the canvas at its end —
             has no edge to be made of
    asked    Henri, 2026-09-02 — "tee sille kortti", after the talk on
             card:session-program.md §"Talk — 2026-09-02"
    see      card:hold.md — rule 4 (cycles are forbidden, at the door)
             and "a node's pull is a lock: a puller takes a shared
             flock", the mechanism this card generalises from the canvas
             to every node; his sentence there, "a pull lasts as long as
             its puller, and the canvas is the puller that does not die"
             card:session-program.md §"Talk — 2026-09-02" — the
             conversation this card is cut from, his words verbatim
             card:canvas.md — the sink of the graph, the interface the
             user uses
             vision.md §"What comes first now" — "raised up and working";
             and §"What must not be broken"
             tools/launch.sh, tools/keep.py, llm/grant — where a grant
             word lands and where the door is
             board/done/pull.md — the first program of tend's own, and the
             pull as it was built

## What it is

A node is a directory: a `grant` (the program line, the keep words, the
sitting), a `state/`, and what the program needs.  `pull` is the one
verb and it is a lock: a puller holds a shared `flock` on the node's
`pulled` file, the runner stays up while anyone holds it, and it idles
out when the last one lets go.  The hold is the canvas holding that
lock without dying.  All of this exists and runs.

What does not exist is a puller that is a **process of another node**.
His edge is exactly the lock the hold card built, held by a program:
taken when the program says `pull`, released when it says `stop` or
exits — and the exit is the kernel dropping the lock, so an edge cannot
be orphaned by a crash.  What flows across the edge is nothing: the
pulled node's port or state is beside it, the way a kanban card is the
signal and the parts travel alongside.

Three things make it a card and not a line:

1. **The edge is a grant word.**  A node may pull only what its grant
   names — `pull NODE` — so a node's reach into the graph is granted,
   not taken (rule 1, every restraint from outside).  The cycle check
   is at that door, as the hold card's rule 4 already says: A pulls B
   pulls A with no person in it is refused before it runs.
2. **A pulled node's grant is inside its puller's.**  His "grant
   derivable from other grant files", given a direction by the value
   stream: downstream pulls, upstream cannot exceed.  The canvas's
   grant is the outermost — the person's — and each edge narrows.  A
   party may not bound itself, scaled to a graph.
3. **A second kind of node.**  Every node in the tree is the llm.
   "Freely and easily definable by the user" is a claim that only a
   second kind tests, and the network is a claim that only an edge
   tests.

## The evidence it is missing

- The four runs of 2026-09-02 morning: a person's loop pulled the llm
  node, the node's own ten-minute sitting ended three loops, and the
  hold's tick brought it back each time — a person and a resolver
  doing by hand what an upstream process would do by holding a lock.
- `proposals/compare/`: six empty turn directories in eighteen seconds
  because a person re-ran a command while a node loaded.  A pulling
  process would have waited on the lock.
- `tools/panel.py` runs outside the fence, by hand, and is the canvas
  — the sink of the graph with no graph behind it.

## What would make this card wrong

If one person pulling one node is the whole of what tend is for — a
workbench with one program in it.  `vision.md` says programs, plural,
and the stranger test says "start a program", any; the hold card wrote
the canvas as *the puller that does not die*, which is a sentence
about a graph.  It would also be wrong if the edge turns out to need
data on it — a pulled node handing a result back through the pull —
in which case this is a pipe and not a lock, and the card closes
pointing at what that would be.

## What it must not become

A service mesh, a scheduler, or a dependency on an init system.  The
tree's line on systemd holds (`card:hold.md`: the implementation,
never the dependency).  A node's process says `pull` and `stop`; it
does not register, subscribe, or heartbeat to a broker.  And it must
not become a way for a node to widen its own reach: the word is in the
grant, the grant is the person's, and a node that pulls what its grant
does not name is refused at the door like any other grant word.

## Day one

Two nodes that are nothing but the edge — the fixture rule, both sides
of the seam: a `die` node whose program answers a number on its port,
and a `solitaire` node whose grant says `pull die` and whose program
pulls it, asks, and stops.  Red first: `solitaire` with `pull die`
missing from its grant is refused at the door; with it, `die` comes up
when `solitaire` starts, `launch.sh die status` shows the puller by
name, and `die` idles out when `solitaire` exits — measured by the
lock, not by the clock.  Then the cycle: `die` given `pull solitaire`,
refused before either runs.  Too simple as programs, he said, and
exactly right as a fixture: there is nothing in them but the edge.

*(question, his call — is the second real node the panel itself, the
canvas as a node at the sink, or something that pulls the llm?
henri: Toinen oikea solmu on canvas nieluna. 2026-09-02)*

His words in full, the same minute: *"Canvas on hakemisto, joka myös
tarvittaessa tarkoittaa ikkunointisysteemin ruutua, eli ikkunat sekä
niiden dimensiot sekä mitä niissä näkyy tulisivat canvas:ista.  Ja
canvaseja olisi tavallaan kaksi.  Käyttäjän kanvas ja systeemikanvas.
jälkimmäiseen voisi laittaa vaikka web serverin pyörimään silloin kun
haluaa että se käynnistyy ja palvelee koko tietokoneen päälläolon
ajan."* — the canvas is a directory that, when needed, also means the
windowing system's screen: the windows, their dimensions and what
shows in them would come from the canvas.  And there would be two, in
a way: the user's canvas and the system canvas; into the latter one
could put a web server, when one wants it to start and serve for the
whole time the computer is up.

*And the same hour, on what the edge is for*: *"Kun prosessi vetää
jonkin toisen solmun päälle, se voi sen jälkeen aloittaa solmun kanssa
keskustelun, joka on verkon pointti.  Mutta tässä päästään
rinnakkaisajon ongelmiin ja aletaan tarvita sitä mallintarkistusta."*
— when a process pulls another node up, it can then start a
conversation with that node, which is the point of the network; but
this is where the problems of concurrency arrive, and the model
checking starts to be needed.  So the pull is the signal and the
conversation is the parts beside it, as this card says above — and
the conversation is the reason for the signal.  `spec/os.md` property
4 (a programming environment designed for concurrency; behaviour
verified by types and automatic model checkers) has been "in the air"
in every status pass since 08-26; this is the first sentence in the
tree that names what would call it.  Not this card's day one, which
has one edge and no conversation on purpose; the card that carries
the first conversation carries the first caller for 4b.

So the second real node is the sink itself, and the tree has both
halves of that sentence already as shape: `card:hold.md` names a
**system canvas** for what opens when the machine starts and a **user
canvas** for when the person logs in; and `later/canvas-windows.md`
(shelved 2026-08-30) is the screen half — a window is a thing held,
and nothing on the person's side records it.  Whether his words today
are the event that card waits on is his to say; this card's day one
stays the die and the solitaire, because the canvas as a node is the
second real node and not the fixture.

## Where it sits

Placed last by the session that wrote it, at his "tee sille kortti";
the tiebreak is his.

## Talk — 2026-09-02, the 12:52 sitting: reconfiguration by pull

Opened at his word at the close of the morning (`doc/kaizen/2026-09-02-0557.md`):
*"tuo uudelleenkonfigurointi vedolla on mielenkiintoinen aihe.  Me
voisimme aloittaa seuraavan keskustelun sillä."*  The tree's state
first, so the talk starts from the thing and not from memory.

**The property** is `spec/os.md` 5: *"mikäli asennus konfiguroi
ohjelman, tehty konfiguraatio tulee merkitä ohjelmasolmuun.
veto-menetelmällä ohjelma tulisi kyetä uudelleenkonfiguroimaan sieltä
mistä se tulikin."*  Its first half is built: the grant beside the
program and `state/` are the configuration recorded in the node, and
`/usr/local/lib/tend/installed` is the same record for the restraints.
Its second half was decided against on 2026-08-27 in one form and
reopened on 2026-09-02 in another, and the two forms are not the same
sentence:

- **Refused, 08-27 — the pull's text as a grant.**  `pull sitting 900`
  is a line in the pull file and nothing more (`tools/launch.sh`'s
  header; `card:session-program.md`, the limit's decision 1).  The
  reason is Rule 1: a pull is the one thing a fenced session may write,
  so a pull that configured the node would be the bounded party writing
  its own boundary.  That refusal stands, and nothing below reopens it.
- **Reopened, 09-02 — a grant derived from a grant.**  His *"ehkä grant
  kuuluisi olla johdettavissa muista grant-tiedostoista"*, given a
  direction by the value stream in point 2 above: the pulled node's
  grant is inside its puller's.  Configuration arrives *with* the pull,
  but from upstream — the puller's grant, which is inside the canvas's,
  which is the person's.  Narrowing only; a widening is refused at the
  door.  It does not touch the 08-27 refusal, because the writer is a
  grant and not a pull line, and the direction is outer to inner.

**Two readings of *"sieltä mistä se tulikin"***, and the tree has held
both since 08-26 without saying they are two:

- (a) **the origin.**  A node came from somewhere — a directory, a
  commit, a hash — and pulling it again reconfigures it from there;
  install is fetch.  This is `card:work-environment-ai.md`'s
  content-addressed node and `spec/os.md` open problem 2 (how are
  programs protected, and installed); every status pass since 08-26
  says it waits on the store.  Nothing of it is built: a node today is
  a directory in the tree, its origin is git, and its state records
  nothing about what a run ran under — the 08-28 "cheap slice" (grant
  sha, tree commit, model file and hash, in `installed`'s shape) still
  has no reader.
- (b) **the puller.**  The node is reconfigured by whoever pulls it,
  from the puller's grant: the edge carrying grant words downstream.
  This is what point 2 says, and it is the one reading day one can
  test — `solitaire`'s grant says `pull die`, and what `die` runs
  under is its own grant narrowed by `solitaire`'s.

What (b) may carry is the real question.  The boundary words —
`allow`, `write`, `sitting`, `idle` — narrow, and narrowing is safe by
construction.  But `bind 18080` or a program argument is not a
boundary: it is a parameter of the conversation that comes after the
pull, and a puller setting it is *configuring*, not bounding — which
is the property's own word, *konfiguroida*.  The tree has no rule yet
for a word that a puller may set and that is not a restraint.

*(question, his call — "sieltä mistä se tulikin": did the 2026-08-19
line mean the origin a node was fetched from (a), the puller that pulls
it (b), or both — and if both, which does the tree build first?)*

*(question, his call — may a puller's grant set a parameter of the
pulled node that is not a boundary, such as its port or a program
argument, or may it only narrow the boundary words, with every
parameter belonging to the conversation after the pull?)*

**The rest of what was "in the air" in `spec/os.md`**, read out at the
close of the morning and left for this sitting at his *"ne jääkööt
seuraavaan istuntoon"*, written down here so the next reader has it in
one place: **4b** (types and model checkers) has its first named caller
above — the conversation after the pull — and nothing else; **6b** (no
central server by default) is half-answered by his *"tilatallenne
taitaa olla solmun identiteetti"*, since an identity that is a state
store on a disk needs no server to be one, and the other half — how two
machines agree on a node — is untouched; **open problem 3** (fast when
closed the moment it is not needed) was seen twice today unnamed — the
80 s reload the hold exists to prevent, and the six empty turn
directories of a person re-running while a node loaded — so the hold
is its first mechanism and the edge its second; and the **language
three** (10, 15, and the bootstrap line) are where they were on 08-26,
untouched, and are not on any card.
