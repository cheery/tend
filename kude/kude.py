#!/usr/bin/env python3
"""kude/kude.py — Kude, day one: deterministic Horn clauses in the LPVM
paper's form, checked before they run.  card:protocol.md.

    kude.py check FILE               accept, saying what was read; or refuse, saying why
    kude.py run FILE 'name(1, 2)'    check, then run the one clause that holds

A program is clauses, `name(inputs; outputs) <- goal, goal, ... .`,
the semicolon splitting a head's arguments into inputs and outputs the
way the paper's modes do (Gange, Navas, Schachte, Søndergaard,
Stuckey, *Horn Clauses as an Intermediate Representation for Program
Analysis and Transformation*).  A goal is a comparison of two terms, a
binding `var = term`, or a call `name(terms; vars)`.  The paper's own
spelling — `←`, `∧`, `≠`, `≤`, `≥` — reads the same as the keyboard's.
`--` starts a comment.

**Exactly one clause holds.**  The paper asks that a predicate's guards
be complementary and exhaustive, so that one clause succeeds and
nothing backtracks; here that is checked and not trusted.  A guard is
a comparison whose operands are head inputs or numbers — what is known
when the clause is chosen.  The check names the atoms the guards
compare (`b` against `0`, `a` against `b`), gives each atom one of
three relations, and walks every combination: a combination under
which no clause holds is refused with the case named, and one under
which two hold is refused naming both.  This is sound and incomplete:
one relation per atom, and a relation *between* atoms (`a < b` and
`b < c` making `a < c`) is not seen, so a program exhaustive only by
such a relation is refused, and the refusal says the check did not
relate the atoms.  `test/test_kude.py` holds that case so the limit
stays written down.

**Modes are checked.**  A call's inputs are bound before it; a call's
outputs bind; a variable binds once; every head output is bound when
the body ends.  A comparison on a value the body computed is refused —
if it failed there would be no clause to fall to, and the form has no
backtracking — so a test belongs in the guards or nowhere.

**Not in day one**, and said here so it is not mistaken for built:
session types (`gcd` has one channel one way; a type nothing exercises
is not built), the paper's state thread, any builtin but `mod`, any
term but a variable or an integer.  The runner asserts what the check
proved — exactly one clause holds — and says so if it ever finds
otherwise, because a check that is wrong must be able to say so.
"""

import itertools
import re
import sys

BUILTINS = {"mod": (2, 1)}
MAX_ATOMS = 10          # 3**10 combinations; past that the check says so rather than hang
RELATIONS = {"<": {"<"}, "=": {"="}, ">": {">"},
             "!=": {"<", ">"}, "<=": {"<", "="}, ">=": {">", "="}}
FLIP = {"<": ">", ">": "<", "<=": ">=", ">=": "<=", "=": "=", "!=": "!="}
COMPARE = {"<": lambda a, b: a < b, "=": lambda a, b: a == b, ">": lambda a, b: a > b,
           "!=": lambda a, b: a != b, "<=": lambda a, b: a <= b, ">=": lambda a, b: a >= b}


class Refusal(Exception):
    """The program is not accepted; the message says why and where."""


class RunError(Exception):
    """The program was accepted and then could not run — a builtin's own refusal."""


# ── reading ───────────────────────────────────────────────────────────────

# The paper's spelling is rewritten to the keyboard's before tokenizing;
# `≤` and `≥` go through one-character stand-ins the tokenizer maps back.
TOKEN = re.compile(r"[ \t\r]+|--[^\n]*|(\n)|(<-|!=|<=|>=|[{}]|[<>=(),;.])|(-?\d+)|([A-Za-z_][A-Za-z0-9_']*)|(.)")
STANDIN = {"{": "<=", "}": ">="}


def tokens(text):
    text = text.replace("←", "<-").replace("≠", "!=").replace("≤", "{").replace("≥", "}").replace("∧", ",")
    line = 1
    for m in TOKEN.finditer(text):
        nl, op, num, name, bad = m.groups()
        if nl:
            line += 1
        elif op:
            yield ("op", STANDIN.get(op, op), line)
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
        clauses = []
        while self.peek()[0] != "end":
            clauses.append(self.clause())
        return clauses

    def clause(self):
        line = self.peek()[2]
        name = self.take("var")[1]
        self.take("op", "(")
        ins = self.names()
        self.take("op", ";")
        outs = self.names()
        self.take("op", ")")
        self.take("op", "<-")
        goals = [self.goal()]
        while self.peek()[1] == ",":
            self.take("op", ",")
            goals.append(self.goal())
        self.take("op", ".")
        return {"name": name, "ins": ins, "outs": outs, "goals": goals, "line": line}

    def names(self):
        out = []
        while self.peek()[0] == "var":
            out.append(self.take("var")[1])
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
            outs = self.names()
            self.take("op", ")")
            return {"kind": "call", "name": name, "args": args, "outs": outs, "line": line}
        left = self.term()
        op = self.take("op")[1]
        if op not in COMPARE:
            raise Refusal(f"line {line}: expected a comparison, got {op!r}")
        right = self.term()
        return {"kind": "cmp", "left": left, "op": op, "right": right, "line": line}


def parse(text):
    return Parser(text).program()


# ── the check ─────────────────────────────────────────────────────────────

def signature(c):
    return f"{c['name']}({', '.join(c['ins'])}; {', '.join(c['outs'])})"


def show(term):
    return str(term[1])


def check(clauses):
    """Refuse, or return the predicates — name → clauses, each goal
    marked `guard`, `bind` or `call` — which is what the runner runs."""
    preds = {}
    for c in clauses:
        first = preds.setdefault(c["name"], [])
        if first and (len(first[0]["ins"]), len(first[0]["outs"])) != (len(c["ins"]), len(c["outs"])):
            raise Refusal(f"line {c['line']}: {signature(c)} does not match {signature(first[0])} at line {first[0]['line']}")
        if c["name"] in BUILTINS:
            raise Refusal(f"line {c['line']}: {c['name']} is a builtin and cannot be defined")
        first.append(c)
    for name, cs in preds.items():
        for c in cs:
            modes(c, preds)
        one_holds(name, cs)
    return preds


def modes(c, preds):
    head = c["ins"] + c["outs"]
    if len(set(head)) != len(head):
        raise Refusal(f"line {c['line']}: {signature(c)} names a variable twice in its head")
    entry = set(c["ins"])          # known when the clause is chosen
    body = {}                      # var → how it was bound in this clause
    where = f"line {{}}, clause {signature(c)}"

    def known(term):
        return term[0] == "int" or term[1] in entry or term[1] in body

    def at_entry(term):
        return term[0] == "int" or term[1] in entry

    for g in c["goals"]:
        here = where.format(g["line"])
        if g["kind"] == "call":
            if g["name"] in BUILTINS:
                nin, nout = BUILTINS[g["name"]]
            elif g["name"] in preds:
                nin, nout = len(preds[g["name"]][0]["ins"]), len(preds[g["name"]][0]["outs"])
            else:
                raise Refusal(f"{here}: no predicate {g['name']}")
            if (len(g["args"]), len(g["outs"])) != (nin, nout):
                raise Refusal(f"{here}: {g['name']} takes {nin} inputs and {nout} outputs")
            for a in g["args"]:
                if not known(a):
                    raise Refusal(f"{here}: {show(a)} is not bound when {g['name']} is called")
            for o in g["outs"]:
                if o in entry or o in body:
                    raise Refusal(f"{here}: {o} is bound twice")
                body[o] = "call"
            continue
        left, op, right = g["left"], g["op"], g["right"]
        if at_entry(left) and at_entry(right):
            g["kind"] = "guard"
            continue
        if op == "=" and left[0] == "var" and not known(left):
            if not known(right):
                raise Refusal(f"{here}: {show(right)} is not bound")
            g["kind"] = "bind"
            body[left[1]] = "bind"
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


def atom(g):
    """A guard as (atom, relations): the atom is the ordered pair of terms it
    compares, the relations the subset of < = > under which it holds."""
    left, op, right = g["left"], g["op"], g["right"]
    if left[0] == "int" and right[0] == "int":
        return None, COMPARE[op](left[1], right[1])
    if left == right:
        return None, "=" in RELATIONS[op]
    if left[0] == "int" or (right[0] == "var" and left[1] > right[1]):
        left, right, op = right, left, FLIP[op]
    return (show(left), show(right)), RELATIONS[op]


def one_holds(name, cs):
    """Every combination of one relation per atom: exactly one clause."""
    sig = signature(cs[0])
    per_clause = []
    atoms = []
    for i, c in enumerate(cs, 1):
        rels = {}
        for g in c["goals"]:
            if g["kind"] != "guard":
                continue
            a, r = atom(g)
            if a is None:
                if r is True:
                    continue
                raise Refusal(f"line {c['line']}: clause {i} of {sig} can never hold: "
                              f"{show(g['left'])} {g['op']} {show(g['right'])}")
            if a not in atoms:
                atoms.append(a)
            rels[a] = rels.get(a, {"<", "=", ">"}) & r
            if not rels[a]:
                raise Refusal(f"line {c['line']}: clause {i} of {sig} can never hold: "
                              f"its guards on {a[0]} against {a[1]} leave nothing")
        per_clause.append(rels)
    if len(atoms) > MAX_ATOMS:
        raise Refusal(f"{sig} compares {len(atoms)} pairs of terms, and this check walks every "
                      f"combination — more than {MAX_ATOMS} is more than it will walk")
    limit = ("" if len(atoms) < 2 else
             "  (this check gives each pair of terms one relation and does not relate one pair "
             "to another, so a case impossible by such a relation is still a case here)")
    for combo in itertools.product("<=>", repeat=len(atoms)):
        case = ", ".join(f"{a[0]} {r} {a[1]}" for a, r in zip(atoms, combo))
        holding = [i for i, rels in enumerate(per_clause, 1)
                   if all(combo[atoms.index(a)] in r for a, r in rels.items())]
        if not holding:
            raise Refusal(f"no clause of {sig} holds when {case}{limit}")
        if len(holding) > 1:
            raise Refusal(f"clauses {holding[0]} and {holding[1]} of {sig} both hold when {case}{limit}")


# ── the run ───────────────────────────────────────────────────────────────

def value(term, env):
    return term[1] if term[0] == "int" else env[term[1]]


def builtin(name, args, trace):
    if name == "mod":
        a, b = args
        if b == 0:
            raise RunError(f"mod by zero: mod({a}, 0; _) in {trace}")
        return [a % b]
    raise RunError(f"no builtin {name}")


def call(preds, name, args):
    cs = preds[name]
    trace = f"{name}({', '.join(map(str, args))})"
    holding = []
    for c in cs:
        env = dict(zip(c["ins"], args))
        if all(COMPARE[g["op"]](value(g["left"], env), value(g["right"], env))
               for g in c["goals"] if g["kind"] == "guard"):
            holding.append((c, env))
    if len(holding) != 1:
        raise RunError(f"the check let this through: {len(holding)} clauses of {signature(cs[0])} hold for {trace}")
    c, env = holding[0]
    for g in c["goals"]:
        if g["kind"] == "bind":
            env[g["left"][1]] = value(g["right"], env)
        elif g["kind"] == "call":
            args = [value(a, env) for a in g["args"]]
            outs = builtin(g["name"], args, trace) if g["name"] in BUILTINS else call(preds, g["name"], args)
            env.update(zip(g["outs"], outs))
    return [env[o] for o in c["outs"]]


CALL = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_']*)\s*\(\s*(-?\d+(?:\s*,\s*-?\d+)*)?\s*\)\s*$")


def run(preds, text):
    m = CALL.match(text)
    if not m:
        raise Refusal(f"a call is name(number, ...): {text!r}")
    name, args = m.group(1), [int(x) for x in m.group(2).split(",")] if m.group(2) else []
    if name not in preds:
        raise Refusal(f"no predicate {name}")
    c = preds[name][0]
    if len(args) != len(c["ins"]):
        raise Refusal(f"{name} takes {len(c['ins'])} inputs, {len(args)} given")
    try:
        outs = call(preds, name, args)
    except RecursionError:
        raise RunError(f"{name}({', '.join(map(str, args))}) recursed deeper than this runner goes")
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
        preds = check(parse(text))
        if argv[0] == "check":
            said = ", ".join(f"{signature(cs[0])}: {len(cs)} clause{'s' if len(cs) != 1 else ''}"
                             for cs in preds.values())
            print(f"kude: {path} checks — {said or 'no clauses'}")
            return 0
        for name, v in run(preds, argv[2]):
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
