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
echo 4. Tiny models for weak PCs (under 1 GB)
echo.

set /p choice="Enter your choice (1-4): "

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

if "%choice%"=="4" (
    echo.
    echo Selected: Tiny models for weak PCs (under 1 GB)
    echo.
    echo Pick one - copy the direct download link into your browser:
    echo.
    echo Qwen3.5-0.8B (0.58 GB, newest):
    echo https://huggingface.co/bartowski/Qwen_Qwen3.5-0.8B-GGUF/resolve/main/Qwen_Qwen3.5-0.8B-Q4_K_M.gguf
    echo.
    echo Qwen3-0.6B (0.48 GB):
    echo https://huggingface.co/bartowski/Qwen_Qwen3-0.6B-GGUF/resolve/main/Qwen_Qwen3-0.6B-Q4_K_M.gguf
    echo.
    echo Gemma 3 1B Instruct (0.81 GB):
    echo https://huggingface.co/bartowski/google_gemma-3-1b-it-GGUF/resolve/main/google_gemma-3-1b-it-Q4_K_M.gguf
    echo.
    echo Llama 3.2 1B Instruct (0.81 GB):
    echo https://huggingface.co/bartowski/Llama-3.2-1B-Instruct-GGUF/resolve/main/Llama-3.2-1B-Instruct-Q4_K_M.gguf
    echo.
    echo Then place the .gguf file in the 'models' folder.
    echo.
    start "" "https://huggingface.co/bartowski/Qwen_Qwen3.5-0.8B-GGUF"
)

echo.
echo ========================================
echo After downloading:
echo 1. Move the .gguf file(s) to the 'models' folder
echo 2. Run the app with:  python launcher.py
echo ========================================
echo.
pause
