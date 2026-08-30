# cords-crate — the second program tend runs will copy the first's shell

    status   shelved — 2026-08-30
    because  a program tend runs has a contract with the tree and the
             contract is written nowhere a program can link to: the env
             words (`$NODE`, `$STATE`, `$MODEL`, `$IDLE`), the pulse
             file whose mtime is its activity, the stop and its reason
             in `$STATE/stopped`, the `status` line, the pin on the
             canvas — spread across `tools/launch.sh`'s header and
             `test/test_launch.py`.  The first program of tend's own was
             a shell script and the second (the llm node) is a foreign
             binary with the contract applied from outside; the third,
             written for this tree, will copy the first's lines by hand
             — and must still be an Ubuntu program when tend is absent,
             or the tree has made a dependency of itself, which is the
             thing it refuses (`systemd is the implementation, never
             the dependency`).  Henri, 2026-08-30: "writing a rust
             library for writing apps on this node network, such that
             they remain backward compatible with ubuntu linux."
    asked    Henri, 2026-08-30, ~10:40 — "put these into later/ as cards"
    blocked  waits on the second program that wants the first's code —
             the library is extracted from two programs that agree, not
             designed for none; `launch.sh` itself was three flags in
             `node/run.sh` until the second node wanted the same three.
             The first candidate is `card:canvas-windows.md`'s daemon.
             And before either, the contract in `spec/` as words the sh
             side and the Rust side both read, held by the launcher's
             tests — the spec is the deliverable that lasts; the crate
             is its Rust reading.
    see      tools/launch.sh (the header is the contract as it stands),
             card:keep.md and card:node-install.md (why static: `check`
             went red on the work laptop on a dynamically linked build
             whose library keep's boundary could not see — a static
             binary passes `check` and installs as one file),
             card:canvas-windows.md, card:hold-mirror.md (where an app
             writes on the person's side), spec/os.md properties 1, 2
             and 4 (bounded on its own interface; install testable;
             behaviour by types), manifesto.md rule 1

## What it is, when it comes

A `cords` crate, not a framework: a program links it and gets the
cooperation layer — read the env words, write the pulse, say why it
stopped, answer `status`, write its row on the canvas — **and every
one of those degrades to nothing or to XDG when tend is not there.**
`$STATE` unset means the program's state goes where an Ubuntu program's
goes and the pulse goes nowhere; the program runs the same.  Backward
compatible means: the grant is applied from outside (rule 1) and the
library is the program's *optional* half of the bargain, never the
condition of running.

Why Rust and not the shell the first program was written in: the
boundary measured it.  keep's Landlock lets a program read beneath the
system paths and the grant's, and a dynamically linked build that
wants a runtime elsewhere fails `check` — as the Intel-LLVM
llama-server did on 2026-08-28.  A static binary has nothing to want.
That is `spec/os.md` property 2 as a build flag.

## What it must not become

The way to write a node.  A node is a directory with a grant and a
program; the program may be sh, Python, a foreign binary, or Rust with
this crate, and the launcher must never know which.  If a Python node
becomes a second-class node because the crate exists, the crate has
become the dependency.  And not a tend SDK: nothing in it talks to the
resolver, the panel or a door; it writes files, as every program here
does.

## Where it sits

Shelved on arrival, 2026-08-30, at Henri's "put these into later/ as
cards"; placed after `card:canvas-windows.md`, whose daemon is the
program that would first want it.  The tiebreak is his.
