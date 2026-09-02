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

**His answers, the same sitting, having set its clock to 120 minutes**,
verbatim: *"1. 19.8 kirjoittamani taisi tarkoittaa alkuperää.  'sieltä
mistä se tulikin'.  2. mielestäni se saisi olla toisinpäin, mutta en ole
nyt varma asiasta.  Solmun grant saisi olla mahdollisimman rajattu, ja
käyttäjä antaisi sille parametrejä ja lisää vapauksia.  Ehkä."*

— 1. The line of 19.8 probably meant the origin.  2. He thinks it
should be the other way round, but is not sure now: the node's grant
should be as narrow as possible, and the user would give it parameters
and more freedoms.  Perhaps.

What that does to the tree, read before anything is built on it:

- **Property 5's second half is (a), the origin, and stays where every
  status pass has put it: waiting on the store**, open problem 2.  The
  note is on `spec/os.md` under the property.  Reading (b) is not the
  property; it is a second thing he wants, and it has its own sentence
  now, the one above.
- **The direction of point 2 is reversed and survives.**  Point 2 said
  each edge narrows: the pulled node's grant is inside its puller's.
  His sentence puts the *node's own* grant at the bottom — the least
  the program needs, written by whoever wrote the program — and has the
  user add to it.  The two are one picture with three layers: the
  node's grant is the **floor**, the puller's grant is the **ceiling**,
  and what the puller gives — parameters and freedoms — lies between
  and may not reach above the ceiling.  Rule 1 holds because the party
  that widens is never the party widened: the node does not write its
  gifts, the puller does, and the puller may give only what it has.
  The 08-27 refusal holds too — a pull *line* still configures nothing;
  a *grant* on the person's side does.
- **The llm node's grant is the evidence he is right.**  Read
  `llm/grant` as two lists: what llama-server needs anywhere (`allow
  model`, `model …`, `bind 18080`, `program …`) and what *this machine*
  needed to run it (`allow-try /opt/intel/oneapi`, `allow /sys`, `write
  /dev/dri`, the two `NEO_CACHE` env lines, `make neo-cache`) — six of
  its thirteen lines are the work laptop's, dated 2026-08-28, mixed into
  the node's own grant because there was nowhere else to put them.
  His floor-and-gifts would put the first list in the node and the
  second in the person's hand on this machine.
- **Where the gifts would live is already built as shape and not as
  content**: a `.hold` in the canvas is the person's standing pull, on
  the person's side, and its content today is the asked-by — words the
  launcher reads and does nothing with.  A hold that carried grant
  words would be reading (b) in the tree's own grammar, with rule 5 of
  `card:hold.md` (the canvas is where a session cannot write) as the
  thing that keeps it Rule 1.  Not built, and not this card's: he said
  *ehkä*, and a mechanism built on a *perhaps* is a session deciding
  for him.

**So day one stands as written and depends on neither answer**: the
die and the solitaire need one edge and no gift.  What changes is one
sentence in point 2, left as it is above with this section as its
correction, kept rather than rewritten.

## Day one landed — 2026-09-02, the same sitting

Built in the hour after his answers, in `tools/launch.sh` and two
directories, and measured by hand in scratch before the tests were
written.

**The word.**  `pull NODE` in a grant.  `pull` was already a grant word
— *the file a pull appends to*, `pull node.state.pull` in the first
node's grant — so the value decides: a value with a grant beside it is
a node, and anything else is the pull file as before.  A bare name is
a node of this tree, `./x` or `../x` is beside the grant that says it
(so a fixture's two nodes can live in one scratch directory), `/x` is a
path.  The launcher adds `--allow NODE/state` to keep's flags — the
pulled node's state readable, and nothing else of it.

**The edge.**  `NODE/state/pulled/<puller>`, one file per puller, made
by the puller's `run` on the person's side before keep execs the
program, and named to the program in `$TEND_PULLS`
(`die=/…/die/state/pulled/solitaire`).  The program takes a shared
`flock` on it — the pull, in force until the process closes the fd
(`stop`) or exits.  The launcher never takes it: the pull is the
process's, his words, not the runner's.  The filename is the puller's
name, so `status` on the pulled node says `pulled by: solitaire` with
no registry and no pid; an unlocked file is the trace of an edge that
was, like `stopped`.

**The pulled node's side.**  Three places read the lock, each with
`flock -n FILE true` failing: the watch loop is not idle while any edge
is held (rule 2, as for a hold); `serve` starts a runner for a node
that is pulled and has none, so the tick is the carrier as it is for a
hold; `status` and `check` name the pullers.  After a death, `serve`
restarts only on an edge newer than the death — rule 3 as for a hold —
and since a puller under keep has read on its edge and cannot touch
it, the die waits for a fresh puller, which is said in the header
rather than hidden.

**The door.**  `reaches_back` follows `pull` lines from each pulled
node's grant; a path that reaches the node itself is ✗ in `check`
(exit 1) and exit 2 in `run` before the lock is taken, from either end
of the cycle.  Sixteen deep is read as a cycle and said.

**The two nodes.**  `die/` — `pulse roll`, `idle 30`, a program that
writes one number to `$STATE/roll` by rename and sleeps; the roll's
mtime is its pulse, so idle counts from the roll.  `solitaire/` —
`pull die`, a program that locks the edge, waits for a `roll` newer
than its own start (a stale roll from an earlier run is not an
answer), says `solitaire: die rolled N`, closes the fd on purpose
before exiting, so `stop` is exercised and not only exit.  Both
`no-net`; both `allow` only their own script.  Their state directories
are gitignored like the first node's.

**Measured, 13:16, in scratch, by hand and then by
`test/test_launch.py` (five tests, 54 in the file, 218 across launch,
resolve and board, none red):**

- Red first, from both sides of the door: a node whose program reads
  `die/state/roll` with no `pull` word is refused by keep — `Permission
  denied`, the kernel's voice; the solitaire with the word deleted says
  *the grant names no edge to die — `pull die` is the word*, exits 2,
  and the death notice on the andon record carries that sentence.
- The cycle: `die` given `pull ../solitaire`, `check` says ✗ *reaches
  back to die*, and `run` exits 2 from either end with no log written.
- The flow: the solitaire's process locks the edge; `die status` says
  *not running, pulled by: solitaire*; `die serve` says *is pulled by
  solitaire and no runner — started one*; the die rolls 1; the
  solitaire's log says *die rolled 1* and it exits 0; the edge is
  unlocked; the die's `stopped` reads *idle: nothing has pulled die for
  1s* within a tick; a second `serve` starts nothing.  **Measured by
  the lock, not by the clock**, as the card asked.
- Rule 3: a lock on an edge older than a death starts nothing; the same
  lock on an edge touched after the death starts the die.

**What is not built, and is said where it was measured.**  (1) A
generic program — llama-server — cannot say `pull`: only a program
written to read `$TEND_PULLS` and lock can, so the edge is for nodes
of tend's own until a wrapper takes the lock on a program's behalf,
which would be the runner pulling and not the process, the thing this
day one refused on purpose.  (2) The pulled node comes up at the next
tick or `serve`, not at the lock: the solitaire waited for the tick,
and its `SOLITAIRE_WAIT` of 60 s is the latency it tolerates.  A puller
that resolves what it pulls would be a scheduler, which §"What it must
not become" forbids; the tick's period is the edge's latency, and that
is the hold card's line too.  (3) Nothing flows: the solitaire read a
file in the die's state.  A conversation over a port needs a `connect`
word keep does not have, and that is the first caller for os.md 4b,
as the talk above says — not this card's.  (4) Nothing of the gifts:
the floor-and-ceiling of the talk is written and not built, at his
*ehkä*.

**The panel, the same sitting** — Henri: *"paneeli voisi näyttää reunat
riveinä.. vasta graafisessa ympäristössä se voi näyttää
sugiyama-graafin."*  Built as said: `tools/panel.py` reads both ends of
an edge as words on a row — `pulled by — solitaire` on the pulled node
and `pulls — die` on the puller — and a node a process pulls with no
runner up is bold, *PULLED, NOT RUNNING*, the same promise a hold makes
and the resolver keeps at its next visit.  A node alive by an edge is
on the canvas whether or not it is pinned, as a held node is; the
counts line says `N pulled`.  Two tests in `test/test_panel.py`; the
first found that `flock -s FILE sleep` hands the lock to its child, so
a killed `flock` is not a released edge — the tests hold the fd
themselves, as the solitaire does.  The graph drawn as a graph —
layered, Sugiyama — is the graphical canvas's and waits with
`later/canvas-windows.md`, in his words; a terminal shows rows.

**His question, the same sitting, 14:20**: *"Mietin tätäkin: pitäisikö
vain canvas-läheisissä solmuissa olla määrätty tila, vai kuuluuko se
jokaiselle solmulle?"* — should only the nodes near the canvas have a
defined state, or does it belong to every node?

What the tree has, read before answering.  Every node has a `state/`
because the launcher writes one — `run.lock`, `stopped`, `watch`,
`ticks`, the pull file, now `pulled/` — and that is **lifecycle**
state: tend's, not the program's, read by the resolver and the panel,
and it belongs to every node by construction.  Beside it, in the same
directory, the tree already has two other kinds without naming them:
`llm/state/neo-cache` is a **cache**, state the program may lose and
rebuild (80 s), and `node/state/node.state` is **identity**, the tally
the first node exists to carry across its stops — property 8's "open
where left", the thing his *"tilatallenne taitaa olla solmun
identiteetti"* meant.  The die has none of the third: its `roll` is
the conversation, not the node; a fresh die is the same die.  So the
question is about the third kind only, and the tree's answer so far is
that it has never said which nodes have it — a node's identity state
is whatever its program happened to write.

A session's reading, offered and not decided: **identity belongs to
the nodes that declare it, and to no node by default** — not to every
node, and not to canvas-nearness as such.  Near the canvas is where
most of it will be, because that is where the person's own work is
(the windows, the document, what shows), and a stateless interior is
what makes the network cheap: a node with no identity can be pulled by
many, restarted anywhere, and reconfigured wholesale from its origin
(property 5's (a): program and configuration both from the store,
nothing of it here).  It is also where 4b's cost does *not* land — the
concurrency he named arrives at nodes with mutable identity, and a
declared boundary keeps the model checking to the few.  But "only
near the canvas" as a rule breaks on the first database node three
edges in, which has identity and no window; so the rule is *declared*,
and the canvas is where the declarations will cluster.  The mechanism,
if it is wanted, is one grant word naming the identity (`state
node.state`, say), so that a node with the word moves with its state
and a node without it is reinstalled by a pull; nothing reads such a
word yet, so it is not built (manifesto rule 1), and the first reader
would be the store.

*(question, his call — is identity state a declared property of a
node — a grant word, absent by default — or a property of every node
that the person may leave empty?)*

**His answer, 14:27**: *"huh. olet oikeassa.  tietokanta tosiaan on
solmu, jossa tila, ja se on syvällä verkossa.  Tässä on vain kysymys
miten solmu pääsee siihen käsiksi.. Varmaan oman tilansa kautta!"* —
a database really is a node with state, deep in the network; the only
question is how a node gets at it, probably through its own state.

So "declared, not canvas-near" stands, and the question moves to the
access.  The tree's day one already answers half of it, read back:
the solitaire reached the die **through the die's state** — `pull die`
grants read on `die/state`, the edge file sits inside it, and the roll
was read beside the edge.  That is one reading of *oman tilansa
kautta*: the pulled node's state is its interface, and what a puller
may see of a node is what the node left in its state.  The other
reading is the puller's own state: the launcher puts the handle where
the program already looks — `$STATE/pulls/die`, a link to the die's
state, made at `run` beside the edge file — so a program finds what it
pulls in its own directory and `$TEND_PULLS` becomes a convenience
rather than the mechanism.  The two are one line apart in
`tools/launch.sh` and are not exclusive; the second is one symlink
and is not built until he says which he meant.  What neither reading
covers is a database's *conversation*: a query is a write or a
connect, and keep's grammar has read on a state and a `bind` for one
port and no word for reaching another node's socket — the first caller
for os.md 4b, as this card said at its opening, now with a concrete
shape: a socket in the pulled node's state, and a grant word that lets
a puller open it.  Not built; measured first, because whether Landlock
governs a connect on a unix socket by path is a fact about the kernel
this tree has not measured.

*(question, his call — "oman tilansa kautta": the pulled node's state
as its interface (what day one did), or a handle in the puller's own
state (`$STATE/pulls/<node>`, one symlink), or both?
henri: vedetyn solmun tilaa rajapintana. ehkä molempia. 2026-09-02)*

So the pulled node's state is the interface, which is what day one
built and what the die and the solitaire measure; the handle in the
puller's own state is an *ehkä* and stays a line not written.

**His two questions, 14:30**: *"Osaisitko sanoa miten lean-tyylisiä
arvovirtaketjuja/veto -käytäntöä sovellettaisiin itse ohjelmiin ja
ohjelma-asennuksiin?"* and *"Ja tarvitseeko sitä miettiä jo nyt?"* —
how would lean value streams and pull practice be applied to programs
themselves and to installs, and does it need thinking about now?

The tree's answer, read off what it already runs, with lean's names
put beside each: the **customer** is the person at the canvas, and
liveness enters only through a canvas (`card:hold.md` rule 4) — that
*is* pull, against the push of an init system starting everything at
boot.  The **kanban card** is the edge: the signal travels upstream
(the lock), the parts travel downstream beside it (the state).  The
**supermarket** — a small standing stock where demand is frequent,
replenished when drawn — is the hold: the llm kept warm because the
80 s reload is the changeover cost, lean's SMED problem, open problem
3 on `spec/os.md`.  **Overproduction**, lean's first waste, is F017
exactly: a node run with no pull, found today.  **Waiting** is the tick:
the solitaire waited up to 30 s for a die that could have come up at
the lock; lean would cut that lead time, and this card's "not a
scheduler" line is the reason it has not.  **Andon** and **jidoka** are
the cord and property 9 (crash, never hang).  The **value stream map**
is the DAG, and the Sugiyama drawing he named is literally that map.
For **installs**: just-in-time supply is property 5's (a) — a node is
not installed in advance but fetched from its origin at the first pull,
its configuration recorded in the node, re-pulled to reconfigure; the
store is the supplier and the node directory is the bin.  What lean
has that the tree does not: a **kanban count** — how many pullers a
node serves at once, the WIP limit on an edge — and **takt**, an even
rhythm of demand; neither has a caller, since no node has two pullers.

*Does it need thinking now?*  Mostly no: the practice is already in
the tree without the vocabulary — it fell out of his 08-19 list and
the hold card — and naming it changes no mechanism.  Two places where
the names earn their keep today: F017 is clearer as *overproduction*
than as a race (it says why running unpulled is the worst waste, not
a harmless extra), and the store, when it comes, is a **supplier**
question — what the pull orders, what the bin holds, what "from the
origin" means — and that thinking is owed before the store is built,
not before.  The kanban count waits for a second puller.

## The conversation over the edge — 2026-09-02, the 15:13 sitting, at his "aloita connect-mittauksesta"

**Measured first, 15:15.**  `tools/keep.py` already has `--connect PORT`
— `--bind`'s twin, written 2026-08-28 for a led turn under keep
(`lead.sh NODE --kept`) and held by `test/test_keep.py` — and it holds
on this kernel, from this seat: under keep with only `bind 1`, a
connect to a listener on 127.0.0.1:18099 is `Permission denied`; with
`--connect 18099` it connects; with `--connect 18098` (the wrong port)
it is refused; and with `--connect 18099` a bind is refused.  Four
lines, one listener, no build.  So the kernel's half of the
conversation has been in the tree for five days with no grant word to
reach it: `tools/launch.sh` knows `bind` and not `connect`, and a grant
saying `connect 18080` was "unknown word", exit 2.  The unix-socket
question from the talk above is not needed for the first conversation
— the llm listens on a TCP port — and stays unmeasured.

**Built, 15:20–15:40.**  `connect PORT` as a grant word in
`tools/launch.sh` — `bind`'s twin, a port and nothing else, red first
(`test_launch.py::test_connect_is_a_grant_word_and_without_it_the_kernel_refuses_the_talk`:
with the word a program under keep reaches a listener, with `bind 1`
instead it is `Permission denied`, `connect eighty` is refused at
parse).  The check prints the third verdict for it: keep lets the
program talk to the port, and whether anything listens is the other
node's business, at run.  Then **`ask/`**, the third node of tend's own
and the first conversation over an edge: `pull llm` for the signal,
`connect 18080` for the talk, a program that takes the edge, waits for
`/health` (the tick brings the llm up; the model takes about 80 s), asks
one question — `run`'s arguments, or one about the tree — writes the
answer to its own `state/answer` beside the signal, says it in the log,
and lets go.  With `connect` gone it does not wait out its clock: the
kernel's refusal comes back wrapped in the first request, and the
program names the missing word and exits 2.  Two tests against a
stand-in for llama-server's two doors on a free port, in a thread —
the fixture rule, the stand-in built and the live llm never touched
from this seat, where `launch.sh llm check` says *not said from this
seat*.  So the live conversation is his hand: `tools/launch.sh ask run`
from his shell, the tick serving the llm, the answer in `ask/state/answer`,
and the panel showing `ask  pulls — llm` and `llm  pulled by — ask`
while it runs.  What flows on the edge is still nothing; the talk goes
over the port beside it, which is what this card said an edge was.

**The live run, 15:25, from his shell — the edge worked and the talk
did not.**  `ask` took the edge at 15:25:49; the tick saw the lock and
started the llm at 15:26:11 — the first node ever started by a
process's pull on this desk — and llama-server died at its loader:
*libsvml.so: cannot open shared object file*, exit 127, on the andon
record.  The tick's unit carries `Environment=TEND_TREE` and nothing
else (`tools/install.sh`), so the oneAPI runtime that his shell puts on
`LD_LIBRARY_PATH` is not there for a runner the tick starts; from his
shell the same node loads.  This is `done/node-install.md`'s 07:10
leftover — *a per-machine grant does* — met by the first start that
was not from his shell.  The fix in the tree's grammar is one `env
LD_LIBRARY_PATH=…` line in `llm/grant`, the node carrying its own
runtime path (property 5's first half), and the directories are his to
name from the shell where it works.  And `ask` then waited its whole
300 s to say *never answered /health*, though the llm's death was in
`llm/state/stopped` the whole time, readable to it: fixed the same
hour — the puller reads the pulled node's `stopped`, and a death newer
than its edge ends the pull at once with the llm's own words and "pull
again once the cause is fixed" (rule 3 seen from the puller's side; a
puller under keep cannot re-assert).  Red first with a stand-in death,
`test_the_ask_node_reads_the_llms_death_from_its_state_and_stops_at_once`.
His "vedetyn solmun tilaa rajapintana" paid for itself within the hour
it was said.

**The second live run, 15:40 — the conversation happened.**  Henri put
the runtime's path into the node — `env LD_LIBRARY_PATH=…`, fourteen
oneAPI directories, in `llm/grant`, his hand — and ran `ask` again: the
edge at 15:40:55, the tick's llm loaded this time, ask asked, and
llama-server answered — *prompt 5 tokens, eval 200 tokens* in its log.
The whole 200 were gemma4's thinking under `--jinja`; `content` was
empty; ask printed `ask: ` and exited 0 as if answered, and his shell
showed nothing, because a runner's words go to its log.  So the edge,
the tick, the talk and the port all held, and what failed was the last
inch: reading the reply.  Fixed the same minute: ask reads `content`
and `reasoning_content` both (`card:private.md`'s two fields, the
courier's own reading since F016), keeps the thinking in `answer` under
its own rule, says *no answer — the llm thought for N words and the
token cap ended it* when that is what happened, and asks for 800 tokens
(`ASK_TOKENS`) instead of 200.  Red first against a stand-in that
thinks and does not answer.  The run that answers is the next one, his
shell again.

**The pulled node comes up at the lock, 15:50** — Henri: *"pystyisikö
vedetty solmu käynnistymään heti vedon jälkeen?  nyt siinä on viive."*
The tick's period was the edge's latency, up to 30 s, and this card's
§"What it must not become" had refused a scheduler.  The tree's own
rule resolves it: a pull from the person's side starts the runner at
once (`pull` from a shell does), and a puller's runner *is* on the
person's side.  So `run`, having made the edge files, forks one watcher
per edge that waits for the program to take the lock, asks `serve` once
for the pulled node, and is gone — the tick stays the carrier for
everything after (a death, a stop under a still-held edge).  Not a
scheduler: nothing loops or decides beyond the moment the lock is
taken.  The flow test no longer calls `serve` by hand: the die comes up
because the solitaire's runner asked, and the solitaire's log carries
the line.  Measured on the way: the watcher hands the pulled node the
puller's environment minus `TEND_STATE_DIR`, so a test that wants a
short idle on the pulled node says so in the puller's — the die ran its
grant's 30 s until the test did.
