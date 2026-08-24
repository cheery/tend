"""No `pgrep -f` or `pkill -f` in this tree matches its own line.

**The countermeasure for a bug made twice.**  Gestate, 2026-08-18:
`pgrep -f "no:randomly"` matched the watcher's own command line, so
every wait loop waited for itself and twelve polling shells
accumulated on the machine being listened on.  Tend, 2026-08-24: a
session that had read that entry an hour earlier ran `pkill -f 'while
:; do'` and killed the shell running it.  Reading a post-mortem does
not install the reflex; a gate does, for everything that lands in the
tree.  What it cannot reach — a pattern a session types into a shell
by hand — is why `tools/leash.sh` kills by scope and never by
pattern, and why the honest countermeasure for the ad-hoc case is to
reach for that instead.

The guard is the bracket: `'[w]hile'` matches `while` and does not
match the literal `[w]hile` sitting in the caller's own command line.
"""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent

#: `pgrep -f PATTERN` / `pkill -f PATTERN`, with any flags between and
#: `-f` possibly bundled (`-af`), capturing the pattern's first
#: character after an optional quote.  The bundled form was the
#: detector's own first miss: `pgrep -af '[p]ytest'` is exactly what
#: the session typed, and the first regex read `-af` as not `-f`.
CALL = re.compile(r"""\bp(?:grep|kill)\b(?:\s+-\S+)*?\s+-\w*f\s+["']?(.)""")

#: Where a pattern would be run by this tree rather than quoted by it.
SCANNED = ["tools", "test"]


def sources():
    """Every shell and Python file under the scanned directories, except
    this one — it quotes the unguarded shape in order to test the
    detector, the same exemption `seedaudit.py` gives its own test."""
    return sorted(p for d in SCANNED for p in (ROOT / d).rglob("*")
                  if p.suffix in (".sh", ".py") and p.is_file()
                  and p.name != "test_selfmatch.py")


@pytest.mark.parametrize("path", sources(), ids=lambda p: p.name)
def test_every_pattern_kill_is_bracket_guarded(path: Path):
    bad = []
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.lstrip().startswith("#"):
            continue
        for m in CALL.finditer(line):
            first = m.group(1)
            if first not in "[$":          # a bracket, or a variable the caller guarded
                bad.append(f"{path.relative_to(ROOT)}:{n}: {line.strip()}")
    assert not bad, (
        "a pattern kill that can match its own command line — bracket the "
        "first character ('[w]hile'), or kill by scope/group instead:\n  "
        + "\n  ".join(bad))


def test_the_detector_sees_an_unguarded_one():
    """An oracle that has only ever passed is a claim (`manifesto.md`)."""
    assert CALL.search('pgrep -f "no:randomly"').group(1) == "n"
    assert CALL.search("pkill -TERM -f '[s]leep 3'").group(1) == "["
    assert CALL.search('pgrep -af "$marker"').group(1) == "$"
