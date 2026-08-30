#!/usr/bin/env python3
#: asked-by: Henri, 2026-08-30 — "would it be time for tools?" / "ok. write a tools card." (card:tools.md, day one)
"""tools/executor.py — the things a mind at the door may do, one call a run.

    tools/executor.py --manifest [NAME ...]    the `tools` array for the wire, one line per tool, by name
    tools/executor.py read PATH                a file under the tree's parts
    tools/executor.py ls DIR                   a directory under the tree's parts
    tools/executor.py grep PATTERN PATH        lines matching a regex under a path, as path:line: text
    tools/executor.py NAME '{"...": ...}'      the same, the arguments as the wire sends them

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

The tools are named what the training data calls them — `read`, `ls`,
`grep` — and described in one line each; the manifest is under 1 KB and
test/test_executor.py is red past it.  `grep` arrived on the first
tooled turn (2026-08-30 15:07, qwen through the openrouter door: "Hmm,
I can't grep"), a want measured before it was built.  The tree is
TEND_TREE or this file's own; a relative path is under it, `~` is the
person's home, and both are handed to the kernel as they are.
"""
import json
import os
import re
import sys

ROOT = os.environ.get("TEND_TREE") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
READCHARS = int(os.environ.get("TEND_READCHARS") or 12000)
GREPLINES = int(os.environ.get("TEND_GREPLINES") or 200)

# name → (one sentence, the parameters in order)
TOOLS = {
    "read": ("a file under the tree's parts, by path", ("path",)),
    "ls": ("a directory under the tree's parts; the open board is ls board/", ("dir",)),
    "grep": ("lines matching a regex under a path in the tree's parts, as path:line: text", ("pattern", "path")),
}


def manifest(names=()):
    """The wire's `tools` array: name, one sentence, string parameters."""
    out = []
    for n, (what, params) in TOOLS.items():
        if names and n not in names:
            continue
        out.append({"type": "function", "function": {
            "name": n, "description": what,
            "parameters": {"type": "object", "properties": {p: {"type": "string"} for p in params}, "required": list(params)}}})
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


def grep(pattern, path):
    """Every line under PATH (a file, or a directory walked, files by name)
    that the regex matches, as `path:line: text`; the paths as given,
    relative to the tree when the call was.  Capped at GREPLINES."""
    try:
        rx = re.compile(pattern)
    except re.error as e:
        return f"bad pattern: {e}", f"bad pattern: {e}"
    top = _where(path)
    errs = []   # a directory the walk could not list: the top is a refusal, a deeper one is counted
    try:
        if os.path.isdir(top):
            files = []
            for d, dirs, names in os.walk(top, onerror=errs.append):
                dirs.sort()
                files += [os.path.join(d, n) for n in sorted(names)]
            for e in errs:
                if e.filename == top:
                    raise e
        else:
            with open(top, "rb"):
                pass
            files = [top]
    except OSError as e:
        return _refusal(e), _refusal(e)
    out = []; hit = set(); unread = len(errs); cut = False
    shown = path if path else "."
    for f in files:
        rel = os.path.join(shown, os.path.relpath(f, top)) if f != top else shown
        rel = os.path.normpath(rel) if not rel.startswith("~") else rel
        try:
            with open(f, encoding="utf-8", errors="replace") as fh:
                for i, line in enumerate(fh, 1):
                    if rx.search(line):
                        if len(out) >= GREPLINES:
                            cut = True; break
                        out.append(f"{rel}:{i}: {line.rstrip()}"); hit.add(rel)
        except OSError:
            unread += 1
        if cut:
            break
    n = len(hit)
    c = f"{len(out)} line{'s' if len(out) != 1 else ''} in {n} file{'s' if n != 1 else ''}"
    if cut:
        c += f", cut at {GREPLINES}"
    if unread:
        c += f", {unread} unreadable"
    text = "\n".join(out) if out else "no match"
    if cut:
        text += f"\n[… cut at {GREPLINES} lines]"
    return c, text


def call(name, args):
    what, params = TOOLS[name]
    values = [args.get(p, "") for p in params]
    fn = {"read": read, "ls": ls, "grep": grep}[name]
    return " ".join([name] + values), fn(*values)


def main(argv):
    if len(argv) >= 2 and argv[1] == "--manifest":
        unknown = [n for n in argv[2:] if n not in TOOLS]
        if unknown:
            sys.stderr.write(f"executor: no tool named {', '.join(unknown)} — the tools are {', '.join(TOOLS)}\n")
            return 2
        print(json.dumps(manifest(argv[2:]), separators=(",", ":")))
        return 0
    if len(argv) < 3 or argv[1] not in TOOLS:
        sys.stderr.write(__doc__.split("\n\n")[1] + "\n")
        return 2
    name = argv[1]; params = TOOLS[name][1]
    if len(argv) == 3 and argv[2].lstrip().startswith("{"):
        try:
            args = json.loads(argv[2])
        except ValueError:
            args = {}
        if not isinstance(args, dict):
            args = {}
        if len(params) == 1 and params[0] not in args and len(args) == 1:
            args = {params[0]: str(next(iter(args.values())))}   # the one parameter, however the model named it
        args = {k: str(v) for k, v in args.items()}
    elif len(argv) == 2 + len(params):
        args = dict(zip(params, argv[2:]))
    else:
        sys.stderr.write(f"executor: {name} wants {' '.join(p.upper() for p in params)}\n")
        return 2
    said, (c, result) = call(name, args)
    print(json.dumps({"c": f"{said} → {c}", "result": result}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
