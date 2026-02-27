import pytest
from pyqt6_icon_theme import IconManager

class TestSetIconDir:
    def test_valid_dir(self, setup_icons):
        assert len(IconManager._svg_cache) > 0 or len(IconManager._raster_cache) > 0

    def test_not_found(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            IconManager.set_icon_dir(tmp_path / "nonexistent")

    def test_not_a_dir(self, tmp_path):
        f = tmp_path / "file.txt"
        f.write_text("x")
        with pytest.raises(NotADirectoryError):
            IconManager.set_icon_dir(f)

class TestStripSvgColors:
    def test_fill_attribute(self):
        result = IconManager._strip_svg_colors('<circle fill="#FF0000"/>')
        assert 'fill="currentColor"' in result

    def test_stroke_attribute(self):
        result = IconManager._strip_svg_colors('<circle stroke="#FF0000"/>')
        assert 'stroke="currentColor"' in result

    def test_fill_none_preserved(self):
        result = IconManager._strip_svg_colors('<circle fill="none"/>')
        assert 'fill="none"' in result

    def test_stroke_none_preserved(self):
        result = IconManager._strip_svg_colors('<circle stroke="none"/>')
        assert 'stroke="none"' in result

    def test_inline_style(self):
        result = IconManager._strip_svg_colors('<circle style="fill:#FF0000"/>')
        assert 'fill:currentColor' in result