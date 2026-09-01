# rewritten-command — a session cannot trust that what it wrote is what ran

    status   open
    because  the harness rewrites a session's own Bash command text before
             it runs, substituting braced shell expansions even inside a
             quoted heredoc, where the shell itself would not touch them.
             A session writes one thing and another thing executes, and
             the result is a hole rather than an error: exit 0, and the
             file on disk is missing a value nobody asked it to drop.  It
             has reached committed files — `tools/consult.sh` shipped a
             message reading "trimmed to  chars", with no number, from
             2026-08-28 (`01f422e`, then again `c6e9fc5`) until it was
             found on 2026-09-01 — and it fired five times in one sitting
             that day, twice inside the prose being written to record it
    asked    Henri, 2026-09-01 — "that command eating is nasty", then
             "Do the card and refuse the route"
    see      card:lost-write.md — the precedent and the shape: a rule in
             front of the hand failed four times, and what held was the
             kernel in front of the write
             doc/kaizen/2026-09-01-0615.md item 5 — where the fourth face
             fired 2026-08-26-1712's own trigger, "a fourth is a mechanism
             owed"
             fixme/F010.md — the committed instance, and the entry whose
             paragraph explaining the bug was itself eaten
             tools/fence-hook.sh, tools/sandbox.sh — where a refusal lives

## Two cases, and only one of them is silent

They are not the same defect and a mechanism has to know which it is
meeting.

**Announced.**  When the brace encloses something that is not a valid
environment variable name — a length sigil, a name with a suffix
operator, a name with punctuation — the harness prints `Invalid
environment variable name evaluates to an empty string: <name>` and
substitutes nothing.  The corruption happens *and* it is announced.  All
five faces of 2026-09-01 were this kind.

**Silent.**  When the brace encloses a *valid* name that is simply not
set in the harness's environment, the substitution is an ordinary empty
string and nothing is printed.  This is the `consult.sh` case: the script
said `trimmed to $ctxchars chars` with the braces on, `ctxchars` meant the
*script's own* variable, the harness read it as its own and found nothing,
and the committed file said "trimmed to  chars" for four days.

## The uncomfortable half, named as the session's

The announced case is the majority of the faces and **the announcement
did not stop anything**.  On 2026-09-01 the warning was printed, read,
and worked past three times in one sitting; twice the very next action
was to write more prose about the bug.  So this card must not be built on
the belief that a louder warning would help — one already exists and it
is not what failed.  What failed is that a warning is advice and the
session kept its hand on the same route.

That is exactly `card:lost-write.md`'s finding one level up: there, the
natural repair for the error (`mkdir -p`) made the *next* write succeed at
exit 0 and vanish, and what closed it was a kernel that refuses.  The
lesson carried here is that the fix must remove the route, not annotate
it.

## Day one — refuse the route, at Henri's call

His pick, 2026-09-01, of the two shapes offered: **refuse**, not detect.

The reason detection cannot be the answer is measured above and is worth
stating plainly, because it is the thing a reader will want to argue
with: **a hook cannot see this defect.**  The rewrite happens before the
hook is handed the command, so the hook receives text in which the
expansion is already gone — an empty pair of backticks, a doubled space.
It has no way to know what was meant to be there.  A `PreToolUse` check
for braced expansions would inspect text they have already vanished from.
So the only thing a mechanism can act on is the *route*, not the damage:
a Bash command that writes a file through a heredoc is refused, and the
session is told to use the tool that does not pass through a shell.

What day one has to get right, and what will decide whether it is worth
having:

- **The boundary.**  A heredoc that writes or appends to a file is the
  route to refuse.  A heredoc that only computes and prints — a scratch
  measurement, a `python3 -` that reads and reports — is not, and
  refusing it would make the fence fight the work all day.  Where exactly
  that line falls is the build's real question and it is not answered
  here.
- **The message.**  A refusal that does not name the alternative is a
  wall.  It says: use the Write tool, then grep the result.
- **Red first**, and red on the actual defect: a fixture whose heredoc
  carries a braced expansion, refused; the same content through the write
  tool, allowed.

## What would make this card wrong

If the boundary cannot be drawn without refusing ordinary work.  A fence
rule that makes every scratch measurement a two-step is a tax paid on
every sitting to prevent a defect that has committed twice in nine days,
and at some width the tax is worse than the defect.  If day one's first
honest attempt at the boundary is that wide, the right answer is to say
so and close this card unbuilt — with the two cases above written down,
which is worth having on its own.

It would also be wrong if the harness stops doing it.  Nothing in this
tree controls that, and a card that waits on someone else's fix waits in
`later/`, not here.
