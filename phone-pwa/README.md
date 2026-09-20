# MS-Cert Trainer — phone app (PWA)

A fully client-side, installable, **offline-capable** web app for practicing
the MS-Cert question bank. No account, no server at runtime — the entire
799-question bank ships inside the app and all progress stays on the device.

| | |
| --- | --- |
| Bank source | `../questions_complete.json` (compiled into `js/bank.js` at build time) |
| Requirements | Any modern phone browser (iOS Safari / Android Chrome). Python 3 for the build tools |
| Build | `python tools\build_bank_js.py` from the repo root |

## Use it on your phone

### Option A — from this PC (immediate, same WiFi)

1. Run **`../start-local-server.bat`** from the repo root.
2. Open the printed `PHONE_URL` (e.g. `http://192.168.1.23:8080`) on the phone,
   on the same network.
3. Browser menu → **Add to Home Screen** (iOS: Share → Add to Home Screen;
   Android: menu → Install app).

Works while the PC is on, but not offline — browsers only enable install and
offline features over HTTPS or localhost. This serves the folder to the whole
LAN, so use it at home rather than on a work network.

### Option B — host once (recommended)

Host `phone-pwa/` on any static host with HTTPS, then install it from the
phone — fully offline afterwards, no PC involved. See `../DEPLOYMENT.md` for
the response headers to set, and `../STORE_REVIEW.md` for what app-store
submission would additionally require.

## Features

- **Sessions**: mix by domain (clinical, concepts, advocacy, education,
  research) and difficulty; 5–50 questions per session.
- **Instant feedback**: one tap to answer; correct option highlighted, full
  rationale shown.
- **Results**: score ring, per-domain breakdown, **Review misses** to re-quiz
  exactly what you got wrong.
- **Lifetime progress** on-device: overall accuracy, answers, weakest domain.
- **About & disclaimer**: scope, non-affiliation, privacy, content review date.
- **Offline**: the service worker precaches the whole app (HTTPS / localhost
  origins only).

## Privacy

Nothing is collected. No accounts, no analytics, no advertising, no
third-party code, no network requests after install. Progress lives in this
device's local storage and nowhere else. See `../PRIVACY.md`.

## Update the question bank

Append a validated batch (see `../expansions\` for format), regenerate, and
bump versions — all from the repo root:

```bat
python tools\add_questions.py expansions\<new-batch>.json   rem validate + merge
python tools\build_bank_js.py    rem regenerate js/bank.js (BANK_COUNT included)
rem bump the cache version so phones replace the old bank:
rem   phone-pwa\sw.js  const VERSION = "vX.Y.Z"
rem   phone-pwa\js\app.js  APP_VERSION
check.bat    rem full audit + smoke test + syntax + version consistency
```

The service worker `VERSION` bump (not the build script) is what makes
installed phones pick up the new bank on next load. Bump
`CONTENT_REVIEWED` in `js/app.js` whenever clinical content is reviewed
— it is shown on the About screen.

Do not hand-edit `js/bank.js` or `js/capacitor.js`; `bank.js` is generated
and `capacitor.js` is a stub that store builds replace with the real bridge.
