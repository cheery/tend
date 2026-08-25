#!/usr/bin/env bash
#: asked-by: Henri, 2026-08-25 — "show me the hook"; then he ran ~/hook-installer.sh against a hook that did not exist yet, which is the word
#
# tools/fence-hook.sh — every shell command a session runs, runs under the leash, inside the fence.
#
# A `PreToolUse` hook on `Bash`.  Claude Code hands it the tool call as
# JSON on stdin before running it; this rewrites the command to run under
# `tools/leash.sh` and, within that, `tools/sandbox.sh` — or refuses it
# out loud.  Installed by Henri, with `~/hook-installer.sh`, because hook
# config is enforcement and the settings file is his.
#
# **Borrowed from `~/gestate/tools/fence-hook.sh` and inverted.**  Gestate
# wraps `pytest` and `cargo` and nothing else, because its fence answers
# one threat — dependency code executing — and wrapping more would be
# theatre.  Tend's fence is about the session's *reach*, and on
# 2026-08-25 it held the session's whole work with the cords passing
# through (doc/experiments/2026-08-25-both.md).  So here the default is
# the other way up: **everything is wrapped**, and the failure mode
# flips with it — in gestate a false wrap breaks a build; here a false
# non-wrap is the hole.  What gestate learned about quoting is kept
# whole: `jq -Rsr ... @sh`, raw in and raw out, because the JSON-encoded
# form reached bash with its escapes doubled.
#
# **The two dials are turned together, and in this order: the leash
# outside, the fence inside** (card:grant.md, measured 2026-08-25).  The
# budget is a cgroup the user manager makes, and the manager spawns
# what it is asked to on the host — so a bus socket handed *inside* the
# fence let a fenced session run anything unfenced through it.  An
# escape, not a dial.  The other order — fence outside, leash inside —
# was what this hook did first, and the ledger said `plain` for every
# fenced run.  Now the hook, which runs on the host, starts the scope
# there; bwrap and the whole fenced tree live inside it, the quota binds
# (measured: 1.51 CPU-s for 3 s at 50%), and stopping the scope reaps
# everything the command left behind.  The leash's defaults are the
# grant for now; a session cannot ask for more, and the ledger line at
# `~/.local/state/tend/leash.log` is the observer.
#
# **The dial, and who holds it.**  A command may ask for rows the fence
# keeps off — `REACH=audio tools/andon.sh` — and the request is granted
# only if every row is in `TEND_REACH_ALLOW`, which is set in the hook's
# own line in `.claude/settings.json`: Henri's bound.  A request outside
# it is refused with a reason a session can read, never silently
# narrowed, because a session may not widen its own reach and must not
# be left guessing why a command did nothing.  With no bound set, no
# row may be asked for.
#
# **Skipped, on purpose**: an empty command, and one that already names
# `tools/sandbox.sh` — the fence cannot nest, and `--check` must run
# outside to grade the escape.  There is no `NOFENCE=1`.  The way to run
# something unfenced in this tree is to ask the person, who can widen
# the bound; that is the whole point of the arrangement.
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
allow="${TEND_REACH_ALLOW:-}"

payload="$(cat)"
cmd="$(printf '%s' "$payload" | jq -r '.tool_input.command // ""')"

# Only the fence's own two read-only forms pass through, and only when
# the command is exactly one of them: `--check` must run outside to grade
# the escape, and `--rows` is a listing.  The first version skipped any
# command *containing* `tools/sandbox.sh` — and the first command a
# session ran under the hook, `sh -n tools/sandbox.sh; ...probes...`, ran
# unfenced through it (doc/kaizen/2026-08-25-0714.md).  Anything else
# that names the fence is wrapped like everything else, and nests, and
# fails out loud.
[[ -z $cmd ]] && exit 0
if [[ $cmd =~ ^[[:space:]]*([^[:space:]]*/)?tools/sandbox\.sh[[:space:]]+(--check|--rows)[[:space:]]*$ ]]; then
  exit 0
fi

# The request: a leading `REACH=row,row `.
reach=""
if [[ $cmd =~ ^[[:space:]]*REACH=([a-z,]+)[[:space:]]+(.*)$ ]]; then
  reach="${BASH_REMATCH[1]}"
  cmd="${BASH_REMATCH[2]}"
fi

IFS=, read -ra rows <<<"$reach"
for row in "${rows[@]}"; do
  [[ -z $row ]] && continue
  if [[ ",$allow," != *",$row,"* ]]; then
    jq -n --arg r "$row" --arg a "${allow:-none}" '{
      hookSpecificOutput: {
        hookEventName: "PreToolUse",
        permissionDecision: "deny",
        permissionDecisionReason: ("fence: the row `" + $r + "` is outside the bound Henri set (allowed: " + $a + ").  A session may not widen its own reach; ask him.  tools/sandbox.sh --rows")
      }
    }'
    exit 0
  fi
done

quoted="$(printf '%s' "$cmd" | jq -Rsr 'rtrimstr("\n") | @sh')"
if [[ -n $reach ]]; then
  wrapped="$root/tools/leash.sh -- $root/tools/sandbox.sh --reach $reach bash -c $quoted"
else
  wrapped="$root/tools/leash.sh -- $root/tools/sandbox.sh bash -c $quoted"
fi

jq -n --arg w "$wrapped" --arg r "$reach" \
      --argjson orig "$(printf '%s' "$payload" | jq '.tool_input')" '{
  hookSpecificOutput: {
    hookEventName: "PreToolUse",
    updatedInput: ($orig + {command: $w}),
    permissionDecisionReason: ("leashed and fenced: tools/leash.sh -- tools/sandbox.sh" + (if $r == "" then "" else " --reach " + $r end))
  }
}'
