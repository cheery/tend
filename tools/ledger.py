#!/usr/bin/env python3
#: asked-by: Henri, 2026-08-26 — "you could work on the keep and resolver" (the ledger's second read; doc/kaizen/2026-08-26-1342.md: on the second ask the parser is a tool)
"""tools/ledger.py — read the leash ledger by record, not by line.

    tools/ledger.py [summary]            counts: records, modes, exits, cpu
    tools/ledger.py grep REGEX           the records whose command matches
    tools/ledger.py since 'YYYY-MM-DD HH:MM' [grep REGEX]

The ledger (`tools/leash.sh`, ~/.local/state/tend/leash.log) is one
tab-separated line per invocation — epoch, seconds, exit, budget, cpu,
command — except that the command is the whole shell text and spans
lines when it carried a heredoc.  A record therefore starts where a
line starts with an epoch and a tab, and runs until the next such line.
A line-based count is wrong before it is printed: the first one made
here said 2978 commands for a sitting of 53 (the kaizen above).

Read-only.  Prints; never writes the ledger.
"""
import collections
import os
import re
import sys
import time

LOG = os.environ.get("TEND_LEASH_LOG", os.path.expanduser("~/.local/state/tend/leash.log"))
HEAD = re.compile(r"^\d{9,10}\t")


def records(path=LOG):
    """[(epoch, seconds, exit, budget, cpu_s or None, command)], oldest first."""
    out = []
    try:
        f = open(path, errors="replace")
    except FileNotFoundError:
        return out
    with f:
        for line in f:
            line = line.rstrip("\n")
            if HEAD.match(line):
                p = line.split("\t", 5)
                if len(p) == 6:
                    out.append(p)
                    continue
            if out:
                out[-1][5] += "\n" + line
    recs = []
    for e, s, x, b, c, cmd in out:
        m = re.search(r"cpu=([\d.]+)s", c)
        recs.append((int(e), int(s), x, b, float(m.group(1)) if m else None, cmd))
    return recs


def mode(r):
    return "scope" if "scope" in r[3] else ("plain" if "plain" in r[3] else "other")


def summary(recs):
    if not recs:
        print("ledger: no records"); return
    modes = collections.Counter(mode(r) for r in recs)
    exits = collections.Counter(r[2] for r in recs)
    cpu = [r[4] for r in recs if r[4] is not None]
    print(f"records  {len(recs)}   from {time.strftime('%F %T', time.localtime(recs[0][0]))} "
          f"to {time.strftime('%F %T', time.localtime(recs[-1][0]))}")
    print("modes    " + "  ".join(f"{k}={v}" for k, v in modes.most_common()))
    print("exits    " + "  ".join(f"{k}×{v}" for k, v in exits.most_common(6)))
    print(f"wall     {sum(r[1] for r in recs)}s total, longest {max(r[1] for r in recs)}s")
    if cpu:
        print(f"cpu      {sum(cpu):.1f}s total, {sum(1 for c in cpu if c > 0)} of {len(cpu)} records > 0, "
              f"largest {max(cpu):.1f}s")


def show(recs):
    for e, s, x, b, c, cmd in recs:
        head = re.sub(r"\s+", " ", cmd)[:100]
        print(f"{time.strftime('%F %T', time.localtime(e))}  {s:>4}s  exit {x:<3}  "
              f"cpu={'-' if c is None else f'{c:.1f}'}  {head}")


def main(argv):
    recs = records()
    i = 0
    if i < len(argv) and argv[i] == "since":
        if i + 1 >= len(argv):
            sys.stderr.write("ledger: since needs 'YYYY-MM-DD HH:MM'\n"); return 2
        t = time.mktime(time.strptime(argv[i + 1], "%Y-%m-%d %H:%M"))
        recs = [r for r in recs if r[0] >= t]; i += 2
    if i < len(argv) and argv[i] == "grep":
        if i + 1 >= len(argv):
            sys.stderr.write("ledger: grep needs a regex\n"); return 2
        rx = re.compile(argv[i + 1])
        recs = [r for r in recs if rx.search(r[5])]
        show(recs); print(f"-- {len(recs)} records"); return 0
    if i < len(argv) and argv[i] not in ("summary",):
        sys.stderr.write(f"ledger: unknown argument `{argv[i]}`\n"); return 2
    summary(recs); return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
