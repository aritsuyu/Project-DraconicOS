import sys
import winreg
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QPalette, QColor, QIcon

class WindowsSettingsApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dark_mode = self.detect_windows_theme()
        self.accent_color = "#0078d4"  # Azul padrão do Windows
        self.current_page = "Home"
        self.init_ui()
        self.setup_styles()
        
    def detect_windows_theme(self):
        """Detecta se o Windows está em tema escuro"""
        try:
            registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            key = winreg.OpenKey(registry, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize")
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            winreg.CloseKey(key)
            return value == 0  # 0 = tema escuro, 1 = tema claro
        except:
            return False  # Padrão para tema claro se não conseguir detectar
        
    def init_ui(self):
        self.setWindowTitle("Configurações do Windows - Personalizado")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(900, 700)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar
        self.create_sidebar(main_layout)
        
        # Área de conteúdo principal
        self.create_main_content(main_layout)
        
        # Barra de status moderna
        self.create_status_bar()
        
    def create_sidebar(self, parent_layout):
        sidebar = QWidget()
        sidebar.setFixedWidth(280)
        sidebar.setObjectName("sidebar")
        
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(20, 30, 20, 20)
        sidebar_layout.setSpacing(15)
        
        # Logo/Título
        title_label = QLabel("⚙️ Configurações")
        title_label.setObjectName("title")
        sidebar_layout.addWidget(title_label)
        
        sidebar_layout.addSpacing(20)
        
        # Botões do menu
        menu_buttons = [
            ("🏠", "Home", "Página inicial"),
            ("🎨", "Personalização", "Temas, cores e aparência"),
            ("🔧", "Sistema", "Informações e configurações do sistema"),
            ("🌐", "Rede", "Configurações de internet e rede"),
            ("🔒", "Privacidade", "Configurações de privacidade"),
            ("🔄", "Atualização", "Windows Update e segurança")
        ]
        
        self.menu_buttons = []
        for icon, text, description in menu_buttons:
            btn_container = QWidget()
            btn_layout = QVBoxLayout(btn_container)
            btn_layout.setContentsMargins(0, 0, 0, 0)
            btn_layout.setSpacing(2)
            
            btn = QPushButton(f"{icon}  {text}")
            btn.setObjectName("menuButton")
            btn.clicked.connect(lambda checked, t=text: self.on_menu_click(t))
            self.menu_buttons.append(btn)
            
            desc_label = QLabel(description)
            desc_label.setObjectName("menuDescription")
            desc_label.setWordWrap(True)
            
            btn_layout.addWidget(btn)
            btn_layout.addWidget(desc_label)
            sidebar_layout.addWidget(btn_container)
        
        sidebar_layout.addStretch()
        parent_layout.addWidget(sidebar)
        
    def create_main_content(self, parent_layout):
        content_area = QWidget()
        content_area.setObjectName("contentArea")
        
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(40, 40, 40, 40)
        content_layout.setSpacing(25)
        
        # Header
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        self.page_title = QLabel("Home")
        self.page_title.setObjectName("pageTitle")
        header_layout.addWidget(self.page_title)
        
        header_layout.addStretch()
        
        # Botão de busca
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Pesquisar configurações...")
        search_bar.setObjectName("searchBar")
        search_bar.setFixedWidth(350)
        header_layout.addWidget(search_bar)
        
        content_layout.addWidget(header)
        
        # Área de conteúdo dinâmico
        self.content_stack = QStackedWidget()
        self.content_stack.setObjectName("contentStack")
        
        # Criar todas as páginas
        self.create_home_page()
        self.create_personalization_page()
        self.create_system_page()
        self.create_network_page()
        self.create_privacy_page()
        self.create_update_page()
        
        content_layout.addWidget(self.content_stack)
        parent_layout.addWidget(content_area)
        
    def create_home_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(25)
        
        # Cards de configurações rápidas
        cards_widget = QWidget()
        cards_layout = QGridLayout(cards_widget)
        cards_layout.setSpacing(20)
        
        # Cards do sistema Windows
        card_data = [
            ("Atualizações", "3 disponíveis", "🔄", "Mantenha seu Windows atualizado"),
            ("Armazenamento", "512 GB", "💾", "Gerencie espaço em disco"),
            ("Rede", "Conectado", "🌐", "Status da conexão"),
            ("Segurança", "Protegido", "🛡️", "Windows Defender ativo"),
            ("Energia", "Balanceado", "🔋", "Configurações de energia"),
            ("Aplicativos", "127 instalados", "📱", "Gerenciar programas")
        ]
        
        for i, (title, value, icon, desc) in enumerate(card_data):
            card = self.create_info_card(title, value, icon, desc)
            cards_layout.addWidget(card, i // 3, i % 3)
            
        layout.addWidget(cards_widget)
        
        # Configurações rápidas
        quick_settings = QWidget()
        quick_layout = QVBoxLayout(quick_settings)
        
        quick_title = QLabel("Configurações Rápidas")
        quick_title.setObjectName("sectionTitle")
        quick_layout.addWidget(quick_title)
        
        # Switches para configurações comuns
        self.create_quick_toggles(quick_layout)
        
        layout.addWidget(quick_settings)
        self.content_stack.addWidget(page)
        
    def create_personalization_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(25)
        
        # Seção de tema
        theme_section = QWidget()
        theme_layout = QVBoxLayout(theme_section)
        
        theme_title = QLabel("Aparência")
        theme_title.setObjectName("sectionTitle")
        theme_layout.addWidget(theme_title)
        
        # Seletor de tema
        theme_group = QWidget()
        theme_group_layout = QHBoxLayout(theme_group)
        
        light_btn = QPushButton("☀️ Claro")
        light_btn.setObjectName("themeSelector")
        light_btn.clicked.connect(lambda: self.set_theme(False))
        
        dark_btn = QPushButton("🌙 Escuro")
        dark_btn.setObjectName("themeSelector")
        dark_btn.clicked.connect(lambda: self.set_theme(True))
        
        auto_btn = QPushButton("🔄 Automático")
        auto_btn.setObjectName("themeSelector")
        auto_btn.clicked.connect(self.auto_theme)
        
        theme_group_layout.addWidget(light_btn)
        theme_group_layout.addWidget(dark_btn)
        theme_group_layout.addWidget(auto_btn)
        theme_group_layout.addStretch()
        
        theme_layout.addWidget(theme_group)
        
        # Seletor de cor de destaque
        color_section = QWidget()
        color_layout = QVBoxLayout(color_section)
        
        color_title = QLabel("Cor de Destaque")
        color_title.setObjectName("sectionTitle")
        color_layout.addWidget(color_title)
        
        color_grid = QWidget()
        color_grid_layout = QGridLayout(color_grid)
        
        colors = [
            ("#0078d4", "Azul Windows"),
            ("#107c10", "Verde"),
            ("#d13438", "Vermelho"),
            ("#ff8c00", "Laranja"),
            ("#5c2d91", "Roxo"),
            ("#008272", "Teal"),
        ]
        
        for i, (color, name) in enumerate(colors):
            btn = QPushButton(name)
            btn.setObjectName("colorSelector")
            btn.setStyleSheet(f"QPushButton#colorSelector {{ background-color: {color}; }}")
            btn.clicked.connect(lambda checked, c=color: self.set_accent_color(c))
            color_grid_layout.addWidget(btn, i // 2, i % 2)
        
        color_layout.addWidget(color_grid)
        
        layout.addWidget(theme_section)
        layout.addWidget(color_section)
        layout.addStretch()
        
        self.content_stack.addWidget(page)
        
    def create_system_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        info_label = QLabel("Informações do Sistema")
        info_label.setObjectName("sectionTitle")
        layout.addWidget(info_label)
        
        system_info = QTextEdit()
        system_info.setObjectName("systemInfo")
        system_info.setReadOnly(True)
        system_info.setPlainText("""
Sistema Operacional: Windows 11
Versão: 22H2
Processador: Intel Core i7-12700K
Memória RAM: 16 GB
Armazenamento: SSD 1TB
Placa de Vídeo: NVIDIA RTX 3070
        """.strip())
        
        layout.addWidget(system_info)
        self.content_stack.addWidget(page)
        
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
        self.content_stack.addWidget(page)
        
    def create_privacy_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("Configurações de Privacidade")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)
        
        privacy_info = QLabel("Gerencie suas configurações de privacidade e dados pessoais")
        layout.addWidget(privacy_info)
        
        layout.addStretch()
        self.content_stack.addWidget(page)
        
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
        self.content_stack.addWidget(page)
        
    def create_info_card(self, title, value, icon, description):
        card = QWidget()
        card.setObjectName("infoCard")
        card.setFixedHeight(140)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(8)
        
        # Header do card
        header_layout = QHBoxLayout()
        
        icon_label = QLabel(icon)
        icon_label.setObjectName("cardIcon")
        header_layout.addWidget(icon_label)
        
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Valor principal
        value_label = QLabel(value)
        value_label.setObjectName("cardValue")
        layout.addWidget(value_label)
        
        # Título
        title_label = QLabel(title)
        title_label.setObjectName("cardTitle")
        layout.addWidget(title_label)
        
        # Descrição
        desc_label = QLabel(description)
        desc_label.setObjectName("cardDescription")
        layout.addWidget(desc_label)
        
        return card
        
    def create_quick_toggles(self, parent_layout):
        toggles = [
            ("Modo Noturno", True),
            ("Notificações", True),
            ("Localização", False),
            ("Bluetooth", True)
        ]
        
        for name, state in toggles:
            toggle_widget = QWidget()
            toggle_layout = QHBoxLayout(toggle_widget)
            
            label = QLabel(name)
            toggle_layout.addWidget(label)
            
            toggle_layout.addStretch()
            
            switch = QCheckBox()
            switch.setChecked(state)
            switch.setObjectName("toggleSwitch")
            toggle_layout.addWidget(switch)
            
            parent_layout.addWidget(toggle_widget)
        
    def create_status_bar(self):
        status_bar = QStatusBar()
        status_bar.setObjectName("statusBar")
        
        status_bar.showMessage(f"Tema: {'Escuro' if self.dark_mode else 'Claro'} | Windows 11")
        
        self.setStatusBar(status_bar)
        
    def on_menu_click(self, menu_name):
        self.current_page = menu_name
        self.page_title.setText(menu_name)
        
        # Mapear menu para índice da página
        menu_index = {
            "Home": 0, "Personalização": 1, "Sistema": 2, 
            "Rede": 3, "Privacidade": 4, "Atualização": 5
        }
        
        if menu_name in menu_index:
            self.content_stack.setCurrentIndex(menu_index[menu_name])
        
        # Atualizar estilo dos botões
        for btn in self.menu_buttons:
            btn.setProperty("active", menu_name in btn.text())
            btn.style().unpolish(btn)
            btn.style().polish(btn)
    
    def set_theme(self, dark):
        self.dark_mode = dark
        self.setup_styles()
        self.statusBar().showMessage(f"Tema: {'Escuro' if dark else 'Claro'} | Windows 11")
    
    def auto_theme(self):
        self.dark_mode = self.detect_windows_theme()
        self.setup_styles()
        self.statusBar().showMessage(f"Tema: Automático ({'Escuro' if self.dark_mode else 'Claro'}) | Windows 11")
    
    def set_accent_color(self, color):
        self.accent_color = color
        self.setup_styles()
        
    def setup_styles(self):
        if self.dark_mode:
            # Tema escuro
            self.setStyleSheet(f"""
                QMainWindow {{
                    background-color: #202020;
                }}
                
                #sidebar {{
                    background-color: #2d2d30;
                    border-right: 1px solid #3f3f46;
                }}
                
                #title {{
                    font-size: 24px;
                    font-weight: bold;
                    color: #ffffff;
                    padding: 10px 0;
                }}
                
                #menuButton {{
                    text-align: left;
                    padding: 15px 20px;
                    border: none;
                    border-radius: 6px;
                    background-color: transparent;
                    color: #cccccc;
                    font-size: 14px;
                    font-weight: 500;
                }}
                
                #menuButton:hover {{
                    background-color: #3f3f46;
                    color: #ffffff;
                }}
                
                #menuButton[active="true"] {{
                    background-color: {self.accent_color};
                    color: #ffffff;
                }}
                
                #menuDescription {{
                    color: #969696;
                    font-size: 11px;
                    padding-left: 20px;
                    margin-bottom: 10px;
                }}
                
                #contentArea {{
                    background-color: #1e1e1e;
                }}
                
                #pageTitle {{
                    font-size: 32px;
                    font-weight: 600;
                    color: #ffffff;
                    margin-bottom: 10px;
                }}
                
                #searchBar {{
                    padding: 12px 20px;
                    border: 2px solid #3f3f46;
                    border-radius: 6px;
                    background-color: #2d2d30;
                    color: #ffffff;
                    font-size: 14px;
                }}
                
                #searchBar:focus {{
                    border-color: {self.accent_color};
                    background-color: #252526;
                }}
                
                #infoCard {{
                    background-color: #2d2d30;
                    border-radius: 8px;
                    border: 1px solid #3f3f46;
                }}
                
                #infoCard:hover {{
                    border-color: {self.accent_color};
                    background-color: #323235;
                }}
                
                #cardIcon {{
                    font-size: 24px;
                }}
                
                #cardValue {{
                    font-size: 20px;
                    font-weight: bold;
                    color: #ffffff;
                }}
                
                #cardTitle {{
                    font-size: 14px;
                    color: #ffffff;
                    font-weight: 600;
                }}
                
                #cardDescription {{
                    font-size: 12px;
                    color: #cccccc;
                }}
                
                #sectionTitle {{
                    font-size: 20px;
                    font-weight: 600;
                    color: #ffffff;
                    margin-bottom: 15px;
                }}
                
                #themeSelector, #colorSelector, #actionButton {{
                    padding: 10px 20px;
                    border: 2px solid #3f3f46;
                    border-radius: 6px;
                    background-color: #2d2d30;
                    color: #ffffff;
                    font-weight: 500;
                }}
                
                #themeSelector:hover, #colorSelector:hover, #actionButton:hover {{
                    border-color: {self.accent_color};
                    background-color: #323235;
                }}
                
                #systemInfo, #networkStatus {{
                    background-color: #2d2d30;
                    border: 1px solid #3f3f46;
                    border-radius: 6px;
                    color: #ffffff;
                    padding: 15px;
                    font-family: 'Consolas', monospace;
                }}
                
                #toggleSwitch {{
                    padding: 5px;
                }}
                
                #statusBar {{
                    background-color: {self.accent_color};
                    color: #ffffff;
                    border: none;
                    font-weight: 500;
                }}
            """)
        else:
            # Tema claro
            self.setStyleSheet(f"""
                QMainWindow {{
                    background-color: #f3f3f3;
                }}
                
                #sidebar {{
                    background-color: #ffffff;
                    border-right: 1px solid #e1e5e9;
                }}
                
                #title {{
                    font-size: 24px;
                    font-weight: bold;
                    color: #323130;
                    padding: 10px 0;
                }}
                
                #menuButton {{
                    text-align: left;
                    padding: 15px 20px;
                    border: none;
                    border-radius: 6px;
                    background-color: transparent;
                    color: #605e5c;
                    font-size: 14px;
                    font-weight: 500;
                }}
                
                #menuButton:hover {{
                    background-color: #f3f2f1;
                    color: #323130;
                }}
                
                #menuButton[active="true"] {{
                    background-color: {self.accent_color};
                    color: #ffffff;
                }}
                
                #menuDescription {{
                    color: #8a8886;
                    font-size: 11px;
                    padding-left: 20px;
                    margin-bottom: 10px;
                }}
                
                #contentArea {{
                    background-color: #ffffff;
                }}
                
                #pageTitle {{
                    font-size: 32px;
                    font-weight: 600;
                    color: #323130;
                    margin-bottom: 10px;
                }}
                
                #searchBar {{
                    padding: 12px 20px;
                    border: 2px solid #e1e5e9;
                    border-radius: 6px;
                    background-color: #f3f2f1;
                    color: #323130;
                    font-size: 14px;
                }}
                
                #searchBar:focus {{
                    border-color: {self.accent_color};
                    background-color: #ffffff;
                }}
                
                #infoCard {{
                    background-color: #ffffff;
                    border-radius: 8px;
                    border: 1px solid #e1e5e9;
                }}
                
                #infoCard:hover {{
                    border-color: {self.accent_color};
                    background-color: #f8f9fa;
                }}
                
                #cardIcon {{
                    font-size: 24px;
                }}
                
                #cardValue {{
                    font-size: 20px;
                    font-weight: bold;
                    color: #323130;
                }}
                
                #cardTitle {{
                    font-size: 14px;
                    color: #323130;
                    font-weight: 600;
                }}
                
                #cardDescription {{
                    font-size: 12px;
                    color: #605e5c;
                }}
                
                #sectionTitle {{
                    font-size: 20px;
                    font-weight: 600;
                    color: #323130;
                    margin-bottom: 15px;
                }}
                
                #themeSelector, #colorSelector, #actionButton {{
                    padding: 10px 20px;
                    border: 2px solid #e1e5e9;
                    border-radius: 6px;
                    background-color: #ffffff;
                    color: #323130;
                    font-weight: 500;
                }}
                
                #themeSelector:hover, #colorSelector:hover, #actionButton:hover {{
                    border-color: {self.accent_color};
                    background-color: #f3f2f1;
                }}
                
                #systemInfo, #networkStatus {{
                    background-color: #f3f2f1;
                    border: 1px solid #e1e5e9;
                    border-radius: 6px;
                    color: #323130;
                    padding: 15px;
                    font-family: 'Consolas', monospace;
                }}
                
                #toggleSwitch {{
                    padding: 5px;
                }}
                
                #statusBar {{
                    background-color: {self.accent_color};
                    color: #ffffff;
                    border: none;
                    font-weight: 500;
                }}
            """)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Configurar fonte padrão
    font = QFont("Segoe UI", 9)
    app.setFont(font)
    
    window = WindowsSettingsApp()
    window.show()
    
    sys.exit(app.exec())