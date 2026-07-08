"""
ui/styles.py

Centralized QSS for the two visual themes ("simple" and "glass") the widget
supports, plus a helper to make sure QSS backgrounds actually paint (Qt does
not reliably auto-paint a plain QWidget's stylesheet background, especially
with gradients, unless WA_StyledBackground is explicitly set) and to attach
the soft drop shadow used by the glass theme.

Font size and window opacity stay completely independent of this module --
ClockWidget applies them separately, on top of whichever theme is active.
"""

from PyQt6.QtWidgets import QWidget, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor


def ensure_styled_background(widget: QWidget) -> None:
    """Force Qt to actually paint this widget's QSS background/border.
    Without this, a plain QWidget styled with a gradient `background:` rule
    can silently render as fully transparent."""
    widget.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)


def build_container_qss(theme: str) -> str:
    """QSS for the main containers (clock view / calendar view)."""
    if theme == 'glass':
        # High alpha values (220-245) on purpose: this is a *frosted*
        # glass card, meant to stay mostly opaque on its own. The user's
        # opacity slider (window-level, applied separately) is the control
        # for making the whole widget see-through if they want that -- the
        # card itself should not rely on it to look "glassy".
        return """
            QWidget#GlassContainer {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 255, 255, 40),
                    stop:0.18 rgba(68, 72, 80, 232),
                    stop:0.55 rgba(34, 36, 41, 240),
                    stop:1 rgba(16, 17, 21, 248)
                );
                border-top: 1px solid rgba(255, 255, 255, 100);
                border-left: 1px solid rgba(255, 255, 255, 65);
                border-right: 1px solid rgba(255, 255, 255, 45);
                border-bottom: 1px solid rgba(255, 255, 255, 28);
                border-radius: 18px;
            }
            QLabel { border: none; background: transparent; }
        """
    return """
        QWidget#GlassContainer {
            background-color: rgba(25, 25, 25, 225);
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 20);
        }
        QLabel { border: none; background: transparent; }
    """


def build_panel_qss(theme: str) -> str:
    """QSS for a nested sub-panel sitting inside the main container
    (currently only the timer panel)."""
    if theme == 'glass':
        return """
            QWidget {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 255, 255, 30),
                    stop:0.2 rgba(70, 74, 82, 210),
                    stop:1 rgba(30, 32, 37, 228)
                );
                border-top: 1px solid rgba(255, 255, 255, 85);
                border-left: 1px solid rgba(255, 255, 255, 50);
                border-right: 1px solid rgba(255, 255, 255, 38);
                border-bottom: 1px solid rgba(255, 255, 255, 25);
                border-radius: 10px;
            }
            QLabel { border: none; background: transparent; }
        """
    return """
        QWidget {
            background-color: rgba(45, 45, 45, 180);
            border-radius: 8px;
            border: none;
        }
        QLabel { border: none; background: transparent; }
    """


def apply_drop_shadow(widget: QWidget, theme: str) -> None:
    """Attach a soft floating-glass shadow for the glass theme; remove any
    shadow for the simple theme. Requires enough margin around `widget`
    inside its parent layout for the blur to fade out -- otherwise the
    window edge clips the shadow and it looks like a hard rectangle
    (see ClockWidget._apply_margins, which adds extra room when theme is
    'glass')."""
    if theme == 'glass':
        effect = QGraphicsDropShadowEffect(widget)
        effect.setBlurRadius(16)
        effect.setOffset(0, 4)
        effect.setColor(QColor(0, 0, 0, 110))
        widget.setGraphicsEffect(effect)
    else:
        widget.setGraphicsEffect(None)