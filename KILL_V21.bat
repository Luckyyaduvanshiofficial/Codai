@echo off
echo ========================================
echo  CodaiPro v2.1 - Kill All Instances
echo ========================================
echo.

echo Killing all CodaiPro processes...
taskkill /f /im "CodaiPro_v21.exe" 2>nul
taskkill /f /im "CodaiPro_v2.exe" 2>nul
taskkill /f /im "python.exe" /fi "WINDOWTITLE eq CodaiPro*" 2>nul

echo.
echo Cleaning up lock files...
del /q "%TEMP%\codaipro_v21.lock" 2>nul
del /q "%TEMP%\codaipro_v21_port8765.lock" 2>nul
del /q "%TEMP%\codaipro_v21_port8000.lock" 2>nul
del /q "%TEMP%\codaipro_v2.lock" 2>nul

echo.
echo Freeing port 8765 (backend port)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8765') do (
    taskkill /f /pid %%a 2>nul
)

echo.
echo ========================================
echo  All instances killed and cleaned up!
echo ========================================
echo.
pause
