import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QScrollArea, QFrame, QGraphicsDropShadowEffect,
                             QMessageBox)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QPixmap, QPainter, QPainterPath
from PIL import Image, ImageOps
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImageHandler:
    """Classe para gerenciar operações com imagens"""
    
    @staticmethod
    def get_dominant_color(image_path):
        """Extrai a cor predominante de uma imagem"""
        try:
            with Image.open(image_path) as img:
                # Redimensionar para acelerar o processamento
                img = img.resize((50, 50))
                img = img.convert("RGB")
                pixels = list(img.getdata())
                
                if not pixels:
                    return "#4a90e2"  # Cor padrão
                
                # Calcular média das cores
                avg_r = sum(p[0] for p in pixels) // len(pixels)
                avg_g = sum(p[1] for p in pixels) // len(pixels) 
                avg_b = sum(p[2] for p in pixels) // len(pixels)
                
                return QColor(avg_r, avg_g, avg_b).name()
        except Exception as e:
            logger.error(f"Erro ao processar imagem {image_path}: {e}")
            return "#4a90e2"  # Cor padrão em caso de erro
    
    @staticmethod
    def create_circular_pixmap(image_path, size):
        """Cria um QPixmap circular da imagem"""
        try:
            pixmap = QPixmap(image_path)
            if pixmap.isNull():
                # Criar um pixmap padrão se a imagem não carregar
                pixmap = QPixmap(size, size)
                pixmap.fill(QColor("#4a90e2"))
            else:
                pixmap = pixmap.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                                     Qt.TransformationMode.SmoothTransformation)
            
            # Criar máscara circular
            circular_pixmap = QPixmap(size, size)
            circular_pixmap.fill(Qt.GlobalColor.transparent)
            
            painter = QPainter(circular_pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            path = QPainterPath()
            path.addEllipse(0, 0, size, size)
            painter.setClipPath(path)
            
            # Desenhar a imagem centralizada
            x = (size - pixmap.width()) // 2
            y = (size - pixmap.height()) // 2
            painter.drawPixmap(x, y, pixmap)
            painter.end()
            
            return circular_pixmap
        except Exception as e:
            logger.error(f"Erro ao criar pixmap circular: {e}")
            # Retornar um pixmap padrão
            pixmap = QPixmap(size, size)
            pixmap.fill(QColor("#4a90e2"))
            return pixmap


class AnimatedButton(QPushButton):
    """Botão com animações suaves"""
    clicked_with_data = pyqtSignal(str)  # Signal personalizado
    
    def __init__(self, text, icon_text="", data=None, parent=None):
        super().__init__(parent)
        self.data = data or text
        self.setText(f"  {icon_text}  {text}")
        self.setFixedHeight(50)
        self.original_color = "#3a3a3a"
        self.hover_color = "#4a90e2"  # Cor padrão
        self.text_color = "#ffffff"
        
        self.setup_style()
        self.setup_animation()
        
        # Conectar sinal personalizado
        self.clicked.connect(lambda: self.clicked_with_data.emit(self.data))

    def set_highlight_color(self, color):
        """Define a cor de destaque do botão"""
        self.hover_color = color
        self.setup_style()

    def setup_style(self):
        """Configura o estilo do botão"""
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.original_color};
                color: {self.text_color};
                border: none;
                outline: none;
                border-radius: 8px;
                padding: 10px 15px;
                font-size: 14px;
                font-weight: 500;
                text-align: left;
                margin: 3px 5px;
                min-width: 200px;
                max-width: 260px;
            }}
            QPushButton:hover {{
                background-color: {self.hover_color};
                color: white;
                border: none;
                outline: none;
            }}
            QPushButton:pressed {{
                background-color: {self.hover_color};
                color: white;
                border: none;
                outline: none;
            }}
            QPushButton:focus {{
                border: none;
                outline: none;
                background-color: {self.hover_color};
            }}
        """)

    def setup_animation(self):
        """Configura a animação do botão"""
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)

    def enterEvent(self, event):
        """Animação ao passar o mouse - removida para evitar assimetria"""
        super().enterEvent(event)
        # Apenas mudança de cor, sem animação de tamanho
        pass

    def leaveEvent(self, event):
        """Animação ao sair o mouse - removida para evitar assimetria"""
        super().leaveEvent(event)
        # Apenas mudança de cor, sem animação de tamanho
        pass


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


class SearchWidget(QWidget):
    """Widget de pesquisa"""
    search_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlight_color = "#4a90e2"
        self.setupUI()

    def set_highlight_color(self, color):
        """Define a cor de destaque"""
        self.highlight_color = color
        self.update_style()

    def setupUI(self):
        """Configura a interface de pesquisa"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search...")
        self.search_input.setFixedHeight(40)
        
        # Conectar sinal de mudança de texto
        self.search_input.textChanged.connect(self.search_changed.emit)
        
        layout.addWidget(self.search_input)
        self.update_style()

    def update_style(self):
        """Atualiza o estilo com a cor de destaque"""
        self.search_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: #4a4a4a;
                color: white;
                border: none;
                outline: none;
                border-radius: 20px;
                padding: 8px 15px;
                font-size: 14px;
            }}
            QLineEdit:focus {{
                background-color: #555555;
                border: none;
                outline: none;
            }}
        """)


class SidebarWidget(QWidget):
    """Widget da barra lateral"""
    menu_clicked = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlight_color = "#4a90e2"
        self.buttons = []
        self.setupUI()

    def set_highlight_color(self, color):
        """Define a cor de destaque para todos os botões"""
        self.highlight_color = color
        for button in self.buttons:
            button.set_highlight_color(color)

    def setupUI(self):
        """Configura a interface da barra lateral"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 0, 8, 10)
        layout.setSpacing(3)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        menu_items = [
            ("🏠", "Home", "home"),
            ("⚙️", "System", "system"),
            ("🌐", "Ethernet", "ethernet"), 
            ("🚀", "Performance", "performance"),
            ("🎨", "Personalization", "personalization"),
            ("📱", "Apps", "apps"),
            ("🎮", "Gaming", "gaming"),
            ("🔧", "Autofixer", "autofixer"),
            ("➕", "Extras", "extras"),
            ("⚡", "Tweaks", "tweaks"),
            ("⭐", "Astrea", "astrea")
        ]

        for icon, text, data in menu_items:
            btn = AnimatedButton(text, icon, data)
            btn.set_highlight_color(self.highlight_color)
            btn.clicked_with_data.connect(self.menu_clicked.emit)
            self.buttons.append(btn)
            layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()

    def filter_buttons(self, search_text):
        """Filtra botões baseado no texto de pesquisa"""
        search_text = search_text.lower()
        for button in self.buttons:
            button_text = button.text().lower()
            if search_text in button_text:
                button.setVisible(True)
            else:
                button.setVisible(False)


class ContentWidget(QWidget):
    """Widget de conteúdo principal"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUI()

    def setupUI(self):
        """Configura a interface de conteúdo"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        self.welcome_label = QLabel("Welcome to Gaming Control Panel")
        self.welcome_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 28px;
                font-weight: bold;
                background: transparent;
                border: none;
                padding: 0;
                margin: 0;
            }
        """)

        self.description_label = QLabel("Select an option from the sidebar to get started")
        self.description_label.setStyleSheet("""
            QLabel {
                color: #cccccc;
                font-size: 16px;
                font-weight: normal;
                background: transparent;
                border: none;
                padding: 0;
                margin: 0;
                line-height: 1.4;
            }
        """)

        # Container para centralizar o conteúdo
        content_container = QWidget()
        content_container.setStyleSheet("background: transparent; border: none;")
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(15)
        
        content_layout.addWidget(self.welcome_label)
        content_layout.addWidget(self.description_label)
        content_layout.addStretch()

        layout.addWidget(content_container)
        layout.addStretch()

    def update_content(self, section):
        """Atualiza o conteúdo baseado na seção selecionada"""
        content_map = {
            "home": ("Home", "Welcome to the main dashboard"),
            "system": ("System Settings", "Configure system parameters and monitoring"),
            "ethernet": ("Network Settings", "Manage network connections and settings"),
            "performance": ("Performance Tuning", "Optimize system performance and resources"),
            "personalization": ("Personalization", "Customize appearance and themes"),
            "apps": ("Applications", "Manage installed applications and software"),
            "gaming": ("Gaming Hub", "Gaming optimization and configuration"),
            "autofixer": ("Auto Fixer", "Automatic system repair and optimization"),
            "extras": ("Extra Tools", "Additional utilities and tools"),
            "tweaks": ("System Tweaks", "Advanced system tweaks and modifications"),
            "astrea": ("Astrea AI", "Astrea AI")
        }
        
        if section in content_map:
            title, description = content_map[section]
            self.welcome_label.setText(title)
            self.description_label.setText(description)
        else:
            self.welcome_label.setText("Unknown Section")
            self.description_label.setText("This section is not implemented yet")


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
        self.setWindowTitle("Gaming Control Panel")
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


def main():
    """Função principal"""
    try:
        app = QApplication(sys.argv)
        
        # Configurar fonte padrão
        font = QFont("Segoe UI", 10)
        app.setFont(font)

        # Verificar se PIL está disponível
        try:
            from PIL import Image
        except ImportError:
            print("AVISO: PIL (Pillow) não encontrado. Funcionalidades de imagem podem ser limitadas.")

        window = MainInterface()
        window.show()
        
        sys.exit(app.exec())
        
    except Exception as e:
        logger.error(f"Erro na execução: {e}")
        print(f"Erro crítico: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()