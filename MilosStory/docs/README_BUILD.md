# Building Executables - Quick Guide

## Understanding Python Versions

**Important:** There are two different Python installations needed:

1. **Mac Python** (what you have) - Used to run the game on Mac
   - ✅ You already have this: Python 3.13.3
   - Used for: Running `python main.py` on Mac

2. **Windows Python in Wine** (what you need for Windows builds) - Used to build Windows executables
   - ❌ You need to install this separately
   - Used for: Building `.exe` files using PyInstaller in Wine

## Building Mac Executable (Easy - Use Your Mac Python)

```bash
./build_mac.sh
```

This uses your existing Mac Python - no extra setup needed!

## Building Windows Executable (Requires Windows Python in Wine)

You have two options:

### Option 1: Install Windows Python in Wine (Complex)

1. Download Windows Python installer: https://www.python.org/downloads/windows/
2. Install it in Wine: `./install_python_wine.sh`
3. Build: `./build_windows.sh`

**Note:** This can be unreliable and may not work perfectly.

### Option 2: Build on Windows Machine (Recommended)

For best results, build on an actual Windows computer:

1. Copy your project to a Windows machine
2. Install Python from python.org
3. Run:
   ```cmd
   pip install -r requirements.txt
   pip install pyinstaller
   pyinstaller --name "MilosStory" --onefile --windowed --add-data "player;player" --add-data "save_data;save_data" main.py
   ```

### Option 3: Use GitHub Actions (Free CI/CD)

Create a `.github/workflows/build.yml` file to automatically build Windows executables in the cloud.

## Summary

- **Mac build**: ✅ Ready to go - just run `./build_mac.sh`
- **Windows build**: Requires Windows Python in Wine OR build on Windows machine
