# Question bank review

Reviewed 17 September 2026. Bank went from **589 → 799 items**: 2 duplicates
removed, 18 items rewritten, every answer key re-seated, and **212 new
questions** written.

---

## 1. Answer-key position bias — FIXED

The reported problem, confirmed and worse than a single-letter skew:

| | before (589 items) | after (799 items) |
| --- | --- | --- |
| A | 178 (30.2%) | 196 (24.5%) |
| **B** | **312 (53.0%)** | 201 (25.2%) |
| C | 71 (12.1%) | 207 (25.9%) |
| D | 28 (4.8%) | 195 (24.4%) |

A student who guessed B on everything scored 53%. D was effectively a dead
slot — 28 items out of 589.

**Fix** (`tools/rebalance.js`): every item's options are permuted so the key
lands on a target position assigned round-robin *within each domain*, so no
domain carries a positional tell of its own. The permutation is deterministic —
seeded from the question ID — so the bank rebuilds identically and diffs stay
reviewable. Two classes of item are excluded: the four with all-numeric options
(kept in ascending order, which is the reading convention; their keys fall
where they fall) and, before the shuffle, the 18 items in §2 that could not be
shuffled at all.

`tools/audit_bank.js` now fails the build if any letter exceeds 30% of keys, so
this cannot silently return.

---

## 2. Eighteen items rewritten

### 2a. Fourteen "All of the above" items

Every one of them sat at position D **and was the correct answer in every
case**. Free points, and prohibited by standard item-writing guidance. Rewritten
with real distractors. Several were also wrong on the merits:

- **q0196** asked which medication is "FDA-approved for MS-related fatigue" and
  keyed *All of the above*. **No drug is FDA-approved for MS fatigue.**
  Amantadine and modafinil are off-label; dalfampridine is approved to improve
  walking. The original rationale hedged with "off-label or FDA-approved,"
  which is not a thing. Rewritten so the correct answer is that none carry the
  indication — which is what matters for consent and for appeals.
- **q0114** keyed *All of the above* while its own rationale said
  non-pharmacologic management is first-line and the drugs are adjuncts. The
  key contradicted the rationale. Rewritten with the fatigue-management program
  as the key.
- **q0312** asked which symptom is *most* responsive to cooling and keyed *All
  of the above*. "Most" and "all" cannot both hold. Rewritten around Uhthoff
  phenomenon — heat-triggered fatigue and conduction-related weakness reverse
  on cooling; spasticity and bladder symptoms do not, reliably.
- **q0350** asked for the principal *international* ethics document and keyed
  *All of the above*, which swept in the Belmont Report and Common Rule — both
  US frameworks. Rewritten to the Declaration of Helsinki.
- **q0290** asked which requirement is *mandatory* for human-subjects research
  and keyed *All of the above*, including a data monitoring committee. DSMBs
  are not universally required. Rewritten to prospective IRB approval.
- **q0366** keyed *All of the above* for nocturnal painful spasms, listing
  cyclobenzaprine — indicated for acute musculoskeletal spasm, not spasticity of
  central origin, and it adds anticholinergic burden that is a real problem in
  MS. The rationale also discussed baclofen, which was not an option.
- **q0370** keyed *All of the above* for MS fatigue including methylphenidate.
  Rewritten around the honest answer: amantadine and modafinil, off-label,
  modest and inconsistent evidence, time-limited trial with a defined endpoint.
- **q0126** dropped *All of the above*; rewritten to test mechanism (baclofen
  as GABA-B agonist vs. tizanidine alpha-2 vs. dantrolene peripheral), which is
  the discriminating knowledge.
- q028, q0270, q0285, q0296, q0316, q0329 — rewritten with real distractors; no
  factual error in the originals beyond the option form.

### 2b. Four "Both A and C" items

These reference option letters, so shuffling would have produced nonsense —
and they are a prohibited form for the same reason. Two were also wrong:

- **q0379** gave the cladribine lymphocyte threshold as **1,000/mm³**. The
  label figure is **≥800 cells/mm³ before the Year 2 course**, with the course
  delayed up to six months for recovery. Worse, the item's "Both A and C"
  answer hinged on `<1000/mm³` and `<1000 ×10⁶/L` being the same number written
  two ways — that tests unit conversion, not cladribine. Rewritten to the
  correct threshold and the correct action.
- **q0383** asked which tool measures walking **capacity** and keyed *Both A
  and B*, while its own rationale said the 6-Minute Walk Test "specifically
  measures walking capacity." Key contradicted rationale. Rewritten with 6MWT
  as the key and T25FW, 9-HPT, and SDMT as distractors.
- q015 (PPI vs. H2 blocker for steroid gastric protection) and q0287
  (modifiable MS risk factors) — content was sound, option form was not.

---

## 3. Outstanding: the length cue is a bigger tell than the letter bias was

**In the original 587 items, the correct option is the longest option in 63%**
(chance is 25%). This survived the reshuffle because it is a property of how
the options are *written*, not where they sit.

This is the single largest remaining quality problem, and it is worth more to a
test-taker than knowing B was 53%. The pattern is the familiar one: the key
gets written as a complete, hedged, clinically careful sentence and the
distractors get written as curt wrong answers.

> "Age-appropriate language with caregiver involvement and honest, reassuring
> information about the illness" — vs. — "Keeping the diagnosis secret from the
> child"

No MS knowledge required.

Fixing it means rewriting distractors to comparable length and plausibility
across several hundred items — real work, not a script. `tools/audit_bank.js`
reports the percentage on every run and warns above 45%, so progress is
measurable.

**A gate now stops it getting worse.** `tools/add_questions.js` rejects any new
item whose key exceeds the longest distractor by both more than 15% and more
than 12 characters. Both tests must trip: a ratio alone misfires on short
one-word options ("Precontemplation" vs. "Maintenance" is not a cue), and an
absolute difference alone misfires when every option is long. The rule is
blunt but it bites — the first batch written for this pass had 26 of 50 items
rejected and rewritten before they were accepted.

Measured against that gate:

| | items | failing the gate | key is unique longest |
| --- | --- | --- | --- |
| pre-existing | 587 | 223 (38%) | 63.4% |
| added this pass | 212 | 3 (1.4%) | 58.5% |

The 223 pre-existing failures are the backlog. They are listed by running the
gate over the bank, and they are the highest-value content work remaining.

---

## 3a. The 212 new questions

Written to fill the thin domains and the thin easy tier, and to cover ground
the bank had little of — insurance and access mechanics in particular.

| Domain | before | after |
| --- | --- | --- |
| Assessment & Intervention | 340 | 430 |
| Concepts | 89 | 112 |
| Advocacy | 50 | 90 |
| Research | 53 | 87 |
| Education | 55 | 80 |

Easy-tier items went from 100 to 138, which matters because the app lets a
student filter to easy only and 100 items made for a thin pool.

New material covers: Medicare Part B versus Part D for infused versus
self-administered DMTs, step therapy and ERISA pre-emption, external review,
copay accumulators, white bagging and site-of-care exceptions, PAP versus
foundation grants and the Anti-Kickback exclusion for federal beneficiaries;
PML risk stratification and extended interval dosing, the monitoring
requirements for each DMT class, pregnancy and lactation, switching and
rebound; pseudo-relapse recognition, neurogenic bladder, dysphagia,
pseudobulbar affect, comorbidity; NfL, central vein sign, paramagnetic rim
lesions, OCT, AHSCT selection; study design, NNT and NNH, confidence
intervals, confounding by indication, equipoise, therapeutic misconception;
teach-back, health literacy, motivational interviewing, interpreter use.

**One deliberate omission: no question turns on a drug's current approval
status.** Tolebrutinib is the cautionary case — FDA priority review in early
2025, then a complete response letter for non-relapsing SPMS on 24 December
2025. An item keyed to an approval date is wrong within a year and there is no
mechanism to catch it. Questions are keyed to mechanism, monitoring, and
decision logic, which stay true. The About screen's content-review date is the
honest way to handle the rest.

## 4. Duplicates removed

- **q0151** — verbatim duplicate of q012 (identical stem apart from quote marks,
  identical options, identical key).
- **q0307** — duplicate of q049; both asked what distinguishes smoldering from
  active lesions, with the same key concept.

Three near-duplicate pairs were **kept** deliberately, because they test
different decisions off a shared clinical setup: q053/q0272 (steroid-refractory
relapse — next step vs. what indicates PLEX), q034/q0309 (unproven stem cell
therapy), q0194/q0389 (neurogenic bladder). The audit reports them as warnings
rather than failures for this reason.

---

## 5. Composition

| Domain | n | | Difficulty | n |
| --- | --- | --- | --- | --- |
| Assessment & Intervention | 430 | | easy | 138 |
| Concepts | 112 | | medium | 411 |
| Advocacy | 90 | | hard | 250 |
| Research | 87 | | | |
| Education | 80 | | | |

Clinical is 54% of the bank. Whether that is right depends on the certification
blueprint you are targeting — worth checking the published domain weights and
rebalancing the *counts*, since the app lets students filter by domain and a
thin domain gives a thin practice session.

---

## 6. Other findings, not blocking

- **ID padding is inconsistent** — `q001`…`q099` are 3-digit, `q0100`+ are
  4-digit. Cosmetic; IDs are opaque to the app. Left alone to keep the diff
  reviewable.
- **ID padding**: new items are `q0680` onward at consistent 4-digit width.
- **One option set is reused across four items** (q001, q002, q003, q0141 — the
  four MS phenotypes). Defensible for a phenotype drill, but a student sees the
  same four options repeatedly and starts pattern-matching.
- **Rationales never name an option letter** — checked, zero occurrences. This
  is what made the reshuffle safe.
