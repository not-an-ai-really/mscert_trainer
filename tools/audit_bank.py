"""Audit the MS-Cert question bank (questions_complete.json).

Usage:
    python tools\audit_bank.py [path-to-json]

Checks:
  - JSON shape: top-level {"questions": [...]}, each question's fields
  - unique IDs, ID range, sequential gaps
  - id -> domain consistency (each domain's block is contiguous)
  - correct_answer is an int within range of options
  - 4-5 non-empty, pairwise-distinct options per question
  - non-empty stem / rationale
  - no duplicate stem text (exact, case-insensitive)
  - domain and difficulty values match the taxonomy
  - subdomain belongs to its domain

Prints a human-readable report; exits 1 if any ERROR-level issue found
(warnings do not fail the run).
"""

import collections
import json
import os
import re
import sys

VALID_DOMAINS = {"conceptual", "clinical", "advocacy", "education", "research"}
VALID_DIFFICULTIES = {"easy", "medium", "hard"}

# expected subdomain prefixes per domain (taxonomy doc, numbered sections)
SUBDOMAIN_PREFIX = {
    "conceptual": ("1.",),
    "clinical": ("2.",),
    "advocacy": ("3.",),
    "education": ("4.",),
    "research": ("5.",),
}


def load(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def audit(questions):
    errors, warnings = [], []

    ids = [q.get("id") for q in questions]
    dupes = [k for k, v in collections.Counter(ids).items() if v > 1]
    if dupes:
        errors.append(f"duplicate ids: {dupes}")

    bad_ids = [i for i in ids if not re.fullmatch(r"q\d{3,4}", i or "")]
    if bad_ids:
        warnings.append(f"ids not matching qXXX/qXXXX format: {bad_ids[:20]}")

    nums = []
    for i in ids:
        if re.fullmatch(r"q\d{3,4}", i or ""):
            nums.append(int(i[1:]))
    if nums:
        missing = sorted(set(range(min(nums), max(nums) + 1)) - set(nums))
        if missing:
            # report compactly: ranges
            ranges, start, prev = [], missing[0], missing[0]
            for n in missing[1:]:
                if n == prev + 1:
                    prev = n
                else:
                    ranges.append((start, prev))
                    start = prev = n
            ranges.append((start, prev))
            compact = ", ".join(
                f"{a}-{b}" if a != b else str(a) for a, b in ranges)
            warnings.append(f"ID gaps ({len(missing)} ids: {compact[:400]})")

    for q in questions:
        qid = q.get("id", "<no-id>")
        dom = q.get("domain")
        if dom not in VALID_DOMAINS:
            errors.append(f"{qid}: unknown domain {dom!r}")
        if q.get("difficulty") not in VALID_DIFFICULTIES:
            errors.append(f"{qid}: unknown difficulty {q.get('difficulty')!r}")
        sub = str(q.get("subdomain", ""))
        if dom in SUBDOMAIN_PREFIX and not sub.startswith(SUBDOMAIN_PREFIX[dom]):
            errors.append(
                f"{qid}: subdomain {sub!r} does not belong to domain {dom!r}")
        stem = (q.get("stem") or "").strip()
        if not stem:
            errors.append(f"{qid}: empty stem")
        opts = q.get("options") or []
        if not (4 <= len(opts) <= 5):
            errors.append(f"{qid}: has {len(opts)} options (need 4-5)")
        elif len({o.strip().lower() for o in opts}) != len(opts):
            errors.append(f"{qid}: options contain duplicates/empties")
        ca = q.get("correct_answer")
        if not isinstance(ca, int) or not (0 <= ca < len(opts)):
            errors.append(
                f"{qid}: correct_answer {ca!r} out of range for "
                f"{len(opts)} options")
        if not (q.get("rationale") or "").strip():
            errors.append(f"{qid}: empty rationale")

    # --- answer-key position balance -------------------------------------
    # The bank was once 53% B / 4.8% D, which nothing here caught. A student
    # guessing the modal letter scored 53%. Fail above 30% for any position.
    n = len(questions)
    if n:
        keys = collections.Counter(
            q.get("correct_answer") for q in questions
            if isinstance(q.get("correct_answer"), int))
        for pos, count in sorted(keys.items()):
            share = count / n
            label = "ABCDE"[pos] if 0 <= pos < 5 else str(pos)
            if share > 0.30:
                errors.append(
                    f"answer-key skew: {label} is {share:.1%} of keys "
                    f"({count}/{n}); cap is 30%")
            elif share < 0.18:
                warnings.append(
                    f"answer-key thin: {label} is only {share:.1%} of keys "
                    f"({count}/{n})")

    # --- option length cue -----------------------------------------------
    # The strongest remaining test-wiseness tell: the key written as a full
    # hedged sentence beside curt distractors. Both tests must trip, so short
    # one-word options ("Precontemplation" vs "Maintenance") do not misfire.
    cued = []
    for q in questions:
        opts = q.get("options") or []
        ca = q.get("correct_answer")
        if not isinstance(ca, int) or not (0 <= ca < len(opts)):
            continue
        lens = [len(o) for o in opts]
        key_len = lens[ca]
        second = max(l for i, l in enumerate(lens) if i != ca)
        if key_len > second * 1.15 and key_len - second > 12:
            cued.append(q.get("id"))
    if cued:
        share = len(cued) / n if n else 0
        msg = (f"length cue: correct option conspicuously longest in "
               f"{len(cued)} items ({share:.1%}) -> {cued[:8]}")
        (errors if share > 0.45 else warnings).append(msg)

    dtext = collections.Counter(
        (q.get("stem") or "").strip().lower() for q in questions)
    dup_stems = [k[:60] + "..." for k, v in dtext.items() if v > 1 and k]
    if dup_stems:
        errors.append(f"duplicate stems: {len(dup_stems)} -> {dup_stems[:5]}")

    return errors, warnings


def summarize(questions):
    out = []
    out.append(f"Total questions: {len(questions)}")
    for level, field in (("domain", "domain"), ("difficulty", "difficulty")):
        c = collections.Counter(q.get(field) for q in questions)
        out.append(f"{level}: " + ", ".join(
            f"{k}={v}" for k, v in sorted(c.items())))
    # id block per domain
    blocks = collections.defaultdict(list)
    for q in questions:
        if re.fullmatch(r"q\d{3,4}", q.get("id") or ""):
            blocks[q["domain"]].append(int(q["id"][1:]))
    out.append("id blocks per domain:")
    for d in sorted(blocks):
        n = sorted(blocks[d])
        out.append(f"  {d:11s} n={len(n):3d}  min=q{n[0]:03d}  max=q{n[-1]:03d}")
    keys = collections.Counter(
        q.get("correct_answer") for q in questions)
    total = len(questions) or 1
    out.append("answer-key distribution: " + "  ".join(
        f"{'ABCDE'[k] if isinstance(k, int) and 0 <= k < 5 else k}="
        f"{v} ({v / total:.1%})" for k, v in sorted(
            keys.items(), key=lambda kv: str(kv[0]))))
    subs = collections.Counter(
        (q.get("domain"), q.get("subdomain")) for q in questions)
    out.append("subdomain counts:")
    for (d, s), n in sorted(subs.items(), key=lambda kv: (str(kv[0][0]), kv[0][1])):
        out.append(f"  {d:11s} {s:8s} {n}")
    return "\n".join(out)


def main():
    default = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "questions_complete.json")
    path = sys.argv[1] if len(sys.argv) > 1 else default
    if not os.path.isfile(path):
        print(f"ERROR: file not found: {path}")
        return 2
    data = load(path)
    if not isinstance(data, dict) or not isinstance(data.get("questions"), list):
        print("ERROR: expected top-level object with a 'questions' list")
        return 2
    qs = data["questions"]

    print(f"== audit: {path}")
    print(summarize(qs))
    errors, warnings = audit(qs)
    print(f"\nERRORS: {len(errors)}")
    for e in errors:
        print("  ERROR", e)
    print(f"WARNINGS: {len(warnings)}")
    for w in warnings:
        print("  WARN ", w)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
