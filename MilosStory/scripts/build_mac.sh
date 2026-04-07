#!/bin/bash
# Build script for Mac executable
# Run from project root or MilosStory directory

# Do not create AppleDouble (._*) files during build — they break codesign / Gatekeeper
export COPYFILE_DISABLE=1
export COPY_EXTENDED_ATTRIBUTES_DISABLE=1

# Change to script directory, then to MilosStory project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_DIR" || exit 1

echo "=========================================="
echo "Building Mac executable for Milo's Story"
echo "=========================================="
echo "  Project dir: $PROJECT_DIR"
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

# Check if PyInstaller is installed (prefer python3 on Mac)
PY_CMD="python"
if ! command -v python &> /dev/null && command -v python3 &> /dev/null; then
    PY_CMD="python3"
fi
echo "[2/5] Checking PyInstaller and jaraco.text..."
# jaraco.text is required by pkg_resources (used by pygame) - must be installed for PyInstaller
if ! $PY_CMD -m pip show jaraco.text &> /dev/null; then
    echo "  Installing jaraco.text (required for pkg_resources)..."
    $PY_CMD -m pip install --quiet jaraco.text
fi
if ! $PY_CMD -m pip show pyinstaller &> /dev/null; then
    echo "  Installing PyInstaller..."
    $PY_CMD -m pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org pyinstaller
    if [ $? -eq 0 ]; then
        echo "✓ PyInstaller installed"
    else
        echo "✗ Failed to install PyInstaller"
        echo "  Trying system PyInstaller..."
        if command -v pyinstaller &> /dev/null || $PY_CMD -m pip show pyinstaller &> /dev/null; then
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

# Clean previous builds (keep MilosStory.spec in repo)
echo "[3/5] Cleaning previous builds..."
rm -rf build dist
echo "✓ Cleaned build artifacts"
echo ""

# Prepare data folders (assets contains music, player, background)
echo "[4/5] Preparing data folders..."
DATA_ARGS=""
if [ -d "assets" ]; then
    DATA_ARGS="--add-data assets:assets"
    echo "  - Including: assets/ folder (music, player, background)"
fi
if [ -z "$DATA_ARGS" ]; then
    echo "✗ Error: assets/ folder not found. Run from MilosStory project directory."
    exit 1
fi
echo ""

# Build the executable
echo "[5/5] Building executable (this may take a few minutes)..."
echo "  Running PyInstaller..."
echo ""

# Prefer checked-in spec (reliable .app bundle); fallback to CLI
if [ -f "MilosStory.spec" ]; then
    echo "  Using MilosStory.spec"
    $PY_CMD -m PyInstaller --clean --noconfirm MilosStory.spec
else
    echo "  Using CLI (no MilosStory.spec found)"
    $PY_CMD -m PyInstaller --name "MilosStory" \
        --onedir \
        --windowed \
        --hidden-import=src.paths \
        --hidden-import=jaraco.text \
        --collect-submodules=jaraco \
        $DATA_ARGS \
        --clean \
        --noconfirm \
        main.py
fi

BUILD_EXIT_CODE=$?

echo ""
echo "=========================================="
if [ $BUILD_EXIT_CODE -eq 0 ]; then
    echo "✓ Build successful!"
    echo ""
    # Check for .app bundle (onedir windowed mode creates .app)
    if [ -d "dist/MilosStory.app" ]; then
        echo "[6/6] Post-processing app bundle (Gatekeeper-safe)..."
        
        SIGN_SCRIPT="$SCRIPT_DIR/macos_sign_app.sh"
        if [ -f "$SIGN_SCRIPT" ]; then
            chmod +x "$SIGN_SCRIPT" 2>/dev/null || true
            bash "$SIGN_SCRIPT" "$PROJECT_DIR/dist/MilosStory.app"
        else
            echo "  ⚠ macos_sign_app.sh missing; using basic cleanup + sign"
            find dist/MilosStory.app -name '.DS_Store' -delete 2>/dev/null || true
            find dist/MilosStory.app -name '._*' -delete 2>/dev/null || true
            xattr -cr dist/MilosStory.app 2>/dev/null || true
            codesign --remove-signature dist/MilosStory.app 2>/dev/null || true
            codesign --force --sign - --deep --timestamp=none dist/MilosStory.app
        fi
        
        # User-facing note next to the app (zip dist/ with this file for players)
        cat > dist/README_MAC_FIRST_OPEN.txt << 'EOF'
Milo's Story — first launch on Mac
==================================

If macOS says the app "is damaged" or "may contain malware" and you click Cancel,
macOS often will NOT show "Open Anyway" in Privacy & Security. That is normal.

Fix (clears the download quarantine and bad metadata):

1. Open Terminal (Cmd+Space, type Terminal).

2. Run BOTH lines below. Replace the path if your app is not in Downloads:

   xattr -cr ~/Downloads/MilosStory.app
   open ~/Downloads/MilosStory.app

   Tip: type "xattr -cr " (with a space), then drag MilosStory.app into Terminal
   to paste its full path, then press Enter.

3. If a dialog appears, click Open — not Cancel.

4. Or: right-click MilosStory.app → Open → Open.

Saves and options: ~/Library/Application Support/MilosStory/
EOF
        
        echo ""
        echo "Mac App Bundle created: dist/MilosStory.app"
        echo "File size: $(du -sh dist/MilosStory.app 2>/dev/null | cut -f1 || echo 'unknown')"
        echo ""
        echo "Also created: dist/README_MAC_FIRST_OPEN.txt (share with players)"
        echo ""
        echo "Test locally:"
        echo "  open dist/MilosStory.app"
        echo ""
        echo "After copying from another Mac or the internet, run:"
        echo "  xattr -cr dist/MilosStory.app"
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
