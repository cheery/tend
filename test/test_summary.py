"""`doc/summary/` — the two sheets cannot cite what is gone, nor keep a
claim the tree has outgrown.

The hard half of keeping the summary honest (the soft half is the lamp,
`tools/summary.sh`).  A summary is prose and prose cannot be tested for
truth — but it can be held to two things a test *can* check: that every
tree path it names still exists, and that its one claim about live state
still holds.  When either breaks, the gate refuses the commit until the
summary is reconciled, which is exactly the drift this directory exists
to prevent.
"""

import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
SUMMARY = ROOT / "doc" / "summary"
SHEETS = [SUMMARY / "rules.md", SUMMARY / "interfaces.md"]

#: A path cited in the summary is checked for existence only when it is
#: repo-relative — under one of these roots.  Host-side keys (`~/…`) and
#: runtime artifacts (`node/*.state`, the ledger) are named in the prose
#: but are not in the tree, so they are not existence-checked here.
TREE_ROOTS = ("tools/", "node/", "board/", "doc/", "spec/", "test/")


def cited_paths(text):
    """Repo-relative paths inside backticks.  A trailing slash means a
    directory; a glob (`*`) is a runtime artifact and is skipped."""
    out = set()
    for span in re.findall(r"`([^`]+)`", text):
        token = span.split()[0].strip()  # `-- cmd` and flags fall away
        if not token.startswith(TREE_ROOTS):
            continue
        if "*" in token:
            continue
        out.add(token)
    return out


def test_the_summaries_exist_and_have_the_printable_sheet():
    for f in SHEETS:
        assert f.is_file(), f
    assert (SUMMARY / "tend-sheets.html").is_file()
    assert (SUMMARY / "README.md").is_file()


def test_every_path_the_summary_cites_exists():
    """Rename or remove a tool and the sheet that names it goes red —
    the summary cannot point at something that is gone."""
    missing = {}
    for f in SHEETS:
        for p in cited_paths(f.read_text(encoding="utf-8")):
            target = ROOT / p
            ok = target.is_dir() if p.endswith("/") else target.exists()
            if not ok:
                missing.setdefault(f.name, []).append(p)
    assert not missing, f"summary cites paths that do not exist: {missing}"


def test_the_summary_names_the_real_tools():
    """The mechanisms table is only honest if it names tools that are
    there — a spot check that the citation extraction is doing its job,
    not matching nothing."""
    cited = cited_paths((SUMMARY / "rules.md").read_text(encoding="utf-8"))
    for expect in ("tools/fence.sh", "tools/leash.sh", "node/node.py"):
        assert expect in cited, f"{expect} is no longer named in rules.md"


def test_the_not_built_claim_still_holds():
    """The one live claim on the sheets: the andon is not built, `cords`
    is blocked.  If `cords` is finished (moves to done/) or unblocks, the
    interfaces sheet is stale by exactly that, and this makes it say so."""
    text = (SUMMARY / "interfaces.md").read_text(encoding="utf-8")
    assert "not built yet" in text.lower()
    assert (ROOT / "board" / "cords.md").is_file(), \
        "the sheet says cords is not built; if it moved, the sheet must too"
    assert not (ROOT / "board" / "done" / "cords.md").exists(), \
        "cords is done — update interfaces.md's 'Not built yet' section"
    status = subprocess.run(
        ["sed", "-n", "s/^    status *//p", str(ROOT / "board" / "cords.md")],
        capture_output=True, text=True).stdout.strip()
    assert status.startswith("blocked"), \
        f"cords is '{status}', not blocked — interfaces.md's andon section is stale"


def test_the_lamp_parses_and_runs():
    lamp = ROOT / "tools" / "summary.sh"
    assert subprocess.run(["sh", "-n", str(lamp)]).returncode == 0
    out = subprocess.run(["sh", str(lamp), "--hook"], capture_output=True, text=True)
    assert out.returncode == 0, "the lamp is a lamp, never a refusal"
