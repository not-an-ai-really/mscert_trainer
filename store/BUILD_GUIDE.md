# Store build guide (phone-only)

Target: ship `phone-pwa/` as a native app to **App Store** and **Play Store**
via a Capacitor shell. Web/desktop builds are out of scope for the release,
but the app still runs as a PWA (the native calls no-op outside the shell).

## What was already done (code side)

- `package.json` + `capacitor.config.ts` at repo root (`webDir: phone-pwa`)
- `phone-pwa/js/app.js` — haptics on every answer (light tap, success/error),
  daily study-reminder toggle, next-morning "review your misses" nudge.
  All native calls feature-detected; web build unchanged.
- `phone-pwa/index.html` — loads `js/capacitor.js` (bridge), new reminder UI
- `phone-pwa/js/capacitor.js` — ships as a **~1 KB web stub** (`"MS-CERT-CAPACITOR-
  STUB"` marker) so the hosted PWA tree is self-contained: sw.js precaches it and
  a 404 there would abort service-worker install and kill offline mode
- `phone-pwa/sw.js` — v1.3.1, precaches `js/capacitor.js`
- `store/copy-native.js` — copies the core bridge JS into the web bundle,
  **overwriting the stub**, and sanity-checks the result
- Listings + review notes: `store/APPSTORE_LISTING.md`, `store/PLAYSTORE_LISTING.md`

## One-time setup (on the machine with Android Studio / Xcode)

```
npm install
node store/copy-native.js
npx cap add android
npx cap add ios
npx cap sync
```

Notes:
- `npx cap sync` copies `phone-pwa/` into `android/app/src/main/assets/public/`
  and `ios/App/App/public/`, and wires the `@capacitor/haptics` and
  `@capacitor/local-notifications` plugins into both native projects.
- Re-run `node store/copy-native.js && npx cap sync` after ANY web change.
- After `copy-native.js`, confirm `phone-pwa\js\capacitor.js` is the real
  bridge (tens of KB, prints its byte count) and NOT the ~1 KB stub —
  shipping the stub to a store build means no haptics/notifications, which
  is a silent regression.
- App ID: `com.notanai.mscerttrainer` (in `capacitor.config.ts`). If it's
  taken, change it BEFORE your first build/signing — not after.
- `android/` and `ios/` are git-ignored (see `.gitignore`); they are
  generated. Commit only the repo root files + `store/`.

## Android (Play Store)

1. `npx cap open android`
2. Android Studio: set `versionCode 1`, `versionName "1.0.0"` in
   `android/app/build.gradle` (default is fine).
3. Build > Generate Signed App Bundle(s) > AAB (Play requires AAB).
   Create a keystore if prompted; keep it safe — you need it for every update.
4. Play Console: create app (title/subtitle/description from
   `store/PLAYSTORE_LISTING.md`), fill Data safety (answers are written there),
   attach the AAB, submit.

## iOS (App Store)

1. `npx cap open ios`
2. Xcode: select `App` target > Signing & Capabilities > your Team.
   Bundle ID is pre-set to `com.notanai.mscerttrainer`.
   Version `1.0`, build `1`.
3. Build > Archive.
4. Distribute App > App Store Connect > upload.
5. App Store Connect: create app record with the listing from
   `store/APPSTORE_LISTING.md`, attach the build, **paste the App Review notes
   section verbatim** into the "App Review Information" > "Notes" field,
   submit for review.

## Pre-submit verification (do this on a real phone)

- [ ] Install from the device build, kill the app, turn on airplane mode,
      reopen → app opens, bank loads, full session completes.
- [ ] Tapping an answer gives haptic feedback; correct/incorrect feel
      different.
- [ ] Enable "Daily study reminder" → permission prompt appears →
      a notification fires at 09:00 (test with a shorter wait or by
      trusting the toggle state).
- [ ] Finish a session with misses → next morning 08:00 reminder exists.
- [ ] About screen shows "clinical content reviewed September 2026".
- [ ] Delete app → reinstall → progress is gone (clean state).

## Versioning

- Store version: 1.0 (build 1) for both.
- In-app `APP_VERSION` in `phone-pwa/js/app.js` is now `1.3.1`; bump it (and
  the matching `VERSION` in `phone-pwa/sw.js`) with every content/code pass
  and note it in release notes.
