import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QScrollArea, QFrame, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect
from PyQt6.QtGui import QFont, QColor, QPixmap
from PIL import Image

# Função para pegar a cor predominante
def get_dominant_color(image_path):
    img = Image.open(image_path)
    img = img.resize((50, 50))
    img = img.convert("RGB")
    pixels = list(img.getdata())
    avg_r = sum([p[0] for p in pixels]) // len(pixels)
    avg_g = sum([p[1] for p in pixels]) // len(pixels)
    avg_b = sum([p[2] for p in pixels]) // len(pixels)
    return QColor(avg_r, avg_g, avg_b).name()

# Carregar cor predominante do perfil
PROFILE_IMG = "perfil.png"
if not os.path.exists(PROFILE_IMG):
    print(f"ERRO: a imagem {PROFILE_IMG} não foi encontrada.")
    sys.exit()

HIGHLIGHT_COLOR = get_dominant_color(PROFILE_IMG)


class AnimatedButton(QPushButton):
    def __init__(self, text, icon_text="", parent=None):
        super().__init__(parent)
        self.setText(f"  {icon_text}  {text}")
        self.setFixedHeight(50)
        self.original_color = "#3a3a3a"
        self.hover_color = HIGHLIGHT_COLOR
        self.text_color = "#ffffff"

        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.original_color};
                color: {self.text_color};
                border: none;
                border-radius: 8px;
                padding: 10px 15px;
                font-size: 14px;
                font-weight: 500;
                text-align: left;
                margin: 2px;
            }}
            QPushButton:hover {{
                background-color: {self.hover_color};
                color: white;
            }}
            QPushButton:pressed {{
                background-color: {HIGHLIGHT_COLOR};
            }}
        """)

        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)

    def enterEvent(self, event):
        super().enterEvent(event)
        current_geometry = self.geometry()
        new_geometry = QRect(current_geometry.x() - 2, current_geometry.y(),
                             current_geometry.width() + 4, current_geometry.height())
        self.animation.setStartValue(current_geometry)
        self.animation.setEndValue(new_geometry)
        self.animation.start()

    def leaveEvent(self, event):
        super().leaveEvent(event)
        current_geometry = self.geometry()
        new_geometry = QRect(current_geometry.x() + 2, current_geometry.y(),
                             current_geometry.width() - 4, current_geometry.height())
        self.animation.setStartValue(current_geometry)
        self.animation.setEndValue(new_geometry)
        self.animation.start()


class ProfileWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(80)
        self.setupUI()

    def setupUI(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(10)

        # Avatar
        self.avatar_label = QLabel()
        self.avatar_label.setFixedSize(60, 60)
        pixmap = QPixmap(PROFILE_IMG).scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio,
                                             Qt.TransformationMode.SmoothTransformation)
        self.avatar_label.setPixmap(pixmap)
        self.avatar_label.setStyleSheet(f"""
            QLabel {{
                border-radius: 30px;
                border: 3px solid {HIGHLIGHT_COLOR};
                background-color: transparent;
            }}
        """)

        # Layout de informações (nome + status)
        info_layout = QVBoxLayout()
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(2)

        name_status_layout = QHBoxLayout()
        name_status_layout.setContentsMargins(0, 0, 0, 0)
        name_status_layout.setSpacing(5)  # distância entre nome e status

        name_label = QLabel("John Doe")
        name_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
                border: none;
                background-color: transparent;
            }
        """)

        status_label = QLabel("sudo")
        status_label.setStyleSheet(f"""
            QLabel {{
                color: {HIGHLIGHT_COLOR};
                font-size: 12px;
                border: none;
                background-color: transparent;
            }}
        """)

        name_status_layout.addWidget(name_label)
        name_status_layout.addWidget(status_label)
        name_status_layout.addStretch()

        info_layout.addLayout(name_status_layout)
        layout.addWidget(self.avatar_label)
        layout.addLayout(info_layout)
        layout.addStretch()


class SearchWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUI()

    def setupUI(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search")
        self.search_input.setFixedHeight(40)
        self.search_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: #4a4a4a;
                color: white;
                border: 2px solid #5a5a5a;
                border-radius: 20px;
                padding: 8px 15px;
                font-size: 14px;
            }}
            QLineEdit:focus {{
                border-color: {HIGHLIGHT_COLOR};
                background-color: #555555;
            }}
        """)

        layout.addWidget(self.search_input)


class MenuButton(AnimatedButton):
    def __init__(self, text, icon, parent=None):
        super().__init__(text, icon, parent)


class SidebarWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 10)
        layout.setSpacing(5)

        menu_items = [
            ("🏠", "Home"),
            ("⚙️", "System"),
            ("🌐", "Ethernet"), 
            ("🚀", "Performance"),
            ("🎨", "Personalization"),
            ("📱", "Apps"),
            ("🎮", "Gaming"),
            ("🔧", "Autofixer"),
            ("➕", "Extras"),
            ("⚡", "Tweaks"),
            ("⭐", "Astrea")
        ]

        for icon, text in menu_items:
            btn = MenuButton(text, icon)
            layout.addWidget(btn)

        layout.addStretch()


class MainInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gaming Control Panel")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(900, 600)
        self.setStyleSheet("QMainWindow { background-color: #2a2a2a; }")
        self.setupUI()

    def setupUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        sidebar = QFrame()
        sidebar.setFixedWidth(280)
        sidebar.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #333333, stop:1 #2a2a2a);
                border-right: 2px solid {HIGHLIGHT_COLOR};
            }}
        """)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)

        profile = ProfileWidget()
        sidebar_layout.addWidget(profile)

        search = SearchWidget()
        sidebar_layout.addWidget(search)

        menu_scroll = QScrollArea()
        menu_scroll.setWidgetResizable(True)
        menu_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        menu_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        menu_scroll.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: transparent;
            }}
            QScrollBar:vertical {{
                background-color: #3a3a3a;
                width: 12px;
                border-radius: 6px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {HIGHLIGHT_COLOR};
                border-radius: 6px;
                min-height: 20px;
            }}
        """)

        sidebar_menu = SidebarWidget()
        menu_scroll.setWidget(sidebar_menu)
        sidebar_layout.addWidget(menu_scroll)

        # Content Area
        content_area = QFrame()
        content_area.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2a2a2a, stop:1 #1a1a1a);
            }
        """)

        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(30, 30, 30, 30)

        welcome_label = QLabel("Welcome to Gaming Control Panel")
        welcome_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 20px;
            }
        """)

        description_label = QLabel("Select an option from the sidebar to get started")
        description_label.setStyleSheet("""
            QLabel {
                color: #aaaaaa;
                font-size: 14px;
                margin-bottom: 20px;
            }
        """)

        content_layout.addWidget(welcome_label)
        content_layout.addWidget(description_label)
        content_layout.addStretch()

        main_layout.addWidget(sidebar)
        main_layout.addWidget(content_area, stretch=1)


def main():
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    window = MainInterface()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
