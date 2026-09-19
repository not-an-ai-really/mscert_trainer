@echo off
rem MS-Cert Trainer - one-click local server.
rem Serves this folder on the LAN so a phone on the same WiFi can open it.
setlocal
cd /d "%~dp0"

python -c "import socket;s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM);s.connect(('8.8.8.8',80));print('PHONE_URL http://' + s.getsockname()[0] + ':8080')" 2>nul

echo.
echo Starting MS-Cert Trainer at  http://localhost:8080
echo On your PHONE (same WiFi):  open the PHONE_URL above, then use your
echo browser menu  "Add to Home Screen"  to get an app icon.
echo (Install/offline features need HTTPS - see the publishing guide.)
echo Keep this window open while you study. Ctrl+C stops the server.
echo.

python -m http.server 8080 --bind 0.0.0.0
endlocal
