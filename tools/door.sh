#!/bin/sh
#: asked-by: Henri, 2026-08-29 — "build capability for both gemma and claude, also I'm thinking about subscribing to openrouter" (card:session-program.md, card:model-acceptance.md)
#
# tools/door.sh NAME — read a door: where a model that is not the node's is admitted.
#
#     tools/door.sh NAME      prints three lines — url, model, key file — after checking them
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
[ $# -eq 1 ] || { echo "door: usage: tools/door.sh NAME" >&2; exit 2; }
name=$1
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
printf '%s\n%s\n%s\n' "$url" "$model" "$key"
