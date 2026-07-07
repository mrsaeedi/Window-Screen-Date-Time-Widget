# 🕒 Window Screen Date Time Widget

<p align="center">
  <img src="https://img.shields.io/github/v/release/mrsaeedi/Window-Screen-Date-Time-Widget?style=flat-square&color=blue" alt="release">
  <img src="https://img.shields.io/github/downloads/mrsaeedi/Window-Screen-Date-Time-Widget/total?style=flat-square&color=green" alt="downloads">
  <img src="https://img.shields.io/github/license/mrsaeedi/Window-Screen-Date-Time-Widget?style=flat-square&color=orange" alt="license">
  <img src="https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python" alt="python">
  <img src="https://img.shields.io/badge/PyQt-6-brightgreen?style=flat-square&logo=qt" alt="PyQt6">
</p>

<p align="center">
  <b>یک ویجت ساعت و تاریخ دسکتاپ مینیمال، شیک و کاربردی برای ویندوز</b><br>
  <sub>توسعه‌یافته با Python و PyQt6 | پشتیبانی از تقویم شمسی و میلادی | مدیریت زمان روی دسکتاپ</sub>
</p>

<p align="center">
  <img src="assets/screenshot.png" alt="Window Screen Date Time Widget Preview" width="600">
</p>

---

## ✨ ویژگی‌های کلیدی

- 🕰️ **نمایش همزمان چند ساعت** از شهرهای دلخواه با قابلیت افزودن یا حذف.
- 📅 **پشتیبانی از تقویم شمسی و میلادی** – تاریخ هجری شمسی با کتابخانه‌های استاندارد.
- 🪟 **حالت ویجت بدون حاشیه** – قابل جابه‌جایی، تغییر شفافیت و همیشه روی دسکتاپ.
- ⏱️ **زمان‌سنج و کرونومتر داخلی** – با امکان باز و بسته کردن جداگانه.
- 🚀 **اجرای خودکار با استارت ویندوز** – قابل تنظیم در بخش Settings.
- 💾 **ذخیره‌سازی ایمن تنظیمات** در مسیر استاندارد `AppData\Roaming` بدون تداخل با فایل‌های برنامه.

---

## 📥 دانلود و نصب (نسخهٔ آمادهٔ ویندوز)

برای کاربران عادی که نیاز به پایتون ندارند، فایل نصبی آماده را از بخش [**Releases**](https://github.com/mrsaeedi/Window-Screen-Date-Time-Widget/releases) دریافت کنید.

1. آخرین نسخه با پسوند `.exe` یا نصب‌کننده را دانلود کنید.
2. فایل را اجرا کرده و مراحل نصب را دنبال کنید.
3. برنامه از منوی Start یا با اجرای خودکار در استارتاپ در دسترس خواهد بود.

---

## 🛠️ راهنمای توسعه (برای برنامه‌نویسان)

اگر تمایل دارید ویژگی جدید اضافه کنید یا باگ‌ها را برطرف نمایید، مراحل زیر را دنبال کنید.

### ✅ پیش‌نیازها
- Python 3.9 یا بالاتر
- Git (اختیاری)

### 📥 ۱. کلون کردن مخزن

```bash
git clone [https://github.com/mrsaeedi/Window-Screen-Date-Time-Widget.git](https://github.com/mrsaeedi/Window-Screen-Date-Time-Widget.git)
cd Window-Screen-Date-Time-Widget
```
### 🐍 ۲. ساخت محیط مجازی (venv)

# ساخت محیط مجازی
```Bash
python -m venv venv
```
# فعال‌سازی (CMD)
```
venv\Scripts\activate
```
# یا فعال‌سازی (PowerShell)
```
.\venv\Scripts\Activate.ps1
```
### 📦 ۳. نصب وابستگی‌ها
```Bash
pip install -r requirements.txt
```
### 🚀 ۴. اجرای برنامه در حالت توسعه
```Bash
python time_screen_widget.pyw
```
تمامی تغییرات به صورت زنده در پنجره قابل مشاهده خواهند بود.

## 📁 ساختار پروژه
```Plaintext
SCREEN_TIME
├── main.py                        # نقطه ورود برنامه
├── config/
│   ├── constants.py                # CITIES_DB, HOLIDAYS_JALALI, MONTHS_EN_ABBR
│   ├── translations.py             # دیکشنری TRANSLATIONS (fa/en)
│   └── settings_store.py           # مسیر فایل کانفیگ + load/save
├── core/
│   ├── number_utils.py             # تبدیل اعداد انگلیسی به فارسی
│   ├── startup_manager.py          # ثبت در Startup ویندوز
│   ├── calendar_engine.py          # محاسبات خالص گرید تقویم شمسی/میلادی
│   └── datetime_formatter.py       # فرمت‌دهی متن ساعت و تاریخ هر شهر
└── ui/
    ├── settings_dialog.py          # دیالوگ تنظیمات
    ├── clock_widget.py             # پنجره اصلی (orchestrator)
    └── components/
        ├── clock_row.py            # یک ردیف ساعت/تاریخ برای هر شهر
        ├── timer_panel.py          # پنل کرونومتر مستقل
        └── calendar_panel.py       # پنل تقویم مستقل
```
## 🎨 نکات توسعه
 استایل‌دهی (UI): ظاهر برنامه با `setStyleSheet` و فناوری `QSS` طراحی شده. برای تغییر رنگ یا پدینگ، بخش‌های مربوطه را در `time_screen_widget.pyw` ویرایش کنید.

تنظیمات برنامه: تنظیمات در فایل `JSON` درون مسیر `AppData\Roaming\WindowScreenWidget` ذخیره می‌شود و با به‌روزرسانی برنامه از دست نمی‌رود.