"""
Interface Principal
Janela principal da aplicação
"""

import os
import logging
from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                             QFrame, QScrollArea, QMessageBox)
from PyQt6.QtCore import Qt

from utils.image_handler import ImageHandler
from widgets.profile_widget import ProfileWidget
from widgets.search_widget import SearchWidget
from widgets.sidebar_widget import SidebarWidget
from widgets.content_widget import ContentWidget

logger = logging.getLogger(__name__)


class MainInterface(QMainWindow):
    """Interface principal da aplicação"""
    
    def __init__(self):
        super().__init__()
        self.profile_image = self.find_profile_image()
        self.highlight_color = self.get_theme_color()
        self.setupUI()
        self.connect_signals()

    def find_profile_image(self):
        """Procura por imagem de perfil nos formatos comuns"""
        possible_names = ["perfil.png", "profile.png", "avatar.png", "perfil.jpg", "profile.jpg"]
        for name in possible_names:
            if os.path.exists(name):
                return name
        return None

    def get_theme_color(self):
        """Obtém a cor tema baseada na imagem de perfil"""
        if self.profile_image:
            return ImageHandler.get_dominant_color(self.profile_image)
        return "#4a90e2"  # Cor padrão azul

    def setupUI(self):
        """Configura a interface principal"""
        self.setWindowTitle("Draconic Panel")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(900, 600)
        self.setStyleSheet("""
            QMainWindow { 
                background-color: #2a2a2a; 
                border: none;
                outline: none;
            }
            * {
                outline: none;
            }
        """)

        central_widget = QWidget()
        central_widget.setStyleSheet("border: none; outline: none;")
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Criar sidebar
        self.setup_sidebar()
        
        # Criar área de conteúdo
        self.setup_content_area()

        main_layout.addWidget(self.sidebar_frame)
        main_layout.addWidget(self.content_area, stretch=1)

    def setup_sidebar(self):
        """Configura a barra lateral"""
        self.sidebar_frame = QFrame()
        self.sidebar_frame.setFixedWidth(280)
        self.sidebar_frame.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #333333, stop:1 #2a2a2a);
                border: none;
                outline: none;
            }}
        """)

        sidebar_layout = QVBoxLayout(self.sidebar_frame)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)

        # Profile widget
        self.profile_widget = ProfileWidget(self.profile_image)
        self.profile_widget.set_highlight_color(self.highlight_color)
        sidebar_layout.addWidget(self.profile_widget)

        # Search widget
        self.search_widget = SearchWidget()
        self.search_widget.set_highlight_color(self.highlight_color)
        sidebar_layout.addWidget(self.search_widget)

        # Menu scroll area
        menu_scroll = QScrollArea()
        menu_scroll.setWidgetResizable(True)
        menu_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        menu_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        menu_scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        menu_scroll.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                outline: none;
                background-color: transparent;
            }}
            QScrollBar:vertical {{
                background-color: #3a3a3a;
                width: 8px;
                border: none;
                outline: none;
                border-radius: 4px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {self.highlight_color};
                border: none;
                outline: none;
                border-radius: 4px;
                min-height: 20px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                border: none;
                background: none;
            }}
        """)

        self.sidebar_menu = SidebarWidget()
        self.sidebar_menu.set_highlight_color(self.highlight_color)
        menu_scroll.setWidget(self.sidebar_menu)
        sidebar_layout.addWidget(menu_scroll)

    def setup_content_area(self):
        """Configura a área de conteúdo"""
        self.content_area = QFrame()
        self.content_area.setFrameShape(QFrame.Shape.NoFrame)
        self.content_area.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2a2a2a, stop:1 #1a1a1a);
                border: none;
                outline: none;
            }
            QFrame * {
                background: transparent;
                border: none;
                outline: none;
            }
        """)

        content_layout = QVBoxLayout(self.content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        self.content_widget = ContentWidget()
        content_layout.addWidget(self.content_widget)

    def connect_signals(self):
        """Conecta os sinais dos widgets"""
        self.sidebar_menu.menu_clicked.connect(self.on_menu_clicked)
        self.search_widget.search_changed.connect(self.sidebar_menu.filter_buttons)

    def on_menu_clicked(self, section):
        """Manipula cliques no menu"""
        logger.info(f"Menu clicked: {section}")
        self.content_widget.update_content(section)

    def show_error_message(self, title, message):
        """Mostra mensagem de erro"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.exec()