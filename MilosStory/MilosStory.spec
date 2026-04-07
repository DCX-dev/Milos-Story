# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for Milo's Story (macOS .app bundle).
# Build from MilosStory/:  ./scripts/build_mac.sh   or   pyinstaller MilosStory.spec

import os

from PyInstaller.utils.hooks import collect_submodules, collect_data_files

# PyInstaller may pass SPECPATH as a relative name; cwd is usually the spec's directory.
_cand = os.path.dirname(os.path.abspath(SPECPATH))
if os.path.isfile(os.path.join(_cand, 'main.py')):
    spec_dir = _cand
elif os.path.isfile(os.path.join(os.getcwd(), 'main.py')):
    spec_dir = os.getcwd()
else:
    raise RuntimeError(
        'main.py not found. Run PyInstaller from the MilosStory folder '
        '(same folder as main.py and MilosStory.spec).'
    )

datas = [(os.path.join(spec_dir, 'assets'), 'assets')]

try:
    datas += collect_data_files('pygame')
except Exception:
    pass

hiddenimports = [
    'src.paths',
    'src.main',
    'src.player',
    'src.enemy',
    'src.arrow',
    'src.boss',
    'src.chest',
    'src.game_platform',
    'src.level_system',
    'src.rock',
    'src.save_system',
    'jaraco.text',
    'PIL',
    'PIL.Image',
]
hiddenimports += collect_submodules('screens')
hiddenimports += collect_submodules('jaraco')

a = Analysis(
    [os.path.join(spec_dir, 'main.py')],
    pathex=[spec_dir],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='MilosStory',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='MilosStory',
)

app = BUNDLE(
    coll,
    name='MilosStory.app',
    icon=None,
    bundle_identifier='com.teambananalabs.milosstory',
    info_plist={
        'CFBundleName': 'MilosStory',
        'CFBundleDisplayName': "Milo's Story",
        'CFBundleExecutable': 'MilosStory',
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '10.13',
    },
)
