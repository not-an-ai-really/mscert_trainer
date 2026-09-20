/* MS-CERT-CAPACITOR-STUB
 *
 * Stub for the hosted/PWA build. For the store build (App Store /
 * Play Store), this file is REPLACED with the real Capacitor core bridge:
 *
 *     npm install && node store/copy-native.js
 *
 * (see store/BUILD_GUIDE.md). The web build has to pass check.bat without
 * node_modules around: sw.js precaches every file it lists, and a 404 on
 * this file aborts service-worker install, which kills offline mode.
 *
 * Keep this a no-op. window.Capacitor stays undefined, and app.js
 * feature-detects the native shell off of that — haptics and notifications
 * are simply absent from the web build. */
"use strict";
