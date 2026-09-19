"""Check version strings across the PWA and the generated bank stamp.

Usage:  python tools\\check_versions.py

Fails if the service-worker cache version and the app footer version
disagree (phones would silently keep a stale cache), or if bank.js
embeds a question count that does not match the canonical bank.
"""

import json
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PWA = os.path.join(BASE, "phone-pwa")
BANK = os.path.join(BASE, "questions_complete.json")

failures = []


def check(label, ok, detail=""):
    print(("  PASS  " if ok else "  FAIL  ") + label)
    if not ok:
        failures.append(label)
        if detail:
            print("         " + detail)


def main():
    sw = open(os.path.join(PWA, "sw.js"), encoding="utf-8").read()
    app = open(os.path.join(PWA, "js", "app.js"), encoding="utf-8").read()
    bank_js = open(os.path.join(PWA, "js", "bank.js"),
                   encoding="utf-8").read()

    m_sw = re.search(r'version\s*=\s*"(v?\d+\.\d+\.\d+)"', sw, re.I)
    m_app = re.search(r'APP_VERSION\s*=\s*"(\d+\.\d+\.\d+)"', app)
    check("sw.js has a VERSION constant", bool(m_sw))
    check("app.js has an APP_VERSION constant", bool(m_app))
    if m_sw and m_app:
        sw_v = m_sw.group(1).lstrip("v")
        app_v = m_app.group(1)
        check("versions agree (%s)" % sw_v,
              sw_v == app_v,
              "sw=%s app=%s" % (sw_v, app_v))

    m_bank = re.search(r'BANK_COUNT\s*=\s*(\d+)', bank_js)
    real = len(json.load(open(BANK, encoding="utf-8"))["questions"])
    check("BANK_COUNT in bank.js matches canonical bank (%d)" % real,
          bool(m_bank) and int(m_bank.group(1)) == real,
          "bank.js=%s canonical=%d" % (m_bank and m_bank.group(1), real))

    if failures:
        print("VERSION CHECK: FAILED")
        return 1
    print("VERSION CHECK: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
