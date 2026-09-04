#!/usr/bin/env python3
#: asked-by: Henri, 2026-08-28 — "I have anthropic api key here.. you could try how sonnet or opus fares in the task you've given to the local llm" (card:session-program.md)
"""tools/compare.py — the led turn's two prompts, put to a Claude model, for comparison with the node.

    tools/compare.py [--thinking] [MODEL ...]                one led turn per model (default: claude-sonnet-5 claude-opus-5)
    tools/compare.py --door NAME [--arm digest|tools] [--seed] [--thinking]
                                                             the paired pick turn through a door: digest arm, then tools arm
    tools/compare.py --draft CARD --task "…" [--cut N] [--cut-notice] [--thinking] [MODEL ...]
                                                             one draft turn alone, on a pinned card — F010's measurement

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

**Two arms added 2026-09-01**, when `card:questions.md`'s day one made
each of the standing "I don't know" questions name what would answer it,
and two of them turned out to want a flag rather than an opinion.

`--seed` is the **third pick arm**.  The original two put the question as
*digest or tools*, and the 08-31 run answered it badly for both: the
digest arm picks well from 7516 chars and cannot go deeper; the tools arm
reads 132.7k and drowns.  Seeded is neither — the digest in the prompt
*and* the tools in the request, so the mind starts where the digest arm
starts and reads further only if it wants to.  `TEND_READCHARS` is the
other knob on the same question (a 4000-char read returns a card's head,
and `executor.py:139`'s notice already says how to continue), and the
account now records which setting it ran under, because an arm that does
not say its own setting cannot be compared with another.

`--draft CARD --task "…"` is **`F010`'s measurement** and runs the draft
turn *alone*.  The card and the task are pinned because the normal path
picks them, so two runs would draft different material from different
tasks and nothing would be comparable; `--cut N` places the cut and
`--cut-notice` is the single thing that varies between the arms.  The
notice is `executor.py:139`'s wording **with its offer removed** — the
executor tells a mind holding tools that `read(path, line=L) continues`,
and a draft turn has no tools, so the same sentence would promise
something the mind cannot do.
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
DIGEST_CHARS = int(os.environ.get("TEND_CTXCHARS", 30000))   # lead.sh's cap — keep the two equal
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
        shown = keep[:8]
        # F009: the eight-line keep is a summary; say so when it is one.
        if len(keep) > 8:
            shown = shown + [f"    [… {len(keep) - 8} more lines of this because "
                             "— the card says more than this]"]
        card = f"\n=== {c.name} ===\n" + "\n".join(shown)
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
    model = ""; calls = []; ans = []; thought = []; in_a = False; in_t = False
    for line in text.splitlines():
        if in_a:
            ans.append(line); continue
        m = re.match(r"^\d{4}-\d\d-\d\d \d\d:\d\d ([A-Z]): (.*)$", line)
        if not m:
            # F011: the reasoning channel's own newlines continue on
            # unprefixed lines, exactly as the answer's do, and until
            # 2026-09-01 they were dropped here with the rest of it
            if in_t:
                thought.append(line)
            continue
        k, v = m.groups()
        in_t = False
        if k == "V":
            model = v.split(" ", 1)[-1]   # the V line is "door model"
        elif k == "C":
            calls.append(v)
        elif k == "T":
            thought.append(v); in_t = True
        elif k == "A":
            ans.append(v); in_a = True
    return model, calls, "\n".join(ans).strip(), "\n".join(thought).strip()


def _thinking_line(asked, thought, knob="template"):
    """F011 — what the account says about thinking.

    Until 2026-09-01 this was `thinking on` whenever `--thinking` was
    passed, which is a fact about the *request*.  Nine arms that day
    through one door across three models: every account said `thinking
    on`, five had an empty reasoning channel, and whether a channel came
    back predicted whether the turn produced a pick nine times out of
    nine.  The account was recording the flag and hiding the only
    variable that had explained anything.

    A turn that never asked and a turn that asked and got nothing are
    different turns and must not read the same.

    And `knob` (F015, 2026-09-02) is what the wire carried: `template`
    when the request had the node's `chat_template_kwargs` — the node's
    own turn, or a door that says `thinking  template` — and empty when
    the door's side has no off switch at all.  The first gemma4 turn
    through `doors/llm/door` read "thinking off — the node's own
    condition" on a request that carried no knob, and the model thought
    7,222 bytes into the content channel under that sentence.
    """
    if not asked:
        if knob == "template":
            return "thinking off — enable_thinking:false on the wire"
        return ("thinking not asked, and this door has no off switch — the "
                "model's own default, whatever it did")
    if thought:
        return f"thinking asked on, and {len(thought)} chars of reasoning came back"
    return ("thinking asked on, and NO reasoning came back — the model "
            "answered in the content channel")


#: What `deliver.sh:217` writes on a call it refused past the cap.  The
#: courier's words, matched rather than reimplemented: if that sentence
#: changes, this stops matching and the count goes back to counting
#: attempts — which is why `test_compare.py` asserts the two agree
#: against the real deliver.sh rather than against this string.
REFUSED = "out of calls"


def _calls_line(calls):
    """`F012` — the calls a turn *ran*, and the ones it only asked for.

    `deliver.sh:217` refuses a call past the cap and still records a `C:`
    line for it, because the record's rule is that the person watches the
    model act and a call the model made is something it did.  That is
    right.  What was wrong is that one number then meant two things — what
    the model wanted, and what the tree paid for — and every reader took
    it as the second, including the write-up of the 48-arm run, which
    compared 11.1 against 13.3 when the figures run were 10.9 and 12.6.

    So: a bare count when nothing was refused, which is what every
    account written before 2026-09-01 already means, and a two-part line
    only where the old form was misleading.  Old accounts stay readable
    and stay true; `F012` §"The shapes a fix could take" is shape (a).
    """
    refused = sum(1 for c in calls if REFUSED in c)
    if not refused:
        return str(len(calls))
    return f"{len(calls) - refused} run, {refused} refused past the cap"


def door_pick(door, tools, board, propdir, thinking=False, seed=False, knob=""):
    """One pick turn through the door, ridden on tools/deliver.sh — the
    courier every talk turn rides, so the calls are run, capped and
    recorded exactly as a turn's are.  The pick prompt goes as a system
    message in TEND_HISTORY; the digest rides it only on the digest arm.

    **`seed` is the third arm** (`card:tools.md`, 2026-09-01).  The two
    original arms put the question as *digest or tools*, and the 08-31
    measurement answered it badly for both: the digest arm picks well
    from 7516 chars and cannot go deeper, the tools arm reads 132.7k and
    drowns.  Seeded is neither — the digest in the prompt *and* the
    tools in the request, so the mind starts where the digest arm starts
    and may read further if it wants to.  It is the arm the card should
    have had, and it exists now because writing the question down as
    `*(question, measure — …)*` made it obvious that "what should the
    tools arm be given" has a third answer.
    """
    now = datetime.datetime.now()
    stamp = now.strftime("%Y-%m-%d-%H%M")
    arm = ("tools-seeded" if seed else "tools") if tools else "digest"
    propdir = Path(propdir); propdir.mkdir(parents=True, exist_ok=True)
    state = propdir / f"{stamp}-door-{door}-{arm}"
    k = 2
    while state.exists() or state.with_suffix(".md").exists():
        state = propdir / f"{stamp}-door-{door}-{arm}-{k}"; k += 1
    # the digest rides on the digest arm always, on the tools arm only when seeded
    carries_digest = seed or not tools
    env = dict(os.environ, TEND_DOOR=door, TEND_STATE_DIR=str(state),
               TEND_HISTORY=json.dumps([{"role": "system", "content":
                                         PICK_SYS + (digest(board) if carries_digest else "")}]))
    if not tools:
        env["TEND_TOOLS"] = ""   # the digest arm sends none, whatever the door says
    if thinking:
        env["TEND_THINK"] = "1"
    r = subprocess.run(["sh", str(HERE / "deliver.sh"), str(ROOT / "llm"), "Pick."],
                       capture_output=True, text=True, env=env)
    if r.returncode != 0:
        raise RuntimeError((r.stderr or r.stdout).strip() or f"deliver exited {r.returncode}")
    model, calls, reply, thought = _parse_replies((state / "replies").read_text())
    got = read_reply(reply, board)
    account = state.with_suffix(".md")
    outcome = "andon" if got["andon"] else "picked"
    # what a read returned before the cut — the knob the `head` arm turns,
    # recorded because an arm that does not say its own setting cannot be
    # compared with another (F011, the same lesson one layer up)
    readchars_said = os.environ.get("TEND_READCHARS") or "the door's own"
    account.write_text(
        f"<!-- COMPARE — one pick turn through the {door} door, {arm} arm, {now:%Y-%m-%d %H:%M}.  NOT tree content.\n"
        f"     card:tools.md's paired measurement: digest against tools, same door, same model.\n"
        f"     The raw exchange is beside this file, in {state.name}/. -->\n\n"
        f"# {door} ({model or 'model unknown'}) — {arm} arm pick — {now:%Y-%m-%d %H:%M}\n\n"
        f"    arm      {arm} — " + (
            ("the pick prompt with lead.sh's digest AND the door's tools; the mind starts "
             "where the digest arm starts and may read further\n" if seed else
             "the pick prompt bare; the door's tools, the mind read the board itself\n") if tools
            else "the pick prompt with lead.sh's digest; no tools\n")
        + f"    readchars {readchars_said}\n"
        + f"    picked   {got['card'] or '—'}\n"
        f"    task     {got['task'] or '—'}\n"
        f"    why      {got['why'] or '—'}\n"
        f"    outcome  {outcome} — {got['andon'] or account.name}\n"
        f"    calls    {_calls_line(calls)}\n"
        f"    limits   deliver.sh's own; {_thinking_line(thinking, thought, knob)}\n\n"
        + ("The calls:\n\n" + "".join(f"    C: {c}\n" for c in calls) + "\n" if calls else "")
        + "The reply, verbatim:\n\n" + "".join("    " + l + "\n" for l in reply.splitlines()))
    return account, got, calls, model


def _pull(args, names):
    """Take `--name value` pairs out of args.  Returns (rest, {name: value}).

    A flag named twice takes the last, and a flag with no value reads as
    None rather than swallowing the next flag — which is how `--task
    --cut 200` would otherwise become a task of "--cut".
    """
    opts = {n: None for n in names}
    rest = []
    i = 0
    while i < len(args):
        if args[i] in opts:
            nxt = args[i + 1] if i + 1 < len(args) else None
            if nxt is not None and not nxt.startswith("--"):
                opts[args[i]] = nxt
                i += 2
                continue
            i += 1
            continue
        rest.append(args[i]); i += 1
    return rest, opts


def cut_notice(kept, total, path):
    """What the material says when it has been cut — `F010`'s told arm.

    Modelled on `tools/executor.py:139`, the one cut in this tree that
    already says what it took, **with its offer removed**.  The
    executor's notice ends `read(path, line=L) continues`, because a mind
    holding tools can ask for the rest.  A draft turn has no tools, so
    the same sentence would promise something the mind cannot do — and a
    notice that offers an impossible remedy is worse than silence,
    because it spends the model's turn on reaching for it.  So this one
    says the material is cut, where, and that there is no more coming.
    """
    # exactly executor.py's arithmetic: `at` is the first line not shown,
    # `lines` is readlines()'s count — so a trailing newline does not
    # invent a line that is not there.  The first draft used
    # `count("\n") + 1` for the total and said "line 3 of 5" of a
    # four-line file, which a test caught.
    at = kept.count("\n") + 1
    lines = len(total.splitlines())
    return (f"\n[… cut at {len(kept)} chars of {len(total)}, at line {at} of "
            f"{lines} of {path}.  The rest of this card is not available in "
            f"this turn — there is no way to ask for it.]")


def draft_turn(client, model, board, propdir, card, task, cut, tell, thinking=False):
    """One draft turn alone, on a named card — `F010`'s measurement.

    **Why the card and the task are pinned rather than picked.**  The
    normal path picks a card and then drafts on it, so two runs draft
    different material from different tasks and nothing is comparable.
    `F010` asks one question — *is a drafting prompt better or worse for
    being told its material was cut* — and the only way to ask it is for
    the two arms to differ in exactly that.  So `--draft CARD --task …`
    fixes both, `--cut N` places the cut, and `--cut-notice` is the one
    thing that varies.

    `--cut` matters as much as the notice.  `F010`'s design says the cut
    is placed **on purpose above a fact that would change the draft**, so
    the outcome per draft is *does it assert what the cut-away tail
    contradicts* — right or wrong, countable — rather than "did it hedge",
    which is taste and would never settle.
    """
    path = Path(board) / card
    if not path.exists():
        raise RuntimeError(f"no card {card} on the open shelf")
    whole = f"\n=== {path} ===\n" + path.read_text()
    kept = whole[:cut]
    was_cut = len(kept) < len(whole)
    material = kept + (cut_notice(kept, whole, card) if (was_cut and tell) else "")

    mode = (dict(thinking={"type": "adaptive"}) if thinking
            else dict(thinking={"type": "disabled"}))
    draft_max = 16000 if thinking else DRAFT_TOKENS
    r = client.messages.create(model=model, max_tokens=draft_max,
                               system=DRAFT_SYS + material,
                               messages=[{"role": "user", "content": task}], **mode)
    draft = _text(r)

    now = datetime.datetime.now()
    stamp = now.strftime("%Y-%m-%d-%H%M")
    arm = "told" if tell else "silent"
    propdir = Path(propdir); propdir.mkdir(parents=True, exist_ok=True)
    account = propdir / f"{stamp}-draft-{arm}-{model}.md"
    k = 2
    while account.exists():
        account = propdir / f"{stamp}-draft-{arm}-{model}-{k}.md"; k += 1
    account.write_text(
        f"<!-- COMPARE — one draft turn, {model}, {now:%Y-%m-%d %H:%M}.  NOT tree content.\n"
        f"     F010's measurement: the same cut material, told and not told. -->\n\n"
        f"# {model} — draft turn, {arm} arm — {now:%Y-%m-%d %H:%M}\n\n"
        f"    arm      {arm} — the material {'carries a cut notice' if tell else 'is cut in silence'}\n"
        f"    card     {card}\n"
        f"    task     {task}\n"
        f"    cut      {len(kept)} of {len(whole)} chars"
        + (" — NOT CUT, the card is shorter than the cap\n" if not was_cut else "\n")
        + f"    usage    {r.usage.input_tokens}→{r.usage.output_tokens} (stop {r.stop_reason})\n\n"
        + ("**The material was not cut, so the arms are identical and this "
           "turn measures nothing.**  Pick a longer card or a smaller --cut.\n\n"
           if not was_cut else "")
        + "The draft, verbatim:\n\n"
        + "".join("    " + l + "\n" for l in draft.splitlines()))
    return account, draft, was_cut


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
        whole = f"\n=== {card} ===\n" + card.read_text()
        # F010: the normal path's draft was the silent arm — cut at MATERIAL_CHARS with
        # nothing said to the mind, the second copy of propose.sh's cut.  It carries the
        # notice now, as the draft turn's told arm does and as every cut in the tree says
        material = whole[:MATERIAL_CHARS]
        if len(material) < len(whole):
            material += cut_notice(material, whole, got["card"])
        r2 = client.messages.create(model=model, max_tokens=draft_max,
                                    system=DRAFT_SYS + material,
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
    seed = "--seed" in args
    args = [a for a in args if a != "--seed"]
    tell = "--cut-notice" in args
    args = [a for a in args if a != "--cut-notice"]
    board = os.environ.get("TEND_BOARD_DIR", ROOT / "board")
    propdir = Path(os.environ.get("TEND_PROPOSAL_DIR", ROOT / "proposals")) / "compare"

    if "--draft" in args:                      # F010's measurement
        args, opts = _pull(args, ("--draft", "--task", "--cut"))
        if opts["--draft"] is None:
            sys.stderr.write("compare: --draft wants a card\n"); return 2
        if not opts["--task"]:
            sys.stderr.write("compare: --draft wants --task \"the one small thing\" — "
                             "pinned, or the two arms draft different things\n"); return 2
        try:
            cut = int(opts["--cut"] or MATERIAL_CHARS)
        except ValueError:
            sys.stderr.write("compare: --cut wants a number of chars\n"); return 2
        if seed:
            sys.stderr.write("compare: --seed is the door's tools arm, not the draft turn\n"); return 2
        try:
            import anthropic
        except ImportError:
            sys.stderr.write("compare: the anthropic SDK is not installed — .venv/bin/pip install anthropic\n")
            return 1
        client = anthropic.Anthropic()
        rc = 0
        for model in args or ["claude-sonnet-5"]:
            try:
                account, draft, was_cut = draft_turn(
                    client, model, board, propdir, opts["--draft"],
                    opts["--task"], cut, tell, thinking)
            except (RuntimeError, anthropic.APIStatusError, anthropic.APIConnectionError) as e:
                sys.stderr.write(f"compare: {model}: {e}\n"); rc = 1; continue
            print(f"{model} draft ({'told' if tell else 'silent'}): "
                  + (draft.strip().splitlines() or ["(empty)"])[0][:110])
            if not was_cut:
                print("  WARNING: the material was not cut — this turn measures nothing")
            print(f"  account: {account}")
        return rc

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
        # the fifth `--tools` line: `template` when the door's side takes the node's
        # off switch, empty when it has none — the account says which (F015)
        knob = (t.stdout.splitlines() + [""] * 5)[4].strip()
        rc = 0
        for tools in arms:
            arm = ("tools-seeded" if seed else "tools") if tools else "digest"
            try:
                account, got, calls, model = door_pick(door, tools, board, propdir,
                                                       thinking, seed and tools, knob)
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
