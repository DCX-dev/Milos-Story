@echo off
REM Build Windows executable (run on Windows)
REM Requires: pip install -r requirements.txt pyinstaller

cd /d "%~dp0.."

echo ==========================================
echo Building Windows executable for Milo's Story
echo ==========================================
echo.

echo [1/3] Checking PyInstaller...
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    python -m pip install pyinstaller
)

echo.
echo [2/3] Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist MilosStory.spec del MilosStory.spec

echo.
echo [3/3] Building executable...
python -m PyInstaller --name "MilosStory" ^
    --onefile ^
    --windowed ^
    --hidden-import=src.paths ^
    --add-data "assets;assets" ^
    --clean ^
    --noconfirm ^
    main.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Trying without --windowed (console app)...
    python -m PyInstaller --name "MilosStory" ^
        --onefile ^
        --hidden-import=src.paths ^
        --add-data "assets;assets" ^
        --clean ^
        --noconfirm ^
        main.py
)

echo.
echo ==========================================
if exist "dist\MilosStory.exe" (
    echo Build successful!
    echo Output: dist\MilosStory.exe
) else (
    echo Build failed. Check errors above.
)
echo ==========================================
pause
