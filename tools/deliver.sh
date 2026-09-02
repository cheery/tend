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
# The reply is streamed (2026-08-30 — Henri: "I'd like the model to
# stream it's output, so that I can see where it's going in its work"):
# each token is written as it arrives to $STATE/turn.thinking and
# $STATE/turn.answer, the live files the panel's talk screen reads while
# a turn is in flight; when the stream ends they are the whole reply,
# the record is written from them, and they are removed.
# TEND_DOOR=NAME sends the turn through a door (tools/door.sh, doors/)
# instead of the node's port (2026-08-30 — Henri: "I now have the
# openrouter available for use"): the door's url, model and key, the key
# on curl's stdin and never its argument line, as lead.sh does.  Through
# a door the ask is not a pull — a pull starts the local node, and the
# door is another mind — and the exchange carries a `V:` line naming the
# door and its model, so the record says who answered.  Thinking through
# a door is OpenRouter's `reasoning` parameter, and the reasoning comes
# back as `delta.reasoning`; both spellings are read.
# TEND_HISTORY is the conversation so far — a JSON array of prior
# messages, prepended to the ask so the model answers in the
# conversation and not cold (tools/panel.py's talk, 2026-08-30 — Henri:
# "so that I can truly talk with the model"); empty or unset is cold, as
# a pull line always was.
# **Tools** (2026-08-30 — Henri: "would it be time for tools?"; card:tools.md,
# day one): a `tools` line in the door file, or in the node's grant, names
# what the mind may call (`tools  read ls`), and `calls N` caps the calls a
# turn (8 when unsaid; TEND_CALLS overrides); `readchars N` is what one read
# returns before the cut (the executor's 12000 unsaid; TEND_READCHARS overrides
# — the first tooled turn spent five of six reads on halves of cards at gemma's
# number on a 262k door).  With one, the request
# carries the executor's manifest (tools/executor.py --manifest, one line
# per tool) and a system line about the seat — under 150 words, nothing
# about the tree; the tree is read on demand.  A `tool_calls` delta ends
# a round: this runs each call through tools/executor.py under keep —
# read on the tree's parts (tools/sandbox.sh's tree_parts), no net, no
# write — appends the assistant's calls and the `tool` results to the
# turn's messages and asks again, until a round has no calls.  A path
# outside the parts is refused by the kernel and the refusal is what the
# model gets.  Every call is a `C:` line — in `replies` between the Q
# and the A, and in $STATE/turn.calls as it happens, which the talk
# screen shows: the person watches the mind act.  Past the cap a call is
# not run and its result says so; a mind that keeps calling after that
# is stopped one round later and the record says why.  Absent a `tools`
# line, the request carries none, as before.  TEND_TOOLS, set, replaces
# the door's or grant's word — set empty it sends none — tools/compare.py's
# paired arms: the same door, the same model, with and without (2026-08-31).
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
door=$(printenv TEND_DOOR || true); dmodel=""; keyfile=""
tools_word=""; calls_cap=""; readchars=""; temp=""
if [ -n "$door" ]; then
    d=$(sh "$here/door.sh" "$door") || exit $?
    CHAT=$(printf '%s\n' "$d" | sed -n 1p); dmodel=$(printf '%s\n' "$d" | sed -n 2p); keyfile=$(printf '%s\n' "$d" | sed -n 3p)
    t=$(sh "$here/door.sh" "$door" --tools) || exit $?
    tools_word=$(printf '%s\n' "$t" | sed -n 1p); calls_cap=$(printf '%s\n' "$t" | sed -n 2p); readchars=$(printf '%s\n' "$t" | sed -n 3p)
    temp=$(printf '%s\n' "$t" | sed -n 4p)
else
    tools_word=$(sed -n 's/^tools  *//p' "$NODE/grant" 2>/dev/null | head -1)
    calls_cap=$(sed -n 's/^calls  *//p' "$NODE/grant" 2>/dev/null | head -1)
    readchars=$(sed -n 's/^readchars  *//p' "$NODE/grant" 2>/dev/null | head -1)
    temp=$(sed -n 's/^temperature  *//p' "$NODE/grant" 2>/dev/null | head -1)
fi
tools_word="${TEND_TOOLS-$tools_word}"   # set replaces the door's or grant's word, set empty sends none — compare.py's arms
calls_cap="${TEND_CALLS:-${calls_cap:-8}}"
case $calls_cap in ''|*[!0-9]*) echo "deliver: calls wants a number, got \`$calls_cap\`" >&2; exit 2 ;; esac
readchars="${TEND_READCHARS:-$readchars}"   # empty is the executor's own default, so the number lives in one place
case $readchars in *[!0-9]*) echo "deliver: readchars wants a number, got \`$readchars\`" >&2; exit 2 ;; esac
temp="${TEND_TEMP:-${temp:-0.2}}"   # `temperature none` sends none — Anthropic's wire deprecates it (2026-08-31, the smoke's first grade)
case $temp in none) ;; ''|*[!0-9.]*|*.*.*|.) echo "deliver: temperature wants a number or none, got \`$temp\`" >&2; exit 2 ;; esac
think=$(printenv TEND_THINK || true)
if [ -n "$think" ]; then think=true; else think=false; fi
tthink="$STATE/turn.thinking"; tans="$STATE/turn.answer"; tcalls="$STATE/turn.calls"   # the turn in flight, as it arrives
rfile="$STATE/.turn.result"   # one call's result, whole — a variable would drop its last newline
tab=$(printf '\t')
hist=$(printenv TEND_HISTORY || true)
[ -n "$hist" ] || hist='[]'
printf '%s' "$hist" | jq -e 'type == "array"' >/dev/null 2>&1 || {
    echo "deliver: TEND_HISTORY is not a JSON array of messages" >&2; exit 2; }
mkdir -p "$STATE" 2>/dev/null || true

# the tools, when the door or the grant names them: the manifest is the executor's own, the grant
# for each call is built here (Rule 1: from outside the thing bounded) from the fence's tree_parts,
# and the system line says the seat and nothing about the tree
py=/usr/bin/python3; [ -x "$py" ] || py=$(command -v python3) || { echo "deliver: no python3 for keep" >&2; exit 127; }
tree="${TEND_TREE:-$(CDPATH= cd -- "$here/.." && pwd)}"
manifest='[]'; keepflags=""; sysmsgs='[]'
if [ -n "$tools_word" ]; then
    manifest=$("$py" "$here/executor.py" --manifest $tools_word) || exit 2
    for p in $(sed -n 's/^tree_parts="\(.*\)"/\1/p' "$here/sandbox.sh"); do
        [ -e "$tree/$p" ] && keepflags="$keepflags --allow $tree/$p"
    done
    keepflags="--allow $here$keepflags --no-net --write /dev/null"   # the executor's own directory (the tree's tools/, or the installed set), then the parts
    seat="You are answering a person who works on the tend tree at $tree. You have the tools $tools_word over the tree's documents — board/, tools/, spec/, doc/ and the root files — read-only; a path outside them is refused by keep. At most $calls_cap calls this turn; every call is shown to the person as it happens. Read the tree whenever the answer may be in it — a call costs little, a guess costs the record. If you need to know how the tree works, read board/README.md."
    sysmsgs=$(jq -cn --arg s "$seat" '[{role:"system",content:$s}]')
fi

stamp() { date '+%Y-%m-%d %H:%M'; }

# ask the model once, streamed, with the turn's messages so far ($1, a JSON
# array after the history).  The server's SSE lines are one JSON each; jq
# turns every delta into `T<text>`, `A<text>` or `K<tool_calls json>` with
# the text's backslashes, newlines and tabs escaped so a line is a line,
# and the loop appends each to its file with printf %b, which undoes
# exactly that.  Nothing is printed; the files are the reply.  Fails
# loudly when the node did not answer, or answered with no completion.
ask() {
    _conv=$1
    # the node gets its loader knob (chat_template_kwargs); a door gets the model it names, and thinking in its own words
    # the conversation goes to jq in a file, never on its argument line: one
    # execve argument is capped at MAX_ARG_STRLEN (32 pages, 131072 bytes here),
    # and at `readchars 60000` two whole cards cross it — F007
    printf '%s' "$_conv" > "$STATE/.turn.conv"
    _body=$(jq -cn --slurpfile c "$STATE/.turn.conv" --argjson n "$maxtok" --argjson h "$hist" --argjson t "$think" --arg m "$dmodel" \
                   --argjson s "$sysmsgs" --argjson tools "$manifest" --arg tmp "$temp" \
        '{messages:($s + $h + $c[0]),max_tokens:$n,stream:true}
         + (if $tmp == "none" then {} else {temperature:($tmp|tonumber)} end)
         + (if ($tools | length) > 0 then {tools:$tools} else {} end)
         + (if $m == "" then {chat_template_kwargs:{enable_thinking:$t}}
            else {model:$m} + (if $t then {reasoning:{enabled:true}} else {} end) end)')
    # and the body goes to curl in a file for the same reason: `-d "$body"`
    # is one execve argument, and the request is bigger than the reply (F007)
    _bodyf="$STATE/.turn.body"; printf '%s' "$_body" > "$_bodyf"
    _raw="$STATE/.turn.raw"; _rcf="$STATE/.turn.rc"; _tc="$STATE/.turn.tc"; : > "$_tc"
    _had=$(cat "$tans" "$tthink" 2>/dev/null | wc -c)
    { if [ -n "$keyfile" ]; then
          # the key goes to curl on stdin (-K -), never on the argument line (tools/door.sh)
          printf 'header = "Authorization: Bearer %s"\n' "$(cat "$keyfile")" \
            | curl -sSN -m 600 -K - -H 'Content-Type: application/json' --data-binary @"$_bodyf" "$CHAT" 2>>"$_raw"
      else curl -sSN -m 600 -H 'Content-Type: application/json' --data-binary @"$_bodyf" "$CHAT" 2>>"$_raw"; fi
      echo $? > "$_rcf"; } \
      | tee "$_raw" | sed -u 's/^data: //' | grep --line-buffered '^{' \
      | jq --unbuffered -r '.choices[0].delta // {}
            | def esc: gsub("\\\\"; "\\\\") | gsub("\n"; "\\n") | gsub("\t"; "\\t") | gsub("\r"; "\\r");
              ((.reasoning_content // .reasoning // "") | select(length > 0) | "T" + esc),
              ((.content // "") | select(length > 0) | "A" + esc),
              ((.tool_calls // []) | select(length > 0) | "K" + (tojson | esc))' 2>/dev/null \
      | while IFS= read -r _line; do
            _text=${_line#?}
            case $_line in
                T*) printf '%b' "$_text" >> "$tthink" ;;
                A*) printf '%b' "$_text" >> "$tans" ;;
                K*) printf '%b\n' "$_text" >> "$_tc" ;;
            esac
        done
    _rc=$(cat "$_rcf" 2>/dev/null || echo 1); rm -f "$_rcf"
    if [ "$_rc" != 0 ]; then
        # F014 (2026-09-02): curl's own line — `curl: (7) … Connection refused`,
        # a DNS miss, the 600 s timeout — was written to $_raw and deleted
        # unread, so every transport failure read "did not answer".  One line
        # of it travels with the sentence; the body never does (kaizen 1624).
        _why=$(grep -m1 '^curl: (' "$_raw" 2>/dev/null || true)
        [ -n "$_why" ] && _why=" — $_why"
        if [ -n "$door" ]; then echo "deliver: the $door door did not answer at $CHAT$_why" >&2
        else echo "deliver: the node did not answer at $CHAT$_why — is it up? (tools/launch.sh $name check / pull)" >&2; fi
        rm -f "$_raw"; return 1; fi
    if [ "$(cat "$tans" "$tthink" 2>/dev/null | wc -c)" -eq "$_had" ] && [ ! -s "$_tc" ]; then
        # a door's refusal is one line — its code and its words — never the raw body
        # (kaizen 1624: a 429 came through as three lines of JSON under "not a completion")
        _e=$(grep -m1 '^{' "$_raw" 2>/dev/null | jq -r 'select(.error) | .error | if type == "object" then "\(.code // .status // .type // "error") \(.message // .msg // tostring)" else tostring end' 2>/dev/null)
        if [ -n "$_e" ] && [ -n "$door" ]; then echo "deliver: the $door door refused: $_e" >&2
        else echo "deliver: the node's reply was not a completion:" >&2; head -3 "$_raw" >&2; fi
        rm -f "$_raw"; return 1; fi
    rm -f "$_raw"
}

# the round's calls, assembled from the deltas: one object per index — id, name, the arguments whole
round_calls() {
    jq -cs '[.[][]] | group_by(.index) | map({
        id: ((map(.id // empty) | first) // ""),
        name: ((map(.function.name // empty) | first) // ""),
        args: ((map(.function.arguments // "") | add) // "")})' "$STATE/.turn.tc" 2>/dev/null || echo '[]'
}

# one call, run under keep — or not run, past the cap — its C line in _c and its result, whole, in $rfile
ncalls=0
run_call() {
    _name=$1; _arg=$2
    # the line's words are the arguments' values, as the executor prints them; a bare argument is itself
    _shown=$(printf '%s' "$_arg" | jq -R -r 'try (fromjson | if type == "object" then [.[] | tostring] | join(" ") else tostring end) catch .' 2>/dev/null || printf '%s' "$_arg")
    if [ "$ncalls" -ge "$calls_cap" ]; then
        _c="$_name $_shown → out of calls ($calls_cap a turn)"
        printf '%s' "out of calls: $calls_cap a turn — answer with what you have" > "$rfile"
        return 0
    fi
    ncalls=$((ncalls + 1))
    _err="$STATE/.turn.err"
    if _out=$(TEND_TREE="$tree" TEND_READCHARS="$readchars" "$py" "$here/keep.py" $keepflags -- "$py" -B "$here/executor.py" "$_name" "$_arg" 2>"$_err") \
       && printf '%s' "$_out" | jq -e '.c' >/dev/null 2>&1; then
        _c=$(printf '%s' "$_out" | jq -r '.c'); printf '%s' "$_out" | jq -j '.result' > "$rfile"
    else
        # keep would not run it, or the executor did not answer: never run unkept; the line says what was said
        _said=$(grep -v 'DeprecationWarning\|^ *class ' "$_err" 2>/dev/null | tail -1)
        _c="$_name $_shown → not run: ${_said:-the executor said nothing}"; printf '%s' "not run: ${_said:-the executor said nothing}" > "$rfile"
    fi
    rm -f "$_err"
}

# answer one pull line "<epoch> <words>"; nothing if it carries no words.
# A turn is one or more rounds: a round that ends in calls runs them and asks again
answer_line() {
    _line=$1
    _words=$(printf '%s' "$_line" | cut -s -d' ' -f2-)
    [ -n "$_words" ] || return 0
    : > "$tthink"; : > "$tans"; : > "$tcalls"
    conv=$(jq -cn --arg q "$_words" '[{role:"user",content:$q}]')
    ncalls=0; rounds=0; crec=""; stopped=""
    while :; do
        ask "$conv" || return 1
        rounds=$((rounds + 1))
        calls=$(round_calls)
        n=$(printf '%s' "$calls" | jq 'length')
        [ "$n" -gt 0 ] || break
        if [ "$rounds" -gt $((calls_cap + 1)) ]; then
            stopped="(stopped: the model kept calling after it was told it was out of calls, $calls_cap a turn)"
            break
        fi
        # the assistant's message with its calls, then one tool message per call
        amsg=$(printf '%s' "$calls" | jq -c --rawfile a "$tans" \
            '{role:"assistant",content:$a,tool_calls:map({id:.id,type:"function",function:{name:.name,arguments:.args}})}')
        tmsgs='[]'; ci=0
        while [ "$ci" -lt "$n" ]; do
            cid=$(printf '%s' "$calls" | jq -r ".[$ci].id"); cname=$(printf '%s' "$calls" | jq -r ".[$ci].name")
            carg=$(printf '%s' "$calls" | jq -r ".[$ci].args | (try fromjson catch {}) | tojson")   # the arguments as sent; the executor names them
            run_call "$cname" "$carg"
            printf 'C: %s\n' "$_c" >> "$tcalls"
            crec="$crec$(stamp) C: $_c
"
            tmsgs=$(printf '%s' "$tmsgs" | jq -c --arg id "$cid" --rawfile r "$rfile" '. + [{role:"tool",tool_call_id:$id,content:$r}]')
            ci=$((ci + 1))
        done
        # the tool results are the big ones; they ride in a file too (F007)
        printf '%s' "$tmsgs" > "$STATE/.turn.tmsgs"
        conv=$(printf '%s' "$conv" | jq -c --argjson a "$amsg" --slurpfile t "$STATE/.turn.tmsgs" '. + [$a] + $t[0]')
    done
    _a=$(cat "$tans"); thought=$(cat "$tthink")
    # an answer with no content is a model that put its whole reply in the reasoning, and that is the answer
    if [ -z "$_a" ]; then _a=$thought; thought=""; fi
    [ -z "$stopped" ] || _a="$_a${_a:+ }$stopped"
    rm -f "$tans" "$tthink" "$tcalls" "$rfile" "$STATE/.turn.conv" "$STATE/.turn.tmsgs" "$STATE/.turn.tc" "$STATE/.turn.body"
    { printf '%s Q: %s\n' "$(stamp)" "$_words"
      [ -z "$door" ] || printf '%s V: %s %s\n' "$(stamp)" "$door" "$dmodel"
      [ -z "$crec" ] || printf '%s' "$crec"
      [ -z "$thought" ] || printf '%s T: %s\n' "$(stamp)" "$thought"
      printf '%s A: %s\n\n' "$(stamp)" "$_a"; } >> "$replies"
    printf '  Q: %s\n' "$_words"
    [ -z "$door" ] || printf '  via: %s (%s)\n' "$door" "$dmodel"
    [ -z "$crec" ] || printf '%s' "$crec" | sed 's/^[0-9-]* [0-9:]* C: /  C: /'
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
    if [ -n "$q" ] && [ -z "$door" ]; then sh "$here/launch.sh" "$NODE" pull "$q"; fi
    echo "deliver: inside the fence — the ask is recorded; the runner's side delivers it (run tools/deliver.sh $name outside the fence)" >&2
    exit 0
fi

total=$( [ -f "$pull" ] && grep -c . "$pull" || echo 0 )
done_n=$( [ -f "$marker" ] && cat "$marker" || echo -1 )

if [ -n "$q" ] && [ -n "$door" ]; then
    # through a door the ask is not a pull: a pull starts the local node, and the door is another
    # mind.  The exchange is the record, and its V line says who answered
    answer_line "$(date +%s) $q" || exit 1
    exit 0
fi
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
