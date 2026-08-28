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

## 2026-08-28, 06:37 — the work laptop: the check ran, and said ✗ before anything ran

The card's next line was `tools/launch.sh llm check` on the machine
the node was built for.  Run from a fenced session at 06:37, one
minute into a 15-minute sitting, on Henri's "We've arrived to the
work laptop … there should be everything you need in place":

    ✓ grant parses; 6 keep words
    ✓ program llama-server → /usr/local/bin/llama-server
    ✗ allow /home/henri/tend/llm/model does not exist
    ✗ no *.gguf under /home/henri/tend/llm/model
    · state … read-only to a session (the fence); … not checked from here
    ✓ bind 18080 is free
    ✗ keep refuses this grant here — llm would not run
    NOT installed — the lines marked ✗ say what.

`node check` on the same machine: installed.  And `llm/state/log`,
written from the person's side at 06:36, holds the same refusal from
keep — *nothing to grant at '/home/henri/tend/llm/model'* — so the
runner had already paid the answer the check gives for free: the ✗ is
the same fact, read before the run instead of after it.  That is the
`because`, shown on the machine it was written about.

**What the check cannot see, and why.**  The model on this laptop is
wherever `~/qwen3.8-27B.sh` points, and inside the fence `~` is a
tmpfs with `tend`, `.local/state` and `.gitconfig` bound in and nothing
else: the script, and the `.gguf` it names, are not in the session's
seat.  The check's ✗ is therefore honest and not yet actionable from
here — the fix is one line of the person's, outside the fence:

    mkdir -p ~/tend/llm/model && ln <the .gguf the script names> ~/tend/llm/model/

A **hard link**, not a symlink: keep's Landlock rule is `path_beneath`
on `llm/model`, and the kernel resolves a symlink to its target before
the rule is checked, so a link into `~/models/…` would be refused at
open with the grant looking correct.  `~` and `~/tend` are one
filesystem here, so the link costs nothing.  Then `tools/launch.sh llm
check` again, then `run`.

**One thing the check does not know**: the grant's program line is
`-c 2048 -t 2` with no GPU offload, which is the tiny-model shape from
the other machine.  If the script here passes `-ngl` or a larger
context, the grant's line is the one that runs, and the difference is
the person's to settle in `llm/grant` — the check reads the grant, and
only the grant.

**The tree-wide half, on the same machine**: `tools/toolbox.sh` at
06:38 — everything required present but `pytest` (*install:
python3-pytest*).  Henri installed it within minutes, and the suite's
first run here was **43 failed, 11 errors, 303 passed** on one root
cause: every fixture that commits set `user.name` and inherited the
rest of his live `~/.gitconfig` — `commit.gpgsign = true` with an SSH
key the fence keeps out by design (`tools/sandbox.sh` probes that
`~/.ssh` does not exist).  The fixture rule's fifth face, on a machine
the fixtures had never met: `test/conftest.py` now gives every test an
empty git config and an identity of its own — 357 passed after it.
The one left, `test_mutate`, is a `.venv` made without pytest sitting
first on PATH; the same thing refuses the gate, so this note waits on
`.venv/bin/pip install pytest` from outside.  Two install tests, two
seats, one morning: the node's says the model, the tree's says pytest,
and neither ran anything to find out — and the suite, which does run
things, found the third: the person's git config in the tests' seat.

**06:52 — the model arrived, the check said *installed*, and it was
wrong.**  Henri hard-linked `gemma-4-26B-A4B-it-UD-Q4_K_XL.gguf` into
`llm/model/` (17 GB, 2 links) and the check went green on every line —
and `/usr/local/bin/llama-server --version` could not start: *error
while loading shared libraries: libsvml.so*.  The build is Intel-LLVM
(SYCL), and its runtime — twelve libraries: MKL, SYCL, TBB, dnnl, svml,
imf, iomp5, intlc, irng — lives where oneAPI installs for a user, in
his home, which the fence does not bind.  *Present is not loadable*, and
day one had named exactly this gap as the toolbox's kind of knowledge;
it is not — a program's libraries are the program's own need, read from
the binary by `ldd` without running any of it.  `check` now has the
line, ✓ *program loads* / ✗ *cannot load — not found by the loader:
…*, with the caveat in the code that it reads with the check's
`LD_LIBRARY_PATH`, which is the check's seat and may not be the
runner's.  Red first: a test builds a binary against a library, deletes
the library, and asks.  And the two tests that run the real second node
had guarded on *binary on PATH and model present* — less than the check
asks — so the moment the model arrived they ran a server that could not
load; they now ask the check.  `llm/bin/` — his SYCL build beside the
model — is gitignored like the model is.

What the runner needs on this machine is now the ✗ line's list, and it
is the grant's business twice over: the libraries must be on the
runner's `LD_LIBRARY_PATH`, and under keep's Landlock they must also be
*readable* — `SYSTEM_READ` covers `/usr` and `/lib*`, not a home
directory — so an `allow` on the oneAPI lib directory belongs in
`llm/grant` on this machine, or the runtime goes where `SYSTEM_READ`
already looks.  Henri's to settle; the check will say when it is.

The card stays open: it closes when the check says *installed* here
and the run that follows agrees.
