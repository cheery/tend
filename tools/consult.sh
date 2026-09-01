#!/bin/sh
#: asked-by: Henri, 2026-08-28 — "brick 2" (card:session-program.md, the road §09:40, brick 2)
#
# tools/consult.sh NODE "question" [file ...]
#
# The model acting on what it reads.  `deliver.sh` carries a bare
# question to the node; this grounds one in named tree files — the
# question is answered from the material given, not the model's cold
# memory.  It is the conditioning question made runnable: gemma cold
# called jidoka a Buddhist practice; grounded in a tree document that
# says stop-the-line, does it read what it was handed?
#
# Default material is board/README.md.  The node's context is small
# (llm/grant: -c 2048), so the material is capped and a warning is said
# when it is trimmed — a card fits, the whole board does not.
#
# It runs on the person's side, like the runner and deliver: it reaches
# the loopback port a fenced session cannot.  The answer is printed and
# appended to $STATE/consult.log.
#
# Env: TEND_LLM_URL / TEND_LLM_HEALTH override the port (tests point them
# at a stub); TEND_MAXTOK caps the answer (default 400); TEND_CTXCHARS
# caps the material (default 6000 ~ 1500 tokens).
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
root=$(CDPATH= cd -- "$here/.." && pwd)
[ $# -ge 2 ] || { echo "consult: usage: tools/consult.sh NODE \"question\" [file ...]" >&2; exit 2; }
NODE=$(CDPATH= cd -- "$1" 2>/dev/null && pwd) || { echo "consult: no such node directory: $1" >&2; exit 2; }
name=$(basename "$NODE"); shift
question=$1; shift
STATE="${TEND_STATE_DIR:-${TEND_NODE_STATE_DIR:-$NODE/state}}"
port=$(sed -n 's/^bind  *//p' "$NODE/grant" 2>/dev/null | head -1); : "${port:=18080}"
CHAT="${TEND_LLM_URL:-http://127.0.0.1:$port/v1/chat/completions}"
HEALTH="${TEND_LLM_HEALTH:-http://127.0.0.1:$port/health}"
maxtok="${TEND_MAXTOK:-400}"
ctxchars="${TEND_CTXCHARS:-6000}"

if [ -n "${TEND_FENCED:-}" ]; then
    echo "consult: inside the fence the node's port is unreachable (--unshare-net) — run tools/consult.sh $name outside the fence" >&2
    exit 1
fi

# gather the material: the named files, or board/README.md by default
[ $# -gt 0 ] || set -- "$root/board/README.md"
material=""
for f in "$@"; do
    [ -f "$f" ] || { echo "consult: no such file: $f" >&2; exit 2; }
    material="$material
=== $f ===
$(cat "$f")"
done

trimmed=""
before=$(printf '%s' "$material" | wc -c)
if [ "$before" -gt "$ctxchars" ]; then
    material=$(printf '%s' "$material" | head -c "$ctxchars")
    trimmed=" (material trimmed to $ctxchars chars of $before — the node's context is small; name one card, not the board)"
fi

sys="You are answering using only the material below, from the tend project. If the material does not answer the question, say so plainly rather than guessing.

$material"

# ensure the node is up: consult is run by hand, so start it if it is not
# and wait for /health, the way deliver does — unless a test says not to
wait_ready() {
    _n=0
    while [ "$_n" -lt 150 ]; do
        curl -sf -m 2 "$HEALTH" >/dev/null 2>&1 && return 0
        sleep 2; _n=$((_n + 2))
    done
    echo "consult: $name did not become ready at $HEALTH within 150s" >&2; return 1
}
if [ -z "${TEND_NO_START:-}" ] && ! curl -sf -m 2 "$HEALTH" >/dev/null 2>&1; then
    echo "consult: $name is not up — starting it (first start compiles kernels, ~80s)…" >&2
    sh "$here/launch.sh" "$NODE" pull "consult warmup" >/dev/null 2>&1 || true
    wait_ready || exit 1
fi

body=$(jq -cn --arg s "$sys" --arg q "$question" --argjson n "$maxtok" \
    '{messages:[{role:"system",content:$s},{role:"user",content:$q}],max_tokens:$n,temperature:0.2,chat_template_kwargs:{enable_thinking:false}}')
out=$(curl -sS -m 180 -H 'Content-Type: application/json' -d "$body" "$CHAT") || {
    echo "consult: the node did not answer at $CHAT — is it up? (tools/launch.sh $name check / pull)" >&2; exit 1; }
answer=$(printf '%s' "$out" | jq -er '.choices[0].message | (.content // "") as $c | if ($c|length)>0 then $c else (.reasoning_content // "") end' 2>/dev/null) || {
    echo "consult: the node's reply was not a completion:" >&2; printf '%s\n' "$out" | head -3 >&2; exit 1; }

mkdir -p "$STATE" 2>/dev/null || true
{ printf '%s Q: %s\n' "$(date '+%Y-%m-%d %H:%M')" "$question"
  printf 'material: %s\n' "$*"
  printf 'A: %s\n\n' "$answer"; } >> "$STATE/consult.log" 2>/dev/null || true

printf 'Q: %s%s\n' "$question" "$trimmed"
printf 'A: %s\n' "$answer"
