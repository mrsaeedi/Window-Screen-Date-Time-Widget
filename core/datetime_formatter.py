# Formatting of date/time text for each city
"""
core/datetime_formatter.py

Pure formatting helpers that turn a timezone-aware `datetime` into the
strings shown in each clock row: the time string (12h/24h, optional seconds,
Persian digits) and the combined Gregorian + Jalali date string.
"""

from datetime import datetime

import jdatetime

from config.translations import TRANSLATIONS
from core.number_utils import en_to_fa_num


def build_time_format(time_format: int, show_seconds: bool) -> str:
    """Build a strftime pattern for the given hour format (12/24) and
    whether to include seconds."""
    if time_format == 12:
        fmt = "%I:%M"
        if show_seconds:
            fmt += ":%S"
        return fmt + " %p"
    fmt = "%H:%M"
    if show_seconds:
        fmt += ":%S"
    return fmt


def format_time(now_zone: datetime, time_format: int, show_seconds: bool, lang: str) -> str:
    """Render the current time for a given timezone-aware datetime."""
    fmt = build_time_format(time_format, show_seconds)
    time_str = now_zone.strftime(fmt)
    if lang == 'fa':
        if time_format == 12:
            time_str = time_str.replace("AM", "ق.ظ").replace("PM", "ب.ظ")
        time_str = en_to_fa_num(time_str)
    return time_str


def format_date(now_zone: datetime, lang: str) -> str:
    """Render the combined Gregorian + Jalali date string shown below the time."""
    gregorian_str = now_zone.strftime("%B %d")
    jalali_date = jdatetime.date.fromgregorian(date=now_zone.date())
    month_name_fa = TRANSLATIONS['fa']['months_fa'][jalali_date.month - 1]
    jalali_str = f"{jalali_date.day} {month_name_fa}"

    if lang == 'fa':
        return f"{en_to_fa_num(jalali_str)} | {gregorian_str}"
    return f"{gregorian_str} | {jalali_date.day} {month_name_fa}"