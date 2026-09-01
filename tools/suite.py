#!/usr/bin/env python3
#: asked-by: Henri, 2026-08-24 — "add the needed cards so that the absent work is completed"
"""tools/suite.py — run tend's suite, and say so; keep a count of what failed.

    python3 tools/suite.py                     everything under test/
    python3 tools/suite.py -k board            arguments pass through to pytest
    python3 tools/suite.py --shake TEST [N]    one test N times (default 10) with every
                                               core burning; says "k of N failed under load"

Borrowed in shape from gestate's `tools/suite.py` on 2026-08-24
(`card:gates.md`), and cut to what tend has: a few seconds of tests and
no page.  The report machinery there exists because gestate's suite runs
for minutes across two runtimes and a run that lives only in scrollback
has said nothing by tomorrow; writing that here before a slow test
exists would be building what nothing needs (`manifesto.md` rule 1).
The page arrives with the first test that takes minutes.

What this buys over calling pytest directly is one thing: a single
name for "the gates" that `tools/pre-commit.sh` and a person run the
same way, so the set of checks a commit must pass is decided here and
nowhere else.

**The failure ledger** (card:flake.md, 2026-08-29 — Henri: "Would there
be a way to catch the flake?").  Three times in six days a test failed
once and passed on the re-run, and each time the session met it with
its own memory.  So every run writes one line per failed test to
`~/.local/state/tend/failed.log` (TEND_FAILED_LOG) — when, where (`gate`
from the hook, `hand` from a terminal, `shake`), the test id, the load
average, the wall — on the person's side, never the tree; and the
report reads the ledger back: a failure with a line already is *seen
before, N times* in the same breath as the red.  Append-only; a re-run
that passes removes nothing.  **The shake** is the 2026-08-26 "1 in 10"
as a tool, with the load that trips a load-sensitive rule.  Never a
silent retry: the suite runs once and reports once; the shake is a
deliberate act and its count is the finding.
"""

import datetime
import os
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# The gate's set.  Henri, 2026-09-01: "it's supposed to be around 30
# seconds, quick check that the things you rely on, citations, notations,
# etc. are still consistent.  The program tests should live in
# tools/suite.py".
#
# Measured that morning, the reason the split was wanted: the whole suite
# was **297 seconds** on every commit, and the consistency half of it is
# **1.9** — 258 tests.  The rest is programs being run: test_launch 65 s,
# test_mutate 62 s, test_deliver 41 s.  A gate that stands where the commit
# happens has to be cheap or it stops being a gate and becomes a toll.
#
# What is here is the tree agreeing with itself — a claim one file makes
# about another, which no amount of running programs will check.  What is
# not here is anything that starts a process.  **A new test file is not in
# the gate unless it is named here**, which is the safe default (it still
# runs in the full suite) and is worth knowing when adding one.
GATE_TARGETS = [
    "test/test_board.py",       # a card's fields, and every card: citation resolving on either shelf
    "test/test_fixme.py",       # the same for F-numbers, and the other tree's written with its tree
    "test/test_summary.py",     # the sheets' citations, and the HTML twin agreeing with the text
    "test/test_rules.py",       # the boot surface stays one line each
    "test/test_selfmatch.py",   # no pattern kill in this tree matches its own command line
                                # (worded without the pattern itself: the first draft of this
                                #  comment named the tool and the gate refused it in 2 seconds)
    "test/test_ledger.py",      # the failure ledger's own parser
    "test/test_precommit.py",   # the gate's own installation
]


def ledger_path():
    return os.environ.get("TEND_FAILED_LOG") or os.path.join(
        os.path.expanduser("~"), ".local", "state", "tend", "failed.log")


def passed_path():
    return os.environ.get("TEND_SUITE_PASSED") or os.path.join(
        os.path.expanduser("~"), ".local", "state", "tend", "suite-passed")


def _git(*args):
    try:
        out = subprocess.run(["git", "-C", str(ROOT), *args],
                             capture_output=True, text=True)
        return out.stdout.strip() if out.returncode == 0 else ""
    except OSError:
        return ""


def stamp_full_pass():
    """Record that the *whole* suite passed, and at which commit.

    The failure ledger records failures only, so until 2026-09-01 nothing
    in the tree knew the suite had ever passed — which was fine while the
    gate ran all of it and is not fine now that the gate runs the
    consistency half.  A gate that stops checking something and says
    nothing is the defect this tree spent that morning removing twice
    (F008, F010); this is what lets it say.
    """
    path = passed_path()
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as fh:
            fh.write(f"{_git('rev-parse', 'HEAD')}\n"
                     f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    except OSError:
        pass        # a stamp that cannot be written is not worth a failed run


def full_pass_line():
    """One line for the gate: when the program tests last passed whole.

    Says `never` rather than nothing when there is no stamp — the whole
    point is that silence is what we are removing.
    """
    try:
        with open(passed_path()) as fh:
            commit = fh.readline().strip()
            when = fh.readline().strip()
    except OSError:
        return ("the program tests did not run here — python3 tools/suite.py is the whole "
                "suite, and it has never been recorded passing")
    behind = _git("rev-list", "--count", f"{commit}..HEAD") if commit else ""
    if behind == "0":
        how = "at this commit"
    elif behind:
        how = f"{behind} commit{'s' if behind != '1' else ''} ago"
    else:
        how = f"at {commit[:7]}"
    return (f"the program tests did not run here — python3 tools/suite.py is the whole "
            f"suite; it last passed {how} ({when})")


def _failed_in(junit):
    """The failed tests of one run, as test/file.py::name, from pytest's junit file."""
    out = []
    try:
        root = ET.parse(junit).getroot()
    except (OSError, ET.ParseError):
        return out
    for tc in root.iter("testcase"):
        if tc.find("failure") is None and tc.find("error") is None:
            continue
        cls = tc.get("classname", "")
        f = tc.get("file") or (cls.replace(".", "/") + ".py")
        out.append(f"{f}::{tc.get('name', '?')}")
    return out


def seen_before(test):
    """How many ledger lines already name this test, and the last one's stamp."""
    n, last = 0, None
    try:
        with open(ledger_path()) as fh:
            for line in fh:
                parts = line.rstrip("\n").split("  ")
                if len(parts) >= 3 and parts[2] == test:
                    n += 1; last = parts[0]
    except OSError:
        pass
    return n, last


def record(failed, where, wall):
    """One ledger line per failed test; the count of earlier lines, read first."""
    before = {t: seen_before(t) for t in failed}
    if not failed:
        return before
    try:
        load = os.getloadavg()[0]
    except (OSError, AttributeError):
        load = float("nan")
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    path = ledger_path()
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "a") as fh:
            for t in failed:
                fh.write(f"{stamp}  {where}  {t}  load {load:.2f}  wall {wall:.1f}s\n")
    except OSError as e:
        print(f"suite.py: could not write the failure ledger {path}: {e}")
    return before


def run(targets, argv, where):
    """One pytest run over targets; returns (returncode, failed ids, wall seconds)."""
    with tempfile.TemporaryDirectory() as d:
        junit = os.path.join(d, "junit.xml")
        t0 = time.monotonic()
        r = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", *targets,
             "--junitxml", junit, "-o", "junit_family=xunit1", *argv], cwd=ROOT)
        wall = time.monotonic() - t0
        failed = _failed_in(junit)
    return r.returncode, failed, wall


def report_failed(failed, before):
    print(f"suite.py: {len(failed)} failed, on the ledger: {ledger_path()}")
    for t in failed:
        n, last = before.get(t, (0, None))
        if n:
            print(f"suite.py:   {t} — seen before, {n} time{'s' if n != 1 else ''} (last {last}); "
                  f"a red that vanishes on retry is a claim about the instrument first")


def shake(test, n, argv):
    cores = os.cpu_count() or 2
    burners = [subprocess.Popen([sys.executable, "-c", "while True: pass"],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
               for _ in range(cores)]
    fails = 0
    try:
        for _ in range(n):
            rc, failed, wall = run([test], argv, "shake")
            if rc != 0:
                fails += 1
                record(failed or [test], "shake", wall)
    finally:
        for b in burners:
            b.kill()
        for b in burners:
            b.wait()
    print(f"suite.py: shake — {fails} of {n} runs of {test} failed under load ({cores} cores burning); "
          f"the ledger has the lines: {ledger_path()}")
    return 1 if fails else 0


def main(argv):
    if argv and argv[0] == "--shake":
        if len(argv) < 2:
            print("suite.py: --shake TEST [N]"); return 2
        test = argv[1]; rest = argv[2:]; n = 10
        if rest and rest[0].isdigit():
            n = int(rest[0]); rest = rest[1:]
        return shake(test, n, rest)
    gate = bool(argv) and argv[0] == "--gate"
    if gate:
        argv = argv[1:]
    targets = GATE_TARGETS if gate else ["test/"]
    where = os.environ.get("TEND_SUITE_WHERE", "hand")
    rc, failed, wall = run(targets, argv, where)
    if rc == 0:
        print("suite.py: the gates hold.")
        if gate:
            # the gate says what it did not check — a cap is a gate and a
            # gate says what it stopped (F008, the same morning)
            print(f"suite.py: {full_pass_line()}")
        elif not argv:
            stamp_full_pass()
    else:
        print("suite.py: a gate failed — the tree disagrees with itself; "
              "the failure above says where.")
        before = record(failed, where, wall)
        if failed:
            report_failed(failed, before)
    return rc


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
