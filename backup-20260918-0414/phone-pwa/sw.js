/* MS-Cert Trainer service worker.
   Cache-first for same-origin GETs so the whole app (including the
   510-question bank) works with zero connectivity.

   Bump VERSION whenever any file changes — old caches are purged on
   activate, so users get the new bank on next load.
*/
"use strict";

const VERSION = "v1.1.0"; // 589-question bank release
const CACHE = "mscert-" + VERSION;

const PRECACHE = [
  "./",
  "index.html",
  "css/app.css",
  "js/app.js",
  "js/bank.js",
  "manifest.webmanifest",
  "icons/icon-192.png",
  "icons/icon-512.png",
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE)
      .then((cache) => cache.addAll(PRECACHE))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(
        keys
          .filter((k) => k.startsWith("mscert-") && k !== CACHE)
          .map((k) => caches.delete(k))
      ))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  event.respondWith(
    caches.match(req, { ignoreSearch: true })
      .then((hit) => hit || fetch(req).then((res) => {
        if (res.ok) {
          const copy = res.clone();
          caches.open(CACHE).then((c) => c.put(req, copy));
        }
        return res;
      }))
      .catch(() => {
        // offline navigation: fall back to the cached app shell
        if (req.mode === "navigate") {
          return caches.match("index.html");
        }
        return Response.error();
      })
  );
});
