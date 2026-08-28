# node-install — whether a node is installed cannot be known without running it

    status   open
    because  a node is a directory with a grant beside the program, and
             nothing says whether that directory can run on this machine
             short of running it.  On 2026-08-27 a grep found the tree's
             install test (`tools/toolbox.sh`) had said "everything
             required is here" while three of the launcher's and the llm
             node's load-bearing deps were undeclared — an install test
             that answered yes to an incomplete install.  The toolbox is
             tree-wide; a node's own needs (its program's binary, the
             paths its grant names, the model the person brings, the port
             it binds, the boundary it runs under) are read by nothing
             until `run`, which is the one thing a fenced session cannot
             do.  The real run is on the work laptop (memory: tiny model
             here, the run there), and the first question there is "is
             it installed?" — asked today of no mechanism
    asked    Henri, 2026-08-28 — "how about we work toward the easy to
             attain features today?" on doc/os-status-2026-08-26.md, and
             "we could write cards for these if they need cards, then
             proceed on implementing the first"
    see      spec/os.md property 2 — testing a program's installation
             should not be hard; doc/os-status-2026-08-26.md put it under
             "a simple solution is already here", and
             doc/os-status-2026-08-28.md says what moved since
             tools/launch.sh — the launcher reads the grant; a check is
             the same reading with nothing exec'd
             tools/toolbox.sh — the tree-wide half, completed 2026-08-27
             (card:work-environment-ai.md §"the toolbox manifest")
             tools/install.sh --check — the same question asked of the
             restraints, answered from the record beside the copies; the
             shape a node's check borrows
             card:keep.md (done/) — the boundary a node runs under, which
             refuses rather than run unconfined; a check asks it whether
             it is there before anything is run

## What it is

An install test for one node that runs nothing: read the grant the way
`run` would, and check each thing it names against the machine —
the program's binary is present, every `allow`/`write` path exists,
`$MODEL` resolves when the program line uses it, the state directory
can be written, the port in a `bind` line is free (or held by this
node's own runner), and keep's boundary is available at the ABI it
needs.  One line per finding, ✓ or ✗, and an exit code; the
`tools/install.sh --check` shape, on a node.  Inside the fence a session
can run it — reading is what a session is allowed — so "is it
installed?" is answerable from where the question is asked.

## What would make this card wrong

If `launch.sh NODE grant` and `tools/toolbox.sh` together already
answer the question.  They do not: `grant` prints what keep would be
handed and checks nothing; the toolbox declares the tree's needs and
knows no node's.  Or if every node's install fails loudly and early on
`run` anyway — it does (keep refuses, the program says no such file) —
but only on `run`, from the person's side, after a pull that a session
can make and cannot see answered.

## What it must not become

* **A second toolbox.**  The tree-wide declarations stay in
  `toolbox.sh`; a node's check reads its own grant and nothing else.
* **A run in disguise.**  Nothing is exec'd under the grant — a check
  that runs the program to see if it runs is `run` with a worse name.
* **Provenance.**  Property 5's "recorded in the node, from wherever it
  came" is the store's territory (`doc/os-status-2026-08-28.md`); a
  check says whether the node can run here, not where it came from.

## Where it sits

Placed last by the session that wrote it, at Henri's word, below the
open builds; the tiebreak is his.  Day one is the check itself, which
is the whole of §"What it is", with each ✗ shown red before trusted.

## 2026-08-28 — day one: `launch.sh NODE check`, and its first run found its own false ✗

Built the hour the card was written.  `tools/launch.sh NODE check`
reads the grant exactly as `run` does and execs nothing: the program's
binary (PATH or absolute), every `allow`/`write` path, `$MODEL` when
the program or status line uses it, the state directory, the `bind`
port (free, or held by this node's own runner — the lock says which),
and keep's Landlock ABI against what the grant needs (4 for
`no-net`/`bind`, 1 otherwise).  One ✓/✗ per line, exit 1 on any ✗.
Six tests in `test/test_launch.py`, each ✗ asserted red before its ✓:
a missing binary, a missing path, a missing model, a port held by a
test socket, and nothing written to the state by a check.

**The first run on the real nodes said ✗ where the fence was.**  From
this fenced session, `check` on both nodes reported *state … is not
writable by you* — true, and by design: `tools/sandbox.sh` binds a
node's state read-only to a session with the pull file as the one
write, and the runner writes the state from the person's side.  A
check that reads as `run` reads had inherited `run`'s seat without
saying so.  Fixed the same minute: inside the fence a read-only state
is a `·` line ("read-only to a session (the fence); the runner writes
it from the person's side — not checked from here"), outside it stays
a ✗; a test holds both sides.  After it: `llm check` — *installed: llm
can run under its grant on this machine* (llama-server on PATH, the
model present, 18080 free, ABI 4); `node check` the same.  The work
laptop's first line is now `tools/launch.sh llm check`, from wherever
the question is asked.

What day one does not do: provenance (§"What it must not become"),
and a check of what the program itself needs beyond its binary — a
shared library, a second binary it shells out to — which is the
toolbox's kind of knowledge and not the grant's.  The card stays open
until the check has been run on the machine it was built for.
