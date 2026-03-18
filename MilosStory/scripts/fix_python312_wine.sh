#!/bin/bash
# Fix Python 3.12 in Wine - install setuptools (pkg_resources) required by PyInstaller
# Run this if you get "ModuleNotFoundError: No module named 'pkg_resources'"

for PY in "$HOME/Desktop/python312/python.exe" "$HOME/Desktop/python/python.exe"; do
    if [ -f "$PY" ]; then
        echo "Installing setuptools for: $PY"
        WINEPREFIX=~/.wine wine "$PY" -m pip install --upgrade pip setuptools
        echo ""
        echo "Verifying..."
        if WINEPREFIX=~/.wine wine "$PY" -c "import pkg_resources; print('OK')"; then
            echo "✓ setuptools installed successfully"
            echo "Run ./scripts/build_windows.sh again"
        else
            echo "✗ Still failing - try running from Windows or use GitHub Actions"
        fi
        exit 0
    fi
done
echo "✗ Python not found in ~/Desktop/python312 or ~/Desktop/python"
exit 1
