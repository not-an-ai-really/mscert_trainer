# MS-Cert Trainer — phone app (PWA)

A fully client-side, installable, **offline-capable** web app (PWA) for
practicing the MS-Cert question bank. No account, no server needed at
runtime — the entire 510-question bank ships inside the app and all
progress is stored on the device.

| | |
| --- | --- |
| Bank source | `..\questions_complete.json` (embedded into `js\bank.js` at build time) |
| Requirements | Any modern phone browser (iOS Safari / Android Chrome). Python only needed for the LAN server below |
| Build steps | `python ..\tools\build_bank_js.py` then `python ..\tools\make_icons.py` |

## Use it on your phone

### Option A — from this PC (immediate, same WiFi)

1. Double-click **`start.bat`** (in this folder).
2. The printed `PHONE_URL` (e.g. `http://192.168.1.23:8080`) — open it in
   the phone's browser while on the same network.
3. Browser menu → **Add to Home Screen** (iOS: Share → Add to Home
   Screen; Android: menu → Install app / Add to Home screen).

Works while the PC is on, but not offline (browsers only allow
install/offline PWA features over HTTPS or localhost).

### Option B — host once, own it forever (recommended)

Host this folder on any free static host with HTTPS, then install it as
an app on the phone — **fully offline, no PC involved afterwards**.
Step-by-step options (Netlify Drop / GitHub Pages / Cloudflare Pages)
are in `..\publishing-guide.md`.

## Features

- **Sessions**: mix by domain (clinical, concepts, advocacy, education,
  research) and difficulty; 5–50 questions per session.
- **Instant feedback**: one tap answers; correct option highlighted,
  full rationale shown.
- **Results**: score ring, per-domain breakdown, **Review misses** to
  re-quiz exactly the questions you got wrong.
- **Lifetime progress** on-device: overall accuracy, answers, weakest
  domain; "Reset progress" in the footer of the home screen.
- **Offline**: service worker precaches the whole app (only active on
  HTTPS / localhost origins).

## Update the question bank

```bat
python ..\tools\audit_bank.py      :: 1. check the bank (tools at mscert root)
python ..\tools\build_bank_js.py   :: 2. regenerate js\bank.js
edit sw.js: bump VERSION           :: 3. bump the cache version
python ..\tools\make_icons.py      :: 4. (only if icon art changed)
```

Then re-host / re-open — the new cache version replaces the old one on
the phone automatically.
