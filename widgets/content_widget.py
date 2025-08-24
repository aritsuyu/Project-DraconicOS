"""
Widget de Conteúdo
Widget principal para exibir o conteúdo das diferentes seções
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

from widgets.extras_widget import ExtrasWidget


class ContentWidget(QWidget):
    """Widget de conteúdo principal"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUI()

    def setupUI(self):
        """Configura a interface de conteúdo"""
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Widget de boas-vindas padrão
        self.default_widget = self.create_default_widget()
        self.layout.addWidget(self.default_widget)

        # Widget específico para extras (inicialmente oculto)
        self.extras_widget = ExtrasWidget()
        self.extras_widget.setVisible(False)
        self.layout.addWidget(self.extras_widget)

    def create_default_widget(self):
        """Cria o widget padrão de boas-vindas"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
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

        layout.addWidget(self.welcome_label)
        layout.addWidget(self.description_label)
        layout.addStretch()

        return widget

    def update_content(self, section):
        """Atualiza o conteúdo baseado na seção selecionada"""
        if section == "extras":
            self.default_widget.setVisible(False)
            self.extras_widget.setVisible(True)
        else:
            self.extras_widget.setVisible(False)
            self.default_widget.setVisible(True)
            
            # Atualizar conteúdo padrão
            content_map = {
                "home": ("Home", "Welcome to the main dashboard"),
                "system": ("System Settings", "Configure system parameters and monitoring"),
                "ethernet": ("Network Settings", "Manage network connections and settings"),
                "performance": ("Performance Tuning", "Optimize system performance and resources"),
                "personalization": ("Personalization", "Customize appearance and themes"),
                "apps": ("Applications", "Manage installed applications and software"),
                "gaming": ("Gaming Hub", "Gaming optimization and configuration"),
                "autofixer": ("Auto Fixer", "Automatic system repair and optimization"),
                "tweaks": ("System Tweaks", "Advanced system tweaks and modifications"),
                "astrea": ("Astrea AI", "Astrea AI assistant and tools")
            }
            
            if section in content_map:
                title, description = content_map[section]
                self.welcome_label.setText(title)
                self.description_label.setText(description)
            else:
                self.welcome_label.setText("Unknown Section")
                self.description_label.setText("This section is not implemented yet")