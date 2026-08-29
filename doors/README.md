# doors/ — where a model that is not the node's is admitted

A door is a directory here with a `door` file, read by `tools/door.sh`:
`url` (the OpenAI chat wire — the node's own port, OpenRouter, and
Anthropic's compatibility endpoint all speak it), `model`, `key` (a
file under the person's home, mode 600, never in the tree), and
`admitted` — who let this model in, when, and in what words
(card:model-acceptance.md: a door is where a refusal has somewhere to
sit).

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
