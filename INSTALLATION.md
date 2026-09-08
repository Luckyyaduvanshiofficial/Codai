# 📦 Installing CodaiPro v3.0

## Option 1: Portable Executable (Recommended)

```text
1. Download CodaiPro-v3.0-Portable-Windows.zip from the releases page:
   https://github.com/Luckyyaduvanshiofficial/Codai/releases/latest
2. Right-click → Extract All to a WRITABLE folder (e.g., D:\CodaiPro or a USB drive)
   Do NOT extract into C:\Program Files - the app writes logs and reads models from its folder.
3. Download ONE model into the models/ folder (see below)
4. Double-click run.bat
5. Wait for [READY] - the browser opens http://127.0.0.1:8081/
```

The zip ships with `Codai.exe` and the official `engine\llama-server.exe` already inside. You only add a model.

## Option 2: From Source

```bash
git clone https://github.com/Luckyyaduvanshiofficial/Codai.git
cd Codai
pip install -r requirements.txt   # installs psutil

# Get the engine binary into engine/ (see "Engine Setup" below)
# Get a model into models/ (see "Model Setup" below)

# Windows: double-click run.bat
# Linux / macOS:
python dev/controller.py
```

---

## Engine Setup (source installs only; the release zip includes it)

The engine is the official [llama.cpp](https://github.com/ggml-org/llama.cpp) `llama-server` binary.

**Windows**
```bash
# Easiest:
winget install llama.cpp
# then copy llama-server.exe from the install location into engine\

# Or download directly:
# https://github.com/ggml-org/llama.cpp/releases → llama-bXXXX-bin-win-cpu-x64.zip
# Extract everything into engine\
```

**Linux**
```bash
# Download llama-bXXXX-bin-ubuntu-x64.tar.gz from llama.cpp releases,
# extract, and copy llama-server + the .so files into engine/
chmod +x engine/llama-server
```

**macOS**
```bash
brew install llama.cpp
# then link the binary:
ln -s $(brew --prefix)/bin/llama-server engine/llama-server
```

**GPU (optional)**: download a CUDA build instead (`llama-bXXXX-bin-win-cuda-12.4-x64.zip` + the cudart zip from the same release) and extract both into `engine\`. The controller passes no GPU flags by default — edit `dev/engine.py` boot arguments (`-ngl 99`) to offload layers.

---

## Model Setup

Drop ONE `.gguf` file into the `models/` folder. Default expected by `config.json`: `gemma-3-1b-it-Q4_K_M.gguf` (0.81 GB) — https://huggingface.co/bartowski/google_gemma-3-1b-it-GGUF

Other verified picks (all direct links on the [website model guide](https://luckyyaduvanshiofficial.github.io/Codai/#download)):
- Qwen3.5-0.8B (0.58 GB, newest)
- Qwen3-0.6B (0.48 GB)
- Llama 3.2 1B Instruct (0.81 GB)
- Phi-3.5-mini (2.3 GB), Qwen2.5-Coder-3B (2 GB), Qwen2.5-Coder-7B (4.7 GB)

Using a different filename? Set `"model_name"` in `config.json` or run `DOWNLOAD_MODEL.bat` for help.

---

## 🚀 First Run

1. `run.bat` shows a startup summary and preflight checks
2. Wait for `[READY]` — this means the engine loaded your model
3. The browser opens `http://127.0.0.1:8081/` automatically
4. Chat! Answers stream in token by token
5. Press any key in the launcher window to stop Codai safely

---

## 🆘 Troubleshooting

### "Missing engine binary: engine\llama-server.exe"
The engine was not found. Re-download the release zip (it includes the engine) or follow Engine Setup above.

### "Missing model file: models\..."
Download a model (see Model Setup) or fix `"model_name"` in `config.json`.

### "Port 8081/8082 is already in use"
Another app (or an old Codai instance) holds the port. Run `kill.bat`, or change `"port"` in `config.json`.

### "Another Codai instance is already running"
Close the other instance. If it crashed earlier, `kill.bat` (Windows) removes the stale `logs\codai.lock`.

### Engine keeps crashing
Check `logs\engine.log` for the native error and `logs\crash.log` for Python traces. Common causes: not enough RAM for the model (pick a smaller one), or a corrupted download (re-download the model).

### Chat replies are slow
That is normal on CPU for bigger models — try Qwen3.5-0.8B or Gemma 3 1B, and close heavy apps. The controller already tunes threads/context to your hardware.

### UI loads but chat fails
Check the health endpoint `http://127.0.0.1:8081/health` — `engine` should say `running`. If not, look at `logs\engine.log`.
