@echo off
echo ========================================
echo  CodaiPro v2.1 - Single Instance Test
echo ========================================
echo.

echo Testing single instance protection...
echo.

echo [1] Starting first instance...
start "" "dist_portable\CodaiPro_v21\CodaiPro_v21.exe"

echo [2] Waiting 3 seconds...
timeout /t 3 /nobreak >nul

echo [3] Trying to start second instance (should fail)...
start "" "dist_portable\CodaiPro_v21\CodaiPro_v21.exe"

echo.
echo ========================================
echo  Test Complete!
echo ========================================
echo.
echo Expected behavior:
echo - First instance should open normally
echo - Second instance should show "already running" message
echo.
pause