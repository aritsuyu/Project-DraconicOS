"""
Widget da Sidebar
Widget da barra lateral com menu de navegação
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import pyqtSignal, Qt

from widgets.animated_button import AnimatedButton


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