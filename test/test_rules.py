"""The boot surface — what reaches a session before it asks for anything.

`AGENTS.md` and `CLAUDE.md` are that surface here: one line each,
pointing at `board/README.md`, which is the first thing to read.  The
gate refuses either of them growing past one line, because everything
they could grow into — rules, method, memory — has a home that is
loaded on purpose rather than unasked, and a boot surface that
accumulates is how a project ends up with rules nobody chose to read
(`~/gestate/spec/rules.md` is the shape that guards against it there).

**Why this file wears the name `test_rules.py` in a tree with no
`spec/rules.md`:** `~/gestate/tools/seedaudit.py` declares this path as
the boot surface's gate, and being findable by the instrument matters
more than a tidier name.  When the rules cap comes off the shelf
(`board/later/rules-and-memory.md`), its checks join this file.
"""

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent

#: Both spellings of the boot surface.  They must agree, because which
#: one a harness reads is the harness's choice, not the tree's.
BOOT = ["AGENTS.md", "CLAUDE.md"]


@pytest.mark.parametrize("name", BOOT)
def test_the_boot_surface_is_one_line(name):
    lines = [l for l in (ROOT / name).read_text(encoding="utf-8").splitlines()
             if l.strip()]
    assert len(lines) == 1, (
        f"{name} has grown to {len(lines)} lines.  The boot surface is one "
        "pointer; what it was about to say belongs behind board/README.md, "
        "where reading it is a choice.")


@pytest.mark.parametrize("name", BOOT)
def test_the_one_line_points_at_the_board(name):
    assert "board/README.md" in (ROOT / name).read_text(encoding="utf-8"), (
        f"{name} does not point at board/README.md, so a session boots "
        "without the one thing it was supposed to read first.")


def test_the_two_spellings_agree():
    a, b = ((ROOT / n).read_text(encoding="utf-8").strip() for n in BOOT)
    assert a == b, (
        "AGENTS.md and CLAUDE.md say different things, so what a session is "
        "told depends on which harness it arrived in.")
