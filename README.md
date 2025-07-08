# Decodificador Gráfico con Árbol de Huffman

<p align="left">
  <img src="https://img.shields.io/badge/Lenguaje-Python-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Framework-PyQt6-orange?style=for-the-badge" alt="PyQt6">
  <img src="https://img.shields.io/badge/Algoritmo-Huffman%20Coding-red?style=for-the-badge" alt="Huffman Coding">
  <img src="https://img.shields.io/badge/Institución-TEC%20Costa%20Rica-darkgreen?style=for-the-badge" alt="TEC Costa Rica">
</p>

> Proyecto final para el curso **Taller de Programación** del **[Instituto Tecnológico de Costa Rica](https://www.tec.ac.cr/)**. [cite_start]Una herramienta educativa diseñada para visualizar el funcionamiento interno del algoritmo de decodificación de Huffman. [cite: 1, 2, 3, 4]

---

## 🎯 Sobre el Proyecto

[cite_start]Esta aplicación permite cifrar mensajes de texto en archivos binarios y, lo más importante, descifrarlos visualmente. [cite: 8] [cite_start]Al cargar un archivo `.bin`, el programa reconstruye el árbol de Huffman utilizado para la codificación y muestra una animación paso a paso de cómo se recorre para reconstruir el mensaje original. [cite: 8, 12]

### ✨ Características Principales

- [cite_start]**Cifrado de Mensajes:** Convierte un texto en un archivo `.bin` compacto usando el algoritmo de Huffman. [cite: 10]
- [cite_start]**Decodificación desde Archivo:** Lee un archivo `.bin` y reconstruye el mensaje original. [cite: 11]
- [cite_start]**Visualización del Árbol:** Dibuja dinámicamente el árbol de Huffman completo basado en las frecuencias de caracteres del archivo. [cite: 12]
- [cite_start]**Animación del Proceso:** Ilustra visualmente el recorrido del árbol bit a bit, mostrando el camino tomado para encontrar cada carácter. [cite: 12]
- **Interfaz Gráfica Intuitiva:** Desarrollado con **PyQt6** para una experiencia de usuario clara y funcional.

### 🎨 La Visualización Animada

La característica central de este proyecto es la animación del proceso de decodificación. Para facilitar la comprensión, se utiliza un código de colores intuitivo para los nodos del árbol:

- 🟡 **Amarillo:** Nodo que acaba de ser visitado en el paso anterior.
- 🟢 **Verde:** Nodo actual donde se encuentra el proceso.
- 🟠 **Naranja:** Nodos hoja, que contienen los caracteres decodificados.
- ⚪ **Gris:** Nodos internos que aún no han sido recorridos.
- 🔵 **Rama "0" (Azul):** Indica que se ha leído un bit `0` y se ha tomado el camino izquierdo.
- 🔴 **Rama "1" (Rojo):** Indica que se ha leído un bit `1` y se ha tomado el camino derecho.

---

## 📂 Estructura del Archivo .bin
El archivo binario generado por el programa sigue una estructura específica para permitir la reconstrucción del árbol y del mensaje:

Cantidad de Caracteres (4 bytes): Un entero que indica cuántos caracteres únicos hay en la tabla de frecuencias.

Tabla de Frecuencias (Variable): Una secuencia de 1 byte para el carácter (ASCII) seguido de 2 bytes para su frecuencia.

Bits de Relleno (1 byte): Un entero que indica cuántos bits se añadieron al final del último byte para completar los 8 bits (padding).

Mensaje Codificado (Resto del archivo): La secuencia de bits que representa el mensaje cifrado.

---

## 🛠️ Instalación y Uso

Para ejecutar este proyecto, sigue estos pasos:

**1. Clona el Repositorio**:
```bash
git clone [https://github.com/TuUsuario/NombreDelRepo.git](https://github.com/TuUsuario/NombreDelRepo.git)
cd NombreDelRepo
```
**2. Instala las Dependencias**. El proyecto requiere PyQt6. Puedes instalarlo usando pip:
```Bash
pip install PyQt6
```
**3. Ejecuta la Aplicación**. Una vez instalada la dependencia, ejecuta el archivo principal:
```Bash
python main.py
```

---

<p align="center">
  <a href="https://www.paypal.me/SoulP2920" target="_blank">
    <img src="https://img.shields.io/badge/PayPal-Invítame%20a%20un%20café-blue?style=for-the-badge&logo=paypal" alt="Donar con PayPal">
  </a>
</p>

![Mi Firma de Zorro - 128p](https://raw.githubusercontent.com/Soulphantom2920/assets-/main/Fox%20signatures/GithubMark%20x128p.gif)


¡Muchas Gracias! 🙌
