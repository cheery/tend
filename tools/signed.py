#!/usr/bin/env python3
#: asked-by: Henri, 2026-09-23 — "Build the done-when gate first then." (card:done-when.md)
"""tools/signed.py — no change to a program lands on a goal he has not signed.

    tools/signed.py MSGFILE     what the commit-msg hook runs: 0 lands, 1 refuses and says why

card:done-when.md, whose `done` line he signed 2026-09-07: "no change to
the tree's programs can land on a card whose definition of done Henri
has not signed."  A commit that changes a program — a path under
tools/, test/, node/ or kude/, or any .py or .sh — lands only if its
message cites a `card:NAME.md` whose `done` line carries `henri:` and
his words, or an F-number on either shelf of fixme/: a defect has its
own ledger and its own red.  A commit of cards, specs, kaizens and the
journal is not gated — that is the work that should come first.

It reads presence, never clarity: a signature and a citation, not the
sentence.  The sentence is his.  And `git commit --no-verify` passes it,
as it passes the pre-commit gates; the body says which gate was skipped.

The same reader answers `test/test_board.py`, which refuses a card at
`doing` whose `done` line is unsigned — so the two gates meet at the
moment a card starts: its goal signed, or it does not start.
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIELD = re.compile(r"^ {4}(\w+)\s{2,}(.*)$")
CONTINUED = re.compile(r"^ {5,}(\S.*)$")
SIGNATURE = re.compile(r"henri:\s*[^\s)]")
PROGRAM_DIRS = ("tools/", "test/", "node/", "kude/")
PROGRAM_ENDINGS = (".py", ".sh")
CARD = re.compile(r"card:([\w-]+\.md)")
DEFECT = re.compile(r"(?<![A-Za-z0-9_/:-])F(\d{3})(?![A-Za-z0-9_.-]|\.md)")   # test_fixme.py's CITE
SHELVES = ("board", "board/done", "board/later")


def field(text, name):
    """A card's header field, continuation lines joined — the header is the
    block of `    name  value` lines the card opens with, ending at the
    first blank line after it."""
    fields, current, seen = {}, None, False
    for line in text.splitlines():
        found = FIELD.match(line)
        if found:
            seen, current = True, found.group(1)
            fields[current] = found.group(2).strip()
        elif seen and not line.strip():
            break
        elif current and CONTINUED.match(line):
            fields[current] += " " + line.strip()
    return fields.get(name, "")


def is_signed(done):
    """His hand on a goal: `henri:` followed by something of his."""
    return bool(SIGNATURE.search(done))


def programs(staged):
    return [p for p in staged if p.startswith(PROGRAM_DIRS) or p.endswith(PROGRAM_ENDINGS)]


def verdict(message, staged):
    """None if the commit lands, or the reasons it does not."""
    changed = programs(staged)
    if not changed:
        return None
    for number in DEFECT.findall(message):
        if (ROOT / "fixme" / f"F{number}.md").exists() or (ROOT / "fixme" / "resolved" / f"F{number}.md").exists():
            return None
    reasons = []
    for name in dict.fromkeys(CARD.findall(message)):
        found = next((ROOT / s / name for s in SHELVES if (ROOT / s / name).exists()), None)
        if found is None:
            reasons.append(f"card:{name} — no such card on any shelf")
        elif is_signed(field(found.read_text(encoding="utf-8"), "done")):
            return None
        else:
            reasons.append(f"card:{name} — its `done` line is not signed")
    if not reasons:
        reasons.append("the message cites no card and no F-number")
    return changed, reasons


def main(argv):
    if len(argv) != 1:
        print(__doc__.split("\n\n")[1], file=sys.stderr)
        return 2
    message = "\n".join(l for l in Path(argv[0]).read_text(encoding="utf-8").splitlines()
                        if not l.startswith("#"))
    staged = subprocess.run(["git", "diff", "--cached", "--name-only"], cwd=ROOT,
                            capture_output=True, text=True, check=True).stdout.split()
    found = verdict(message, staged)
    if found is None:
        return 0
    changed, reasons = found
    shown = "\n".join(f"    {p}" for p in changed[:8]) + (f"\n    … and {len(changed) - 8} more" if len(changed) > 8 else "")
    print(f"""
signed: refused — this commit changes a program:
{shown}

  and {'; '.join(reasons)}.

  A change to a program lands on a goal he has signed (card:done-when.md):
  cite a `card:NAME.md` whose `done` line carries `henri:` and his words,
  or an F-number from fixme/.  If the card's line is a draft, the next
  step is his hand on it, not this commit.

  To commit anyway: git commit --no-verify, and say in the body which
  gate you skipped.
""", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
