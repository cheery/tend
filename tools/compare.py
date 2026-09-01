#!/usr/bin/env python3
#: asked-by: Henri, 2026-08-28 — "I have anthropic api key here.. you could try how sonnet or opus fares in the task you've given to the local llm" (card:session-program.md)
"""tools/compare.py — the led turn's two prompts, put to a Claude model, for comparison with the node.

    tools/compare.py [--thinking] [MODEL ...]                one led turn per model (default: claude-sonnet-5 claude-opus-5)
    tools/compare.py --door NAME [--arm digest|tools] [--thinking]
                                                             the paired pick turn through a door: digest arm, then tools arm

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

**Thinking is off, as it is on the node.**  The first run (18:27) came
back with both drafts empty at `600 (stop max_tokens)`: on these models
thinking is adaptive by default and its tokens count against
`max_tokens`, so the whole budget went to thinking and none to the
draft — a limit copied from the node without the node's other setting
(`enable_thinking:false`).  Now `thinking: disabled` is sent, which is
the node's condition; `--thinking` is the other measurement — adaptive
thinking on, with `max_tokens` raised to 16000 so the draft has room —
and its account says so.

**The door pair (2026-08-31 — card:tools.md's owed measurement).**  The
card's prediction is decided on the pick turn: in ten paired turns, the
tooled turn's TASK: line cites a line of the card the digest does not
carry in five or more, or the tools are not earning their calls.  So
`--door NAME` runs the pick twice through the door: the *digest* arm —
the pick prompt with lead.sh's digest, and TEND_TOOLS set empty so the
door's tools line does not ride; the *tools* arm — the pick prompt
bare, the door's own `tools` line, the mind reading the board itself.
Both ride tools/deliver.sh, the same courier every talk turn rides, so
each arm's account carries the courier's own C: lines, and the raw
exchange stays in a state directory beside it, all under the
gitignored proposals/compare/.  The draft turn stays the SDK path's:
the prediction's number lives in the pick.  A door with no `tools`
line refuses the tools arm and says the line to write — the line is
the person's, as the model line was.  `--arm` reruns one arm alone.
`card:simpleqa.md`'s day one is this instrument with a different
question set.
"""
import datetime
import json
import os
import re
import subprocess
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
DIGEST_CHARS = int(os.environ.get("TEND_CTXCHARS", 20000))   # lead.sh's cap — keep the two equal
MATERIAL_CHARS = 6000                                        # propose.sh's


def digest(board):
    """lead.sh's digest: for each open card, line 1, then the `because`
    block up to (not including) `asked`, at most 8 lines; README, done/
    and later/ never."""
    out = ""
    dropped = []
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
        card = f"\n=== {c.name} ===\n" + "\n".join(keep[:8])
        # F008: this was `out[:DIGEST_CHARS]`, lead.sh's `head -c` in Python and
        # silent the same way.  The cut is on a card boundary, the rest go once
        # one goes, and the digest says which — see tools/lead.sh's own loop.
        if not dropped and (not out or len(out) + len(card) <= DIGEST_CHARS):
            out += card
        else:
            dropped.append(c.name)
    if dropped:
        out += (f"\n\n[{len(dropped)} card{'' if len(dropped) == 1 else 's'} did not fit: "
                f"{', '.join(dropped)}.  The board is longer than this list; these\n"
                "cards exist and are not shown.  Pull the cord if the one you want is missing.]")
    return out


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


def _parse_replies(text):
    """One exchange out of deliver.sh's record: the V: (who answered), the
    C: lines (the calls), and the A: — whose own newlines continue on
    unprefixed lines to the end of the file."""
    model = ""; calls = []; ans = []; in_a = False
    for line in text.splitlines():
        if in_a:
            ans.append(line); continue
        m = re.match(r"^\d{4}-\d\d-\d\d \d\d:\d\d ([A-Z]): (.*)$", line)
        if not m:
            continue
        k, v = m.groups()
        if k == "V":
            model = v.split(" ", 1)[-1]   # the V line is "door model"
        elif k == "C":
            calls.append(v)
        elif k == "A":
            ans.append(v); in_a = True
    return model, calls, "\n".join(ans).strip()


def door_pick(door, tools, board, propdir, thinking=False):
    """One pick turn through the door, ridden on tools/deliver.sh — the
    courier every talk turn rides, so the calls are run, capped and
    recorded exactly as a turn's are.  The pick prompt goes as a system
    message in TEND_HISTORY; the digest rides it only on the digest arm."""
    now = datetime.datetime.now()
    stamp = now.strftime("%Y-%m-%d-%H%M")
    arm = "tools" if tools else "digest"
    propdir = Path(propdir); propdir.mkdir(parents=True, exist_ok=True)
    state = propdir / f"{stamp}-door-{door}-{arm}"
    k = 2
    while state.exists() or state.with_suffix(".md").exists():
        state = propdir / f"{stamp}-door-{door}-{arm}-{k}"; k += 1
    env = dict(os.environ, TEND_DOOR=door, TEND_STATE_DIR=str(state),
               TEND_HISTORY=json.dumps([{"role": "system", "content": PICK_SYS + ("" if tools else digest(board))}]))
    if not tools:
        env["TEND_TOOLS"] = ""   # the digest arm sends none, whatever the door says
    if thinking:
        env["TEND_THINK"] = "1"
    r = subprocess.run(["sh", str(HERE / "deliver.sh"), str(ROOT / "llm"), "Pick."],
                       capture_output=True, text=True, env=env)
    if r.returncode != 0:
        raise RuntimeError((r.stderr or r.stdout).strip() or f"deliver exited {r.returncode}")
    model, calls, reply = _parse_replies((state / "replies").read_text())
    got = read_reply(reply, board)
    account = state.with_suffix(".md")
    outcome = "andon" if got["andon"] else "picked"
    account.write_text(
        f"<!-- COMPARE — one pick turn through the {door} door, {arm} arm, {now:%Y-%m-%d %H:%M}.  NOT tree content.\n"
        f"     card:tools.md's paired measurement: digest against tools, same door, same model.\n"
        f"     The raw exchange is beside this file, in {state.name}/. -->\n\n"
        f"# {door} ({model or 'model unknown'}) — {arm} arm pick — {now:%Y-%m-%d %H:%M}\n\n"
        f"    arm      {arm} — " + ("the pick prompt bare; the door's tools, the mind read the board itself\n" if tools
                                    else "the pick prompt with lead.sh's digest; no tools\n")
        + f"    picked   {got['card'] or '—'}\n"
        f"    task     {got['task'] or '—'}\n"
        f"    why      {got['why'] or '—'}\n"
        f"    outcome  {outcome} — {got['andon'] or account.name}\n"
        f"    calls    {len(calls)}\n"
        f"    limits   deliver.sh's own; thinking {'on' if thinking else 'off'}\n\n"
        + ("The calls:\n\n" + "".join(f"    C: {c}\n" for c in calls) + "\n" if calls else "")
        + "The reply, verbatim:\n\n" + "".join("    " + l + "\n" for l in reply.splitlines()))
    return account, got, calls, model


def one_turn(client, model, board, propdir, thinking=False):
    d = digest(board)
    if thinking:
        # the other measurement: adaptive thinking on, and room for it — not the node's limits
        mode = dict(thinking={"type": "adaptive"}); pick_max = 16000; draft_max = 16000
    else:
        # the node's condition: enable_thinking:false, and the node's limits
        mode = dict(thinking={"type": "disabled"}); pick_max = PICK_TOKENS; draft_max = DRAFT_TOKENS
    r1 = client.messages.create(model=model, max_tokens=pick_max, system=PICK_SYS + d,
                                messages=[{"role": "user", "content": "Pick."}], **mode)
    reply = _text(r1)
    got = read_reply(reply, board)
    draft = ""; r2 = None
    if got["card"]:
        card = Path(board) / got["card"]
        material = f"\n=== {card} ===\n" + card.read_text()
        r2 = client.messages.create(model=model, max_tokens=draft_max,
                                    system=DRAFT_SYS + material[:MATERIAL_CHARS],
                                    messages=[{"role": "user", "content": got["task"]}], **mode)
        draft = _text(r2)
    now = datetime.datetime.now()
    stamp = now.strftime("%Y-%m-%d-%H%M")
    propdir = Path(propdir); propdir.mkdir(parents=True, exist_ok=True)
    tag = f"{model}-thinking" if thinking else model
    account = propdir / f"{stamp}-{tag}.md"
    k = 2
    while account.exists():
        account = propdir / f"{stamp}-{tag}-{k}.md"; k += 1
    outcome = "andon" if got["andon"] else "proposed"
    usage = ("thinking adaptive, max_tokens 16000; " if thinking else "thinking off, the node's limits; ") \
        + f"pick {r1.usage.input_tokens}→{r1.usage.output_tokens} (stop {r1.stop_reason})"
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
    args = argv[1:]
    thinking = "--thinking" in args
    args = [a for a in args if a != "--thinking"]
    board = os.environ.get("TEND_BOARD_DIR", ROOT / "board")
    propdir = Path(os.environ.get("TEND_PROPOSAL_DIR", ROOT / "proposals")) / "compare"
    if "--door" in args:
        i = args.index("--door")
        door = args[i + 1] if i + 1 < len(args) else ""
        rest = args[:i] + args[i + 2:]
        arms = [False, True]
        if "--arm" in rest:
            j = rest.index("--arm")
            which = rest[j + 1] if j + 1 < len(rest) else ""
            rest = rest[:j] + rest[j + 2:]
            if which not in ("digest", "tools"):
                sys.stderr.write("compare: --arm is digest or tools\n"); return 2
            arms = [which == "tools"]
        if not door or rest:
            sys.stderr.write("compare: --door NAME [--arm digest|tools] [--thinking] — the door names its model\n"); return 2
        t = subprocess.run(["sh", str(HERE / "door.sh"), door, "--tools"], capture_output=True, text=True)
        if t.returncode != 0:
            sys.stderr.write(t.stderr); return 2
        if True in arms and not (t.stdout.splitlines() or [""])[0].strip():
            sys.stderr.write(f"compare: the {door} door has no tools line — the tools arm needs one"
                             f" (`tools  read ls grep` on the door file; the line is the person's to write)\n")
            return 2
        rc = 0
        for tools in arms:
            arm = "tools" if tools else "digest"
            try:
                account, got, calls, model = door_pick(door, tools, board, propdir, thinking)
            except (RuntimeError, OSError) as e:
                sys.stderr.write(f"compare: {door} {arm} arm: {e}\n"); rc = 1; continue
            if got["andon"]:
                print(f"{door} {arm}: andon — {got['andon']}")
            else:
                print(f"{door} {arm}: picked {got['card']} — {got['task']}")
            print(f"  calls: {len(calls)}")
            print(f"  account: {account}")
        return rc
    try:
        import anthropic
    except ImportError:
        sys.stderr.write("compare: the anthropic SDK is not installed — .venv/bin/pip install anthropic\n")
        return 1
    models = args or ["claude-sonnet-5", "claude-opus-5"]
    client = anthropic.Anthropic()
    rc = 0
    for model in models:
        try:
            account, got, draft = one_turn(client, model, board, propdir, thinking)
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
