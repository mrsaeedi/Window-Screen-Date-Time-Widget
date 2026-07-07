# Entry point for the application
"""
main.py

Application entry point: creates the QApplication, shows the ClockWidget,
and starts the Qt event loop.
"""

import sys
from PyQt6.QtWidgets import QApplication

from ui.clock_widget import ClockWidget


def main() -> None:
    app = QApplication(sys.argv)
    widget = ClockWidget()
    widget.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()