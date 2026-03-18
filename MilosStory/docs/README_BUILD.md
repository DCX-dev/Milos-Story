# Building Executables for Milo's Story

## Mac Application (.app)

From the **MilosStory** project directory:

```bash
./scripts/build_mac.sh
```

**Output:** `dist/MilosStory.app` — double-click to run or drag to Applications.

- First run: Right-click → Open (macOS Gatekeeper for unsigned apps)
- Save files: `~/Library/Application Support/MilosStory/`

## Windows Executable (.exe)

### Option A: GitHub Actions (recommended — always works)

1. Push your project to GitHub
2. Go to **Actions** tab → **Build Windows EXE** → **Run workflow**
3. When done, download **MilosStory-Windows** from the workflow run

Uses real Windows in the cloud — no Wine, no manifest errors.

### Option B: On Windows (native)

```cmd
scripts\build_windows.bat
```

**Output:** `dist\MilosStory.exe`

### Option C: Docker on Mac (alternative to Wine)

```bash
./scripts/build_windows_docker.sh
```

Uses `kivy/python-winpython` container — sometimes works when local Wine fails.

### Option D: Wine + Desktop Python on Mac

```bash
./scripts/build_windows.sh
```

Uses `~/Desktop/python/python.exe`. May fail with manifest error — try Option A or C.

### Option B: Install Python in Wine First

1. Download Python for Windows (64-bit): https://www.python.org/downloads/windows/
2. Run: `./scripts/install_python_wine.sh`
3. During install: check **Add Python to PATH**
4. Build: `./scripts/build_windows.sh`

### Option C: Build on a Windows Machine

1. Copy the project to Windows
2. Install Python and run: `pip install -r requirements.txt pyinstaller`
3. From the MilosStory folder:
   ```cmd
   pyinstaller --name "MilosStory" --onefile --windowed --add-data "assets;assets" --hidden-import=src.paths main.py
   ```

## Summary

| Platform | Command | Output |
|----------|---------|--------|
| Mac | `./scripts/build_mac.sh` | `dist/MilosStory.app` |
| Windows (Wine) | `./scripts/build_windows.sh` | `dist/MilosStory.exe` |
