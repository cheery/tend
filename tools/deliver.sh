#!/bin/sh
#: asked-by: Henri, 2026-08-28 — "do that delivery now" (card:session-program.md, the road §09:40, brick 1)
#
# tools/deliver.sh NODE [question]
#
# A pull's words are an ask, and until now nothing carried them: `pull`
# appended the words to the pull file and the person spoke to the port
# by hand.  This delivers.  Given a NODE it reads the questions in the
# pull file that have no reply yet, asks the running model at the node's
# port, and writes the reply to $STATE/replies — a stamp, the question,
# the answer.  With a question argument it pulls it first (records and
# starts the node, via the installed launcher), waits for the node to be
# ready, then answers that one.
#
# It runs on the person's side, like the runner, because it reaches a
# loopback port a fenced session cannot.  Inside the fence it records
# the ask through `pull` and says the delivery is the runner's side to
# make — the same boundary `launch.sh pull` draws.
#
#   $STATE/pull       the questions, one per line: "<epoch> <words...>"
#   $STATE/replies    what came back, appended
#   $STATE/delivered  how many pull lines have been handled (the marker)
#
# Env: TEND_LLM_URL / TEND_LLM_HEALTH override the port (tests point them
# at a stub); TEND_NO_START skips starting the node; TEND_MAXTOK caps the
# answer (default 2000 — 300 until 2026-08-30, when thinking arrived and
# Henri said "lift the token cap": a model that thinks spends its cap on
# the thinking first); TEND_STATE_DIR points state at a scratch dir.
# TEND_THINK, non-empty, turns the chat template's thinking mode on
# (`enable_thinking`, off until 2026-08-30 — Henri: "can I enable
# thinking for the model somehow?"): the model reasons before it answers,
# the server returns the reasoning apart from the answer, and it is kept
# in `replies` as a `T:` line between the Q and the A — read, never fed
# back as history.  Whether a model has a thinking mode is its chat
# template's to say; one that does not ignores the switch.
# TEND_HISTORY is the conversation so far — a JSON array of prior
# messages, prepended to the ask so the model answers in the
# conversation and not cold (tools/panel.py's talk, 2026-08-30 — Henri:
# "so that I can truly talk with the model"); empty or unset is cold, as
# a pull line always was.
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
[ $# -ge 1 ] || { echo "deliver: usage: tools/deliver.sh NODE [question]" >&2; exit 2; }
NODE=$(CDPATH= cd -- "$1" 2>/dev/null && pwd) || { echo "deliver: no such node directory: $1" >&2; exit 2; }
name=$(basename "$NODE"); shift
q="${1:-}"
STATE="${TEND_STATE_DIR:-${TEND_NODE_STATE_DIR:-$NODE/state}}"
pull="$STATE/pull"; replies="$STATE/replies"; marker="$STATE/delivered"
port=$(sed -n 's/^bind  *//p' "$NODE/grant" 2>/dev/null | head -1); : "${port:=18080}"
CHAT="${TEND_LLM_URL:-http://127.0.0.1:$port/v1/chat/completions}"
HEALTH="${TEND_LLM_HEALTH:-http://127.0.0.1:$port/health}"
maxtok="${TEND_MAXTOK:-2000}"
think=$(printenv TEND_THINK || true)
if [ -n "$think" ]; then think=true; else think=false; fi
thoughtf="$STATE/.thought"   # what the model thought before its last answer, when it was asked to —
                             # a file, because ask() runs in a $(...) and a variable set there is lost
hist=$(printenv TEND_HISTORY || true)
[ -n "$hist" ] || hist='[]'
printf '%s' "$hist" | jq -e 'type == "array"' >/dev/null 2>&1 || {
    echo "deliver: TEND_HISTORY is not a JSON array of messages" >&2; exit 2; }
mkdir -p "$STATE" 2>/dev/null || true

stamp() { date '+%Y-%m-%d %H:%M'; }

# ask the model one question; print the answer text, or fail loudly.
# The thinking, if any, is left in $thoughtf: an answer with no content is
# a model that put its whole reply in the reasoning, and that is the answer.
ask() {
    _q=$1
    _body=$(jq -cn --arg q "$_q" --argjson n "$maxtok" --argjson h "$hist" --argjson t "$think" \
        '{messages:($h + [{role:"user",content:$q}]),max_tokens:$n,temperature:0.2,chat_template_kwargs:{enable_thinking:$t}}')
    _out=$(curl -sS -m 600 -H 'Content-Type: application/json' -d "$_body" "$CHAT") || {
        echo "deliver: the node did not answer at $CHAT — is it up? (tools/launch.sh $name check / pull)" >&2; return 1; }
    printf '%s' "$_out" | jq -e '.choices[0].message' >/dev/null 2>&1 || {
        echo "deliver: the node's reply was not a completion:" >&2; printf '%s\n' "$_out" | head -3 >&2; return 1; }
    _c=$(printf '%s' "$_out" | jq -r '.choices[0].message.content // ""')
    _r=$(printf '%s' "$_out" | jq -r '.choices[0].message.reasoning_content // ""')
    if [ -n "$_c" ]; then printf '%s' "$_r" > "$thoughtf"; printf '%s' "$_c"; else : > "$thoughtf"; printf '%s' "$_r"; fi
}

# answer one pull line "<epoch> <words>"; nothing if it carries no words
answer_line() {
    _line=$1
    _words=$(printf '%s' "$_line" | cut -s -d' ' -f2-)
    [ -n "$_words" ] || return 0
    _a=$(ask "$_words") || return 1
    thought=$(cat "$thoughtf" 2>/dev/null || true); rm -f "$thoughtf"
    { printf '%s Q: %s\n' "$(stamp)" "$_words"
      [ -z "$thought" ] || printf '%s T: %s\n' "$(stamp)" "$thought"
      printf '%s A: %s\n\n' "$(stamp)" "$_a"; } >> "$replies"
    printf '  Q: %s\n' "$_words"
    [ -z "$thought" ] || printf '  T: %s\n' "$thought"
    printf '  A: %s\n' "$_a"
}

wait_ready() {
    _n=0
    while [ "$_n" -lt 150 ]; do
        curl -sf -m 2 "$HEALTH" >/dev/null 2>&1 && return 0
        sleep 2; _n=$((_n + 2))
    done
    echo "deliver: $name did not become ready at $HEALTH within 150s" >&2; return 1
}

# inside the fence the delivery is the runner's side to make
if [ -n "${TEND_FENCED:-}" ]; then
    if [ -n "$q" ]; then sh "$here/launch.sh" "$NODE" pull "$q"; fi
    echo "deliver: inside the fence — the ask is recorded; the runner's side delivers it (run tools/deliver.sh $name outside the fence)" >&2
    exit 0
fi

total=$( [ -f "$pull" ] && grep -c . "$pull" || echo 0 )
done_n=$( [ -f "$marker" ] && cat "$marker" || echo -1 )

if [ -n "$q" ]; then
    # pull records the words and starts the node; then answer just this one
    [ -n "${TEND_NO_START:-}" ] || sh "$here/launch.sh" "$NODE" pull "$q" >/dev/null 2>&1 || true
    [ -n "${TEND_NO_START:-}" ] || wait_ready
    # if pull did not append (TEND_NO_START in a test), append the ask ourselves
    total_now=$( [ -f "$pull" ] && grep -c . "$pull" || echo 0 )
    if [ "$total_now" -le "$total" ]; then printf '%s %s\n' "$(date +%s)" "$q" >> "$pull"; fi
    answer_line "$(tail -1 "$pull")" || exit 1
    grep -c . "$pull" > "$marker"
    exit 0
fi

# no question: deliver every pull line past the marker; arm on first run
if [ "$done_n" -lt 0 ]; then
    echo "$total" > "$marker"
    echo "deliver: armed at $total lines — pull a question, or pass one: tools/deliver.sh $name \"...\""
    exit 0
fi
[ "$total" -gt "$done_n" ] || { echo "deliver: nothing new to deliver ($done_n of $total handled)."; exit 0; }
i=$done_n
while [ "$i" -lt "$total" ]; do
    i=$((i + 1))
    answer_line "$(sed -n "$i"p "$pull")" || { echo "$((i - 1))" > "$marker"; exit 1; }
done
echo "$total" > "$marker"
