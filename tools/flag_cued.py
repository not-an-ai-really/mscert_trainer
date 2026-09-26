"""Dump the length-cue-flagged questions (audit_bank.py's rule) to a
readable worklist for the rewriting pass.

Usage:  python tools\\flag_cued.py [out.md]

Default out: tools\\cued_worklist.md
The flag rule is copied verbatim from audit_bank.py so the worklist is
exactly the set the audit warns about:
    key_len > second_longest * 1.15  AND  key_len - second_longest > 12
"""

import json
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def is_cued(q):
    opts = q.get("options") or []
    ca = q.get("correct_answer")
    if not isinstance(ca, int) or not (0 <= ca < len(opts)):
        return False
    lens = [len(o) for o in opts]
    key_len = lens[ca]
    second = max(l for i, l in enumerate(lens) if i != ca)
    return key_len > second * 1.15 and key_len - second > 12


def main():
    out = os.path.join(BASE, "tools", "cued_worklist.md")
    if len(sys.argv) > 1:
        out = sys.argv[1]
    with open(os.path.join(BASE, "questions_complete.json"), "r",
              encoding="utf-8") as fh:
        qs = json.load(fh)["questions"]
    cued = [q for q in qs if is_cued(q)]
    lines = [f"# Length-cue worklist ({len(cued)} questions)", ""]
    for q in cued:
        ca = q["correct_answer"]
        lines.append(f"### {q['id']} ({q.get('domain')} {q.get('subdomain')}, "
                     f"{q.get('difficulty')}) key={'ABCDE'[ca]}")
        lines.append(f"STEM: {q['stem']}")
        for i, o in enumerate(q["options"]):
            mark = "   <-- KEY" if i == ca else ""
            lines.append(f"{'ABCDE'[i]}: {o}   [{len(o)}]{mark}")
        lines.append(f"RATIONALE: {q['rationale']}")
        lines.append("")
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines))
    print(f"{len(cued)} flagged -> {out}")


if __name__ == "__main__":
    main()
