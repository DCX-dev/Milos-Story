#!/bin/bash
# Build script for Windows executable (using Wine on Mac/Linux)

echo "=========================================="
echo "Building Windows executable for Milo's Story"
echo "=========================================="
echo ""

# Check if Wine is available
echo "[1/7] Checking Wine installation..."
if ! command -v wine &> /dev/null; then
    echo "✗ Error: Wine is not installed."
    echo ""
    echo "Please install Wine first:"
    echo "  On Mac: brew install wine-stable"
    echo "  On Linux: sudo apt-get install wine"
    exit 1
fi
echo "✓ Wine is installed"
echo ""

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    echo "[2/7] Activating virtual environment..."
    source .venv/bin/activate
    echo "✓ Virtual environment activated"
else
    echo "[2/7] No virtual environment found, using system Python"
fi
echo ""

# Check if Python is installed in Wine (Windows Python, not Mac Python)
echo "[3/7] Checking Windows Python installation in Wine..."
echo "  (Note: Mac Python won't work - we need Windows Python in Wine)"

# Try Wine's Python first
PYTHON_CMD="python"
if ! WINEPREFIX=~/.wine wine python --version &> /dev/null 2>&1; then
    # Try using Python from Desktop/python folder if it exists
    DESKTOP_PYTHON="$HOME/Desktop/python/python.exe"
    if [ -f "$DESKTOP_PYTHON" ]; then
        echo "  Trying Python from Desktop/python folder..."
        if WINEPREFIX=~/.wine wine "$DESKTOP_PYTHON" --version &> /dev/null 2>&1; then
            PYTHON_CMD="$DESKTOP_PYTHON"
            PYTHON_VERSION=$(WINEPREFIX=~/.wine wine "$DESKTOP_PYTHON" --version 2>&1 | grep -i "python" | head -1)
            echo "  ✓ Using Python from Desktop/python folder: $PYTHON_VERSION"
        else
            PYTHON_CMD=""
        fi
    else
        PYTHON_CMD=""
    fi
fi

if [ -z "$PYTHON_CMD" ]; then
    echo "✗ Python is not installed in Wine"
    echo ""
    echo "To build Windows executables with Wine, you need to install Python in Wine first."
    echo ""
    echo "EASIEST METHOD - Use the helper script:"
    echo "  ./install_python_wine.sh"
    echo ""
    echo "MANUAL METHOD:"
    echo "1. Download Python Windows installer (64-bit) from:"
    echo "   https://www.python.org/downloads/windows/"
    echo ""
    echo "2. Save it to your Downloads folder"
    echo ""
    echo "3. Run the helper script:"
    echo "   ./install_python_wine.sh"
    echo ""
    echo "   OR manually install:"
    echo "   WINEPREFIX=~/.wine wine ~/Downloads/python-3.XX.X-amd64.exe"
    echo ""
    echo "4. During installation, make sure to check 'Add Python to PATH'"
    echo ""
    echo "ALTERNATIVE - For best results:"
    echo "  - Build on an actual Windows machine (recommended)"
    echo "  - Use a Windows virtual machine"
    echo "  - Use GitHub Actions or similar CI/CD service"
    echo ""
    exit 1
fi

# Display Python version
if [ "$PYTHON_CMD" != "python" ]; then
    PYTHON_VERSION=$(WINEPREFIX=~/.wine wine "$PYTHON_CMD" --version 2>&1 | grep -i "python" | head -1)
    echo "✓ Python is installed: $PYTHON_VERSION"
else
    PYTHON_VERSION=$(WINEPREFIX=~/.wine wine python --version 2>&1 | head -1)
    echo "✓ Python is installed: $PYTHON_VERSION"
fi
echo ""

# Check if PyInstaller is installed in Wine
echo "[4/7] Checking PyInstaller in Wine..."
if ! WINEPREFIX=~/.wine wine "$PYTHON_CMD" -m pip show pyinstaller &> /dev/null 2>&1; then
    echo "  Installing PyInstaller in Wine (this may take a moment)..."
    WINEPREFIX=~/.wine wine "$PYTHON_CMD" -m pip install pyinstaller
    if [ $? -eq 0 ]; then
        echo "✓ PyInstaller installed in Wine"
    else
        echo "✗ Failed to install PyInstaller in Wine"
        exit 1
    fi
else
    echo "✓ PyInstaller already installed in Wine"
fi

# Verify PyInstaller works
if ! WINEPREFIX=~/.wine wine "$PYTHON_CMD" -m pip show pyinstaller &> /dev/null 2>&1; then
    echo "✗ PyInstaller check failed"
    exit 1
fi
echo ""

# Clean previous builds
echo "[5/7] Cleaning previous builds..."
rm -rf build dist *.spec
echo "✓ Cleaned build artifacts"
echo ""

# Prepare data folders
echo "[6/7] Preparing data folders..."
# Note: Windows uses semicolons (;) instead of colons (:) for data separators
# Build data args array properly to handle paths with spaces
DATA_ARGS=()
DATA_ARGS+=("--add-data")
DATA_ARGS+=("player;player")
DATA_ARGS+=("--add-data")
DATA_ARGS+=("save_data;save_data")
echo "  - Including: player/ folder"
echo "  - Including: save_data/ folder"

# Add optional folders if they exist
if [ -d "music" ]; then
    DATA_ARGS+=("--add-data")
    DATA_ARGS+=("music;music")
    echo "  - Including: music/ folder"
fi

if [ -d "world_map" ]; then
    DATA_ARGS+=("--add-data")
    DATA_ARGS+=("world_map;world_map")
    echo "  - Including: world_map/ folder"
fi
echo ""

# Build the Windows executable
echo "[7/7] Building Windows executable with Wine..."
echo "  This may take several minutes..."
echo "  (Note: Wine builds can be slow and may have issues)"
echo ""

# Try building with --no-manifest to avoid Wine limitations
WINEPREFIX=~/.wine wine "$PYTHON_CMD" -m PyInstaller \
    --name "MilosStory" \
    --onefile \
    --windowed \
    "${DATA_ARGS[@]}" \
    --icon=NONE \
    --clean \
    --noconfirm \
    main.py 2>&1 | tee /tmp/pyinstaller_build.log

BUILD_EXIT_CODE=${PIPESTATUS[0]}

# If build failed due to manifest error, try without windowed mode
if [ $BUILD_EXIT_CODE -ne 0 ] && grep -q "EnumResourceTypes\|winmanifest\|win32ctypes" /tmp/pyinstaller_build.log 2>/dev/null; then
    echo ""
    echo "⚠ Wine manifest error detected. Trying alternative build method..."
    echo ""
    
    # Build without windowed mode (console window will show)
    WINEPREFIX=~/.wine wine "$PYTHON_CMD" -m PyInstaller \
        --name "MilosStory" \
        --onefile \
        "${DATA_ARGS[@]}" \
        --icon=NONE \
        --clean \
        --noconfirm \
        main.py
    
    BUILD_EXIT_CODE=$?
fi

BUILD_EXIT_CODE=$?

echo ""
echo "=========================================="
if [ $BUILD_EXIT_CODE -eq 0 ]; then
    echo "✓ Build successful!"
    echo ""
    if [ -f "dist/MilosStory.exe" ]; then
        echo "Executable location: dist/MilosStory.exe"
        echo "File size: $(du -h dist/MilosStory.exe 2>/dev/null | cut -f1 || echo 'unknown')"
    else
        echo "⚠ Warning: MilosStory.exe not found in dist folder"
        echo "  Check the build output above for errors"
    fi
    echo ""
    echo "Note: For best results, build on an actual Windows machine."
else
    echo "✗ Build failed with exit code: $BUILD_EXIT_CODE"
    echo ""
    echo "Common issues:"
    echo "  - Wine may not be properly configured"
    echo "  - Python may not be installed in Wine"
    echo "  - Consider building on an actual Windows machine"
    echo ""
    echo "Check the output above for specific errors."
fi
echo "=========================================="
