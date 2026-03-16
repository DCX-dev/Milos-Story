#!/bin/bash
# Quick script to check if Python is working in Wine

echo "Checking Python installation in Wine..."
echo ""

# Check if Python is installed in Wine
if WINEPREFIX=~/.wine wine python --version &> /dev/null 2>&1; then
    PYTHON_VERSION=$(WINEPREFIX=~/.wine wine python --version 2>&1 | head -1)
    echo "✓ Python is installed in Wine: $PYTHON_VERSION"
    echo ""
    echo "You can now run: ./build_windows.sh"
    exit 0
else
    echo "✗ Python is NOT installed in Wine"
    echo ""
    echo "You have python.exe files in ~/Desktop/python, but they need to be"
    echo "installed in Wine. You need the Python INSTALLER (.exe installer file)."
    echo ""
    echo "If you have the installer file, run:"
    echo "  ./install_python_wine.sh"
    echo ""
    echo "Or manually install it:"
    echo "  WINEPREFIX=~/.wine wine ~/Desktop/python/python-3.x.x-amd64.exe"
    exit 1
fi
