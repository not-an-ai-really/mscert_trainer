@echo off
rem MS-Cert Trainer - one-command check suite.
rem Usage:  check.bat
setlocal
cd /d "%~dp0"

echo === 1/4 bank audit ===
python tools\audit_bank.py
if errorlevel 1 goto fail

echo.
echo === 2/4 PWA smoke test ===
python tools\test_pwa.py
if errorlevel 1 goto fail

echo.
echo === 3/4 JS syntax (node, if installed) ===
where node >nul 2>nul
if errorlevel 1 (
  echo node not found - skipping (install Node.js to enable)
) else (
  node --check phone-pwa\js\app.js || goto fail
  node --check phone-pwa\js\bank.js || goto fail
  node --check phone-pwa\sw.js || goto fail
  echo JS syntax OK
)

echo.
echo === 4/4 version consistency ===
python tools\check_versions.py || goto fail

echo.
echo ALL CHECKS PASSED
endlocal
exit /b 0

:fail
echo.
echo CHECKS FAILED
endlocal
exit /b 1
