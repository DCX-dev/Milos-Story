#!/bin/bash
# Script to continue building Windows executable after Python installation

echo "Checking if Python is installed in Wine..."
echo ""

if WINEPREFIX=~/.wine wine python --version &> /dev/null 2>&1; then
    PYTHON_VERSION=$(WINEPREFIX=~/.wine wine python --version 2>&1 | head -1)
    echo "✓ Python is installed: $PYTHON_VERSION"
    echo ""
    echo "Starting Windows build..."
    echo ""
    ./build_windows.sh
else
    echo "✗ Python is not yet installed in Wine"
    echo ""
    echo "Please complete the Python installation:"
    echo "  1. In the Python installer window, check 'Add Python to PATH'"
    echo "  2. Click 'Install Now'"
    echo "  3. Wait for installation to complete"
    echo "  4. Then run this script again: ./continue_build.sh"
    echo ""
    echo "Or run the build script directly: ./build_windows.sh"
fi
