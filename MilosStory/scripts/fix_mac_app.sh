#!/bin/bash
# Fix Gatekeeper issues on MilosStory.app (quarantine, broken signature, ._ files).
# Usage: ./scripts/fix_mac_app.sh [path/to/MilosStory.app]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_NAME="MilosStory.app"

if [ -n "$1" ]; then
    APP_PATH="$1"
elif [ -d "./$APP_NAME" ]; then
    APP_PATH="./$APP_NAME"
else
    echo "Usage: $0 /path/to/MilosStory.app"
    echo "   Or place $APP_NAME in the current directory and run with no arguments."
    exit 1
fi

if [ ! -d "$APP_PATH" ]; then
    echo "Error: $APP_PATH not found."
    exit 1
fi

echo "Fixing: $APP_PATH"
export COPYFILE_DISABLE=1
export COPY_EXTENDED_ATTRIBUTES_DISABLE=1

SIGN_SCRIPT="$SCRIPT_DIR/macos_sign_app.sh"
if [ -f "$SIGN_SCRIPT" ]; then
    chmod +x "$SIGN_SCRIPT" 2>/dev/null || true
    bash "$SIGN_SCRIPT" "$APP_PATH"
else
    echo "Warning: macos_sign_app.sh not found; applying minimal fix..."
    find "$APP_PATH" -name '.DS_Store' -delete 2>/dev/null || true
    find "$APP_PATH" -name '._*' -delete 2>/dev/null || true
    xattr -cr "$APP_PATH" 2>/dev/null || true
    codesign --remove-signature "$APP_PATH" 2>/dev/null || true
    codesign --force --sign - --deep --timestamp=none "$APP_PATH"
fi

echo ""
echo "Done. Try: open \"$APP_PATH\""
echo "Or right-click the app → Open."
