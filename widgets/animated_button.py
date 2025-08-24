"""
Botão Animado
Widget de botão com animações suaves
"""

from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import pyqtSignal, QPropertyAnimation, QEasingCurve


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