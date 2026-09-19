# Play Store listing — MS-Cert Trainer

## Facts

- App name: **MS-Cert Trainer** (≤30 chars ✓)
- Category: Medical
- Language: English (US)
- App icon: 512×512 (from `phone-pwa/icons/icon-512.png`)
- Feature graphic: 1024×500 — create (banner: dark navy #0b1026, "799
  offline practice questions for MS nursing certification")
- Privacy policy URL: **required** — publish `PRIVACY.md` at a stable URL
  (e.g. GitHub Pages for this repo) and paste the URL into the console.
- Content rating: answer the questionnaire — all "No".

## Short description (≤80 chars)

Offline MS nursing cert practice — 799 questions with rationales.

## Full description (≤4000 chars)

MS-Cert Trainer is an offline study companion for nurses preparing for
Multiple Sclerosis (MS) nursing certification.

The app ships with a 799-question practice bank spanning the five core
domains — Concepts, Assessment & Intervention, Advocacy, Education, and
Research. Every question is paired with a written explanation of the answer,
so a wrong guess still teaches you.

WHAT'S INSIDE
• Domain, difficulty, and session-length controls (5–50 questions)
• Instant feedback with a rationale for every answer
• Session scores with a per-domain breakdown, so you can see exactly where
  you are weakest
• Review mode: jump straight back into the questions you missed
• Haptic feedback on every answer
• Optional daily study reminder and a next-morning nudge to review misses
• Your progress stays on your device — no account, no analytics, no
  advertising, and no data ever leaves the phone
• Works fully offline: the entire question bank ships inside the app and
  every session runs with no connection at all

QUESTION-BANK QUALITY
The bank is curated and audited: duplicates and biased items were removed,
answer-position distribution is balanced and re-verified on every build, and
the clinical content is reviewed and dated. The review date is shown in the
About screen.

IMPORTANT
Study aid only. This app is not medical advice, is not affiliated with or
endorsed by any certifying body, and contains no actual examination items.

## Data safety (console form)

- Data collected: **We don't collect any data.**
  (No data is collected or shared by this app.)
- Security: data is stored only on the device; no network transmission.
- If Play asks: "How is the app's data protected?" → all data is on-device
  only; the app performs no network communication.

## Screenshots (phone)

Same six as the App Store (see `APPSTORE_LISTING.md`), in Play's order:
1. Home with progress strip
2. Question in progress
3. Answered + rationale
4. Results + breakdown
5. About & disclaimer
6. Reminder toggle on

## Minimum requirements check

- Target API: Capacitor 6 builds to API 34/35 — meets current Play minimum.
- Permissions requested: VIBRATE (haptics), POST_NOTIFICATIONS
  (Android 13+ reminders) — both explained in-app and in the data-safety
  answers. No location, no camera, no ads.
