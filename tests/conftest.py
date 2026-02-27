import pytest
from pathlib import Path
from pyqt6_icon_theme import IconManager

ICONS_DIR = Path(__file__).parent.parent / "icons"

@pytest.fixture(scope="session", autouse=True)
def setup_icons():
    IconManager.set_icon_dir(ICONS_DIR)
    yield
    IconManager._icon_cache.clear()
    IconManager._svg_cache.clear()
    IconManager._raster_cache.clear()