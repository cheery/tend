# lock-test — the tree tests a lock by taking it, so two tests of one lock collide, and every such collision is a latent flake nobody has found yet

    status   open
    because  Henri, 2026-09-03, after F019 and F020: "flaket olivat todella
             aikaa vieviä. mitä seuraavalla kerralla voidaan tehdä?"  The
             two flakes that ate a sitting were one root: the tree asks "is
             this lock held?" by taking the lock — a momentary exclusive
             `flock -n "$X" true` — and two such tests of one lock collide
             for the microseconds either holds it.  On the release side a
             reader read a let-go edge as held (F019); on the start side a
             reader read a free lock as held and left a pulled node
             unstarted, its puller hung (F020).  Each was found and fixed
             one at a time, statistically, under load.  The idiom is on
             about eleven sites still — `pulled_by`, `status`, the panel's
             `_lock_held`, serve's and pull's guards — and any two of them
             colliding is the next flake of the same family, latent and
             unfound, and as slow to chase as the last two
    asked    Henri, 2026-09-03 — "Avaisitko kortin vankasta lukkotesti-
             primitiivistä? ja lisää siihen mukaan tuo testiapuri."
    see      F019 (the release side — a watcher's poll made a let-go edge
             read as held), F020 (the start side — a node never served
             because two guards read a free lock as held), card:flake.md
             (the ledger and the shake — the instrument this card would
             make sharper), card:edge.md (the edge is a shared flock a
             puller holds; the reads that test it are this card's subject),
             card:hold.md (the same idiom, the resolver's lock test),
             tools/launch.sh (pulled_by, status, serve, the guards),
             tools/panel.py (`_lock_held`)

## What it is

An advisory lock is held or it is not, and the tree asks which by trying
to take it: `flock -n "$X" true` fails when someone holds it and succeeds
when no one does.  The trouble is that the *test itself takes the lock* —
exclusively, for the microseconds `true` runs — so a test is
indistinguishable, to another test, from a real holder.  Two readers
testing one lock at the same instant see each other, not the truth.  And
a puller holds its edge **shared**, so an exclusive test always fails
against it (that part is reliable); the unreliability is the reverse — a
reader's momentary exclusive lock makes a *free* lock read as held, and a
watcher or a guard that decides on one such read decides wrong.

F019 and F020 are this defect on two sides, and both fixes said the same
thing in the small: do not decide from one test.  F019's release
assertions poll for the edge to free; F020's serve concludes "a runner is
up" only if the lock fails the test across ten tries, and its watcher
stops reading the lock at all, waiting on lock-free signals (`run.pid`,
`stopped`) instead.  Each fix hardened one site.  The card is that the
**idiom is everywhere the fix is not**, and the family is not closed: the
next collision is latent in `pulled_by`, in `status`, in `_lock_held`, in
the resolver's guard, waiting for the load that trips it.

Two things make it a card and not a fix already done:

- **The class, not the instance.**  Eleven sites share one fragile idiom.
  Fixing them as they surface is what cost a sitting; one robust test used
  everywhere is the class closed at once — a `held` primitive that
  concludes "held" only when the lock fails the test consistently (a real
  holder does; a reader's momentary lock cannot, it is gone by the next
  try), replacing every raw `flock -n true` read.
- **The instrument the finding needed.**  What turned F019 and F020 from
  hours to minutes was forcing the collision deterministically — a hammer
  that takes and drops the lock in a tight loop (F020: 24 of 40 pulls hung
  under it, where load alone reproduced nothing), and, for a clean
  regression, holding the contended lock for a fixed window while the code
  under test runs (F020's day-one test held the run lock 0.1 s).  The tree
  has no such helper; each flake this family throws is reproduced from
  scratch.  A test helper — a hammer and a hold-for-a-window — is the
  second half of this card, so the *next* one is a written test, not a
  morning of scratch harnesses.

## What would make this card wrong

If a retrying `held` cannot in fact tell a real holder from a hammer —
a sustained hammer holds the lock across every try, exactly as a real
runner does — then the read is genuinely undecidable from the lock alone,
and the answer is not a better test but a **lock-free signal**, which is
what F020 already reached for (`run.pid` naming a live process, a
`stopped` file).  If most of the eleven sites turn out to be decisions
that should ride on such a signal rather than a lock test, the primitive
shrinks to the few genuine reads and this card is mostly the audit that
found that out.  It is also wrong if the collisions are rare enough in
the real system (no test's poll, no shake) that only the tests ever felt
them — in which case the fix is the tests polling (as F019 and F020 did)
and the primitive is for the test helper alone.

## What it must not become

A test that **blocks**: a lock read must stay non-blocking, or `status`
and the panel wait on a runner that will not let go.  A primitive that
**hides a real held lock** by retrying past it — the retry concludes
held, never free, when the lock stays taken.  A replacement for the
lock-free signals where those are the right answer (`run.pid`, `stopped`):
the primitive is for reading a lock, not for deciding whether to start a
runner, which F020 settled belongs on a signal no lock test can fake.
And the hammer must live in the tree's test helpers, never on a path a
node runs — it is an instrument for finding the flake, not a thing the
fence has to reason about.

## Day one — proposed, not declared

A `held PATH` helper in `tools/launch.sh` (and its twin in
`tools/panel.py`): tries `flock -n` a few times with a short sleep and
reports held only if every try fails — one success is a free lock.  Swap
the read-only sites to it (`pulled_by`, `status`, `_lock_held`, the bind
check), and leave the decision sites that F020 already moved onto
lock-free signals alone.  The test helper: a hammer (`hammer PATH` — take
and drop the lock in a tight loop, in the background, stopped on exit) and
a hold-for-a-window (`hold PATH SECONDS`), in `test/`'s helpers.  Red
first: a regression test that reproduces the collision under the hammer —
the raw `flock -n true` read flips to a wrong answer, the `held`
primitive does not — and the F020-shaped hold-the-lock test as its
deterministic sibling.  The measurement is the shake: a site read through
`held`, hammered, goes from flaky to 0, the way F019 and F020 did, but now
in one place for the whole family.

## Where it sits

Placed last by the session that wrote it, at his "Avaisitko kortin", as
the sitting's work closed; the tiebreak is his.
