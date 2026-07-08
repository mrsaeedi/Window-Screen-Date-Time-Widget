# Independent stopwatch panel
"""
ui/components/timer_panel.py

Self-contained stopwatch widget: its own QTimer, start/pause/reset logic,
and the small header/display/buttons UI. `ClockWidget` only needs to
show/hide this panel and call `apply_language()` / `apply_fonts()` when
settings change -- all stopwatch state lives here.
"""
from ui.styles import build_panel_qss, ensure_styled_background
from ui.styles import build_panel_qss
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont
from config.translations import TRANSLATIONS
from core.number_utils import en_to_fa_num


class TimerPanel(QWidget):
    """A minimal stopwatch (start/pause/reset) with a close button.

    Signal:
        closed: emitted when the user clicks the small "x" to hide the
                panel. The parent decides what to do with that (e.g.
                persist `show_timer_section = False`).
    """

    closed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._lang = 'en'
        self._tenths = 0
        self._running = False

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._on_tick)

        self.setStyleSheet("background-color: rgba(45, 45, 45, 180); border-radius: 8px; border: none;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 8)

        header_layout = QHBoxLayout()
        self.lbl_title = QLabel()
        self.lbl_title.setStyleSheet("color: #888888; border: none; background: transparent;")

        self.btn_close = QPushButton("×")
        self.btn_close.setFixedSize(18, 18)
        self.btn_close.setStyleSheet("color: #FF5555; font-weight: bold; background: transparent; border: none; font-size: 14px;")
        self.btn_close.clicked.connect(self._on_close_clicked)

        header_layout.addWidget(self.lbl_title)
        header_layout.addStretch()
        header_layout.addWidget(self.btn_close)
        layout.addLayout(header_layout)

        self.lbl_display = QLabel("00:00:00.0")
        self.lbl_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_display.setStyleSheet("color: #FFCC00; font-weight: bold; background: transparent; border: none;")
        layout.addWidget(self.lbl_display)

        buttons_layout = QHBoxLayout()
        self.btn_toggle = QPushButton("▶")
        self.btn_toggle.setFixedSize(28, 24)
        self.btn_toggle.clicked.connect(self.toggle)

        self.btn_reset = QPushButton("↻")
        self.btn_reset.setFixedSize(28, 24)
        self.btn_reset.setStyleSheet("background-color: #555555; color: white; border-radius: 4px; font-weight: bold; font-size: 14px;")
        self.btn_reset.clicked.connect(self.reset)

        buttons_layout.addStretch()
        buttons_layout.addWidget(self.btn_toggle)
        buttons_layout.addWidget(self.btn_reset)
        buttons_layout.addStretch()
        layout.addLayout(buttons_layout)

        self._refresh_toggle_button()

    # --- public API used by ClockWidget -------------------------------------

    @property
    def is_running(self) -> bool:
        return self._running

    def apply_language(self, lang: str) -> None:
        self._lang = lang
        t = TRANSLATIONS[lang]
        self.lbl_title.setText(t['timer'])
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft if lang == 'fa' else Qt.LayoutDirection.LeftToRight)
        self._refresh_display()

    def apply_fonts(self, title_font: QFont, display_font: QFont) -> None:
        self.lbl_title.setFont(title_font)
        self.lbl_display.setFont(display_font)

    def apply_theme(self, theme: str) -> None:
        ensure_styled_background(self)
        self.setStyleSheet(build_panel_qss(theme))

    def toggle(self) -> None:
        self.pause() if self._running else self.start()

    def start(self) -> None:
        self._timer.start(100)
        self._running = True
        self._refresh_toggle_button()

    def pause(self) -> None:
        self._timer.stop()
        self._running = False
        self._refresh_toggle_button()

    def reset(self) -> None:
        self._timer.stop()
        self._running = False
        self._tenths = 0
        self._refresh_toggle_button()
        self._refresh_display()

    # --- internal ------------------------------------------------------------

    def _on_tick(self) -> None:
        self._tenths += 1
        self._refresh_display()

    def _on_close_clicked(self) -> None:
        self.reset()
        self.closed.emit()

    def _refresh_display(self) -> None:
        total_tenths = self._tenths
        tenths = total_tenths % 10
        total_sec = total_tenths // 10
        seconds = total_sec % 60
        total_min = total_sec // 60
        minutes = total_min % 60
        hours = total_min // 60

        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}.{tenths}"
        if self._lang == 'fa':
            time_str = en_to_fa_num(time_str)
        self.lbl_display.setText(time_str)

    def _refresh_toggle_button(self) -> None:
        if self._running:
            self.btn_toggle.setText("⏸")
            self.btn_toggle.setStyleSheet("background-color: #ea4335; color: white; border-radius: 4px; font-weight: bold; font-size: 12px;")
        else:
            self.btn_toggle.setText("▶")
            self.btn_toggle.setStyleSheet("background-color: #33a852; color: white; border-radius: 4px; font-weight: bold; font-size: 12px;")