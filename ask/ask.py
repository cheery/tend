#!/usr/bin/python3
#: asked-by: Henri, 2026-09-02 — "Kun prosessi vetää jonkin toisen solmun päälle, se voi sen jälkeen aloittaa solmun kanssa keskustelun, joka on verkon pointti" (card:edge.md)
"""ask — pull the llm, ask it one thing, let go.

The first conversation over an edge.  The pull is a shared flock on the
edge file the launcher made and named in $TEND_PULLS; it stays in force
until this process closes the fd or exits.  The talk is one request to
the llm's port, which keep lets through because the grant says
`connect 18080` — with the word gone, the kernel refuses and this says
so.  The llm comes up because it is pulled (the tick, `serve`), and
loading its model takes about 80 s, so the wait is long and says how
long it waited when it gives up.  The answer goes into this node's
state, `answer`, beside the signal.
"""
import fcntl
import json
import os
import pathlib
import sys
import time
import urllib.error
import urllib.request

pulls = dict(kv.split("=", 1) for kv in os.environ.get("TEND_PULLS", "").split())
edge = pulls.get("llm")
if not edge:
    print("ask: the grant names no edge to llm — `pull llm` is the word (card:edge.md)", file=sys.stderr)
    sys.exit(2)
state = pathlib.Path(os.environ["STATE"])
url = os.environ.get("ASK_URL", "http://127.0.0.1:18080").rstrip("/")
question = " ".join(sys.argv[1:]) or "What is tend for?  Answer in one sentence."
# the material (card:material.md): the tree files the grant lets this node read, named in $TEND_MATERIAL by
# the launcher.  Each is put in front of the question under its name, as tools/propose.sh's digest does, so a
# node asks with the tree in hand instead of cold; `answer` records what was handed.  With no `material` word
# the list is empty and the ask is cold — the measurement's baseline (the 16:29 answer on card:edge.md)
material = os.environ.get("TEND_MATERIAL", "").split()
handed = []
preamble = ""
for f in material:
    try:
        content = pathlib.Path(f).read_text()
    except OSError as e:
        print(f"ask: material {f} could not be read — {e}; `material PATH` is the grant word and keep grants the read (card:material.md)", file=sys.stderr)
        sys.exit(2)
    label = os.path.basename(f)
    preamble += f"=== {label} ===\n{content}\n\n"
    handed.append(f"{label} ({len(content)} chars)")
asked = question if not preamble else f"{preamble}---\n{question}"
start = time.time()
fd = os.open(edge, os.O_RDONLY)
fcntl.flock(fd, fcntl.LOCK_SH)   # the pull: in force until `stop` (close) or exit
deadline = start + float(os.environ.get("ASK_WAIT", "300"))
# the pulled node's state is the interface (Henri, 2026-09-02): the llm's `stopped` is readable here,
# and a death newer than this edge is one the resolver will not undo on this edge (card:hold.md, rule
# 3) — so it is read, and said at once, instead of waiting out the clock.  Found 15:26 the same day:
# the llm died at its loader under the tick and ask waited 300 s to say "never answered"
stopped = pathlib.Path(edge).parent.parent / "stopped"
edge_at = os.stat(edge).st_mtime
while True:
    try:
        st = stopped.stat()
        if st.st_mtime > edge_at:
            first = stopped.read_text().splitlines()[0] if stopped.read_text() else ""
            if first.startswith("exited ") and not first.startswith("exited 0"):
                print(f"ask: llm died while pulled — {first}; the resolver restarts it only on an edge newer than the death, so this pull is over: pull again once the cause is fixed (its log and the panel say what it said)", file=sys.stderr)
                os.close(fd)
                sys.exit(1)
    except OSError:
        pass
    try:
        if urllib.request.urlopen(url + "/health", timeout=2).status == 200:
            break
    except urllib.error.URLError as e:
        if isinstance(e.reason, PermissionError):   # the kernel's refusal, wrapped: keep has no connect rule for this port
            print("ask: connect refused by keep — `connect PORT` is the word for the talk (card:edge.md)", file=sys.stderr)
            sys.exit(2)
        pass   # not up yet, or loading: the tick brings it up, the model takes its time
    except OSError:
        pass
    if time.time() >= deadline:
        print(f"ask: pulled llm for {time.time() - start:.0f}s and it never answered /health — is anything serving it?", file=sys.stderr)
        sys.exit(1)
    time.sleep(1)
# 800 tokens, not 200: the first live answer (15:41) was 200 tokens of gemma4's thinking under --jinja and an
# empty `content` — the cap was spent before the answer began, and ask said "ask: " and exited 0
# 2000 when the node reads the tree (card:material.md, closed 2026-09-04): reasoning over ~12k tokens of
# material plus the answer did not fit in 800 — the right sentence was cut at "jossa" — and 2000 finished it.
# A cold ask keeps 800.  ASK_TOKENS set by hand wins either way
cap = int(os.environ.get("ASK_TOKENS", "2000" if material else "800"))
body = json.dumps({"messages": [{"role": "user", "content": asked}],
                   "max_tokens": cap, "temperature": 0}).encode()
req = urllib.request.Request(url + "/v1/chat/completions", data=body, headers={"Content-Type": "application/json"})
reply = json.load(urllib.request.urlopen(req, timeout=600))
choice = (reply.get("choices") or [{}])[0]
msg = choice.get("message", {})
answer = (msg.get("content") or "").strip()
thinking = (msg.get("reasoning_content") or "").strip()   # the mind's thinking, when the door returns it (card:private.md)
# the token cap ended the reply before the model stopped (card:material.md, 2026-09-03: gemma4's answer cut
# mid-sentence at "jossa" and written as if whole).  A cut that says nothing is the F010 family; this one says
cut = choice.get("finish_reason") == "length"
if not answer and not thinking:
    print(f"ask: the llm returned no answer and no thinking — {json.dumps(reply)[:300]}", file=sys.stderr)
    os.close(fd)
    sys.exit(1)
out = f"{question}\n"
if handed:   # the material arm records what it handed; the cold arm's answer is unchanged (card:material.md)
    out += f"---material: {', '.join(handed)}---\n"
out += f"---\n{answer}\n"
if thinking:
    out += f"---thinking ({len(thinking.split())} words)---\n{thinking}\n"
if cut:
    out += f"---cut: the reply hit the token cap (ASK_TOKENS={cap}) and is unfinished; raise ASK_TOKENS or ask for less---\n"
(state / "answer").write_text(out)
note = f"  [cut: the {cap}-token cap ended it — the answer is unfinished; raise ASK_TOKENS]" if cut else ""
if answer:
    print(f"ask: {answer}{note}", flush=True)
else:
    print(f"ask: no answer — the llm thought for {len(thinking.split())} words and the {cap}-token cap ended it before it answered; the thinking is in $STATE/answer.  Raise ASK_TOKENS, or ask for less", flush=True)
os.close(fd)   # stop: the edge let go before the exit, on purpose
