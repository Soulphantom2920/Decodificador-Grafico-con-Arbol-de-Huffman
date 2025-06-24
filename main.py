import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QPushButton, QLabel, QLineEdit, QFileDialog, 
                            QMessageBox, QStackedWidget, QSizePolicy, QHBoxLayout,
                            QProgressBar, QSlider)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QFont, QPainter, QPen, QBrush, QColor, QPainterPath
from encriptar import comprimir_mensaje
from desencriptar import leer_cabecera, convertir_a_bits, decodificar_mensaje
from árbol_huffman import construir_arbol_huffman

class TreeVisualizationWidget(QWidget):
    """
    Widget personalizado para visualizar el árbol binario de Huffman con animación
    Muestra el proceso de decodificación paso a paso
    - 🟡 Amarillo: Nodo visitado (el nodo que se acaba de recorrer)
    - 🟢 Verde: Nodo actual (el nodo donde se encuentra actualmente el proceso de decodificación)
    - 🟠 Naranja: Hojas (nodos que contienen caracteres del mensaje original)
    - ⚪ Gris: Nodos normales (nodos internos que no han sido visitados)
    - 🔵 Azul "0": Rama izquierda (cuando el bit es 0)
    - 🔴 Rojo "1": Rama derecha (cuando el bit es 1)
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        # Estado del árbol y animación
        self.arbol = None
        self.bits = ""
        self.nodo_actual = None
        self.nodo_visitado = None
        self.mensaje_reconstruido = ""
        self.indice_bit_actual = 0
        self.animacion_activa = False
        
        # Timer para controlar la velocidad de animación
        self.timer = QTimer()
        self.timer.timeout.connect(self.siguiente_paso)
        self.velocidad_animacion = 800  # ms entre cada paso
        
        # Esquema de colores para diferenciar estados de los nodos
        self.color_nodo_normal = QColor(200, 200, 200)    # Gris: nodos no visitados
        self.color_nodo_visitado = QColor(255, 255, 0)    # Amarillo: nodo recién visitado
        self.color_nodo_actual = QColor(0, 255, 0)        # Verde: nodo actual en proceso
        self.color_hoja = QColor(255, 165, 0)             # Naranja: hojas con caracteres
        self.color_texto = QColor(0, 0, 0)
        self.color_linea = QColor(100, 100, 100)
        
        self.setMinimumSize(800, 600)
        self.setStyleSheet("background-color: white; border: 1px solid #ccc;")

    def cargar_arbol(self, archivo):
        """
        Carga un archivo .bin y construye el árbol de Huffman para visualización
        Retorna True si se cargó exitosamente, False en caso contrario
        """
        try:
            # Extraer datos del archivo comprimido
            frecuencias, cuerpo_codificado, padding = leer_cabecera(archivo)
            self.arbol = construir_arbol_huffman(frecuencias)
            self.bits = convertir_a_bits(cuerpo_codificado, padding)
            
            # Reiniciar estado de animación
            self.nodo_actual = self.arbol
            self.nodo_visitado = None
            self.mensaje_reconstruido = ""
            self.indice_bit_actual = 0
            self.animacion_activa = False
            self.timer.stop()
            self.update()
            return True
        except Exception as e:
            print(f"Error al cargar el árbol: {e}")
            return False

    def iniciar_animacion(self):
        """Inicia la animación automática de decodificación"""
        if self.arbol and self.bits:
            self.animacion_activa = True
            self.timer.start(self.velocidad_animacion)

    def siguiente_paso(self):
        """
        Procesa el siguiente bit en la secuencia de decodificación
        Actualiza el estado visual del árbol y reconstruye el mensaje
        """
        if self.indice_bit_actual >= len(self.bits):
            self.animacion_activa = False
            self.timer.stop()
            return

        bit = self.bits[self.indice_bit_actual]
        self.nodo_visitado = self.nodo_actual
        
        # Navegar por el árbol según el bit actual
        if bit == "0":
            self.nodo_actual = self.nodo_actual.left
        else:
            self.nodo_actual = self.nodo_actual.right

        # Si llegamos a una hoja, extraer el carácter y volver a la raíz
        if self.nodo_actual.left is None and self.nodo_actual.right is None:
            self.mensaje_reconstruido += self.nodo_actual.char
            self.nodo_actual = self.arbol  # Volver a la raíz para el siguiente carácter

        self.indice_bit_actual += 1
        self.update()

    def paintEvent(self, event):
        """
        Evento de pintura: dibuja el árbol binario completo
        Muestra mensaje de instrucción si no hay árbol cargado
        """
        if not self.arbol:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setPen(QPen(QColor(100, 100, 100), 2))
            painter.setFont(QFont("Arial", 16))
            
            rect = self.rect()
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, 
                           "Seleccione un archivo .bin para visualizar el árbol")
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Dibujar el árbol centrado con espaciado compacto
        self.dibujar_nodo(painter, self.arbol, self.width() // 2, 80, self.width() // 4, 100)

    def dibujar_nodo(self, painter, nodo, x, y, ancho_rama, separacion_y):
        """
        Dibuja recursivamente un nodo y sus hijos
        Aplica colores según el estado del nodo en la animación
        """
        if not nodo:
            return

        # Determinar color del nodo según su estado en la animación
        color_nodo = self.color_nodo_normal
        if nodo == self.nodo_visitado:
            color_nodo = self.color_nodo_visitado
        elif nodo == self.nodo_actual:
            color_nodo = self.color_nodo_actual
        elif nodo.char is not None:  # Es una hoja
            color_nodo = self.color_hoja

        # Dibujar círculo del nodo
        radio = 30
        painter.setBrush(QBrush(color_nodo))
        
        # Borde más grueso para resaltar el nodo actual
        if nodo == self.nodo_actual:
            painter.setPen(QPen(QColor(0, 0, 0), 5))
        else:
            painter.setPen(QPen(self.color_texto, 3))
            
        painter.drawEllipse(int(x - radio), int(y - radio), radio * 2, radio * 2)

        # Texto del nodo: carácter si es hoja, frecuencia si es nodo interno
        painter.setPen(self.color_texto)
        if nodo.char is not None:
            texto = f"'{nodo.char}'"
        else:
            texto = str(nodo.freq)
        
        font = painter.font()
        font.setPointSize(11)
        font.setBold(True)
        painter.setFont(font)
        
        # Centrar texto en el nodo
        rect_texto = painter.fontMetrics().boundingRect(texto)
        painter.drawText(int(x - rect_texto.width() // 2), 
                        int(y + rect_texto.height() // 2), texto)

        # Dibujar ramas y nodos hijos recursivamente
        if nodo.left:
            x_izq = int(x - ancho_rama)
            y_izq = int(y + separacion_y)
            
            # Línea hacia hijo izquierdo
            painter.setPen(QPen(self.color_linea, 3))
            painter.drawLine(int(x), int(y + radio), x_izq, int(y_izq - 30))
            
            # Etiqueta "0" para rama izquierda
            painter.setPen(QColor(0, 0, 255))
            font.setPointSize(10)
            font.setBold(True)
            painter.setFont(font)
            painter.drawText(int(x - ancho_rama // 2 - 10), int(y + separacion_y // 2), "0")
            
            # Llamada recursiva para hijo izquierdo
            self.dibujar_nodo(painter, nodo.left, x_izq, y_izq, int(ancho_rama // 2.0), separacion_y)

        if nodo.right:
            x_der = int(x + ancho_rama)
            y_der = int(y + separacion_y)
            
            # Línea hacia hijo derecho
            painter.setPen(QPen(self.color_linea, 3))
            painter.drawLine(int(x), int(y + radio), x_der, int(y_der - 30))
            
            # Etiqueta "1" para rama derecha
            painter.setPen(QColor(255, 0, 0))
            font.setPointSize(10)
            font.setBold(True)
            painter.setFont(font)
            painter.drawText(int(x + ancho_rama // 2 + 10), int(y + separacion_y // 2), "1")
            
            # Llamada recursiva para hijo derecho
            self.dibujar_nodo(painter, nodo.right, x_der, y_der, int(ancho_rama // 2.0), separacion_y)

    def get_mensaje_reconstruido(self):
        """Retorna el mensaje reconstruido hasta el momento actual"""
        return self.mensaje_reconstruido

    def get_progreso(self):
        """Calcula el porcentaje de progreso de la decodificación"""
        if not self.bits:
            return 0
        return (self.indice_bit_actual / len(self.bits)) * 100

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
        """
        Configura la pantalla de decodificación con visualización del árbol
        Interfaz simplificada: solo botón de selección, árbol y mensaje
        """
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)
        
        # Título
        titulo = QLabel("Descifrar Mensaje")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setFont(QFont(self.TITULO_FUENTE, self.TITULO_TAMANO, QFont.Weight.Bold))
        layout.addWidget(titulo)
        
        # Botón para seleccionar archivo
        btn_seleccionar = self.crear_boton("Seleccionar archivo a descifrar")
        btn_seleccionar.clicked.connect(self.seleccionar_archivo_abrir)
        layout.addWidget(btn_seleccionar)
        
        # Widget de visualización del árbol
        self.tree_widget = TreeVisualizationWidget()
        layout.addWidget(self.tree_widget)
        
        # Mensaje reconstruido
        self.label_mensaje = QLabel("")
        self.label_mensaje.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_mensaje.setWordWrap(True)
        self.label_mensaje.setStyleSheet("font-size: 18px; padding: 15px; background-color: #e8f4f8; border: 2px solid #4CAF50; border-radius: 8px; min-height: 60px;")
        layout.addWidget(self.label_mensaje)
        
        # Botón volver
        btn_volver = self.crear_boton("Volver al menú")
        btn_volver.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(btn_volver)
        
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
        """
        Maneja la selección de archivo .bin para decodificación
        Carga el árbol automáticamente e inicia la animación
        """
        archivo, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo",
            "",
            "Archivos binarios (*.bin);;Todos los archivos (*.*)"
        )
        if archivo:
            try:
                # Cargar el árbol en el widget de visualización
                if self.tree_widget.cargar_arbol(archivo):
                    # Iniciar animación automáticamente
                    self.tree_widget.iniciar_animacion()
                    
                    # Mostrar mensaje inicial
                    self.label_mensaje.setText("Iniciando decodificación...")
                    
                    # Timer para actualizar el mensaje reconstruido
                    self.timer_mensaje = QTimer()
                    self.timer_mensaje.timeout.connect(self.actualizar_mensaje)
                    self.timer_mensaje.start(100)
                    
                else:
                    QMessageBox.critical(self, "Error", "No se pudo cargar el archivo")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error: {str(e)}")

    def actualizar_mensaje(self):
        """
        Actualiza el mensaje reconstruido en tiempo real
        Se ejecuta cada 100ms durante la animación
        """
        mensaje_actual = self.tree_widget.get_mensaje_reconstruido()
        if mensaje_actual:
            self.label_mensaje.setText(f"Mensaje descifrado:\n{mensaje_actual}")
        else:
            self.label_mensaje.setText("Decodificando...")
        
        # Detener timer cuando se complete la decodificación
        if self.tree_widget.get_progreso() >= 100:
            self.timer_mensaje.stop()

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