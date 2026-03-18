"""
Run PyInstaller with a Wine compatibility patch.
Patches winresource.get_resources to catch EnumResourceTypes errors (Wine bug).
Usage: python pyinstaller_wine_fix.py [pyinstaller args...]
"""
import sys

# Load and patch winresource BEFORE PyInstaller imports it
import PyInstaller.utils.win32.winresource as wr
_original_get_resources = wr.get_resources

def _patched_get_resources(filename, res_types, names=None, languages=None):
    try:
        return _original_get_resources(filename, res_types, names, languages)
    except Exception as e:
        err_str = str(e)
        if "EnumResourceTypes" in err_str or "EnumResourceNames" in err_str or "Success" in err_str:
            return []
        raise

wr.get_resources = _patched_get_resources

# Run PyInstaller
if __name__ == "__main__":
    import runpy
    sys.argv = ["pyinstaller"] + sys.argv[1:]
    runpy.run_module("PyInstaller.__main__", run_name="__main__")
