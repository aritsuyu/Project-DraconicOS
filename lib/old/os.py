# decrapted, new version is coming soon
import sys
import winreg
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from themes import *

class WindowsSettingsApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.accent_color = "#0078d4"  # Azul padrão Windows
        self.dark_mode = self.detect_windows_theme()
        self.current_page = "Home"

        self.menu_data = [
            ("🏠", "Home", "Página inicial"),
            ("🎨", "Personalização", "Temas, cores e aparência"),
            ("🔧", "Sistema", "Informações e configurações do sistema"),
            ("🌐", "Rede", "Configurações de internet e rede"),
            ("🔒", "Privacidade", "Configurações de privacidade"),
            ("🔄", "Atualização", "Windows Update e segurança")
        ]

        self.card_data_home = [
            ("Atualizações", "3 disponíveis", "🔄", "Mantenha seu Windows atualizado"),
            ("Armazenamento", "512 GB", "💾", "Gerencie espaço em disco"),
            ("Rede", "Conectado", "🌐", "Status da conexão"),
            ("Segurança", "Protegido", "🛡️", "Windows Defender ativo"),
            ("Energia", "Balanceado", "🔋", "Configurações de energia"),
            ("Aplicativos", "127 instalados", "📱", "Gerenciar programas")
        ]

        self.quick_toggles_data = [
            ("Modo Noturno", True),
            ("Notificações", True),
            ("Localização", False),
            ("Bluetooth", True)
        ]

        self.theme_colors = [
            ("#0078d4", "Azul Windows"),
            ("#107c10", "Verde"),
            ("#d13438", "Vermelho"),
            ("#ff8c00", "Laranja"),
            ("#5c2d91", "Roxo"),
            ("#008272", "Teal"),
        ]

        self.init_ui()

    def detect_windows_theme(self):
        try:
            registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            key = winreg.OpenKey(registry, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize")
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            winreg.CloseKey(key)
            return value == 0  # 0 = escuro, 1 = claro
        except Exception:
            return False  # fallback escuro

    def init_ui(self):
        self.setWindowTitle("Configurações do Windows - Personalizado")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(900, 700)

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        sidebar = QWidget()
        sidebar.setFixedWidth(280)
        sidebar.setObjectName("sidebar")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(20, 30, 20, 20)
        sidebar_layout.setSpacing(15)

        title_label = QLabel("⚙️ Configurações")
        title_label.setObjectName("title")
        sidebar_layout.addWidget(title_label)
        sidebar_layout.addSpacing(20)

        self.menu_buttons = []
        for icon, text, desc in self.menu_data:
            btn_widget = self.create_menu_button(icon, text, desc)
            sidebar_layout.addWidget(btn_widget)

        sidebar_layout.addStretch()
        main_layout.addWidget(sidebar)

        # Main content
        content_area = QWidget()
        content_area.setObjectName("contentArea")
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(40, 40, 40, 40)
        content_layout.setSpacing(25)

        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)

        self.page_title = QLabel("Home")
        self.page_title.setObjectName("pageTitle")
        header_layout.addWidget(self.page_title)
        header_layout.addStretch()

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Pesquisar configurações...")
        self.search_bar.setObjectName("searchBar")
        self.search_bar.setFixedWidth(350)
        header_layout.addWidget(self.search_bar)

        content_layout.addWidget(header)

        self.content_stack = QStackedWidget()
        self.content_stack.setObjectName("contentStack")

        # Criar páginas dinâmicas
        self.pages = {}
        self.pages["Home"] = self.create_home_page()
        self.pages["Personalização"] = self.create_personalization_page()
        self.pages["Sistema"] = self.create_system_page()
        self.pages["Rede"] = self.create_network_page()
        self.pages["Privacidade"] = self.create_privacy_page()
        self.pages["Atualização"] = self.create_update_page()

        for key in self.menu_data:
            page_name = key[1]
            if page_name in self.pages:
                self.content_stack.addWidget(self.pages[page_name])

        content_layout.addWidget(self.content_stack)
        main_layout.addWidget(content_area)

        # Status bar
        self.status_bar = QStatusBar()
        self.status_bar.setObjectName("statusBar")
        self.statusBar().showMessage(f"Tema: {'Escuro' if self.dark_mode else 'Claro'} | Windows 11")
        self.setStatusBar(self.status_bar)

    def create_menu_button(self, icon, text, description):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        btn = QPushButton(f"{icon}  {text}")
        btn.setObjectName("menuButton")
        btn.clicked.connect(lambda _, t=text: self.on_menu_click(t))
        self.menu_buttons.append(btn)

        desc_label = QLabel(description)
        desc_label.setObjectName("menuDescription")
        desc_label.setWordWrap(True)

        layout.addWidget(btn)
        layout.addWidget(desc_label)
        return container

    def create_info_card(self, title, value, icon, description):
        card = QWidget()
        card.setObjectName("infoCard")
        card.setFixedHeight(140)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(8)

        header_layout = QHBoxLayout()
        icon_label = QLabel(icon)
        icon_label.setObjectName("cardIcon")
        header_layout.addWidget(icon_label)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        value_label = QLabel(value)
        value_label.setObjectName("cardValue")
        layout.addWidget(value_label)

        title_label = QLabel(title)
        title_label.setObjectName("cardTitle")
        layout.addWidget(title_label)

        desc_label = QLabel(description)
        desc_label.setObjectName("cardDescription")
        layout.addWidget(desc_label)

        return card

    def create_quick_toggle(self, name, state):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        label = QLabel(name)
        layout.addWidget(label)
        layout.addStretch()
        toggle = QCheckBox()
        toggle.setChecked(state)
        toggle.setObjectName("toggleSwitch")
        layout.addWidget(toggle)
        return widget

    def create_home_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(25)

        cards_widget = QWidget()
        cards_layout = QGridLayout(cards_widget)
        cards_layout.setSpacing(20)

        for i, (title, value, icon, desc) in enumerate(self.card_data_home):
            card = self.create_info_card(title, value, icon, desc)
            cards_layout.addWidget(card, i // 3, i % 3)

        layout.addWidget(cards_widget)

        quick_settings = QWidget()
        quick_layout = QVBoxLayout(quick_settings)

        quick_title = QLabel("Configurações Rápidas")
        quick_title.setObjectName("sectionTitle")
        quick_layout.addWidget(quick_title)

        for name, state in self.quick_toggles_data:
            quick_layout.addWidget(self.create_quick_toggle(name, state))

        layout.addWidget(quick_settings)
        return page

    def create_personalization_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(25)

        # Tema
        theme_section = QWidget()
        theme_layout = QVBoxLayout(theme_section)
        theme_title = QLabel("Aparência")
        theme_title.setObjectName("sectionTitle")
        theme_layout.addWidget(theme_title)

        theme_buttons = QWidget()
        theme_btn_layout = QHBoxLayout(theme_buttons)

        # Botões salvos como atributos para conectar depois no main()
        self.btn_light = QPushButton("☀️ Claro")
        self.btn_light.setObjectName("themeSelector")

        self.btn_dark = QPushButton("🌙 Escuro")
        self.btn_dark.setObjectName("themeSelector")

        self.btn_auto = QPushButton("🔄 Automático")
        self.btn_auto.setObjectName("themeSelector")

        theme_btn_layout.addWidget(self.btn_light)
        theme_btn_layout.addWidget(self.btn_dark)
        theme_btn_layout.addWidget(self.btn_auto)
        theme_btn_layout.addStretch()

        theme_layout.addWidget(theme_buttons)

        # Cores
        color_section = QWidget()
        color_layout = QVBoxLayout(color_section)
        color_title = QLabel("Cor de Destaque")
        color_title.setObjectName("sectionTitle")
        color_layout.addWidget(color_title)

        color_grid = QWidget()
        color_grid_layout = QGridLayout(color_grid)

        for i, (color, name) in enumerate(self.theme_colors):
            btn = QPushButton(name)
            btn.setObjectName("colorSelector")
            btn.setStyleSheet(f"QPushButton#colorSelector {{ background-color: {color}; }}")
            btn.clicked.connect(lambda checked, c=color: self.set_accent_color(c))
            color_grid_layout.addWidget(btn, i // 2, i % 2)

        color_layout.addWidget(color_grid)

        layout.addWidget(theme_section)
        layout.addWidget(color_section)
        layout.addStretch()

        return page

    def create_system_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        info_label = QLabel("Informações do Sistema")
        info_label.setObjectName("sectionTitle")
        layout.addWidget(info_label)

        system_info = QTextEdit()
        system_info.setObjectName("systemInfo")
        system_info.setReadOnly(True)
        system_info.setPlainText(
            "Sistema Operacional: Windows 11\n"
            "Versão: 22H2\n"
            "Processador: Intel Core i7-12700K\n"
            "Memória RAM: 16 GB\n"
            "Armazenamento: SSD 1TB\n"
            "Placa de Vídeo: NVIDIA RTX 3070"
        )
        layout.addWidget(system_info)
        return page

    def create_network_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        title = QLabel("Configurações de Rede")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)

        network_status = QLabel("Status: Conectado à Internet\nIP: 192.168.1.100\nDNS: 8.8.8.8")
        network_status.setObjectName("networkStatus")
        layout.addWidget(network_status)

        layout.addStretch()
        return page

    def create_privacy_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        title = QLabel("Configurações de Privacidade")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)

        privacy_info = QLabel("Gerencie suas configurações de privacidade e dados pessoais")
        layout.addWidget(privacy_info)

        layout.addStretch()
        return page

    def create_update_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        title = QLabel("Windows Update")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)

        update_status = QLabel("Última verificação: Hoje, 14:30\n3 atualizações disponíveis")
        layout.addWidget(update_status)

        check_btn = QPushButton("Verificar atualizações")
        check_btn.setObjectName("actionButton")
        layout.addWidget(check_btn)

        layout.addStretch()
        return page

    def on_menu_click(self, menu_name):
        self.current_page = menu_name
        self.page_title.setText(menu_name)

        menu_index = {name: i for i, (_, name, _) in enumerate(self.menu_data)}
        if menu_name in menu_index:
            self.content_stack.setCurrentIndex(menu_index[menu_name])

        for btn in self.menu_buttons:
            active = menu_name in btn.text()
            btn.setProperty("active", active)
            btn.style().unpolish(btn)
            btn.style().polish(btn)


def main():
    app = QApplication(sys.argv)
    window = WindowsSettingsApp()

    from types import MethodType
    import themes
    window.set_theme = MethodType(themes.set_theme, window)
    window.auto_theme = MethodType(themes.auto_theme, window)
    window.set_accent_color = MethodType(themes.set_accent_color, window)
    window.setup_styles = MethodType(themes.setup_styles, window)

    # conecta os botões de tema só depois que as funções existem no objeto
    window.btn_light.clicked.connect(lambda: window.set_theme(False))
    window.btn_dark.clicked.connect(lambda: window.set_theme(True))
    window.btn_auto.clicked.connect(window.auto_theme)

    window.setup_styles()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
