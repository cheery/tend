#!/bin/sh
#: asked-by: Henri, 2026-08-24 — "add the needed cards so that the absent work is completed"
#
# tools/pre-commit.sh — the gates, at the commit that breaks them.
#
#     tools/pre-commit.sh --install     put it in .git/hooks/pre-commit
#     tools/pre-commit.sh --uninstall   take it out again
#     tools/pre-commit.sh --check       say whether it is installed
#     tools/pre-commit.sh               run the gates now (what the hook does)
#
# Borrowed whole from gestate's `tools/pre-commit.sh` on 2026-08-24,
# named as borrowed (`card:gates.md`).  The shape was paid for there:
# checks that ran once per shift, at the end, died on a breakage hours
# old and landed as a chore on the author — a rule in a README would
# have been read by the same session that had already skipped it.  So
# the gate stands where the commit happens, outside the model that must
# pass it.
#
# It fires on Henri's commits too, and the answer is not to make it
# clever about who is committing — it cannot know — but to make it
# cheap, loud about what failed, and trivial to remove.  Hence
# --uninstall, named in the failure message.
#
# It checks the working tree, not the index — the same deliberate gap as
# gestate's: what it guards is whether the tree the next reader opens
# agrees with itself, not the diff.
set -eu

root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)

# The shim, rather than a symlink: it survives the repository being
# moved, and works from a worktree.  The marker on the second line is
# how --check and --uninstall recognise their own work and refuse to
# touch anybody else's hook.
MARKER='tend:tools/pre-commit.sh'

hookdir=$(git -C "$root" rev-parse --git-path hooks 2>/dev/null || echo '')
case "$hookdir" in /*) ;; *) hookdir="$root/$hookdir" ;; esac
hook="$hookdir/pre-commit"

case "${1:-}" in
--install)
    if [ -e "$hook" ] && ! grep -q "$MARKER" "$hook" 2>/dev/null; then
        echo "pre-commit: $hook exists and is not ours — not overwriting it." >&2
        echo "            look at it, then move it aside if you want this one." >&2
        exit 3
    fi
    mkdir -p "$hookdir"
    cat > "$hook" <<'SHIM'
#!/bin/sh
# tend:tools/pre-commit.sh — installed by `tools/pre-commit.sh --install`.
# Not tracked (hooks never are); remove with `tools/pre-commit.sh --uninstall`.
exec "$(git rev-parse --show-toplevel)/tools/pre-commit.sh"
SHIM
    chmod +x "$hook"
    echo "pre-commit: installed at $hook"
    echo "            every commit now runs the gates first (a few seconds)."
    exit 0
    ;;
--uninstall)
    if [ ! -e "$hook" ]; then
        echo "pre-commit: nothing installed at $hook"
    elif grep -q "$MARKER" "$hook" 2>/dev/null; then
        rm -f "$hook"; echo "pre-commit: removed $hook"
    else
        echo "pre-commit: $hook is not ours — left alone." >&2; exit 3
    fi
    exit 0
    ;;
--check)
    if [ -x "$hook" ] && grep -q "$MARKER" "$hook" 2>/dev/null; then
        echo "✓ pre-commit hook installed — the gates run at every commit"
        exit 0
    fi
    echo "✗ no pre-commit hook — run tools/pre-commit.sh --install"
    exit 1
    ;;
-h|--help)
    sed -n '2,28p' "$0" | sed 's/^# \{0,1\}//'
    exit 0
    ;;
"") ;;
*)  echo "pre-commit: unknown argument \`$1\`" >&2; exit 2 ;;
esac

cd "$root"
if python3 tools/suite.py; then
    exit 0
fi

cat >&2 <<'MSG'

pre-commit: a gate failed, so this commit was refused.

  Named above.  The gates take seconds and are about documents rather
  than behaviour — the board's contract, the boot surface.  A red one
  nearly always means an edit in this commit left the tree disagreeing
  with itself, and fixing it belongs in this commit rather than in
  somebody's morning.

  To commit anyway:      git commit --no-verify
  To stop this entirely: tools/pre-commit.sh --uninstall

  If you use --no-verify, say in the commit body which gate you skipped.
  A skipped gate nobody wrote down is the state this hook was built to
  end.

MSG
exit 1
