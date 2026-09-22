"""`kude/kude.py` — day one of card:protocol.md: the paper's `gcd` as
clauses, checked before it runs.

A Kude program is deterministic Horn clauses in the LPVM paper's form:
`name(inputs; outputs) <- goals.`, exactly one clause of a predicate
holding for any input, so that nothing backtracks.  Day one is the
checker that refuses a clause set whose guards are not complementary
and exhaustive — naming the case with no clause, or the two clauses
that both hold — and a runner that runs the one clause that holds.
Session types are not in day one: `gcd` has one channel one way.

Red first: every refusal below was run before the checker existed.
"""

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
KUDE = ROOT / "kude" / "kude.py"
GCD = ROOT / "kude" / "gcd.kude"

GCD_TEXT = GCD.read_text(encoding="utf-8")


def kude(*args):
    return subprocess.run([sys.executable, str(KUDE), *map(str, args)],
                          capture_output=True, text=True, cwd=ROOT)


def check(tmp_path, text, name="p.kude"):
    src = tmp_path / name
    src.write_text(text, encoding="utf-8")
    return kude("check", src)


def refused(tmp_path, text):
    r = check(tmp_path, text)
    assert r.returncode == 1, (r.stdout, r.stderr)
    assert r.stdout == "", "a refusal is on stderr, and stdout says nothing"
    return r.stderr


# ── the paper's gcd ───────────────────────────────────────────────────────

def test_it_parses():
    assert subprocess.run([sys.executable, "-m", "py_compile", str(KUDE)]).returncode == 0


def test_the_papers_gcd_checks():
    r = kude("check", GCD)
    assert r.returncode == 0, r.stderr
    assert "gcd" in r.stdout and "2 clauses" in r.stdout, r.stdout


def test_the_papers_gcd_runs():
    for call, want in [("gcd(48, 18)", "ret = 6"), ("gcd(18, 48)", "ret = 6"),
                       ("gcd(7, 0)", "ret = 7"), ("gcd(0, 5)", "ret = 5"),
                       ("gcd(1071, 462)", "ret = 21")]:
        r = kude("run", GCD, call)
        assert r.returncode == 0, (call, r.stderr)
        assert r.stdout.strip() == want, (call, r.stdout)


def test_the_run_reads_the_papers_own_spelling(tmp_path):
    """`←`, `∧`, `≠` are the paper's; `<-`, `,`, `!=` are the keyboard's.
    Both are one program."""
    text = ("gcd(a, b; ret) ← b ≠ 0 ∧ mod(a, b; r) ∧ gcd(b, r; ret).\n"
            "gcd(a, b; ret) ← b = 0 ∧ ret = a.\n")
    src = tmp_path / "g.kude"
    src.write_text(text, encoding="utf-8")
    r = kude("run", src, "gcd(48, 18)")
    assert r.returncode == 0 and r.stdout.strip() == "ret = 6", r.stderr


# ── the check: exactly one clause holds ───────────────────────────────────

def test_a_missing_case_is_refused_and_named(tmp_path):
    """The done line's first half: gcd with its `b = 0` clause removed is
    refused at the check, naming the case that has no clause."""
    text = "gcd(a, b; ret) <- b != 0, mod(a, b; r), gcd(b, r; ret).\n"
    err = refused(tmp_path, text)
    assert "no clause" in err and "gcd" in err and "b = 0" in err, err
    # and run refuses the same, before running anything
    src = tmp_path / "p.kude"
    r = kude("run", src, "gcd(48, 18)")
    assert r.returncode == 1 and "b = 0" in r.stderr and r.stdout == "", (r.stdout, r.stderr)


def test_two_clauses_that_both_hold_are_refused_and_named(tmp_path):
    text = ("f(x; y) <- x > 0, y = 1.\n"
            "f(x; y) <- x >= 0, y = 2.\n"
            "f(x; y) <- x < 0, y = 3.\n")
    err = refused(tmp_path, text)
    assert "clauses 1 and 2" in err and "f" in err and "x > 0" in err, err


def test_three_cases_over_one_subject_are_exhaustive(tmp_path):
    text = ("sign(x; s) <- x < 0, s = -1.\n"
            "sign(x; s) <- x = 0, s = 0.\n"
            "sign(x; s) <- x > 0, s = 1.\n")
    r = check(tmp_path, text)
    assert r.returncode == 0, r.stderr
    src = tmp_path / "p.kude"
    assert kude("run", src, "sign(-7)").stdout.strip() == "s = -1"
    assert kude("run", src, "sign(0)").stdout.strip() == "s = 0"
    assert kude("run", src, "sign(9)").stdout.strip() == "s = 1"
    # and with the middle one gone, the hole is named
    err = refused(tmp_path, "sign(x; s) <- x < 0, s = -1.\nsign(x; s) <- x > 0, s = 1.\n")
    assert "no clause" in err and "x = 0" in err, err


def test_a_guard_between_two_variables_is_a_case(tmp_path):
    text = ("max(a, b; m) <- a < b, m = b.\n"
            "max(a, b; m) <- a >= b, m = a.\n")
    r = check(tmp_path, text)
    assert r.returncode == 0, r.stderr
    src = tmp_path / "p.kude"
    assert kude("run", src, "max(3, 9)").stdout.strip() == "m = 9"
    assert kude("run", src, "max(9, 3)").stdout.strip() == "m = 9"
    assert kude("run", src, "max(4, 4)").stdout.strip() == "m = 4"


def test_a_clause_with_no_guard_is_the_only_clause_or_refused(tmp_path):
    r = check(tmp_path, "id(x; y) <- y = x.\n")
    assert r.returncode == 0, r.stderr
    err = refused(tmp_path, "f(x; y) <- y = x.\nf(x; y) <- x = 0, y = 1.\n")
    assert "clauses 1 and 2" in err and "x = 0" in err, err


def test_a_clause_that_can_never_hold_is_refused(tmp_path):
    err = refused(tmp_path, "f(x; y) <- x < 0, x > 0, y = 1.\nf(x; y) <- x = 0, y = 0.\n")
    assert "never" in err and "clause 1" in err, err


# ── the check: modes ──────────────────────────────────────────────────────

def test_an_unbound_input_is_refused(tmp_path):
    err = refused(tmp_path, "f(a; r) <- a = 0, mod(a, c; r).\nf(a; r) <- a != 0, r = a.\n")
    assert "c" in err and "not bound" in err, err


def test_an_output_never_bound_is_refused(tmp_path):
    err = refused(tmp_path, "f(a; r) <- a = 0.\nf(a; r) <- a != 0, r = a.\n")
    assert "r" in err and "never bound" in err, err


def test_a_variable_bound_twice_is_refused(tmp_path):
    err = refused(tmp_path, "f(a; r) <- r = a, r = 0.\n")
    assert "r" in err and "twice" in err, err


def test_a_call_to_nothing_is_refused(tmp_path):
    err = refused(tmp_path, "f(a; r) <- g(a; r).\n")
    assert "g" in err and "no predicate" in err, err


def test_a_test_after_a_call_cannot_choose_a_clause(tmp_path):
    """A comparison on a value the body computed is not a guard: if it
    fails there is no other clause to fall to, and the paper's form has
    no backtracking.  Refused, and the refusal says why."""
    err = refused(tmp_path, "f(a; r) <- mod(a, 2; m), m = 0, r = 1.\nf(a; r) <- mod(a, 2; m), m != 0, r = 0.\n")
    assert "after a call" in err and "m" in err, err
    # and not only `=`, which is also a second binding: the other comparisons
    # — the mutate row that survived on 2026-09-22 until this line was here
    err = refused(tmp_path, "f(a; r) <- mod(a, 2; m), m != 0, r = 0.\nf(a; r) <- mod(a, 2; m), m = 0, r = 1.\n")
    assert "after a call" in err and "m" in err, err


# ── the run ───────────────────────────────────────────────────────────────

def test_mod_by_zero_is_a_run_error_that_names_the_call(tmp_path):
    src = tmp_path / "p.kude"
    src.write_text("f(a; r) <- mod(a, 0; r).\n", encoding="utf-8")
    r = kude("run", src, "f(5)")
    assert r.returncode == 2 and "mod" in r.stderr and "zero" in r.stderr, (r.returncode, r.stderr)


def test_a_call_that_names_no_predicate_or_the_wrong_count_is_refused():
    r = kude("run", GCD, "lcm(4, 6)")
    assert r.returncode == 1 and "lcm" in r.stderr, r.stderr
    r = kude("run", GCD, "gcd(4)")
    assert r.returncode == 1 and "gcd" in r.stderr and "2 inputs" in r.stderr, r.stderr


def test_the_check_says_its_limit(tmp_path):
    """Sound and incomplete: cases are enumerated over the atoms the guards
    name, one relation per atom, and a relation between atoms (a < b and
    b < c making a < c) is not seen — so a program exhaustive only by such
    a relation is refused, and the refusal says the check did not relate
    the atoms, so the reader knows the verdict is the check's and not the
    program's."""
    text = ("f(a, b, c; r) <- a < b, b < c, r = 1.\n"
            "f(a, b, c; r) <- a >= b, r = 2.\n"
            "f(a, b, c; r) <- a < b, b >= c, r = 3.\n")
    # exhaustive as written — every (a,b) × (b,c) case is covered
    assert check(tmp_path, text).returncode == 0
    text2 = ("g(a, b, c; r) <- a < b, b < c, a < c, r = 1.\n"
             "g(a, b, c; r) <- a >= b, r = 2.\n"
             "g(a, b, c; r) <- a < b, b >= c, r = 3.\n")
    # the same program with `a < c` said out loud in clause 1: true by
    # relation, and the check cannot see that, so it refuses and says so
    err = refused(tmp_path, text2)
    assert "no clause" in err and "does not relate" in err, err
