@echo off
echo ========================================
echo Installing CodaiPro Dependencies
echo ========================================
echo.
echo NOTE: Python 3.11 is recommended. On Python 3.12/3.13 the
echo llama-cpp-python package is built from source and needs
echo CMake + a C/C++ compiler (Visual Studio Build Tools).
echo.

echo [1/2] Installing all dependencies from requirements.txt...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo Installation FAILED. If llama-cpp-python was the problem,
    echo install Visual Studio Build Tools + CMake and run this again.
    pause
    exit /b 1
)

echo.
echo [2/2] Verifying installation...
python -c "import fastapi, uvicorn, customtkinter, pyperclip, requests; print('All dependencies OK')"

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Now start the app with:  python launcher.py
echo.
pause
