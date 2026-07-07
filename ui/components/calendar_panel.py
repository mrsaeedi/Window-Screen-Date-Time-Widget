"""
ui/components/calendar_panel.py

Self-contained month-view calendar: top bar (back / today / prev / next /
title) plus a day grid. All date math is delegated to `core.calendar_engine`
-- this widget only turns the computed `DayCell` list into `QLabel`s and
tracks the small amount of navigation state (which year/month is on screen).
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont

from config.translations import TRANSLATIONS
from core.number_utils import en_to_fa_num
from core import calendar_engine


class CalendarPanel(QWidget):
    """Month-view calendar with prev/next navigation and a "back to today"
    shortcut.

    Signal:
        back_clicked: emitted when the user clicks the "x" to return to the
                      clock view.
    """

    back_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._year = None
        self._month = None

        # Cache of the last values passed to render(), so navigation methods
        # (prev/next/today) can re-render themselves without the parent
        # having to know about it.
        self._calendar_type = 'jalali'
        self._lang = 'en'
        self._font_size = 16

        layout = QVBoxLayout(self)

        top_bar = QHBoxLayout()

        self.btn_back = QPushButton("×")
        self.btn_back.setFixedSize(22, 22)
        self.btn_back.setStyleSheet("color: #FF5555; font-weight: bold; background: transparent; border: none; font-size: 15px;")
        self.btn_back.clicked.connect(self.back_clicked.emit)
        top_bar.addWidget(self.btn_back)

        self.btn_today = QPushButton("↺")
        self.btn_today.setFixedSize(20, 20)
        self.btn_today.setStyleSheet("color: #00FFCC; font-weight: bold; background: transparent; border: none; font-size: 13px;")
        self.btn_today.clicked.connect(self._on_today_clicked)
        self.btn_today.setVisible(False)
        top_bar.addWidget(self.btn_today)

        top_bar.addStretch()

        # NOTE: these two connections intentionally look "reversed". The
        # original single-file version wired them this way to read correctly
        # in the RTL (Persian) layout, and the behavior is preserved here.
        self.btn_prev_month = QPushButton(">")
        self.btn_prev_month.setFixedSize(22, 22)
        self.btn_prev_month.setStyleSheet("color: #00FFCC; background: rgba(255,255,255,15); border-radius: 4px; border: none; font-weight: bold;")
        self.btn_prev_month.clicked.connect(self.go_next_month)
        top_bar.addWidget(self.btn_prev_month)

        self.lbl_title = QLabel()
        self.lbl_title.setStyleSheet("color: #FFFFFF; font-weight: bold; background: transparent; border: none;")
        self.lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_bar.addWidget(self.lbl_title)

        self.btn_next_month = QPushButton("<")
        self.btn_next_month.setFixedSize(22, 22)
        self.btn_next_month.setStyleSheet("color: #00FFCC; background: rgba(255,255,255,15); border-radius: 4px; border: none; font-weight: bold;")
        self.btn_next_month.clicked.connect(self.go_prev_month)
        top_bar.addWidget(self.btn_next_month)

        top_bar.addStretch()
        layout.addLayout(top_bar)

        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(4)
        layout.addLayout(self.grid_layout)

    # --- navigation ------------------------------------------------------

    def goto_today(self) -> None:
        """Reset navigation state only. Does NOT render -- callers that
        change calendar_type/lang/font_size (e.g. SettingsDialog) call this
        first and then call render() themselves with the new values, so we
        avoid rendering once with stale settings and once with fresh ones."""
        self._year = None
        self._month = None

    def go_prev_month(self) -> None:
        if self._year is None:
            return
        self._year, self._month = calendar_engine.shift_month(self._year, self._month, -1)
        self.render(self._calendar_type, self._lang, self._font_size)

    def go_next_month(self) -> None:
        if self._year is None:
            return
        self._year, self._month = calendar_engine.shift_month(self._year, self._month, 1)
        self.render(self._calendar_type, self._lang, self._font_size)

    def _on_today_clicked(self) -> None:
        """Handle the '↺ back to today' button: reset then render immediately."""
        self.goto_today()
        self.render(self._calendar_type, self._lang, self._font_size)

    # --- rendering --------------------------------------------------------

    def render(self, calendar_type: str, lang: str, font_size: int) -> None:
        """Recompute and redraw the whole grid for the current year/month."""
        self._calendar_type = calendar_type
        self._lang = lang
        self._font_size = font_size

        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        is_fa = lang == 'fa'
        t = TRANSLATIONS[lang]

        today_g, today_j = calendar_engine.get_today_dates()
        if self._year is None or self._month is None:
            if calendar_type == 'jalali':
                self._year, self._month = today_j.year, today_j.month
            else:
                self._year, self._month = today_g.year, today_g.month

        self.btn_today.setVisible(
            not calendar_engine.is_current_month(self._year, self._month, calendar_type)
        )

        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft if is_fa else Qt.LayoutDirection.LeftToRight)

        font_name = "Vazirmatn" if is_fa else "Segoe UI"
        title_font = QFont(font_name, font_size - 3, QFont.Weight.DemiBold)
        cell_font = QFont(font_name, font_size - 2)

        title_str = calendar_engine.get_month_title(self._year, self._month, calendar_type)
        if is_fa and calendar_type == 'jalali':
            title_str = en_to_fa_num(title_str)
        self.lbl_title.setText(title_str)
        self.lbl_title.setFont(title_font)

        week_days = t['week_days_fa'] if calendar_type == 'jalali' else t['week_days_en']
        weekend_col = calendar_engine.get_weekend_column(calendar_type)
        for col, day_name in enumerate(week_days):
            lbl = QLabel(day_name)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setFont(cell_font)
            if col == weekend_col:
                lbl.setStyleSheet("color: #FF5555; font-weight: bold; padding: 1px;")
            else:
                lbl.setStyleSheet("color: #888888; padding: 1px;")
            self.grid_layout.addWidget(lbl, 0, col)

        cells = calendar_engine.build_month_grid(self._year, self._month, calendar_type)

        row, col = 1, 0
        for cell in cells:
            if cell.day is not None:
                display_num = en_to_fa_num(cell.day) if (is_fa and calendar_type == 'jalali') else str(cell.day)
                lbl_day = QLabel(display_num)
                lbl_day.setAlignment(Qt.AlignmentFlag.AlignCenter)
                lbl_day.setFont(cell_font)

                if cell.is_today:
                    lbl_day.setStyleSheet("""
                        color: #111111;
                        background-color: #00FFCC;
                        font-weight: bold;
                        border-radius: 4px;
                        padding: 1px;
                    """)
                elif cell.is_holiday:
                    lbl_day.setStyleSheet("color: #FF5555; font-weight: bold; padding: 1px;")
                    if cell.holiday_name:
                        lbl_day.setToolTip(cell.holiday_name)
                else:
                    lbl_day.setStyleSheet("color: #E0E0E0; padding: 1px;")

                self.grid_layout.addWidget(lbl_day, row, col)
            else:
                self.grid_layout.addWidget(QLabel(""), row, col)

            col += 1
            if col > 6:
                col = 0
                row += 1

        QTimer.singleShot(30, lambda: self.window().adjustSize())