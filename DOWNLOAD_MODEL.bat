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
echo 3. DeepSeek-Coder-6.7B (Most powerful - 4GB)
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
    echo Selected: DeepSeek-Coder-6.7B
    echo.
    echo Please download manually from:
    echo https://huggingface.co/TheBloke/deepseek-coder-6.7B-instruct-GGUF/tree/main
    echo.
    echo Download this file: deepseek-coder-6.7b-instruct.Q4_K_M.gguf
    echo.
    echo Then place it in the 'models' folder.
    echo.
    start https://huggingface.co/TheBloke/deepseek-coder-6.7B-instruct-GGUF/tree/main
)

echo.
echo ========================================
echo After downloading:
echo 1. Move the .gguf file to the 'models' folder
echo 2. Delete or rename the old TinyLlama model (optional)
echo 3. Run START.bat to launch the app
echo ========================================
echo.
pause
