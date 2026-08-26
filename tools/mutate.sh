#!/bin/bash
#: asked-by: Henri, 2026-08-26 — "put the harness in tools/, then measure test_kaizen and test_limit" (card:green.md)
#
# tools/mutate.sh — break the thing a detector guards, in a copy, and read the detector.
#
#     tools/mutate.sh TEST 'shell'      one break: run the shell in a fresh copy of this
#                                       tree, run TEST there, say red / GREEN / NOOP
#     tools/mutate.sh --gate 'shell'    one break of the gates hook: in the copy, with the
#                                       hook installed, commit a because-less card;
#                                       say refused / COMMITTED, and the suite's verdict — the
#                                       gate can never refuse a cut in its own wiring, so the
#                                       detector there is the suite it runs
#     tools/mutate.sh                   the recorded breaks, at the foot of this file;
#                                       exit 1 if any survived
#
# **A gate that has only ever passed is a claim** (`card:green.md`).
# gestate's F88 named a defect, stayed green from the day it was
# written, and passed with the defect put back; on 2026-08-26 the same
# question was put to tend's own detectors — thirty-eight breaks, seven
# survived, every one in the wiring between a detector and the thing
# that runs it — and the harness that asked it lived in a session's
# scratch.  Henri: "put the harness in tools/".  This is that harness,
# in `~/gestate/tools/seedmutate.sh`'s shape: a fresh copy per break,
# one hand's `sed`, one detector's verdict.
#
# **What it is not**: a framework, a quota, or a percentage.  The card
# says why — a quota is answered by inventing tests that pass.  One
# break, one verdict, read by a person; the recorded list is so a
# verdict can be re-read when the tree moves, not so a number can go up.
#
# **The harness is checked before any row is read.**  The morning's
# scratch version lied twice before it was trusted (`$?` read after a
# `local`; a `sed` that deleted the line it had added), both caught by
# a number that could not be right.  So, first: the intact copy is
# green on the detector, and a break every run knows is detected —
# `exit $fail` → `exit 0` in `tools/fence.sh` — is red.  If either is
# not, nothing below can be read, and it says so.  And a break that
# leaves the copy identical to the tree is `NOOP`, never a verdict.
#
# **The copy is the working tree** — tracked and untracked files that
# git does not ignore — with its own `.git` and the pre-commit hook
# installed, so `--gate` commits for real.  Nothing here touches this
# tree, and nothing here touches the desk: `test_limit.py` and
# `test_kaizen.py` point their ledgers at temporary directories
# themselves.
#
# Exit: 0 the break was detected (or every recorded one was);
#       1 a break survived; 2 usage; 3 the harness could not be trusted.
set -u
SRC=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
T=$(mktemp -d "${TMPDIR:-/tmp}/mutate.XXXXXX"); trap 'rm -rf "$T"' EXIT
G="git -c user.name=mutate -c user.email=mutate@tend"

fresh() {
    rm -rf "$T/t"; mkdir -p "$T/t"
    (cd "$SRC" && git ls-files -co --exclude-standard -z | xargs -0 cp --parents -t "$T/t")
    (cd "$T/t" && git init -q && $G add -A && $G commit -qm intact && sh tools/pre-commit.sh --install) >/dev/null
}
# a breaking shell, run in the copy; NOOP if the copy is left as it was
apply() { (cd "$T/t" && eval "$1") >/dev/null 2>&1 || return 2; (cd "$T/t" && { [ -n "$(git status --porcelain)" ] || [ ! -x .git/hooks/pre-commit ]; }); }
run_tests() { (cd "$T/t" && python3 -m pytest -q -p no:cacheprovider -rf "$@" 2>&1); }
tally() { printf '%s\n' "$1" | grep -E '^[0-9]+ (passed|failed)' | tail -1 | sed -E 's/ in [0-9.]+s//'; }
names() { printf '%s\n' "$1" | grep -E '^FAILED' | sed -E 's/^FAILED [^:]*::([^ ]*).*/\1/' | tr '\n' ' '; }
say() { printf '  %-10s %-44s %-22s %s\n' "$@"; }

survived=0
# one TEST 'shell' [label]
one() {
    local test=$1 cmd=$2 label=${3:-$2} out v=GREEN
    fresh; apply "$cmd"; case $? in 2) say ERR "$label" "the break itself failed"; return 3 ;; 1) say NOOP "$label" "the copy is unchanged"; return 3 ;; esac
    out=$(run_tests "$test") || v=red
    say "$v" "$label" "$(tally "$out")" "$(names "$out")"
    [ $v = red ] || { survived=$((survived+1)); return 1; }
}
# gate 'shell' [label] — a because-less card, listed, committed for real
gate() {
    local cmd=$1 label=${2:-$1} out tv=GREEN before after v=refused
    fresh; apply "$cmd"; case $? in 2) say ERR "$label" "the break itself failed"; return 3 ;; 1) say NOOP "$label" "the copy is unchanged"; return 3 ;; esac
    out=$(run_tests test/) || tv=red
    before=$(cd "$T/t" && git rev-parse HEAD)
    (cd "$T/t" && printf '    status   open\n    asked    mutate, today\n\nno because.\n' > board/dud.md \
        && echo '- [dud](dud.md)' >> board/README.md && $G add -A && $G commit -qm dud) >/dev/null 2>&1
    after=$(cd "$T/t" && git rev-parse HEAD)
    [ "$before" != "$after" ] && v=COMMITTED
    say "$v" "$label" "suite: $tv" "$(names "$out")"
    [ $v = refused ] || [ $tv = red ] || { survived=$((survived+1)); return 1; }
}
# the harness, before any row is read
trust() {
    local test=$1 out
    fresh; out=$(run_tests "$test") || { echo "mutate: the intact copy is red on $test; nothing below can be read"; printf '%s\n' "$out" | tail -3; exit 3; }
    say GREEN "intact copy" "$(tally "$out")"
    fresh; apply 'sed -i "s/^exit \$fail$/exit 0/" tools/fence.sh' || { echo "mutate: the known break did not apply"; exit 3; }
    out=$(run_tests test/test_fence.py) && { echo "mutate: the break every run knows — fence.sh exit 0 — came back GREEN; the harness cannot be trusted"; exit 3; }
    say red "known break: fence.sh exit 0" "$(tally "$out")"
}

case "${1:-}" in
    -h|--help) sed -n '2,50p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    --gate) [ $# -ge 2 ] || { echo "mutate: --gate 'shell'" >&2; exit 2; }
            trust test/test_precommit.py; gate "$2"; exit $? ;;
    "")  ;;
    -*)  echo "mutate: unknown argument \`$1\`" >&2; exit 2 ;;
    *)   [ $# -ge 2 ] || { echo "mutate: TEST 'shell'" >&2; exit 2; }
         trust "$1"; one "$1" "$2"; exit $? ;;
esac

# The recorded breaks: TEST (or `gate`), a label, the shell — tab-separated.
# A row is a verdict that was read once; rerun, it says whether the tree
# still holds it.  A row added is a break one hand tried, with its date.
rows() { cat <<'ROWS' | grep -v '^#'
# test_fence.py against tools/fence.sh — 2026-08-26
test/test_fence.py	fence: exit code always 0	sed -i "s/^exit \$fail$/exit 0/" tools/fence.sh
test/test_fence.py	fence: MISSING printed, no fail=1	sed -i "s/MISSING from the deny-list\"; fail=1; missing=1/MISSING from the deny-list\"; missing=1/" tools/fence.sh
test/test_fence.py	fence: rule name gone from MISSING line	sed -i "s/say \"✗\" \"\$1 — MISSING/say \"✗\" \"— MISSING/" tools/fence.sh
test/test_fence.py	fence: drop rule Edit(./.claude/**)	sed -i "s|^rules=\"Edit(./.claude/\*\*)\$nl\"|rules=\"\"|" tools/fence.sh
test/test_fence.py	fence: drop rule Bash(sudo:*)	sed -i "s|Bash(sudo:\*)\${nl}||" tools/fence.sh
test/test_fence.py	fence: drop rule Bash(git push:*)	sed -i "s|Bash(git push:\*)\${nl}||" tools/fence.sh
test/test_fence.py	fence: drop rule Read(~/.ssh/**)	sed -i "s|\${nl}Read(~/.ssh/\*\*)\"|\"|" tools/fence.sh
test/test_fence.py	fence: drop the protected-set rules	sed -i "s|^for p in \$protected; do rules=.*||" tools/fence.sh
test/test_fence.py	fence: hook check, kaizen dropped	sed -i "s/for h in kaizen limit fence; do/for h in limit fence; do/" tools/fence.sh
test/test_fence.py	fence: hook check, limit dropped	sed -i "s/for h in kaizen limit fence; do/for h in kaizen fence; do/" tools/fence.sh
test/test_fence.py	fence: hook check, fence dropped	sed -i "s/for h in kaizen limit fence; do/for h in kaizen limit; do/" tools/fence.sh
test/test_fence.py	fence: PreToolUse missing, no fail=1	sed -i "s/every shell command runs unfenced\"; fail=1/every shell command runs unfenced\"/" tools/fence.sh
test/test_fence.py	fence: valid() always true	sed -i "s/^valid() { .*/valid() { return 0; }/" tools/fence.sh
test/test_fence.py	fence: --hook silent when down	sed -i "s/    if \[ \$fail -ne 0 \]; then/    if false; then/" tools/fence.sh
test/test_fence.py	fence: home spelling not normalised	sed -i "/map(sub(/d" tools/fence.sh
test/test_fence.py	fence: --protect hint gone	sed -i "s|^        say \"→\" \"tools/fence.sh --protect adds.*|        :|" tools/fence.sh
test/test_fence.py	fence: --restore reverts a parsing file	sed -i "s/    force) restore || exit \$? ;;/    force|restore) restore || exit \$? ;;/" tools/fence.sh
# test_board.py against the board — 2026-08-26
test/test_board.py	board: card with no because, listed	printf '    status   open\n    asked    x, 2026-08-26\n\nbody\n' > board/dud.md; echo '- [dud](dud.md)' >> board/README.md
test/test_board.py	board: because line with empty value	sed -i "s/^    because  .*/    because  /" board/green.md
test/test_board.py	board: valid card, not listed in README	printf '    status   open\n    because  a problem\n    asked    x, 2026-08-26\n\nbody\n' > board/dud.md
test/test_board.py	board: README lists a card not there	echo '- [ghost](ghost.md)' >> board/README.md
test/test_board.py	board: two cards wear one name	sed "s/^    status   done.*/    status   open/" board/done/grant.md > board/grant.md; echo '- [grant](grant.md)' >> board/README.md
test/test_board.py	board: status done, sitting in board/	sed -i "s/^    status   .*/    status   done — 2026-08-26/" board/cords.md
test/test_board.py	board: status open, sitting in later/	sed -i "s/^    status   .*/    status   open/" board/later/rules-and-memory.md
test/test_board.py	board: blocked, says not on what	sed -i "s/^    status   .*/    status   blocked/; /^    blocked  /d" board/cords.md
test/test_board.py	board: blocked on a card not there	sed -i "/^    blocked  /d; s/^    status   .*/    status   blocked\n    blocked  board\/nothing.md/" board/cords.md
test/test_board.py	board: status word misspelt	sed -i "s/^    status   open/    status   opne/" board/green.md
test/test_board.py	board: header indented 3, not 4	sed -i "s/^    \(status\|because\|asked\|see\)  /   \1  /" board/green.md
test/test_board.py	board: done with no date, in done/	sed -i "s/^    status   done.*/    status   done/" board/done/grant.md
test/test_kaizen.py	kaizen: lamp matches the dir, not the name	sed -i 's|kzn="doc/kaizen/[^"]*"|kzn="doc/kaizen/"|' tools/kaizen.sh
# the gates hook against a commit — 2026-08-26
gate	gate: pre-commit.sh ignores the suite's verdict	sed -i "s/^if python3 tools\/suite.py; then/if python3 tools\/suite.py || true; then/" tools/pre-commit.sh
gate	gate: suite.py always returns 0	sed -i "s/^    return r.returncode/    return 0/" tools/suite.py
gate	gate: the drift block removed	sed -i "/^drift=\"\"/,/^fi$/d" tools/pre-commit.sh
gate	gate: hook uninstalled	sh tools/pre-commit.sh --uninstall
test/test_keep.py	keep: node launcher drops the code grant	sed -i '/--allow "$here\/node.py"/d' node/run.sh
test/test_suite.py	suite: always returns 0	sed -i "s/^    return r.returncode/    return 0/" tools/suite.py
# test_kaizen.py against tools/kaizen.sh, test_limit.py against tools/limit.sh — 2026-08-26
test/test_kaizen.py	kaizen: never lights	sed -i 's/^if \[ "\$n" -eq 0 \] && \[ -z "\$wanted" \]; then/if true; then/' tools/kaizen.sh
test/test_kaizen.py	kaizen: last kaizen never found	sed -i 's/^last=\$(git .*/last=""/' tools/kaizen.sh
test/test_kaizen.py	kaizen: counts every commit ever	sed -i 's/^    range="\$last..HEAD"/    range="HEAD"/' tools/kaizen.sh
test/test_kaizen.py	kaizen: a want is never forgotten	sed -i 's/^        rm -f "\$WANT"/        :/' tools/kaizen.sh
test/test_kaizen.py	kaizen: want-time comparison inverted	sed -i 's/-lt "\$last_at"/-gt "$last_at"/' tools/kaizen.sh
test/test_kaizen.py	kaizen: want stamped at epoch 0	sed -i 's/"\$(date +%s)" "\$2" >/0 "$2" >/' tools/kaizen.sh
test/test_kaizen.py	kaizen: want needs no reason	sed -i '/^    if \[ -z "\${2:-}" \]; then/,/^    fi/d' tools/kaizen.sh
test/test_kaizen.py	kaizen: --hook exits before the lamp	sed -i 's/^--hook) cat >\/dev\/null ;;/--hook) cat >\/dev\/null; exit 0 ;;/' tools/kaizen.sh
test/test_kaizen.py	kaizen: exit 1 when lit	sed -i '$ s/^exit 0$/exit 1/' tools/kaizen.sh
test/test_kaizen.py	kaizen: file name gone from the line	sed -i 's/doc\/kaizen\/\$began.md/doc\/kaizen\//g' tools/kaizen.sh
test/test_kaizen.py	kaizen: began = last commit, not first	sed -i 's/git -C "\$root" log --reverse --format=%cd/git -C "$root" log --format=%cd/' tools/kaizen.sh
test/test_kaizen.py	kaizen: unknown argument accepted	sed -i 's/^\*) echo "kaizen: unknown argument .*/*) ;;/' tools/kaizen.sh
test/test_limit.py	limit: reset allowed inside a session	sed -i '/^    if \[ -n "\${CLAUDECODE:-}" \]; then/,/^    fi/d' tools/limit.sh
test/test_limit.py	limit: grant regex unanchored	sed -i 's/=~ \^\[\[:space:\]\]\*sitting(\[\[:space:\]\]+(\[0-9\]+))?\[\[:space:\]\]\*\$ /=~ sitting([[:space:]]+([0-9]+))? /' tools/limit.sh
test/test_limit.py	limit: bare word grants 45 not 15	sed -i 's/\${BASH_REMATCH\[2\]:-\$LIMIT_MIN}/${BASH_REMATCH[2]:-45}/' tools/limit.sh
test/test_limit.py	limit: grant reaches the session (exit 0)	sed -i '/note grant/,/exit 2/ s/    exit 2/    exit 0/' tools/limit.sh
test/test_limit.py	limit: the block never fires	sed -i 's/^  if \[ "\$elapsed" -ge "\$limit" \]; then/  if false; then/' tools/limit.sh
test/test_limit.py	limit: elapsed from last, not started	sed -i 's/^elapsed=\$(( (now - started) \/ 60 ))/elapsed=$(( (now - last) \/ 60 ))/' tools/limit.sh
test/test_limit.py	limit: the way back in gone from the message	sed -i '/To sit down again on purpose/d' tools/limit.sh
test/test_limit.py	limit: closed branch never fires	sed -i 's/^    if \[ "\$limit" -eq 0 \]; then/    if false; then/' tools/limit.sh
test/test_limit.py	limit: state write drops the reason	sed -i 's/"\$limit" "\$closed" > "\$STATE"/"$limit" > "$STATE"/' tools/limit.sh
test/test_limit.py	limit: stop keeps the limit instead of 0	sed -i 's/"\$now" 0 "\${2:-/"$now" "$limit" "${2:-/' tools/limit.sh
test/test_limit.py	limit: empty stdin records a prompt	sed -i '/^  if ! printf .%s. "\$input" | jq -e/,/^  fi/d' tools/limit.sh
test/test_limit.py	limit: the wake block removed	sed -i '/^  if \[ "\${prompt#\*<task-notification>}" != "\$prompt" \]; then/,/^  fi/d' tools/limit.sh
test/test_limit.py	limit: a wake writes the state	sed -i 's/^    note wake "gap=\$gap"/    printf "%s %s %s %s\\n" "$now" "$now" "$limit" "$closed" > "$STATE"; note wake "gap=$gap"/' tools/limit.sh
test/test_limit.py	limit: a wake is logged as a prompt	sed -i 's/^    note wake "gap=\$gap"/    note prompt "gap=$gap"/' tools/limit.sh
test/test_limit.py	limit: the log records the prompt text	sed -i 's/^  note prompt "gap=\$gap elapsed=\$elapsed limit=\$limit"/  note prompt "$prompt"/' tools/limit.sh
test/test_limit.py	limit: a fresh sitting keeps the old length	sed -i '/^  fresh=1$/,/^fi$/ s/^  limit="\$LIMIT_MIN"$/  :/' tools/limit.sh
test/test_limit.py	limit: reading the clock moves it	sed -i 's/^if \[ "\$limit" -eq 0 \]; then$/printf "%s %s %s %s\\n" "$now" "$now" "$limit" "$closed" > "$STATE"\nif [ "$limit" -eq 0 ]; then/' tools/limit.sh
test/test_limit.py	limit: GAP default 30 -> 60	sed -i 's/^GAP_MIN="\${GESTATE_LIMIT_GAP:-30}"/GAP_MIN="${GESTATE_LIMIT_GAP:-60}"/' tools/limit.sh
# test_limit.py against tools/limit.sh — card:arrival.md, 2026-08-26
test/test_limit.py	limit: the message block removed	sed -i '/^  if \[ "\${prompt#\*<cross-session-message}" != "\$prompt" \]; then/,/^  fi/d' tools/limit.sh
test/test_limit.py	limit: a message writes the state	sed -i 's/^    note peer "gap=\$gap"/    printf "%s %s %s %s\\n" "$now" "$now" "$limit" "$closed" > "$STATE"; note peer "gap=$gap"/' tools/limit.sh
test/test_limit.py	limit: a message is logged as a prompt	sed -i 's/^    note peer "gap=\$gap"/    note prompt "gap=$gap"/' tools/limit.sh
# the eight files board/green.md left unmeasured, swept 2026-08-26 — one break each
test/test_selfmatch.py	selfmatch: an unbracketed pattern kill in a tool	printf "\npkill -f \"while :; do :; done\"\n" >> tools/summary.sh
test/test_summary.py	summary: a cited tool removed	rm tools/leash.sh
test/test_rules.py	rules: the boot surface grows a line	printf "second line\n" >> CLAUDE.md
test/test_toolbox.py	toolbox: --check claims a change	sed -i "s/nothing was changed/changed lots/" tools/toolbox.sh
test/test_node.py	node: the pull ledger renamed	sed -i "s/\.pull/\.pxll/g" node/node.py
test/test_leash.py	leash: the hang message changed	sed -i "s/budget is spent/all gone/" tools/leash.sh
test/test_fence_hook.py	fence-hook: the leash prefix dropped	sed -i "s#tools/leash.sh -- ##g" tools/fence-hook.sh
# test_keep.py against tools/keep.py and node/run.sh — card:keep.md, the write and network slices, 2026-08-26
test/test_keep.py	keep: write bits never handled (--write collapses to read-only)	sed -i 's/^        write_bits = WRITE_HANDLED .*/        write_bits = 0/' tools/keep.py
test/test_keep.py	keep: net bits zeroed (--no-net handles nothing)	sed -i 's/^NET_HANDLED = NET_BIND_TCP | NET_CONNECT_TCP/NET_HANDLED = 0/' tools/keep.py
test/test_keep.py	keep: --no-net parsed but never handed to confine()	sed -i 's/confine(allow, write, no_net)/confine(allow, write)/' tools/keep.py
test/test_keep.py	keep: --no-net on an old ABI runs the program anyway	sed -i 's/^        if abiv < 4:/        if False:/; s/^        attr = ruleset_attr_v4(handled, NET_HANDLED)/        attr = ruleset_attr(handled)/' tools/keep.py
test/test_keep.py	keep: node launcher drops --no-net	sed -i '/^    --no-net \\$/d' node/run.sh
# node/run.sh against test_keep.py — card:resolver.md day one, the pull is the launch, 2026-08-26
test/test_keep.py	resolver: pull never starts a runner	sed -i '/^        setsid -f sh "\$0" run/d' node/run.sh
test/test_keep.py	resolver: pull starts a runner even when one holds the lock	sed -i 's/^    if flock -n "\$lock" true 2>\/dev\/null; then/    if true; then/' node/run.sh
test/test_keep.py	resolver: run never takes the lock	sed -i 's/^    flock -n 9 || {.*/    :/' node/run.sh
test/test_keep.py	resolver: pull does not wait for the runner to open	sed -i 's/^        while \[ "\$(generation)" -le "\$before" \] && \[ "\$n" -lt 60 \]; do/        while false; do/' node/run.sh
# node/run.sh — the grant appears once — card:green.md, 2026-08-26
test/test_keep.py	green: a second keep invocation pasted into the launcher	printf '%s\n' 'exec "$py" "$root/tools/keep.py" --allow "$here/node.py" -- true' >> node/run.sh
# tools/ledger.py and node/node.py — the session half of keep and resolver, 2026-08-26
test/test_ledger.py	ledger: a continuation line is dropped, not joined	sed -i 's/^                out\[-1\]\[5\] += "\\n" + line/                pass/' tools/ledger.py
test/test_ledger.py	ledger: read by line — every line is a record	sed -i 's/^            if HEAD.match(line):/            if True:/; s/^                if len(p) == 6:/                if len(p) >= 1:/' tools/ledger.py
test/test_ledger.py	ledger: since never cuts	sed -i 's/^        recs = \[r for r in recs if r\[0\] >= t\]; i += 2/        i += 2/' tools/ledger.py
test/test_node.py	node: the runner lock never taken	sed -i 's/^        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)/        pass/' node/node.py
# tools/resolve.sh and node/node.py — the resolver outside the fence, card:resolver.md, 2026-08-26
test/test_resolve.py	resolve: starts even when every pull is served	sed -i 's/^\[ "\$pulled" -gt "\${served:-0}" \] || exit 0/[ "$pulled" -ge "${served:-0}" ] || exit 0/' tools/resolve.sh
test/test_resolve.py	resolve: the lock is never looked at	sed -i 's/^flock -n "\$lock" true 2>\/dev\/null || exit 0.*/:/' tools/resolve.sh
test/test_resolve.py	resolve: does not wait for the runner's lock	sed -i 's/^n=0; while flock -n "\$lock" true.*/:/' tools/resolve.sh
test/test_resolve.py	node: a runner reads the ledger at open and serves only what follows	sed -i 's/^    seen = st\["pulls"\]/    seen = pulls_in(ledger(a.state))/' node/node.py
# node/run.sh — the runner waits for the lock rather than refusing at once, card:resolver.md 15:12 (NOOP until resolver-lock.patch is in)
test/test_keep.py	resolver: the runner refuses the lock at once instead of waiting	sed -i 's/^    flock -w 2 9 || {/    flock -n 9 || {/' node/run.sh
ROWS
}

trust test/test_fence.py
echo
while IFS=$'\t' read -r test label cmd; do
    [ -n "$test" ] || continue
    if [ "$test" = gate ]; then gate "$cmd" "$label"; else one "$test" "$cmd" "$label"; fi
done <<< "$(rows)"
echo; echo "mutate: $survived survived"
[ "$survived" -eq 0 ]
