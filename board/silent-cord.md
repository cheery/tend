# silent-cord — the andon sounds only through a reach row the session must be allowed

    status   open
    because  the andon is the session's one way to reach the person when
             it is stuck, and its sound travels through the `audio` reach
             row — so the moment the person narrows what a session may
             touch (`tend-reach-allow` without `audio`, one line, the
             normal case), the cord goes quiet.  Measured 2026-08-28,
             from a fenced session: with `audio` out of the bound,
             `REACH=audio tools/andon.sh ring` is denied by the hook
             before it runs, and a bare `ring` fails at the player —
             loud, logged as `ring-failed`, `pulled` false.  Never
             silent, and still no sound: the person narrowed reach and,
             without meaning to, cut the line the session is supposed to
             use when it needs him.  What a session may touch and what
             it may say were tied together by the first row ever allowed
    asked    Henri, 2026-08-28 — "the andon needs to sound even with no
             sound allowed"; then "andon card"
    see      card:cords.md (done/) — the andon as built: ask, ring, be
             answered; the ring through the PipeWire socket, the `audio`
             row the socket alone; the record in ~/.local/state/tend
             card:session-program.md §2026-08-28 — where the problem was
             first noted, the morning's measurement in full
             tools/andon.sh — the mechanism; its header says the sound
             needs the row and fails loudly without it (Rule 9), which is
             the half that is right
             tools/fence-hook.sh — where a `REACH=audio` is granted or
             refused against TEND_REACH_ALLOW; tools/reach-allow.sh — the
             person's bound, one line to narrow
             tools/resolve.sh — the shape that already exists for "a
             thing the session may not do, done on the person's side on
             the session's prompt": a PostToolUse hook, unfenced,
             protected, reading a record the session wrote
             card:work-environment-ai.md — the boundary; the cord must not
             become a door through it

## What it is

Two things the fence governs got one switch.  *Reach* is what a
session may touch — the network, the bus, the sound card, the display
— and the person sets its bound; narrowing it is right and cheap.
*The cord* is what a session may say to the person when it cannot go
on, and the whole point of a cord is that it works when everything
else has been taken away.  Today the cord is a reach: the sound is a
player inside the fence talking to a socket the row lets through.  The
record half is already on the person's side (`andon.pending` and
`andon.log` pass through the fence and `limit.sh` reads them from
outside); the sound half is not.

## What would make this card wrong

If `audio` is never actually narrowed — if the row stays allowed on
every machine tend runs on, always — then the cord never goes quiet and
this is a defect on paper.  Two things say otherwise: the reach bound
exists to be narrowed and its one-line tool makes it the normal act,
and the work laptop (the next machine) has no row set yet at all.  It
would also be wrong if a person prefers the cord to obey the reach
bound — "no sound means no sound" — but Henri said the opposite, in
those words.

## What it must not become

* **A door.**  The sound moving to the person's side must carry
  nothing but the fact that the record has a question in it — no
  text, no argument, no command.  A session that can make the person's
  side *do* something on its prompt has a channel; the resolver's
  discipline holds: the person's side reads a record and acts on its
  own rule, never on the session's words.
* **A probe.**  Every ring reaches the person.  Tests ring a fake
  player; the one real ring is his to hear and answer (`card:cords.md`:
  "a cord is never a probe", five rings paid for that lesson).
* **A daemon.**  Nothing waits in the background holding the sound
  card.  The person's-side hook runs when it already runs, reads the
  record, rings if a ring is wanted, and exits — the resolver's cost.
* **Louder or more frequent.**  gestate's numbers stay: three rings,
  eight seconds apart, ten minutes of quiet; a cord on the person's
  side is the same cord with the row taken out of the path.

## Where it sits

Placed last by the session that wrote it on 2026-08-28, at Henri's
"andon card"; the tiebreak is his.  Day one is the sound on the
person's side, shown red first with the row off — this morning's
measurement is the red — and then green with the row off; then his
`tend-reach-allow` without `audio` and one ring he hears, which is the
demonstration and the only one there is.

## 2026-08-28, 10:07 — the row was on and the cord was still silent

At Henri's "you can also try andon there", a session inside the fence
rang the andon with the `audio` row allowed (`TEND_REACH_ALLOW` carried
`net,audio,display`, and `REACH=audio tools/andon.sh ring 2` was the
call).  It did not sound.  Not the failure this card was opened for —
the row was *on* — but a second one beneath it: on the work laptop
there is no PipeWire socket at `$XDG_RUNTIME_DIR/pipewire-0` for the
`audio` row to bind (the fence's `/run/user/1000` held only
`gestate-sitting-1000`), so `pw-play` reached no server and the ring
failed loudly (`ring-failed player=pw-play` in `andon.log`).  The
alternate channels are no better from here: `notify-send` exists and
`WAYLAND_DISPLAY` is set, but the fence binds neither the Wayland nor
the D-Bus session socket, so a desktop notification cannot travel
either.

**What it means for this card.**  The andon's sound rides one host
socket, and that socket is not a given — a different machine, a
headless session, a PipeWire that is not running, and the person in the
next room hears nothing while the row reads *allowed*.  The record held
(the question is in `andon.pending`), which is the cord's other half
doing its job; but a record the person is not looking at is not a reach.
So `silent-cord`'s day one is larger than "red with the row off": the
cord needs a fallback that does not assume PipeWire — the plainest being
that a ring which cannot reach a sound server says so *to a channel the
person will see* (a marked line the lander/limit lamp surfaces, a file
the person's shell greets them with), and the andon's exit already
distinguishes "no server" from "row off" for it to branch on.  Measured
red here, on the machine, before any of it is built.

## 2026-08-28, 10:18 — the socket is there; the fence is what blocks

Henri checked the host: `/run/user/1000/pipewire-0` is a live socket and
`pipewire`/`pipewire-pulse` have run since 06:26.  So the 10:07 reading
("no socket") was the fence's view, not the machine's — the socket
exists and the fenced session cannot see it.  With `audio` allowed and
`REACH=audio` on the ring, a command inside the fence still reports
`XDG_RUNTIME_DIR=/run/user/1000` with no `pipewire-0` beneath it, and
the ring fails at `pw-play` all the same.  A hard `--bind` of a source
that exists would not vanish silently, so the audio row is not reaching
the exec that runs a session's command — most likely because the
session already runs fenced (`TEND_FENCED=1`) and a per-command
`--reach audio` nests inside a parent fence that never bound the socket,
so there is nothing in the child's parent namespace to bind.

**This is the sharper finding.**  The andon is a *session's* cord — its
whole purpose is a restrained session reaching the person — and a
restrained session is exactly where the sound does not travel.  The row
being allowed is necessary and not sufficient; the socket must be in the
namespace the ring runs in.  Two shapes for the build, and the choice is
Henri's: the session's own fence carries `audio` (binds the socket at
session start when reach allows it, so a nested ring inherits it), or the
ring is delegated to the host side — the resolver, which starts a node's
runner outside the fence, carries the andon too, and a fenced session
that pulls the cord hands the ring across the same seam a pull already
crosses.  The record-and-fallback of §10:07 still stands beneath either:
a ring that cannot sound says so to a channel the person sees.

*Confirmed, 10:20: `tools/andon.sh ring 1` from Henri's shell outside the
fence rang clean (`pw-play` exit 0) against the real socket.  The
mechanism is whole; the fence is the whole of the gap, and the build is
one of the two shapes above — the sound need not be rebuilt, only carried
across the seam.*