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

`tools  read ls grep` on a door file admits the mind to the tools it names
(`tools/executor.py` — `read`, `ls`, `grep` — one process under keep per call, run by the
courier `tools/deliver.sh`), and `calls  N` caps the calls a turn (8
unsaid); `tools/door.sh NAME --tools` reads the two.  Absent, a turn
carries no tools.  Every call is a `C:` line on the record
(card:tools.md, day one, 2026-08-30).

`thinking  template` says the door's side takes the node's own off
switch — `chat_template_kwargs.enable_thinking`, llama-server's wire —
and the knob then goes out beside the model's name, off unless asked.
Absent, the side has no off switch: thinking is asked in OpenRouter's
`reasoning` spelling and a turn that did not ask gets the model's own
default, and the account says so.  The door for the node at its own
port (`doors/llm/door`) is the one that carries it: without the word,
its first turn on 2026-09-02 thought 7,222 bytes into the content
channel under an account line that said "thinking off" (F015).

`tools/lead.sh NODE --door NAME` and `TEND_DOOR=NAME tools/propose.sh …`
run the same turn through the door instead of the node's port, on the
person's side; the account and the proposal say which door.  A kept
turn through a door that calls out is not built (keep's `--connect` is
one loopback port) and says so; through a door at 127.0.0.1 — a node at
its own port, `llm/` — `--kept` is that one port, since 2026-09-04
(card:session-program.md).  The node with no door named is the loop as
it was: gemma, local, under keep.

Opened 2026-08-29 at Henri's "build capability for both gemma and
claude, also I'm thinking about subscribing to openrouter".  The model
names below are the doors' own vocabulary and a wrong one is a 404 on
the first turn, not a silent wrong model: a door names what it asks
for, and the door's side says what that means.
