"""
Widget do Perfil
Widget para exibir informações do perfil do usuário
"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

from utils.image_handler import ImageHandler


class ProfileWidget(QWidget):
    """Widget do perfil do usuário"""
    
    def __init__(self, profile_image_path="perfil.png", parent=None):
        super().__init__(parent)
        self.profile_image_path = profile_image_path
        self.setFixedHeight(80)
        self.highlight_color = "#4a90e2"  # Cor padrão
        self.setupUI()

    def set_highlight_color(self, color):
        """Define a cor de destaque"""
        self.highlight_color = color
        self.update_style()

    def setupUI(self):
        """Configura a interface do perfil"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(10)

        # Avatar
        self.avatar_label = QLabel()
        self.avatar_label.setFixedSize(60, 60)
        
        # Criar pixmap circular
        pixmap = ImageHandler.create_circular_pixmap(self.profile_image_path, 60)
        self.avatar_label.setPixmap(pixmap)
        
        # Layout de informações
        info_layout = QVBoxLayout()
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(2)

        name_status_layout = QHBoxLayout()
        name_status_layout.setContentsMargins(0, 0, 0, 0)
        name_status_layout.setSpacing(5)

        self.name_label = QLabel("John Doe")
        self.name_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
                border: none;
                outline: none;
                background-color: transparent;
            }
        """)

        self.status_label = QLabel("sudo")
        
        name_status_layout.addWidget(self.name_label)
        name_status_layout.addWidget(self.status_label)
        name_status_layout.addStretch()

        info_layout.addLayout(name_status_layout)
        layout.addWidget(self.avatar_label)
        layout.addLayout(info_layout)
        layout.addStretch()
        
        self.update_style()

    def update_style(self):
        """Atualiza o estilo com a cor de destaque"""
        self.avatar_label.setStyleSheet(f"""
            QLabel {{
                border-radius: 30px;
                border: 2px solid {self.highlight_color};
                background-color: transparent;
                outline: none;
            }}
        """)
        
        self.status_label.setStyleSheet(f"""
            QLabel {{
                color: {self.highlight_color};
                font-size: 12px;
                border: none;
                outline: none;
                background-color: transparent;
            }}
        """)