#!/usr/bin/env python3
#: asked-by: Henri, 2026-08-30 evening — "Once we have the full toolset, we could experiment with a benchmark … this would make a great card, make it so"; the runner at his "can we run the benchmark? Can we compose a checklist and go through it?" (2026-08-31)
"""tools/simpleqa.py — does a mind with a place to look stop guessing when the answer is not there? (card:simpleqa.md)

    tools/simpleqa.py run [N]     answer and grade the first N of the sample (default 150), three arms, resumable
    tools/simpleqa.py hand        thirty answers graded blind by the person, against the grader
    tools/simpleqa.py tally       the bins per arm, the fourth count, and day one's verdict

SimpleQA's answers are not in the tree; a tooled turn can look, find
nothing, and choose.  Three arms per question, same model, same door:
*bare* — no system line, no tools (TEND_TOOLS empty on the wire);
*seat* — the door's tools and tools/deliver.sh's seat line, nothing
else; *bland* — the same, plus one plain line before the question:
"Answer the question; say so if you do not know."  Every turn rides
tools/deliver.sh cold (no TEND_HISTORY, a fresh state directory), so
every call is a C: line in the account and nothing is carried between
questions or arms.  The grader is the paper's GRADER_TEMPLATE, read
verbatim from bench/simple-evals/simpleqa_eval.py, one turn per answer
through the grader door; the sample is the paper's own draw,
random.Random(0).sample(rows, 150), the same for every arm, and
`run N` takes its first N — the smoke is a prefix of the run.

Runs on the person's side (keys, net); writes only under the
gitignored proposals/simpleqa/ — one account per question and arm,
skipped when it already exists, which is also the resume.  The data
never rides a commit: bench/ is filled by hand, and a run without it
says the cp lines and exits 2.  A turn the door refuses is skipped and
said; the next run answers it.

    TEND_DOOR          the answering door (default openrouter)
    TEND_GRADER_DOOR   the grading door (default anthropic — a different
                       mind than the answerer; Henri's pick, 2026-08-31)
    TEND_BENCH_DIR / TEND_PROPOSAL_DIR / TEND_SAMPLE   tests point these elsewhere

The fourth count: a NOT_ATTEMPTED whose turn made no call is counted
apart — declining without looking is not the trade the seat line
names, and the paper's bin hides it.  `tally` prints the verdict only
past `hand`: thirty answers graded blind by the person, more than
three disagreements with the grader and the run stops there.
"""
import csv
import datetime
import json
import os
import random
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(os.environ.get("TEND_TREE", HERE.parent))
BENCH = Path(os.environ.get("TEND_BENCH_DIR", ROOT / "bench"))
PROP = Path(os.environ.get("TEND_PROPOSAL_DIR", ROOT / "proposals")) / "simpleqa"
DOOR = os.environ.get("TEND_DOOR", "openrouter")
GRADER_DOOR = os.environ.get("TEND_GRADER_DOOR", "anthropic")
SAMPLE = int(os.environ.get("TEND_SAMPLE", 150))
ARMS = ("bare", "seat", "bland")
BLAND = "Answer the question; say so if you do not know."
GRADES = {"A": "CORRECT", "B": "INCORRECT", "C": "NOT_ATTEMPTED"}


def bench_files():
    csvf = BENCH / "simple_qa_test_set.csv"
    evalf = BENCH / "simple-evals" / "simpleqa_eval.py"
    if not csvf.is_file() or not evalf.is_file():
        sys.stderr.write(
            "simpleqa: bench/ is filled by hand, and it is not (the data never rides a commit):\n"
            f"  cp ~/simple-evals/simple_qa_test_set.csv {BENCH}/\n"
            f"  cp -r ~/simple-evals {BENCH}/simple-evals\n")
        return None
    return csvf, evalf


def sample_rows(csvf):
    """The paper's own draw: random.Random(0).sample — the same rows, in
    the same order, every run and every arm."""
    with open(csvf, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return random.Random(0).sample(rows, min(SAMPLE, len(rows)))


def grader_template(evalf):
    m = re.search(r'GRADER_TEMPLATE = """(.*?)"""', evalf.read_text(encoding="utf-8"), re.S)
    if not m:
        sys.stderr.write(f"simpleqa: no GRADER_TEMPLATE in {evalf}\n")
        return None
    return m.group(1).strip()


def door_turn(door, question, state, tools, history=None):
    """One cold turn through the door, ridden on tools/deliver.sh; the
    courier's record is parsed back — V: (who answered), C: (the calls),
    A: (the answer, whose own newlines continue unprefixed)."""
    state.mkdir(parents=True, exist_ok=True)
    (state / "replies").unlink(missing_ok=True)
    env = dict(os.environ, TEND_DOOR=door, TEND_STATE_DIR=str(state),
               TEND_HISTORY=json.dumps(history or []))
    if not tools:
        env["TEND_TOOLS"] = ""
    r = subprocess.run(["sh", str(HERE / "deliver.sh"), str(ROOT / "llm"), question],
                       capture_output=True, text=True, env=env)
    if r.returncode != 0:
        raise RuntimeError((r.stderr or r.stdout).strip() or f"deliver exited {r.returncode}")
    model = ""; calls = []; ans = []; in_a = False
    for line in (state / "replies").read_text().splitlines():
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


LOG = BENCH / "log"


def say(line, err=False):
    """The run's line, on the screen and appended to bench/log (Henri,
    2026-08-31, green-lighting the 150: "lets put it write its output
    into bench/log") — gitignored with the rest of bench/."""
    (sys.stderr if err else sys.stdout).write(line + "\n")
    try:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(f"{datetime.datetime.now():%Y-%m-%d %H:%M} {line}\n")
    except OSError:
        pass


def field(text, name):
    m = re.search(rf"^    {name}\s+(.*)$", text, re.M)
    return m.group(1).strip() if m else ""


def answer_of(text):
    m = re.search(r"The answer, verbatim:\n\n(.*)\Z", text, re.S)
    if not m:
        return ""
    return "\n".join(l[4:] if l.startswith("    ") else l for l in m.group(1).splitlines()).strip()


def add_field(account, name, value):
    """A field appended to the account's field block — the block ends at
    the first section heading, so the answer text is never touched."""
    text = account.read_text()
    account.write_text(text.replace("\n\nThe ", f"\n    {name}    {value}\n\nThe ", 1))


def cmd_run(n):
    got = bench_files()
    if not got:
        return 2
    csvf, evalf = got
    tpl = grader_template(evalf)
    if tpl is None:
        return 2
    t = subprocess.run(["sh", str(HERE / "door.sh"), DOOR, "--tools"], capture_output=True, text=True)
    if t.returncode != 0:
        sys.stderr.write(t.stderr); return 2
    if not (t.stdout.splitlines() or [""])[0].strip():
        sys.stderr.write(f"simpleqa: the {DOOR} door has no tools line — the seat and bland arms need one (`tools  read ls grep` on the door file)\n")
        return 2
    rows = sample_rows(csvf)[:n]
    PROP.mkdir(parents=True, exist_ok=True)
    rc = 0; answered = 0; graded = 0
    for i, row in enumerate(rows):
        q = " ".join(str(row["problem"]).split())   # one line on the wire
        target = str(row["answer"]).strip()
        for arm in ARMS:
            account = PROP / f"q{i:03d}-{arm}.md"
            if not account.exists():
                ask = q if arm != "bland" else f"{BLAND} Question: {q}"
                state = PROP / "state" / account.stem
                try:
                    model, calls, ans = door_turn(DOOR, ask, state, tools=(arm != "bare"))
                except (RuntimeError, OSError) as e:
                    say(f"q{i:03d} {arm}: skipped — {e}", err=True); rc = 1; continue
                now = datetime.datetime.now()
                account.write_text(
                    f"<!-- SIMPLEQA — q{i:03d}, {arm} arm, {now:%Y-%m-%d %H:%M}.  NOT tree content (card:simpleqa.md). -->\n\n"
                    f"    question  {q}\n"
                    f"    target    {target}\n"
                    f"    arm       {arm}\n"
                    f"    door      {DOOR} ({model or 'model unknown'})\n"
                    f"    calls     {len(calls)}\n"
                    f"    looked    {'yes' if calls else 'no'}\n\n"
                    + ("The calls:\n\n" + "".join(f"    C: {c}\n" for c in calls) + "\n" if calls else "")
                    + "The answer, verbatim:\n\n" + "".join("    " + l + "\n" for l in ans.splitlines()))
                answered += 1
                first = ans.splitlines()[0][:80] if ans else "(empty)"
                say(f"q{i:03d} {arm}: {len(calls)} calls — {first}")
            text = account.read_text()
            if "\n    grade    " not in text:
                prompt = tpl.format(question=q, target=target, predicted_answer=answer_of(text))
                gstate = PROP / "state" / f"{account.stem}-grade"
                try:
                    gmodel, _, greply = door_turn(GRADER_DOOR, "Grade.", gstate, tools=False,
                                                  history=[{"role": "user", "content": prompt}])
                except (RuntimeError, OSError) as e:
                    say(f"q{i:03d} {arm}: not graded — {e}", err=True); rc = 1; continue
                m = re.search(r"(A|B|C)", greply)   # the paper's own reading
                if not m:
                    say(f"q{i:03d} {arm}: not graded — the grader said `{greply[:80]}`", err=True); rc = 1; continue
                add_field(account, "grade", f"{GRADES[m.group(1)]} — {GRADER_DOOR} ({gmodel or 'model unknown'})")
                graded += 1
                say(f"q{i:03d} {arm}: graded {GRADES[m.group(1)]}")
    say(f"{answered} answered and {graded} graded this pass; `tools/simpleqa.py tally` for the bins")
    return rc


def cmd_hand():
    accounts = sorted(PROP.glob("q*-*.md"))
    graded = [a for a in accounts if "\n    grade    " in a.read_text()]
    if len(graded) < 30:
        sys.stderr.write(f"simpleqa: hand wants 30 graded answers and there are {len(graded)} — run first\n")
        return 2
    pick = random.Random(1).sample(graded, 30)
    dis = 0; done = 0
    for a in pick:
        text = a.read_text()
        gword = field(text, "grade").split(" — ", 1)[0].strip()
        hand = field(text, "hand")
        if not hand:
            print(f"\n[{done + 1}/30] {a.name}")
            print(f"  Q:    {field(text, 'question')}")
            print(f"  gold: {field(text, 'target')}")
            print(f"  answer:\n" + "".join("    " + l + "\n" for l in answer_of(text).splitlines()))
            while True:
                got = input("  your grade — A correct, B incorrect, C not attempted: ").strip().upper()
                if got in GRADES:
                    break
            hand = GRADES[got]
            add_field(a, "hand", hand)
        done += 1
        if hand != gword:
            dis += 1
    print(f"\nhand: 30 graded, {dis} disagree with the grader ({GRADER_DOOR})")
    if dis > 3:
        print("more than three — the grader is not trusted; stop and look at the disagreements before quoting any number")
        return 1
    print("the grader holds; `tools/simpleqa.py tally` prints the verdict")
    return 0


def cmd_tally():
    accounts = sorted(PROP.glob("q*-*.md"))
    if not accounts:
        sys.stderr.write("simpleqa: nothing under proposals/simpleqa — run first\n")
        return 2
    bins = {arm: {"CORRECT": 0, "INCORRECT": 0, "NOT_ATTEMPTED": 0} for arm in ARMS}
    blind = {arm: 0 for arm in ARMS}
    saw = {arm: 0 for arm in ARMS}   # turns whose calls touched the benchmark's own card — the smoke's
    pending = 0; hands = 0; dis = 0  # find, 2026-08-31 ("I'd rather … than score in the incorrect bin");
    for a in accounts:               # Henri: run as-is and count it — the card is honestly part of the tree
        text = a.read_text()
        arm = field(text, "arm")
        gword = field(text, "grade").split(" — ", 1)[0].strip()
        if arm not in bins or gword not in ("CORRECT", "INCORRECT", "NOT_ATTEMPTED"):
            pending += 1
            continue
        bins[arm][gword] += 1
        if gword == "NOT_ATTEMPTED" and field(text, "looked") == "no":
            blind[arm] += 1
        if any("simpleqa" in c.lower() for c in re.findall(r"^    C: (.*)$", text, re.M)):
            saw[arm] += 1
        hand = field(text, "hand")
        if hand:
            hands += 1
            if hand != gword:
                dis += 1
    for arm in ARMS:
        b = bins[arm]
        print(f"{arm:6}  correct {b['CORRECT']:4}  incorrect {b['INCORRECT']:4}  not-attempted {b['NOT_ATTEMPTED']:4}  (never looked {blind[arm]}, saw the card {saw[arm]})")
    if pending:
        print(f"{pending} account(s) ungraded — run again")
    print(f"hand: {hands} graded, {dis} disagree")
    if hands >= 30 and dis <= 3:
        bi, si = bins["bare"]["INCORRECT"], bins["seat"]["INCORRECT"]
        bc, sc = bins["bare"]["CORRECT"], bins["seat"]["CORRECT"]
        hit = si * 5 <= bi * 4 and abs(sc - bc) <= 5
        print(f"day one's number (card:simpleqa.md): seat incorrect {si} against bare {bi} (a fifth lower is ≤ {bi * 4 // 5}), "
              f"correct {sc} against {bc} (within 5) — "
              + ("the tools earn their calls" if hit else "under the line, and the card says so"))
    else:
        print("the verdict waits on `hand` — thirty blind grades, at most three disagreements, before any number is quoted")
    return 0


def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        sys.stdout.write(__doc__)
        return 0 if len(argv) >= 2 else 2
    cmd = argv[1]
    if cmd == "run":
        if os.environ.get("TEND_FENCED"):
            sys.stderr.write("simpleqa: inside the fence there is no net and no key — run tools/simpleqa.py from your shell\n")
            return 1
        try:
            n = int(argv[2]) if len(argv) > 2 else SAMPLE
        except ValueError:
            sys.stderr.write("simpleqa: run wants a number\n"); return 2
        return cmd_run(n)
    if cmd == "hand":
        return cmd_hand()
    if cmd == "tally":
        return cmd_tally()
    sys.stderr.write("simpleqa: run [N] | hand | tally\n")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
