#!/bin/sh
#: asked-by: Henri, 2026-08-28 — "take session-program" (card:session-program.md, §11:10: "a node that leads work is these three under a loop with the cords")
#
# tools/lead.sh NODE [--kept]
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
#
# **--kept** (or TEND_LEAD_KEPT=1): the turn runs under keep — the tree
# readable, only proposals/, the node's state and the andon record
# writable, one `--connect` to the node's port — so the boundary brick
# 3 held in propose.sh's code is the kernel's: a party may not bound
# itself, and here the party is confined rather than trusted.  The node
# must be up first (`tools/launch.sh NODE pull`), because a runner
# started from inside keep would inherit the confinement.
# TEND_KEPT_PROBE=FILE is the test's proof: after the turn, the kept
# process tries to append to FILE and says `probe: refused` or
# `probe: WROTE` — a board file named there must come back refused.
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
ctxchars="${TEND_CTXCHARS:-20000}"   # the digest's budget in characters, sized to the node's own window
# 5000 until 2026-09-01, and that was the whole of F008: it was chosen for a node at `-c 2048`
# and stayed 5000 when 37092d7 took the node to `-c 8192` on 2026-08-28 — a number that fitted
# one mechanism and was silently wrong for the next, for four days.  20000 chars is ~6700 tokens
# at a pessimistic 3 chars/token; the whole open board was 7516 chars on 2026-09-01, so it fits
# it 2.6 times over.  **This number is not written down anywhere else on purpose**: the window it
# has to fit inside is the `-c` on llm/grant's program line, and that is the number that moves —
# so test_lead.py reads `-c` from the grant and goes red if either end moves without the other,
# which is the only part of this comment that cannot go stale the way 5000 did.
kept=${TEND_LEAD_KEPT:-}; door=${TEND_DOOR:-}
shift
while [ $# -gt 0 ]; do
    case $1 in
        --kept) kept=1 ;;
        --door) door=${2:-}; [ -n "$door" ] || { echo "lead: --door NAME" >&2; exit 2; }; shift ;;
        *) echo "lead: usage: tools/lead.sh NODE [--kept] [--door NAME]" >&2; exit 2 ;;
    esac
    shift
done

if [ -n "${TEND_FENCED:-}" ]; then
    echo "lead: inside the fence the node's port is unreachable (--unshare-net) — run tools/lead.sh $name outside the fence" >&2
    exit 1
fi

# A door (tools/door.sh, doors/README.md — 2026-08-29, Henri: "build
# capability for both gemma and claude"): the same turn, its two asks
# sent through a door instead of the node's port.  No health, no start —
# the door's side is up or it is not — and never under keep: keep's
# --connect is one loopback port and a door calls out.
model=""; keyfile=""
if [ -n "$door" ]; then
    if [ -n "$kept" ]; then
        echo "lead: a kept turn through a door is not built — keep's --connect is one loopback port, and a door calls out; the turn through $door runs on the person's side, unkept, until a leader's reach is a grant row (card:session-program.md)" >&2
        exit 1
    fi
    d=$(sh "$here/door.sh" "$door") || exit $?
    CHAT=$(printf '%s\n' "$d" | sed -n 1p); model=$(printf '%s\n' "$d" | sed -n 2p); keyfile=$(printf '%s\n' "$d" | sed -n 3p)
    export TEND_DOOR="$door"
fi

andon_state="${TEND_ANDON_STATE:-$HOME/.local/state/tend}"
if [ -n "$kept" ]; then
    # re-exec this turn under keep; the grants must exist before keep can name them
    py=/usr/bin/python3; [ -x "$py" ] || py=$(command -v python3)
    cport=$(printf '%s' "$CHAT" | sed -n 's|^http://[^:/]*:\([0-9]*\)/.*|\1|p'); : "${cport:=$port}"
    mkdir -p "$propdir/lead" "$STATE" "$andon_state"
    if ! curl -sf -m 2 "$HEALTH" >/dev/null 2>&1; then
        if ! flock -n "$STATE/run.lock" true 2>/dev/null; then
            # a runner holds the lock and is not answering yet: loading (the llm node takes ~80 s)
            echo "lead: $name is up and not yet answering — waiting for $HEALTH (up to 150s)…" >&2
            _n=0; until curl -sf -m 2 "$HEALTH" >/dev/null 2>&1; do
                [ "$_n" -lt 150 ] || { echo "lead: $name did not become ready within 150s — see $STATE/log" >&2; exit 1; }
                sleep 2; _n=$((_n + 2)); done
        else
            # no runner at all: say what the last one said as it stopped, not just "not up"
            # (Henri, 2026-08-28 13:27: "it should not crash silently" — the loader failure was in the log only)
            echo "lead: $name is not up — a kept turn cannot start a runner; start it first: tools/launch.sh $name pull" >&2
            [ -f "$STATE/stopped" ] && echo "lead: its last stop: $(head -1 "$STATE/stopped")" >&2
            said=$(grep -iv 'deprecationwarning\|^ *class \|^$' "$STATE/log" 2>/dev/null | tail -1)
            [ -n "$said" ] && echo "lead: it last said: $said" >&2
            exit 1
        fi
    fi
    extra=""; case "$board" in "$root"/*) ;; *) extra="--allow $board" ;; esac
    TEND_LEAD_KEPT= TEND_NO_START=1 TEND_LEAD_IN_KEEP=1 \
        exec "$py" "$here/keep.py" --allow "$root" $extra --write "$propdir" --write "$STATE" --write "$andon_state" --write /dev/null \
             --connect "$cport" -- sh "$0" "$NODE"
fi

# the open board, as a digest the node's small context can hold: each
# card on the open shelf, its title and its because — never done/ or
# later/, which are not open work
digest=""; dropped=""; ndrop=0
for c in "$board"/*.md; do
    [ -f "$c" ] || continue
    b=$(basename "$c")
    case $b in README.md) continue ;; esac
    _all=$(sed -n '1p; /^    because/,/^    asked/p' "$c" | grep -v '^    asked')
    _n=$(printf '%s\n' "$_all" | wc -l)
    _keep=$(printf '%s\n' "$_all" | head -8)
    # F009 (2026-09-01): the eight lines are a *summary* of the because, and
    # until today they were an unmarked one — 9 of the 13 open cards ended
    # mid-sentence with nothing said.  A because that stops mid-sentence names
    # a smaller problem than the card's, and the mind cannot tell the two apart.
    if [ "$_n" -gt 8 ]; then
        _keep="$_keep
    [… $((_n - 8)) more lines of this because — the card says more than this]"
    fi
    card="
=== $b ===
$_keep"
    # F008 (2026-08-31): this was one `head -c` after the loop, a byte cut
    # mid-word and mid-card with nothing said — 9 of 13 cards reached the
    # node and it never knew, so it could not pick its priority-1 card.  A
    # cut card is not a shortened card: it is a card that does not exist for
    # the mind being asked to choose.  So the cut falls on a card boundary,
    # and once one card is dropped the rest are — what the node sees is a
    # prefix of the board, never a gap in the middle.  The first card is
    # always carried, even alone over the cap: a digest of nothing is not a
    # smaller digest.
    if [ -z "$dropped" ] && { [ -z "$digest" ] || [ "$(printf '%s%s' "$digest" "$card" | wc -c)" -le "$ctxchars" ]; }; then
        digest="$digest$card"
    else
        ndrop=$((ndrop + 1))
        if [ -z "$dropped" ]; then dropped="$b"; else dropped="$dropped, $b"; fi
    fi
done
[ -n "$digest" ] || { echo "lead: no open cards in $board" >&2; exit 2; }
if [ "$ndrop" -gt 0 ]; then
    _s=cards; [ "$ndrop" -eq 1 ] && _s=card
    # a cap is a gate, and a gate says what it stopped — the same thing the
    # executor's readchars cut says, which this one did not (F008, shape (a))
    digest="$digest

[$ndrop $_s did not fit: $dropped.  The board is longer than this list; these
cards exist and are not shown.  Pull the cord if the one you want is missing.]"
fi

if [ -z "$door" ] && [ -z "${TEND_NO_START:-}" ] && ! curl -sf -m 2 "$HEALTH" >/dev/null 2>&1; then
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
CARD: the filename only, one word ending in .md, from the list below
TASK: the one small thing, in one line
WHY: one line
If you cannot decide, or need the person, answer instead with one line:
ANDON: your question for the person
$digest"
# the node's loader knob (chat_template_kwargs) stays on the node's side; a door gets the model it names
body=$(jq -cn --arg s "$sys" --arg q "Pick." --arg m "$model" \
    '{messages:[{role:"system",content:$s},{role:"user",content:$q}],max_tokens:160,temperature:0.2}
     + (if $m == "" then {chat_template_kwargs:{enable_thinking:false}} else {model:$m} end)')
if [ -n "$door" ]; then
    # the key goes to curl on stdin (-K -), never on the argument line
    out=$(printf 'header = "Authorization: Bearer %s"\n' "$(cat "$keyfile")" \
          | curl -sS -m 240 -K - -H 'Content-Type: application/json' -d "$body" "$CHAT") || {
        echo "lead: the $door door did not answer at $CHAT" >&2; exit 1; }
else
    out=$(curl -sS -m 240 -H 'Content-Type: application/json' -d "$body" "$CHAT") || {
        echo "lead: the node did not answer at $CHAT — is it up? (tools/launch.sh $name check / pull)" >&2; exit 1; }
fi
reply=$(printf '%s' "$out" | jq -er '.choices[0].message | (.content // "") as $c | if ($c|length)>0 then $c else (.reasoning_content // "") end' 2>/dev/null) || {
    echo "lead: the node's reply was not a completion:" >&2; printf '%s\n' "$out" | head -3 >&2; exit 1; }

field() { printf '%s\n' "$reply" | sed -n "s/^[[:space:]]*$1:[[:space:]]*//p" | head -1; }
card=$(field CARD); task=$(field TASK); why=$(field WHY); andon=$(field ANDON)
# the prompt's own typography, echoed (13:57, live: `CARD: <canvas-script.md>`; 18:01: `CARD: canvas.md ===`,
# the digest's fence): the filename is the one thing the open shelf judges, whatever the model wraps it in —
# the first word ending in .md, and an invented card so wrapped is still a pull
card=$(printf '%s' "$card" | grep -o '[A-Za-z0-9_][A-Za-z0-9_.-]*\.md' | head -1 || true)

stamp=$(date '+%Y-%m-%d-%H%M'); now=$(date '+%Y-%m-%d %H:%M')
mkdir -p "$propdir/lead" "$STATE"
# one account per turn: two turns in one minute (13:48, the first live ones) must not share a file
account="$propdir/lead/$stamp.md"; _k=2
while [ -e "$account" ]; do account="$propdir/lead/$stamp-$_k.md"; _k=$((_k + 1)); done
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
    [ -n "$door" ] && printf '    door     %s (%s)\n' "$door" "$model"
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
if [ -n "${TEND_KEPT_PROBE:-}" ]; then
    if echo "probe" >> "$TEND_KEPT_PROBE" 2>/dev/null; then echo "probe: WROTE $TEND_KEPT_PROBE"
    else echo "probe: refused — $TEND_KEPT_PROBE is outside what keep granted${TEND_LEAD_IN_KEEP:+ (under keep)}"; fi
fi
