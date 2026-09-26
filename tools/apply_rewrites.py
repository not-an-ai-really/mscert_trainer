"""Apply option rewrites (length-cue pass) to the canonical bank.

Usage:
    python tools\\apply_rewrites.py            # apply tools\\rewrites.json
    python tools\\apply_rewrites.py --check    # validate only, no write

rewrites.json shape:
    { "q007": ["new A", "new B", "new C", "new D"], ... }

Rules enforced per entry (rejects the whole file on any violation):
  - 4-5 non-empty options, pairwise distinct (strip/lower)
  - the question's correct_answer index stays valid
  - the length-cue flag (audit_bank.py rule) no longer trips
  - the correct option's text is unchanged OR its key position is
    unchanged (we never move the key, so position is constant)
"""

import json
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANK = os.path.join(BASE, "questions_complete.json")
REWRITES = os.path.join(BASE, "tools", "rewrites.json")


def is_cued(opts, ca):
    lens = [len(o) for o in opts]
    key_len = lens[ca]
    second = max(l for i, l in enumerate(lens) if i != ca)
    return key_len > second * 1.15 and key_len - second > 12


def main():
    check_only = "--check" in sys.argv
    with open(BANK, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    qs = data["questions"]
    by_id = {q["id"]: q for q in qs}

    with open(REWRITES, "r", encoding="utf-8") as fh:
        rw = json.load(fh)

    problems = []
    applied = 0
    for qid, opts in rw.items():
        q = by_id.get(qid)
        if q is None:
            problems.append(f"{qid}: not in bank")
            continue
        if not isinstance(opts, list) or not (4 <= len(opts) <= 5):
            problems.append(f"{qid}: needs 4-5 options, got "
                            f"{len(opts) if isinstance(opts, list) else type(opts)}")
            continue
        if any(not isinstance(o, str) or not o.strip() for o in opts):
            problems.append(f"{qid}: empty/non-string option")
            continue
        norm = {o.strip().lower() for o in opts}
        if len(norm) != len(opts):
            problems.append(f"{qid}: duplicate options")
            continue
        ca = q["correct_answer"]
        if not (0 <= ca < len(opts)):
            problems.append(f"{qid}: correct_answer {ca} out of range")
            continue
        if is_cued(opts, ca):
            lens = [len(o) for o in opts]
            problems.append(
                f"{qid}: STILL cued after rewrite "
                f"(lens={lens}, key={'ABCDE'[ca]})")
            continue
        if not check_only:
            q["options"] = opts
        applied += 1

    print(f"rewrites: {len(rw)} entries, {applied} valid")
    if problems:
        print("PROBLEMS:")
        for p in problems:
            print("  -", p)
        return 1
    if check_only:
        print("all rewrites valid (no write)")
        return 0

    with open(BANK, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"applied {applied} option rewrites -> {BANK}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
