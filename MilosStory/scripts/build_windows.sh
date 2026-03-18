#!/bin/bash
# Build script for Windows executable (using Wine on Mac/Linux)
# Uses Python for Windows from ~/Desktop/python if available

# Change to script directory, then to MilosStory project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_DIR" || exit 1

echo "=========================================="
echo "Building Windows executable for Milo's Story"
echo "=========================================="
echo "  Project dir: $PROJECT_DIR"
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

# Use Windows Python from Desktop (Python 3.12 for PyInstaller 5.x compatibility)
for DESKTOP_PYTHON in "$HOME/Desktop/python/python.exe" "$HOME/Desktop/Python/python.exe" "$HOME/Desktop/python312/python.exe"; do
    if [ -f "$DESKTOP_PYTHON" ] && WINEPREFIX=~/.wine wine "$DESKTOP_PYTHON" --version &> /dev/null 2>&1; then
        PYTHON_CMD="$DESKTOP_PYTHON"
        echo "  ✓ Using Windows Python from Desktop: $DESKTOP_PYTHON"
        break
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    echo "✗ Windows Python from Desktop/python is required"
    echo ""
    echo "Place your Windows Python in: ~/Desktop/python/"
    echo "  (Folder must contain python.exe)"
    echo ""
    echo "To install: Download Python for Windows from python.org,"
    echo "  then run: WINEPREFIX=~/.wine wine ~/Downloads/python-3.x.x-amd64.exe"
    echo "  Install to a folder, then copy that folder to ~/Desktop/python/"
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

# Use PyInstaller 6.x (no pkg_resources dependency - 5.x needs setuptools which fails in some Wine setups)
echo "[4/7] Installing PyInstaller..."
WINEPREFIX=~/.wine wine "$PYTHON_CMD" -m pip install --upgrade pip pyinstaller
echo "✓ PyInstaller ready"
echo ""

# Clean previous builds
echo "[5/7] Cleaning previous builds..."
rm -rf build dist *.spec
echo "✓ Cleaned build artifacts"
echo ""

# Prepare data folders (Windows uses semicolon for path separator)
echo "[6/7] Preparing data folders..."
DATA_ARGS=()
if [ -d "assets" ]; then
    DATA_ARGS+=("--add-data")
    DATA_ARGS+=("assets;assets")
    echo "  - Including: assets/ folder (music, player, background)"
fi
if [ ${#DATA_ARGS[@]} -eq 0 ]; then
    echo "✗ Error: assets/ folder not found. Run from MilosStory project directory."
    exit 1
fi
echo ""

# Build the Windows executable
echo "[7/7] Building Windows executable with Wine..."
echo "  This may take several minutes..."
echo "  (Note: Wine builds can be slow and may have issues)"
echo ""

# Build with Wine - try multiple methods due to manifest/Wine compatibility issues
BUILD_LOG="/tmp/pyinstaller_build.log"
[ -d /tmp ] || BUILD_LOG="./pyinstaller_build.log"

# Method 1: Build with Wine patch (avoids EnumResourceTypes error)
echo "  Attempting build (with Wine compatibility patch)..."
WINEPREFIX=~/.wine wine "$PYTHON_CMD" "$PROJECT_DIR/scripts/pyinstaller_wine_fix.py" \
    --name "MilosStory" \
    --onefile \
    --windowed \
    --hidden-import=src.paths \
    "${DATA_ARGS[@]}" \
    --icon=NONE \
    --clean \
    --noconfirm \
    main.py 2>&1 | tee "$BUILD_LOG"

BUILD_EXIT_CODE=${PIPESTATUS[0]}

# Method 2: If manifest/win32ctypes error, try without windowed (console app)
if [ $BUILD_EXIT_CODE -ne 0 ] && grep -qE "EnumResourceTypes|winmanifest|win32ctypes|pywintypes" "$BUILD_LOG" 2>/dev/null; then
    echo ""
    echo "⚠ Manifest error detected. Trying build without windowed mode..."
    echo "  (Result will show a console window when run)"
    echo ""
    
    WINEPREFIX=~/.wine wine "$PYTHON_CMD" "$PROJECT_DIR/scripts/pyinstaller_wine_fix.py" \
        --name "MilosStory" \
        --onefile \
        --hidden-import=src.paths \
        "${DATA_ARGS[@]}" \
        --icon=NONE \
        --clean \
        --noconfirm \
        main.py
    
    BUILD_EXIT_CODE=$?
fi

# Method 3: If still failing, try onedir (folder output) - simpler exe, fewer manifest issues
if [ $BUILD_EXIT_CODE -ne 0 ] && grep -qE "EnumResourceTypes|winmanifest|win32ctypes|pywintypes" "$BUILD_LOG" 2>/dev/null; then
    echo ""
    echo "⚠ Trying onedir mode (output as folder instead of single exe)..."
    echo ""
    
    WINEPREFIX=~/.wine wine "$PYTHON_CMD" "$PROJECT_DIR/scripts/pyinstaller_wine_fix.py" \
        --name "MilosStory" \
        --onedir \
        --windowed \
        --hidden-import=src.paths \
        "${DATA_ARGS[@]}" \
        --icon=NONE \
        --clean \
        --noconfirm \
        main.py
    
    BUILD_EXIT_CODE=$?
fi

echo ""
echo "=========================================="
if [ $BUILD_EXIT_CODE -eq 0 ]; then
    echo "✓ Build successful!"
    echo ""
    if [ -f "dist/MilosStory.exe" ]; then
        echo "Executable: dist/MilosStory.exe"
        echo "File size: $(du -h dist/MilosStory.exe 2>/dev/null | cut -f1 || echo 'unknown')"
    elif [ -f "dist/MilosStory/MilosStory.exe" ]; then
        echo "Executable: dist/MilosStory/MilosStory.exe (onedir build)"
        echo "Include the entire dist/MilosStory/ folder when distributing."
        echo "File size: $(du -sh dist/MilosStory 2>/dev/null | cut -f1 || echo 'unknown')"
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
    echo "  - Wine + PyInstaller 6 has a known EnumResourceTypes manifest error"
    echo "  - RECOMMENDED: Build on an actual Windows machine (no Wine) - it works there"
    echo "  - Copy project to Windows, run: scripts\\build_windows.bat"
    echo ""
    echo "Check the output above for specific errors."
fi
echo "=========================================="
