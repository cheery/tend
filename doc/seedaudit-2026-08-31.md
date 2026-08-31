# seedaudit — gestate's audit, run against tend, 2026-08-31

*The first run on this laptop.  On 2026-08-25 the same command here was
`can't open file '/home/cheery/gestate/tools/seedaudit.py'` — the other tree
was not bound (`doc/experiments/2026-08-25-reach.md`).  It runs now because
`card:trees.md` landed this morning and Henri put gestate at `~/gestate` and
ran `sudo tend-install` that afternoon; this was the first use the bind was
put to.  Kept verbatim so the next run has something to diff against —
the 7 of 2026-08-26 has no stored output, which is why the board's
paragraph cannot say which piece moved.  Run from inside the fence,
read-only, by a session:*

    $ python ~/gestate/tools/seedaudit.py ~/tend

    seedaudit: /home/henri/tend
    
      the pieces that exist only because a person is on the other end
    
        UNBACKED  the fence                   no test names it
                  a session cannot edit its own restraints
        ok        the gates                   test/test_precommit.py
        UNBACKED  the consent register        no test names it
                  a named third party agreed to being named
        ok        the andon                   test/test_andon.py
        ok        a blocked status            test/test_board.py
        ABSENT    the rules cap               missing spec/rules.md, tools/rulecount.py
                  the rules stay short enough that a person actually reads them
        ABSENT    the memory split            missing doc/memory/README.md
                  what is known about a person is not automatically the tree's
        ok        the sitting limit           test/test_limit.py
        ok        the boot surface            test/test_rules.py
        UNBACKED  the author's own document   no test names it
                  the person keeps a document no session rewrites
    
      promises the method documents make that this directory cannot keep
    
        MISSING   (the document itself)       named in doc/instruments.md
        MISSING   fixme/F000.md               named in board/README.md
        MISSING   test/test_safety.py         named in board/README.md
        MISSING   tools/andon-panel.py        named in board/README.md
    
      8 of 10 pieces present,  3 unbacked,  4 unkept promise(s),  0 unbuilt
    
      An unbacked piece is a rule with no gate — the second of the
      two failures this audit exists for.  It fails the run.

*Verdict: red, as it has been since 2026-08-24 — an unbacked piece fails
the run.  What each line means for tend, and which of the four "unkept
promises" are the audit reading tend's own prose as a claim, is in
`board/README.md` §"What this tree does not have yet".*
