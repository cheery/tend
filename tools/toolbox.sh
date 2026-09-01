#!/bin/sh
#: asked-by: Henri, 2026-08-24 — "please create a tools/toolbox.sh to install all tools you need, also those that are present."
#
# tools/toolbox.sh — set this clone up, and say what a machine is missing.
#
#     tools/toolbox.sh            check everything, install what tend can
#     tools/toolbox.sh --check    check only; change nothing
#
# One command for the stranger test (`vision.md` §"Ease of use"):
# somebody who has never read this repository runs this once and either
# has a working clone or a short list of what their machine lacks, each
# line saying why it is needed.  Idempotent — running it twice is safe
# and the second run mostly says "already there".
#
# **It never installs system packages.**  Two reasons: on this machine
# the fence (`.claude/settings.json`) denies a session the package
# managers, and that denial is the feature — a setup script a session
# runs must not be a road around it; and on a stranger's machine the
# package manager is theirs, so this says the package's name and leaves
# the installing to whoever owns the prompt.
#
# What tend can install itself, it does: the pre-commit hook (the gate
# `card:gates.md` exists for), and the execute bits an archive download
# loses.
set -eu

root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
check_only=false
[ "${1:-}" = "--check" ] && check_only=true
case "${1:-}" in ""|--check) ;; -h|--help)
    sed -n '2,24p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
*)  echo "toolbox: unknown argument \`$1\`" >&2; exit 2 ;;
esac

missing=0

need() { # need COMMAND WHY [PACKAGE-HINT]
    if command -v "$1" >/dev/null 2>&1; then
        echo "  ✓ $1"
    else
        echo "  ✗ $1 — $2 (install: ${3:-$1})"
        missing=1
    fi
}

want() { # want COMMAND WHY — degraded without, not broken
    if command -v "$1" >/dev/null 2>&1; then
        echo "  ✓ $1"
    else
        echo "  · $1 — absent; $2"
    fi
}

echo "toolbox: $root"
echo
echo "  required"
need git      "the tree is a repository and the gates hang off its hooks"
need python3  "the suite and every tool under tools/ run on it"
need sh       "the hooks and this script"
need jq       "tools/limit.sh reads the hook's stdin with it, and tools/fence.sh reads the deny-list"
need timeout  "a hang is a crash only if something enforces it (tools/leash.sh)" "coreutils"
need bwrap    "tools/sandbox.sh is the fence; with tools/fence-hook.sh installed every shell command runs inside it" "bubblewrap"
need flock    "tools/launch.sh gives each node one runner with it — the lock a second run is refused on (exit 75)" "util-linux"
need setsid   "tools/launch.sh and tools/resolve.sh start a node's runner detached with it, so it outlives the pull" "util-linux"
if python3 -m pytest --version >/dev/null 2>&1; then
    echo "  ✓ pytest"
else
    echo "  ✗ pytest — the suite is pytest; without it nothing runs the contract (install: python3-pytest)"
    missing=1
fi

echo
echo "  optional"
if systemd-run --user --scope -q true >/dev/null 2>&1; then
    echo "  ✓ systemd user manager — tools/leash.sh gets real CPU/memory budgets"
else
    echo "  · systemd user manager — absent; tools/leash.sh degrades to nice + timeout"
fi
want bash "tools/limit.sh needs it only when installed as a hook"
# the andon (tools/andon.sh) rings through a sound player; without one it
# records the question and cannot sound.  The player is a package; the
# *socket* it needs (PipeWire's $XDG_RUNTIME_DIR/pipewire-0) is runtime,
# not a package, and this cannot check it — on 2026-08-28 the work laptop
# had the player, and the socket, and the ring still failed: a fenced
# session cannot see a socket its fence never bound (card:silent-cord.md
# §10:18, correcting that morning's "no socket", which was the fence's
# view stated as the machine's).  So a green here is "a player exists",
# never "the andon will sound" — and an absence here is never "the machine
# has none", only "not from this seat".
andon_player=""
for c in pw-play paplay aplay; do command -v "$c" >/dev/null 2>&1 && { andon_player=$c; break; }; done
if [ -n "$andon_player" ]; then
    echo "  ✓ $andon_player — the andon rings through it (tools/andon.sh); the socket it needs is runtime, not a package"
else
    echo "  · pw-play — absent; the andon (tools/andon.sh) can record but not sound (install: pipewire-bin)"
fi

echo
echo "  the nodes"
want llama-server "the llm node (llm/grant) is a llama.cpp server; without it that one node cannot run, the others can"
if [ -n "$(find "$root"/llm/model -maxdepth 1 -name '*.gguf' 2>/dev/null | head -1)" ]; then
    echo "  ✓ a model under llm/model/ — the llm node has something to serve"
else
    echo "  · no *.gguf under llm/model/ — the llm node's model is data you bring; it is gitignored, never in the tree (card:work-environment-ai.md)"
fi

echo
echo "  the fence"
if sh "$root/tools/fence.sh" >/dev/null 2>&1; then
    echo "  ✓ .claude/settings.json — the deny-list and the hooks are in force"
else
    echo "  ✗ the fence is down — tools/fence.sh says which line; the settings"
    echo "    file is not this script's to edit (hook config is enforcement, and"
    echo "    the edit is the person's — test/test_fence.py has the jq)"
    missing=1
fi

echo
if $check_only; then
    echo "  --check: nothing was changed."
else
    echo "  installing what tend can"
    chmod +x "$root"/tools/*.sh 2>/dev/null || true
    echo "  ✓ execute bits on tools/*.sh"
    sh "$root/tools/pre-commit.sh" --install | sed 's/^/  /'
fi

echo
if [ "$missing" -eq 1 ]; then
    echo "toolbox: something required is missing — the lines marked ✗ say what and why."
    exit 1
fi
echo "toolbox: everything required is here."
