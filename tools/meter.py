#!/usr/bin/env python3
#: asked-by: Henri, 2026-09-04 — "Me tarvittaisiin numeroita mittaamaan että kehitystä tapahtuu" (card:meter.md)
"""tools/meter.py — the tree's own counts, by week, read from what it already keeps.

    tools/meter.py                 one row per ISO week, oldest first
    tools/meter.py --by day        one row per day
    tools/meter.py --root PATH     another tree (the test's fixture)

Reads, and never writes: `doc/kaizen/` (a file per sitting), the
`**Wrong, mine.**` paragraph in each, `doc/ingested.md`'s verdict per
kaizen, `fixme/` and its `status` dates, the board's `asked` and
`status` dates, `git log` for commits and for the day an F-number's
file arrived, and the failure ledger (`tools/suite.py`,
`~/.local/state/tend/failed.log`, TEND_FAILED_LOG).

**Every number is read from a file by this program**; none is a
session's sentence about itself, except the one column that is exactly
that — `wrong`, the first word of a paragraph a session wrote — and
the table's footer says how many kaizens it could not read that way.
A kaizen with no such paragraph is *not counted*, never zero.  The
`henri` column is his: a line `henri: N` (1–5) in the sitting's kaizen,
written before this is run.

Card: `card:meter.md`.  What this is not: a target, a lamp, a gate.
"""

import argparse
import collections
import datetime
import os
import re
import statistics
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
KAIZEN = re.compile(r"^(\d{4}-\d{2}-\d{2})-\d{4}\.md$")
FIELD = re.compile(r"^ {4}(\w+)\s{2,}(.*)$")
INGESTED = re.compile(r"^\| (\d{4}-\d{2}-\d{2}-\d{4}) \|.*\| `(\w+)`")
HENRI = re.compile(r"^henri:\s*([1-5])\b", re.M)
PAREN = re.compile(r"\((\d+)\)")
DOTTED = re.compile(r"(?:^|\s)(\d+)\.\s")
LEDGER = re.compile(r"^(\d{4}-\d{2}-\d{2}) \d\d:\d\d\s+(\w+)\s")
WORDS = {"none": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
         "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}


def ledger_path():
    return os.environ.get("TEND_FAILED_LOG") or os.path.join(
        os.path.expanduser("~"), ".local", "state", "tend", "failed.log")


def date(s):
    return datetime.date.fromisoformat(s)


def first_date(text):
    found = DATE.search(text or "")
    return date(found.group(0)) if found else None


def header(path):
    out = {}
    seen = False
    for line in path.read_text(encoding="utf-8").splitlines():
        found = FIELD.match(line)
        if found:
            seen = True
            out[found.group(1)] = found.group(2).strip()
        elif seen and not line.strip():
            break
    return out


def wrong_count(text):
    """The `**Wrong, mine.**` paragraph's count, or None when it cannot be read.

    Markers win — `(1) … (4)` or `1. … 3.` — then the paragraph's first
    word as a number word (`None.`, `Two.`).  A paragraph that opens with
    prose is not counted; that is the footer's line, not a zero here.
    """
    lines = text.splitlines()
    start = next((i for i, l in enumerate(lines) if l.startswith("**Wrong, mine")), None)
    if start is None:
        return None
    para = []
    for line in lines[start:]:
        if not line.strip():
            break
        para.append(line)
    body = " ".join(para)
    body = body[body.index("**", 2) + 2:] if body.count("**") >= 2 else body
    marks = [int(m) for m in PAREN.findall(body)]
    if marks and sorted(marks) == list(range(1, len(marks) + 1)):
        return len(marks)
    marks = [int(m) for m in DOTTED.findall(body)]
    if marks and sorted(marks) == list(range(1, len(marks) + 1)):
        return len(marks)
    first = re.match(r"\s*([A-Za-z]+)", body)
    if first and first.group(1).lower() in WORDS:
        return WORDS[first.group(1).lower()]
    return None


def git(root, *args):
    try:
        out = subprocess.run(["git", "-C", str(root), *args],
                             capture_output=True, text=True)
    except OSError:
        return ""
    return out.stdout if out.returncode == 0 else ""


def gather(root):
    root = Path(root)
    k = {"kaizens": [], "fixme": [], "cards": [], "commits": collections.Counter(),
         "reds": collections.defaultdict(collections.Counter)}

    verdicts = {}
    ingested = root / "doc" / "ingested.md"
    if ingested.is_file():
        for line in ingested.read_text(encoding="utf-8").splitlines():
            found = INGESTED.match(line)
            if found:
                verdicts[found.group(1)] = found.group(2)

    for path in sorted((root / "doc" / "kaizen").glob("*.md")):
        found = KAIZEN.match(path.name)
        if not found:
            continue
        text = path.read_text(encoding="utf-8")
        his = HENRI.search(text)
        k["kaizens"].append({
            "date": date(found.group(1)),
            "wrong": wrong_count(text),
            "verdict": verdicts.get(path.stem),
            "henri": int(his.group(1)) if his else None,
        })

    arrived = {}
    day = None
    for line in git(root, "log", "--diff-filter=A", "--no-renames",
                    "--format=%x01%as", "--name-only", "--", "fixme").splitlines():
        if line.startswith("\x01"):
            day = date(line[1:])
        elif line.strip() and day:
            stem = Path(line).stem
            if stem not in arrived or day < arrived[stem]:
                arrived[stem] = day
    for shelf in ("", "resolved"):
        for path in sorted((root / "fixme" / shelf).glob("F*.md")):
            fields = header(path)
            status = fields.get("status", "")
            opened = arrived.get(path.stem) or first_date(fields.get("seen", ""))
            resolved = first_date(status) if status.startswith("resolved") else None
            if opened:
                k["fixme"].append({"opened": opened, "resolved": resolved})

    board = root / "board"
    for shelf in ("", "done", "later"):
        for path in sorted((board / shelf).glob("*.md")):
            if path.name == "README.md":
                continue
            fields = header(path)
            opened = first_date(fields.get("asked", ""))
            status = fields.get("status", "")
            done = first_date(status) if status.startswith("done") else None
            if opened:
                k["cards"].append({"opened": opened, "done": done})

    for line in git(root, "log", "--format=%as").splitlines():
        if line.strip():
            k["commits"][date(line.strip())] += 1

    try:
        with open(ledger_path(), errors="replace") as f:
            for line in f:
                found = LEDGER.match(line)
                if found:
                    k["reds"][date(found.group(1))][found.group(2)] += 1
    except FileNotFoundError:
        pass
    return k


def period(day, by):
    return day if by == "day" else day - datetime.timedelta(days=day.weekday())


def rows(k, by):
    keys = set()
    for x in k["kaizens"]:
        keys.add(period(x["date"], by))
    for x in k["fixme"]:
        keys.add(period(x["opened"], by))
        if x["resolved"]:
            keys.add(period(x["resolved"], by))
    for x in k["cards"]:
        keys.add(period(x["opened"], by))
        if x["done"]:
            keys.add(period(x["done"], by))
    for d in list(k["commits"]) + list(k["reds"]):
        keys.add(period(d, by))
    out = []
    for p in sorted(keys):
        ks = [x for x in k["kaizens"] if period(x["date"], by) == p]
        readable = [x["wrong"] for x in ks if x["wrong"] is not None]
        read = [x for x in ks if x["verdict"]]
        recurs = sum(1 for x in read if x["verdict"] == "recurs")
        his = [x["henri"] for x in ks if x["henri"] is not None]
        f_open = sum(1 for x in k["fixme"] if period(x["opened"], by) == p)
        f_done = [x for x in k["fixme"] if x["resolved"] and period(x["resolved"], by) == p]
        c_open = sum(1 for x in k["cards"] if period(x["opened"], by) == p)
        c_done = [x for x in k["cards"] if x["done"] and period(x["done"], by) == p]
        commits = sum(n for d, n in k["commits"].items() if period(d, by) == p)
        gate = sum(c["gate"] for d, c in k["reds"].items() if period(d, by) == p)
        hand = sum(c["hand"] for d, c in k["reds"].items() if period(d, by) == p)
        out.append({
            "period": p,
            "sittings": len(ks),
            "commits": commits,
            "wrong": f"{sum(readable)} ({len(readable)} read)" if readable else "·",
            "recurs": f"{recurs} of {len(read)}" if read else "·",
            "fixme": f"+{f_open} −{len(f_done)}" + _days([(x["resolved"] - x["opened"]).days for x in f_done]),
            "cards": f"+{c_open} −{len(c_done)}" + _days([(x["done"] - x["opened"]).days for x in c_done]),
            "reds": f"{gate}/{hand}",
            "henri": f"{statistics.mean(his):.1f}" if his else "·",
        })
    return out


def _days(ds):
    return f" ({statistics.median(ds):g} d)" if ds else ""


def footer(k):
    unread = sum(1 for x in k["kaizens"] if x["wrong"] is None)
    not_ingested = sum(1 for x in k["kaizens"] if not x["verdict"])
    yield f"not counted from here: {unread} of {len(k['kaizens'])} kaizens have no `Wrong, mine` paragraph that opens with a count"
    yield f"not counted from here: {not_ingested} of {len(k['kaizens'])} kaizens have no verdict in doc/ingested.md yet"
    yield "not counted from here: a `--no-verify` commit leaves no line the tree can read (F021 was two)"
    yield "days on F and cards are the median from the file's first commit, or `asked`, to the `status` date; `shake` reds are a deliberate act and are left out"


def render(k, by):
    head = ["week" if by == "week" else "day", "sittings", "commits", "wrong",
            "recurs", "F +/−", "cards +/−", "reds gate/hand", "henri"]
    lines = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    for r in rows(k, by):
        lines.append("| " + " | ".join(str(r[c]) for c in
                     ("period", "sittings", "commits", "wrong", "recurs",
                      "fixme", "cards", "reds", "henri")) + " |")
    lines.append("")
    lines.extend(footer(k))
    return "\n".join(lines) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--by", choices=("week", "day"), default="week")
    ap.add_argument("--root", default=str(ROOT))
    args = ap.parse_args(argv)
    sys.stdout.write(render(gather(args.root), args.by))
    return 0


if __name__ == "__main__":
    sys.exit(main())
