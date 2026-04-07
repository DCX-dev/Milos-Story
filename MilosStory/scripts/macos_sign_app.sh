#!/bin/bash
# Fix MilosStory.app for Gatekeeper: strip AppleDouble/xattrs, remove broken
# signatures, then ad-hoc sign. Run after PyInstaller (see build_mac.sh).
set -eu

APP="${1:-}"
if [[ -z "$APP" || ! -d "$APP" ]]; then
    echo "Usage: $0 path/to/MilosStory.app"
    exit 1
fi

echo "  [sign] Cleaning metadata in $APP ..."

# Avoid creating ._ files during any copies in this script
export COPYFILE_DISABLE=1
export COPY_EXTENDED_ATTRIBUTES_DISABLE=1

# Remove AppleDouble, trash, and any stray xattrs (quarantine, Finder, etc.)
find "$APP" -name '.DS_Store' -delete 2>/dev/null || true
find "$APP" -name '._*' -print -delete 2>/dev/null || true
xattr -cr "$APP" 2>/dev/null || true

echo "  [sign] Removing old code signatures (fixes broken PyInstaller sign) ..."
codesign --remove-signature "$APP" 2>/dev/null || true
if [[ -f "$APP/Contents/MacOS/MilosStory" ]]; then
    codesign --remove-signature "$APP/Contents/MacOS/MilosStory" 2>/dev/null || true
fi
# PyInstaller puts dylibs/so under Contents/Frameworks or MacOS
find "$APP" -type f \( -name '*.dylib' -o -name '*.so' \) 2>/dev/null | while IFS= read -r f; do
    [[ -f "$f" ]] || continue
    codesign --remove-signature "$f" 2>/dev/null || true
done

echo "  [sign] Ad-hoc signing bundle (deep) ..."
# --timestamp=none avoids ad-hoc timestamp issues; --deep signs nested code
codesign --force --sign - --deep --timestamp=none "$APP"

if codesign --verify --verbose=2 "$APP" 2>/dev/null; then
    echo "  ✓ codesign verify OK"
else
    echo "  ⚠ codesign verify reported an issue; app may still run locally"
fi
