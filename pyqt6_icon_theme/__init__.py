"""
pyqt6-icon-theme
================
Quick start::

    from pyqt6_icon_theme import IconManager, IconButton

    IconManager.set_icon_dir("icons")

    # Auto color: black on light background, white on dark background
    btn = IconButton("delete", size=24)

    # Custom color + hover
    btn = IconButton("delete", size=24,
                     normal_color="#EF4444", hover_color="#10B981")

    # After changing stylesheet, call refresh_all() to re-detect background
    app.setStyleSheet(DARK_STYLE)
    IconManager.refresh_all()
"""

from .core import IconManager, IconButton

__version__ = "0.1.0"
__all__ = ["IconManager", "IconButton"]