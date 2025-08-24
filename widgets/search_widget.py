"""
Widget de Pesquisa
Widget para funcionalidade de busca
"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLineEdit
from PyQt6.QtCore import pyqtSignal


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