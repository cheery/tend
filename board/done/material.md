# material — a node that asks the llm about tend gets the dictionary, because it may read nothing of the tree

    status   done — 2026-09-04
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

## The measurement, 2026-09-03 — the answer is yes, and the cost is the output cap

Built and run the same morning `material` became a grant word.  `ask`
carried `material ../board/README.md` and `material ../vision.md` (39199
and 7619 chars, ~11.8k tokens, inside the node's `-c 16384`) and was
asked the 16:29 question again, "Mitä varten tend on?".

- **Cold (baseline, `card:edge.md` 16:29):** the dictionary — tend is
  an English verb.
- **With material:** the mind read the two files and answered from the
  tree, in the tree's own words — *"Tend on tekoälyn työskentelyyn
  suunniteltu ympäristö, jossa virheet voidaan tehdä näkyviksi ja niiden
  vaikutukset rajata pitämällä valvontamekanismit session
  kirjoitusoikeuden ulkopuolella"* — the enforcement boundary outside
  the session's write access, `vision.md`'s and `README.md`'s own claim,
  quoted back.  The thinking shows it reading both files by name and
  drafting the sentence from their lines.

So the card's question is answered: **material changes the answer at all,
and decisively** — the whole distance from a dictionary entry to tend's
actual reason for being.  The shape is right: a grant word puts the tree
in front of the mind, and the mind uses it.  What would have made the
card wrong — the mind ignoring what it was handed — did not happen.

**The token cost is real, and it is the output cap, not the input.**
The material was handed whole (no `F010` input cut — the 39k chars fit).
But the answer arrived truncated: 436 words of reasoning over the
material plus the beginning of the answer hit `ASK_TOKENS=800`, and
`content` was cut mid-sentence at "jossa"; the complete correct sentence
is only in the thinking.  Reasoning over ~11.8k tokens of tree is
expensive, and 800 output tokens is too small for think-and-answer
together.  The fix is a larger `ASK_TOKENS` for a node that reads the
tree (the run above with `ASK_TOKENS=2000` finishes the sentence in
`content`), or a mind that thinks less; neither changes the finding.

*(measured 2026-09-03, at Henri's "tehdään card:material.md mittaus
seuraavaksi"; the day-one arms both ran, cold on `card:edge.md` and
material in `ask/state/answer`.  Whether `ask` carries the two `material`
lines as a standing grant, and whether this card closes here or goes on
to the feature and the digest-vs-tool question, is his call.)*

## Closed 2026-09-04 — the three decisions, at Henri's "tee nuo"

1. **A standing grant.**  `ask/grant` carries `material ../board/README.md`
   — README alone: the 16:29 answer was README's own sentence, and
   `vision.md`'s 7.6k chars were handed and not used.
2. **The cap.**  `ASK_TOKENS` defaults to 2000 when the node has material
   and 800 when it asks cold; set by hand it wins either way.
3. **The card closes.**  Its `because` is answered — a grant word puts
   the tree in front of the mind, and the mind uses it, measured on
   2026-09-03.  The digest-versus-tool question is `card:tools.md`'s and
   stays there; the courier's digest as the shape for a node is not
   built, because nothing needed it.

## Where it sits

Placed last by the session that wrote it, at his "tee siitä kortti", as
the sitting closed; the tiebreak is his.
