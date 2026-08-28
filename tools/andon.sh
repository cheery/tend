#!/bin/sh
#: asked-by: Henri, 2026-08-24 — "add the needed cards so that the absent work is completed" (card:cords.md); taken into a batch on 2026-08-27, "cords could be taken now into this batch"
#
# tools/andon.sh — pull the cord.  A session needs a person, and says what for first.
#
#     tools/andon.sh ask "the question"   write the question down; no sound
#     tools/andon.sh ring [N]             ring N times (1..3, 8 s apart) — refused
#                                         with nothing asked, and within 10 min
#                                         of the last ring
#     tools/andon.sh pending              the unanswered questions
#     tools/andon.sh pulled [-q]          exit 0 if a ring is unanswered — the
#                                         record `tools/limit.sh` reads for
#                                         `sitting N because andon`
#     tools/andon.sh answered             the person's: clear the questions
#     tools/andon.sh relay                the person's: sound a ring the fence could not —
#                                         each `ring-failed` once, then `relayed`; the
#                                         resolver's hook runs it (card:silent-cord.md)
#
# **Borrowed in shape from `~/gestate/tools/andon.sh` (2026-08-17: "I am
# here for you in need"), and changed in two ways.**  Gestate rings a
# score through its own synth; tend has no synth and needs *a* cord, not
# that cord (card:cords.md), so the sound is a two-note tone written
# with python's `wave` and played through the PipeWire socket — the
# first row Henri ever put in `TEND_REACH_ALLOW` was `audio`, for this.
# And gestate's cord is sound only; tend's has a **record**: the
# questions are written before the ring, so that what reaches the
# person is a list and not a noise, and so that a program — the sitting
# limit's `andon` reason — can read whether a cord is pulled and
# unanswered without asking the session, which would be asking the
# restrained party.  The record is `~/.local/state/tend/andon.pending`
# (the questions) and `andon.log` (every ask, ring and answer, dated);
# the state row carries both through the fence.
#
# **Deliberately hard to make loud or frequent**, gestate's rule kept
# with its numbers: at most three rings a call, eight seconds apart —
# if three did not reach him he is not in the room — and a second
# `ring` within ten minutes of the first is refused, because ringing
# again into the same silence is waiting at volume for him to walk
# back in.  A ring with nothing asked is refused too: the question is
# the point, the sound is only how it travels.
#
# **Inside the fence the sound needs the row**: `REACH=audio
# tools/andon.sh ring`.  Without it the player cannot reach the socket
# and this says so and exits 1, never silently — the one failure a
# cord may not have.  `answered` is the person's word and is refused
# inside the fence, the way `tools/limit.sh reset` is: a session that
# could answer its own question would be verifying its own reason.
#
# **The ring crosses the seam** (2026-08-28, card:silent-cord.md — Henri:
# "the andon needs to sound even with no sound allowed").  A cord a
# session must be granted reach to pull is not a cord: narrowing the
# reach is the normal act, and it cut the one line a stuck session has.
# So a fenced ring that fails at the player is still a pull — `pulled`
# and the quiet window count `ring-failed` as a ring — and the sound is
# the person's side's: `relay` reads the record, plays each failed ring
# once through the real player where the socket is, and writes
# `relayed`.  It is run by `tools/resolve.sh --hook`, on the person's
# side after every command, never as a daemon; it carries nothing but
# the fact that the record has a ring in it, and it is refused inside
# the fence like `answered`.  The panel (tools/andon-panel.py) hears the
# same failed ring while it is open; relay is for when it is not.
#
# **What a session can do with this, honestly**: ask and ring — which
# is loud, on purpose — and get `sitting N because andon` while the
# ring is unanswered.  A ring for nothing is a ring the person hears;
# that is the check, and it is not a program's.
set -eu

state="${TEND_ANDON_STATE:-$HOME/.local/state/tend}"
pending="$state/andon.pending"
log="$state/andon.log"
gap="${TEND_ANDON_GAP:-8}"          # seconds between rings
quiet="${TEND_ANDON_QUIET:-600}"    # seconds a ring buys of silence
player="${TEND_ANDON_PLAYER:-}"     # a command that plays a wav; tests set it

mode="${1:-pending}"
[ $# -gt 0 ] && shift
now=$(date +%s)
# the two-note tone, written with wave; $1 the path
make_wav() {
    python3 - "$1" <<'PY'
import math, struct, sys, wave
path = sys.argv[1]; rate = 22050
def tone(f, secs, vol=0.35):
    n = int(rate * secs)
    for i in range(n):
        env = min(1.0, i / (rate * 0.02), (n - i) / (rate * 0.10))
        yield vol * env * math.sin(2 * math.pi * f * i / rate)
s = list(tone(660, 0.30)) + [0.0] * int(rate * 0.05) + list(tone(880, 0.45))
with wave.open(path, "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate)
    w.writeframes(b"".join(struct.pack("<h", int(x * 32767)) for x in s))
PY
}
# a player that can reach a sound card from here, or empty
find_player() {
    [ -n "$player" ] && { echo "$player"; return; }
    for c in pw-play paplay aplay; do command -v "$c" >/dev/null 2>&1 && { echo "$c"; return; }; done
}
stamp() { date -d "@$now" '+%Y-%m-%d %H:%M'; }
note() { mkdir -p "$state"; printf '%s %s %s\n' "$now" "$(stamp)" "$*" >> "$log"; }
count() { if [ -f "$pending" ]; then grep -c . "$pending" || true; else echo 0; fi; }

case "$mode" in
    ask)
        q=$(printf '%s' "${1:-}" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')   # a space is nothing asked (18:00)
        [ -n "$q" ] || { echo "andon: nothing asked — tools/andon.sh ask \"the question\"" >&2; exit 2; }
        mkdir -p "$state"
        printf '%s %s\n' "$(stamp)" "$q" >> "$pending"
        note "ask $q"
        echo "andon: asked ($(count) pending).  tools/andon.sh ring when the batch is ready."
        ;;
    pending)
        n=$(count)
        if [ "$n" -eq 0 ]; then echo "andon: nothing pending."; else
            echo "andon: $n pending —"; sed 's/^/  /' "$pending"; fi
        ;;
    pulled)
        # A cord is pulled when there is a question and a ring since the
        # last answer.  Ask without ring is a draft; ring without a
        # question cannot happen (refused below).
        n=$(count)
        # a ring that could not sound (the row off, the fence) is a pull all the same — card:silent-cord.md
        last_ring=$( [ -f "$log" ] && awk '$4=="ring"||$4=="ring-failed"{r=$1} $4=="answered"{r=""} END{print r}' "$log" || true )
        if [ "$n" -gt 0 ] && [ -n "$last_ring" ]; then
            [ "${1:-}" = -q ] || echo "andon: pulled — $n unanswered since $(date -d "@$last_ring" '+%H:%M')"
            exit 0
        fi
        [ "${1:-}" = -q ] || echo "andon: not pulled — $n pending, $( [ -n "$last_ring" ] && echo "rung" || echo "no ring since the last answer")"
        exit 1
        ;;
    ring)
        times="${1:-1}"
        case $times in ''|*[!0-9]*) echo "andon: \`$times\` is not a number of rings" >&2; exit 2 ;; esac
        [ "$times" -lt 1 ] && times=1
        [ "$times" -gt 3 ] && times=3
        n=$(count)
        [ "$n" -gt 0 ] || { echo "andon: nothing asked — a ring with no question is noise.  tools/andon.sh ask \"...\" first" >&2; exit 2; }
        last_ring=$( [ -f "$log" ] && awk '$4=="ring"||$4=="ring-failed"{r=$1} END{print r}' "$log" || true )
        if [ -n "$last_ring" ] && [ $((now - last_ring)) -lt "$quiet" ]; then
            echo "andon: rang at $(date -d "@$last_ring" '+%H:%M'), $(( (now - last_ring) / 60 )) min ago — he heard it or is not in the room; not ringing again for $(( (quiet - now + last_ring) / 60 + 1 )) min" >&2
            exit 3
        fi
        echo "andon: ringing $times — $n pending:"; sed 's/^/  /' "$pending"
        wav="${TMPDIR:-/tmp}/tend-andon-$$.wav"
        make_wav "$wav"
        player=$(find_player)
        [ -n "$player" ] || { rm -f "$wav"; echo "andon: no player (pw-play, paplay, aplay) — could not reach the sound card" >&2; exit 1; }
        i=0
        while [ "$i" -lt "$times" ]; do
            [ "$i" -gt 0 ] && sleep "$gap"
            if ! $player "$wav" >/dev/null 2>&1; then
                rm -f "$wav"
                note "ring-failed player=$player pending=$n"
                echo "andon: could not reach the sound card ($player) — inside the fence the row is off: REACH=audio tools/andon.sh ring" >&2
                exit 1
            fi
            i=$((i + 1))
        done
        rm -f "$wav"
        note "ring n=$times pending=$n"
        echo "andon: rang $times."
        ;;
    answered)
        if [ "${TEND_FENCED:-}" = 1 ]; then
            echo "andon: answered is the person's word, from outside the fence — a session cannot answer its own question" >&2; exit 2
        fi
        n=$(count)
        [ "$n" -gt 0 ] || { echo "andon: nothing pending."; exit 0; }
        sed 's/^/answered: /' "$pending" | while IFS= read -r line; do note "$line"; done
        note "answered n=$n"
        : > "$pending"
        echo "andon: $n answered."
        ;;
    relay)
        # the person's side: a ring the fence could not sound, sounded here — once per failed ring
        if [ "${TEND_FENCED:-}" = 1 ]; then
            echo "andon: relay is the person's word, from outside the fence — a session cannot carry its own ring across" >&2; exit 2
        fi
        [ -f "$log" ] || exit 0
        # by the record's order, not the clock: a failed ring and its relay can share a second
        failed=$(awk '$4=="ring-failed"{f=$1; n=NR} $4=="relayed"{r=NR} $4=="answered"{f=""} END{if (f != "" && n > r) print f}' "$log")
        [ -n "$failed" ] || exit 0
        n=$(count)
        player=$(find_player)
        [ -n "$player" ] || { echo "andon: relay — no player (pw-play, paplay, aplay) on the person's side; $n pending, the ring at $(date -d "@$failed" '+%H:%M') is unsounded" >&2; exit 1; }
        wav="${TMPDIR:-/tmp}/tend-andon-$$.wav"
        make_wav "$wav"
        if $player "$wav" >/dev/null 2>&1; then
            rm -f "$wav"; note "relayed player=$player pending=$n for=$failed"
            echo "andon: relayed the ring of $(date -d "@$failed" '+%H:%M') — $n pending"
        else
            rm -f "$wav"; echo "andon: relay — $player could not play on the person's side either; $n pending" >&2; exit 1
        fi
        ;;
    -h|--help) sed -n '4,17p' "$0" | sed 's/^# \{0,1\}//' ;;
    *) echo "andon: unknown word \`$mode\` — ask, ring, pending, pulled, answered, relay" >&2; exit 2 ;;
esac
