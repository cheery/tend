#!/bin/sh
#: asked-by: Henri, 2026-08-28 — "take session-program" (card:session-program.md, §11:10: "a node that leads work is these three under a loop with the cords")
#
# tools/lead.sh NODE
#
# One led turn.  The three bricks — deliver, consult, propose — put under
# a loop with the cords: the node reads the open board, names one card
# and one small thing, and either proposes it (through propose.sh, into
# the gitignored proposals area — never a tracked file) or, when it
# cannot decide, pulls the andon: `andon.sh ask`, the record, no reach
# row, which the panel outside the fence turns into a sound
# (card:andon-panel.md).  Either way it writes its own account of the
# turn under proposals/lead/ — the node's lamp, the reflective account
# the card said waits for the first node that leads.
#
# The model's word is not trusted for the card: a name that is not on
# the open shelf is a cord pull, not a proposal on a card that does not
# exist.  A reply with no shape is a cord pull too — a node that leads
# and cannot say what it picked is exactly the node that should ask.
#
# Runs on the person's side (it reaches the port), one turn per call;
# the sitting limit in the node's grant is the clock over any loop of
# these.  Env: TEND_BOARD_DIR (default <tree>/board); TEND_PROPOSAL_DIR;
# TEND_ANDON_STATE; TEND_LLM_URL / TEND_LLM_HEALTH; TEND_NO_START.
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
root=$(CDPATH= cd -- "$here/.." && pwd)
[ $# -ge 1 ] || { echo "lead: usage: tools/lead.sh NODE" >&2; exit 2; }
NODE=$(CDPATH= cd -- "$1" 2>/dev/null && pwd) || { echo "lead: no such node directory: $1" >&2; exit 2; }
name=$(basename "$NODE")
STATE="${TEND_STATE_DIR:-${TEND_NODE_STATE_DIR:-$NODE/state}}"
board="${TEND_BOARD_DIR:-$root/board}"
propdir="${TEND_PROPOSAL_DIR:-$root/proposals}"
port=$(sed -n 's/^bind  *//p' "$NODE/grant" 2>/dev/null | head -1); : "${port:=18080}"
CHAT="${TEND_LLM_URL:-http://127.0.0.1:$port/v1/chat/completions}"
HEALTH="${TEND_LLM_HEALTH:-http://127.0.0.1:$port/health}"
ctxchars="${TEND_CTXCHARS:-5000}"

if [ -n "${TEND_FENCED:-}" ]; then
    echo "lead: inside the fence the node's port is unreachable (--unshare-net) — run tools/lead.sh $name outside the fence" >&2
    exit 1
fi

# the open board, as a digest the node's small context can hold: each
# card on the open shelf, its title and its because — never done/ or
# later/, which are not open work
digest=""
for c in "$board"/*.md; do
    [ -f "$c" ] || continue
    case $(basename "$c") in README.md) continue ;; esac
    digest="$digest
=== $(basename "$c") ===
$(sed -n '1p; /^    because/,/^    asked/p' "$c" | grep -v '^    asked' | head -8)"
done
[ -n "$digest" ] || { echo "lead: no open cards in $board" >&2; exit 2; }
if [ "$(printf '%s' "$digest" | wc -c)" -gt "$ctxchars" ]; then
    digest=$(printf '%s' "$digest" | head -c "$ctxchars")
fi

if [ -z "${TEND_NO_START:-}" ] && ! curl -sf -m 2 "$HEALTH" >/dev/null 2>&1; then
    echo "lead: $name is not up — starting it (first start ~80s)…" >&2
    sh "$here/launch.sh" "$NODE" pull "lead warmup" >/dev/null 2>&1 || true
    _n=0; until curl -sf -m 2 "$HEALTH" >/dev/null 2>&1; do
        [ "$_n" -lt 150 ] || { echo "lead: $name did not become ready within 150s" >&2; exit 1; }
        sleep 2; _n=$((_n + 2)); done
fi

sys="You are leading one turn of work on the tend project's board.  Below
are the open cards: each one's title and the problem it names.  Pick ONE
card and ONE small thing that could be drafted for it now — a few lines,
not a build.  Answer in exactly this shape, three lines, nothing else:
CARD: <filename from the list>
TASK: <the one small thing, one line>
WHY: <one line>
If you cannot decide, or need the person, answer instead with one line:
ANDON: <your question for the person>
$digest"
body=$(jq -cn --arg s "$sys" --arg q "Pick." \
    '{messages:[{role:"system",content:$s},{role:"user",content:$q}],max_tokens:160,temperature:0.2,chat_template_kwargs:{enable_thinking:false}}')
out=$(curl -sS -m 240 -H 'Content-Type: application/json' -d "$body" "$CHAT") || {
    echo "lead: the node did not answer at $CHAT — is it up? (tools/launch.sh $name check / pull)" >&2; exit 1; }
reply=$(printf '%s' "$out" | jq -er '.choices[0].message | (.content // "") as $c | if ($c|length)>0 then $c else (.reasoning_content // "") end' 2>/dev/null) || {
    echo "lead: the node's reply was not a completion:" >&2; printf '%s\n' "$out" | head -3 >&2; exit 1; }

field() { printf '%s\n' "$reply" | sed -n "s/^[[:space:]]*$1:[[:space:]]*//p" | head -1; }
card=$(field CARD); task=$(field TASK); why=$(field WHY); andon=$(field ANDON)

stamp=$(date '+%Y-%m-%d-%H%M'); now=$(date '+%Y-%m-%d %H:%M')
mkdir -p "$propdir/lead" "$STATE"
account="$propdir/lead/$stamp.md"
outcome=""; result=""

pull() {
    # the cord: the record, no reach row — the panel outside makes the sound
    sh "$here/andon.sh" ask "$name (lead): $1" >/dev/null
    outcome="andon"; result="$1"
    echo "andon: $name pulled the cord — $1"
}

if [ -n "$andon" ]; then
    pull "$andon"
elif [ -z "$card" ] || [ -z "$task" ]; then
    pull "my reply had no CARD/TASK shape; what should I take? (reply was: $(printf '%s' "$reply" | head -c 200))"
elif [ ! -f "$board/$card" ] || [ "$card" = README.md ]; then
    pull "I named $card and it is not on the open board; which card is mine?"
else
    res=$(TEND_STATE_DIR="$STATE" TEND_PROPOSAL_DIR="$propdir" TEND_NO_START=1 \
          sh "$here/propose.sh" "$NODE" "$task" "$board/$card") || {
        outcome="failed"; result="propose.sh did not draft"; }
    [ -n "$outcome" ] || { outcome="proposed"; result=$(printf '%s\n' "$res" | sed -n 's/^proposed: //p'); }
    printf '%s\n' "$res"
fi

# the lamp: the node's own account of the turn, beside its proposals,
# never in the tree
{
    printf '<!-- LEAD ACCOUNT — one turn of the tend %s node, %s.\n' "$name" "$now"
    printf '     The node'"'"'s own account of what it did; a person reads it (card:session-program.md, the lamp). -->\n\n'
    printf '# %s led one turn — %s\n\n' "$name" "$now"
    printf '    read     the open board: %s\n' "$(cd "$board" && ls *.md | grep -v README.md | tr '\n' ' ')"
    printf '    picked   %s\n' "${card:-—}"
    printf '    task     %s\n' "${task:-—}"
    printf '    why      %s\n' "${why:-—}"
    printf '    outcome  %s — %s\n' "$outcome" "$result"
    printf '\nThe reply, verbatim:\n\n'
    printf '%s\n' "$reply" | sed 's/^/    /'
} > "$account"
printf '%s lead %s %s\n' "$now" "$outcome" "${card:-}" >> "$STATE/lead.log"
echo "account: $account"
