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

`for him` is the keeper's queue (Henri, 2026-09-04: "Alan ymmärtää miten
vaikeaa keeperin rolli on.  Se vaatii että on hereillä ja hyvin") — the
self-shaped marks and `his call` questions keeper.md's two greps find,
placed by the date the mark carries or git's blame of its line, struck
by the date in his `henri:` answer; the footer says how many wait and
since when.  A mark waiting is a session's boundary nobody has stood
behind yet, which is what the tree looks like when he is not there.

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
# a ledger row: the kaizen's name in the first cell; the verdict is the first backticked word of
# the LAST cell — `rule`, `open — card:x.md` (the where inside the backticks), **`promoted` — …**
# (bold first) — and the last cell because a phrase has carried a bare pipe twice, which makes a
# fourth cell.  F025 (2026-09-04): the first form of this wanted `word` closed by a backtick right
# after the third cell's pipe, and seven of 110 rows were counted as never ingested
INGESTED = re.compile(r"^\| (\d{4}-\d{2}-\d{2}-\d{4}) \|(.*)$")
VERDICT_CELL = re.compile(r"\**`(\w+)")
HENRI = re.compile(r"^henri:\s*([1-5])\b", re.M)
PAREN = re.compile(r"\((\d+)\)")
DOTTED = re.compile(r"(?:^|\s)(\d+)\.\s")
LEDGER = re.compile(r"^(\d{4}-\d{2}-\d{2}) \d\d:\d\d\s+(\w+)\s")
#: keeper.md's two greps, as one: a mark or a question that is his to answer
#: a mark carries its date in its form; a question does not, and a date quoted in its
#: text is not its placing (edge.md:224 asks about a 2026-08-19 line) — git's blame is
FOR_HIM = re.compile(r"^\*\((?:self-shaped, (\d{4}-\d{2}-\d{2})|question, his call)\b")
VERDICT = re.compile(r"\bhenri:\s*(.+?)\s*\)?\*?\s*$", re.M)
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


def blamed(root, path, lineno):
    """The day a line was committed, by git's blame; None for an uncommitted line."""
    out = git(root, "blame", "-L", f"{lineno},{lineno}", "--porcelain", "--", str(path))
    found = re.search(r"^author-time (\d+)$", out, re.M)
    if not found:
        return None
    return datetime.datetime.fromtimestamp(int(found.group(1))).date()


def for_him(root):
    """[{placed, struck, where}] — every mark and his-call question keeper.md's greps find."""
    files = sorted(root.glob("*.md"))
    for name in ("board", "spec", "doc", "fixme"):
        files += sorted((root / name).rglob("*.md"))
    out = []
    for path in files:
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError:
            continue
        for i, line in enumerate(lines):
            found = FOR_HIM.match(line)
            if not found:
                continue
            end = i
            while end < len(lines) and ")*" not in lines[end]:
                end += 1
            text = "\n".join(lines[i:end + 1])
            placed = (date(found.group(1)) if found.group(1)
                      else blamed(root, path.relative_to(root), i + 1))
            struck = None
            said = VERDICT.search(text)
            if said:
                struck = first_date(said.group(1)) or blamed(root, path.relative_to(root), i + 1 + text[:said.start()].count("\n"))
            if placed:
                out.append({"placed": placed, "struck": struck,
                            "where": f"{path.relative_to(root)}:{i + 1}", "line": line})
    return out


def waiting(k):
    """--waiting: the marks and his-call questions with no `henri:` line, oldest first —
    keeper.md's two greps with the struck ones left out (Henri, 2026-09-04: "henri: approved
    rivit voisi merkata jotenkin ettei ne pomppaa kun hakee (self-shaped").  The grep stays
    the definition of a mark; this is the same list the meter's `for him` footer counts."""
    rows = sorted((x for x in k["him"] if not x["struck"]), key=lambda x: (x["placed"], x["where"]))
    if not rows:
        return "for him: nothing waiting for his hand\n"
    return "".join(f"{x['placed']}  {x['where']}  {x['line']}\n" for x in rows)


def gather(root):
    root = Path(root)
    k = {"kaizens": [], "fixme": [], "cards": [], "commits": collections.Counter(),
         "reds": collections.defaultdict(collections.Counter), "him": for_him(root)}

    verdicts = {}
    ingested = root / "doc" / "ingested.md"
    if ingested.is_file():
        for line in ingested.read_text(encoding="utf-8").splitlines():
            found = INGESTED.match(line)
            if found:
                cells = [c.strip() for c in found.group(2).strip().strip("|").split("|")]
                said = VERDICT_CELL.match(cells[-1]) if cells else None
                if said:
                    verdicts[found.group(1)] = said.group(1)

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
    for x in k["him"]:
        keys.add(period(x["placed"], by))
        if x["struck"]:
            keys.add(period(x["struck"], by))
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
        h_placed = sum(1 for x in k["him"] if period(x["placed"], by) == p)
        h_struck = [x for x in k["him"] if x["struck"] and period(x["struck"], by) == p]
        out.append({
            "him": f"+{h_placed} −{len(h_struck)}" + _days([(x["struck"] - x["placed"]).days for x in h_struck]),
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
    waiting = sorted((x for x in k["him"] if not x["struck"]), key=lambda x: x["placed"])
    if waiting:
        yield (f"for him: {len(waiting)} waiting for his hand, the oldest since {waiting[0]['placed']} "
               f"({waiting[0]['where']}) — keeper.md's two greps")
    else:
        yield "for him: nothing waiting for his hand"
    yield "days on F and cards are the median from the file's first commit, or `asked`, to the `status` date; `shake` reds are a deliberate act and are left out"


def render(k, by):
    head = ["week" if by == "week" else "day", "sittings", "commits", "wrong",
            "recurs", "F +/−", "cards +/−", "reds gate/hand", "for him +/−", "henri"]
    lines = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    for r in rows(k, by):
        lines.append("| " + " | ".join(str(r[c]) for c in
                     ("period", "sittings", "commits", "wrong", "recurs",
                      "fixme", "cards", "reds", "him", "henri")) + " |")
    lines.append("")
    lines.extend(footer(k))
    return "\n".join(lines) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--by", choices=("week", "day"), default="week")
    ap.add_argument("--root", default=str(ROOT))
    ap.add_argument("--waiting", action="store_true",
                    help="list the marks and his-call questions with no henri: line, oldest first, instead of the table")
    args = ap.parse_args(argv)
    if args.waiting:
        sys.stdout.write(waiting({"him": for_him(Path(args.root))}))
        return 0
    sys.stdout.write(render(gather(args.root), args.by))
    return 0


if __name__ == "__main__":
    sys.exit(main())
