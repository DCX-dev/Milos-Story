#!/bin/bash
# Helper script to fix "damaged" app error on macOS
# Run this script after downloading MilosStory.app

APP_NAME="MilosStory.app"

echo "=========================================="
echo "Fixing MilosStory.app for macOS"
echo "=========================================="
echo ""

# Check if app exists in current directory
if [ ! -d "$APP_NAME" ]; then
    echo "Error: $APP_NAME not found in current directory."
    echo ""
    echo "Usage:"
    echo "  1. Place this script in the same folder as $APP_NAME"
    echo "  2. Run: ./fix_mac_app.sh"
    echo ""
    echo "Or specify the path:"
    echo "  ./fix_mac_app.sh /path/to/$APP_NAME"
    exit 1
fi

# Allow user to specify path as argument
if [ -n "$1" ]; then
    APP_PATH="$1"
else
    APP_PATH="./$APP_NAME"
fi

# Check if the specified path exists
if [ ! -d "$APP_PATH" ]; then
    echo "Error: $APP_PATH not found."
    exit 1
fi

echo "Processing: $APP_PATH"
echo ""

# Remove macOS metadata files
echo "[1/3] Removing macOS metadata files..."
find "$APP_PATH" -name "._*" -type f -delete 2>/dev/null
find "$APP_PATH" -name "._*" -type d -exec rm -rf {} + 2>/dev/null
echo "  ✓ Metadata files removed"

# Remove quarantine attribute
echo "[2/3] Removing quarantine attribute..."
xattr -dr com.apple.quarantine "$APP_PATH" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "  ✓ Quarantine attribute removed"
else
    echo "  ⚠ Could not remove quarantine (may not be needed)"
fi

# Ad-hoc sign the app
echo "[3/3] Signing app bundle..."
codesign --force --deep --sign - "$APP_PATH" 2>&1 | grep -v "replacing existing signature" || true
if codesign --verify --verbose "$APP_PATH" 2>/dev/null; then
    echo "  ✓ App signed successfully"
else
    echo "  ⚠ Warning: Could not verify signature"
fi

echo ""
echo "=========================================="
echo "✓ Done! You can now open $APP_NAME"
echo ""
echo "To open the app:"
echo "  Right-click $APP_NAME and select 'Open'"
echo "  Or double-click it (may need to right-click first time)"
echo "=========================================="
