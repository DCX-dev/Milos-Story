#!/bin/bash
# Helper script to install Python in Wine
# This script should be run from the project directory

echo "=========================================="
echo "Python Installation Helper for Wine"
echo "=========================================="
echo ""
echo "Note: Make sure you've downloaded Python installer to ~/Downloads first"
echo ""

# Check if Wine is installed
if ! command -v wine &> /dev/null; then
    echo "✗ Error: Wine is not installed."
    echo ""
    echo "Please install Wine first:"
    echo "  On Mac: brew install wine-stable"
    exit 1
fi
echo "✓ Wine is installed"
echo ""

# Check Downloads folder for Python installers
echo "Searching for Python installers..."
PYTHON_INSTALLERS=""

# Check Desktop/python folder first (common location)
# Look for installer files (python-*.exe) not just python.exe
if [ -d ~/Desktop/python ]; then
    # Look for installer files in the folder itself and subdirectories
    PYTHON_INSTALLERS=$(find ~/Desktop/python -maxdepth 2 -type f \( -name "python-*.exe" -o -name "*python*installer*.exe" -o -name "*python*setup*.exe" -o -name "python-*-amd64.exe" \) 2>/dev/null | grep -v "python.exe$" | grep -v "pythonw.exe$" | head -1)
    if [ -n "$PYTHON_INSTALLERS" ]; then
        echo "  ✓ Found installer in Desktop/python folder"
    fi
fi

# Check Downloads folder
if [ -z "$PYTHON_INSTALLERS" ] && [ -d ~/Downloads ]; then
    PYTHON_INSTALLERS=$(ls ~/Downloads/python*.exe 2>/dev/null)
    if [ -n "$PYTHON_INSTALLERS" ]; then
        echo "  ✓ Found in Downloads folder"
    fi
fi

# Check Applications folder
if [ -z "$PYTHON_INSTALLERS" ] && [ -d /Applications ]; then
    PYTHON_INSTALLERS=$(ls /Applications/python*.exe 2>/dev/null)
    if [ -n "$PYTHON_INSTALLERS" ]; then
        echo "  ✓ Found in Applications folder"
    fi
fi

# Also check Desktop root
if [ -z "$PYTHON_INSTALLERS" ] && [ -d ~/Desktop ]; then
    PYTHON_INSTALLERS=$(ls ~/Desktop/python*.exe 2>/dev/null)
    if [ -n "$PYTHON_INSTALLERS" ]; then
        echo "  ✓ Found on Desktop"
    fi
fi

# Check current directory
if [ -z "$PYTHON_INSTALLERS" ]; then
    PYTHON_INSTALLERS=$(ls python*.exe 2>/dev/null)
    if [ -n "$PYTHON_INSTALLERS" ]; then
        echo "  ✓ Found in current directory"
    fi
fi

if [ -z "$PYTHON_INSTALLERS" ]; then
    echo "✗ No Python installer found"
    echo ""
    
    # Check if there's a Python installation in Desktop/python
    if [ -f ~/Desktop/python/python.exe ]; then
        echo "⚠ Found Python installation in ~/Desktop/python"
        echo "  However, Wine needs the INSTALLER file to set up Python properly."
        echo ""
        echo "The installer file should be named something like:"
        echo "  python-3.12.0-amd64.exe"
        echo "  (not just python.exe)"
        echo ""
    fi
    
    echo "Please download Python for Windows INSTALLER:"
    echo ""
    echo "OPTION 1 - Direct download link:"
    echo "  Open this URL in your browser:"
    echo "  https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe"
    echo ""
    echo "OPTION 2 - Official website:"
    echo "  1. Go to: https://www.python.org/downloads/windows/"
    echo "  2. Click 'Download Python 3.x.x' (latest version)"
    echo "  3. Make sure to download the 64-bit INSTALLER"
    echo "  4. Save it to ~/Desktop/python folder or Downloads"
    echo ""
    echo "After downloading the installer, run this script again:"
    echo "  ./install_python_wine.sh"
    echo ""
    exit 1
fi

echo "Found Python installer(s):"
echo "$PYTHON_INSTALLERS" | while read -r installer; do
    echo "  - $(basename "$installer")"
done
echo ""

# Use the first one found (or let user choose)
INSTALLER=$(echo "$PYTHON_INSTALLERS" | head -1)
INSTALLER_NAME=$(basename "$INSTALLER")

echo "Using: $INSTALLER_NAME"
echo ""
echo "Installing Python in Wine..."
echo "  (A window should open - make sure to check 'Add Python to PATH')"
echo ""

# Install Python
WINEPREFIX=~/.wine wine "$INSTALLER"

INSTALL_EXIT_CODE=$?

echo ""
echo "=========================================="
if [ $INSTALL_EXIT_CODE -eq 0 ]; then
    echo "✓ Installation completed!"
    echo ""
    echo "Verifying Python installation..."
    if WINEPREFIX=~/.wine wine python --version &> /dev/null; then
        PYTHON_VERSION=$(WINEPREFIX=~/.wine wine python --version 2>&1 | head -1)
        echo "✓ Python is installed: $PYTHON_VERSION"
        echo ""
        echo "You can now run: ./build_windows.sh"
    else
        echo "⚠ Python may not be in PATH"
        echo "  Make sure you checked 'Add Python to PATH' during installation"
        echo "  Try running: WINEPREFIX=~/.wine wine python --version"
    fi
else
    echo "⚠ Installation may have failed or was cancelled"
    echo "  Check the output above for errors"
fi
echo "=========================================="
