"""
Manipulador de Imagens
Classe para gerenciar operações com imagens
"""

import logging
from PyQt6.QtGui import QColor, QPixmap, QPainter, QPainterPath
from PyQt6.QtCore import Qt
from PIL import Image

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
                pixmap.fill(QColor("#4a4a4a"))
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
            pixmap.fill(QColor("#4a4a4a"))
            return pixmap