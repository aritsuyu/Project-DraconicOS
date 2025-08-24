#!/usr/bin/env python3
"""
Gaming Control Panel - Arquivo Principal
Ponto de entrada da aplicação
"""

import sys
import logging
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont

from ui.main_interface import MainInterface

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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