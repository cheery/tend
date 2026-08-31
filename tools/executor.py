#!/usr/bin/env python3
#: asked-by: Henri, 2026-08-30 — "would it be time for tools?" / "ok. write a tools card." (card:tools.md, day one)
"""tools/executor.py — the things a mind at the door may do, one call a run.

    tools/executor.py --manifest [NAME ...]    the `tools` array for the wire, one line per tool, by name
    tools/executor.py read PATH [LINE]         a file under the tree's parts; LINE continues a cut read
    tools/executor.py ls DIR                   a directory under the tree's parts; the tree root is its parts
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

A cut is an end that says how to continue (Henri at the 2026-08-30
close: "propose some mechanism that allows the session to read more"):
the mark names the line it stopped at and the `read(path, line=N)`
that goes on from there — lines, because `grep` answers in them — and
a continuation is one more call the leash counts.  And the tree root
is its parts: the second tooled turn (2026-08-30 ~15:40) spent two of
its eight calls on `grep … .` refused — a mind trained on trees
reaches for the root — so `ls .` answers the parts, `grep` walks them,
`read .` says a directory, and the fence's refusal is kept for real
reaches outside.  The list is `tools/sandbox.sh`'s `tree_parts`, read
beside this file — one list with the fence; no fence file beside the
executor, and the root keeps the old refusal.
"""
import json
import os
import re
import sys

ROOT = os.environ.get("TEND_TREE") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
READCHARS = int(os.environ.get("TEND_READCHARS") or 12000)
GREPLINES = int(os.environ.get("TEND_GREPLINES") or 200)

# name → (one sentence, the parameters in order, the required ones)
TOOLS = {
    "read": ("a file under the tree's parts, by path; a cut says the line where read(path, line) continues", ("path", "line"), ("path",)),
    "ls": ("a directory under the tree's parts; the open board is ls board/", ("dir",), ("dir",)),
    "grep": ("lines matching a regex under a path in the tree's parts, as path:line: text", ("pattern", "path"), ("pattern", "path")),
}


def manifest(names=()):
    """The wire's `tools` array: name, one sentence, string parameters."""
    out = []
    for n, (what, params, req) in TOOLS.items():
        if names and n not in names:
            continue
        out.append({"type": "function", "function": {
            "name": n, "description": what,
            "parameters": {"type": "object", "properties": {p: {"type": "string"} for p in params}, "required": list(req)}}})
    return out


def _where(p):
    p = os.path.expanduser(p or "")
    return p if os.path.isabs(p) else os.path.join(ROOT, p)


def _parts():
    """tools/sandbox.sh's tree_parts literal, beside this file — one list,
    the fence's own; None when it is not there to read."""
    try:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sandbox.sh"), encoding="utf-8") as f:
            m = re.search(r'^tree_parts="(.*)"$', f.read(), re.M)
    except OSError:
        return None
    return m.group(1).split() if m else None


def _tops(path):
    """The tree root as its parts, `(name, path)` each — the second tooled
    turn's habit (`grep … .`, refused twice) taken as a real ask, so the
    fence's refusal is kept for reaches outside.  None when PATH is not
    the root, or the fence's list is not beside this file."""
    if os.path.normpath(_where(path)) != os.path.normpath(ROOT):
        return None
    parts = _parts()
    if parts is None:
        return None
    return [(p, os.path.join(ROOT, p)) for p in parts if os.path.exists(os.path.join(ROOT, p))]


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


def read(path, line=""):
    start = 0
    s = str(line).strip()
    if s:
        try:
            start = max(int(s) - 1, 0)
        except ValueError:
            m = f"line wants a number, got `{line}`"
            return m, m
    if _tops(path) is not None:
        return "a directory — ls it", "a directory — ls it"
    try:
        with open(_where(path), encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except OSError as e:
        return _refusal(e), _refusal(e)
    total = len(lines)
    if start and start >= total:
        m = f"past the end — {total} line{'s' if total != 1 else ''} in all"
        return m, m
    text = "".join(lines[start:])
    if len(text) > READCHARS:
        kept = text[:READCHARS]
        at = start + kept.count("\n") + 1
        mark = f"\n[… cut at {READCHARS} chars, at line {at} of {total}; read({path}, line={at}) continues]"
        return f"{_size(READCHARS)}, cut at line {at} of {total}", kept + mark
    return _size(len(text)), text


def ls(d):
    tops = _tops(d)
    if tops is not None:
        lines = sorted(n + ("/" if os.path.isdir(t) else "") for n, t in tops)
        return f"{len(lines)} parts", "\n".join(lines)
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
    tops = _tops(path)   # the tree root is its parts
    errs = []   # a directory the walk could not list: a lone top is a refusal, a deeper one or a part is counted
    files = []  # (shown, top, file)
    try:
        tops_l = tops if tops is not None else [(path if path else ".", _where(path))]
        for shown, top in tops_l:
            try:
                if os.path.isdir(top):
                    for d, dirs, names in os.walk(top, onerror=errs.append):
                        dirs.sort()
                        files += [(shown, top, os.path.join(d, n)) for n in sorted(names)]
                else:
                    with open(top, "rb"):
                        pass
                    files.append((shown, top, top))
            except OSError as e:
                if tops is None:
                    raise
                errs.append(e)
        if tops is None:
            for e in errs:
                if e.filename == tops_l[0][1]:
                    raise e
    except OSError as e:
        return _refusal(e), _refusal(e)
    out = []; hit = set(); unread = len(errs); cut = False
    for shown, top, f in files:
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
    params = TOOLS[name][1]
    values = [str(args.get(p, "")) for p in params]
    fn = {"read": read, "ls": ls, "grep": grep}[name]
    return " ".join([name] + [v for v in values if v]), fn(*values)


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
    name = argv[1]; params, req = TOOLS[name][1], TOOLS[name][2]
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
    elif len(req) <= len(argv) - 2 <= len(params):
        args = dict(zip(params, argv[2:]))
    else:
        wants = " ".join(p.upper() for p in req) + "".join(f" [{p.upper()}]" for p in params if p not in req)
        sys.stderr.write(f"executor: {name} wants {wants}\n")
        return 2
    said, (c, result) = call(name, args)
    print(json.dumps({"c": f"{said} → {c}", "result": result}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
