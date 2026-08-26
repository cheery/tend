"""`tools/ledger.py` — the leash ledger read by record, not by line.

A record's command spans lines when it carried a heredoc, so a
line-based count is wrong before it is printed (the 13:42 kaizen: 2978
for a sitting of 53).  The fixture here has exactly that seam — one
record whose command is three lines — and the counts must not see it.
"""

import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LEDGER = ROOT / "tools" / "ledger.py"

FIXTURE = (
    "1787740020\t3\t0\tt=900 c=200% m=- scope\tcpu=1.5s\tsandbox.sh bash -c one\n"
    "1787740080\t97\t0\tt=900 c=200% m=- scope\tcpu=23.3s\tsandbox.sh bash -c cat <<'EOF'\n"
    "line two of the same command\n"
    "EOF\n"
    "1787740140\t900\t124\tt=900 c=200% m=- scope\tcpu=0.0s\tsandbox.sh bash -c sleep\n"
    "1787740200\t1\t0\tt=900 c=- m=- plain\tcpu=-\tsandbox.sh bash -c plain one\n"
)


def ledger(tmp_path, *args):
    log = tmp_path / "leash.log"
    if not log.exists():
        log.write_text(FIXTURE)
    return subprocess.run([sys.executable, str(LEDGER), *args],
                          env=dict(os.environ, TEND_LEASH_LOG=str(log)),
                          capture_output=True, text=True)


def test_it_parses():
    assert subprocess.run([sys.executable, "-m", "py_compile", str(LEDGER)]).returncode == 0


def test_a_record_spans_lines_and_is_counted_once(tmp_path):
    r = ledger(tmp_path)
    assert r.returncode == 0, r.stderr
    assert "records  4 " in r.stdout, r.stdout
    assert "scope=3" in r.stdout and "plain=1" in r.stdout
    assert "124×1" in r.stdout
    assert "cpu      24.8s total, 2 of 3 records > 0" in r.stdout, r.stdout


def test_grep_finds_the_continuation_line(tmp_path):
    """The heredoc body belongs to its record: grep for a phrase that
    only appears on the continuation line finds the record."""
    r = ledger(tmp_path, "grep", "line two")
    assert "-- 1 records" in r.stdout, r.stdout
    assert " 97s" in r.stdout


def test_since_cuts_by_time(tmp_path):
    import time
    t = time.strftime("%Y-%m-%d %H:%M", time.localtime(1787740140))  # a minute boundary
    r = ledger(tmp_path, "since", t)
    assert "records  2 " in r.stdout, r.stdout


def test_a_missing_ledger_is_said(tmp_path):
    r = subprocess.run([sys.executable, str(LEDGER)],
                       env=dict(os.environ, TEND_LEASH_LOG=str(tmp_path / "none")),
                       capture_output=True, text=True)
    assert r.returncode == 0 and "no records" in r.stdout


def test_an_unknown_argument_is_refused(tmp_path):
    r = ledger(tmp_path, "bogus")
    assert r.returncode == 2 and "unknown argument" in r.stderr
