# 🚀 CodaiPro Deployment Guide

How CodaiPro ships: GitHub Releases for the app, GitHub Pages for the website, GitHub Actions for both.

## GitHub Releases (the app)

Automated by `.github/workflows/release.yml` on every `v*` tag:

1. Builds `Codai.exe` from `Codai.spec` (PyInstaller)
2. Downloads the latest official `llama-server` (Windows CPU) from llama.cpp releases into `engine/`
3. Assembles the portable folder: `Codai.exe`, `dev/`, `ui/`, `engine/`, `config.json`, `run.bat`, `kill.bat`, `help.txt`, `models/README.txt`
4. Zips it as `CodaiPro-<version>-Portable-Windows.zip` and attaches it to the release with notes

To cut a release: push a tag (`git tag v3.0.1 && git push origin v3.0.1`) or run the workflow manually with a version input.

The optional Windows installer (`installer.iss`, Inno Setup) is compiled locally: build `Codai.exe` first, then compile the script with Inno Setup 6.

## GitHub Pages (the website)

Automated by `.github/workflows/website-pages.yml` on every push that touches `website/`. The site deploys to:

https://luckyyaduvanshiofficial.github.io/Codaipro/

The website is fully static with no build step — `website/` is the deploy artifact.

## Repository Layout

- `dev/`, `ui/`, `engine/`, `models/`, `config.json`, `run.bat`, `kill.bat` — the application (Codai Pro architecture)
- `website/` — the public site
- `.github/workflows/` — release + Pages automation

Models (`models/`) and the engine binary (`engine/`) are intentionally not in git — large binaries are fetched per machine and in CI.
