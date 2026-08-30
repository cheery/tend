#!/bin/sh
#: asked-by: Henri, 2026-08-29 — "build capability for both gemma and claude, also I'm thinking about subscribing to openrouter" (card:session-program.md, card:model-acceptance.md)
#
# tools/door.sh NAME — read a door: where a model that is not the node's is admitted.
#
#     tools/door.sh NAME                    prints three lines — url, model, key file — after checking them
#     tools/door.sh NAME --models [PATTERN] what the door's side lists: id, context, price per M tokens in
#                                           and out, by id; PATTERN keeps the ids that contain it
#     tools/door.sh NAME --use ID           set the door's model line to ID — only an id the door lists
#     tools/door.sh NAME --tools            two lines: the door's `tools` word (empty when it has none) and
#                                           its `calls` cap (empty when unsaid) — card:tools.md, day one
#
# **Browsing and picking** (2026-08-30 — Henri, after a door turn the
# record's V: line showed was Sonnet where he meant qwen: "It's just the
# wrong model in the router itself.. I'd need a way to browse through all
# 500 models there are").  The listing is the door's own (`/models` beside
# `/chat/completions`, the same wire everywhere), and `--use` rewrites the
# one line a person would otherwise edit by hand — refusing an id the door
# does not list, so a typo is refused here and not a 404 on the first
# turn.  The key rides along on the listing request as it does on a turn.
#
# A door is a directory under doors/ (TEND_DOOR_DIR) with a `door` file in
# the grant's shape — a key, two spaces, a value:
#
#     url       https://…/v1/chat/completions      the OpenAI chat wire, which is the
#                                                  wire the node's own port speaks (llama.cpp),
#                                                  OpenRouter's, and Anthropic's compatibility
#                                                  endpoint — one shape, one door reader
#     model     vendor/name                        what the door is asked for; the door's
#                                                  side decides what that name means
#     key       ~/…/name.key                       the person's key, in a file under the
#                                                  person's home — never in the tree
#     admitted  who, when, the words               card:model-acceptance.md: a door is where a
#                                                  refusal has somewhere to sit
#     tools     read ls                            what the mind may call (tools/executor.py's
#                                                  names); absent, the request carries no tools
#     calls     8                                  calls a turn; 8 when unsaid
#
# The node is the default door and needs none of this: `lead.sh NODE` with
# no door speaks to the node's port as it always did.  A door is named by
# `--door NAME` or TEND_DOOR, and the turn runs on the person's side —
# unkept, as every turn did before `--kept` existed — because keep's
# `--connect` is one loopback port and a door calls out.  A leader's reach
# as a grant row is the build that ends that (card:session-program.md).
#
# **The key never leaves this side.**  It is refused when it lives inside
# the tree (every session reads the tree) or when anyone but its owner can
# read it; it goes to curl through `-K -` on stdin, never on the argument
# line, and the account and the proposal name the door, never the key.
set -u
here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
root=$(CDPATH= cd -- "$here/.." && pwd)
doors="${TEND_DOOR_DIR:-$root/doors}"
[ $# -ge 1 ] || { echo "door: usage: tools/door.sh NAME [--models [PATTERN] | --use ID]" >&2; exit 2; }
name=$1; verb=${2:-}; arg=${3:-}   # `mode` below is the key file's
case $verb in ""|--models|--use|--tools) ;; *) echo "door: unknown argument \`$verb\` — tools/door.sh NAME [--models [PATTERN] | --use ID | --tools]" >&2; exit 2 ;; esac
case $name in ''|*/*|.*) echo "door: not a door's name: \`$name\`" >&2; exit 2 ;; esac
f="$doors/$name/door"
[ -f "$f" ] || { echo "door: no door named $name in $doors" >&2; exit 2; }
field() { sed -n "s/^$1  *//p" "$f" | head -1; }
url=$(field url); model=$(field model); key=$(field key)
[ -n "$url" ] && [ -n "$model" ] && [ -n "$key" ] || { echo "door: $f needs url, model and key lines" >&2; exit 2; }
case $key in "~/"*) key="${HOME:?door: no HOME to find $key under}/${key#\~/}" ;; esac
case $key in
    "$root"/*) echo "door: $name's key $key is inside the tree — every session reads the tree; put it under your home" >&2; exit 2 ;;
    /*) ;;
    *) echo "door: $name's key must be an absolute path or ~/…, not \`$key\`" >&2; exit 2 ;;
esac
[ -f "$key" ] || { echo "door: $name's key file is not there: $key (umask 077; printf '%s\\n' KEY > $key)" >&2; exit 2; }
[ -r "$key" ] || { echo "door: $name's key file is not readable by you: $key" >&2; exit 2; }
mode=$(stat -c '%a' "$key" 2>/dev/null || echo 000)
case $mode in
    *00) ;;
    *) echo "door: $name's key $key is readable by others (mode $mode) — chmod 600 it" >&2; exit 2 ;;
esac
[ -n "$verb" ] || { printf '%s\n%s\n%s\n' "$url" "$model" "$key"; exit 0; }
[ "$verb" != --tools ] || { printf '%s\n%s\n' "$(field tools)" "$(field calls)"; exit 0; }

# The door's side, listed: one line per model — id, context, $/M in, $/M out — by id.
base=${url%/chat/completions}
listing() {
    _l=$(printf 'header = "Authorization: Bearer %s"\n' "$(cat "$key")" | curl -sS -m 30 -K - "$base/models") \
        || { echo "door: $name did not answer at $base/models" >&2; return 1; }
    _rows=$(printf '%s' "$_l" | jq -r '.data[]? | [.id, ((.context_length // 0) | tostring),
        ((((.pricing.prompt // "0") | tonumber) * 1000000 * 100 | round) / 100 | tostring),
        ((((.pricing.completion // "0") | tonumber) * 1000000 * 100 | round) / 100 | tostring)] | @tsv' 2>/dev/null | sort)
    [ -n "$_rows" ] || { echo "door: $name's listing at $base/models names no models:" >&2; printf '%s\n' "$_l" | head -3 >&2; return 1; }
    printf '%s\n' "$_rows"
}
listed() { listing | cut -f1 | grep -qxF -- "$1"; }

case $verb in
    --models)
        rows=$(listing) || exit 1
        total=$(printf '%s\n' "$rows" | grep -c .)
        if [ -n "$arg" ]; then rows=$(printf '%s\n' "$rows" | grep -i -- "$arg" || true); fi
        shown=$(printf '%s\n' "$rows" | grep -c .)
        [ -z "$rows" ] || printf '%s\n' "$rows" | awk -F'\t' '{ printf "  %-48s %8s ctx  $%s/M in  $%s/M out\n", $1, $2, $3, $4 }'
        if [ -n "$arg" ]; then echo "door: $name lists $total models, $shown matching \`$arg\`; the door's model is $model"
        else echo "door: $name lists $total models; the door's model is $model"; fi ;;
    --use)
        [ -n "$arg" ] || { echo "door: --use ID" >&2; exit 2; }
        case $arg in *[!A-Za-z0-9._:/-]*) echo "door: not a model id: \`$arg\`" >&2; exit 2 ;; esac
        listed "$arg" || { echo "door: $name does not list \`$arg\` — tools/door.sh $name --models $arg" >&2; exit 2; }
        sed -i "s|^model  .*|model  $arg|" "$f"
        echo "door: $name's model is $arg (was $model)" ;;
esac
