"""One-off fixes for audit findings in questions_complete.json.

Fixes applied (2026-09-07):
  1. q050 (conceptual 1.4): options[0] and options[3] were identical
     ("It correlates with cortical lesion formation and neurodegeneration").
     Replaced the duplicate options[3] with a plausible distractor.
  2. Six research questions (q0475-q0480) carried the bare subdomain "5".
     Assigned proper 5.x subdomains following the bank's established
     usage (5.1 design/methodology, 5.2 ethics & consent, 5.3 evidence
     levels / EBP integration):
       q0475 RCT gold standard            -> 5.1
       q0476 informed consent / autonomy  -> 5.2
       q0477 external validity            -> 5.1
       q0478 EBP evidence hierarchy       -> 5.3
       q0479 purpose of blinding          -> 5.1
       q0480 integrating multiple studies -> 5.3

Idempotent: re-running makes no further changes.
"""

import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANK = os.path.join(BASE, "questions_complete.json")

RESEARCH_SUBDOMAIN = {
    "q0475": "5.1",
    "q0476": "5.2",
    "q0477": "5.1",
    "q0478": "5.3",
    "q0479": "5.1",
    "q0480": "5.3",
}

REPLACEMENT_DISTRACTOR = (
    "It is the primary driver of demyelination in the spinal cord")


def main():
    with open(BANK, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    changed = []
    for q in data["questions"]:
        if q["id"] == "q050" and len(set(q["options"])) != len(q["options"]):
            # keep the correct option (index 0) and repair the duplicate slot
            seen = []
            for i, opt in enumerate(q["options"]):
                if opt in seen:
                    q["options"][i] = REPLACEMENT_DISTRACTOR
                    changed.append(f"q050: replaced duplicated option {i}")
                else:
                    seen.append(opt)
        elif q["id"] in RESEARCH_SUBDOMAIN:
            want = RESEARCH_SUBDOMAIN[q["id"]]
            if q["subdomain"] != want:
                q["subdomain"] = want
                changed.append(f"{q['id']}: subdomain -> {want}")
    if changed:
        tmp = BANK + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        os.replace(tmp, BANK)
    for line in changed:
        print("FIXED", line)
    if not changed:
        print("nothing to fix (already clean)")


if __name__ == "__main__":
    main()
