"""
Widget Extras
Widget específico para a seção Extras com ferramentas de processamento de imagem
"""

import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QSlider, QColorDialog, QFileDialog, 
                             QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPixmap


class ExtrasWidget(QWidget):
    """Widget específico para a seção Extras"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_image_path = None
        self.selected_color = (255, 255, 255)  # Cor padrão branca
        self.tolerance = 30  # Tolerância padrão
        self.setupUI()

    def setupUI(self):
        """Configura a interface da seção Extras"""
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)

        # Lado esquerdo - Controles
        left_layout = QVBoxLayout()
        left_layout.setSpacing(20)

        # Título
        title_label = QLabel("Icon Processing Tools")
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 28px;
                font-weight: bold;
                background: transparent;
                border: none;
            }
        """)
        left_layout.addWidget(title_label)

        # Descrição
        description_label = QLabel("Select an image and choose processing options:")
        description_label.setStyleSheet("""
            QLabel {
                color: #cccccc;
                font-size: 16px;
                background: transparent;
                border: none;
                margin-bottom: 20px;
            }
        """)
        left_layout.addWidget(description_label)

        # Label do arquivo selecionado
        self.file_label = QLabel("No image selected")
        self.file_label.setStyleSheet("""
            QLabel {
                color: #888888;
                font-size: 14px;
                background: transparent;
                border: none;
                font-style: italic;
                margin: 10px 0;
            }
        """)
        left_layout.addWidget(self.file_label)

        # Seção de controles de cor
        color_section = QWidget()
        color_layout = QVBoxLayout(color_section)
        color_layout.setContentsMargins(0, 10, 0, 10)
        color_layout.setSpacing(15)

        # Seletor de cor
        color_container = QHBoxLayout()
        color_label = QLabel("Tint Color:")
        color_label.setStyleSheet("color: white; font-size: 14px; font-weight: 500;")
        
        self.color_button = QPushButton()
        self.color_button.setFixedSize(60, 30)
        self.update_color_button()
        self.color_button.clicked.connect(self.select_color)
        
        color_container.addWidget(color_label)
        color_container.addWidget(self.color_button)
        color_container.addStretch()
        color_layout.addLayout(color_container)

        # Slider de tolerância
        tolerance_container = QVBoxLayout()
        tolerance_label = QLabel("Transparency Tolerance:")
        tolerance_label.setStyleSheet("color: white; font-size: 14px; font-weight: 500;")
        
        self.tolerance_slider = QSlider(Qt.Orientation.Horizontal)
        self.tolerance_slider.setMinimum(0)
        self.tolerance_slider.setMaximum(100)
        self.tolerance_slider.setValue(30)
        self.tolerance_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #666666;
                height: 6px;
                background: #333333;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #4a90e2;
                border: 1px solid #357abd;
                width: 16px;
                height: 16px;
                border-radius: 8px;
                margin: -5px 0;
            }
            QSlider::handle:horizontal:hover {
                background: #5ba0f2;
            }
        """)
        
        self.tolerance_value_label = QLabel("30")
        self.tolerance_value_label.setStyleSheet("color: #4a90e2; font-size: 12px; font-weight: bold;")
        self.tolerance_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.tolerance_slider.valueChanged.connect(self.update_tolerance)
        
        tolerance_container.addWidget(tolerance_label)
        tolerance_container.addWidget(self.tolerance_slider)
        tolerance_container.addWidget(self.tolerance_value_label)
        color_layout.addLayout(tolerance_container)

        left_layout.addWidget(color_section)

        # Botões de ação
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(15)

        self.transparent_btn = QPushButton("Make Background Transparent")
        self.tinter_btn = QPushButton("Apply Color Tint")

        for btn in [self.transparent_btn, self.tinter_btn]:
            btn.setFixedHeight(50)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #4a4a4a;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-size: 14px;
                    font-weight: 500;
                    padding: 10px 20px;
                }
                QPushButton:hover {
                    background-color: #4a90e2;
                }
                QPushButton:pressed {
                    background-color: #357abd;
                }
                QPushButton:disabled {
                    background-color: #333333;
                    color: #666666;
                }
            """)
            btn.setEnabled(False)  # Inicialmente desabilitados
            buttons_layout.addWidget(btn)

        left_layout.addLayout(buttons_layout)
        left_layout.addStretch()

        # Lado direito - Área de imagem
        right_layout = QVBoxLayout()
        
        # Área clicável para selecionar imagem
        self.image_area = QLabel()
        self.image_area.setFixedSize(400, 300)
        self.image_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_area.setStyleSheet("""
            QLabel {
                background-color: #3a3a3a;
                border: 2px dashed #666666;
                border-radius: 12px;
                color: #888888;
                font-size: 16px;
                font-weight: 500;
            }
            QLabel:hover {
                border-color: #4a90e2;
                background-color: #404040;
                color: #aaaaaa;
            }
        """)
        self.image_area.setText("Click here to select an image\n\n📸")
        self.image_area.setCursor(Qt.CursorShape.PointingHandCursor)
        self.image_area.mousePressEvent = self.select_image

        # Informações sobre os arquivos de saída
        output_info = QLabel("Output files will be saved as:\n• output.png (transparent background)\n• icon_tinted.png (color tinted)")
        output_info.setStyleSheet("""
            QLabel {
                color: #888888;
                font-size: 12px;
                background: transparent;
                border: none;
                margin-top: 10px;
            }
        """)
        output_info.setAlignment(Qt.AlignmentFlag.AlignCenter)

        right_layout.addWidget(self.image_area)
        right_layout.addWidget(output_info)
        right_layout.addStretch()

        # Adicionar layouts ao layout principal
        main_layout.addLayout(left_layout, stretch=1)
        main_layout.addLayout(right_layout, stretch=1)

        # Conectar sinais dos botões
        self.transparent_btn.clicked.connect(self.make_background_transparent)
        self.tinter_btn.clicked.connect(self.apply_color_tint)

    def update_color_button(self):
        """Atualiza a cor do botão de seleção de cor"""
        r, g, b = self.selected_color
        self.color_button.setStyleSheet(f"""
            QPushButton {{
                background-color: rgb({r}, {g}, {b});
                border: 2px solid #666666;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                border-color: #4a90e2;
            }}
        """)

    def select_color(self):
        """Abre diálogo para selecionar cor"""
        color = QColorDialog.getColor(QColor(*self.selected_color), self)
        if color.isValid():
            self.selected_color = (color.red(), color.green(), color.blue())
            self.update_color_button()

    def update_tolerance(self, value):
        """Atualiza o valor da tolerância"""
        self.tolerance = value
        self.tolerance_value_label.setText(str(value))

    def select_image(self, event):
        """Abre diálogo para selecionar imagem"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            "",
            "Image files (*.png *.jpg *.jpeg *.gif *.bmp *.tiff);;All files (*.*)"
        )
        
        if file_path:
            self.selected_image_path = file_path
            self.update_image_display()
            self.update_file_label()
            self.enable_buttons()

    def update_image_display(self):
        """Atualiza a exibição da imagem selecionada"""
        if self.selected_image_path:
            try:
                pixmap = QPixmap(self.selected_image_path)
                if not pixmap.isNull():
                    # Redimensionar mantendo proporção
                    scaled_pixmap = pixmap.scaled(
                        self.image_area.size(), 
                        Qt.AspectRatioMode.KeepAspectRatio, 
                        Qt.TransformationMode.SmoothTransformation
                    )
                    self.image_area.setPixmap(scaled_pixmap)
                    self.image_area.setStyleSheet("""
                        QLabel {
                            background-color: #3a3a3a;
                            border: 2px solid #4a90e2;
                            border-radius: 12px;
                        }
                        QLabel:hover {
                            border-color: #5ba0f2;
                            background-color: #404040;
                        }
                    """)
                else:
                    self.show_error("Error", "Could not load the selected image.")
            except Exception as e:
                self.show_error("Error", f"Error loading image: {str(e)}")

    def update_file_label(self):
        """Atualiza o label com o nome do arquivo"""
        if self.selected_image_path:
            filename = os.path.basename(self.selected_image_path)
            self.file_label.setText(f"Selected: {filename}")
            self.file_label.setStyleSheet("""
                QLabel {
                    color: #4a90e2;
                    font-size: 14px;
                    background: transparent;
                    border: none;
                    font-style: normal;
                    font-weight: 500;
                    margin: 10px 0;
                }
            """)

    def enable_buttons(self):
        """Habilita os botões após selecionar imagem"""
        self.transparent_btn.setEnabled(True)
        self.tinter_btn.setEnabled(True)

    def make_background_transparent(self):
        """Função integrada do icontransparent.py"""
        if not self.selected_image_path:
            self.show_error("Error", "Please select an image first.")
            return

        try:
            from PIL import Image
            
            # Carregar a imagem
            img = Image.open(self.selected_image_path).convert("RGBA")
            data = img.getdata()
            new_data = []

            # Processar cada pixel
            for item in data:
                r, g, b, a = item
                if r <= self.tolerance and g <= self.tolerance and b <= self.tolerance:
                    # Transformar em transparente
                    new_data.append((0, 0, 0, 0))
                else:
                    new_data.append(item)

            # Salvar resultado
            img.putdata(new_data)
            output_path = "output.png"
            img.save(output_path)
            
            self.show_success("Success", f"Background made transparent!\n\nSaved as: {output_path}\nTolerance used: {self.tolerance}")
            
        except Exception as e:
            self.show_error("Error", f"Error processing image: {str(e)}")

    def apply_color_tint(self):
        """Função integrada do icontinter.py"""
        if not self.selected_image_path:
            self.show_error("Error", "Please select an image first.")
            return

        try:
            from PIL import Image
            
            # Carregar a imagem
            img = Image.open(self.selected_image_path).convert("RGBA")
            pixels = img.getdata()

            # Aplicar nova cor mantendo transparência
            updated_pixels = [
                (self.selected_color[0], self.selected_color[1], self.selected_color[2], a) if a > 0 else (r, g, b, a)
                for r, g, b, a in pixels
            ]

            # Salvar resultado
            img.putdata(updated_pixels)
            output_path = "icon_tinted.png"
            img.save(output_path)
            
            r, g, b = self.selected_color
            self.show_success("Success", f"Color tint applied!\n\nSaved as: {output_path}\nColor used: RGB({r}, {g}, {b})")
            
        except Exception as e:
            self.show_error("Error", f"Error processing image: {str(e)}")

    def show_error(self, title, message):
        """Mostra mensagem de erro"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #2a2a2a;
                color: white;
            }
            QMessageBox QPushButton {
                background-color: #4a4a4a;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
            }
            QMessageBox QPushButton:hover {
                background-color: #4a90e2;
            }
        """)
        msg_box.exec()

    def show_success(self, title, message):
        """Mostra mensagem de sucesso"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #2a2a2a;
                color: white;
            }
            QMessageBox QPushButton {
                background-color: #4a4a4a;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
            }
            QMessageBox QPushButton:hover {
                background-color: #4a90e2;
            }
        """)
        msg_box.exec()