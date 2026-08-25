# os.md — what tend is striving for, in the words it was first asked in

*Henri's list, written 2026-08-19 as `~/misc/os.txt`, brought into the
tree 2026-08-25 at his ask — "so that we have more clear idea of what
we're striving for."  His words are the Finnish and the first line, kept
verbatim; the English beside each is a session's rendering and is his
to correct.  Until now the list lived only outside the tree and as one
paraphrasing sentence in `board/work-environment-ai.md`.  Read and
approved by Henri, 2026-08-25 — the renderings and the rule at the
foot, which a session drafted, are his from that date.*

*This is a property sheet, not a vision and not a card.  A line in
`vision.md` has already decided something; a card names a problem; a
property here names what the finished thing should be like, and most
of them name a fix, which is why the list could not be a card as
written (`board/work-environment-ai.md` §"How the reading was chosen").
It binds nothing by itself.  What it does is let a reader ask of any
mechanism that arrives: which of these does it serve?*

## The properties

1. *software should be auditable and bounded on it's own interface and
   specification* — a program can be audited and bounded from its own
   interface and specification alone.

2. *käyttöjärjestelmässä ohjelman asentamisen testaamisen ei saisi olla
   vaikeata.* — testing a program's installation should not be hard.

3. *käyttöjärjestelmä tulisi olla turvalliseksi suunniteltu* — designed
   secure.

4. *rinnakkaisajoon suunniteltu ohjelmaympäristö, ohjelman
   toiminnallisuus tulisi varmistaa tietotyypein ja automaattisten
   mallintarkastimien avulla.  käyttöjärjestelmä tulisi suunnitella
   siten että sen jokainen osa on testattavissa.* — an environment
   designed for concurrent execution; a program's behaviour verified by
   types and automatic model checkers; every part of the system
   testable.

5. *mikäli asennus konfiguroi ohjelman, tehty konfiguraatio tulee
   merkitä ohjelmasolmuun.  veto-menetelmällä ohjelma tulisi kyetä
   uudelleenkonfiguroimaan sieltä mistä se tulikin.* — if installing
   configures a program, the configuration is recorded in the program's
   node; by pull, a program can be reconfigured from wherever it came
   from.

6. *ohjelma versio merkitään siten että sen tunn.  oletuksena ei ole
   keskuspalvelinta* — a program's version is marked so that it can be
   identified *(the original breaks off at "tunn.")*; there is no
   central server by default.

7. *ohjelman pitää kyetä ajamaan Linuxia, mutta se ei saa heikentää
   turvallisuutta.* — it must be able to run Linux, and that must not
   weaken security.  *(Decided for tend: `vision.md` §"What tend won't
   be" — runs over Linux for now, an OS of its own is a later question.)*

8. *tilaverkko, ohjelmien kuuluisi avautua siihen tilaan mihin ne jäivät
   sammutuksessa.  ohjelmien vuorovaikutus ei saisi rikkoa toisiaan.* —
   a state network: programs open in the state they were left in at
   shutdown; programs interacting must not break each other.
   *(Decided for tend: `vision.md` §"Tend as a working platform" — a
   program opens where it was left.)*

9. *ohjelma saa kaatua, mutta se ei saa jäädä pysähdyksiin ellei se
   kaadu jatkuvasti uudelleen tai ei vastaa ajoissa.* — a program may
   crash, but it may not hang: not unless it crashes over and over, or
   fails to answer in time.  *(In force for one instrument:
   `tools/leash.sh` treats a hang as a crash, exit 124.)*

10. *lokalisaatio kääntäjällä.* — localisation by the compiler.

11. *Käyttöjärjestelmä suunniteltu siten että siihen on vaikea hyökätä
    ulkopuolelta.* — designed so that it is hard to attack from outside.

12. *tekoälyn käyttöön suunniteltu.  käyttö ei saa uhata
    turvallisuutta.* — designed for the use of AI; that use must not
    threaten security.  *(Decided for tend, in these words: `vision.md`
    §"Tend as a working platform".  The one property the card calls
    genuinely novel.)*

13. *ohjelmien käynnistyminen pull-menetelmään perustuva.  mikäli käyttäjä
    ei "vedä" niin ohjelma sammuu itsestään.* — programs start by pull;
    if the user does not "pull", the program shuts itself down.
    *(Decided for tend: `vision.md`, the stranger test — "see it stop
    when they stop pulling".)*

14. *virheet eivät saa olla hiljaisia.  ne täytyy tuoda esiin.* — errors
    may not be silent; they must be brought out.  *(Decided for tend:
    `vision.md` — "won't ever do anything unexpected silently".)*

15. *käyttöjärjestelmä tuottaa oman ohjelmointikielensä.* — the system
    produces its own programming language.  *uusi ohjelmointikieli
    tehdään seuraavan paperin pohjalta:* https://arxiv.org/abs/1507.05762
    — the new language is made on the basis of that paper.

16. *enkryptattu levy standardina* — encrypted disk as standard.

*bootstrap kielet ovat python ja rust* — the bootstrap languages are
Python and Rust.

## Open problems, as he left them

*Avoimia ongelmia:*

* *miten käyttäjien tiedot suojataan ohjelmilta?* — how are users' data
  protected from programs?
* *miten ohjelmat suojataan ja asennetaan?* — how are programs
  protected, and installed?
* *miten ohjelmien toiminta pidetään nopeana jos ne suljetaan samantien
  kun tarvetta ei enää ole?* — how do programs stay fast if they are
  closed the moment they are no longer needed?

These three are the nearest thing on the sheet to a `because`, and the
only lines on it that name a problem rather than a fix.  The third is
already touched by `board/work-environment-ai.md` (CRIU kept in the
pocket as a latency optimisation, not as the state model); the first
two are on no card.

## What this document is not

It is not the architecture — that is in `board/work-environment-ai.md`
and is marked suspected there.  It is not a promise that all sixteen
will be built; `vision.md` says ease of use wins when the platform
conflicts with it.  A session does not rewrite the Finnish.  It may
append, dated, which property a new mechanism serves, and may add to
the open problems; taking one off is Henri's.
