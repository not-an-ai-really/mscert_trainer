# Store readiness and security review

Reviewed 17 September 2026 against the App Store Review Guidelines and the
Google Play Developer Program Policy as published on that date. Items marked
**FIXED** were changed in this pass; the rest need a decision or work outside
the code.

---

## 1. Blocking: this is a PWA, and neither store takes a PWA as-is

The biggest problem is not a bug. `phone-pwa/` is a website. Neither store
accepts a URL — both need a signed native binary, so the app has to be
wrapped (Capacitor is the least painful route for this codebase) before it can
be submitted at all. And a bare wrapper is what Apple rejects most often:

> **4.2 Minimum Functionality** — "Your app should include features, content,
> and UI that elevate it beyond a repackaged website. If your app is not
> particularly useful, unique, or 'app-like,' it doesn't belong on the App
> Store."

> **4.2.2** — "Other than catalogs, apps shouldn't primarily be marketing
> materials, advertisements, web clippings, content aggregators, or a
> collection of links."

Google Play's Spam and Minimum Functionality policy applies the same test from
the other direction, and Trusted Web Activity submissions are currently being
bounced there for it.

**What clears 4.2 for this app.** It already has two things reviewers count:
the content ships in the binary (a 799-question bank, fully offline, no server)
and progress persists locally. That is genuinely not a web clipping. What it
lacks is native surface. Add at least two of:

- local notifications for a study reminder / spaced-repetition nudge
- haptic feedback on answer selection
- a home-screen widget or Siri shortcut ("start a 10-question session")
- offline-first framing made explicit in the listing copy and screenshots

Then say so in the App Review notes: state that the bank is embedded, the app
is fully functional in airplane mode, and name the native integrations. A
reviewer who cannot tell the difference between this and a bookmark rejects it.

**Action:** wrap with Capacitor, add native features, write review notes.
Not done here — it is a build-system change, not an edit.

---

## 2. Blocking: medical-content requirements were entirely missing — **FIXED**

Apple reviews health content harder than anything else in the app:

> **1.4.1 Physical Harm** — "Medical apps that could provide inaccurate data or
> information, or that could be used for diagnosing or treating patients may be
> reviewed with greater scrutiny. Apps must clearly disclose data and
> methodology to support accuracy claims… Apps should remind users to check
> with a doctor in addition to using the app and before making medical
> decisions."

The app shipped drug names, dose thresholds, and lab-monitoring cut-offs with
no disclaimer, no scope statement, and no content-review date. That is a
straightforward 1.4.1 rejection, and a liability problem independent of the
store.

**FIXED** — added an **About & disclaimer** screen (`#view-about`) stating
educational use only, not clinical decision support, not a drug reference,
verify against current prescribing information; plus a `CONTENT_REVIEWED`
constant surfaced in-app so the review date is visible and has to be bumped
each content pass.

**Still to do:** Google Play requires the **Health apps declaration form** for
every app in a health category. This one is *Medical Reference and Education*
— "educational resources for healthcare professionals and patients, including
medical encyclopedias, treatment guidelines and symptom checkers." Fill it in
Play Console before the first release or the release is blocked.

---

## 3. Blocking: certification-body trademark exposure — **PARTLY FIXED**

The name "MS-Cert Trainer" plus the tagline "Multiple Sclerosis
certification" implies a relationship with the body that grants the MSCN
credential. Apple:

> **4.1(c)** — "You cannot use another developer's icon, brand, or product
> name in your app's icon or name, without approval from the developer."

Google Play's Impersonation policy covers the same ground and is enforced by
automated takedown, which is worse — you find out after publication.

**FIXED** — the About screen now carries an explicit non-affiliation
statement naming MSNICB and IOMSN, and states the app contains no actual exam
items and predicts no certification result.

**Still to do — your call.** Do not put "MSCN" or "MSNICB" in the app *name*,
subtitle, or keywords. "MS-Cert Trainer" is defensible; "MSCN Exam Prep" is
not, without written permission. If you want the certification named in the
listing, get it in writing from MSNICB first. Repeat the non-affiliation line
in the store description, not just in-app — reviewers read the description.

---

## 4. Blocking: no privacy policy — **FIXED**

> **5.1.1(i)** — "All apps must include a link to their privacy policy in the
> App Store Connect metadata field **and within the app in an easily accessible
> manner**… Explain its data retention/deletion policies and describe how a
> user can revoke consent and/or request deletion of the user's data."

There was none. Both stores require a reachable URL even for an app that
collects nothing, and Play additionally requires the Data Safety form.

**FIXED** — `PRIVACY.md` added, covering collection (none), local storage,
retention, and erasure. The About screen carries the same statement in-app.

**Still to do:** host `PRIVACY.md` at a stable public URL and paste that URL
into App Store Connect and Play Console. Fill the Play **Data Safety** form as
"no data collected, no data shared" and Apple's privacy nutrition label as
"Data Not Collected." Both are true here and that is a real competitive
advantage for a hospital-adjacent app — say so in the listing.

---

## 5. Security

### 5.1 Stored-XSS path through the question bank — **FIXED**

`renderQuestion()` built the domain/difficulty tags with `innerHTML` and
interpolated bank fields directly, including into an attribute:

```js
`<span class="tag" data-d="${q.difficulty}">${q.difficulty}</span>`
```

Bank content is authored today, so this was not live-exploitable. It becomes
exploitable the moment the bank is fetched remotely, user-importable, or
community-contributed — all plausible next features — and a `"` in
`difficulty` breaks out of the attribute. `buildDomainChips()` had the same
pattern.

**FIXED** — both rebuilt with `createElement`/`textContent`. The remaining
three `innerHTML` uses are `= ""` clears, which are safe. Stem, options, and
rationale already used `textContent` and were fine.

### 5.2 No Content-Security-Policy — **FIXED**

**FIXED** — added a strict CSP meta tag. `connect-src 'none'` is the load-
bearing directive: even if bank.js were tampered with, it cannot exfiltrate
anything. `frame-ancestors` is ignored in `<meta>` form and has to be an HTTP
header — see `DEPLOYMENT.md` for the `_headers` file.

### 5.3 `start.bat` shipped inside the deployable folder — **FIXED**

It ran `python -m http.server --bind 0.0.0.0`, which serves the directory with
listing enabled to every host on the LAN. Harmless on a home network, not
something to have on a hospital network, and it had no business in the payload
that gets uploaded to a static host or bundled into an app binary.

**FIXED** — moved to `tools/serve-local.bat`. `phone-pwa/` is now a clean
deployable payload.

### 5.4 Clean bill elsewhere

No secrets, tokens, or keys anywhere in the tree or in git history. No
third-party scripts, no CDN, no analytics, no ad SDK, no trackers, no network
calls at runtime. `localStorage` holds only aggregate counters — no PII, no
patient data. The service worker is same-origin-only and checks `res.ok`
before caching. This is a genuinely clean app from a privacy standpoint.

One operational note: the service worker is cache-first with no expiry, so a
stale bank persists until `VERSION` is bumped. `tools/build_bank.js` now bumps
it automatically, which removes the manual step the README relied on.

---

## 6. Icons — **FIXED**

Three problems, all of which fail at upload or look broken on device:

1. `icon-512.png` has an **alpha channel and pre-rounded corners**. App Store
   Connect rejects an app icon with alpha outright.
2. The maskable icon was the same art as the "any" icon. Android crops maskable
   icons to a circle or squircle; the art ran to the edges, so the cross and
   underline were getting clipped on Android launchers.
3. No 1024×1024 icon, which the App Store listing requires.

**FIXED** — generated `icon-1024.png` (opaque, square, no alpha),
`icon-maskable-192/512.png` (art inside the inner 76% safe zone, opaque
background), and `apple-touch-icon-180.png`. Manifest and service worker
precache updated.

---

## 7. Smaller items

| Item | Status |
| --- | --- |
| `alert()` on empty filter set — a blocking JS dialog reads as "web page" to a reviewer | **FIXED** — inline message |
| Load-failure message exposed an internal path (`tools\build_bank_js.py`) to end users | **FIXED** — user-facing text |
| Filter chips had no `aria-pressed`; option buttons had no `type` | **FIXED** |
| `manifest.id` was `"mscert-trainer"` | **FIXED** — `"/"`, plus `categories`, `lang`, `dir` |
| No `<meta name="description">` | **FIXED** |
| README claimed 510 questions; bank had 589 | **FIXED** — build script writes the real count into both |
| README referenced `../tools/*.py` and `../publishing-guide.md`, none of which are in the repo | **FIXED** — working Node tools committed; see §8 |
| `confirm()` still used for quit/reset | Left as-is. Acceptable to both stores; replace with a styled sheet if you want the polish |

---

## 8. The build pipeline was not in the repo

`bank.js` was generated by `tools/build_bank_js.py` from
`questions_complete.json` — neither of which is committed. Anyone cloning this
repo, including you on a new machine, could not rebuild the bank, and any edit
to `bank.js` would be silently destroyed by the next build.

**FIXED** — committed a working pipeline:

| File | Purpose |
| --- | --- |
| `tools/questions.json` | source of truth, 799 questions |
| `tools/build_bank.js` | regenerates `phone-pwa/js/bank.js`, auto-bumps `sw.js` VERSION |
| `tools/audit_bank.js` | quality gate; exits non-zero on a blocking defect |
| `tools/rebalance.js` | the one-time answer-key repair, kept for the record |

```bash
node tools/audit_bank.js    # check
node tools/build_bank.js    # regenerate bank.js + bump sw VERSION
```

`tools/add_questions.js batch.json` appends new questions, assigns IDs,
validates, and rebuilds in one step — it rejects an item rather than admitting
a defect.

Run the audit in CI. It fails the build on answer-key skew above 30%, duplicate
stems, duplicate IDs, prohibited option forms, and malformed records — which is
what let the problems in §9 accumulate unnoticed.

---

## 9. Question bank defects

Covered in full in `BANK_REVIEW.md`. Headline: the answer key was 53% B and
only 4.8% D; that is fixed to 25/25/25/25. Eighteen items had defects serious
enough to teach the wrong thing and were rewritten, two verbatim duplicates
were removed, and 212 new questions were added, taking the bank from 589 to
799.

---

## Priority order

1. Wrap natively and add native features (§1) — nothing ships without this
2. Host `PRIVACY.md`, fill Data Safety + Health apps declaration (§2, §4)
3. Decide the naming question and keep MSCN/MSNICB out of the title (§3)
4. Ship the icons and code fixes already made (§5, §6, §7)
5. Keep working the length-cue problem in the bank (`BANK_REVIEW.md` §3)
