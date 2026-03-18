"""
Path helpers for Milo's Story.
Handles both development (run from source) and frozen (PyInstaller) modes.
"""
import os
import sys

def _is_frozen():
    """True when running as a PyInstaller bundle"""
    return getattr(sys, 'frozen', False)

def get_base_path():
    """
    Base path for bundled assets (music, images, etc.).
    When frozen: PyInstaller's extraction folder (sys._MEIPASS).
    When developing: project root (MilosStory/).
    """
    if _is_frozen():
        return sys._MEIPASS
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_data_path():
    """
    Path for writable data (saves, options).
    When frozen: use user app data directory (persists across runs).
    When developing: project data/ folder.
    """
    if _is_frozen():
        if sys.platform == 'darwin':
            base = os.path.expanduser('~/Library/Application Support')
        elif sys.platform == 'win32':
            base = os.environ.get('APPDATA', os.path.expanduser('~'))
        else:
            base = os.path.expanduser('~/.local/share')
        return os.path.normpath(os.path.join(base, "MilosStory"))
    return os.path.normpath(os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data"
    ))
