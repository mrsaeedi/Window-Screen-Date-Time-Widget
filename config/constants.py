# CITIES_DB, HOLIDAYS_JALALI, MONTHS_EN_ABBR
"""
config/constants.py

Static reference data used across the app: month abbreviations, the list of
fixed Jalali (Persian) public holidays, and the database of selectable cities
with their IANA timezone names. This module holds pure data only -- no logic,
no Qt imports -- so it can be reused or tested independently of the UI.
"""

# Short English month abbreviations, used as the Gregorian calendar header (e.g. "Jun 2026")
MONTHS_EN_ABBR = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
]

# Fixed-date Jalali public holidays, keyed by (month, day).
# Lunar-based holidays (Eid al-Fitr, Eid al-Adha, Tasua/Ashura, etc.) shift every
# year and would require a precise Hijri conversion table, so they are not
# covered in this version.
HOLIDAYS_JALALI = {
    (1, 1): 'نوروز', (1, 2): 'نوروز', (1, 3): 'نوروز', (1, 4): 'نوروز',
    (1, 12): 'روز جمهوری اسلامی', (1, 13): 'روز طبیعت',
    (3, 14): 'رحلت امام خمینی', (3, 15): 'قیام ۱۵ خرداد',
    (11, 22): 'پیروزی انقلاب اسلامی',
    (12, 29): 'ملی شدن صنعت نفت',
}

# City database: 3-letter code -> display names (fa/en) and IANA timezone id.
CITIES_DB = {
    'TEH': {'fa': 'تهران', 'en': 'Tehran', 'tz': 'Asia/Tehran'},
    'AKL': {'fa': 'اوکلند', 'en': 'Auckland', 'tz': 'Pacific/Auckland'},
    'ATH': {'fa': 'آتن', 'en': 'Athens', 'tz': 'Europe/Athens'},
    'BAG': {'fa': 'بغداد', 'en': 'Baghdad', 'tz': 'Asia/Baghdad'},
    'BAK': {'fa': 'باکو', 'en': 'Baku', 'tz': 'Asia/Baku'},
    'BER': {'fa': 'برلین', 'en': 'Berlin', 'tz': 'Europe/Berlin'},
    'BKK': {'fa': 'بانکوک', 'en': 'Bangkok', 'tz': 'Asia/Bangkok'},
    'BOM': {'fa': 'بمبئی', 'en': 'Mumbai', 'tz': 'Asia/Kolkata'},
    'BRU': {'fa': 'بروکسل', 'en': 'Brussels', 'tz': 'Europe/Brussels'},
    'BUE': {'fa': 'بوئنوس آیرس', 'en': 'Buenos Aires', 'tz': 'America/Argentina/Buenos_Aires'},
    'CAI': {'fa': 'قاهره', 'en': 'Cairo', 'tz': 'Africa/Cairo'},
    'CHI': {'fa': 'شیکاگو', 'en': 'Chicago', 'tz': 'America/Chicago'},
    'KBL': {'fa': 'کابل', 'en': 'Kabul', 'tz': 'Asia/Kabul'},
    'CMN': {'fa': 'کازابلانکا', 'en': 'Casablanca', 'tz': 'Africa/Casablanca'},
    'CPH': {'fa': 'کپنهاگ', 'en': 'Copenhagen', 'tz': 'Europe/Copenhagen'},
    'DOH': {'fa': 'دوحه', 'en': 'Doha', 'tz': 'Asia/Qatar'},
    'DXB': {'fa': 'دبی', 'en': 'Dubai', 'tz': 'Asia/Dubai'},
    'ERE': {'fa': 'ایروان', 'en': 'Yerevan', 'tz': 'Asia/Yerevan'},
    'HEL': {'fa': 'هلسینکی', 'en': 'Helsinki', 'tz': 'Europe/Helsinki'},
    'HKG': {'fa': 'هنگ کنگ', 'en': 'Hong Kong', 'tz': 'Asia/Hong_Kong'},
    'IST': {'fa': 'استانبول', 'en': 'Istanbul', 'tz': 'Europe/Istanbul'},
    'JKT': {'fa': 'جاکارتا', 'en': 'Jakarta', 'tz': 'Asia/Jakarta'},
    'JNB': {'fa': 'ژوهانسبورگ', 'en': 'Johannesburg', 'tz': 'Africa/Johannesburg'},
    'KWI': {'fa': 'کویت', 'en': 'Kuwait', 'tz': 'Asia/Kuwait'},
    'LAX': {'fa': 'لس آنجلس', 'en': 'Los Angeles', 'tz': 'America/Los_Angeles'},
    'LIM': {'fa': 'لیما', 'en': 'Lima', 'tz': 'America/Lima'},
    'LON': {'fa': 'لندن', 'en': 'London', 'tz': 'Europe/London'},
    'LOS': {'fa': 'لاگوس', 'en': 'Lagos', 'tz': 'Africa/Lagos'},
    'MAD': {'fa': 'مادرید', 'en': 'Madrid', 'tz': 'Europe/Madrid'},
    'MCT': {'fa': 'مسقط', 'en': 'Muscat', 'tz': 'Asia/Muscat'},
    'MEL': {'fa': 'ملبورن', 'en': 'Melbourne', 'tz': 'Australia/Melbourne'},
    'MEX': {'fa': 'مکزیکو سیتی', 'en': 'Mexico City', 'tz': 'America/Mexico_City'},
    'MNL': {'fa': 'مانیل', 'en': 'Manila', 'tz': 'Asia/Manila'},
    'MSC': {'fa': 'مسکو', 'en': 'Moscow', 'tz': 'Europe/Moscow'},
    'NBO': {'fa': 'نایروبی', 'en': 'Nairobi', 'tz': 'Africa/Nairobi'},
    'NYC': {'fa': 'نیویورک', 'en': 'New York', 'tz': 'America/New_York'},
    'OSL': {'fa': 'اسلو', 'en': 'Oslo', 'tz': 'Europe/Oslo'},
    'PAR': {'fa': 'پاریس', 'en': 'Paris', 'tz': 'Europe/Paris'},
    'ROM': {'fa': 'رم', 'en': 'Rome', 'tz': 'Europe/Rome'},
    'SAO': {'fa': 'سائوپائولو', 'en': 'São Paulo', 'tz': 'America/Sao_Paulo'},
    'SCL': {'fa': 'سانتیاگو', 'en': 'Santiago', 'tz': 'America/Santiago'},
    'SEL': {'fa': 'سئول', 'en': 'Seoul', 'tz': 'Asia/Seoul'},
    'SHA': {'fa': 'شانگهای', 'en': 'Shanghai', 'tz': 'Asia/Shanghai'},
    'SIN': {'fa': 'سنگاپور', 'en': 'Singapore', 'tz': 'Asia/Singapore'},
    'STO': {'fa': 'استکهلم', 'en': 'Stockholm', 'tz': 'Europe/Stockholm'},
    'SYD': {'fa': 'سیدنی', 'en': 'Sydney', 'tz': 'Australia/Sydney'},
    'TOR': {'fa': 'تورنتو', 'en': 'Toronto', 'tz': 'America/Toronto'},
    'TYO': {'fa': 'توکیو', 'en': 'Tokyo', 'tz': 'Asia/Tokyo'},
    'VIE': {'fa': 'وین', 'en': 'Vienna', 'tz': 'Europe/Vienna'},
    'ISB': {'fa': 'اسلام‌آباد', 'en': 'Islamabad', 'tz': 'Asia/Karachi'},
    'ASB': {'fa': 'عشق‌آباد', 'en': 'Ashgabat', 'tz': 'Asia/Ashgabat'},
    'RUH': {'fa': 'ریاض', 'en': 'Riyadh', 'tz': 'Asia/Riyadh'},
    'BAH': {'fa': 'منامه', 'en': 'Manama', 'tz': 'Asia/Bahrain'},
    'DYU': {'fa': 'دوشنبه', 'en': 'Dushanbe', 'tz': 'Asia/Dushanbe'},
    'WAW': {'fa': 'ورشو', 'en': 'Warsaw', 'tz': 'Europe/Warsaw'},
}