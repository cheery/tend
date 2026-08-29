"""fixme/ — the defect ledger, held to its own contract (Henri, 2026-08-29: "we've reached a point where we need fixme/ -ledger").

A card is work to do; an F-number is something that is wrong.  The
shape is the board's: one file per defect, the filename its id
(`fixme/F000.md`), two shelves — `fixme/` for open, `fixme/resolved/`
for closed — a move never renames, and a citation is the bare id
(`F000`), which resolves on either shelf.  Presence, not wisdom: no
test can tell a symptom from a fix, but it can refuse an entry that
names neither, a number worn twice, a resolved entry with no date and
no gate, and a citation to no entry.
"""
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
FIXME = ROOT / "fixme"
SHELVES = [FIXME, FIXME / "resolved"]
ID = re.compile(r"^F\d{3}\.md$")
CITE = re.compile(r"(?<![A-Za-z0-9_/:-])F(\d{3})(?![A-Za-z0-9_.-]|\.md)")   # `gestate:F182` is another tree's


def entries():
    return sorted(p for s in SHELVES if s.is_dir() for p in s.glob("F*.md"))


def fields(p):
    out = {}
    for line in p.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^    (\w+)  +(.*)$", line)
        if m and m.group(1) not in out:
            out[m.group(1)] = m.group(2).strip()
        elif line and not line.startswith(" ") and out:
            break
    return out


def test_the_ledger_exists_with_both_shelves():
    assert (FIXME / "README.md").is_file() and (FIXME / "resolved").is_dir()


def test_every_entry_is_named_by_its_number_and_no_number_is_worn_twice():
    seen = {}
    for p in entries():
        assert ID.match(p.name), f"{p}: an entry is F<three digits>.md"
        assert p.name not in seen, f"{p.name} is on two shelves: {seen[p.name]} and {p}"
        seen[p.name] = p


@pytest.mark.parametrize("entry", entries(), ids=lambda p: p.name)
def test_every_entry_says_what_shows_and_where_it_was_seen(entry):
    f = fields(entry)
    for k in ("status", "shows", "seen"):
        assert k in f and f[k], f"{entry.name}: `{k}` is on every entry — `shows` is the symptom, in whose words; `seen` is when and where"
    assert f["status"].split(" ")[0] in ("open", "resolved"), entry.name


@pytest.mark.parametrize("entry", entries(), ids=lambda p: p.name)
def test_a_resolved_entry_is_on_the_resolved_shelf_says_when_and_names_its_gate(entry):
    f = fields(entry)
    resolved = f["status"].startswith("resolved")
    assert resolved == (entry.parent.name == "resolved"), f"{entry.name}: `resolved` lives in fixme/resolved/, `open` does not"
    if resolved:
        assert re.search(r"resolved — \d{4}-\d{2}-\d{2}", f["status"]), f"{entry.name}: resolved says when"
        # gestate's lesson (its ungated-fixes card): a defect closed on a photograph comes back
        # with nobody told — a resolved entry names the test that holds it, or says `none — why`
        assert f.get("gate"), f"{entry.name}: a resolved entry names its gate — a test id, or `none — <why>`"


# Citations older than the ledger, into gestate's fixme.md — accepted as written
# (a done card is history), and this set may shrink and never grow: gestate's own
# proposed shape for a rule applied only to what comes after it.  From the ledger's
# day on, another tree's number is written `gestate:F182`, which this regex skips.
BASELINE = {"board/done/green.md: F182"}


def test_every_f_citation_resolves_on_some_shelf():
    have = {p.stem for p in entries()}
    sources = entries() + [FIXME / "README.md", ROOT / "board" / "README.md"]
    sources += sorted((ROOT / "board").glob("*.md")) + sorted((ROOT / "board" / "done").glob("*.md")) + sorted((ROOT / "board" / "later").glob("*.md"))
    dangling = []
    for src in sources:
        if not src.is_file():
            continue
        for m in CITE.finditer(src.read_text(encoding="utf-8")):
            if f"F{m.group(1)}" not in have:
                dangling.append(f"{src.relative_to(ROOT)}: F{m.group(1)}")
    new = sorted(set(dangling) - BASELINE)
    assert not new, "a citation names an entry on no shelf:\n  " + "\n  ".join(new)
    gone = sorted(BASELINE - set(dangling))
    assert not gone, "a baseline citation is no longer there — shrink BASELINE:\n  " + "\n  ".join(gone)
