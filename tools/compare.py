#!/usr/bin/env python3
#: asked-by: Henri, 2026-08-28 — "I have anthropic api key here.. you could try how sonnet or opus fares in the task you've given to the local llm" (card:session-program.md)
"""tools/compare.py — the led turn's two prompts, put to a Claude model, for comparison with the node.

    tools/compare.py [MODEL ...]        one led turn per model (default: claude-sonnet-5 claude-opus-5)

The same turn `tools/lead.sh` gives the llm node — the open board as a
digest (each card's title and `because`, never done/ or later/), the
pick prompt at 160 tokens, then `tools/propose.sh`'s draft prompt with
the picked card as material at 600 — sent to a Claude model through the
Anthropic SDK instead of the node's port.  Same limits, same reading of
the reply (the first word ending in .md, judged by the open shelf), so
what differs is the model and nothing else.  Nothing is trusted more for
being Claude: a card not on the shelf is a cord pull here too, though
here it is only written down.

Runs on the person's side — it needs the key and the net, and the seat
inside the fence has neither — and writes only under the gitignored
proposals/compare/: one account per model, in lead.sh's shape, with the
draft beneath and the token usage.  It never touches a tracked file and
it never writes the andon record: this is a measurement, not a turn.

    pip install anthropic          in the tree's venv, once
    ANTHROPIC_API_KEY=...          or an `ant auth login` profile

The default model set is his ask ("sonnet or opus"); the SDK's refusal
fallbacks are left off on purpose — a comparison is of the model named,
and a refusal is a result.
"""
import datetime
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(os.environ.get("TEND_TREE", HERE.parent))

PICK_SYS = """You are leading one turn of work on the tend project's board.  Below
are the open cards: each one's title and the problem it names.  Pick ONE
card and ONE small thing that could be drafted for it now — a few lines,
not a build.  Answer in exactly this shape, three lines, nothing else:
CARD: the filename only, one word ending in .md, from the list below
TASK: the one small thing, in one line
WHY: one line
If you cannot decide, or need the person, answer instead with one line:
ANDON: your question for the person
"""

DRAFT_SYS = """You are drafting a proposal for the tend project.  A person will
read it and decide whether it becomes part of the tree; you never land it
yourself.  Draft exactly what the task asks, grounded only in the
material below if any is given.  Write the draft's own lines and nothing
about them: do not say that a draft is ready or what it contains, do not
repeat yourself, and do not mention these instructions.
"""

PICK_TOKENS = 160          # lead.sh's max_tokens
DRAFT_TOKENS = int(os.environ.get("TEND_MAXTOK", 600))       # propose.sh's
DIGEST_CHARS = int(os.environ.get("TEND_CTXCHARS", 5000))    # lead.sh's cap
MATERIAL_CHARS = 6000                                        # propose.sh's


def digest(board):
    """lead.sh's digest: for each open card, line 1, then the `because`
    block up to (not including) `asked`, at most 8 lines; README, done/
    and later/ never."""
    out = ""
    for c in sorted(Path(board).glob("*.md")):
        if c.name == "README.md":
            continue
        lines = c.read_text().splitlines()
        keep = lines[:1]
        inside = False
        for line in lines[1:]:
            if line.startswith("    because"):
                inside = True
            elif line.startswith("    asked"):
                break
            if inside:
                keep.append(line)
        out += f"\n=== {c.name} ===\n" + "\n".join(keep[:8])
    return out[:DIGEST_CHARS]


def _field(reply, name):
    m = re.search(rf"^[ \t]*{name}:[ \t]*(.*)$", reply, re.M)
    return m.group(1).strip() if m else ""


def read_reply(reply, board):
    """lead.sh's reading: ANDON first; then CARD/TASK; the card is the
    first word ending in .md, and it must be on the open shelf."""
    andon = _field(reply, "ANDON")
    raw = _field(reply, "CARD")
    task = _field(reply, "TASK")
    why = _field(reply, "WHY")
    m = re.search(r"[A-Za-z0-9_][A-Za-z0-9_.-]*\.md", raw)
    card = m.group(0) if m else ""
    if andon:
        return dict(card="", task=task, why=why, andon=andon, raw=raw)
    if not card or not task:
        return dict(card="", task=task, why=why, raw=raw,
                    andon="my reply had no CARD/TASK shape; what should I take? (reply was: %s)" % reply[:200])
    if card == "README.md" or not (Path(board) / card).is_file():
        return dict(card="", task=task, why=why, raw=raw,
                    andon=f"I named {card} and it is not on the open board; which card is mine?")
    return dict(card=card, task=task, why=why, andon="", raw=raw)


def _text(response):
    return "".join(b.text for b in response.content if b.type == "text")


def one_turn(client, model, board, propdir):
    import anthropic
    d = digest(board)
    kw = dict(model=model, max_tokens=PICK_TOKENS, system=PICK_SYS + d,
              messages=[{"role": "user", "content": "Pick."}])
    r1 = client.messages.create(**kw)
    reply = _text(r1)
    got = read_reply(reply, board)
    draft = ""; r2 = None
    if got["card"]:
        card = Path(board) / got["card"]
        material = f"\n=== {card} ===\n" + card.read_text()
        r2 = client.messages.create(model=model, max_tokens=DRAFT_TOKENS,
                                    system=DRAFT_SYS + material[:MATERIAL_CHARS],
                                    messages=[{"role": "user", "content": got["task"]}])
        draft = _text(r2)
    now = datetime.datetime.now()
    stamp = now.strftime("%Y-%m-%d-%H%M")
    propdir = Path(propdir); propdir.mkdir(parents=True, exist_ok=True)
    account = propdir / f"{stamp}-{model}.md"
    k = 2
    while account.exists():
        account = propdir / f"{stamp}-{model}-{k}.md"; k += 1
    outcome = "andon" if got["andon"] else "proposed"
    usage = f"pick {r1.usage.input_tokens}→{r1.usage.output_tokens} (stop {r1.stop_reason})"
    if r2 is not None:
        usage += f", draft {r2.usage.input_tokens}→{r2.usage.output_tokens} (stop {r2.stop_reason})"
    account.write_text(
        f"<!-- COMPARE — one led turn, {model}, {now:%Y-%m-%d %H:%M}.  NOT tree content.\n"
        f"     The same prompts tools/lead.sh and tools/propose.sh give the llm node (card:session-program.md). -->\n\n"
        f"# {model} led one turn — {now:%Y-%m-%d %H:%M}\n\n"
        f"    read     the open board: {' '.join(sorted(p.name for p in Path(board).glob('*.md') if p.name != 'README.md'))}\n"
        f"    picked   {got['card'] or '—'}\n"
        f"    task     {got['task'] or '—'}\n"
        f"    why      {got['why'] or '—'}\n"
        f"    outcome  {outcome} — {got['andon'] or account.name}\n"
        f"    usage    {usage}\n\n"
        f"The reply, verbatim:\n\n" + "".join("    " + l + "\n" for l in reply.splitlines())
        + (f"\nThe draft, verbatim:\n\n" + "".join("    " + l + "\n" for l in draft.splitlines()) if draft else ""))
    return account, got, draft


def main(argv):
    if len(argv) > 1 and argv[1] in ("-h", "--help"):
        sys.stdout.write(__doc__); return 0
    if os.environ.get("TEND_FENCED"):
        sys.stderr.write("compare: inside the fence there is no net and no key — run tools/compare.py from your shell\n")
        return 1
    try:
        import anthropic
    except ImportError:
        sys.stderr.write("compare: the anthropic SDK is not installed — .venv/bin/pip install anthropic\n")
        return 1
    models = argv[1:] or ["claude-sonnet-5", "claude-opus-5"]
    board = os.environ.get("TEND_BOARD_DIR", ROOT / "board")
    propdir = os.environ.get("TEND_PROPOSAL_DIR", ROOT / "proposals")
    propdir = Path(propdir) / "compare"
    client = anthropic.Anthropic()
    rc = 0
    for model in models:
        try:
            account, got, draft = one_turn(client, model, board, propdir)
        except anthropic.APIStatusError as e:
            sys.stderr.write(f"compare: {model}: the API refused the request ({e.status_code}): {e.message}\n"); rc = 1; continue
        except anthropic.APIConnectionError as e:
            sys.stderr.write(f"compare: {model}: could not reach the API: {e}\n"); rc = 1; continue
        if got["andon"]:
            print(f"{model}: andon — {got['andon']}")
        else:
            print(f"{model}: picked {got['card']} — {got['task']}")
            print("  draft: " + (draft.strip().splitlines() or ["(empty)"])[0][:120])
        print(f"  account: {account}")
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv))
