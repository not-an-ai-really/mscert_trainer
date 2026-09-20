"""Rebuild the versioned production zip (mscert-phone-pwa-vX.Y.Z.zip).

Usage:  python tools\\make_zip.py

Reads APP_VERSION from phone-pwa/js/app.js so the zip name always matches
the in-app version, then zips the self-contained phone-pwa/ tree (same
`phone-pwa/`-prefixed layout the hosted build expects). Run it after
check.bat passes; commit the new zip and `git rm` the old one together.
"""

import os
import re
import sys
import zipfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    app = open(os.path.join(BASE, "phone-pwa", "js", "app.js"),
               encoding="utf-8").read()
    m = re.search(r'APP_VERSION\s*=\s*"(\d+\.\d+\.\d+)"', app)
    if not m:
        print("cannot find APP_VERSION in phone-pwa/js/app.js")
        return 1
    ver = m.group(1)
    out = os.path.join(BASE, "mscert-phone-pwa-v%s.zip" % ver)
    src_root = os.path.join(BASE, "phone-pwa")

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("phone-pwa/", "")
        for r, ds, fs in os.walk(src_root):
            ds.sort()
            fs.sort()
            rel_dir = os.path.relpath(r, BASE).replace(os.sep, "/")
            if rel_dir != "phone-pwa":
                z.writestr(rel_dir + "/", "")
            for f in fs:
                p = os.path.join(r, f)
                z.write(p, (os.path.relpath(p, BASE)).replace(os.sep, "/"))

    print("wrote", out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
