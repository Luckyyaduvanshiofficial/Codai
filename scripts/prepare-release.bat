@echo off
echo ========================================
echo  CodaiPro Release Preparation Script
echo ========================================
echo.

REM Clean previous builds
echo [1/5] Cleaning previous builds...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "dist_portable" rmdir /s /q "dist_portable"
if exist "*.spec" del /q "*.spec"

REM Build new version
echo.
echo [2/5] Building new version...
call BUILD_V21.bat

REM Create release folder
echo.
echo [3/5] Creating release package...
mkdir "release"
xcopy /e /i /q "dist_portable\CodaiPro_v21" "release\CodaiPro_v21"

REM Copy documentation
echo.
echo [4/5] Adding documentation...
copy "README.md" "release\"
copy "LICENSE" "release\"
copy "INSTALLATION.md" "release\"

REM Create ZIP for release
echo.
echo [5/5] Creating ZIP archive...
powershell Compress-Archive -Path "release\*" -DestinationPath "CodaiPro-v2.1-Portable-Windows.zip" -Force

echo.
echo ========================================
echo  Release package ready!
echo ========================================
echo.
echo Files created:
echo - CodaiPro-v2.1-Portable-Windows.zip
echo - release/ folder with all files
echo.
echo Next steps:
echo 1. Test the release package
echo 2. Create GitHub release
echo 3. Upload ZIP file
echo.
pause