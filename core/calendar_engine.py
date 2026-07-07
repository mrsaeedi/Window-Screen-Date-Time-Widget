# Pure calendar calculations for Jalali and Gregorian calendars
"""
core/calendar_engine.py

Pure calendar math for both calendar systems (Gregorian and Jalali/Persian):
month length, starting weekday, today/holiday checks, and building the flat
list of day cells that `CalendarPanel` turns into a grid. Nothing here
imports Qt, so this module can be unit tested with plain assertions.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Tuple
import calendar

import jdatetime

from config.constants import HOLIDAYS_JALALI, MONTHS_EN_ABBR
from config.translations import TRANSLATIONS


@dataclass
class DayCell:
    """One cell in the calendar grid. `day` is None for the leading blank
    cells that appear before the 1st of the month."""
    day: Optional[int]
    is_today: bool = False
    is_holiday: bool = False
    holiday_name: Optional[str] = None


def get_today_dates() -> Tuple[object, object]:
    """Return (gregorian_date, jalali_date) for "now"."""
    today_g = datetime.now().date()
    today_j = jdatetime.date.fromgregorian(date=today_g)
    return today_g, today_j


def is_current_month(year: int, month: int, calendar_type: str) -> bool:
    """Whether (year, month) in the given calendar system is the current month."""
    today_g, today_j = get_today_dates()
    if calendar_type == 'jalali':
        return year == today_j.year and month == today_j.month
    return year == today_g.year and month == today_g.month


def shift_month(year: int, month: int, delta: int) -> Tuple[int, int]:
    """Move `delta` months forward (positive) or backward (negative),
    rolling the year over as needed."""
    month += delta
    while month > 12:
        month -= 12
        year += 1
    while month < 1:
        month += 12
        year -= 1
    return year, month


def get_days_in_month(year: int, month: int, calendar_type: str) -> int:
    """Number of days in the given month."""
    if calendar_type == 'jalali':
        if month <= 6:
            return 31
        if month <= 11:
            return 30
        try:
            jdatetime.date(year, 12, 30)
            return 30
        except ValueError:
            return 29
    return calendar.monthrange(year, month)[1]


def get_start_column(year: int, month: int, calendar_type: str) -> int:
    """Weekday column (0-6) of the 1st of the month.
    Jalali weeks start on Saturday (col 0) ... Friday (col 6).
    Gregorian weeks start on Sunday (col 0) ... Saturday (col 6).
    """
    if calendar_type == 'jalali':
        return jdatetime.date(year, month, 1).weekday()
    weekday_first, _ = calendar.monthrange(year, month)
    return (weekday_first + 1) % 7


def get_weekend_column(calendar_type: str) -> int:
    """Index of the weekly day-off column: Friday for Jalali, Sunday for
    Gregorian."""
    return 6 if calendar_type == 'jalali' else 0


def get_month_title(year: int, month: int, calendar_type: str) -> str:
    """Human-readable "Month Year" header, e.g. 'دی 1405' or 'Jun 2026'."""
    if calendar_type == 'jalali':
        month_name = TRANSLATIONS['fa']['months_fa'][month - 1]
        return f"{month_name} {year}"
    return f"{MONTHS_EN_ABBR[month - 1]} {year}"


def build_month_grid(year: int, month: int, calendar_type: str) -> List[DayCell]:
    """Build the flat list of `DayCell`s for one month, including the
    leading blank cells needed to align the 1st under the correct weekday
    column."""
    today_g, today_j = get_today_dates()
    total_days = get_days_in_month(year, month, calendar_type)
    start_col = get_start_column(year, month, calendar_type)
    weekend_col = get_weekend_column(calendar_type)

    cells: List[DayCell] = [DayCell(day=None) for _ in range(start_col)]

    for day in range(1, total_days + 1):
        if calendar_type == 'jalali':
            is_today = (year == today_j.year and month == today_j.month and day == today_j.day)
            holiday_name = HOLIDAYS_JALALI.get((month, day))
        else:
            is_today = (year == today_g.year and month == today_g.month and day == today_g.day)
            holiday_name = None

        col = len(cells) % 7
        is_holiday = (col == weekend_col) or (holiday_name is not None)

        cells.append(DayCell(day=day, is_today=is_today, is_holiday=is_holiday, holiday_name=holiday_name))

    return cells