# MS-Cert Trainer — Publishing Guide (phone app)

Goal: get the 589-question PWA onto Jeff's phone as a real "app" —
icon on the home screen, launches full-screen, **works offline**, no
account, no PC needed after it's hosted once.

The app is packaged and checked:

```
phone-pwa\                <- the app (self-contained, no server required)
mscert-phone-pwa-v1.1.0.zip
check.bat                 <- one-command verification suite (all passing)
```

---

## How "app stores" actually work for this app

Because the trainer is a **PWA (Progressive Web App)**, the cleanest
"publishing" is **host the folder on any HTTPS web host, then install it
on the phone**. The phone's browser adds a home-screen icon, full-screen
launch, and offline support via the built-in service worker — no
developer accounts, no $-fees, no Mac, no code signing.

Real app stores are still possible (see the end), but they require paid
accounts and re-wrapping the app in a native shell, and they buy nothing
for a personal study tool.

| Route | Cost | Time on phone | Offline | Updates |
| --- | --- | --- | --- | --- |
| **A: Static host + home-screen install (recommended)** | $0 | ~20 min | Yes (after first load) | Re-upload folder; phone auto-updates on next open |
| **B: Temporary — just this PC, same WiFi** | $0 | 5 min | No | Just refresh |
| **C: Real app stores (Google Play / Apple)** | $25 once / $99 per year | 30-60 min | Yes | New upload per update |

---

## Option B first (do this today, no hosting at all)

1. On the PC, in `mscert\phone-pwa`, double-click **`start.bat`**.
2. It prints a `PHONE_URL` like `http://192.168.1.23:8080`.
3. On the phone (connected to the **same WiFi**), open that URL in
   Chrome/Safari.
4. Use it right away. Optionally: browser menu → **Add to Home Screen**
   (Android: "Install app") so it gets an icon.

Limitations: the PC must be on, and no offline mode (browsers only allow
the PWA service worker on HTTPS or `localhost`). That's why Option A is
the keeper.

---

## Option A — host once, own it forever (recommended)

### What you are uploading

**The contents** of `mscert\phone-pwa` (8 items):

```
index.html  sw.js  manifest.webmanifest  css\  js\  icons\
```

Do **not** upload the parent `mscert` folder, `tools`, or the zipped
bank — the app is already self-contained (the bank is embedded in
`js\bank.js`).

### A1. Netlify Drop (fastest, ~10 minutes)

1. In any browser: **https://app.netlify.com/drop**.
2. Create a free account (email or Google) and sign in.
3. Drag the **`phone-pwa` folder** onto the big drop zone.
   (If you don't want `/phone-pwa/` in the URL: temporarily copy the
   eight items above into a fresh empty folder and drag that folder's
   *contents* instead.)
4. Netlify publishes immediately and gives you a URL like
   `https://shiny-mousse-1234.netlify.app/`.
5. Open that URL **on your phone's browser** (any network).
6. **Android (Chrome):** menu (⋮) → **Install app** (or "Add to Home
   screen"). **iOS (Safari):** Share button → **Add to Home Screen**.
7. Tap the new **MS-Cert** icon. It launches full-screen. Close the
   browser, turn off WiFi, and open it again — it still works (offline
   cache).

Keep your Netlify account — that's how you update later
(deploy tab → drag the new folder) or delete the site.

### A2. GitHub Pages (most permanent, ~20 minutes)

1. Create a free account at **https://github.com** (if you don't have
   one).
2. Click **+ → New repository**. Name it e.g. `mscert`. **Public** works
   (the app code isn't sensitive — see the note about the bank below);
   click **Create repository**.
3. On the new repo page: **uploading an existing file** → drag the
   *contents* of `phone-pwa` in → **Commit changes**.
4. Repo menu → **Settings → Pages**. Under **Build and deployment →
   Source**: choose **Deploy from a branch**, branch `main`, folder
   `/ (root)` → **Save**.
5. Wait a minute; the page prints your URL:
   `https://<yourname>.github.io/mscert/`.
6. Open that URL on the phone and install (same steps as Netlify, 6-7).

Updating later: drag the new files into the repo (overwrite), commit —
the phone picks up the new version the next time it opens the app
(service worker cache bumps, see "Updating the app" below).

### A3. Cloudflare Pages (same idea, drag-and-drop)

`dash.cloudflare.com` → **Workers & Pages → Create → Pages → Upload** →
drag the folder → free `https://<name>.pages.dev` URL → install on the
phone exactly like A1.

### Privacy note (important)

Anyone who has the URL can open the app — including its embedded
question bank, which is your personal study material. If you'd rather
keep it private:

- **Easiest:** pick a long, random site name (e.g. on Netlify: site
  settings → change site name to something unguessable) and don't share
  the link.
- **Stronger:** put a password page in front (Netlify/Cloudflare both
  support basic auth on paid plans, or a 3-line login check in JS).
- For personal use, the random-name approach is enough.

---

## Updating the app after the question bank grows

On the PC:

```bat
cd C:\Users\Administrator\Documents\AgentWorkspace\files\mscert

rem 1. check the bank (must be 0 ERRORS)
python tools\audit_bank.py

rem 2. merge any new validated batch (see expansions\ for examples)
python tools\add_questions.py expansions\<new-batch>.json

rem 3. regenerate the embedded bank file
python tools\build_bank_js.py

rem 4. bump the cache version so phones replace the old bank
rem    — edit ONE number in phone-pwa\sw.js   (const VERSION = "v1.1.0")
rem    — edit the matching one in phone-pwa\js\app.js  (APP_VERSION)

rem 5. run the whole check suite (audit + PWA test + JS syntax + versions)
check.bat
```

Then re-upload the `phone-pwa` folder to your host (overwrite). The next
time the phone opens the app it downloads and caches the new version —
including the new questions — and shows the new count in the header.

---

## Option C — real app stores (only if you want to distribute it)

Requires wrapping the PWA in a native shell with **Capacitor**
(https://capacitorjs.com). Outline, not step-by-step, since it only
pays off if you're actually shipping to stores:

**Android (Google Play)**
1. Node.js installed. In a project folder: `npm init -y`
   then `npm i @capacitor/core @capacitor/cli`.
2. `npx cap init "MS-Cert Trainer" com.yourname.mscert --web-dir=phone-pwa`.
3. `npx cap add android` → `npx cap sync`.
4. `npx cap open android` (needs Android Studio) → Build → APK.
5. To distribute to others you must register a **Google Play developer
   account ($25 one-time)** and upload the AAB; for your own phone only,
   install the APK directly (Android: allow "install unknown apps").

**Apple (App Store)**
1. Same setup, then `npx cap add ios`.
2. Requires a **Mac** with Xcode; open `ios/App.xcworkspace`.
3. **Apple Developer Program costs $99/year**; sign the build, archive,
   upload via App Store Connect, pass the (light) review.

Store review for a personal medical-education app is generally light,
but Apple in particular dislikes apps that can look like copyrighted
study content — another reason to keep the hosted version personal.

---

## What to remember

- **The app has no server.** All 589 questions and all your progress
  live on the device; nothing is uploaded or tracked.
- **Offline works only on HTTPS hosts** (Netlify/GitHub Pages/Cloudflare
  all qualify — Option B on the LAN does not).
- **Progress is per-device** (localStorage). Reset it from the Home
  screen ("Reset progress" line) if you ever want a clean slate.
- The desktop trainer (`desktop-trainer\`) and web trainer
  (`web-trainer\`) both read the same `questions_complete.json`, so they
  automatically use the 589-question bank.
