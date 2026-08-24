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
need jq       "tools/limit.sh reads the hook's stdin with it"
need timeout  "a hang is a crash only if something enforces it (tools/leash.sh)" "coreutils"
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
