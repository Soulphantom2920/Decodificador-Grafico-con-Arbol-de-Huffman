import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QPushButton, QLabel, QLineEdit, QFileDialog, 
                            QMessageBox, QStackedWidget, QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from encriptar import comprimir_mensaje
from desencriptar import leer_y_decomprimir

class MainWindow(QMainWindow):
    #Configuración de la ventana
    VENTANA_ANCHO = 0.8  #80% del ancho de la pantalla
    VENTANA_ALTO = 0.8   #80% del alto de la pantalla
    
    #Configuración del título
    TITULO_FUENTE = "Arial"
    TITULO_TAMANO = 45
    TITULO_ALTURA = 140
    TITULO_PADDING = 20
    TITULO_COLOR = "#333"
    
    #Configuración de botones
    BOTON_ALTURA = 40
    BOTON_FUENTE = 20
    BOTON_COLOR = "#6495ED"
    BOTON_COLOR_HOVER = "#4169E1"
    
    #Configuración de campos de texto
    CAMPO_ALTURA = 30
    CAMPO_FUENTE = 14

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Decodificador Gráfico de Mensajes")
        self.configurar_ventana()
        self.configurar_estilos()
        self.setup_ui()

    def configurar_ventana(self):
        screen = QApplication.primaryScreen().geometry()
        self.resize(
            int(screen.width() * self.VENTANA_ANCHO),
            int(screen.height() * self.VENTANA_ALTO)
        )
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout_principal = QVBoxLayout(central_widget)
        self.layout_principal.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_principal.setSpacing(20)
        
        self.stacked_widget = QStackedWidget()
        self.layout_principal.addWidget(self.stacked_widget)

    def configurar_estilos(self):
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: #f0f0f0;
            }}
            QPushButton {{
                background-color: {self.BOTON_COLOR};
                color: white;
                border: black;
                padding: 10px;
                border-radius: 5px;
                font-size: {self.BOTON_FUENTE}px;
                min-height: {self.BOTON_ALTURA}px;
            }}
            QPushButton:hover {{
                background-color: {self.BOTON_COLOR_HOVER};
            }}
            QLineEdit {{
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: {self.CAMPO_FUENTE}px;
                min-height: {self.CAMPO_ALTURA}px;
            }}
            QLabel {{
                font-size: 50px;
                color: {self.TITULO_COLOR};
            }}
            QMessageBox {{
                font-size: 20px;
                color: white;
            }}
            QMessageBox QLabel {{
                font-size: 20px;
                qproperty-alignment: AlignLeft;
                color: white;
            }}
        """)

    def setup_ui(self):
        self.setup_menu_principal()
        self.setup_pantalla_codificar()
        self.setup_pantalla_decodificar()
        self.stacked_widget.setCurrentIndex(0)

    def crear_boton(self, texto, altura=None):
        boton = QPushButton(texto)
        boton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        boton.setMinimumHeight(altura or self.BOTON_ALTURA)
        return boton

    def setup_menu_principal(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 50, 20, 20)
        
        #Título
        titulo = QLabel("Decodificador Gráfico de Mensajes")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setFont(QFont(self.TITULO_FUENTE, self.TITULO_TAMANO, QFont.Weight.Bold))
        titulo.setMinimumHeight(self.TITULO_ALTURA)
        titulo.setStyleSheet(f"padding: {self.TITULO_PADDING}px;")
        layout.addWidget(titulo)
        
        #Botones
        botones_container = QWidget()
        botones_layout = QVBoxLayout(botones_container)
        botones_layout.setSpacing(20)
        
        btn_codificar = self.crear_boton("Cifrar mensaje")
        btn_decodificar = self.crear_boton("Descifrar mensaje")
        btn_salir = self.crear_boton("Salir")
        
        for btn in [btn_codificar, btn_decodificar, btn_salir]:
            botones_layout.addWidget(btn)
        
        btn_codificar.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        btn_decodificar.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        btn_salir.clicked.connect(self.close)
        
        layout.addWidget(botones_container)
        self.stacked_widget.addWidget(widget)

    def setup_pantalla_codificar(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)
        
        #Título
        titulo = QLabel("Cifrar Mensaje")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setFont(QFont(self.TITULO_FUENTE, self.TITULO_TAMANO, QFont.Weight.Bold))
        layout.addWidget(titulo)
        
        #Elementos
        elementos_container = QWidget()
        elementos_layout = QVBoxLayout(elementos_container)
        elementos_layout.setSpacing(20)
        
        self.campo_mensaje = QLineEdit()
        self.campo_mensaje.setPlaceholderText("Ingrese el mensaje a cifrar...")
        self.campo_mensaje.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        elementos_layout.addWidget(self.campo_mensaje)
        
        btn_seleccionar = self.crear_boton("Seleccionar archivo de salida")
        btn_seleccionar.clicked.connect(self.seleccionar_archivo_guardar)
        elementos_layout.addWidget(btn_seleccionar)
        
        self.label_archivo = QLabel("")
        self.label_archivo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_archivo.setWordWrap(True)
        self.label_archivo.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.label_archivo.setStyleSheet("font-size: 16px;")
        elementos_layout.addWidget(self.label_archivo)
        
        btn_codificar = self.crear_boton("Cifrar")
        btn_volver = self.crear_boton("Volver al menú")
        
        elementos_layout.addWidget(btn_codificar)
        elementos_layout.addWidget(btn_volver)
        
        btn_codificar.clicked.connect(self.codificar_mensaje)
        btn_volver.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        
        layout.addWidget(elementos_container)
        self.stacked_widget.addWidget(widget)

    def setup_pantalla_decodificar(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)
        
        #Título
        titulo = QLabel("Descifrar Mensaje")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setFont(QFont(self.TITULO_FUENTE, self.TITULO_TAMANO, QFont.Weight.Bold))
        layout.addWidget(titulo)
        
        #Elementos
        elementos_container = QWidget()
        elementos_layout = QVBoxLayout(elementos_container)
        elementos_layout.setSpacing(20)
        
        btn_seleccionar = self.crear_boton("Seleccionar archivo a descifrar")
        btn_seleccionar.clicked.connect(self.seleccionar_archivo_abrir)
        elementos_layout.addWidget(btn_seleccionar)
        
        self.label_mensaje = QLabel("")
        self.label_mensaje.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_mensaje.setWordWrap(True)
        self.label_mensaje.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.label_mensaje.setStyleSheet("font-size: 18px;")
        elementos_layout.addWidget(self.label_mensaje)
        
        btn_volver = self.crear_boton("Volver al menú")
        btn_volver.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        elementos_layout.addWidget(btn_volver)
        
        layout.addWidget(elementos_container)
        self.stacked_widget.addWidget(widget)

    def seleccionar_archivo_guardar(self):
        archivo, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar archivo como",
            "",
            "Archivos binarios (*.bin);;Todos los archivos (*.*)"
        )
        if archivo:
            if not archivo.endswith(".bin"):
                archivo += ".bin"
            self.label_archivo.setText(f"Archivo seleccionado: {archivo}")
            self.archivo_actual = archivo

    def seleccionar_archivo_abrir(self):
        archivo, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo",
            "",
            "Archivos binarios (*.bin);;Todos los archivos (*.*)"
        )
        if archivo:
            try:
                mensaje = leer_y_decomprimir(archivo)
                self.label_mensaje.setText(f"Mensaje descifrado:\n{mensaje}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error: {str(e)}")

    def codificar_mensaje(self):
        if not hasattr(self, "archivo_actual"):
            QMessageBox.warning(self, "Advertencia", "Seleccione un archivo de salida")
            return
            
        mensaje = self.campo_mensaje.text()
        if not mensaje:
            QMessageBox.warning(self, "Advertencia", "Ingrese un mensaje")
            return
            
        try:
            tabla, bits = comprimir_mensaje(mensaje, self.archivo_actual)
            QMessageBox.information(self, "Éxito", "Mensaje cifrado")
            self.campo_mensaje.clear()
            self.label_archivo.clear()
            delattr(self, "archivo_actual")
            self.stacked_widget.setCurrentIndex(0)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error: {str(e)}")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()