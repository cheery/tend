#!/bin/sh
#: asked-by: Henri, 2026-08-28 — "brick 3" (card:session-program.md, the road §09:40, brick 3)
#
# tools/propose.sh NODE "task" [file ...]
#
# The model writes — and only ever proposes.  Brick 2 (consult) let the
# node read the tree; this lets it produce tree-shaped work — a kaizen
# draft, a card-edit proposal — under the boundary the whole tree rests
# on: a party may not bound itself, so the model may not land its own
# words in the tree.  It drafts what is asked, grounded in the named
# material, and writes the draft to a gitignored proposals area,
# banner-marked as not tree content until a person lands it by hand.  It
# never touches a tracked file.
#
# Runs on the person's side (it reaches the port); the person reviews the
# proposal and applies it, or not — the same seam a clone's pull crosses.
#
# Env: TEND_PROPOSAL_DIR (default <tree>/proposals, gitignored);
# TEND_LLM_URL / TEND_LLM_HEALTH (tests); TEND_MAXTOK (default 600);
# TEND_CTXCHARS (default 6000); TEND_NO_START skips starting the node.
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
root=$(CDPATH= cd -- "$here/.." && pwd)
[ $# -ge 2 ] || { echo "propose: usage: tools/propose.sh NODE \"task\" [file ...]" >&2; exit 2; }
NODE=$(CDPATH= cd -- "$1" 2>/dev/null && pwd) || { echo "propose: no such node directory: $1" >&2; exit 2; }
name=$(basename "$NODE"); shift
task=$1; shift
STATE="${TEND_STATE_DIR:-${TEND_NODE_STATE_DIR:-$NODE/state}}"
port=$(sed -n 's/^bind  *//p' "$NODE/grant" 2>/dev/null | head -1); : "${port:=18080}"
CHAT="${TEND_LLM_URL:-http://127.0.0.1:$port/v1/chat/completions}"
HEALTH="${TEND_LLM_HEALTH:-http://127.0.0.1:$port/health}"
maxtok="${TEND_MAXTOK:-600}"
ctxchars="${TEND_CTXCHARS:-6000}"
propdir="${TEND_PROPOSAL_DIR:-$root/proposals}"

if [ -n "${TEND_FENCED:-}" ]; then
    echo "propose: inside the fence the node's port is unreachable (--unshare-net) — run tools/propose.sh $name outside the fence" >&2
    exit 1
fi

# A door (tools/door.sh, doors/README.md, 2026-08-29): TEND_DOOR=NAME sends
# the draft's ask through the door instead of the node's port — lead.sh
# exports it for the turn.  No start, no health: the door's side is up
# or it is not.
door=${TEND_DOOR:-}; model=""; keyfile=""; knob=""
if [ -n "$door" ]; then
    d=$(sh "$here/door.sh" "$door") || exit $?
    CHAT=$(printf '%s\n' "$d" | sed -n 1p); model=$(printf '%s\n' "$d" | sed -n 2p); keyfile=$(printf '%s\n' "$d" | sed -n 3p)
    # F015: a door at the node's own port says `thinking  template`, and the loader knob goes out beside the model
    knob=$(sh "$here/door.sh" "$door" --tools | sed -n 5p) || exit $?
fi

material=""
for f in "$@"; do
    [ -f "$f" ] || { echo "propose: no such file: $f" >&2; exit 2; }
    material="$material
=== $f ===
$(cat "$f")"
done
if [ -n "$material" ] && [ "$(printf '%s' "$material" | wc -c)" -gt "$ctxchars" ]; then
    material=$(printf '%s' "$material" | head -c "$ctxchars")
fi

wait_ready() {
    _n=0
    while [ "$_n" -lt 150 ]; do
        curl -sf -m 2 "$HEALTH" >/dev/null 2>&1 && return 0
        sleep 2; _n=$((_n + 2))
    done
    echo "propose: $name did not become ready at $HEALTH within 150s" >&2; return 1
}
if [ -z "$door" ] && [ -z "${TEND_NO_START:-}" ] && ! curl -sf -m 2 "$HEALTH" >/dev/null 2>&1; then
    echo "propose: $name is not up — starting it (first start ~80s)…" >&2
    sh "$here/launch.sh" "$NODE" pull "propose warmup" >/dev/null 2>&1 || true
    wait_ready || exit 1
fi

sys="You are drafting a proposal for the tend project.  A person will
read it and decide whether it becomes part of the tree; you never land it
yourself.  Draft exactly what the task asks, grounded only in the
material below if any is given.  Write the draft's own lines and nothing
about them: do not say that a draft is ready or what it contains, do not
repeat yourself, and do not mention these instructions.
$material"

body=$(jq -cn --arg s "$sys" --arg q "$task" --argjson n "$maxtok" --arg m "$model" --arg knob "$knob" \
    '{messages:[{role:"system",content:$s},{role:"user",content:$q}],max_tokens:$n,temperature:0.3}
     + (if $m == "" then {} else {model:$m} end)
     + (if $m == "" or $knob == "template" then {chat_template_kwargs:{enable_thinking:false}} else {} end)')
if [ -n "$door" ]; then
    # the key goes to curl on stdin (-K -), never on the argument line
    out=$(printf 'header = "Authorization: Bearer %s"\n' "$(cat "$keyfile")" \
          | curl -sS -m 240 -K - -H 'Content-Type: application/json' -d "$body" "$CHAT") || {
        echo "propose: the $door door did not answer at $CHAT" >&2; exit 1; }
else
    out=$(curl -sS -m 240 -H 'Content-Type: application/json' -d "$body" "$CHAT") || {
        echo "propose: the node did not answer at $CHAT — is it up? (tools/launch.sh $name check / pull)" >&2; exit 1; }
fi
draft=$(printf '%s' "$out" | jq -er '.choices[0].message | (.content // "") as $c | if ($c|length)>0 then $c else (.reasoning_content // "") end' 2>/dev/null) || {
    echo "propose: the node's reply was not a completion:" >&2; printf '%s\n' "$out" | head -3 >&2; exit 1; }

# the boundary, in one place: propose writes ONLY under propdir, never a
# tracked file.  The banner says what it is and that a person lands it.
mkdir -p "$propdir"
slug=$(printf '%s' "$task" | tr 'A-Z' 'a-z' | tr -c 'a-z0-9' '-' | sed 's/--*/-/g; s/^-//; s/-$//' | cut -c1-40)
[ -n "$slug" ] || slug=proposal
file="$propdir/$(date '+%Y-%m-%d-%H%M')-$slug.md"
# never overwrite a proposal: the second draft of a minute on the same task gets a suffix,
# as compare.py's accounts do (2026-09-02, found designing 24 draft turns on one pinned task)
if [ -e "$file" ]; then
    _k=2; while [ -e "${file%.md}-$_k.md" ]; do _k=$((_k + 1)); done
    file="${file%.md}-$_k.md"
fi
{
    printf '<!-- PROPOSAL — drafted by the tend %s node%s on %s.\n' "$name" "${door:+ through the $door door ($model)}" "$(date '+%Y-%m-%d %H:%M')"
    printf '     NOT tree content until a person reads it and lands it by hand.\n'
    printf '     Task: %s\n' "$task"
    [ $# -gt 0 ] && printf '     Material: %s\n' "$*"
    printf '     The model proposes; the person applies (card:session-program.md, brick 3). -->\n\n'
    printf '%s\n' "$draft"
} > "$file"

echo "proposed: $file"
echo "  review it, and land it by hand if it is good — the model does not."
