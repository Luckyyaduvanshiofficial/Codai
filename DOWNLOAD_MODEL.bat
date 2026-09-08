@echo off
echo ========================================
echo   CodaiPro - Production Model Downloader
echo ========================================
echo.

echo This will help you download a fast, production-ready model.
echo.
echo Recommended Models:
echo 1. Phi-3.5-mini (BEST - Balanced speed/quality - 2.3GB) ⭐
echo 2. Qwen2.5-Coder-3B (Excellent for coding - 2GB)
echo 3. Qwen2.5-Coder-7B (Most powerful - 4.7GB)
echo.

set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    echo.
    echo Selected: Phi-3.5-mini ⭐ RECOMMENDED
    echo.
    echo Please download manually from:
    echo https://huggingface.co/microsoft/Phi-3.5-mini-instruct-gguf/tree/main
    echo.
    echo Download this file: Phi-3.5-mini-instruct-q4.gguf
    echo.
    echo Then place it in the 'models' folder.
    echo.
    echo This model offers the BEST balance of speed and quality!
    echo.
    start https://huggingface.co/microsoft/Phi-3.5-mini-instruct-gguf/tree/main
)

if "%choice%"=="2" (
    echo.
    echo Selected: Qwen2.5-Coder-3B
    echo.
    echo Please download manually from:
    echo https://huggingface.co/Qwen/Qwen2.5-Coder-3B-Instruct-GGUF/tree/main
    echo.
    echo Download this file: qwen2.5-coder-3b-instruct-q4_k_m.gguf
    echo.
    echo Then place it in the 'models' folder.
    echo.
    start https://huggingface.co/Qwen/Qwen2.5-Coder-3B-Instruct-GGUF/tree/main
)

if "%choice%"=="3" (
    echo.
    echo Selected: Qwen2.5-Coder-7B
    echo.
    echo Please download manually from:
    echo https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct-GGUF/tree/main
    echo.
    echo Download the q4_k_m GGUF file. If it is split into parts like
    echo qwen2.5-coder-7b-instruct-q4_k_m-00001-of-00002.gguf, download
    echo ALL parts into the 'models' folder - they are loaded together.
    echo.
    start https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct-GGUF/tree/main
)

echo.
echo ========================================
echo After downloading:
echo 1. Move the .gguf file(s) to the 'models' folder
echo 2. Run the app with:  python launcher.py
echo ========================================
echo.
pause
