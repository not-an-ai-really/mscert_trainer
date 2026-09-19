# Question Bank Numbering System

## Current Issues
- ID numbering has gaps: q008 jumps to q014 (missing q009-q013)
- Duplicate IDs present: q043 appears twice in advocacy domain
- Metadata counts mismatch actual question count (91 vs 500)

## Proposed System

### Base Format
`qXXX` where XXX is three-digit sequential number

### Domain-Based Segmentation
- conceptual: q001-q099 (100 questions)
- clinical: q101-q299 (200 questions)
- advocacy: q301-q399 (100 questions)
- education: q401-q499 (100 questions)
- research: q501-q599 (100 questions)

### Subdomain within Domain
- Conceptual 1.1: q001-q029
- Conceptual 1.2: q030-q049
- Conceptual 1.3: q050-q079
- Conceptual 1.4: q080-q099

### Difficulty within Subdomain
- Easy questions start numbering in subdomain range
- Medium questions continue sequence
- Hard questions finish sequence

### New Question Generation
- Always use next available sequential ID in domain
- Never reuse IDs or skip numbers intentionally
- Update metadata after each addition

## Status (verified 2026-09-07, `tools\audit_bank.py`)

- **510 questions**, 0 audit errors.
- IDs q001-q0600 with **gaps where questions were removed** — gaps are
  historical and must NOT be closed by renumbering (existing references
  would break). **Next free ID: q0601.**
- The 3-digit `qXXX` format below predates bank growth: **q0100 and up
  use a 4th digit** (e.g. `q0475`). The audit flags these as warnings by
  design — treat as informational.
- The domain-segmented ID ranges above (conceptual q001-q099 etc.) were a
  proposal that was **never applied**: early 3-digit IDs are mixed across
  domains. The 4-digit era (q0100+) is roughly domain-ordered
  (advocacy ~q046x, education/research ~q047x-q0600) but is not a hard
  guarantee. Do not re-segment.
- Fixed in this verification pass: q050 had option A duplicated as option
  D (replaced with a true distractor); q0475-q0480 carried bare subdomain
  "5" (assigned 5.1/5.2/5.3 per the bank's established 5.x usage).

---

*Created for consistent question bank maintenance. Verified 2026-09-07.*