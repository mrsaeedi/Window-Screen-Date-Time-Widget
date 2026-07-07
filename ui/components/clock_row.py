# A single clock/date row for each city
"""
ui/components/clock_row.py

A single reusable row showing one city's live time and date. `ClockWidget`
creates one `ClockRowWidget` per selected city and calls `update_display()`
on every tick. Each row is rebuilt (not mutated) whenever settings change --
this mirrors how the rest of the app already rebuilds its whole clock list
on every `apply_config()`, and keeps this widget dead simple.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class ClockRowWidget(QWidget):
    def __init__(self, city_name: str, is_fa: bool, only_time: bool,
                 time_font: QFont, date_font: QFont, show_date: bool, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: transparent; border: none;")

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 8, 0, 8)
        outer_layout.setSpacing(1)

        time_row = QWidget()
        time_row.setStyleSheet("background: transparent; border: none;")
        time_row.setLayoutDirection(Qt.LayoutDirection.RightToLeft if is_fa else Qt.LayoutDirection.LeftToRight)
        time_row_layout = QHBoxLayout(time_row)
        time_row_layout.setContentsMargins(4, 0, 4, 0)

        self.lbl_city = QLabel(city_name)
        self.lbl_city.setFont(time_font)
        self.lbl_city.setStyleSheet("color: #BBBBBB;")
        if only_time:
            self.lbl_city.hide()

        self.lbl_time = QLabel()
        self.lbl_time.setFont(time_font)
        self.lbl_time.setStyleSheet("color: #00FFCC; font-weight: bold;")
        self.lbl_time.setAlignment(
            Qt.AlignmentFlag.AlignCenter if only_time
            else (Qt.AlignmentFlag.AlignLeft if is_fa else Qt.AlignmentFlag.AlignRight)
        )

        time_row_layout.addWidget(self.lbl_city)
        if not only_time:
            time_row_layout.addStretch()
        time_row_layout.addWidget(self.lbl_time)

        self.lbl_date = QLabel()
        self.lbl_date.setFont(date_font)
        self.lbl_date.setStyleSheet("color: #888888; border: none; background: transparent; padding-top: 1px;")
        self.lbl_date.setAlignment(
            Qt.AlignmentFlag.AlignCenter if only_time
            else (Qt.AlignmentFlag.AlignLeft if is_fa else Qt.AlignmentFlag.AlignRight)
        )
        self.lbl_date.setVisible(show_date)

        outer_layout.addWidget(time_row)
        outer_layout.addWidget(self.lbl_date)

    def update_display(self, time_text: str, date_text: str) -> None:
        """Push a freshly formatted time/date string into the labels."""
        self.lbl_time.setText(time_text)
        self.lbl_date.setText(date_text)