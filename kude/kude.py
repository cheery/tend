#!/usr/bin/env python3
"""kude/kude.py — Kude: deterministic Horn clauses in the LPVM paper's form,
their channels typed by session types, checked before they run.
card:protocol.md.

    kude.py check FILE               accept, saying what was read; or refuse, saying why
    kude.py run FILE 'name(c, 2)'    check, then run the one clause that holds — a
                                     channel argument is played against stdin and stdout

A program is type definitions and clauses.  A clause is
`name(inputs; outputs) <- goal, goal, ... .`, the semicolon splitting a
head's arguments into inputs and outputs the way the paper's modes do
(Gange, Navas, Schachte, Søndergaard, Stuckey, *Horn Clauses as an
Intermediate Representation for Program Analysis and Transformation*).
A goal is a comparison of two terms, a binding `var = term`, a call
`name(terms; vars)`, or an action on a channel: `c ! term` sends,
`c ? var` receives, `c . label` chooses or, on a channel that offers the
choice, names the branch this clause is.  The paper's own spelling —
`←`, `∧`, `≠`, `≤`, `≥` — reads the same as the keyboard's.  `--` starts
a comment.

**A channel is a head input with a type**, `c: T`, and the type is the
warp: `!Int . S` sends a number and goes on as S, `?Int . S` receives
one, `+{l: S, ...}` chooses a branch, `&{l: S, ...}` offers the choice
to the other side, `end` is done, a name refers to `type Name = T.`, and
`~Name` is its dual — the same protocol from the other end, every `!` a
`?` and every `+` an `&`.  The check walks each clause's actions on a
channel through its type and refuses an action the type does not
allow, naming the state the channel is at; a channel is used to its
`end` or passed on in a call at the type the callee expects, and never
touched after.  Day two, 2026-09-22: one party against its type, run
against a partner on stdin and stdout.  Two parties joined by a cut is
day three.

**Exactly one clause holds.**  The paper asks that a predicate's guards
be complementary and exhaustive, so that one clause succeeds and
nothing backtracks; here that is checked and not trusted.  A guard is
a comparison whose operands are head inputs or numbers, or the branch
a clause names on a channel that offers the choice — what is known
when the clause is chosen, which is why a branch comes before any
action.  The check names the atoms the guards decide (`b` against `0`,
`a` against `b`, the branch on `c`), gives each atom one of its
relations, and walks every combination: a combination under which no
clause holds is refused with the case named, and one under which two
hold is refused naming both.  This is sound and incomplete: one
relation per atom, and a relation *between* atoms (`a < b` and `b < c`
making `a < c`) is not seen, so a program exhaustive only by such a
relation is refused, and the refusal says the check did not relate the
atoms.  `test/test_kude.py` holds that case so the limit stays written
down.

**Modes are checked.**  A call's inputs are bound before it; a call's
outputs bind; a variable binds once; every head output is bound when
the body ends.  A comparison on a value the body computed is refused —
if it failed there would be no clause to fall to, and the form has no
backtracking — so a test belongs in the guards or nowhere.

**Not built**, and said here so it is not mistaken for built: the cut
(two parties in one run), a message type but `Int`, sending a channel
over a channel, the replicable service `!A`, polymorphism, the paper's
state thread, any builtin but `mod`, `add`, `sub`, any term but a
variable or an integer.  The runner asserts what the check proved —
exactly one clause holds — and says so if it ever finds otherwise,
because a check that is wrong must be able to say so.
"""

import itertools
import re
import sys

BUILTINS = {"mod": (2, 1), "add": (2, 1), "sub": (2, 1)}
MAX_CASES = 3 ** 10     # past this the check says so rather than hang
RELATIONS = {"<": {"<"}, "=": {"="}, ">": {">"},
             "!=": {"<", ">"}, "<=": {"<", "="}, ">=": {">", "="}}
FLIP = {"<": ">", ">": "<", "<=": ">=", ">=": "<=", "=": "=", "!=": "!="}
COMPARE = {"<": lambda a, b: a < b, "=": lambda a, b: a == b, ">": lambda a, b: a > b,
           "!=": lambda a, b: a != b, "<=": lambda a, b: a <= b, ">=": lambda a, b: a >= b}


class Refusal(Exception):
    """The program is not accepted; the message says why and where."""


class RunError(Exception):
    """The program was accepted and then could not run — a builtin's or the partner's doing."""


# ── reading ───────────────────────────────────────────────────────────────

SPELLING = [("←", "<-"), ("∧", ","), ("≠", "!="), ("≤", "<="), ("≥", ">=")]
TOKEN = re.compile(r"[ \t\r]+|--[^\n]*|(\n)|(<-|!=|<=|>=|[<>=(),;.!?+&{}:~])|(-?\d+)|([A-Za-z_][A-Za-z0-9_']*)|(.)")


def tokens(text):
    for theirs, ours in SPELLING:
        text = text.replace(theirs, ours)
    line = 1
    for m in TOKEN.finditer(text):
        nl, op, num, name, bad = m.groups()
        if nl:
            line += 1
        elif op:
            yield ("op", op, line)
        elif num:
            yield ("int", int(num), line)
        elif name:
            yield ("var", name, line)
        elif bad:
            raise Refusal(f"line {line}: unexpected character {bad!r}")
    yield ("end", None, line)


class Parser:
    def __init__(self, text):
        self.toks = list(tokens(text))
        self.i = 0

    def peek(self, k=0):
        return self.toks[min(self.i + k, len(self.toks) - 1)]

    def take(self, kind=None, value=None):
        t = self.peek()
        if (kind and t[0] != kind) or (value is not None and t[1] != value):
            want = repr(value) if value is not None else kind
            got = "end of file" if t[0] == "end" else repr(str(t[1]))
            raise Refusal(f"line {t[2]}: expected {want}, got {got}")
        self.i += 1
        return t

    def program(self):
        types, clauses = {}, []
        while self.peek()[0] != "end":
            if self.peek()[1] == "type" and self.peek(1)[0] == "var":
                line = self.take("var")[2]
                name = self.take("var")[1]
                self.take("op", "=")
                t = self.type_expr()
                self.take("op", ".")
                if name in types:
                    raise Refusal(f"line {line}: type {name} is defined twice")
                types[name] = t
            else:
                clauses.append(self.clause())
        return types, clauses

    def type_expr(self):
        t = self.peek()
        if t[1] in ("!", "?"):
            self.i += 1
            if self.take("var")[1] != "Int":
                raise Refusal(f"line {t[2]}: a message is an Int — nothing else is sent yet")
            self.take("op", ".")
            return ("send" if t[1] == "!" else "recv", self.type_expr())
        if t[1] in ("+", "&"):
            self.i += 1
            self.take("op", "{")
            branches = []
            while True:
                label = self.take("var")[1]
                self.take("op", ":")
                branches.append((label, self.type_expr()))
                if self.peek()[1] != ",":
                    break
                self.take("op", ",")
            self.take("op", "}")
            if len({l for l, _ in branches}) != len(branches):
                raise Refusal(f"line {t[2]}: a branch is named twice")
            return ("choose" if t[1] == "+" else "offer", branches)
        if t[1] == "~":
            self.i += 1
            return ("dual", self.take("var")[1])
        if t[0] == "var":
            self.i += 1
            return ("end",) if t[1] == "end" else ("name", t[1])
        raise Refusal(f"line {t[2]}: expected a type, got {t[1]!r}")

    def clause(self):
        line = self.peek()[2]
        name = self.take("var")[1]
        self.take("op", "(")
        ins = self.params(typed=True)
        self.take("op", ";")
        outs = [n for n, _ in self.params(typed=False)]
        self.take("op", ")")
        self.take("op", "<-")
        goals = [self.goal()]
        while self.peek()[1] == ",":
            self.take("op", ",")
            goals.append(self.goal())
        self.take("op", ".")
        return {"name": name, "ins": ins, "outs": outs, "goals": goals, "line": line}

    def params(self, typed):
        out = []
        while self.peek()[0] == "var":
            name = self.take("var")[1]
            t = None
            if self.peek()[1] == ":":
                if not typed:
                    raise Refusal(f"line {self.peek()[2]}: an output has no type — a channel is made by nothing yet")
                self.take("op", ":")
                t = self.type_expr()
            out.append((name, t))
            if self.peek()[1] != ",":
                break
            self.take("op", ",")
        return out

    def term(self):
        t = self.peek()
        if t[0] in ("int", "var"):
            self.i += 1
            return (t[0], t[1])
        raise Refusal(f"line {t[2]}: expected a variable or a number, got {t[1]!r}")

    def goal(self):
        line = self.peek()[2]
        if self.peek()[0] == "var" and self.peek(1)[1] == "(":
            name = self.take("var")[1]
            self.take("op", "(")
            args = []
            while self.peek()[1] != ";":
                args.append(self.term())
                if self.peek()[1] != ",":
                    break
                self.take("op", ",")
            self.take("op", ";")
            outs = [n for n, _ in self.params(typed=False)]
            self.take("op", ")")
            return {"kind": "call", "name": name, "args": args, "outs": outs, "line": line}
        if self.peek()[0] == "var" and self.peek(1)[1] in ("!", "?", "."):
            chan = self.take("var")[1]
            op = self.take("op")[1]
            if op == "!":
                return {"kind": "send", "chan": chan, "term": self.term(), "line": line}
            if op == "?":
                return {"kind": "recv", "chan": chan, "var": self.take("var")[1], "line": line}
            return {"kind": "label", "chan": chan, "label": self.take("var")[1], "line": line}
        left = self.term()
        op = self.take("op")[1]
        if op not in COMPARE:
            raise Refusal(f"line {line}: expected a comparison, got {op!r}")
        right = self.term()
        return {"kind": "cmp", "left": left, "op": op, "right": right, "line": line}


def parse(text):
    return Parser(text).program()


# ── types ─────────────────────────────────────────────────────────────────

def tshow(t):
    k = t[0]
    if k == "end":
        return "end"
    if k in ("send", "recv"):
        return ("!Int . " if k == "send" else "?Int . ") + tshow(t[1])
    if k in ("choose", "offer"):
        return ("+" if k == "choose" else "&") + "{" + ", ".join(f"{l}: {tshow(s)}" for l, s in t[1]) + "}"
    return t[1] if k == "name" else "~" + t[1]


def dual(t):
    k = t[0]
    if k == "end":
        return t
    if k in ("send", "recv"):
        return ("recv" if k == "send" else "send", dual(t[1]))
    if k in ("choose", "offer"):
        return ("offer" if k == "choose" else "choose", [(l, dual(s)) for l, s in t[1]])
    return ("dual", t[1]) if k == "name" else ("name", t[1])


def unfold(t, types):
    """One step: a name or a dual becomes the type it stands for."""
    while t[0] in ("name", "dual"):
        if t[1] not in types:
            raise Refusal(f"no type {t[1]}")
        t = types[t[1]] if t[0] == "name" else dual(types[t[1]])
    return t


def same(a, b, types, seen=()):
    if a == b or (a, b) in seen:
        return True
    ua, ub = unfold(a, types), unfold(b, types)
    if ua[0] != ub[0]:
        return False
    seen = seen + ((a, b),)
    if ua[0] in ("send", "recv"):
        return same(ua[1], ub[1], types, seen)
    if ua[0] in ("choose", "offer"):
        return [l for l, _ in ua[1]] == [l for l, _ in ub[1]] and \
            all(same(s, r, types, seen) for (_, s), (_, r) in zip(ua[1], ub[1]))
    return True


def names_exist(t, types, where):
    stack = [t]
    while stack:
        t = stack.pop()
        if t[0] in ("name", "dual"):
            if t[1] not in types:
                raise Refusal(f"{where}: no type {t[1]}")
        elif t[0] in ("send", "recv"):
            stack.append(t[1])
        elif t[0] in ("choose", "offer"):
            stack.extend(s for _, s in t[1])


# ── the check ─────────────────────────────────────────────────────────────

def signature(c):
    ins = ", ".join(n if t is None else f"{n}: {tshow(t)}" for n, t in c["ins"])
    return f"{c['name']}({ins}; {', '.join(c['outs'])})"


def show(term):
    return str(term[1])


def check(program):
    """Refuse, or return (types, predicates) — name → clauses, each goal
    marked by what it is — which is what the runner runs."""
    types, clauses = program
    for name, t in types.items():
        names_exist(t, types, f"type {name}")
    preds = {}
    for c in clauses:
        for n, t in c["ins"]:
            if t is not None:
                names_exist(t, types, f"line {c['line']}, {signature(c)}")
        first = preds.setdefault(c["name"], [])
        if first and signature(first[0]) != signature(c):
            raise Refusal(f"line {c['line']}: {signature(c)} does not match {signature(first[0])} at line {first[0]['line']}")
        if c["name"] in BUILTINS:
            raise Refusal(f"line {c['line']}: {c['name']} is a builtin and cannot be defined")
        first.append(c)
    for name, cs in preds.items():
        for c in cs:
            modes(c, preds, types)
        one_holds(name, cs)
    return types, preds


def modes(c, preds, types):
    head = [n for n, _ in c["ins"]] + c["outs"]
    if len(set(head)) != len(head):
        raise Refusal(f"line {c['line']}: {signature(c)} names a variable twice in its head")
    entry = {n for n, t in c["ins"] if t is None}     # numbers known when the clause is chosen
    chans = {n: t for n, t in c["ins"] if t is not None}
    passed = {}                    # channel → the call it went to
    body = {}                      # var → how it was bound in this clause
    acted = False                  # a non-guard goal has been seen
    where = f"line {{}}, clause {signature(c)}"

    def known(term):
        return term[0] == "int" or term[1] in entry or term[1] in body

    def at_entry(term):
        return term[0] == "int" or term[1] in entry

    def channel(g, here):
        ch = g["chan"]
        if ch in passed:
            raise Refusal(f"{here}: {ch} was passed to {passed[ch]} and is not used after")
        if ch not in chans:
            raise Refusal(f"{here}: {ch} is not a channel")
        return ch, unfold(chans[ch], types)

    for g in c["goals"]:
        here = where.format(g["line"])
        if g["kind"] == "call":
            if g["name"] in BUILTINS:
                nin, nout = BUILTINS[g["name"]]
                params = [(None, None)] * nin
            elif g["name"] in preds:
                callee = preds[g["name"]][0]
                nin, nout = len(callee["ins"]), len(callee["outs"])
                params = callee["ins"]
            else:
                raise Refusal(f"{here}: no predicate {g['name']}")
            if (len(g["args"]), len(g["outs"])) != (nin, nout):
                raise Refusal(f"{here}: {g['name']} takes {nin} inputs and {nout} outputs")
            for a, (pname, ptype) in zip(g["args"], params):
                if a[0] == "var" and a[1] in chans:
                    if ptype is None:
                        raise Refusal(f"{here}: {g['name']} takes a number where {a[1]} is a channel")
                    if a[1] in passed:
                        raise Refusal(f"{here}: {a[1]} was passed to {passed[a[1]]} and is not used after")
                    if not same(chans[a[1]], ptype, types):
                        raise Refusal(f"{here}: {g['name']} takes {pname} at {tshow(ptype)}, and {a[1]} is at {tshow(chans[a[1]])}")
                    passed[a[1]] = g["name"]
                elif a[0] == "var" and a[1] in passed:
                    raise Refusal(f"{here}: {a[1]} was passed to {passed[a[1]]} and is not used after")
                elif ptype is not None:
                    raise Refusal(f"{here}: {g['name']} takes {pname} as a channel at {tshow(ptype)}, and {show(a)} is a number")
                elif not known(a):
                    raise Refusal(f"{here}: {show(a)} is not bound when {g['name']} is called")
            for o in g["outs"]:
                if o in entry or o in body or o in chans:
                    raise Refusal(f"{here}: {o} is bound twice")
                body[o] = "call"
            acted = True
            continue
        if g["kind"] == "send":
            ch, cur = channel(g, here)
            if cur[0] != "send":
                raise Refusal(f"{here}: `{ch} ! {show(g['term'])}` — {ch} is at {tshow(chans[ch])}, which does not send")
            if not known(g["term"]):
                raise Refusal(f"{here}: {show(g['term'])} is not bound")
            chans[ch] = cur[1]
            acted = True
            continue
        if g["kind"] == "recv":
            ch, cur = channel(g, here)
            if cur[0] != "recv":
                raise Refusal(f"{here}: `{ch} ? {g['var']}` — {ch} is at {tshow(chans[ch])}, which does not receive")
            if g["var"] in entry or g["var"] in body or g["var"] in chans:
                raise Refusal(f"{here}: {g['var']} is bound twice")
            body[g["var"]] = "recv"
            chans[ch] = cur[1]
            acted = True
            continue
        if g["kind"] == "label":
            ch, cur = channel(g, here)
            if cur[0] not in ("choose", "offer"):
                raise Refusal(f"{here}: `{ch} . {g['label']}` — {ch} is at {tshow(chans[ch])}, which has no branches")
            branches = dict(cur[1])
            if g["label"] not in branches:
                raise Refusal(f"{here}: {g['label']} is not a branch of {ch}'s {tshow(cur)}")
            if cur[0] == "offer":
                if acted:
                    raise Refusal(f"{here}: the branch on {ch} is chosen at entry — `{ch} . {g['label']}` comes before any action")
                g["kind"] = "branch"
                g["labels"] = tuple(l for l, _ in cur[1])
            else:
                g["kind"] = "choose"
                acted = True
            chans[ch] = branches[g["label"]]
            continue
        left, op, right = g["left"], g["op"], g["right"]
        for t in (left, right):
            if t[0] == "var" and (t[1] in chans or t[1] in passed):
                raise Refusal(f"{here}: {t[1]} is a channel, not a number to compare")
        if at_entry(left) and at_entry(right):
            g["kind"] = "guard"
            continue
        if op == "=" and left[0] == "var" and not known(left):
            if not known(right):
                raise Refusal(f"{here}: {show(right)} is not bound")
            g["kind"] = "bind"
            body[left[1]] = "bind"
            acted = True
            continue
        computed = [show(t) for t in (left, right) if t[0] == "var" and t[1] in body]
        if op == "=" and left[0] == "var" and left[1] in body:
            raise Refusal(f"{here}: {left[1]} is already bound in this clause — a variable is bound once, never twice, "
                          f"and a test after a call cannot choose a clause: there is no clause to fall to")
        if computed:
            raise Refusal(f"{here}: a test after a call cannot choose a clause — {', '.join(computed)} was computed "
                          f"in this clause, and if the test failed there would be no clause to fall to")
        unbound = [show(t) for t in (left, right) if not known(t)]
        raise Refusal(f"{here}: {', '.join(unbound)} is not bound")
    for o in c["outs"]:
        if o not in body:
            raise Refusal(f"{where.format(c['line'])}: output {o} is never bound")
    for ch, t in chans.items():
        if ch not in passed and unfold(t, types)[0] != "end":
            raise Refusal(f"{where.format(c['line'])}: {ch} is at {tshow(t)} when the clause ends — "
                          f"a channel is used to its end, or passed on")


def atom(g):
    """A comparison guard as (atom, relations): the atom is the ordered pair
    of terms it compares, the relations the subset of < = > under which it
    holds; (None, bool) when it is constant."""
    left, op, right = g["left"], g["op"], g["right"]
    if left[0] == "int" and right[0] == "int":
        return None, COMPARE[op](left[1], right[1])
    if left == right:
        return None, "=" in RELATIONS[op]
    if left[0] == "int" or (right[0] == "var" and left[1] > right[1]):
        left, right, op = right, left, FLIP[op]
    return (show(left), show(right)), RELATIONS[op]


def case_text(a, r):
    return f"{a[1]} . {r}" if a[0] == "\0branch" else f"{a[0]} {r} {a[1]}"


def one_holds(name, cs):
    """Every combination of one relation per atom: exactly one clause."""
    sig = signature(cs[0])
    per_clause = []
    atoms, universes = [], []
    for i, c in enumerate(cs, 1):
        rels = {}
        for g in c["goals"]:
            if g["kind"] == "guard":
                a, r = atom(g)
                universe = ("<", "=", ">")
                if a is None:
                    if r is True:
                        continue
                    raise Refusal(f"line {c['line']}: clause {i} of {sig} can never hold: "
                                  f"{show(g['left'])} {g['op']} {show(g['right'])}")
            elif g["kind"] == "branch":
                a, r, universe = ("\0branch", g["chan"]), {g["label"]}, g["labels"]
            else:
                continue
            if a not in atoms:
                atoms.append(a)
                universes.append(universe)
            rels[a] = rels.get(a, set(universe)) & r
            if not rels[a]:
                raise Refusal(f"line {c['line']}: clause {i} of {sig} can never hold: "
                              f"its guards on {case_text(a, '…')} leave nothing")
        per_clause.append(rels)
    n = 1
    for u in universes:
        n *= len(u)
    if n > MAX_CASES:
        raise Refusal(f"{sig} has {n} cases, and this check walks every one — more than {MAX_CASES} is more than it will walk")
    limit = ("" if len(atoms) < 2 else
             "  (this check gives each pair of terms one relation and does not relate one pair "
             "to another, so a case impossible by such a relation is still a case here)")
    for combo in itertools.product(*universes):
        case = ", ".join(case_text(a, r) for a, r in zip(atoms, combo))
        holding = [i for i, rels in enumerate(per_clause, 1)
                   if all(combo[atoms.index(a)] in r for a, r in rels.items())]
        if not holding:
            raise Refusal(f"no clause of {sig} holds when {case}{limit}")
        if len(holding) > 1:
            raise Refusal(f"clauses {holding[0]} and {holding[1]} of {sig} both hold when {case}{limit}")


# ── the run ───────────────────────────────────────────────────────────────

class Stdio:
    """The partner at the other end of every channel in a run: what this
    party sends and chooses goes to stdout, one line each; what it receives
    and the branches chosen for it are read from stdin, one line each."""

    def send(self, ch, v, trace):
        print(f"{ch} ! {v}", flush=True)

    def choose(self, ch, label, trace):
        print(f"{ch} . {label}", flush=True)

    def recv(self, ch, var, trace):
        line = sys.stdin.readline()
        if not line:
            raise RunError(f"the partner closed on `{ch} ? {var}` in {trace}")
        try:
            return int(line.strip())
        except ValueError:
            raise RunError(f"the partner sent {line.strip()!r} on {ch} where a number was due, in {trace}")

    def offer(self, ch, trace):
        line = sys.stdin.readline()
        if not line:
            raise RunError(f"the partner closed while {trace} waited for its choice on {ch}")
        return line.strip()


def value(term, env):
    return term[1] if term[0] == "int" else env[term[1]]


def builtin(name, args, trace):
    a, b = args
    if name == "mod":
        if b == 0:
            raise RunError(f"mod by zero: mod({a}, 0; _) in {trace}")
        return [a % b]
    if name == "add":
        return [a + b]
    if name == "sub":
        return [a - b]
    raise RunError(f"no builtin {name}")


def call(preds, name, args, partner):
    cs = preds[name]
    trace = f"{name}({', '.join(n if isinstance(v, str) else str(v) for (n, _), v in zip(cs[0]['ins'], args))})"
    chosen = {}
    for c in cs:
        for g in c["goals"]:
            if g["kind"] == "branch" and g["chan"] not in chosen:
                chosen[g["chan"]] = partner.offer(g["chan"], trace)
    holding = []
    for c in cs:
        env = dict(zip((n for n, _ in c["ins"]), args))
        ok = True
        for g in c["goals"]:
            if g["kind"] == "guard":
                ok = COMPARE[g["op"]](value(g["left"], env), value(g["right"], env))
            elif g["kind"] == "branch":
                ok = chosen[g["chan"]] == g["label"]
            if not ok:
                break
        if ok:
            holding.append((c, env))
    if len(holding) != 1:
        raise RunError(f"the check let this through: {len(holding)} clauses of {signature(cs[0])} hold for {trace}")
    c, env = holding[0]
    for g in c["goals"]:
        k = g["kind"]
        if k == "bind":
            env[g["left"][1]] = value(g["right"], env)
        elif k == "call":
            a = [value(t, env) for t in g["args"]]
            outs = builtin(g["name"], a, trace) if g["name"] in BUILTINS else call(preds, g["name"], a, partner)
            env.update(zip(g["outs"], outs))
        elif k == "send":
            partner.send(g["chan"], value(g["term"], env), trace)
        elif k == "recv":
            env[g["var"]] = partner.recv(g["chan"], g["var"], trace)
        elif k == "choose":
            partner.choose(g["chan"], g["label"], trace)
    return [env[o] for o in c["outs"]]


CALL = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_']*)\s*\(\s*((?:-?\d+|[A-Za-z_][A-Za-z0-9_']*)(?:\s*,\s*(?:-?\d+|[A-Za-z_][A-Za-z0-9_']*))*)?\s*\)\s*$")


def run(types, preds, text):
    m = CALL.match(text)
    if not m:
        raise Refusal(f"a call is name(number or channel, ...): {text!r}")
    name = m.group(1)
    given = [x.strip() for x in m.group(2).split(",")] if m.group(2) else []
    if name not in preds:
        raise Refusal(f"no predicate {name}")
    c = preds[name][0]
    if len(given) != len(c["ins"]):
        raise Refusal(f"{name} takes {len(c['ins'])} inputs, {len(given)} given")
    args, channels = [], []
    for g, (pname, ptype) in zip(given, c["ins"]):
        if ptype is None:
            if not re.fullmatch(r"-?\d+", g):
                raise Refusal(f"{pname} is a number, and {g} is not one")
            args.append(int(g))
        else:
            if re.fullmatch(r"-?\d+", g):
                raise Refusal(f"{pname} is a channel at {tshow(ptype)}, and {g} is not a name for one")
            args.append(g)
            channels.append(g)
    if len(channels) > 1:
        raise Refusal(f"one channel per run for now — {name} has {len(channels)}; the cut is day three")
    try:
        outs = call(preds, name, args, Stdio())
    except RecursionError:
        raise RunError(f"{name}({', '.join(given)}) recursed deeper than this runner goes")
    return list(zip(c["outs"], outs))


# ── the command ───────────────────────────────────────────────────────────

def main(argv):
    if len(argv) < 2 or argv[0] not in ("check", "run") or (argv[0] == "run") != (len(argv) == 3):
        print(__doc__.split("\n\n")[1], file=sys.stderr)
        return 1
    path = argv[1]
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        print(f"kude: {e}", file=sys.stderr)
        return 1
    try:
        types, preds = check(parse(text))
        if argv[0] == "check":
            said = ", ".join(f"{signature(cs[0])}: {len(cs)} clause{'s' if len(cs) != 1 else ''}"
                             for cs in preds.values())
            print(f"kude: {path} checks — {said or 'no clauses'}")
            return 0
        for name, v in run(types, preds, argv[2]):
            print(f"{name} = {v}")
        return 0
    except Refusal as e:
        print(f"kude: {path}: {e}", file=sys.stderr)
        return 1
    except RunError as e:
        print(f"kude: {path}: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
