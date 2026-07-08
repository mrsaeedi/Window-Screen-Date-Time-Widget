"""
ui/settings_dialog.py

Modal dialog for editing all user-configurable options: title/seconds/date
visibility, always-on-top, run-at-startup, 12h/24h format, calendar type,
widget theme (simple/glass), language, font size, opacity, and the list of
visible cities.

On "Save" it writes the new values into `parent.config` and calls
`parent.apply_config()`, which re-renders the whole widget and persists the
config to disk.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QRadioButton,
    QButtonGroup, QComboBox, QSlider, QPushButton, QGroupBox, QScrollArea, QWidget,
)
from PyQt6.QtCore import Qt

from config.constants import CITIES_DB
from config.translations import TRANSLATIONS


class SettingsDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowCloseButtonHint)
        self._init_ui()

    def _init_ui(self) -> None:
        lang = self.parent.config['lang']
        t = TRANSLATIONS[lang]
        self.setWindowTitle(t['settings'])
        self.setMinimumWidth(380)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft if lang == 'fa' else Qt.LayoutDirection.LeftToRight)

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
        (self.rad_12 if self.parent.config['time_format'] == 12 else self.rad_24).setChecked(True)
        format_layout.addWidget(self.rad_12)
        format_layout.addWidget(self.rad_24)
        format_group.setLayout(format_layout)
        layout.addWidget(format_group)

        cal_group = QGroupBox(t['cal_type'])
        cal_layout = QHBoxLayout()
        self.btn_group_cal = QButtonGroup(self)
        self.rad_shamsi = QRadioButton(t['shamsi'])
        self.rad_miladi = QRadioButton(t['miladi'])
        self.btn_group_cal.addButton(self.rad_shamsi)
        self.btn_group_cal.addButton(self.rad_miladi)
        is_jalali = self.parent.config.get('calendar_type', 'jalali') == 'jalali'
        (self.rad_shamsi if is_jalali else self.rad_miladi).setChecked(True)
        cal_layout.addWidget(self.rad_shamsi)
        cal_layout.addWidget(self.rad_miladi)
        cal_group.setLayout(cal_layout)
        layout.addWidget(cal_group)

        theme_group = QGroupBox(t['theme'])
        theme_layout = QHBoxLayout()
        self.btn_group_theme = QButtonGroup(self)
        self.rad_theme_simple = QRadioButton(t['theme_simple'])
        self.rad_theme_glass = QRadioButton(t['theme_glass'])
        self.btn_group_theme.addButton(self.rad_theme_simple)
        self.btn_group_theme.addButton(self.rad_theme_glass)
        is_glass = self.parent.config.get('theme', 'simple') == 'glass'
        (self.rad_theme_glass if is_glass else self.rad_theme_simple).setChecked(True)
        theme_layout.addWidget(self.rad_theme_simple)
        theme_layout.addWidget(self.rad_theme_glass)
        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)

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
        btn_save.clicked.connect(self._save_settings)
        layout.addWidget(btn_save)

        self.setLayout(layout)

    def _save_settings(self) -> None:
        selected = [code for code, chk in self.city_checkboxes.items() if chk.isChecked()] or ['TEH']

        config = self.parent.config
        config['show_title'] = self.chk_title.isChecked()
        config['always_on_top'] = self.chk_on_top.isChecked()
        config['run_at_startup'] = self.chk_startup.isChecked()
        config['show_seconds'] = self.chk_seconds.isChecked()
        config['show_date'] = self.chk_date.isChecked()
        config['only_time'] = self.chk_only_time.isChecked()
        config['time_format'] = 12 if self.rad_12.isChecked() else 24
        config['theme'] = 'glass' if self.rad_theme_glass.isChecked() else 'simple'

        old_calendar_type = config.get('calendar_type', 'jalali')
        new_calendar_type = 'jalali' if self.rad_shamsi.isChecked() else 'gregorian'
        config['calendar_type'] = new_calendar_type
        if new_calendar_type != old_calendar_type:
            self.parent.reset_calendar_navigation()

        config['lang'] = self.cmb_lang.currentData()
        config['font_size'] = self.sld_font.value()
        config['opacity'] = self.sld_opacity.value() / 100.0
        config['selected_cities'] = selected

        self.parent.apply_config()
        self.accept()