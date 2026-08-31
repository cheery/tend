"""tools/simpleqa.py — the benchmark's runner: three arms, cold turns, the paper's grader (card:simpleqa.md, day one).

What is held: the arms differ only as the card says (bare — nothing at
all; seat — the courier's seat line and the door's tools; bland — one
plain line before the question); every turn is cold, with no history
and nothing carried between questions or arms; every account lands
under the gitignored proposals dir with the gold target beside the
answer; a run with no bench/ says the cp lines and exits 2; a rerun
answers nothing twice; and the verdict waits on the thirty hand
grades.
"""
import http.server
import subprocess
import sys
import threading
from pathlib import Path

import test_deliver as td

ROOT = Path(__file__).resolve().parent.parent
SQ = ROOT / "tools" / "simpleqa.py"


def _stub_server():
    srv = http.server.HTTPServer(("127.0.0.1", 0), td._Stub)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{srv.server_address[1]}"
    return srv, {"TEND_LLM_URL": base + "/v1/chat/completions", "TEND_LLM_HEALTH": base + "/health"}


def a_bench(tmp_path):
    """A bench of the test's own: three rows, and a grader template whose
    filled form is one predictable line."""
    b = tmp_path / "bench"; (b / "simple-evals").mkdir(parents=True)
    (b / "simple_qa_test_set.csv").write_text(
        "metadata,problem,answer\n"
        '"{m}","What is one?","1"\n'
        '"{m}","What is two?","2"\n'
        '"{m}","What is three?","3"\n')
    (b / "simple-evals" / "simpleqa_eval.py").write_text(
        'GRADER_TEMPLATE = """\nGrade Q {question} T {target} P {predicted_answer}\n""".strip()\n')
    return b


def run_sq(tmp_path, *args, stub, doors, tree):
    env = {"PATH": "/usr/bin:/bin", "TEND_TREE": str(tree),
           "TEND_BENCH_DIR": str(tmp_path / "bench"),
           "TEND_PROPOSAL_DIR": str(tmp_path / "props"), **stub, **doors}
    return subprocess.run([sys.executable, str(SQ), *args], capture_output=True, text=True, env=env)


def test_a_run_with_no_bench_says_the_cp_lines_and_touches_nothing(tmp_path):
    t = td.a_tree(tmp_path)
    r = run_sq(tmp_path, "run", "1", stub={}, doors={}, tree=t)
    assert r.returncode == 2 and "cp " in r.stderr and "bench" in r.stderr, r.stderr
    assert not (tmp_path / "props").exists(), "refused before any ask"


def test_run_answers_three_cold_arms_grades_them_through_the_other_door_and_resumes(tmp_path):
    srv, stub = _stub_server()
    doors = td.a_tooled_door(tmp_path, stub, tools="read ls grep")
    td.a_door(tmp_path, stub, name="anthropic")   # the grader's door, same stub
    t = td.a_tree(tmp_path); a_bench(tmp_path)
    for w, n in (("one", 1), ("two", 2), ("three", 3)):
        td.SCRIPT[f"What is {w}?"] = [("say", "I do not know")]
        td.SCRIPT[f"Answer the question; say so if you do not know. Question: What is {w}?"] = [("say", "I do not know")]
        td.SCRIPT[f"Grade Q What is {w}? T {n} P I do not know"] = [("say", "C")]
    n0 = len(td.BODIES)
    r = run_sq(tmp_path, "run", "1", stub=stub, doors=doors, tree=t)
    assert r.returncode == 0, r.stderr + r.stdout
    reqs = td.BODIES[n0:]
    assert len(reqs) == 8, "four arms and four grades, one question"
    tooled = [b for b in reqs if "tools" in b]
    assert len(tooled) == 2, "seat and bland carry the door's tools; bare, think and the grader never"
    seat = next(b for b in tooled if b["messages"][-1]["content"].startswith("What is"))
    bland = next(b for b in tooled if b["messages"][-1]["content"].startswith("Answer the question; say so if you do not know. Question: What is"))
    assert seat["messages"][0]["role"] == "system" and "read ls grep" in seat["messages"][0]["content"], "the courier's seat line, nothing else"
    assert len(seat["messages"]) == 2 and len(bland["messages"]) == 2, "cold — no history, no memories between turns"
    bare = next(b for b in reqs if "tools" not in b and "reasoning" not in b and b["messages"][0]["content"].startswith("What is"))
    assert len(bare["messages"]) == 1 and bare["messages"][0]["role"] == "user", "bare: no system line at all"
    think = next(b for b in reqs if "reasoning" in b)
    assert think["reasoning"] == {"enabled": True} and "tools" not in think, "think: bare with the reasoning channel on — the leak's control"
    assert len(think["messages"]) == 1 and think["messages"][0]["content"].startswith("What is")
    grades = [b for b in reqs if b["messages"][0]["content"].startswith("Grade Q")]
    assert len(grades) == 4 and all("tools" not in b for b in grades)
    assert all(b["messages"][-1]["content"] == "Grade." and len(b["messages"]) == 2 for b in grades), "the rubric rides whole, unflattened, as the first message"
    props = tmp_path / "props" / "simpleqa"
    accounts = sorted(props.glob("q000-*.md"))
    assert [a.name for a in accounts] == ["q000-bare.md", "q000-bland.md", "q000-seat.md", "q000-think.md"]
    for a in accounts:
        txt = a.read_text()
        assert "    looked    no" in txt and "I do not know" in txt
        assert "    grade    NOT_ATTEMPTED — anthropic (vendor/some-model)" in txt, txt
        assert txt.index("    grade    ") < txt.index("The answer"), "the grade joins the field block"
    # the run's lines land in bench/log too (Henri, 2026-08-31: "lets put it write its output into bench/log")
    log = (tmp_path / "bench" / "log").read_text()
    assert "graded NOT_ATTEMPTED" in log and "answered and" in log
    # resume: a second run answers nothing and grades nothing twice
    n1 = len(td.BODIES)
    r = run_sq(tmp_path, "run", "1", stub=stub, doors=doors, tree=t)
    srv.shutdown()
    assert r.returncode == 0, r.stderr
    assert len(td.BODIES) == n1, "a rerun answers nothing twice — the account is the resume"
    assert "0 answered and 0 graded" in r.stdout
    # tally: bins per arm, the fourth count apart, the exam-card count (the smoke's find), the verdict held back
    def synth(name, arm, grade, looked, answer, calls=()):
        (props / name).write_text(
            f"<!-- SIMPLEQA — synthetic for the tally. -->\n\n"
            f"    question  q\n    target    t\n    arm       {arm}\n    door      openrouter (m)\n"
            f"    calls     {len(calls)}\n    looked    {looked}\n    grade    {grade} — anthropic (m)\n\n"
            + ("The calls:\n\n" + "".join(f"    C: {c}\n" for c in calls) + "\n" if calls else "")
            + f"The answer, verbatim:\n\n    {answer}\n")

    synth("q001-seat.md", "seat", "NOT_ATTEMPTED", "yes", "I do not know",
          ("grep SimpleQA . → 3 lines in 1 file", "read board/simpleqa.md → 9.0k chars"))
    # a question the baseline got right and the tooled arm got wrong, sourced — the churn
    # the three bins hide, and the provenance the grader cannot see (2026-08-31, the first run)
    synth("q002-bare.md", "bare", "CORRECT", "no", "Francois de Malherbe.")
    synth("q002-seat.md", "seat", "INCORRECT", "yes",
          "The tree has no answer, so from my own knowledge: Tangdan.", ("grep Tangdan . → 0 lines in 0 files",))
    r = run_sq(tmp_path, "tally", stub={}, doors={}, tree=t)
    assert r.returncode == 0, r.stderr
    assert "bare    correct    1  incorrect    0  not-attempted    1  (never looked 1, saw the card 0)" in r.stdout, r.stdout
    assert "saw the card 1" in r.stdout, "a turn whose calls touched the benchmark's own card is counted"
    assert "waits on `hand`" in r.stdout
    # what the bins cannot see: whether the assertion says where it comes from, and whether looking gated it
    assert "bare       1 asserted,    0 wrong (0%),    0 say where the claim comes from" in r.stdout, r.stdout
    assert "seat       1 asserted,    1 wrong (100%),    1 say where the claim comes from" in r.stdout, r.stdout
    assert "looked then asserted    1, looked then refused    1" in r.stdout, "the split says whether looking gated the assertion"
    # what the bins hide: the churn, question by question against the baseline arm
    assert "bare → seat, where 2 answers went:" in r.stdout, r.stdout
    assert "was correct        (  1)  →  correct 0, incorrect 1, not-attempted 0" in r.stdout, r.stdout
    assert "0 wrongs repaired, 1 created, 0 known answers withheld; 50% stayed in their bin" in r.stdout, r.stdout
    # hand: thirty are wanted before any number, and three are not thirty
    r = run_sq(tmp_path, "hand", stub={}, doors={}, tree=t)
    assert r.returncode == 2 and "30" in r.stderr, r.stderr
