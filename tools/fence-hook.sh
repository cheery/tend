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

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# The tree this governs: TEND_TREE when installed (tools/install.sh), else the
# parent of this file.  The leash and the sandbox are this file's siblings —
# the installed hook runs the installed fence, never the tree's copy — and
# the sandbox is told the tree the same way.
root="${TEND_TREE:-$(cd "$here/.." && pwd)}"
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

# card:rewritten-command.md day one — the route, refused.
#
# The harness substitutes braced shell expansions into a session's own
# command text before it runs — inside a quoted heredoc, where the shell
# itself would not — so a session writes one thing and another executes,
# at exit 0, leaving a hole and not an error.  It reached committed files
# twice (`tools/consult.sh` shipped "trimmed to  chars", no number,
# 01f422e and c6e9fc5, 2026-08-28) and fired five times in the sitting
# that carded it, twice inside the prose recording it.
#
# **A hook cannot see this defect.**  The rewrite happens before the tool
# call is handed here, so the expansion is already gone from what arrives:
# an empty pair of backticks, a doubled space.  There is nothing to
# detect, and a check for braced forms would inspect text they have
# already vanished from.  So what is refused is the *route* — a heredoc
# that writes a file — and the session is sent to a tool whose text does
# not pass through a shell.  This is card:lost-write.md's shape: the
# announced half of this defect already prints a warning, and the warning
# was read and worked past three times in one sitting, so annotating the
# route was never going to be the fix.
#
# **The boundary, which is the whole of the build.**  A redirect is looked
# for only in the text *before* the first heredoc marker — that is the
# command line, and inside a python body `>` is a comparison, not a
# redirect.  `test_fence_hook.py` holds both directions, and the
# comparison case is the false positive that would have made this rule
# unusable.  A heredoc that only computes and prints is untouched.
if [[ $cmd == *"<<"* ]]; then
  head_="${cmd%%<<*}"
  # /dev/null and >&N are not writes; drop them before looking for one
  head_="$(printf '%s' "$head_" | sed 's|[0-9]*>>*[[:space:]]*/dev/null||g; s|>&[0-9-]*||g')"
  writes=""
  if printf '%s' "$head_" | grep -qE '(^|[^0-9])>>?[[:space:]]*[^|[:space:]]'; then
    writes="a redirect on the command line"
  elif printf '%s' "$head_" | grep -qE '(^|[[:space:]])tee([[:space:]]|$)'; then
    writes="a tee on the command line"
  # The body is scanned as *code* only when something is going to run it as
  # code — the head names an interpreter.  Otherwise the heredoc is data:
  # `git commit -F -` carries a message, and this tree's messages talk about
  # code all day.  Measured 2026-09-01 against the sitting's own commands: a
  # commit message containing `write_text(` was the rule's one false refusal
  # before this line, and commit messages are how the tree keeps its record.
  #
  # `open(` needs its *mode*, the argument after the comma: `open('x')` is a
  # read, and its variable name must not be mistaken for a mode letter — the
  # first run of this rule refused a measurement because the `x` in
  # `open('x')` matched, which is why the comma is here.
  elif printf '%s' "$head_" | grep -qE '(^|[[:space:]/])(python[0-9.]*|perl|ruby|node|bash|sh|zsh)([[:space:]]|$)' \
       && printf '%s' "$cmd" | grep -qE "write_text\(|\.writelines\(|\.write\(|json\.dump\(|open\([^)]*,[^)]*['\"][wax]"; then
    writes="a write call inside the heredoc"
  fi
  if [[ -n $writes ]]; then
    jq -n --arg w "$writes" '{
      hookSpecificOutput: {
        hookEventName: "PreToolUse",
        permissionDecision: "deny",
        permissionDecisionReason: ("fence: this heredoc writes a file (" + $w + "), and the harness silently drops braced shell expansions from a heredoc before it runs — a hole at exit 0, committed twice already.  Use the Write tool for the file, then grep the result.  A heredoc that only computes and prints is fine.  card:rewritten-command.md")
      }
    }'
    exit 0
  fi
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
  wrapped="TEND_TREE=$root $here/leash.sh -- $here/sandbox.sh --reach $reach bash -c $quoted"
else
  wrapped="TEND_TREE=$root $here/leash.sh -- $here/sandbox.sh bash -c $quoted"
fi

jq -n --arg w "$wrapped" --arg r "$reach" \
      --argjson orig "$(printf '%s' "$payload" | jq '.tool_input')" '{
  hookSpecificOutput: {
    hookEventName: "PreToolUse",
    updatedInput: ($orig + {command: $w}),
    permissionDecisionReason: ("leashed and fenced: tools/leash.sh -- tools/sandbox.sh" + (if $r == "" then "" else " --reach " + $r end))
  }
}'
