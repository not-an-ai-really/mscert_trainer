# MS-Cert Trainer — things only Jeff can do

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

## Route C — real app stores (optional; was deferred earlier — still?)

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

## Decisions (no action, just say which)

- [ ] **Route?** A only (recommended) vs. A + Play vs. both stores.
- [ ] **Name**: keep "MS-Cert Trainer"? The About screen and listings already
      disclaim any affiliation with the certifying bodies; only a final
      call on using "MS-Cert" in the store listing is needed.
- [ ] **Bank polish**: the audit flags 225 questions (28%) where the correct
      option is conspicuously the longest — a real-test tell. Say the word
      and I'll do a rewriting pass to equalize option lengths.
