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
start = time.time()
fd = os.open(edge, os.O_RDONLY)
fcntl.flock(fd, fcntl.LOCK_SH)   # the pull: in force until `stop` (close) or exit
deadline = start + float(os.environ.get("ASK_WAIT", "300"))
while True:
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
body = json.dumps({"messages": [{"role": "user", "content": question}], "max_tokens": 200, "temperature": 0}).encode()
req = urllib.request.Request(url + "/v1/chat/completions", data=body, headers={"Content-Type": "application/json"})
reply = json.load(urllib.request.urlopen(req, timeout=300))
answer = (reply.get("choices") or [{}])[0].get("message", {}).get("content") or ""
(state / "answer").write_text(f"{question}\n---\n{answer.strip()}\n")
print(f"ask: {answer.strip()}", flush=True)
os.close(fd)   # stop: the edge let go before the exit, on purpose
