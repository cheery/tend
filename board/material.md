# material — a node that asks the llm about tend gets the dictionary, because it may read nothing of the tree

    status   open
    because  Henri, 2026-09-02 16:4x, after the first conversation over an
             edge: "hmm. ask voisi kyllä olla jotenkin järjestetty siten
             että se voi lukea puuta."  The `ask` node asked the llm
             "Mitä varten tend on?" and was told, correctly, that tend is
             an English verb: what a node knows is what its grant lets it
             read, and `ask/grant` lets it read `llm/state` and nothing
             of the tree.  The tree has two ways to put its own words in
             front of a mind — the courier's digest and the read tool —
             and neither is a grant word a node can carry, so a node's
             conversation with the llm is always cold
    asked    Henri, 2026-09-02 — "tee siitä kortti", closing the sitting
    see      card:edge.md — the third live run, 16:29: the answer verbatim
             and the sentence this card is cut from ("what it may read
             is a grant word, and what it is handed is the courier's")
             card:tools.md — the read tool under keep, every call a line
             on the record; a mind reading the tree by asking
             card:simpleqa.md, doc/cold/ — what material does and does
             not buy: sourced assertions, not fewer wrong answers
             tools/propose.sh — "Material:" lines, the digest as a
             program hands it
             tools/deliver.sh, tools/executor.py — the courier and the
             executor, the two existing readers
             tools/launch.sh — `pull NODE` as the shape: a word that
             grants a read and tells the program where (`$TEND_PULLS`)
             card:private.md — what a mind reads is public by
             construction; this card adds nothing private

## What it is

A node is bounded by its grant, and that is right: rule 1, every
restraint from outside, and `ask`'s answer is the boundary working.
The tree already has two readers for a mind:

1. **The digest.**  A program reads tree files on the person's side and
   puts them in the prompt — `propose.sh`'s `Material:` lines, `lead.sh`'s
   seat.  The mind reads what it was handed, and the record says what.
2. **The tool.**  The mind asks for a file by name and `executor.py read`
   runs under keep with the tree's parts readable, one process per call,
   a `C:` line on the record (`card:tools.md`, day one).

Both run on the person's side of keep.  A *node* runs inside it, and
has neither: `ask` cannot read `board/README.md` to hand it over, and
cannot run an executor.  The missing piece is a grant word, and the tree
has its shape already in `pull NODE`: a word that **grants a read and
tells the program where** — `material PATH`, an `allow` on the path and
the path named in `$TEND_MATERIAL`, so the program knows what it may
put in front of the mind and the grant says, from outside, what a
node's conversation may be *about*.  A node with `material board/README.md`
asks with the board in hand; a node with none asks cold, as `ask` did,
and the difference is measurable on the same question.

Three things make it a card and not a line:

- **What a node may read is a decision, not a default.**  The tree
  bound whole would make the node a session (`card:tools.md`: "a tool
  executor with the person's reach would be a session with no fence").
  A path at a time, deny by omission, is the fence's own idiom.
- **Material is the first gift.**  `card:edge.md`'s talk put the node's
  grant as the floor and the person's additions between it and the
  ceiling; what a node may read of the tree is exactly a person's
  addition — this machine's, this person's tree — and the first case
  where the floor-and-gifts picture has a caller.
- **It is a measurement before it is a feature.**  `card:simpleqa.md`
  measured that tools bought sourced assertions and not fewer wrong
  answers; `doc/cold/` measured the cold arm.  The same question, cold
  and with material, is one more arm on the same instrument.

## What would make this card wrong

If the answer with `material board/README.md` is no better than the
dictionary — the mind ignores what it is handed, or the 800-token cap
is spent reading — then the missing piece is not a grant word but the
courier's digest (`tools/deliver.sh`) or a bigger mind, and this card
closes pointing there.  It is also wrong if the right shape is the
tool and not the digest — the mind asking for files, through a node —
in which case the executor moves inside keep and that is `card:tools.md`'s.

## What it must not become

A node with the tree bound whole; a mind writing the tree (reads only,
and every write is still a proposal — `card:tools.md`, `card:private.md`);
a second courier (the digest's shape is `propose.sh`'s and is reused,
not rewritten); and a way for a node to widen its own reach — the word
is in the grant, the grant is the person's, and `material` with no
grant is refused at the door like `pull` and `connect`.

## Day one — proposed, not declared

`material PATH` in `tools/launch.sh`: `--allow PATH` to keep, the paths
in `$TEND_MATERIAL`, refused at parse when the path is not there; the
check lists them.  `ask` reads `$TEND_MATERIAL`, puts each file under
its name in front of the question as `propose.sh` does, and says in
`answer` what it handed over.  Red first: `ask` with `material
../board/README.md` and no such word, refused by keep on the read.  The
measurement: the 16:29 question again, cold (the 16:29 answer is the
baseline, on `card:edge.md`) and with `material board/README.md`,
`vision.md` — the same mind, the same tokens, the answers side by side
in `ask/state/answer`.  What the tokens cost is part of the measurement:
gemma4 spent 200 on thinking with nothing to read.

*(question, measure — does material change the answer at all, and at
what token cost? the day-one run, both arms, is what answers it)*

## Where it sits

Placed last by the session that wrote it, at his "tee siitä kortti", as
the sitting closed; the tiebreak is his.
