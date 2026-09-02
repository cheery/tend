#!/usr/bin/python3
#: asked-by: Henri, 2026-09-02 — "solmuun kuuluva prosessi voisi antaa 'pull' -käskyn, joka pysyy voimassa kunnes prosessi sanoo 'stop' tai lopettaa" (card:edge.md, day one)
"""solitaire — pull the die, read its roll, let go.

The near end of an edge.  The pull is a shared flock on the edge file
the launcher made and named in $TEND_PULLS (`die=/path/to/die/state/
pulled/solitaire`); it is in force until this process closes the fd
(`stop`) or exits, when the kernel drops it.  The conversation is the
die's `roll` file beside the signal — read, because `pull die` grants
read on the die's state and nothing else.
"""
import fcntl
import os
import pathlib
import sys
import time

pulls = dict(kv.split("=", 1) for kv in os.environ.get("TEND_PULLS", "").split())
edge = pulls.get("die")
if not edge:
    print("solitaire: the grant names no edge to die — `pull die` is the word (card:edge.md)", file=sys.stderr)
    sys.exit(2)
start = time.time()
fd = os.open(edge, os.O_RDONLY)
fcntl.flock(fd, fcntl.LOCK_SH)   # the pull: in force until `stop` (close) or exit
roll = pathlib.Path(edge).parent.parent / "roll"
deadline = start + float(os.environ.get("SOLITAIRE_WAIT", "60"))
while time.time() < deadline:
    try:
        if roll.stat().st_mtime >= start:   # a roll made for this pull, not a stale one
            break
    except FileNotFoundError:
        pass
    time.sleep(0.1)
else:
    print(f"solitaire: pulled die for {time.time() - start:.0f}s and it never rolled — is anything serving it?", file=sys.stderr)
    sys.exit(1)
print(f"solitaire: die rolled {roll.read_text().strip()}", flush=True)
os.close(fd)   # stop: the edge is let go before the exit, on purpose
