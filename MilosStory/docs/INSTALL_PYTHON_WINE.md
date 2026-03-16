# Installing Python in Wine for Windows Builds

This guide explains how to install Python in Wine so you can build Windows executables on Mac/Linux.

## Step 1: Download Python for Windows

1. Go to: https://www.python.org/downloads/windows/
2. Download the latest Python 3.x **64-bit** installer
   - Look for "Windows installer (64-bit)" 
   - File will be named something like: `python-3.12.0-amd64.exe`

## Step 2: Install Python in Wine

After downloading, open Terminal and run:

```bash
# Navigate to your Downloads folder (or wherever you saved the installer)
cd ~/Downloads

# Install Python in Wine
WINEPREFIX=~/.wine wine python-3.XX.X-amd64.exe
```

**Important:** Replace `python-3.XX.X-amd64.exe` with the actual filename you downloaded.

## Step 3: During Installation

When the Python installer opens in Wine:

1. ✅ Check "Add Python to PATH" (very important!)
2. Click "Install Now"
3. Wait for installation to complete
4. Click "Close" when done

## Step 4: Verify Installation

Test that Python is installed:

```bash
WINEPREFIX=~/.wine wine python --version
```

You should see something like: `Python 3.12.0`

## Step 5: Build Your Windows Executable

Now you can run the build script:

```bash
./build_windows.sh
```

## Troubleshooting

### Python not found after installation
- Make sure you checked "Add Python to PATH" during installation
- Try restarting your terminal
- Check if Python is in Wine's PATH: `WINEPREFIX=~/.wine wine cmd /c "where python"`

### Wine errors
- Make sure Wine is properly installed: `wine --version`
- Try initializing Wine: `WINEPREFIX=~/.wine winecfg`
- Some Windows installers may not work perfectly in Wine

### Alternative: Build on Windows
For the most reliable results, build on an actual Windows machine:
1. Copy your project to a Windows computer
2. Install Python and pip on Windows
3. Run: `pip install -r requirements.txt`
4. Run: `pip install pyinstaller`
5. Use the same PyInstaller command from the build script
