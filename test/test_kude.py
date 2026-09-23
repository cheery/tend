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


BANK = ROOT / "kude" / "bank.kude"


def kude(*args, stdin=""):
    return subprocess.run([sys.executable, str(KUDE), *map(str, args)],
                          input=stdin, capture_output=True, text=True, cwd=ROOT)


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


# ── day two: one party against its type, run against a scripted partner ──
#
# A head argument `c: T` is a channel at session type T; `~T` is the dual.
# The checker walks each clause's actions on the channel through the type
# and refuses one the type does not allow, naming the state the channel is
# at; a branch offered (`&`) is a clause each, and the exhaustiveness check
# walks labels the way it walks comparisons.  The runner plays one party
# against stdin and stdout: what it sends and chooses goes out one line
# each, what it receives and the branches chosen for it come in.  Two
# parties joined by a cut is day three.

BANK_TYPE = BANK.read_text(encoding="utf-8").split("-- The client")[0]
BANK_CLAUSES = "".join(l for l in BANK.read_text(encoding="utf-8").splitlines(keepends=True) if l.startswith("bank("))


def test_the_bank_and_its_client_check():
    r = kude("check", BANK)
    assert r.returncode == 0, r.stderr
    assert "client(c: ~Bank; got): 1 clause" in r.stdout and "bank(c: Bank, bal; ): 3 clauses" in r.stdout, r.stdout


def test_the_client_runs_against_a_scripted_bank():
    r = kude("run", BANK, "client(c)", stdin="120\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout.splitlines() == ["c . deposit", "c ! 50", "c . withdraw", "c ! 30", "c . quit", "got = 120"], r.stdout


def test_the_bank_runs_against_a_scripted_client():
    r = kude("run", BANK, "bank(c, 100)", stdin="deposit\n50\nwithdraw\n30\nquit\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout.splitlines() == ["c ! 120"], r.stdout


def test_a_partner_that_closes_early_is_a_run_error():
    r = kude("run", BANK, "client(c)", stdin="")
    assert r.returncode == 2 and "closed" in r.stderr and "c ? got" in r.stderr, (r.returncode, r.stderr)
    r = kude("run", BANK, "bank(c, 100)", stdin="deposit\n")
    assert r.returncode == 2 and "closed" in r.stderr, (r.returncode, r.stderr)


def test_a_send_where_the_type_receives_is_refused_naming_the_state(tmp_path):
    err = refused(tmp_path, BANK_TYPE + "client(c: ~Bank; got) <- c.deposit, c?got, c.quit.\n")
    assert "c ? got" in err and "!Int . ~Bank" in err, err


def test_a_channel_left_unfinished_is_refused_naming_the_state(tmp_path):
    err = refused(tmp_path, BANK_TYPE + "client(c: ~Bank; got) <- c.deposit, c!50, got = 0.\n")
    assert "c is at ~Bank" in err and "ends" in err, err


def test_a_branch_not_offered_is_refused_naming_the_label(tmp_path):
    two = ("bank(c: Bank, bal; ) <- c.deposit, c?n, add(bal, n; bal'), bank(c, bal'; ).\n"
           "bank(c: Bank, bal; ) <- c.withdraw, c?n, sub(bal, n; bal'), c!bal', bank(c, bal'; ).\n")
    err = refused(tmp_path, BANK_TYPE + two)
    assert "no clause of bank(c: Bank, bal; )" in err and "c . quit" in err, err


def test_a_label_the_type_does_not_have_is_refused(tmp_path):
    err = refused(tmp_path, BANK_TYPE + "client(c: ~Bank; got) <- c.steal, c?got, c.quit.\n")
    assert "steal" in err and "deposit" in err and "quit" in err, err


def test_a_channel_used_after_it_was_passed_on_is_refused(tmp_path):
    # a bank with one clause is refused for its missing branches first — the
    # first run of this test, 2026-09-22, was the checker being right about
    # the fixture — so the whole bank stands under the clause on trial
    text = BANK_TYPE + BANK_CLAUSES + "f(c: Bank, bal; ) <- c.deposit, c?n, bank(c, n; ), c.quit.\n"
    err = refused(tmp_path, text)
    assert "c was passed to bank" in err, err


def test_a_call_with_the_channel_at_another_type_is_refused(tmp_path):
    text = BANK_TYPE + BANK_CLAUSES + "f(c: Bank, bal; ) <- c.deposit, bank(c, bal; ).\n"
    err = refused(tmp_path, text)
    assert "bank takes c at Bank" in err and "?Int . Bank" in err, err


def test_a_branch_is_chosen_at_entry_so_it_comes_first(tmp_path):
    text = BANK_TYPE + ("bank(c: Bank, bal; ) <- add(bal, 1; b), c.deposit, c?n, bank(c, n; ).\n"
                        "bank(c: Bank, bal; ) <- c.withdraw, c?n, c!bal, bank(c, bal; ).\n"
                        "bank(c: Bank, bal; ) <- c.quit.\n")
    err = refused(tmp_path, text)
    assert "at entry" in err and "c . deposit" in err, err


def test_a_type_that_names_nothing_is_refused(tmp_path):
    err = refused(tmp_path, "f(c: Teller; ) <- c.quit.\n")
    assert "Teller" in err and "no type" in err, err


def test_a_run_needs_a_name_for_a_channel_and_a_number_for_a_number():
    r = kude("run", BANK, "client(5)")
    assert r.returncode == 1 and "c" in r.stderr and "channel" in r.stderr, r.stderr
    r = kude("run", BANK, "bank(c, d)")
    assert r.returncode == 1 and "bal" in r.stderr and "number" in r.stderr, r.stderr


# ── day three: the cut — two parties in one run ──────────────────────────
#
# `new c: T (p(c, ...) | q(c, ...))` makes a channel, gives the end at T to
# p and the end at ~T to q, and runs both until both are done.  The check
# is the cut's: each side takes c at its end's type, so the two ends are
# dual; c is used by both sides and by nothing else; and a channel the
# clause already holds goes to one side at most.  The parties of a run
# then form a tree with one channel per edge, and a tree of parties each
# following its type has no cycle of waiting — the transcript's "deadlock
# freedom from the cut".  The run is coroutines and a queue each way, one
# thread and no lock; if every party ever waits, the run says the check let
# a deadlock through, because a check that is wrong must be able to say so.

NUM = ("type Num = !Int . end.\n"
       "fwd(d: ~Num, c: Num; ) <- d ? x, c ! x.\n"
       "sink(c: ~Num; y) <- c ? y.\n")


def test_the_bank_and_its_client_run_together():
    r = kude("check", BANK)
    assert r.returncode == 0 and "main(; got): 1 clause" in r.stdout, (r.stdout, r.stderr)
    r = kude("run", BANK, "main()")
    assert r.returncode == 0, r.stderr
    assert r.stdout.splitlines() == ["got = 120"], r.stdout


def test_either_end_of_the_cut_can_be_named(tmp_path):
    src = tmp_path / "b.kude"
    src.write_text(BANK.read_text(encoding="utf-8") +
                   "other(; got) <- new c: ~Bank (client(c; got) | bank(c, 100; )).\n", encoding="utf-8")
    r = kude("run", src, "other()")
    assert r.returncode == 0 and r.stdout.splitlines() == ["got = 120"], (r.stdout, r.stderr)


def test_a_party_that_waits_is_resumed_when_its_partner_sends(tmp_path):
    # sink is run first and waits on c; fwd reads stdin and sends; sink
    # takes it on the next round — and the stdin channel lives beside the cut
    src = tmp_path / "n.kude"
    src.write_text(NUM + "main(d: ~Num; y) <- new c: ~Num (sink(c; y) | fwd(d, c; )).\n", encoding="utf-8")
    r = kude("run", src, "main(d)", stdin="7\n")
    assert r.returncode == 0 and r.stdout.splitlines() == ["y = 7"], (r.stdout, r.stderr)


def test_a_cut_whose_ends_are_not_dual_is_refused_naming_the_types(tmp_path):
    err = refused(tmp_path, BANK_TYPE + BANK_CLAUSES +
                  "main(; ) <- new c: Bank (bank(c, 100; ) | bank(c, 0; )).\n")
    assert "bank takes c at Bank" in err and "c is at ~Bank" in err and "main" in err, err


def test_a_cut_channel_one_side_leaves_unused_is_refused(tmp_path):
    err = refused(tmp_path, BANK_TYPE + BANK_CLAUSES + "id(a; b) <- b = a.\n"
                  "main(; x) <- new c: Bank (bank(c, 100; ) | id(5; x)).\n")
    assert "c" in err and "id" in err and "each side" in err, err


def test_a_channel_given_to_both_sides_of_a_cut_is_refused(tmp_path):
    # the tree: one channel per edge, so d cannot join both sides as well
    text = ("type P = !Int . end.\n"
            "give(a: P, b: P; ) <- a ! 1, b ! 2.\n"
            "take(a: ~P, b: P; x) <- a ? x, b ! 3.\n"
            "f(d: P; x) <- new c: P (give(c, d; ) | take(c, d; x)).\n")
    err = refused(tmp_path, text)
    assert "d was passed to give" in err, err


def test_the_cut_channel_is_not_used_after_the_cut(tmp_path):
    err = refused(tmp_path, BANK.read_text(encoding="utf-8") +
                  "late(; got) <- new c: Bank (bank(c, 100; ) | client(c; got)), c.quit.\n")
    assert "c was passed to" in err, err


def test_a_cut_names_a_channel_that_is_new(tmp_path):
    err = refused(tmp_path, BANK.read_text(encoding="utf-8") +
                  "twice(c; got) <- new c: Bank (bank(c, 100; ) | client(c; got)).\n")
    assert "c is bound twice" in err, err


def test_a_cut_at_a_type_that_names_nothing_is_refused(tmp_path):
    err = refused(tmp_path, BANK.read_text(encoding="utf-8") +
                  "t(; got) <- new c: Teller (bank(c, 100; ) | client(c; got)).\n")
    assert "Teller" in err and "no type" in err, err


def unchecked(tmp_path, text):
    """Run main() with the check made wrong, in-process: every two types
    are `same`, so a cut whose ends are not dual is let through, and the
    run must be the one to say so rather than hang or answer."""
    src = tmp_path / "d.kude"
    src.write_text(text, encoding="utf-8")
    script = ("import sys; sys.path.insert(0, sys.argv[1]); import kude\n"
              "kude.same = lambda *a, **k: True\n"
              "sys.exit(kude.main(['run', sys.argv[2], 'main()']))\n")
    return subprocess.run([sys.executable, "-c", script, str(KUDE.parent), str(src)],
                          capture_output=True, text=True, timeout=30)


def test_the_run_says_so_if_the_check_ever_lets_a_deadlock_through(tmp_path):
    # two banks on one channel: each waits for the other to choose
    text = BANK_TYPE + BANK_CLAUSES + "main(; ) <- new c: Bank (bank(c, 100; ) | bank(c, 0; )).\n"
    assert "bank takes c at Bank" in refused(tmp_path, text)
    r = unchecked(tmp_path, text)
    assert r.returncode == 2, (r.returncode, r.stdout, r.stderr)
    assert "the check let this through" in r.stderr and "every party waits" in r.stderr, r.stderr
    assert r.stderr.count("waited for its choice on c") == 2, r.stderr


def test_the_run_says_so_if_the_check_ever_lets_a_wrong_message_through(tmp_path):
    # two clients on one channel do not deadlock — a queue each way, and each
    # takes the other's choices where it waits for a number.  The first run
    # of the deadlock test, 2026-09-23, used this pair and it answered
    # `a = deposit`: the fixture's claim was wrong, and the run said nothing
    text = (BANK_TYPE + "client(c: ~Bank; got) <- c.deposit, c!50, c.withdraw, c!30, c?got, c.quit.\n"
            "main(; a, b) <- new c: ~Bank (client(c; a) | client(c; b)).\n")
    assert "client takes c at ~Bank" in refused(tmp_path, text)
    r = unchecked(tmp_path, text)
    assert r.returncode == 2, (r.returncode, r.stdout, r.stderr)
    assert "the check let this through" in r.stderr and "'deposit'" in r.stderr and "a number" in r.stderr, r.stderr
