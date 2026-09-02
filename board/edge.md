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
canvas as a node at the sink, or something that pulls the llm?)*

## Where it sits

Placed last by the session that wrote it, at his "tee sille kortti";
the tiebreak is his.
