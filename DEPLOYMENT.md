# Deployment notes

## Response headers to set at the host

`phone-pwa/index.html` carries a Content-Security-Policy in a `<meta>` tag,
which covers the app if it is ever opened from a plain static host. Two
directives are ignored in `<meta>` form and must be set as real HTTP headers.

For **Netlify**, add `phone-pwa/_headers`:

```
/*
  Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'
  X-Content-Type-Options: nosniff
  Referrer-Policy: no-referrer
  Permissions-Policy: geolocation=(), camera=(), microphone=(), usb=(), payment=()
  Strict-Transport-Security: max-age=31536000; includeSubDomains

/sw.js
  Cache-Control: no-cache
```

For **Cloudflare Pages**, the same file works. For **GitHub Pages**, custom
headers are not supported — use Netlify or Cloudflare Pages if the headers
matter to you.

`sw.js` must be served with `Cache-Control: no-cache` so a new service worker
is actually picked up; otherwise phones can stay pinned to an old bank for as
long as the host's default cache lifetime.

## Native store packaging

The PWA in `phone-pwa/` is the source of truth for the app's UI and content.
Submitting it to the App Store or Play Store requires a native shell — see
`STORE_REVIEW.md` for what Apple and Google will and will not accept.
