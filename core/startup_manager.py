# Windows startup registration utilities
"""
core/startup_manager.py

Registers or unregisters the app to run automatically when Windows starts,
by writing/removing a value under the current user's Run registry key.
This is a no-op on non-Windows platforms.
"""

import sys
import os

_APP_NAME = "TimeWidget"
_KEY_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"


def set_windows_startup(enabled: bool) -> None:
    """Enable or disable launching the app automatically on Windows sign-in."""
    if sys.platform != 'win32':
        return

    import winreg  # local import: this module only exists on Windows

    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, _KEY_PATH, 0, winreg.KEY_SET_VALUE)
        if enabled:
            if getattr(sys, 'frozen', False):
                command = f'"{sys.executable}"'
            else:
                command = f'"{sys.executable}" "{os.path.abspath(sys.argv[0])}"'
            winreg.SetValueEx(key, _APP_NAME, 0, winreg.REG_SZ, command)
        else:
            try:
                winreg.DeleteValue(key, _APP_NAME)
            except FileNotFoundError:
                pass
        winreg.CloseKey(key)
    except Exception as e:
        print(f"Error modifying Startup Registry: {e}")