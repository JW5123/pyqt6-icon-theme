from PyQt6.QtGui import QColor
import pytest
from pyqt6_icon_theme.core import _relative_luminance, _icon_color_for_bg


class TestRelativeLuminance:
    def test_black(self):
        assert _relative_luminance(QColor(0, 0, 0)) == pytest.approx(0.0)

    def test_white(self):
        assert _relative_luminance(QColor(255, 255, 255)) == pytest.approx(1.0, abs=1e-6)

    def test_mid_gray(self):
        lum = _relative_luminance(QColor(128, 128, 128))
        assert 0.0 < lum < 1.0

class TestIconColorForBg:
    def test_light_bg_returns_black(self):
        assert _icon_color_for_bg(QColor(255, 255, 255)) == "#000000"
        assert _icon_color_for_bg(QColor(240, 240, 240)) == "#000000"

    def test_dark_bg_returns_white(self):
        assert _icon_color_for_bg(QColor(0, 0, 0)) == "#FFFFFF"
        assert _icon_color_for_bg(QColor(30, 30, 30)) == "#FFFFFF"