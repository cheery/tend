# Transkriptio: lineaarilogiikkaan perustuva ohjelmointikieli LLM-aikakaudelle

Päivämäärä: 2026-09-21
Osapuolet: käyttäjä (U) ja Claude (C)
Tarkoitus: jaettava konteksti Claude Code -sessiolle. Keskustelu on tallennettu alkuperäisillä kielillä (englanti, sitten suomi).

Viitattu paperi:
**Horn Clauses as an Intermediate Representation for Program Analysis and Transformation**
Graeme Gange, Jorge A. Navas, Peter Schachte, Harald Søndergaard, Peter J. Stuckey
https://jorgenavas.github.io/papers/lpvm.pdf
(Tässä keskustelussa siihen viitataan nimillä "LPVM-paperi" ja "LP form".)

---

## 1. Ohjelma LLM:n "kätenä"

**U:** Wondering that when LLM session writes a program, it is a bit like it's "hand". I wonder what should be understandable by human here, and what is?

**C:** The "hand" metaphor is off in one important way, and that's where the answer sits. A hand stops when you stop paying attention. A program doesn't. What an LLM session produces is less a hand than a prosthesis that keeps moving after the session is gone, with no operator attached. So the question isn't really "what should be understandable" but "what has to be understandable to something that will still be around when this runs."

Three layers, in order of how much a human should own them:

- **What it does** — the observable behavior. This has to be understandable, and the honest form of it is tests and examples, not prose. If the only description of behavior is a comment the model wrote, you have the model's claim about the model's work.
- **Why it does it** — the intent, the constraints, the things deliberately not handled. This is where LLM-written code is weakest, and it's not obvious from the outside because the code *looks* like it has reasons. Comments in generated code are often post-hoc rationalization: plausible, fluent, and not the actual causal story of why that line exists. The actual causal story was in the conversation and is now gone. If you don't write the "why" down yourself, it doesn't exist anywhere.
- **How it does it** — the implementation. This can be delegated. It should stay *auditable*, meaning a competent person could read it and check it, but it doesn't need to be *understood* by anyone up front. Same deal as with libraries you didn't write.

What actually *is* understandable: syntactically, all of it. Practically, less than people assume. Generated code is idiomatic and confident, and those surface features are what humans use as proxies for "this is fine"; the proxies stop working when the author is a model. And nobody reads it: generation got cheap, reading didn't, so the ratio of code-that-exists to code-someone-understands moves in one direction.

The realistic answer: a person ends up responsible for a program they didn't write and didn't read. That's already common with legacy code; the difference is the timescale collapses from years to minutes. The defensible position is to own the behavior (tests you wrote or at least read) and the intent (a spec or commit message in your words), and treat the implementation as a black box you *could* open, with the discipline to actually open it when the stakes justify it.

---

## 2. Kielisuunnitelmat lineaarilogiikan päälle

**U:** I would want us to design a programming language around linear logic. The type would be writeable and readable by a person familiar with linear logic and common programming concepts. The program would be represented in some way that is natural for LLM to handle, and it would be compiled into some kind of a virtual machine natural for computers to handle. Present variety of different designs that would satisfy this, if there are multiple ones.

**C:** Three layers, three different audiences, and the point of linear logic is that the type layer can carry the *intent* that got lost in the previous discussion: "this file handle is used exactly once, then returned" is a specification, not a comment. So the split is: human writes propositions, LLM writes proofs, checker verifies, VM runs.

### Design 1 — Sequent proofs as tactic scripts, linear abstract machine

**Types:** intuitionistic linear logic with fixpoints and second-order quantifiers.

```
sort     : ∀α. !(α ⊗ α ⊸ Bool ⊗ α ⊗ α) ⊸ List α ⊸ List α
withFile : Path ⊸ (Handle ⊸ Handle ⊗ A) ⊸ A
```

**Program representation:** a proof script — a sequence of rule applications on named hypotheses, like a Coq/Lean proof.

```
withFile p k :
  intro h ← open p            -- h : Handle
  cut (h', a) ← k h            -- ⊗-left
  close h'
  exact a
```

LLM-natural because each line is one inference step with a local, checkable obligation; the context (unconsumed resources) is explicit at every point; holes (`?goal : Handle ⊗ A`) give the model a target.

**VM:** Lafont-style linear abstract machine. Every value has exactly one consumer, so the heap is a set of uniquely-owned cells: no GC, in-place update free, `!A` cells the only ones refcounted or copied.

### Design 2 — Classical linear logic as session types, process VM

**Types:** classical LL read as protocols. `⊗` = send then continue, `⅋` = receive then continue, `⊕` = I choose, `&` = you choose, `!A` = replicable service, `1`/`⊥` = close channel. Duality is protocol complement.

```
Bank   = &{ deposit : Int ⅋ Bank,
            withdraw : Int ⅋ (Int ⊕ Err) ⊗ Bank,
            quit : 1 }
Client = Bank⊥
```

**Program representation:** CP/SILL-style processes — a sequential list of `send`/`recv`/`case`/`offer`/`close` per channel.

```
client c =
  c.withdraw ; send c 50 ;
  case c { ok n  → c.quit ; close c
         ; err e → c.quit ; close c }
```

LLM-natural because it's imperative-looking: one channel, a linear sequence of actions, and the type is literally a state machine the model can walk. Concurrency structure comes from `cut` (parallel composition), the only place two channels meet, so deadlock and race freedom fall out of the typing.

**VM:** typed channels + coroutines. Each cut is a pair of lightweight threads; `!` is a server that forks on demand. Every channel has exactly two endpoints, so it compiles to shared-memory single-producer/single-consumer queues with no locking, or to a message-passing runtime.

### Design 3 — Concatenative (stack) language, linear stack machine

**Types:** stack effects as linear implications.

```
open  : Path ⊸ Handle
split : List α ⊸ List α ⊗ List α
dup   : !α ⊸ !α ⊗ !α           -- the only source of copying
```

**Program representation:** point-free word sequences, no variables.

```
mergesort = split mergesort swap mergesort merge
```

Linearity on a stack is trivial: every push produced once, every pop consumes once. Variable binding is where LLMs make the most mechanical errors; there is none here. Stack shuffling words are exactly the exchange rule; no contraction or weakening unless the type has a `!`. Type checking is a left-to-right fold, so a model can be checked token by token as it generates. Cost: humans read long point-free programs badly; mitigate with local names that desugar to shuffles.

**VM:** nearly the identity; the source *is* a linear stack machine program.

### Design 4 — Proof nets as canonical form, interaction-net VM

**Types:** MLL/MALL with exponentials.

**Program representation:** the canonical object is the proof net (a graph), serialized as nodes and wires:

```
(net
  (ax a1 a2) (tensor t1 a1 b1 out) (par p1 ...)
  (cut a2 x1) ...)
```

Humans write a small term language that elaborates into nets and see nets rendered. A sequent proof over-specifies order; many textually different proofs are the same net. For an LLM that matters: sampling diversity in the token stream maps to one object, so equivalence checking, caching, and diffing happen on the net. Whether LLMs handle graph serializations *well* is unproven.

**VM:** interaction nets. Local rewriting, confluent, parallel; HVM/Bend is a production-grade instance. Optimal reduction for the multiplicative fragment; exponentials (boxes) are where it gets hard.

### Design 5 — Ownership surface, linear core

**Types:** LL notation in signatures, term language ML/Rust-shaped.

```
read : File ⊸ File ⊗ !String
let (f', s) = read f in
close f'; s
```

Least novel, most fluent for an LLM today due to training distribution. Linearity is checked, not inferred from ownership heuristics. Effects fall out for free: the outside world is a linear token (as in Clean).

**VM:** MIR/LLVM-like register machine with moves. Deterministic destruction and in-place mutation; `!` values the only ones needing refcounts.

### Cross-cutting choices

- **Intuitionistic vs classical.** ILL gives functions; CLL gives protocols and duality. Design 2 needs CLL.
- **Exponential vs grading.** Pure `!` is coarse. Graded modalities (`[0]`, `[1]`, `[ω]`, `[≤n]`) are more readable and give cost bounds (Granule).
- **Recursion.** `μ/ν` fixpoints on types (total, proof-theoretically clean) or general recursion via `!`.
- **Polymorphism.** Second-order LL = System F-linear.
- **Light/bounded fragments** (LLL, SLL) give polynomial-time guarantees by construction.

### Comparison

| | Human-readable types | LLM-natural terms | VM fit |
|---|---|---|---|
| 1 Tactic scripts | ✓ | best for checkability | linear AM, good |
| 2 Sessions | ✓ (as protocols) | good, imperative shape | channels, excellent for concurrency |
| 3 Concatenative | ✓ | best for mechanical correctness, no binders | trivial, excellent |
| 4 Proof nets | ✓ | unproven; canonical form is the win | interaction nets, best for parallelism |
| 5 Ownership surface | ✓ | best by familiarity | register machine, best today |

"Natural for an LLM" splits into *familiar* (5 wins) and *hard to get wrong* (3 and 1 win). "Natural for a computer" splits into sequential (1, 3, 5) and parallel (2, 4).

Recommendation given: Design 3's core with Design 1's checker discipline, a Design 5-like sugar layer for humans, compile to a linear stack machine first, retarget to interaction nets if parallelism matters. Design 2 is the pick if the domain is actually concurrent systems, and there it isn't close.

---

## 3. Käyttöliittymät, tarpeellisuus, Design 2 ja LPVM

**U:** Minulla on toistuvaa halua tehdä tietokoneen käyttöliittymistä, niin sisäisistä kuin ulkoisistakin, parempia. Mutta olen alkanut miettiä mitä se tarkoittaisi? Toisena mietin mikä siitä on tarpeen? Minua esimerkiksi kiehtoisi paljon juuri nyt "design 2" vietynä niin pitkälle että sillä voisi tuottaa oikeita ohjelmia. Ja se sitoutuu kivasti seuraavan paperin https://jorgenavas.github.io/papers/lpvm.pdf kanssa. Mutta minun täytyy myöntää että tämä kaikki tällainen on omaksi ilokseni.

**C:**

### Mitä "parempi käyttöliittymä" tarkoittaisi?

Käyttöliittymä on rajapinta kahden osapuolen välillä; "sisäinen vs ulkoinen" on vain kysymys siitä, ovatko osapuolet ihminen ja kone vai kaksi koneen osaa. Molemmissa tapauksissa rajapinta on protokolla: mitä saa lähettää, missä järjestyksessä, ja mikä on sen jälkeen mahdollista. Halu ei siis ole epämääräinen: se on halu tehdä protokollista eksplisiittisiä ja tarkistettavia. Se on täsmälleen se, mitä sessiotyypit ovat. Design 2 on sama halu kirjoitettuna logiikan kielelle.

"Parempi" tarkoittaa kolmea konkreettista asiaa: vähemmän tapoja tehdä virhe (tyyppi kieltää ne), vähemmän pidettävää päässä (tyyppi kertoo missä tilassa keskustelu on), ja enemmän tarkoitusta, joka säilyy rajan yli (tyyppi on spesifikaatio, ei kommentti). Osion 1 "why-kerros" asuu tässä.

### Mikä siitä on tarpeen?

Sinulle ei mikään. Alalle vähän. Rust otti ehkä 80 % lineaarisuuden käytännön hyödystä omistajuudella ilman logiikkaa, eikä loput 20 % ole ollut riittävä syy kenellekään rakentaa tuotantokieltä lineaarilogiikan päälle.

Missä se saattaisi tulla tarpeelliseksi: kun ohjelmia kirjoittaa malli eikä ihminen, spesifikaation on asuttava jossain, jonka kone tarkistaa, ja rajapinnat ovat paikka jossa virheet oikeasti syntyvät. Siinä maailmassa "protokolla tyyppinä" on yksi harvoista asioista, jotka skaalautuvat generoidun koodin määrän mukana. Tämä on veto, ei havainto.

### Design 2 ja LPVM-paperi

Paperin ydin: deterministinen, yksimoodinen logiikkaohjelma (Horn-lauseet) kääntäjän välikielenä koko käännösprosessin ajan. Argumentit jaetaan syötteisiin ja tuloksiin (`p(in; out)`), lohkojen tilalla on lauseet, hyppyjen tilalla proseduurikutsut, silmukoiden tilalla rekursio, ei φ-solmuja. Vahdit (guards) ovat lausekohtaisia ja niiden on oltava toisiaan täydentäviä ja tyhjentäviä, jotta täsmälleen yksi lause onnistuu eikä paluuhakua tarvita. Sivuvaikutukset mallinnetaan erillisellä tilamuuttujalla `st`, joka pujotetaan lauseesta toiseen (`st → st'`), jolloin puhtaat operaatiot voi järjestää uudelleen ja vaikutukselliset eivät. Proseduureilla voi olla useita tuloksia. Paperin esimerkki gcd yksinkertaistettuna:

```
gcd(a, b; ret) ← b ≠ 0 ∧ mod(a, b; b') ∧ gcd(b, b'; ret)
gcd(a, b; ret) ← b = 0 ∧ ret = a
```

Yhteys Design 2:een:

- `st → st'` -pujotus on lineaarinen resurssi, jota kohdellaan lineaarisesti pelkästään sopimuksen voimalla: käytetään kerran, saadaan uusi.
- Moodi (in/out) on degeneroitunut sessiotyyppi: protokolla, jossa on yksi viesti yhteen suuntaan. Sessiotyyppi on moodi, jolla on historia.
- Kun LP-muodon moodit yleistetään sessiotyypeiksi, saadaan Design 2:n välikieli: lauseet ovat prosesseja, argumentit kanavien päitä, ja `&`-valinnan tyhjentävyys on paperin vaatimus lauseiden vahtien täydentävyydestä.

Aiempi työ, joka kannattaa tuntea ennen rakentamista:

- Saraswat, Janus (1990): rinnakkainen logiikkakieli, jossa jokaisella muuttujalla on täsmälleen yksi kysyjä ja yksi kertoja (kaksipäinen kanava), tietoisesti lineaarilogiikan hengessä.
- Miller: Lolli ja Forum — lineaarilogiikan todistushaku ohjelmointina.
- Wadler: CP ("Propositions as Sessions"); Wadler & Lindley: GV; Caires & Pfenning: sessiotyypit ILL:n todistuksina; SILL, Rast.
- Lafont: lineaarinen abstrakti kone; interaktioverkot. HVM/Bend interaktioverkkojen tuotantoinstanssina.

Design 2:n "oikea VM" on olemassa palasina: LPVM antaa sekventiaalisen, determinististen lauseiden koneen, Janus kanavakurin, CP/GV tyyppijärjestelmän. Työ on liimata ne, ei keksiä.

### Konkreettinen minimipolku

1. Klassinen lineaarilogiikka rekursiivisilla sessiotyypeillä; ei polymorfismia aluksi.
2. Lähdemuoto on LP-lauseita, joissa argumentit on tyypitetty sessiotyypeillä; paperin `st` on vain yksi kanava muiden joukossa.
3. Determinismivaatimus säilytetään: `&`-valinnan jokaisesta haarasta täsmälleen yksi lause.
4. Ajoympäristö: korutiineja ja kaksipäisiä (SPSC) jonoja.
5. Virstanpylväs 1: paperin gcd ajaa.
6. Virstanpylväs 2: kahden osapuolen protokolla (esim. yllä oleva Bank/Client), jossa deadlock-vapaus tulee cutista ilmaiseksi.

Jos virstanpylväs 2 ei toteudu, koko juttu on jäänyt teoriaksi.

### Omaksi iloksi

Rehellinen syy, ja suurin osa tästä lajista työtä tehdään sillä syyllä. Mutta lause vapauttaa sekä siitä, että kukaan tarvitsisi tulosta, että siitä, että tulosta ylipäätään tulisi. Jälkimmäinen on ansa: ilo ilman määriteltyä valmista on ikuista suunnittelua. Määrittele valmis pieneksi ja ajettavaksi.

---

## 4. Päätös

**U:** Ok. Tehdään jotakin valmiiksi sitten.

Tämä tiedosto on tuon päätöksen konteksti. Seuraava askel on osion 3 minimipolun kohdat 1–5.
