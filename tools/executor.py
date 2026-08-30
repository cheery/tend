#!/usr/bin/env python3
#: asked-by: Henri, 2026-08-30 — "would it be time for tools?" / "ok. write a tools card." (card:tools.md, day one)
"""tools/executor.py — the two things a mind at the door may do, one call a run.

    tools/executor.py --manifest [NAME ...]    the `tools` array for the wire, one line per tool, by name
    tools/executor.py read PATH                a file under the tree's parts
    tools/executor.py ls DIR                   a directory under the tree's parts

A program with a grant, never a party (card:tools.md): it does one call
and exits, and what it may reach is keep's to say — tools/deliver.sh
runs it as `keep.py --allow <each of the tree's parts> --no-net
--write /dev/null -- executor.py read PATH`.  A path outside the parts
is refused by the kernel, and the refusal is the call's result, printed
as itself: the executor never judges a path, so it can never be talked
into one.  It prints one JSON object — `c`, the line the record shows
(`read board/lander.md → 2.1k chars`), and `result`, what the model
gets — and exits 0 whether the call was served or refused; exit 2 is a
call it does not know.

The tools are named what the training data calls them — `read`, `ls` —
and described in one line each; the manifest is under 1 KB and
test/test_executor.py is red past it.  The tree is TEND_TREE or this
file's own; a relative path is under it, `~` is the person's home, and
both are handed to the kernel as they are.
"""
import json
import os
import sys

ROOT = os.environ.get("TEND_TREE") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
READCHARS = int(os.environ.get("TEND_READCHARS") or 12000)

TOOLS = {
    "read": ("a file under the tree's parts, by path", "path"),
    "ls": ("a directory under the tree's parts; the open board is ls board/", "dir"),
}


def manifest(names=()):
    """The wire's `tools` array: name, one sentence, one string parameter."""
    out = []
    for n, (what, arg) in TOOLS.items():
        if names and n not in names:
            continue
        out.append({"type": "function", "function": {
            "name": n, "description": what,
            "parameters": {"type": "object", "properties": {arg: {"type": "string"}}, "required": [arg]}}})
    return out


def _where(p):
    p = os.path.expanduser(p or "")
    return p if os.path.isabs(p) else os.path.join(ROOT, p)


def _size(n):
    return f"{n} chars" if n < 1000 else f"{n / 1000:.1f}k chars"


def _refusal(e):
    if isinstance(e, PermissionError):
        return "refused by keep"
    if isinstance(e, FileNotFoundError):
        return "not there"
    if isinstance(e, IsADirectoryError):
        return "a directory — ls it"
    if isinstance(e, NotADirectoryError):
        return "not a directory — read it"
    return f"refused: {e.strerror or e}"


def read(path):
    try:
        with open(_where(path), encoding="utf-8", errors="replace") as f:
            text = f.read(READCHARS + 1)
    except OSError as e:
        return _refusal(e), _refusal(e)
    if len(text) > READCHARS:
        text = text[:READCHARS] + f"\n[… cut at {READCHARS} chars]"
        return f"{_size(READCHARS)}, cut", text
    return _size(len(text)), text


def ls(d):
    try:
        names = sorted(os.listdir(_where(d)))
    except OSError as e:
        return _refusal(e), _refusal(e)
    base = _where(d)
    lines = [n + ("/" if os.path.isdir(os.path.join(base, n)) else "") for n in names]
    return f"{len(lines)} entries", "\n".join(lines)


def call(name, arg):
    if name == "read":
        return read(arg)
    if name == "ls":
        return ls(arg)
    raise KeyError(name)


def main(argv):
    if len(argv) >= 2 and argv[1] == "--manifest":
        unknown = [n for n in argv[2:] if n not in TOOLS]
        if unknown:
            sys.stderr.write(f"executor: no tool named {', '.join(unknown)} — the tools are {', '.join(TOOLS)}\n")
            return 2
        print(json.dumps(manifest(argv[2:]), separators=(",", ":")))
        return 0
    if len(argv) != 3 or argv[1] not in TOOLS:
        sys.stderr.write(__doc__.split("\n\n")[1] + "\n")
        return 2
    c, result = call(argv[1], argv[2])
    print(json.dumps({"c": f"{argv[1]} {argv[2]} → {c}", "result": result}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
