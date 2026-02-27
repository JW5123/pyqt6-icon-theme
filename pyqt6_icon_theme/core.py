"""
pyqt_icon_theme/core.py

Monochrome Icon Manager

- SVG: Automatically strips original colors and supports dynamic recoloring,
       theme-aware color updates, and hover state styling.
       If keep_original=True, the SVG is rendered as-is without any recoloring.
- PNG / JPG: Always preserves original colors (no recoloring support).
- Supports automatic icon refresh on theme changes (SVG only, keep_original=False).

Auto-color detection (normal_color=None):
IconButton reads the widget's QPalette.Window background color at runtime and
computes its relative luminance (sRGB standard).  Icons on light backgrounds
become black (#000000); icons on dark backgrounds become white (#FFFFFF).
This works with both system themes and user-applied stylesheets — any time the
palette changes a PaletteChange event is fired and the icon refreshes automatically.
"""

import re
from pathlib import Path
from PyQt6.QtCore import Qt, QSize, QByteArray, QEvent
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor, QPalette
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QPushButton

_SVG_EXT = {".svg"}
_RASTER_EXT = {".png", ".jpg", ".jpeg"}
_SUPPORTED_EXT = _SVG_EXT | _RASTER_EXT

def _relative_luminance(color: QColor) -> float:
    """Return the relative luminance of color per WCAG 2.x / sRGB spec (0-1)."""
    def _linearize(c: int) -> float:
        v = c / 255.0
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4

    return (0.2126 * _linearize(color.red())
            + 0.7152 * _linearize(color.green())
            + 0.0722 * _linearize(color.blue()))


def _icon_color_for_bg(bg: QColor) -> str:
    return "#000000" if _relative_luminance(bg) > 0.179 else "#FFFFFF"

class IconManager:
    _icon_cache: dict[tuple, QIcon] = {}
    _svg_cache: dict[str, str] = {}
    _raster_cache: dict[str, Path] = {}
    _icon_dir: Path | None = None

    @classmethod
    def set_icon_dir(cls, path: str | Path):
        p = Path(path).expanduser().resolve()
        if not p.exists():
            raise FileNotFoundError(f"Icon directory not found: {p}")
        if not p.is_dir():
            raise NotADirectoryError(f"Not a directory: {p}")
        cls._icon_dir = p
        cls.load_icons()

    @classmethod
    def load_icons(cls):
        cls._svg_cache.clear()
        cls._raster_cache.clear()
        if cls._icon_dir is None:
            raise RuntimeError("Icon directory not set. Call set_icon_dir() first.")
        for file in cls._icon_dir.iterdir():
            if file.suffix.lower() in _SVG_EXT:
                cls._svg_cache[file.stem] = file.read_text(encoding="utf-8")
            elif file.suffix.lower() in _RASTER_EXT:
                cls._raster_cache[file.stem] = file

    @classmethod
    def _strip_svg_colors(cls, svg_str: str) -> str:
        svg_str = re.sub(r'\bfill="(?!none")[^"]*"', 'fill="currentColor"', svg_str)
        svg_str = re.sub(r'\bstroke="(?!none")[^"]*"', 'stroke="currentColor"', svg_str)
        svg_str = re.sub(r'fill\s*:\s*[^;}"]+', 'fill:currentColor', svg_str)
        svg_str = re.sub(r'stroke\s*:\s*[^;}"]+', 'stroke:currentColor', svg_str)
        return svg_str

    @classmethod
    def _render_svg(cls, name: str, size: int,
                    color: str | None = None,
                    keep_original: bool = False) -> QIcon:
        """
        keep_original=False : strip colors then recolor with `color`
        keep_original=True  : render the SVG as-is, ignoring `color`
        """
        svg_str = cls._svg_cache[name]

        if not keep_original:
            svg_str = cls._strip_svg_colors(svg_str)

        renderer = QSvgRenderer(QByteArray(svg_str.encode()))
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)

        if not keep_original and color is not None:
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
            painter.fillRect(pixmap.rect(), QColor(color))

        painter.end()
        return QIcon(pixmap)

    @classmethod
    def _render_raster(cls, name: str, size: int) -> QIcon:
        path = cls._raster_cache[name]
        source = QPixmap(str(path)).scaled(
            size, size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        canvas = QPixmap(size, size)
        canvas.fill(Qt.GlobalColor.transparent)
        painter = QPainter(canvas)
        ox = (size - source.width()) // 2
        oy = (size - source.height()) // 2
        painter.drawPixmap(ox, oy, source)
        painter.end()
        return QIcon(canvas)

    @classmethod
    def get_icon(cls, name: str, color: str | None, size: int,
                 keep_original: bool = False) -> QIcon:
        """
        Return a QIcon instance.

        SVG:
            keep_original=False (default)
                color=None    → the SVG is rendered without recoloring.
                                (When used via IconButton, the color is typically
                                resolved from the widget palette before calling.)
                color="#hex"  → rendered with the specified color.

            keep_original=True
                Renders the SVG with its original colors, ignoring `color`.

        PNG/JPG:
            Always rendered with original colors. `color` and `keep_original` are ignored.
        """
        cache_key = (name, color, size, keep_original)
        if cache_key in cls._icon_cache:
            return cls._icon_cache[cache_key]

        if name in cls._svg_cache:
            icon = cls._render_svg(name, size, color, keep_original)
        elif name in cls._raster_cache:
            icon = cls._render_raster(name, size)
        else:
            raise KeyError(
                f"Icon '{name}' not found. "
                f"Supported formats: {', '.join(sorted(_SUPPORTED_EXT))}"
            )

        cls._icon_cache[cache_key] = icon
        return icon


class IconButton(QPushButton):
    def __init__(self, name: str,
                 size: int = 16,
                 normal_color: str | None = None,
                 hover_color: str | None = None,
                 keep_original: bool = False,
                 parent=None):
        """
        Parameters
        ----------
        name : str
            Icon file name (without extension).

        size : int
            Icon size in pixels.

        normal_color : str | None
            SVG only, keep_original=False.
            The icon color in the normal state.
            If None, the color is derived automatically from the widget's
            background (QPalette.Window): black on light backgrounds,
            white on dark ones.  The icon updates whenever the palette
            changes (e.g. stylesheet swap, system theme change).

        hover_color : str | None
            SVG only, keep_original=False.
            The icon color in the hover state.
            If None, no hover recoloring is applied.

        keep_original : bool
            SVG only.
            False (default) - strip original colors and apply normal_color /
                              auto-detected color. hover_color is also supported.
            True            - render the SVG with its original colors.
                              normal_color and hover_color are both ignored.

        Note: PNG/JPG icons always display their original colors regardless
              of any parameters.
        """
        super().__init__(parent)

        self._name = Path(name).stem
        self._size = size
        self._normal_color = normal_color
        self._hover_color = hover_color
        self._keep_original = keep_original

        self.setText("")
        self.setIconSize(QSize(size, size))

        self.refresh_icon()

    def _is_svg(self) -> bool:
        return self._name in IconManager._svg_cache

    def _resolve_normal_color(self) -> str | None:
        """
        Return the color to use for the normal (non-hover) state.

        If the user pinned a specific color, return that.
        For SVG icons with auto-color (normal_color=None, keep_original=False),
        read the widget's background from the palette and compute black/white.
        """
        if self._normal_color is not None:
            return self._normal_color
        if self._is_svg() and not self._keep_original:
            bg = self.palette().color(QPalette.ColorRole.Window)
            # palette may return an invalid / fully-transparent color before
            # the widget is fully styled; fall back to global default then.
            if bg.isValid() and bg.alpha() > 0:
                return _icon_color_for_bg(bg)
        return None  # let IconManager._default_color() handle it

    def refresh_icon(self):
        color = self._resolve_normal_color()
        icon = IconManager.get_icon(
            self._name, color, self._size,
            keep_original=self._keep_original
        )
        self.setIcon(icon)

    def changeEvent(self, event: QEvent):
        """Refresh icon whenever the widget's palette changes.

        A palette change is triggered automatically when:
        - A QSS stylesheet is applied to the widget or any ancestor.
        - The OS / system theme switches (light <-> dark).
        - QApplication.setPalette() is called.

        """
        if (event.type() == QEvent.Type.PaletteChange
                and self._normal_color is None
                and self._is_svg()
                and not self._keep_original):
            self.refresh_icon()
        super().changeEvent(event)

    def enterEvent(self, event):
        if self._hover_color and self._is_svg() and not self._keep_original:
            icon = IconManager.get_icon(
                self._name, self._hover_color, self._size,
                keep_original=False
            )
            self.setIcon(icon)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.refresh_icon()
        super().leaveEvent(event)