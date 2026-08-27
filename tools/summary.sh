#!/bin/sh
#: asked-by: Henri, 2026-08-25 — "Save them into doc/summary/ ... make something that ensures they're kept updated"
#
# tools/summary.sh — the lamp for the summary in doc/summary/.
#
#     tools/summary.sh           list mechanisms changed since the summary was; a lamp, never a refusal
#     tools/summary.sh --hook    the UserPromptSubmit form: silent when fresh, exit 0
#
# **A summary that cannot say when it is stale is a wish** — the same
# stance as the rest of the tree (`doc/summary/rules.md` R4).  Two
# instruments keep it honest, and they are deliberately split:
#
# * The **hard half** is `test/test_summary.py`, at the gate: every tree
#   path the summary cites must exist, its one live claim — that the
#   andon is built — must agree with `card:cords.md`'s shelf, and the
#   printable twin must say what the sheets say (`tools/sheets.py`,
#   2026-08-27).  Rename a tool, move a card, or let the HTML lag, and
#   the commit is refused until the summary is reconciled.  That is
#   correctness, so it blocks.
#
# * The **soft half** is this lamp: it does not know whether the *prose*
#   is still true, only that a mechanism the summary describes has a
#   commit newer than the summary's own — so the words *may* have gone
#   stale and want re-reading.  Prose is not a thing a test can grade
#   (the kaizen lamp has the same honest limit), so this informs and
#   never blocks.  It clears when `doc/summary/` gets a commit newer
#   than every source below — i.e. when a person or session re-reads the
#   summary against the change and commits it, even unchanged.
#
# Measured in commits, not mtimes, so a checkout does not light it.
set -eu

root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$root"
mode=lamp
case "${1:-}" in
    "") ;;
    --hook) mode=hook ;;
    -h|--help) sed -n '4,8p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "summary: unknown argument \`$1\`" >&2; exit 2 ;;
esac

# The sources the summary describes: the mechanisms it names, the first
# program, and the documents its rules are drawn from.  A source added
# to the tree that belongs on the sheets is added here too — itself a
# small act of keeping the summary honest.
sources="tools/fence.sh tools/sandbox.sh tools/fence-hook.sh tools/leash.sh
  tools/limit.sh tools/kaizen.sh tools/pre-commit.sh tools/toolbox.sh
  tools/suite.py node/node.py board/ vision.md manifesto.md spec/os.md"

# Newest commit that touched the summary itself.  git log prints nothing
# (and exits 0) for a path with no commits, so empty is coerced to 0 —
# an untracked summary is "older than everything", which lights the lamp
# until the first commit, correctly.
sum_at=$(git log -1 --format=%ct -- doc/summary/ 2>/dev/null || true)
sum_at=${sum_at:-0}

stale=""
for s in $sources; do
    at=$(git log -1 --format=%ct -- "$s" 2>/dev/null || true)
    at=${at:-0}
    [ "$at" -gt "$sum_at" ] && stale="$stale $s"
done

if [ -z "$stale" ]; then
    [ $mode = hook ] || echo "summary: fresh — no mechanism has changed since doc/summary/ was last confirmed."
    exit 0
fi

# stdout on UserPromptSubmit reaches the session; a lamp, so exit 0.
{
    echo "🟡 summary: these have changed since doc/summary/ was last confirmed —"
    for s in $stale; do echo "     $s"; done
    echo "   re-read doc/summary/rules.md and interfaces.md against them; if still true,"
    echo "   a commit touching doc/summary/ clears this (an unchanged re-confirm is fine)."
}
exit 0
