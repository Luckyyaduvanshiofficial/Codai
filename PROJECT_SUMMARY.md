# 📊 CodaiPro v3.0 (Codai Pro) - Project Summary

## 🎯 Project Overview

**CodaiPro v3.0** is an offline AI coding assistant for students in restricted environments — university labs, exams, competitions. Version 3.0 rebuilt the product on the official llama.cpp engine:

- `llama-server` runs the model natively with streaming responses
- A lightweight Python controller (only dependency: `psutil`) serves the browser UI, proxies requests, and supervises the engine
- The old CustomTkinter desktop GUI and the llama-cpp-python backend were retired

## ✨ Key Capabilities

### Runtime
- **Streaming chat** over SSE with a stop button, markdown rendering, and code copy
- **Engine supervision** — health checks every 5s, staged auto-restart, graceful shutdown
- **Hardware-aware tuning** — RAM/CPU tiers set context size and thread count
- **Single instance** — PID lock with stale-lock recovery
- **Observability** — rotating logs, engine logs, crash reports, optional `/telemetry` page

### Distribution
- Portable Windows zip with `Codai.exe` + bundled `llama-server.exe` (CI-built)
- Inno Setup installer script for a classic setup.exe
- Cross-platform from source (Linux/macOS supported with a platform llama-server binary)

### Web Presence
- GitHub Pages website with model guide, live poll, and star count
- GitHub Actions release pipeline

## 📚 Documentation

- [README](README.md) — overview, quick start, model guide
- [INSTALLATION](INSTALLATION.md) — detailed setup and troubleshooting
- [DEPLOYMENT](DEPLOYMENT.md) — how releases and the site ship
- [docs/contributor-project-info.md](docs/contributor-project-info.md) — developer deep-dive
- [help.txt](help.txt) — end-user quick reference

## 📄 License

MIT — see [LICENSE](LICENSE).
