@echo off
echo ========================================
echo Installing Missing Dependencies
echo ========================================
echo.
echo NOTE: You are using Python 3.13 which needs pre-built wheels
echo We'll install compatible versions...
echo.

echo [1/3] Installing llama-cpp-python (pre-built for Python 3.13)...
pip install llama-cpp-python --prefer-binary --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu

if errorlevel 1 (
    echo.
    echo Pre-built version failed. Trying older compatible version...
    pip install llama-cpp-python==0.2.90 --prefer-binary
)

echo.
echo [2/3] Installing customtkinter...
pip install customtkinter

echo.
echo [3/3] Installing pyperclip...
pip install pyperclip

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Now run START_SIMPLE.bat to launch the app
echo.
pause
