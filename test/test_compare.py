"""tools/compare.py — the led turn's two prompts, put to a Claude model (card:session-program.md, 2026-08-28 18:30).

Henri: "I have anthropic api key here.. you could try how sonnet or opus
fares in the task you've given to the local llm."  The seat cannot run
it (no key, no net inside the fence), so the tool runs on the person's
side; what is tested here is that it builds the same digest lead.sh
builds and reads a reply the same way — the comparison is only a
comparison if the inputs are the node's.
"""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("compare", ROOT / "tools" / "compare.py")
compare = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(compare)


def board(tmp_path):
    b = tmp_path / "board"; b.mkdir(); (b / "done").mkdir()
    (b / "README.md").write_text("# board\n")
    (b / "lander.md").write_text("# lander — a change waits\n\n    status   open\n    because  a commit waits on a hand\n             and nobody carries it\n    asked    Henri\n\nbody\n")
    (b / "silent-cord.md").write_text("# silent-cord — quiet\n\n    status   open\n    because  the cord needs a row\n    asked    Henri\n")
    (b / "done" / "grant.md").write_text("# grant\n\n    status   done\n    because  x\n    asked    Henri\n")
    return b


def test_the_digest_is_the_open_shelfs_title_and_because_never_done(tmp_path):
    d = compare.digest(board(tmp_path))
    assert "=== lander.md ===" in d and "# lander — a change waits" in d
    assert "a commit waits on a hand" in d and "and nobody carries it" in d
    assert "asked" not in d and "grant" not in d and "README" not in d


def test_a_reply_is_read_by_the_filename_the_shelf_judges(tmp_path):
    b = board(tmp_path)
    got = compare.read_reply("CARD: `lander.md` ===\nTASK: one line\nWHY: because\n", b)
    assert got["card"] == "lander.md" and got["task"] == "one line" and got["andon"] == ""
    got = compare.read_reply("CARD: unicorn.md\nTASK: x\nWHY: y\n", b)
    assert got["card"] == "" and "unicorn.md" in got["andon"]
    got = compare.read_reply("ANDON: which?\n", b)
    assert got["andon"] == "which?"
