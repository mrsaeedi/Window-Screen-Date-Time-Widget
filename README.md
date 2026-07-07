<p align="center">
  <img src="https://img.shields.io/github/v/release/mrsaeedi/Window-Screen-Date-Time-Widget?style=flat-square&color=blue" alt="release">
  <img src="https://img.shields.io/github/downloads/mrsaeedi/Window-Screen-Date-Time-Widget/total?style=flat-square&color=green" alt="downloads">
  <img src="https://img.shields.io/github/license/mrsaeedi/Window-Screen-Date-Time-Widget?style=flat-square&color=orange" alt="license">
  <img src="https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python" alt="python">
  <img src="https://img.shields.io/badge/PyQt-6-brightgreen?style=flat-square&logo=qt" alt="PyQt6">
</p>

<p align="center">
  <a href="#-english">🇬🇧 English</a> &nbsp;•&nbsp; <a href="#-فارسی">🇮🇷 فارسی</a>
</p>

<p align="center">
  <img src="assets/screenshot.png" alt="Window Screen Date Time Widget Preview" width="600">
</p>

---

## 🇬🇧 English

**A minimal, elegant desktop date & time widget for Windows.**
Built with Python and PyQt6 · Supports both Jalali (Persian) and Gregorian calendars · Lives quietly on your desktop.

### ✨ Features

- 🕰️ **Multiple live clocks** from any city you pick, add or remove them anytime.
- 📅 **Full month calendar view** — browse forward/backward, jump back to today, with Jalali holidays highlighted. *(new in 1.1.0)*
- 🗓️ **Dual calendar support** — Jalali (Shamsi) and Gregorian, switchable from settings.
- 🪟 **Frameless floating widget** — draggable, adjustable opacity, always-on-top.
- ⏱️ **Built-in stopwatch** — open/close independently from the clock view.
- 🚀 **Launch on Windows startup**, toggleable from Settings.
- 💾 **Config stored safely** under `AppData\Roaming`, so updates never wipe your settings.

### 📥 Download (Windows, no Python required)

Grab the latest installer from the [**Releases**](https://github.com/mrsaeedi/Window-Screen-Date-Time-Widget/releases) page:

1. Download the latest `.exe` installer.
2. Run it and follow the setup steps.
3. Launch it from the Start Menu, or let it start automatically with Windows.

> **Note:** the download counter badge above reflects downloads across all published GitHub Releases.

### 🛠️ Developer Guide

#### Prerequisites
- Python 3.9+
- Git (optional)

#### 1. Clone the repository
```bash
git clone https://github.com/mrsaeedi/Window-Screen-Date-Time-Widget.git
cd Window-Screen-Date-Time-Widget
```

#### 2. Create a virtual environment
```bash
python -m venv venv
# Windows CMD
venv\Scripts\activate
# PowerShell
.\venv\Scripts\Activate.ps1
```

#### 3. Install dependencies
```bash
pip install -r requirements.txt
```

#### 4. Run in development mode
```bash
python main.pyw
```

### 📁 Project Structure

```
screen_time/
├── main.pyw                    # Application entry point
├── config/                     # Static data & persisted settings (no logic)
│   ├── constants.py             # Cities database, holidays, month names
│   ├── translations.py          # fa/en UI strings
│   └── settings_store.py        # Load/save JSON config under AppData
├── core/                       # Pure business logic (no Qt dependency)
│   ├── calendar_engine.py       # Jalali/Gregorian month grid math
│   ├── datetime_formatter.py    # Time/date string formatting
│   ├── number_utils.py          # EN → FA digit conversion
│   └── startup_manager.py       # Windows "run at startup" registration
├── ui/                          # Presentation layer (PyQt6)
│   ├── clock_widget.py           # Main window (orchestrator)
│   ├── settings_dialog.py        # Settings dialog
│   └── components/
│       ├── clock_row.py           # One city's time/date row
│       ├── timer_panel.py         # Stopwatch panel
│       └── calendar_panel.py      # Month calendar panel
├── assets/
│   └── screenshot.png            # Preview image for README
├── requirements.txt
├── LICENSE
└── README.md
```

### 🎨 Notes for Contributors
- **UI styling**: handled via `setStyleSheet` / QSS, mostly inside `ui/clock_widget.py` and `ui/components/*`.
- **Settings**: stored as JSON in `AppData\Roaming\TimeWidget`, preserved across updates.
- **Adding a city**: add an entry to `CITIES_DB` in `config/constants.py` with its IANA timezone name — no other file needs touching.

### 🗒️ Changelog
- **v1.1.0** — Added full calendar view (Jalali + Gregorian, holiday highlights, month navigation), modularized the entire codebase into `config/ / core/ / ui/`.
- **v1.0.0** — Initial release: multi-city clocks, stopwatch, Windows startup integration.

---

## 🇮🇷 فارسی

**یک ویجت ساعت و تاریخ دسکتاپ مینیمال، شیک و کاربردی برای ویندوز**
توسعه‌یافته با Python و PyQt6 · پشتیبانی از تقویم شمسی و میلادی · مدیریت زمان روی دسکتاپ.

### ✨ ویژگی‌های کلیدی

- 🕰️ **نمایش همزمان چند ساعت** از شهرهای دلخواه با قابلیت افزودن یا حذف.
- 📅 **نمایش کامل تقویم ماهانه** — ناوبری بین ماه‌ها، بازگشت سریع به امروز، و مشخص‌کردن تعطیلات رسمی شمسی. *(جدید در نسخه ۱.۱.۰)*
- 🗓️ **پشتیبانی از تقویم شمسی و میلادی** — قابل تغییر از تنظیمات.
- 🪟 **حالت ویجت بدون حاشیه** — قابل جابه‌جایی، تغییر شفافیت و همیشه روی دسکتاپ.
- ⏱️ **زمان‌سنج داخلی** — با امکان باز و بسته کردن جداگانه از ساعت.
- 🚀 **اجرای خودکار با استارت ویندوز** — قابل تنظیم در بخش Settings.
- 💾 **ذخیره‌سازی ایمن تنظیمات** در مسیر `AppData\Roaming`، بدون از دست رفتن هنگام آپدیت.

### 📥 دانلود و نصب (نسخهٔ آمادهٔ ویندوز)

آخرین نصب‌کننده رو از بخش [**Releases**](https://github.com/mrsaeedi/Window-Screen-Date-Time-Widget/releases) دریافت کنید:

1. آخرین فایل `.exe` رو دانلود کنید.
2. اجرا کرده و مراحل نصب رو دنبال کنید.
3. برنامه از منوی Start یا با اجرای خودکار در استارتاپ در دسترس خواهد بود.

> **نکته:** برچسب شمارشگر دانلود بالای صفحه، مجموع دانلود از تمام Release هایی که روی گیت‌هاب منتشر شده رو نشون می‌ده.

### 🛠️ راهنمای توسعه (برای برنامه‌نویسان)

#### پیش‌نیازها
- Python 3.9 یا بالاتر
- Git (اختیاری)

#### ۱. کلون کردن مخزن
```bash
git clone https://github.com/mrsaeedi/Window-Screen-Date-Time-Widget.git
cd Window-Screen-Date-Time-Widget
```

#### ۲. ساخت محیط مجازی
```bash
python -m venv venv
# فعال‌سازی در CMD
venv\Scripts\activate
# یا در PowerShell
.\venv\Scripts\Activate.ps1
```

#### ۳. نصب وابستگی‌ها
```bash
pip install -r requirements.txt
```

#### ۴. اجرای برنامه در حالت توسعه
```bash
python main.pyw
```

### 📁 ساختار پروژه

```
screen_time/
├── main.pyw                    # نقطه ورود برنامه
├── config/                     # داده ثابت و تنظیمات ذخیره‌شده (بدون منطق)
│   ├── constants.py             # دیتابیس شهرها، تعطیلات، نام ماه‌ها
│   ├── translations.py          # متن‌های رابط کاربری fa/en
│   └── settings_store.py        # خواندن/نوشتن تنظیمات JSON در AppData
├── core/                       # منطق خالص کسب‌وکار (بدون وابستگی به Qt)
│   ├── calendar_engine.py       # محاسبات گرید تقویم شمسی/میلادی
│   ├── datetime_formatter.py    # فرمت‌دهی رشته زمان/تاریخ
│   ├── number_utils.py          # تبدیل اعداد انگلیسی به فارسی
│   └── startup_manager.py       # ثبت اجرای خودکار در استارتاپ ویندوز
├── ui/                          # لایه نمایش (PyQt6)
│   ├── clock_widget.py           # پنجره اصلی (orchestrator)
│   ├── settings_dialog.py        # دیالوگ تنظیمات
│   └── components/
│       ├── clock_row.py           # ردیف ساعت/تاریخ هر شهر
│       ├── timer_panel.py         # پنل زمان‌سنج
│       └── calendar_panel.py      # پنل تقویم ماهانه
├── assets/
│   └── screenshot.png            # تصویر پیش‌نمایش برای README
├── requirements.txt
├── LICENSE
└── README.md
```

### 🎨 نکات برای مشارکت‌کنندگان
- **استایل‌دهی UI**: با `setStyleSheet` و `QSS`، عمدتاً داخل `ui/clock_widget.py` و `ui/components/*`.
- **تنظیمات**: به‌صورت JSON در `AppData\Roaming\TimeWidget` ذخیره می‌شه و با آپدیت از بین نمی‌ره.
- **افزودن یک شهر جدید**: کافیه یک آیتم به `CITIES_DB` در `config/constants.py` با نام timezone استاندارد IANA اضافه کنید.

### 🗒️ تاریخچه تغییرات
- **نسخه ۱.۱.۰** — افزودن نمای کامل تقویم (شمسی و میلادی، هایلایت تعطیلات، ناوبری بین ماه‌ها)، و ماژولار شدن کامل ساختار پروژه به `config/ / core/ / ui/`.
- **نسخه ۱.۰.۰** — انتشار اولیه: ساعت چندشهری، زمان‌سنج، اجرای خودکار در استارتاپ ویندوز.

<p align="right"><a href="#-فارسی">⬆ بازگشت به بالا</a></p>