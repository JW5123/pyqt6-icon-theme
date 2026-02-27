import pytest
from pyqt6_icon_theme import IconManager, IconButton

@pytest.fixture(autouse=True)
def clear_cache():
    IconManager._icon_cache.clear()

class TestIconButton:
    def test_stem_only(self, qtbot):
        btn = IconButton("user", size=16)
        qtbot.addWidget(btn)
        assert btn._name == "user"

    def test_with_extension(self, qtbot):
        btn = IconButton("user.svg", size=16)
        qtbot.addWidget(btn)
        assert btn._name == "user"

    def test_custom_color(self, qtbot):
        btn = IconButton("add", size=16, normal_color="#49ADF0")
        qtbot.addWidget(btn)
        assert btn._normal_color == "#49ADF0"

    def test_hover_color(self, qtbot):
        btn = IconButton("add", size=36, normal_color="#49ADF0", hover_color="#F08884")
        qtbot.addWidget(btn)
        assert btn._hover_color == "#F08884"

    def test_keep_original(self, qtbot):
        btn = IconButton("edit-color", size=36, keep_original=True)
        qtbot.addWidget(btn)
        assert btn._keep_original is True

    def test_palette_auto_color_light(self, qtbot):
        btn = IconButton("user", size=16)
        qtbot.addWidget(btn)
        btn.setStyleSheet("background-color: white;")
        btn.show()
        qtbot.waitExposed(btn)
        assert btn._resolve_normal_color() == "#000000"

    def test_palette_auto_color_dark(self, qtbot):
        btn = IconButton("user", size=16)
        qtbot.addWidget(btn)
        btn.setStyleSheet("background-color: #1e1e1e;")
        btn.show()
        qtbot.waitExposed(btn)
        assert btn._resolve_normal_color() == "#FFFFFF"

    def test_png_is_not_svg(self, qtbot):
        btn = IconButton("delete.png", size=40)
        qtbot.addWidget(btn)
        assert not btn._is_svg()

    def test_invalid_icon_raises(self, qtbot):
        with pytest.raises(KeyError):
            IconButton("nonexistent_icon", size=16)