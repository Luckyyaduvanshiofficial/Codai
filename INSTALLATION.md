# 📦 CodaiPro Installation Guide

## 🎯 Choose Your Installation Method

### 🚀 Option 1: Portable Executable (Recommended for Students)

**Perfect for lab environments, exams, and quick setup**

#### Step 1: Download
1. Go to [Releases Page](https://github.com/luckyyaduvanshi/codaipro/releases)
2. Download `CodaiPro-v2.1-Portable-Windows.zip`
3. File size: ~500MB (includes all dependencies)

#### Step 2: Extract & Run
```bash
# Extract the ZIP file
Right-click → Extract All → Choose location

# Navigate to extracted folder
cd CodaiPro_v21/

# Run the application
Double-click CodaiPro_v21.exe
```

#### ✅ Advantages
- No installation required
- Works on restricted lab computers
- Portable - run from USB drive
- No admin rights needed
- 100% offline ready

---

### 🐍 Option 2: Python Installation (For Developers)

**Best for customization and development**

#### Prerequisites
- Python 3.11 or higher
- pip package manager
- Git (optional)

#### Step 1: Clone Repository
```bash
# Using Git
git clone https://github.com/luckyyaduvanshi/codaipro.git
cd codaipro

# Or download ZIP from GitHub
# Extract and navigate to folder
```

#### Step 2: Install Dependencies
```bash
# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install requirements
pip install -r requirements.txt
```

#### Step 3: Run Application
```bash
python launcher.py
```

#### ✅ Advantages
- Full source code access
- Easy customization
- Latest development features
- Contribute to project

---

### 🔧 Option 3: Build from Source

**For advanced users who want to create their own executable**

#### Prerequisites
- Python 3.11+
- PyInstaller
- All dependencies from requirements.txt

#### Step 1: Setup Environment
```bash
git clone https://github.com/luckyyaduvanshi/codaipro.git
cd codaipro
pip install -r requirements.txt
pip install pyinstaller
```

#### Step 2: Build Executable
```bash
# Windows
BUILD_V21.bat

# Manual build (all platforms)
python -m PyInstaller --onedir --windowed --name "CodaiPro_v21" launcher.py
```

#### Step 3: Find Your Executable
```bash
# Built executable location
dist_portable/CodaiPro_v21/CodaiPro_v21.exe
```

---

## 🎓 Lab Environment Setup

### For Students
1. **Download portable version** to USB drive
2. **Plug into lab computer**
3. **Run directly** - no installation needed
4. **Start coding** with AI assistance!

### For Lab Administrators
1. **Download once** and deploy to all machines
2. **No network configuration** required
3. **No admin rights** needed for users
4. **Resource efficient** - won't slow down systems

---

## 🔧 Troubleshooting

### Common Issues

#### "Multiple instances opening"
```bash
# Solution 1: Kill all instances
KILL_V21.bat

# Solution 2: Restart and try again
# Close all CodaiPro windows and restart
```

#### "Application won't start"
```bash
# Check system requirements
- Windows 10/11 (64-bit)
- 4GB RAM minimum
- 2GB free space

# Try running as administrator (if needed)
Right-click CodaiPro_v21.exe → Run as administrator
```

#### "Missing dependencies" (Python installation)
```bash
# Reinstall requirements (single source of truth)
pip install --force-reinstall -r requirements.txt
```

#### "Port 8765 already in use"
```bash
# Kill processes using port 8765 (backend port)
netstat -ano | findstr :8765
taskkill /PID <process_id> /F

# Or use the kill script
KILL_V21.bat
```

---

## 🚀 First Run Guide

### What to Expect
1. **Startup Screen** - Application initializes (5-10 seconds)
2. **Backend Loading** - AI engine starts up
3. **Main Interface** - Ready to use!

### Initial Setup
1. **Adjust Settings** - Temperature, response length
2. **Test AI Chat** - Ask a simple coding question
3. **Explore Features** - Code generation, explanation, debugging

### Tips for Best Performance
- **Close other applications** to free up RAM
- **Use SSD storage** for faster loading
- **Keep application updated** for latest features

---

## 📊 System Requirements

### Minimum Requirements
| Component | Requirement |
|-----------|-------------|
| **OS** | Windows 10 (64-bit) |
| **RAM** | 4GB |
| **Storage** | 2GB free space |
| **CPU** | Dual-core 2.0GHz |

### Recommended Requirements
| Component | Requirement |
|-----------|-------------|
| **OS** | Windows 11 (64-bit) |
| **RAM** | 8GB or more |
| **Storage** | 4GB free space (SSD) |
| **CPU** | Quad-core 2.5GHz+ |

---

## 🆘 Getting Help

### Documentation
- **README**: [Main documentation](README.md)
- **Wiki**: [Detailed guides](https://github.com/luckyyaduvanshi/codaipro/wiki)
- **FAQ**: [Common questions](https://github.com/luckyyaduvanshi/codaipro/wiki/FAQ)

### Support Channels
- **Issues**: [Report bugs](https://github.com/luckyyaduvanshi/codaipro/issues)
- **Discussions**: [Ask questions](https://github.com/luckyyaduvanshi/codaipro/discussions)
- **Email**: [Contact developer](https://luckyyaduvanshiofficial.github.io)

---

## 🎉 You're Ready!

Congratulations! You now have CodaiPro installed and ready to use. Start by asking the AI assistant to help you with your coding projects!

**Happy Coding! 🚀**