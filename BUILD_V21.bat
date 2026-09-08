@echo off
echo ========================================
echo  CodaiPro v2.1 - Enhanced Build System
echo  (Single Instance Protection)
echo ========================================
echo.
echo Starting automated build...
echo.

REM Get Python path
for /f "tokens=*" %%i in ('python -c "import sys; print(sys.executable)"') do set PYTHON_EXE=%%i
echo [1/5] Found Python: %PYTHON_EXE%

REM Install PyInstaller if needed
echo.
echo [2/5] Checking PyInstaller...
"%PYTHON_EXE%" -m pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    "%PYTHON_EXE%" -m pip install --quiet pyinstaller
)

REM Install dependencies (requirements.txt includes llama-cpp-python)
echo.
echo [3/5] Installing dependencies...
"%PYTHON_EXE%" -m pip install --quiet -r requirements.txt

REM Check launcher exists and ensure models folder exists
echo.
echo [4/5] Checking launcher...
if not exist "launcher.py" (
    echo ERROR: launcher.py not found!
    pause
    exit /b 1
)
if not exist "models" mkdir "models"

REM Build with PyInstaller
echo.
echo [5/5] Building package (this takes 5-10 min)...
"%PYTHON_EXE%" -m PyInstaller ^
    --onedir ^
    --windowed ^
    --name "CodaiPro_v21" ^
    --noconsole ^
    --add-data "models;models" ^
    --hidden-import="uvicorn" ^
    --hidden-import="fastapi" ^
    --hidden-import="llama_cpp" ^
    --hidden-import="customtkinter" ^
    --hidden-import="tkinter" ^
    --hidden-import="requests" ^
    --hidden-import="json" ^
    --hidden-import="threading" ^
    --hidden-import="queue" ^
    --hidden-import="time" ^
    --hidden-import="os" ^
    --hidden-import="sys" ^
    --hidden-import="ctypes" ^
    --hidden-import="socket" ^
    --collect-all="customtkinter" ^
    --collect-all="llama_cpp" ^
    launcher.py

if %errorlevel% neq 0 (
    echo.
    echo BUILD FAILED!
    echo Check the error messages above.
    pause
    exit /b 1
)

REM Create portable distribution
echo.
echo Finalizing...
if exist "dist_portable" rmdir /s /q "dist_portable"
mkdir "dist_portable"
xcopy /e /i /q "dist\CodaiPro_v21" "dist_portable\CodaiPro_v21"

echo.
echo ========================================
echo  BUILD COMPLETE!
echo ========================================
echo.
echo Location: %cd%\dist_portable\CodaiPro_v21\
echo NEXT: Copy "CodaiPro_v21" folder to pendrive
echo.
echo Done! Press any key to exit...
pause >nul
