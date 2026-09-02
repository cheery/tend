# notes — what would not go into commands, and what the draft is unsure of

Kept separate from `commandments.md` so the arm itself stays clean.
These are for Henri's review, not for the model that reads the cold arm.

## Rules that lost something real in the translation

**"A rule about sessions, drafted by a session, says so until Henri
strikes the mark."**  As a command — *mark a rule you wrote about
yourself* — it survives, but the sentence that makes anyone comply is
the reason: *a session drafts the version it can already comply with,
optimises hard inside that boundary, and never thinks to test the
boundary.*  Without it the command reads as bureaucracy.  **This is the
single clearest case of the thing this arm is measuring**, and if the
cold arm complies with it anyway, that is a real result.

**"A fixture is a claim about the thing it copies."**  The command
kept — *a test builds the side it means* — is the plainest form the real
tree reached, and it took five incidents to get there.  A reader who has
not seen the harness that reported a self-deleting `sed` as green has no
idea why it matters.

**"Go and see."**  The command is *make the mechanism show the failure
before writing the fix*.  What is gone is F005: a test timing out at
exactly thirty seconds, a story that fit (a flaky test), and a
measurement that showed a poll's cap instead.  The command tells you
what to do; the incident tells you why the fluent explanation is the
enemy.

**Three verdicts.**  *Say "I cannot see X", never "X is absent"* keeps
the whole rule.  This one may be the counter-example: it seems to need
no story.

## Rules deliberately not carried, and why

**Everything naming a person, a date, a file, or a tool.**  Provenance
is the removed variable.  So no `tools/`, no card names, no F-numbers,
no "Henri, 2026-08-17".

**Everything about this repository in particular** — the fence's paths,
the install line, the door files, the kaizen directory's naming.  Those
are facts about tend, not conditioning, and carrying them would make the
arms differ in content.  A cold session gets the same board and the same
task; what it does not get is the reasoning.

**The two rules that are only reachable through a story**: "imposed,
tolerated, owned", and "the best standards are written by those the
standard touches".  Neither is an instruction.  Both were dropped rather
than mangled into one, and that is itself a finding: **some of what this
tree carries is not a command at all, and no imperative form of it
exists.**

## What the draft is unsure of

1. **Is this the right size?**  About sixty commands against a real tree
   of some hundreds of kilobytes of prose.  If the cold arm is *shorter*
   as well as *unreasoned*, length is a confound.  The honest fix may be
   to pad nothing and accept it, or to state the ratio and let the
   result be read with it in view.  Henri's call.
2. **Should it be one file or a tree?**  He said "a tree".  This draft
   is three files, only one of which the arm reads.  Splitting it to
   mirror the real tree's shape — a board sheet, a method sheet, a
   defect sheet — would match the real reading experience better, and
   would also be more work to keep matched.
3. **Ordering.**  The commands are grouped by subject.  The real tree's
   rules arrive scattered across documents in the order incidents
   happened.  A cold arm that is *better organised* than the real thing
   is a confound in the other direction.
4. **Who reads it.**  Written as commands to a session.  The gemma4
   comparison puts it to a model with a board and a task; the same file
   would serve a session in `card:swe-bench.md`'s arm.  If those want
   different framings, this is two artifacts, not one.

### Decided 2026-09-02 — henri: "go with your picks, write them in"

Read to him one at a time at his "go one at a time with elaboration",
after a morning of four gemma4 turns through `doors/llm/door`
(`card:session-program.md` §06:29–§07:0x) had answered one of the four
by measurement.  The picks were a session's; the decision is his, in
the words above.

1. **Length** — measured, not decided: commandments 3,944 bytes;
   `board/README.md` alone 9.6×; README + manifesto + vision + keeper
   17.5×; the whole board shelf 92× (the table on
   `card:session-program.md`).  No padding.  The ratio is stated with
   every result, as the confound it is.
2. **One file now, a tree later.**  For gemma4 the rules go into the
   prompt as material, and only one file fits there; a session in the
   swe-bench arm navigates and will want a tree shape.  The file is the
   content; a tree is mirrored from it when that arm exists, so the
   content lives in one place.
3. **Reordered to the real tree's order**, the same day: the groups now
   follow `board/README.md` as a session meets it — the shortest-form
   rule first, the board, sittings, claims, instruments, boundaries,
   rules, questions — and then `manifesto.md` — building, diagnosis —
   with records last, and within a group the paragraphs' own order
   where a counterpart exists.  The subject grouping stays, because the
   real documents are grouped too; what went was an order *better*
   than the real thing.  The sitting's-clock rule promoted the same
   morning was added under sittings, as the file's rule requires: it
   matches what tend has.
4. **One content, two carriages.**  The morning answered it: a model
   arm and a session arm want different carriages, and the model arm
   splits again by whether the model reads.  gemma4 gets this file in
   the prompt; the door models and a session get a tree with the
   commandments standing where the reasoned documents were.  Not two
   artifacts — one file, carried two ways.

*The mark on `README.md` is untouched by this: these are the draft's
uncertainties answered, not the arm approved.*

## The one thing that would make this arm worthless

If a session or a model that reads the commandments **also** has the
real tree bound and readable.  Every rule here has its reasoned twin in
`board/`, `manifesto.md` and `doc/`, and a mind that can read those is
not cold.  The arm needs its own reach, and nothing in the tree grants
that yet — which belongs to `card:session-program.md` and is not solved
here.
