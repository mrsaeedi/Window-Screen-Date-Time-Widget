import sys
import os
import json
from datetime import datetime
import pytz
import jdatetime

from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QMenu, QDialog, QCheckBox, QRadioButton, 
                             QButtonGroup, QComboBox, QSlider, QPushButton, QGroupBox,
                             QScrollArea)
from PyQt6.QtCore import Qt, QTimer, QPoint
from PyQt6.QtGui import QFont, QAction, QIcon

# دیتابیس شهرها
CITIES_DB = {
    'TEH': {'fa': 'تهران', 'en': 'Tehran', 'tz': 'Asia/Tehran'},
    'NYC': {'fa': 'نیویورک', 'en': 'New York', 'tz': 'America/New_York'},
    'TOR': {'fa': 'تورنتو', 'en': 'Toronto', 'tz': 'America/Toronto'},
    'BER': {'fa': 'برلین', 'en': 'Berlin', 'tz': 'Europe/Berlin'},
    'PAR': {'fa': 'پاریس', 'en': 'Paris', 'tz': 'Europe/Paris'},
    'SYD': {'fa': 'سیدنی', 'en': 'Sydney', 'tz': 'Australia/Sydney'},
    'IST': {'fa': 'استانبول', 'en': 'Istanbul', 'tz': 'Europe/Istanbul'},
    'BAG': {'fa': 'بغداد', 'en': 'Baghdad', 'tz': 'Asia/Baghdad'},
    'BAK': {'fa': 'باکو', 'en': 'Baku', 'tz': 'Asia/Baku'},
    'ERE': {'fa': 'ایروان', 'en': 'Yerevan', 'tz': 'Asia/Yerevan'},
    'DXB': {'fa': 'دبی', 'en': 'Dubai', 'tz': 'Asia/Dubai'},
    'MSC': {'fa': 'مسکو', 'en': 'Moscow', 'tz': 'Europe/Moscow'},
    'DOH': {'fa': 'دوحه', 'en': 'Doha', 'tz': 'Asia/Qatar'},
    'MCT': {'fa': 'مسقط', 'en': 'Muscat', 'tz': 'Asia/Muscat'},
    'KWI': {'fa': 'کویت', 'en': 'Kuwait', 'tz': 'Asia/Kuwait'}
}

TRANSLATIONS = {
    'fa': {
        'title_text': 'زمان',
        'settings': 'تنظیمات ویجت ساعت', 'close': 'خروج', 'minimize': 'کوچک کردن',
        'always_on_top': 'همیشه رو باشد (Always on Top)', 'show_seconds': 'نمایش ثانیه',
        'time_format': 'فرمت زمان', 'lang': 'زبان (Language)', 'font_size': 'اندازه فونت',
        'opacity': 'میزان شفافیت', 'cities': 'انتخاب شهرها (لیست اسکرول)', 'save': 'ذخیره تنظیمات',
        'show_title': 'نمایش عنوان ویجت («زمان»)', 'show_date': 'نمایش تاریخ زیر ساعت',
        'only_time': 'فقط زمان (پنهان کردن نام شهر در حالت تک‌شهری)',
        'run_at_startup': 'اجرا همزمان با روشن شدن سیستم (Startup)',
        'timer': 'زمان‌سنج',
        'months_fa': ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']
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
        'timer': 'Timer'
    }
}

# دسترسی به مسیر فایل‌ها در حالت کامپایل شده PyInstaller
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# تنظیم مسیر ذخیره‌سازی استاندارد در AppData ویندوز برای جلوگیری از آلودگی محیط دسکتاپ
app_data_dir = os.path.join(os.getenv('APPDATA', os.path.expanduser('~')), 'TimeWidget')
os.makedirs(app_data_dir, exist_ok=True)
CONFIG_FILE = os.path.join(app_data_dir, 'widget_config.json')


def en_to_fa_num(number_str):
    translation_table = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
    return str(number_str).translate(translation_table)

def set_windows_startup(enabled):
    if sys.platform != 'win32':
        return
    import winreg
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    app_name = "TimeWidget"
    
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
        if enabled:
            if getattr(sys, 'frozen', False):
                cmd = f'"{sys.executable}"'
            else:
                cmd = f'"{sys.executable}" "{os.path.abspath(sys.argv[0])}"'
            winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, cmd)
        else:
            try:
                winreg.DeleteValue(key, app_name)
            except FileNotFoundError:
                pass
        winreg.CloseKey(key)
    except Exception as e:
        print(f"Error modifying Startup Registry: {e}")


class SettingsDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowCloseButtonHint)
        self.init_ui()
        
    def init_ui(self):
        lang = self.parent.config['lang']
        t = TRANSLATIONS[lang]
        self.setWindowTitle(t['settings'])
        self.setMinimumWidth(380)
        
        if lang == 'fa':
            self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        else:
            self.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
            
        layout = QVBoxLayout()
        
        self.chk_title = QCheckBox(t['show_title'])
        self.chk_title.setChecked(self.parent.config.get('show_title', True))
        layout.addWidget(self.chk_title)
        
        self.chk_on_top = QCheckBox(t['always_on_top'])
        self.chk_on_top.setChecked(self.parent.config['always_on_top'])
        layout.addWidget(self.chk_on_top)
        
        self.chk_startup = QCheckBox(t['run_at_startup'])
        self.chk_startup.setChecked(self.parent.config.get('run_at_startup', True))
        layout.addWidget(self.chk_startup)
        
        self.chk_seconds = QCheckBox(t['show_seconds'])
        self.chk_seconds.setChecked(self.parent.config['show_seconds'])
        layout.addWidget(self.chk_seconds)
        
        self.chk_date = QCheckBox(t['show_date'])
        self.chk_date.setChecked(self.parent.config.get('show_date', True))
        layout.addWidget(self.chk_date)
        
        self.chk_only_time = QCheckBox(t['only_time'])
        self.chk_only_time.setChecked(self.parent.config.get('only_time', False))
        layout.addWidget(self.chk_only_time)
        
        format_group = QGroupBox(t['time_format'])
        format_layout = QHBoxLayout()
        self.btn_group_format = QButtonGroup(self)
        self.rad_12 = QRadioButton("12H")
        self.rad_24 = QRadioButton("24H")
        self.btn_group_format.addButton(self.rad_12)
        self.btn_group_format.addButton(self.rad_24)
        if self.parent.config['time_format'] == 12:
            self.rad_12.setChecked(True)
        else:
            self.rad_24.setChecked(True)
        format_layout.addWidget(self.rad_12)
        format_layout.addWidget(self.rad_24)
        format_group.setLayout(format_layout)
        layout.addWidget(format_group)
        
        lang_layout = QHBoxLayout()
        lang_layout.addWidget(QLabel(t['lang']))
        self.cmb_lang = QComboBox()
        self.cmb_lang.addItem("فارسی", "fa")
        self.cmb_lang.addItem("English", "en")
        self.cmb_lang.setCurrentIndex(self.cmb_lang.findData(lang))
        lang_layout.addWidget(self.cmb_lang)
        layout.addLayout(lang_layout)
        
        font_layout = QHBoxLayout()
        font_layout.addWidget(QLabel(t['font_size']))
        self.sld_font = QSlider(Qt.Orientation.Horizontal)
        self.sld_font.setRange(10, 32)
        self.sld_font.setValue(self.parent.config['font_size'])
        font_layout.addWidget(self.sld_font)
        layout.addLayout(font_layout)
        
        opacity_layout = QHBoxLayout()
        opacity_layout.addWidget(QLabel(t['opacity']))
        self.sld_opacity = QSlider(Qt.Orientation.Horizontal)
        self.sld_opacity.setRange(20, 100)
        self.sld_opacity.setValue(int(self.parent.config['opacity'] * 100))
        opacity_layout.addWidget(self.sld_opacity)
        layout.addLayout(opacity_layout)
        
        cities_group = QGroupBox(t['cities'])
        cities_group_layout = QVBoxLayout(cities_group)
        cities_group_layout.setContentsMargins(5, 10, 5, 5)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: 1px solid #555555; background-color: transparent; }")
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(5, 5, 5, 5)
        scroll_layout.setSpacing(6)
        
        self.city_checkboxes = {}
        for code, info in CITIES_DB.items():
            name = info['fa'] if lang == 'fa' else info['en']
            chk = QCheckBox(name)
            chk.setChecked(code in self.parent.config.get('selected_cities', ['TEH']))
            scroll_layout.addWidget(chk)
            self.city_checkboxes[code] = chk
            
        scroll.setWidget(scroll_content)
        scroll.setFixedHeight(150)
        
        cities_group_layout.addWidget(scroll)
        layout.addWidget(cities_group)
        
        btn_save = QPushButton(t['save'])
        btn_save.setStyleSheet("padding: 6px; font-weight: bold; background-color: #00FFCC; color: #111111; border-radius: 4px;")
        btn_save.clicked.connect(self.save_settings)
        layout.addWidget(btn_save)
        
        self.setLayout(layout)
        
    def save_settings(self):
        selected = [code for code, chk in self.city_checkboxes.items() if chk.isChecked()]
        if not selected:
            selected = ['TEH']
            
        self.parent.config['show_title'] = self.chk_title.isChecked()
        self.parent.config['always_on_top'] = self.chk_on_top.isChecked()
        self.parent.config['run_at_startup'] = self.chk_startup.isChecked()
        self.parent.config['show_seconds'] = self.chk_seconds.isChecked()
        self.parent.config['show_date'] = self.chk_date.isChecked()
        self.parent.config['only_time'] = self.chk_only_time.isChecked()
        self.parent.config['time_format'] = 12 if self.rad_12.isChecked() else 24
        self.parent.config['lang'] = self.cmb_lang.currentData()
        self.parent.config['font_size'] = self.sld_font.value()
        self.parent.config['opacity'] = self.sld_opacity.value() / 100.0
        self.parent.config['selected_cities'] = selected
        
        self.parent.apply_config()
        self.accept()


class ClockWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.old_pos = QPoint()
        self.stopwatch_time = 0
        self.stopwatch_running = False
        
        self.load_default_config()
        self.init_ui()
        
    def load_default_config(self):
        default_config = {
            'always_on_top': True,
            'run_at_startup': True,
            'show_seconds': True,
            'time_format': 24,
            'lang': 'fa',
            'font_size': 16,
            'opacity': 0.85,
            'selected_cities': ['TEH'],
            'show_title': False,
            'show_date': True,
            'only_time': True,
            'show_timer_section': False
        }
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    self.config = {**default_config, **json.load(f)}
                    return
            except:
                pass
        self.config = default_config

    def save_config_to_file(self):
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=4)

    def init_ui(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        
        # بارگذاری آیکون از منابع داخلی
        self.setWindowIcon(QIcon(resource_path("icon.ico")))
        
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        
        self.container = QWidget(self)
        self.container_layout = QVBoxLayout(self.container)
        self.main_layout.addWidget(self.container)
        
        self.lbl_main_title = QLabel()
        self.container_layout.addWidget(self.lbl_main_title)
        
        self.clocks_layout = QVBoxLayout()
        self.container_layout.addLayout(self.clocks_layout)
        
        self.init_timer_ui()
        self.apply_config()
        
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_clocks_display)
        self.clock_timer.start(1000)
        
        self.stopwatch_timer = QTimer(self)
        self.stopwatch_timer.timeout.connect(self.update_stopwatch_logic)
        
        self.update_clocks_display()

    def init_timer_ui(self):
        self.timer_widget = QWidget()
        self.timer_widget.setStyleSheet("background-color: rgba(45, 45, 45, 180); border-radius: 8px; border: none;")
        t_layout = QVBoxLayout(self.timer_widget)
        t_layout.setContentsMargins(8, 6, 8, 8)
        
        header_layout = QHBoxLayout()
        self.lbl_timer_title = QLabel()
        self.lbl_timer_title.setStyleSheet("color: #888888; border: none; background: transparent;")
        
        self.btn_close_timer = QPushButton("×")
        self.btn_close_timer.setFixedSize(18, 18)
        self.btn_close_timer.setStyleSheet("color: #FF5555; font-weight: bold; background: transparent; border: none; font-size: 14px;")
        self.btn_close_timer.clicked.connect(self.hide_timer_section)
        
        header_layout.addWidget(self.lbl_timer_title)
        header_layout.addStretch()
        header_layout.addWidget(self.btn_close_timer)
        t_layout.addLayout(header_layout)
        
        self.lbl_timer_display = QLabel("00:00:00.0")
        self.lbl_timer_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_timer_display.setStyleSheet("color: #FFCC00; font-weight: bold; background: transparent; border: none;")
        t_layout.addWidget(self.lbl_timer_display)
        
        btn_layout = QHBoxLayout()
        
        self.btn_timer_toggle = QPushButton("▶")
        self.btn_timer_toggle.setFixedSize(28, 24)
        
        self.btn_timer_reset = QPushButton("↻")
        self.btn_timer_reset.setFixedSize(28, 24)
        self.btn_timer_reset.setStyleSheet("background-color: #555555; color: white; border-radius: 4px; font-weight: bold; font-size: 14px;")
        self.btn_timer_reset.clicked.connect(self.reset_stopwatch)
        
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_timer_toggle)
        btn_layout.addWidget(self.btn_timer_reset)
        btn_layout.addStretch()
        t_layout.addLayout(btn_layout)
        
        self.container_layout.addWidget(self.timer_widget)

    def apply_config(self):
        self.save_config_to_file()
        is_fa = self.config['lang'] == 'fa'
        t = TRANSLATIONS[self.config['lang']]
        
        set_windows_startup(self.config.get('run_at_startup', True))
        
        if self.config['always_on_top']:
            self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool | Qt.WindowType.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
        self.show()
        
        self.setWindowOpacity(self.config['opacity'])
        
        self.container.setStyleSheet("""
            QWidget {
                background-color: rgba(25, 25, 25, 225);
                border-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 20);
            }
            QLabel { border: none; background: transparent; }
        """)
        
        if self.config.get('show_title', True):
            self.lbl_main_title.setText(t['title_text'])
            self.lbl_main_title.setFont(QFont("Vazirmatn" if is_fa else "Segoe UI", self.config['font_size'] + 3, QFont.Weight.Bold))
            self.lbl_main_title.setStyleSheet("color: #FFFFFF; padding-bottom: 4px;")
            self.lbl_main_title.setAlignment(Qt.AlignmentFlag.AlignCenter if is_fa else Qt.AlignmentFlag.AlignLeft)
            self.lbl_main_title.show()
        else:
            self.lbl_main_title.hide()
            
        while self.clocks_layout.count():
            item = self.clocks_layout.takeAt(0)
            w = item.widget()
            if w: w.deleteLater()
            
        font_name = "Vazirmatn" if is_fa else "Segoe UI"
        self.ui_font = QFont(font_name, self.config['font_size'])
        self.date_font = QFont(font_name, max(6, int(self.config['font_size'] * 0.65) - 2))
        
        self.clock_rows = {}
        alignment_dir = Qt.LayoutDirection.RightToLeft if is_fa else Qt.LayoutDirection.LeftToRight
        
        selected_cities = self.config.get('selected_cities', ['TEH'])
        is_single = len(selected_cities) == 1
        is_only_time = is_single and self.config.get('only_time', False)
        is_timer_visible = self.config.get('show_timer_section', False)
        is_title_visible = self.config.get('show_title', True)
        
        if is_only_time and not is_timer_visible and not is_title_visible:
            self.main_layout.setContentsMargins(8, 8, 8, 8)
            self.container_layout.setContentsMargins(10, 10, 10, 10)
        else:
            self.main_layout.setContentsMargins(14, 14, 14, 14)
            self.container_layout.setContentsMargins(16, 16, 16, 16)
            
        for code in selected_cities:
            if code not in CITIES_DB: continue
            
            row_block = QWidget()
            row_block.setStyleSheet("background: transparent; border: none;")
            row_block_layout = QVBoxLayout(row_block)
            row_block_layout.setContentsMargins(0, 8, 0, 8)
            row_block_layout.setSpacing(1)
            
            time_row = QWidget()
            time_row.setStyleSheet("background: transparent; border: none;")
            time_row.setLayoutDirection(alignment_dir)
            time_row_layout = QHBoxLayout(time_row)
            time_row_layout.setContentsMargins(4, 0, 4, 0)
            
            lbl_city = QLabel(CITIES_DB[code]['fa'] if is_fa else CITIES_DB[code]['en'])
            lbl_city.setFont(self.ui_font)
            lbl_city.setStyleSheet("color: #BBBBBB;")
            
            if is_only_time:
                lbl_city.hide()
                
            lbl_time = QLabel()
            lbl_time.setFont(self.ui_font)
            lbl_time.setStyleSheet("color: #00FFCC; font-weight: bold;")
            lbl_time.setAlignment(Qt.AlignmentFlag.AlignCenter if is_only_time else (Qt.AlignmentFlag.AlignLeft if is_fa else Qt.AlignmentFlag.AlignRight))
            
            time_row_layout.addWidget(lbl_city)
            if not is_only_time:
                time_row_layout.addStretch()
            time_row_layout.addWidget(lbl_time)
            
            row_block_layout.addWidget(time_row)
            
            lbl_date = QLabel()
            lbl_date.setFont(self.date_font)
            lbl_date.setStyleSheet("color: #888888; border: none; background: transparent; padding-top: 1px;")
            lbl_date.setAlignment(Qt.AlignmentFlag.AlignCenter if is_only_time else (Qt.AlignmentFlag.AlignLeft if is_fa else Qt.AlignmentFlag.AlignRight))
            
            if self.config.get('show_date', True):
                lbl_date.show()
            else:
                lbl_date.hide()
                
            row_block_layout.addWidget(lbl_date)
            
            self.clocks_layout.addWidget(row_block)
            self.clock_rows[code] = {'time_lbl': lbl_time, 'date_lbl': lbl_date}
            
        if is_timer_visible:
            self.lbl_timer_title.setText(t['timer'])
            self.lbl_timer_title.setFont(self.date_font)
            self.lbl_timer_display.setFont(QFont(font_name, self.config['font_size'] + 2, QFont.Weight.Bold))
            
            if self.stopwatch_running:
                self.btn_timer_toggle.setText("⏸")
                self.btn_timer_toggle.setStyleSheet("background-color: #ea4335; color: white; border-radius: 4px; font-weight: bold; font-size: 12px;")
            else:
                self.btn_timer_toggle.setText("▶")
                self.btn_timer_toggle.setStyleSheet("background-color: #33a852; color: white; border-radius: 4px; font-weight: bold; font-size: 12px;")
                
            try:
                self.btn_timer_toggle.clicked.disconnect()
            except:
                pass
            self.btn_timer_toggle.clicked.connect(self.toggle_stopwatch)
            
            if is_fa:
                self.timer_widget.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
            else:
                self.timer_widget.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
                
            self.timer_widget.show()
        else:
            self.timer_widget.hide()
            
        self.update_clocks_display()
        self.update_stopwatch_ui_text()
        
        def force_shrink():
            self.resize(10, 10)
            self.adjustSize()
        QTimer.singleShot(50, force_shrink)

    def update_clocks_display(self):
        is_fa = self.config['lang'] == 'fa'
        
        fmt = "%H:%M"
        if self.config['show_seconds']: fmt += ":%S"
        if self.config['time_format'] == 12:
            fmt = "%I:%M"
            if self.config['show_seconds']: fmt += ":%S"
            fmt += " %p"
            
        for code, labels in self.clock_rows.items():
            timezone = pytz.timezone(CITIES_DB[code]['tz'])
            now_zone = datetime.now(timezone)
            
            time_str = now_zone.strftime(fmt)
            if is_fa:
                if self.config['time_format'] == 12:
                    time_str = time_str.replace("AM", "ق.ظ").replace("PM", "ب.ظ")
                time_str = en_to_fa_num(time_str)
            labels['time_lbl'].setText(time_str)
            
            gregorian_str = now_zone.strftime("%B %d")
            jalali_date = jdatetime.date.fromgregorian(date=now_zone.date())
            month_name_fa = TRANSLATIONS['fa']['months_fa'][jalali_date.month - 1]
            jalali_str = f"{jalali_date.day} {month_name_fa}"
            
            if is_fa:
                date_text = f"{en_to_fa_num(jalali_str)} | {gregorian_str}"
            else:
                date_text = f"{gregorian_str} | {jalali_date.day} {month_name_fa}"
                
            labels['date_lbl'].setText(date_text)

    def toggle_stopwatch(self):
        if self.stopwatch_running:
            self.stopwatch_timer.stop()
            self.stopwatch_running = False
        else:
            self.stopwatch_timer.start(100)
            self.stopwatch_running = True
        self.apply_config()

    def reset_stopwatch(self):
        self.stopwatch_timer.stop()
        self.stopwatch_running = False
        self.stopwatch_time = 0
        self.apply_config()
        self.update_stopwatch_ui_text()

    def update_stopwatch_logic(self):
        self.stopwatch_time += 1
        self.update_stopwatch_ui_text()

    def update_stopwatch_ui_text(self):
        total_tenths = self.stopwatch_time
        tenths = total_tenths % 10
        total_sec = total_tenths // 10
        seconds = total_sec % 60
        total_min = total_sec // 60
        minutes = total_min % 60
        hours = total_min // 60
        
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}.{tenths}"
        if self.config['lang'] == 'fa':
            time_str = en_to_fa_num(time_str)
        self.lbl_timer_display.setText(time_str)

    def hide_timer_section(self):
        self.stopwatch_timer.stop()
        self.stopwatch_running = False
        self.stopwatch_time = 0
        self.config['show_timer_section'] = False
        self.apply_config()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if not self.old_pos.isNull():
            delta = QPoint(event.globalPosition().toPoint() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.old_pos = QPoint()

    def contextMenuEvent(self, event):
        context_menu = QMenu(self)
        t = TRANSLATIONS[self.config['lang']]
        if self.config['lang'] == 'fa':
            context_menu.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
            
        action_timer = QAction(t['timer'], self)
        action_timer.setCheckable(True)
        action_timer.setChecked(self.config.get('show_timer_section', False))
        action_timer.triggered.connect(self.toggle_timer_section_visibility)
        
        action_settings = QAction(t['settings'], self)
        action_minimize = QAction(t['minimize'], self)
        action_close = QAction(t['close'], self)
        
        action_settings.triggered.connect(self.open_settings)
        action_minimize.triggered.connect(self.showMinimized)
        action_close.triggered.connect(QApplication.instance().quit)
        
        context_menu.addAction(action_timer)
        context_menu.addSeparator()
        context_menu.addAction(action_settings)
        context_menu.addAction(action_minimize)
        context_menu.addSeparator()
        context_menu.addAction(action_close)
        
        context_menu.exec(event.globalPos())

    def toggle_timer_section_visibility(self):
        self.config['show_timer_section'] = not self.config.get('show_timer_section', False)
        if not self.config['show_timer_section']:
            self.stopwatch_timer.stop()
            self.stopwatch_running = False
            self.stopwatch_time = 0
        self.apply_config()

    def open_settings(self):
        dialog = SettingsDialog(self)
        dialog.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = ClockWidget()
    widget.show()
    sys.exit(app.exec())