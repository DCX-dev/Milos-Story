# Building Executables for Milo's Story

This guide explains how to build Mac and Windows executables for the game.

## Prerequisites

- Python 3.8 or higher
- Virtual environment (recommended)
- All dependencies installed (`pip install -r requirements.txt`)

## Mac Build

### Option 1: Using the build script (Recommended)

```bash
chmod +x build_mac.sh
./build_mac.sh
```

The executable will be created in the `dist` folder as `MilosStory`.

### Option 2: Manual build

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --name "MilosStory" \
    --onefile \
    --windowed \
    --add-data "player:player" \
    --add-data "save_data:save_data" \
    --add-data "music:music" \
    --add-data "world_map:world_map" \
    --clean \
    main.py
```

## Windows Build

### Option 1: Using Wine on Mac/Linux

```bash
# Install Wine first
# On Mac: brew install wine-stable
# On Linux: sudo apt-get install wine

chmod +x build_windows.sh
./build_windows.sh
```

**Note:** Building Windows executables with Wine can be tricky. For best results, build on an actual Windows machine.

### Option 2: Build on Windows Machine

1. Install Python and pip on Windows
2. Install dependencies: `pip install -r requirements.txt`
3. Install PyInstaller: `pip install pyinstaller`
4. Run:

```cmd
pyinstaller --name "MilosStory" ^
    --onefile ^
    --windowed ^
    --add-data "player;player" ^
    --add-data "save_data;save_data" ^
    --add-data "music;music" ^
    --add-data "world_map;world_map" ^
    --clean ^
    main.py
```

### Option 3: Using the spec file

```bash
pyinstaller milos_story.spec
```

## Output

After building, you'll find:
- **Mac**: `dist/MilosStory` (executable file)
- **Windows**: `dist/MilosStory.exe` (executable file)

## Troubleshooting

### Missing assets
If the game can't find images or sounds, make sure all folders (`player`, `music`, `save_data`, `world_map`) are included in the build.

### Console window appears
If you see a console window, make sure `--windowed` flag is used (or `console=False` in the spec file).

### Large file size
The executable includes Python and all dependencies. This is normal. To reduce size, you can:
- Use `--exclude-module` to exclude unused modules
- Use UPX compression (already enabled in spec file)

## Distribution

The executable is standalone and includes everything needed to run the game. You can distribute just the executable file, but make sure:
- The `save_data` folder is created if it doesn't exist (the game will create it automatically)
- Users have write permissions in the game directory for save files
