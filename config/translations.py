# TRANSLATIONS dictionary for fa/en
"""
config/translations.py

All user-facing strings for the two supported languages (Persian and
English), including month names and week-day abbreviations for both
calendar systems. Keeping every translation in one dictionary makes it
trivial to add a new language later without touching any UI code.
"""

TRANSLATIONS = {
    'fa': {
        'title_text': 'زمان',
        'settings': 'تنظیمات ویجت', 'close': 'خروج', 'minimize': 'کوچک کردن',
        'always_on_top': 'همیشه رو باشد (Always on Top)', 'show_seconds': 'نمایش ثانیه',
        'time_format': 'فرمت زمان', 'lang': 'زبان (Language)', 'font_size': 'اندازه فونت',
        'opacity': 'میزان شفافیت', 'cities': 'انتخاب شهرها (لیست اسکرول)', 'save': 'ذخیره تنظیمات',
        'show_title': 'نمایش عنوان ویجت («زمان»)', 'show_date': 'نمایش تاریخ زیر ساعت',
        'only_time': 'فقط زمان (پنهان کردن نام شهر در حالت تک‌شهری)',
        'run_at_startup': 'اجرا همزمان با روشن شدن سیستم (Startup)',
        'timer': 'زمان‌سنج',
        'calendar': 'تقویم',
        'back_to_clock': 'بازگشت به زمان',
        'cal_type': 'نوع تقویم پیش‌فرض',
        'shamsi': 'شمسی',
        'miladi': 'میلادی',
        'months_fa': ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند'],
        'months_en': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
        'week_days_fa': ['ش', 'ی', 'د', 'س', 'چ', 'پ', 'ج'],
        'week_days_en': ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'],
    },
    'en': {
        'title_text': 'Time',
        'settings': 'Widget Settings', 'close': 'Close', 'minimize': 'Minimize',
        'always_on_top': 'Always on Top', 'show_seconds': 'Show Seconds',
        'time_format': 'Time Format', 'lang': 'Language', 'font_size': 'Font Size',
        'opacity': 'Opacity', 'cities': 'Cities List (Scrollable)', 'save': 'Save',
        'show_title': 'Show Widget Title ("Time")', 'show_date': 'Show Date below Time',
        'only_time': 'Only Time (Hide city name in single mode)',
        'run_at_startup': 'Run at Windows Startup',
        'timer': 'Timer',
        'calendar': 'Calendar',
        'back_to_clock': 'Back to Clock',
        'cal_type': 'Default Calendar',
        'shamsi': 'Persian (Jalali)',
        'miladi': 'Gregorian',
        'months_fa': ['Farvardin', 'Ordibehesht', 'Khordad', 'Tir', 'Mordad', 'Shahrivar', 'Mehr', 'Aban', 'Azar', 'Dey', 'Bahman', 'Esfand'],
        'months_en': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
        'week_days_fa': ['Sa', 'Su', 'Mo', 'Tu', 'We', 'Th', 'Fr'],
        'week_days_en': ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'],
    },
}