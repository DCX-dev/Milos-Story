#!/bin/bash
# Build Windows .exe using Docker + Wine (alternative to local Wine - sometimes works when local fails)
# Requires: Docker Desktop installed

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_DIR" || exit 1

echo "=========================================="
echo "Building Windows EXE via Docker (kivy/python-winpython)"
echo "=========================================="
echo ""

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "✗ Docker is not installed. Install Docker Desktop from docker.com"
    exit 1
fi

echo "[1/4] Pulling Docker image..."
docker pull kivy/python-winpython:3.11

echo ""
echo "[2/4] Installing dependencies in container..."
docker run --rm -v "$PROJECT_DIR:/app" -w /app kivy/python-winpython:3.11 \
    pip install -r requirements.txt pyinstaller -q

echo ""
echo "[3/4] Building EXE (this may take a few minutes)..."
docker run --rm -v "$PROJECT_DIR:/app" -w /app kivy/python-winpython:3.11 \
    pyinstaller --name "MilosStory" --onefile --windowed \
    --hidden-import=src.paths --add-data "assets;assets" \
    --clean --noconfirm main.py

BUILD_EXIT=$?

echo ""
echo "=========================================="
if [ $BUILD_EXIT -eq 0 ] && [ -f "dist/MilosStory.exe" ]; then
    echo "✓ Build successful!"
    echo "  Output: dist/MilosStory.exe"
else
    echo "✗ Build failed (exit code: $BUILD_EXIT)"
fi
echo "=========================================="
