"""
ui/clock_widget.py

The main frameless, always-on-desktop widget. Responsibilities:
- own the persisted config (load/save via config.settings_store)
- lay out and show/hide its three areas: the clock list, the timer panel,
  and the calendar panel
- react to user interaction: dragging the window, the right-click menu, and
  opening the settings dialog
- tick every second to refresh the displayed time/date
- apply the active visual theme ("simple" or "glass") to its containers

All calendar-grid math and stopwatch bookkeeping live in `CalendarPanel` /
`TimerPanel` -- this class only wires them together and applies the current
config to them.
"""

from datetime import datetime

import pytz
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QMenu, QApplication
from PyQt6.QtCore import Qt, QTimer, QPoint
from PyQt6.QtGui import QFont, QAction, QIcon

from config.constants import CITIES_DB
from config.translations import TRANSLATIONS
from config.settings_store import load_config, save_config, resource_path
from core.startup_manager import set_windows_startup
from core.datetime_formatter import format_time, format_date
from ui.components.clock_row import ClockRowWidget
from ui.components.timer_panel import TimerPanel
from ui.components.calendar_panel import CalendarPanel
from ui.settings_dialog import SettingsDialog
from ui.styles import build_container_qss, apply_drop_shadow, ensure_styled_background


class ClockWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._old_pos = QPoint()
        self.config = load_config()
        self.clock_rows: dict = {}

        self._init_ui()

    # --- construction -------------------------------------------------------

    def _init_ui(self) -> None:
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setWindowIcon(QIcon(resource_path("icon.ico")))

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Clock + timer container
        self.container = QWidget(self)
        self.container.setObjectName("GlassContainer")
        ensure_styled_background(self.container)
        self.container_layout = QVBoxLayout(self.container)
        self.main_layout.addWidget(self.container)

        self.lbl_main_title = QLabel()
        self.container_layout.addWidget(self.lbl_main_title)

        self.clocks_layout = QVBoxLayout()
        self.container_layout.addLayout(self.clocks_layout)

        self.timer_panel = TimerPanel()
        self.timer_panel.closed.connect(self._on_timer_panel_closed)
        self.container_layout.addWidget(self.timer_panel)

        # Independent calendar container
        self.calendar_container = QWidget(self)
        self.calendar_container.setObjectName("GlassContainer")
        ensure_styled_background(self.calendar_container)
        calendar_layout = QVBoxLayout(self.calendar_container)
        calendar_layout.setContentsMargins(0, 0, 0, 0)
        self.calendar_panel = CalendarPanel()
        self.calendar_panel.back_clicked.connect(self.switch_to_clock_view)
        calendar_layout.addWidget(self.calendar_panel)
        self.main_layout.addWidget(self.calendar_container)

        self.apply_config()

        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_clocks_display)
        self.clock_timer.start(1000)

        self.update_clocks_display()

    # --- config application ---------------------------------------------

    def apply_config(self) -> None:
        """Re-render the entire widget from `self.config` and persist it."""
        save_config(self.config)
        is_fa = self.config['lang'] == 'fa'
        t = TRANSLATIONS[self.config['lang']]

        set_windows_startup(self.config.get('run_at_startup', True))

        flags = Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool
        if self.config['always_on_top']:
            flags |= Qt.WindowType.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.show()

        self.setWindowOpacity(self.config['opacity'])

        theme = self.config.get('theme', 'simple')
        qss_style = build_container_qss(theme)
        self.container.setStyleSheet(qss_style)
        self.calendar_container.setStyleSheet(qss_style)
        apply_drop_shadow(self.container, theme)
        apply_drop_shadow(self.calendar_container, theme)

        if self.config.get('view_mode', 'clock') == 'calendar':
            self.container.hide()
            self.calendar_container.show()
            self.calendar_panel.render(
                self.config.get('calendar_type', 'jalali'),
                self.config['lang'],
                self.config['font_size'],
            )
        else:
            self.calendar_container.hide()
            self.container.show()

        self._apply_title(is_fa, t)
        self._rebuild_clock_rows(is_fa)
        self._apply_timer_panel(is_fa)
        self._apply_margins()

        self.update_clocks_display()

        QTimer.singleShot(50, self._force_shrink)

    def _apply_title(self, is_fa: bool, t: dict) -> None:
        if self.config.get('show_title', True):
            self.lbl_main_title.setText(t['title_text'])
            self.lbl_main_title.setFont(
                QFont("Vazirmatn" if is_fa else "Segoe UI", self.config['font_size'] + 3, QFont.Weight.Bold)
            )
            self.lbl_main_title.setStyleSheet("color: #FFFFFF; padding-bottom: 4px;")
            self.lbl_main_title.setAlignment(Qt.AlignmentFlag.AlignCenter if is_fa else Qt.AlignmentFlag.AlignLeft)
            self.lbl_main_title.show()
        else:
            self.lbl_main_title.hide()

    def _rebuild_clock_rows(self, is_fa: bool) -> None:
        while self.clocks_layout.count():
            item = self.clocks_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self.clock_rows = {}

        font_name = "Vazirmatn" if is_fa else "Segoe UI"
        time_font = QFont(font_name, self.config['font_size'])
        date_font = QFont(font_name, max(6, int(self.config['font_size'] * 0.65) - 2))

        selected_cities = self.config.get('selected_cities', ['TEH'])
        only_time = len(selected_cities) == 1 and self.config.get('only_time', False)
        show_date = self.config.get('show_date', True)

        for code in selected_cities:
            if code not in CITIES_DB:
                continue
            city_name = CITIES_DB[code]['fa'] if is_fa else CITIES_DB[code]['en']
            row = ClockRowWidget(city_name, is_fa, only_time, time_font, date_font, show_date)
            self.clocks_layout.addWidget(row)
            self.clock_rows[code] = row

    def _apply_timer_panel(self, is_fa: bool) -> None:
        font_name = "Vazirmatn" if is_fa else "Segoe UI"
        title_font = QFont(font_name, max(6, int(self.config['font_size'] * 0.65) - 2))
        display_font = QFont(font_name, self.config['font_size'] + 2, QFont.Weight.Bold)

        self.timer_panel.apply_language(self.config['lang'])
        self.timer_panel.apply_fonts(title_font, display_font)
        self.timer_panel.apply_theme(self.config.get('theme', 'simple'))
        self.timer_panel.setVisible(self.config.get('show_timer_section', False))

    def _apply_margins(self) -> None:
        selected_cities = self.config.get('selected_cities', ['TEH'])
        only_time = len(selected_cities) == 1 and self.config.get('only_time', False)
        minimal = (
            only_time
            and not self.config.get('show_timer_section', False)
            and not self.config.get('show_title', True)
        )
        is_glass = self.config.get('theme', 'simple') == 'glass'
        shadow_room = 12 if is_glass else 0

        if minimal:
            m = 8 + shadow_room
            self.main_layout.setContentsMargins(m, m, m, m)
            self.container_layout.setContentsMargins(10, 10, 10, 10)
        else:
            m = 14 + shadow_room
            self.main_layout.setContentsMargins(m, m, m, m)
            self.container_layout.setContentsMargins(16, 16, 16, 16)

    def _force_shrink(self) -> None:
        self.resize(10, 10)
        self.adjustSize()

    # --- live updates -----------------------------------------------------

    def update_clocks_display(self) -> None:
        for code, row in self.clock_rows.items():
            timezone = pytz.timezone(CITIES_DB[code]['tz'])
            now_zone = datetime.now(timezone)
            time_text = format_time(now_zone, self.config['time_format'], self.config['show_seconds'], self.config['lang'])
            date_text = format_date(now_zone, self.config['lang'])
            row.update_display(time_text, date_text)

    # --- view switching -----------------------------------------------------

    def switch_to_calendar_view(self) -> None:
        self.calendar_panel.goto_today()
        self.config['view_mode'] = 'calendar'
        self.apply_config()

    def switch_to_clock_view(self) -> None:
        self.config['view_mode'] = 'clock'
        self.apply_config()

    def reset_calendar_navigation(self) -> None:
        """Called by SettingsDialog when the calendar type changes."""
        self.calendar_panel.goto_today()

    # --- timer section --------------------------------------------------

    def _on_timer_panel_closed(self) -> None:
        self.config['show_timer_section'] = False
        self.apply_config()

    def toggle_timer_section_visibility(self) -> None:
        self.config['show_timer_section'] = not self.config.get('show_timer_section', False)
        if not self.config['show_timer_section']:
            self.timer_panel.reset()
        self.apply_config()

    # --- window dragging (frameless window) --------------------------------

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self._old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event) -> None:
        if not self._old_pos.isNull():
            delta = QPoint(event.globalPosition().toPoint() - self._old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self._old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event) -> None:
        self._old_pos = QPoint()

    # --- right-click menu ----------------------------------------------

    def contextMenuEvent(self, event) -> None:
        context_menu = QMenu(self)
        t = TRANSLATIONS[self.config['lang']]
        if self.config['lang'] == 'fa':
            context_menu.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        action_timer = QAction(t['timer'], self)
        action_timer.setCheckable(True)
        action_timer.setChecked(self.config.get('show_timer_section', False))
        action_timer.triggered.connect(self.toggle_timer_section_visibility)

        is_calendar_view = self.config.get('view_mode', 'clock') == 'calendar'
        if is_calendar_view:
            action_calendar = QAction(t['back_to_clock'], self)
            action_calendar.triggered.connect(self.switch_to_clock_view)
        else:
            action_calendar = QAction(t['calendar'], self)
            action_calendar.triggered.connect(self.switch_to_calendar_view)

        action_settings = QAction(t['settings'], self)
        action_minimize = QAction(t['minimize'], self)
        action_close = QAction(t['close'], self)

        action_settings.triggered.connect(self.open_settings)
        action_minimize.triggered.connect(self.showMinimized)
        action_close.triggered.connect(QApplication.instance().quit)

        if not is_calendar_view:
            context_menu.addAction(action_timer)
        context_menu.addAction(action_calendar)
        context_menu.addSeparator()
        context_menu.addAction(action_settings)
        context_menu.addAction(action_minimize)
        context_menu.addSeparator()
        context_menu.addAction(action_close)

        context_menu.exec(event.globalPos())

    def open_settings(self) -> None:
        dialog = SettingsDialog(self)
        dialog.exec()