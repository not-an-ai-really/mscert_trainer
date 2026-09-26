# MSRN Exam Prep — things only Jeff can do

Everything code-side is built, checked (`check.bat` all green) and pushed to
GitHub (`not-an-ai-really/mscert_trainer`, commit `db37005`, v1.3.1). The
items below need Jeff's accounts, hands, or a decision. Nothing here blocks
using the app.

## Route A — phone app via free static host (recommended, ~20 min, $0)

- [ ] **Create a free hosting account** — https://app.netlify.com/drop
      (or Cloudflare Pages / GitHub Pages). I can't sign up with his email.
- [ ] **Upload**: drag the **contents of `phone-pwa\`** onto the drop zone
      (or unpack `mscert-phone-pwa-v1.3.1.zip` first; it unpacks to
      `phone-pwa/`, so drag what's *inside* that folder).
      Optional hardening: add the `_headers` block from `DEPLOYMENT.md`.
- [ ] **Pick an unguessable site name** in host settings — the app (and its
      question bank) is personal study material; only the URL is the key.
- [ ] **On the phone**: open the host URL → browser menu →
      *Add to Home Screen* / *Install app* → run one session →
      airplane-mode test (close app, kill, reopen — it must still load;
      that exercises the offline cache).

## Route C — real app stores (agreed path 2026-09-22: both stores, standalone)

- [ ] **Android**: Google Play Console account ($25 one-time) — identity
      verification, 2FA, and payment are account-level, so Jeff-only.
- [ ] **iOS**: Apple Developer Program ($99/yr) **and a Mac with Xcode** —
      this box has no Mac; iOS signing/archiving must happen there.
- [ ] **Keystore** (Android): created in Android Studio on first signed
      AAB build — keep the `.keystore` + password safe forever (required
      for every future update).
- [ ] **App ID check**: confirm `com.notanai.mscerttrainer` is available in
      both stores *before* the first build (can't change it after).
- [ ] **Listing entry**: title/description/screenshots are pre-written in
      `store/APPSTORE_LISTING.md` and `store/PLAYSTORE_LISTING.md` —
      Jeff pastes them into the store consoles.
- [ ] **Privacy policy URL**: full policy text already exists in
      `PRIVACY.md` — it just needs a public URL (e.g. `yourhost.com/privacy`
      from his Route-A host; I can prepare the page file if he picks the URL).
- [ ] **Screenshots**: easiest is real captures of the app on his phone
      (Home, quiz, results, About views) — store specs want 2–8.
- [ ] **Review**: submit, then answer any Apple/Google reviewer messages
      (inbound mail on his accounts).

## Decisions — Jeff answered 2026-09-22 (see the shared todo file)

- [x] **Route** — BOTH stores; the app should be compiled and standalone
      so no hosting is needed. → Capacitor builds: Android AAB here (needs
      the keystore step), iOS on a Mac (Jeff). Route A kept as fallback +
      for the privacy-policy URL.
- [x] **Name** — decided: **"MSRN Exam Prep"** (short name "MSRN Prep").
      MSRN = Multiple Sclerosis Registered Nurse, the certification the
      bank prepares for; keeps the credential keyword searchable in both
      stores. Applied across the app + listings 2026-09-26.
- [x] **Bank polish** — "yes please": rewriting pass in progress —
      equalizing option lengths on the 225 flagged questions (28.2%),
      keeping the key correct and the distractors wrong.
