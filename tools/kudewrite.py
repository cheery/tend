#!/usr/bin/env python3
#: asked-by: Henri, 2026-09-23 — "We could add into the chapter 1: The model writes a program" (card:kude.md); the door his "anthropic sonnet" and the hand-over his pick "Type + language reference", 2026-09-24
"""tools/kudewrite.py — a door model writes the ask node in Kude, and the check reads every try.

    tools/kudewrite.py --door NAME [--tries N]   from the person's shell (the door's key is under his home)
    tools/kudewrite.py --handed                  print what the model is handed, and nothing else

card:kude.md chapter 1's second half.  **The hand-over** is Henri's pick,
2026-09-24: the llm wire's three session types, kude.py's header — the
language as built — and one task.  Not ask-kude/ask.kude, and not the
example programs: the count is meant to say what the type does for the
one writing it, not what copying does.

**Every try goes through the check.**  A reply's first fenced block, or
the whole reply when it has none, is the program; `kude.py check` reads
it.  A refusal goes back as the checker's words alone, nothing added, and
the next reply is the next try, up to N (5).  The record is
proposals/kudewrite/<stamp>/: `handed.md`, each try's reply, program and
check, the whole conversation, and `count` — tries, refused, and the try
that checked, which after a refusal was fixed from the refusal's words
alone.  A try that checks is written to ask-kude-model/node.kude, the
node whose grant runs it; the run against the real llm is the person's
hand, `tools/launch.sh ask-kude-model run`, and its line goes in the
chapter beside the count.

The door is read by tools/door.sh, and its turn goes on the OpenAI chat
wire as tools/deliver.sh sends one; `temperature none` sends none.
"""
import argparse
import importlib.util
import json
import pathlib
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
KUDE = ROOT / "kude" / "kude.py"
MAX_TOKENS = 8000
QUESTION = "What is tend for?  Answer in one sentence."


def kude_module():
    spec = importlib.util.spec_from_file_location("kude", KUDE)
    k = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(k)
    return k


def handed():
    """The first message: the task, the llm wire's types, the language's reference."""
    k = kude_module()
    types = "\n".join(l for l in k.WORLD_TEXT.splitlines() if l.startswith("type Llm"))
    return (
        "Write the ask node as a Kude program.  It is run as `kude.py run node.kude 'main(llm)'`, where `llm` is a "
        "channel at the type `Llm`, and the llm node is the party at its other end.  Pull the llm; when it is up, ask "
        f'it "{QUESTION}" and give its answer as the output `answer`; when it is down, give the reason instead.  '
        "Reply with the program: its first fenced block, or the whole reply if it has none, is what the checker "
        "reads.\n\n"
        "The session types, which are the checker's own and which the program does not define:\n\n"
        f"{types}\n\n"
        "The language, as kude.py's header says it:\n\n"
        f"{k.__doc__}"
    )


def program_of(reply):
    m = re.search(r"```[^\n]*\n(.*?)```", reply, re.S)
    return m.group(1) if m else reply


def door_of(name):
    r = subprocess.run(["sh", str(HERE / "door.sh"), name], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(r.stderr.strip() or f"kudewrite: tools/door.sh {name} said nothing")
    url, model, keyfile = r.stdout.splitlines()[:3]
    t = subprocess.run(["sh", str(HERE / "door.sh"), name, "--tools"], capture_output=True, text=True)
    temp = (t.stdout.splitlines() + [""] * 4)[3].strip() if t.returncode == 0 else ""
    return url, model, pathlib.Path(keyfile).read_text().strip(), temp


def turn(url, model, key, temp, messages):
    body = {"model": model, "messages": messages, "max_tokens": MAX_TOKENS}
    if temp and temp != "none":
        body["temperature"] = float(temp)
    req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"})
    reply = json.load(urllib.request.urlopen(req, timeout=300))
    return (reply.get("choices") or [{}])[0].get("message", {}).get("content") or ""


def stamp_dir(out):
    base = out / time.strftime("%Y-%m-%d-%H%M")
    d, k = base, 2
    while d.exists():
        d = pathlib.Path(f"{base}-{k}")
        k += 1
    d.mkdir(parents=True)
    return d


def main(argv):
    ap = argparse.ArgumentParser(prog="kudewrite.py")
    ap.add_argument("--door")
    ap.add_argument("--tries", type=int, default=5)
    ap.add_argument("--handed", action="store_true")
    ap.add_argument("--out", default=str(ROOT / "proposals" / "kudewrite"))
    ap.add_argument("--node", default=str(ROOT / "ask-kude-model"))
    a = ap.parse_args(argv)
    if a.handed:
        print(handed())
        return 0
    if not a.door:
        ap.error("--door NAME, or --handed")
    url, model, key, temp = door_of(a.door)
    run = stamp_dir(pathlib.Path(a.out))
    first = handed()
    (run / "handed.md").write_text(first)
    messages = [{"role": "user", "content": first}]
    lines = [f"door {a.door}, model {model}, hand-over: the Llm types, kude.py's header, the task (handed.md)"]
    refused, checked = 0, None
    for n in range(1, a.tries + 1):
        try:
            reply = turn(url, model, key, temp, messages)
        except (urllib.error.URLError, OSError, ValueError) as e:
            lines.append(f"try {n}: the door refused the turn — {e}")
            (run / "count").write_text("\n".join(lines) + "\n")
            (run / "conversation.json").write_text(json.dumps(messages, indent=1, ensure_ascii=False))
            print(f"kudewrite: {a.door} refused the turn — {e}; the record is {run}", file=sys.stderr)
            return 2
        messages.append({"role": "assistant", "content": reply})
        (run / f"try-{n}.reply").write_text(reply)
        src = run / f"try-{n}.kude"
        src.write_text(program_of(reply))
        c = subprocess.run([sys.executable, str(KUDE), "check", str(src)], capture_output=True, text=True)
        said = (c.stdout if c.returncode == 0 else c.stderr).strip()
        (run / f"try-{n}.check").write_text(said)
        first_line = said.splitlines()[0] if said else ""
        if c.returncode == 0:
            checked = n
            lines.append(f"try {n}: checks — {first_line}")
            break
        refused += 1
        lines.append(f"try {n}: refused — {first_line}")
        messages.append({"role": "user", "content": said})   # the refusal's words, nothing added
    (run / "conversation.json").write_text(json.dumps(messages, indent=1, ensure_ascii=False))
    tries = checked or a.tries
    if checked:
        how = "first time" if checked == 1 else "from the refusal's words alone"
        summary = f"tries {tries}, refused {refused}, checked at try {checked} — {how}"
        node = pathlib.Path(a.node)
        node.mkdir(parents=True, exist_ok=True)
        (node / "node.kude").write_text((run / f"try-{checked}.kude").read_text())
        summary += f"; written to {node / 'node.kude'} — run it against the real llm: tools/launch.sh {node.name} run"
    else:
        summary = f"tries {tries}, refused {refused}, none checked"
    (run / "count").write_text(summary + "\n" + "\n".join(lines) + "\n")
    print(f"kudewrite: {summary}\nkudewrite: the record is {run}")
    return 0 if checked else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
