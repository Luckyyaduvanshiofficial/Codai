@echo off
REM Optional: Install GPU-accelerated version of llama-cpp-python
REM This will make responses 2-5x faster if you have an NVIDIA GPU

echo ========================================
echo   GPU Acceleration Setup (Optional)
echo ========================================
echo.
echo This will install GPU support for faster responses.
echo.
echo Requirements:
echo - NVIDIA GPU (GTX/RTX series)
echo - 4GB+ VRAM
echo - CUDA Toolkit installed (developer.nvidia.com/cuda-downloads)
echo.
echo If you don't have an NVIDIA GPU, press Ctrl+C to cancel.
echo.
pause

echo.
echo Uninstalling CPU-only version...
pip uninstall llama-cpp-python -y

echo.
echo Installing GPU-accelerated version...
echo This may take 5-10 minutes...
set CMAKE_ARGS=-DGGML_CUDA=on
pip install llama-cpp-python --no-cache-dir --force-reinstall

echo.
echo ========================================
echo GPU acceleration installed!
echo To offload layers to the GPU, set this before starting the app:
echo   set CODAIPRO_GPU_LAYERS=99
echo Your responses should now be 2-5x faster.
echo ========================================
echo.
pause
