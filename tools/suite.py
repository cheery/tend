#!/usr/bin/env python3
#: asked-by: Henri, 2026-08-24 — "add the needed cards so that the absent work is completed"
"""tools/suite.py — run tend's suite, and say so.

    python3 tools/suite.py              everything under test/
    python3 tools/suite.py -k board     arguments pass through to pytest

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
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main(argv):
    r = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "test/", *argv], cwd=ROOT)
    if r.returncode == 0:
        print("suite.py: the gates hold.")
    else:
        print("suite.py: a gate failed — the tree disagrees with itself; "
              "the failure above says where.")
    return r.returncode


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
