# Configuration file path loader/saver
"""
config/settings_store.py

Everything related to persisted app configuration:
- resolving bundled resource paths (works both in dev and in a PyInstaller build)
- the on-disk location of the settings file under %APPDATA%
- the default configuration values
- loading/saving the config as JSON

This module has no Qt dependency, so it can be tested with plain dict/JSON
assertions.
"""

import os
import sys
import json

DEFAULT_CONFIG = {
    'always_on_top': True,
    'run_at_startup': True,
    'show_seconds': True,
    'time_format': 24,
    'calendar_type': 'jalali',
    'lang': 'en',
    'font_size': 16,
    'opacity': 0.85,
    'selected_cities': ['TEH'],
    'show_title': False,
    'show_date': True,
    'only_time': True,
    'show_timer_section': False,
    'view_mode': 'clock',  # 'clock' or 'calendar'
}

_APP_DATA_DIR = os.path.join(os.getenv('APPDATA', os.path.expanduser('~')), 'TimeWidget')
os.makedirs(_APP_DATA_DIR, exist_ok=True)
CONFIG_FILE = os.path.join(_APP_DATA_DIR, 'widget_config.json')


def resource_path(relative_path: str) -> str:
    """Resolve the path to a bundled resource (e.g. an icon), whether the app
    is running from source or from a frozen PyInstaller executable."""
    try:
        base_path = sys._MEIPASS  # type: ignore[attr-defined]
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def load_config() -> dict:
    """Load the saved config and merge it over the defaults, so any setting
    added in a later version always has a sane fallback for older config
    files."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return {**DEFAULT_CONFIG, **json.load(f)}
        except Exception:
            pass
    return DEFAULT_CONFIG.copy()


def save_config(config: dict) -> None:
    """Persist the given config dict to disk as UTF-8 JSON."""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)