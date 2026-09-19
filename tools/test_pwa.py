"""Smoke test for the MS-Cert phone PWA.

Usage:  python tools\test_pwa.py

Starts a local http.server on a free port, then:
  1. every asset (index, css, js, bank, manifest, sw, icons) returns 200
  2. js/bank.js parses and its questions match the canonical
     questions_complete.json exactly (ids, correct answers, domains)
  3. manifest.webmanifest parses; every referenced file exists
  4. index.html references every file the service worker precaches
Exits non-zero on any failure.
"""

import json
import os
import re
import socket
import sys
import threading
import urllib.request
from http.server import HTTPServer, SimpleHTTPRequestHandler

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PWA = os.path.abspath(os.path.join(BASE, "phone-pwa"))
BANK = os.path.abspath(os.path.join(BASE, "questions_complete.json"))

failures = []


def check(label, ok, detail=""):
    print(("  PASS  " if ok else "  FAIL  ") + label + (("  [" + detail + "]") if detail and not ok else ""))
    if not ok:
        failures.append(label)


def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def main():
    if not os.path.isdir(PWA):
        print("FAIL: phone-pwa folder missing")
        return 1
    handler = lambda *a, **k: SimpleHTTPRequestHandler(
        *a, directory=PWA, **k)
    port = free_port()
    srv = HTTPServer(("127.0.0.1", port), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    root = "http://127.0.0.1:%d" % port

    def get(path):
        with urllib.request.urlopen(root + "/" + path) as r:
            return r.status, r.read()

    assets = [
        "", "index.html", "css/app.css", "js/app.js", "js/bank.js",
        "sw.js", "manifest.webmanifest",
        "icons/icon-192.png", "icons/icon-512.png",
    ]
    print("== fetch assets")
    bodies = {}
    for a in assets:
        try:
            status, body = get(a)
            check("GET /%s -> 200" % (a or "index"), status == 200,
                  "status=%s" % status)
            bodies[a] = body
        except Exception as e:
            check("GET /%s" % a, False, str(e))

    print("== bank.js vs canonical bank")
    bank = json.load(open(BANK, encoding="utf-8"))["questions"]
    raw = bodies.get("js/bank.js", b"").decode("utf-8", "replace")
    m = re.search(r"const QUESTION_BANK = (\[.*\]);", raw, re.S)
    check("QUESTION_BANK array found in bank.js", bool(m))
    if m:
        try:
            embedded = json.loads(m.group(1))
            check("embedded question count",
                  len(embedded) == len(bank),
                  "embedded=%d canonical=%d" % (len(embedded), len(bank)))
            eids = {q["id"] for q in embedded}
            cids = {q["id"] for q in bank}
            check("id sets identical", eids == cids,
                  "only-embedded=%s only-canonical=%s" % (
                      sorted(eids - cids)[:5], sorted(cids - eids)[:5]))
            same = all(
                a["correct_answer"] == b["correct_answer"]
                and a["domain"] == b["domain"]
                and a["options"] == b["options"]
                for a, b in zip(
                    sorted(embedded, key=lambda q: q["id"]),
                    sorted(bank, key=lambda q: q["id"]))
            ) if len(embedded) == len(bank) else False
            check("answers/domains/options identical", same)
            opts_ok = all(
                4 <= len(q["options"]) <= 5
                and 0 <= q["correct_answer"] < len(q["options"])
                and len(set(q["options"])) == len(q["options"])
                for q in embedded)
            check("every embedded question well-formed", opts_ok)
        except json.JSONDecodeError as e:
            check("bank.js is valid JSON payload", False, str(e))
    check("bank.js is pure ASCII (safe on any server)", raw.isascii())

    print("== manifest")
    man_raw = bodies.get("manifest.webmanifest", b"")
    try:
        man = json.loads(man_raw)
        check("manifest has name + start_url + icons",
              bool(man.get("name") and man.get("start_url")
                   and man.get("icons")))
        for ic in man.get("icons", []):
            p = ic["src"]
            check("icon exists: %s" % p, os.path.isfile(
                os.path.join(PWA, p)))
    except json.JSONDecodeError as e:
        check("manifest is valid JSON", False, str(e))

    print("== cross-references")
    html = bodies.get("index.html", b"").decode("utf-8", "replace")
    sw = bodies.get("sw.js", b"").decode("utf-8", "replace")
    for ref in re.findall(r'href="([^"]+)"|src="([^"]+)"', html):
        p = next(t for t in ref if t)
        if p.startswith(("http", "data:")):
            continue
        check("index.html ref exists: %s" % p,
              os.path.isfile(os.path.join(PWA, p)))
    pm = re.search(r"const PRECACHE = \[(.*?)\];", sw, re.S)
    check("sw.js has a PRECACHE list", bool(pm))
    if pm:
        entries = re.findall(r'"([^"]+)"', pm.group(1))
        for p in entries:
            q = p[2:] if p.startswith("./") else p
            if not q:
                q = "index.html"
            check("precache entry exists: %s" % p,
                  os.path.isfile(os.path.join(PWA, q)))
        # sw.js is intentionally not in its own PRECACHE (the browser
        # registers it directly; self-precaching is redundant)
        for a in ("index.html", "css/app.css", "js/app.js", "js/bank.js",
                  "manifest.webmanifest"):
            check("precached: %s" % a,
                  ('"%s"' % a) in pm.group(1))

    print("== app.js sanity")
    app = bodies.get("js/app.js", b"").decode("utf-8", "replace")
    for token in ("QUESTION_BANK", "registerSW", "PROGRESS_KEY",
                  "renderResults", "startQuiz"):
        check("app.js references %s" % token, token in app)
    check("app.js uses no eval()", "eval(" not in app)
    check("no external http(s) script/font includes (offline-safe)",
          not re.search(r'(src|href)="https?://', html))

    srv.shutdown()
    print()
    if failures:
        print("PWA TEST: %d FAILURES" % len(failures))
        for f in failures:
            print("  -", f)
        return 1
    print("PWA TEST: ALL PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
