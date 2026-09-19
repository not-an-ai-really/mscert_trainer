"""Applied to tools/audit_bank.py: add the two checks that would have caught
the answer-key bias and the length cue, and accept 4-digit IDs."""
import re, io, sys
p = sys.argv[1]
s = io.open(p, encoding="utf-8").read()

# 1. accept q0680-style 4-digit ids (the bank already had them from q0100 on)
s = s.replace('re.fullmatch(r"q\\d{3}", i or "")', 're.fullmatch(r"q\\d{3,4}", i or "")')
s = s.replace('re.fullmatch(r"q\\d{3}", q.get("id") or "")', 're.fullmatch(r"q\\d{3,4}", q.get("id") or "")')
s = s.replace('warnings.append(f"ids not matching qXXX format: {bad_ids[:20]}")',
              'warnings.append(f"ids not matching qXXX/qXXXX format: {bad_ids[:20]}")')

# 2. new checks, inserted just before the duplicate-stem block in audit()
anchor = """    dtext = collections.Counter(
        (q.get("stem") or "").strip().lower() for q in questions)"""
new = '''    # --- answer-key position balance -------------------------------------
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

''' + anchor
s = s.replace(anchor, new, 1)

# 3. report key distribution in the summary
s = s.replace('''    subs = collections.Counter(
        (q.get("domain"), q.get("subdomain")) for q in questions)''',
'''    keys = collections.Counter(
        q.get("correct_answer") for q in questions)
    total = len(questions) or 1
    out.append("answer-key distribution: " + "  ".join(
        f"{'ABCDE'[k] if isinstance(k, int) and 0 <= k < 5 else k}="
        f"{v} ({v / total:.1%})" for k, v in sorted(
            keys.items(), key=lambda kv: str(kv[0]))))
    subs = collections.Counter(
        (q.get("domain"), q.get("subdomain")) for q in questions)''', 1)

io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("audit_bank.py patched")
