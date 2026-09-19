# MS-Cert Trainer — phone app (PWA)

A fully client-side, installable, **offline-capable** web app for practicing
the MS-Cert question bank. No account, no server at runtime — the entire
799-question bank ships inside the app and all progress stays on the device.

| | |
| --- | --- |
| Bank source | `../tools/questions.json` (compiled into `js/bank.js` at build time) |
| Requirements | Any modern phone browser (iOS Safari / Android Chrome). Node for the build tools |
| Build | `node ../tools/build_bank.js` from the repo root |

## Use it on your phone

### Option A — from this PC (immediate, same WiFi)

1. Run **`../tools/serve-local.bat`**.
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

Edit `../tools/questions.json`, or append a batch with the helper, then
rebuild:

```bash
node tools/add_questions.js batch.json   # optional: append + validate new items
node tools/audit_bank.js                 # quality gate; non-zero exit on defects
node tools/build_bank.js                 # regenerate js/bank.js, bump sw VERSION
```

`build_bank.js` bumps the service worker `VERSION` itself, so installed phones
pick up the new bank on next load. Bump `CONTENT_REVIEWED` in `js/app.js`
whenever clinical content is reviewed — it is shown on the About screen.

Do not hand-edit `js/bank.js`; it is generated and will be overwritten.
