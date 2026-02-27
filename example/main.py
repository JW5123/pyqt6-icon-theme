import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QPushButton, QLabel
)
from pyqt6_icon_theme import IconManager, IconButton
from style import LIGHT_STYLE, DARK_STYLE

class TestWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Icon Theme Test")
        self.resize(400, 300)

        layout = QVBoxLayout(self)
        IconManager.set_icon_dir("icons")
        self.dark = False

        self.label = QLabel("svg default color auto-detect (Light/Dark):")
        layout.addWidget(self.label)
        layout.addWidget(IconButton("user.svg", size=30))

        self.label = QLabel("svg default color (hover color set):")
        layout.addWidget(self.label)
        layout.addWidget(IconButton("user.svg", size=30, hover_color="#3B82F6"))

        self.label = QLabel("custom colors + hover:")
        layout.addWidget(self.label)
        layout.addWidget(IconButton("add.svg", size=36,
                                    normal_color="#49ADF0",
                                    hover_color="#F08884"))

        self.label = QLabel("keep original colors (for colorful svg icons):")
        layout.addWidget(self.label)
        layout.addWidget(IconButton("edit-color.svg", size=36, keep_original=True))

        self.label = QLabel("png icon (color setting is invalid):")
        layout.addWidget(self.label)
        layout.addWidget(IconButton("delete.png", size=40))

        self.label = QLabel("Current Theme: Light")
        layout.addWidget(self.label)

        toggle = QPushButton("Toggle Theme")
        toggle.clicked.connect(self.toggle_theme)
        layout.addWidget(toggle)

        self.setStyleSheet(LIGHT_STYLE)

    def toggle_theme(self):
        self.dark = not self.dark
        if self.dark:
            self.setStyleSheet(DARK_STYLE)
            self.label.setText("Current Theme: Dark")
        else:
            self.setStyleSheet(LIGHT_STYLE)
            self.label.setText("Current Theme: Light")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = TestWindow()
    w.show()
    sys.exit(app.exec())