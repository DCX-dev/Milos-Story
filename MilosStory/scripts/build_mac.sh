#!/bin/bash
# Build script for Mac executable

echo "=========================================="
echo "Building Mac executable for Milo's Story"
echo "=========================================="
echo ""

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    echo "[1/5] Activating virtual environment..."
    source .venv/bin/activate
    echo "✓ Virtual environment activated"
else
    echo "[1/5] No virtual environment found, using system Python"
fi
echo ""

# Check if PyInstaller is installed
echo "[2/5] Checking PyInstaller installation..."
if ! python -m pip show pyinstaller &> /dev/null; then
    echo "  Installing PyInstaller..."
    python -m pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org pyinstaller
    if [ $? -eq 0 ]; then
        echo "✓ PyInstaller installed"
    else
        echo "✗ Failed to install PyInstaller"
        echo "  Trying system PyInstaller..."
        if command -v pyinstaller &> /dev/null || python3 -m pip show pyinstaller &> /dev/null; then
            echo "✓ PyInstaller found in system"
        else
            echo "✗ Could not install PyInstaller. Please install manually:"
            echo "  pip install pyinstaller"
            exit 1
        fi
    fi
else
    echo "✓ PyInstaller already installed"
fi
echo ""

# Clean previous builds
echo "[3/5] Cleaning previous builds..."
rm -rf build dist *.spec
echo "✓ Cleaned build artifacts"
echo ""

# Prepare data folders
echo "[4/5] Preparing data folders..."
DATA_ARGS="--add-data player:player --add-data save_data:save_data"
echo "  - Including: player/ folder"
echo "  - Including: save_data/ folder"

# Add optional folders if they exist
if [ -d "music" ]; then
    DATA_ARGS="$DATA_ARGS --add-data music:music"
    echo "  - Including: music/ folder"
fi

if [ -d "world_map" ]; then
    DATA_ARGS="$DATA_ARGS --add-data world_map:world_map"
    echo "  - Including: world_map/ folder"
fi
echo ""

# Build the executable
echo "[5/5] Building executable (this may take a few minutes)..."
echo "  Running PyInstaller..."
echo ""

# Use python -m PyInstaller to ensure we use the right installation
# For macOS, use onedir mode instead of onefile (onefile + windowed doesn't work well on Mac)
python -m PyInstaller --name "MilosStory" \
    --onedir \
    --windowed \
    $DATA_ARGS \
    --clean \
    --noconfirm \
    main.py

BUILD_EXIT_CODE=$?

echo ""
echo "=========================================="
if [ $BUILD_EXIT_CODE -eq 0 ]; then
    echo "✓ Build successful!"
    echo ""
    # Check for .app bundle (onedir windowed mode creates .app)
    if [ -d "dist/MilosStory.app" ]; then
        echo "[6/6] Post-processing app bundle..."
        
        # Remove macOS metadata files (._* files) that can cause signing issues
        echo "  Removing macOS metadata files..."
        find dist/MilosStory.app -name "._*" -type f -delete 2>/dev/null
        find dist/MilosStory.app -name "._*" -type d -exec rm -rf {} + 2>/dev/null
        
        # Remove quarantine attribute if it exists
        echo "  Removing quarantine attribute..."
        xattr -dr com.apple.quarantine dist/MilosStory.app 2>/dev/null || true
        
        # Ad-hoc sign the app bundle (required for distribution)
        echo "  Signing app bundle..."
        codesign --force --deep --sign - dist/MilosStory.app 2>&1 | grep -v "replacing existing signature" || true
        
        # Verify the signature
        if codesign --verify --verbose dist/MilosStory.app 2>/dev/null; then
            echo "  ✓ App bundle signed successfully"
        else
            echo "  ⚠ Warning: Could not verify signature (may need manual signing)"
        fi
        
        echo ""
        echo "Mac App Bundle created: dist/MilosStory.app"
        echo "File size: $(du -sh dist/MilosStory.app 2>/dev/null | cut -f1 || echo 'unknown')"
        echo ""
        echo "For distribution:"
        echo "  Users may need to right-click and select 'Open' the first time"
        echo "  (macOS Gatekeeper requires this for unsigned apps)"
        echo ""
        echo "You can run it with:"
        echo "  open dist/MilosStory.app"
        echo "  or double-click MilosStory.app in Finder"
    elif [ -f "dist/MilosStory" ]; then
        echo "Executable location: dist/MilosStory"
        echo "File size: $(du -h dist/MilosStory 2>/dev/null | cut -f1 || echo 'unknown')"
        echo ""
        echo "You can run it with:"
        echo "  ./dist/MilosStory"
    elif [ -d "dist/MilosStory" ]; then
        echo "Application folder created: dist/MilosStory/"
        echo "File size: $(du -sh dist/MilosStory 2>/dev/null | cut -f1 || echo 'unknown')"
        echo ""
        echo "Run the executable inside:"
        echo "  ./dist/MilosStory/MilosStory"
        echo "  or"
        echo "  open dist/MilosStory/MilosStory"
    fi
else
    echo "✗ Build failed with exit code: $BUILD_EXIT_CODE"
    echo "Check the output above for errors."
fi
echo "=========================================="
