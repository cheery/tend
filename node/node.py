#!/usr/bin/env python3
"""node.py — the first program tend runs, not a program that governs it.

A node opens where it was left, runs while something pulls it, and quits
by itself when nothing does (spec/os.md items 8, 9, 13; board/pull.md).
Its state is a plain JSON file a person can read without it; its work is
to serve pulls — count them, timestamp them, say so.  No manifest, no
broker, no language: the directory holding this file is the whole node.

    node.py run    [--idle S] [--poll S] [--state F]   run until pulls stop
    node.py pull                          [--state F]   one pull
    node.py status                        [--state F]   what it did

The stranger test, and nothing to read first: `node.py run --idle 3` in
one shell; `node.py pull` in another, a few times; stop, and watch run
exit on its own; then `node.py status`.  The pull signal is a plain
ledger beside the state file — a pull with no runner is simply not
served, which is the lifecycle, not an error.

  may not hang: the run loop always ends when the ledger goes quiet for
  --idle seconds, and the leash's wall budget bounds it besides (a node
  pulled past that budget is exit 124, a real interaction left for the
  grant that sizes the budget, not solved here).
  not silent (item 14): a corrupt state file raises rather than resets.
  a pull is served by the next runner, whenever it comes: the ledger is
  append-only and the state counts what was served, so a runner opening
  serves the difference first (board/resolver.md, 2026-08-26 — the
  resolver outside the fence starts the runner after the pull is written).
  one runner per state (board/resolver.md, the session half, measured
  2026-08-26): two `run`s on one state both opened, and each served the
  same pulls — the state was whichever wrote last.  So `run` takes
  `<state>.lock` and a second runner is refused, exit 75, out loud.
  The lock is the node's own and not the launcher's: however the node
  was started — pulled, or by a hand that bypassed the launcher — one
  state has one runner.
"""
import argparse
import fcntl
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_STATE = os.environ.get("TEND_NODE_STATE", os.path.join(HERE, "node.state"))


def fresh():
    return {"node": "tally", "generations": 0, "pulls": 0, "runtime_s": 0.0,
            "last_pull": None, "last_stop": None, "log": []}


def load(path):
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        return fresh()


def save(path, st):
    tmp = path + ".new"
    with open(tmp, "w") as f:
        json.dump(st, f, indent=2)
        f.write("\n")
    os.replace(tmp, path)  # atomic: a crash mid-write keeps the old state


def note(st, msg, cap=50):
    st["log"].append(time.strftime("%Y-%m-%d %H:%M:%S  ") + msg)
    del st["log"][:-cap]


def ledger(state):
    return state + ".pull"


def pulls_in(path):
    try:
        with open(path) as f:
            return sum(1 for _ in f)
    except FileNotFoundError:
        return 0


def cmd_pull(a):
    with open(ledger(a.state), "a") as f:
        f.write(str(int(time.time())) + "\n")
    print("pull: " + ledger(a.state))


def cmd_status(a):
    st = load(a.state)
    print(f"node {st['node']}: {st['pulls']} pulls over {st['generations']} "
          f"generations, {st['runtime_s']:.1f}s running")
    print("state: " + a.state)
    for line in st["log"][-5:]:
        print("  " + line)


def cmd_run(a):
    lock = open(a.state + ".lock", "a")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        print(f"node: another runner holds {a.state}.lock — pull it instead.", file=sys.stderr)
        sys.exit(75)
    st = load(a.state)
    st["generations"] += 1
    gen = st["generations"]
    note(st, f"gen {gen} opened at {st['pulls']} pulls, {st['runtime_s']:.1f}s")
    save(a.state, st)
    print(f"node: gen {gen}, state {a.state} — pull it, or it stops after "
          f"{a.idle}s idle")
    began = time.monotonic()
    # every pull the ledger holds that no runner has served — so a runner
    # started *after* a pull (by a resolver outside the fence, board/resolver.md)
    # serves it, rather than reading the ledger at open and serving only
    # what comes later.  Item 13, "starts by pull", made literal.
    seen = st["pulls"]
    last = began
    try:
        while True:
            time.sleep(a.poll)
            now = pulls_in(ledger(a.state))
            if now > seen:
                st["pulls"] += now - seen
                st["last_pull"] = time.time()
                note(st, f"served {now - seen}, total {st['pulls']}")
                save(a.state, st)
                print(f"node: pull, total {st['pulls']}")
                seen, last = now, time.monotonic()
            elif time.monotonic() - last >= a.idle:
                break
    finally:
        st["runtime_s"] += time.monotonic() - began
        st["last_stop"] = time.time()
        note(st, f"gen {gen} stopped, idle {a.idle}s")
        save(a.state, st)
    print(f"node: stopped — nobody pulled for {a.idle}s.  node.py status")


def main(argv=None):
    p = argparse.ArgumentParser(description="a node: pull it, or it stops")
    p.add_argument("--state", default=DEFAULT_STATE)
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run"); r.set_defaults(fn=cmd_run)
    r.add_argument("--idle", type=float, default=30.0)
    r.add_argument("--poll", type=float, default=0.2)
    sub.add_parser("pull").set_defaults(fn=cmd_pull)
    sub.add_parser("status").set_defaults(fn=cmd_status)
    a = p.parse_args(argv)
    a.fn(a)


if __name__ == "__main__":
    main()
