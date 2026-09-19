/* Copies the Capacitor core runtime into the web bundle so the app needs no
   bundler. The native shell (android/ and ios/) provides Haptics and
   LocalNotifications at runtime; only the core bridge JS must ship with the
   web files.
   Run after `npm install`:  node store/copy-native.js */
const fs = require("fs");
const path = require("path");

const root = path.join(__dirname, "..");
const src = path.join(root, "node_modules", "@capacitor", "core", "dist", "capacitor.js");
const dst = path.join(root, "phone-pwa", "js", "capacitor.js");

if (!fs.existsSync(src)) {
  console.error("capacitor.js not found at:", src);
  console.error("Run `npm install` first (see package.json at the repo root).");
  process.exit(1);
}
fs.copyFileSync(src, dst);
console.log("copied:", src, "->", dst);
