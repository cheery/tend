#!/usr/bin/python3
#: asked-by: Henri, 2026-09-02 — "Ensimmäinen solmu joka ei ole LLM... se voisi olla vaikkapa solitaire -ohjelma, tai digitaalinen noppa" (card:edge.md, day one)
"""die — roll once into the state, then wait to be let go.

The far end of an edge.  Its whole conversation is one file, `roll`,
beside the signal: a puller with read on this state reads it.  The
program never stops itself; the launcher stops it when nothing pulls
(`idle`), which is the thing being tested.
"""
import os
import pathlib
import random
import sys
import time

state = pathlib.Path(sys.argv[sys.argv.index("--state") + 1])
roll = state / "roll"
new = state / "roll.new"
new.write_text(f"{random.randint(1, 6)}\n")
os.replace(new, roll)   # one rename, so a reader never sees half a roll
print(f"die: rolled {roll.read_text().strip()}", flush=True)
while True:
    time.sleep(3600)
