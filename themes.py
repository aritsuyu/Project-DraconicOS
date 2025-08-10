def set_theme(self, dark: bool):
    self.dark_mode = dark
    self.setup_styles()
    self.statusBar().showMessage(f"Tema: {'Escuro' if dark else 'Claro'} | Windows 11")

def auto_theme(self):
    self.dark_mode = self.detect_windows_theme()
    self.setup_styles()
    self.statusBar().showMessage(f"Tema: Automático ({'Escuro' if self.dark_mode else 'Claro'}) | Windows 11")

def set_accent_color(self, color: str):
    self.accent_color = color
    self.setup_styles()

def setup_styles(self):
    dark_style = f"""
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
    """

    light_style = f"""
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
            background-color: #e1e5e9;
            color: #323130;
        }}
        #menuButton[active="true"] {{
            background-color: {self.accent_color};
            color: #ffffff;
        }}
        #menuDescription {{
            color: #a19f9d;
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
            background-color: #ffffff;
            color: #323130;
            font-size: 14px;
        }}
        #searchBar:focus {{
            border-color: {self.accent_color};
            background-color: #f9f9f9;
        }}
        #infoCard {{
            background-color: #f9f9f9;
            border-radius: 8px;
            border: 1px solid #e1e5e9;
        }}
        #infoCard:hover {{
            border-color: {self.accent_color};
            background-color: #f0f0f0;
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
            background-color: #f0f0f0;
        }}
        #systemInfo, #networkStatus {{
            background-color: #f9f9f9;
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
    """

    style = dark_style if self.dark_mode else light_style
    self.setStyleSheet(style)
