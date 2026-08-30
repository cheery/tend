# doors/ — where a model that is not the node's is admitted

A door is a directory here with a `door` file, read by `tools/door.sh`:
`url` (the OpenAI chat wire — the node's own port, OpenRouter, and
Anthropic's compatibility endpoint all speak it), `model`, `key` (a
file under the person's home, mode 600, never in the tree), and
`admitted` — who let this model in, when, and in what words
(card:model-acceptance.md: a door is where a refusal has somewhere to
sit).

`tools/door.sh NAME --models [PATTERN]` lists what the door's side
offers — id, context, price per M tokens — and `--use ID` sets the
door's `model` line to an id it lists (2026-08-30, Henri: "I'd need a
way to browse through all 500 models there are").

`tools  read ls` on a door file admits the mind to the two tools
(`tools/executor.py`, one process under keep per call, run by the
courier `tools/deliver.sh`), and `calls  N` caps the calls a turn (8
unsaid); `tools/door.sh NAME --tools` reads the two.  Absent, a turn
carries no tools.  Every call is a `C:` line on the record
(card:tools.md, day one, 2026-08-30).

`tools/lead.sh NODE --door NAME` and `TEND_DOOR=NAME tools/propose.sh …`
run the same turn through the door instead of the node's port, on the
person's side; the account and the proposal say which door.  A kept
turn through a door is not built (keep's `--connect` is one loopback
port; a door calls out) and says so.  The node with no door named is
the loop as it was: gemma, local, under keep.

Opened 2026-08-29 at Henri's "build capability for both gemma and
claude, also I'm thinking about subscribing to openrouter".  The model
names below are the doors' own vocabulary and a wrong one is a 404 on
the first turn, not a silent wrong model: a door names what it asks
for, and the door's side says what that means.
