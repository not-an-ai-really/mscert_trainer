"""Merge validated question batches into the canonical bank.

Usage:  python tools\add_questions.py <batch.json> [<batch2.json> ...]

Each batch file: {"batch": str, "source": str, "questions": [ ... ]} with
questions using exactly the canonical 7-key schema.

The tool refuses to merge unless every new question passes validation:
required keys present (no extras), q+digit id, unique against the bank
and within the batch, valid domain/difficulty, 4-5 unique non-empty
options, correct_answer in range, non-empty stem/rationale, and no
duplicate stem text against the existing bank.

On success the union is written back to questions_complete.json sorted by
numeric id (2-space indent, UTF-8). Idempotent: re-merging an already
merged batch is rejected on duplicate ids.
"""

import json
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANK = os.path.join(BASE, "questions_complete.json")

REQUIRED_KEYS = {"id", "domain", "subdomain", "difficulty", "stem",
                 "options", "correct_answer", "rationale"}
VALID_DOMAINS = {"conceptual", "clinical", "advocacy", "education", "research"}
VALID_DIFFICULTIES = {"easy", "medium", "hard"}


def validate(q, seen_ids, seen_stems):
    problems = []
    qid = q.get("id", "<no-id>")
    keys = set(q.keys())
    if keys != REQUIRED_KEYS:
        problems.append(f"{qid}: keys {sorted(keys)} != canonical schema")
    if not re.fullmatch(r"q\d{3,}", qid or ""):
        problems.append(f"{qid}: id not q+numeric")
    if qid in seen_ids:
        problems.append(f"{qid}: id already in bank or this batch")
    dom = q.get("domain")
    if dom not in VALID_DOMAINS:
        problems.append(f"{qid}: unknown domain {dom!r}")
    if q.get("difficulty") not in VALID_DIFFICULTIES:
        problems.append(f"{qid}: unknown difficulty {q.get('difficulty')!r}")
    # subdomain section numbers: conceptual 1.x, clinical 2.x, advocacy
    # 3.x, education 4.x, research 5.x
    section = {"conceptual": "1.", "clinical": "2.", "advocacy": "3.",
               "education": "4.", "research": "5."}.get(dom)
    if section and not str(q.get("subdomain", "")).startswith(section):
        problems.append(
            f"{qid}: subdomain {q.get('subdomain')!r} not in section "
            f"{section!r} for domain {dom!r}")
    stem = (q.get("stem") or "").strip()
    if not stem:
        problems.append(f"{qid}: empty stem")
    elif stem.lower() in seen_stems:
        problems.append(f"{qid}: stem duplicates an existing question")
    opts = q.get("options") or []
    if not (4 <= len(opts) <= 5):
        problems.append(f"{qid}: {len(opts)} options (need 4-5)")
    elif len({o.strip().lower() for o in opts}) != len(opts):
        problems.append(f"{qid}: duplicate or empty options")
    ca = q.get("correct_answer")
    if not isinstance(ca, int) or not (0 <= ca < len(opts)):
        problems.append(f"{qid}: correct_answer {ca!r} out of range")
    if not (q.get("rationale") or "").strip():
        problems.append(f"{qid}: empty rationale")
    if not problems:
        seen_ids.add(qid)
        seen_stems.add(stem.lower())
    return problems


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    data = json.load(open(BANK, encoding="utf-8"))
    bank = data["questions"]
    seen_ids = {q["id"] for q in bank}
    seen_stems = {(q.get("stem") or "").lower() for q in bank}
    before = len(bank)

    all_problems = []
    added = []
    for path in sys.argv[1:]:
        batch = json.load(open(path, encoding="utf-8"))
        qs = batch.get("questions", [])
        batch_problems = []
        for q in qs:
            p = validate(q, seen_ids, seen_stems)
            batch_problems.extend(p)
            if not p:
                added.append(q)
        if batch_problems:
            all_problems.extend(batch_problems)
            print(f"REJECTED {os.path.basename(path)}: "
                  f"{len(batch_problems)} problem(s)")
        else:
            print(f"VALID  {os.path.basename(path)}: {len(qs)} questions "
                  f"({batch.get('source', 'no source note')[:70]})")

    if all_problems:
        print("\nNOTHING MERGED - fix the problems above and re-run:")
        for p in all_problems:
            print("  -", p)
        return 1

    bank.extend(added)
    bank.sort(key=lambda q: int(q["id"][1:]))
    tmp = BANK + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    os.replace(tmp, BANK)
    print(f"\nMERGED {len(added)} questions: {before} -> {len(bank)} "
          f"(max id q{max(int(q['id'][1:]) for q in bank)})")
    print("Next steps: python tools\\audit_bank.py  "
          "python tools\\build_bank_js.py  python tools\\test_pwa.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
