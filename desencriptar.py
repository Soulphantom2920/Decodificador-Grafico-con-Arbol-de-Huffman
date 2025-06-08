from árbol_huffman import HuffmanNode, construir_arbol_huffman

def leer_cabecera(nombre_archivo):
    with open(nombre_archivo, "rb") as f:
        datos = f.read()

    puntero = 0

    #Leer los primeros 4 bytes: cantidad de caracteres únicos
    cantidad = int.from_bytes(datos[puntero:puntero+4], byteorder="big")
    puntero += 4

    frecuencias = {}
    for _ in range(cantidad):
        char = chr(datos[puntero])
        puntero += 1
        freq = int.from_bytes(datos[puntero:puntero+2], byteorder="big")
        puntero += 2
        frecuencias[char] = freq

    #Leer el byte de padding
    padding = datos[puntero]
    puntero += 1

    #Leer el cuerpo codificado
    cuerpo_codificado = datos[puntero:]

    return frecuencias, cuerpo_codificado, padding

def convertir_a_bits(cuerpo_codificado, padding):
    bits = ""
    for byte in cuerpo_codificado:
        bits += f'{byte:08b}'
    if padding > 0:
        bits = bits[:-padding]
    return bits

def decodificar_mensaje(bits, arbol):
    mensaje = ""
    nodo_actual = arbol
    for bit in bits:
        if bit == "0":
            nodo_actual = nodo_actual.left
        else:
            nodo_actual = nodo_actual.right

        if nodo_actual.left is None and nodo_actual.right is None:
            mensaje += nodo_actual.char
            nodo_actual = arbol  # volver a la raíz

    return mensaje

def leer_y_decomprimir(nombre_archivo):
    frecuencias, cuerpo_codificado, padding = leer_cabecera(nombre_archivo)
    arbol = construir_arbol_huffman(frecuencias)
    bits = convertir_a_bits(cuerpo_codificado, padding)
    mensaje = decodificar_mensaje(bits, arbol)
    return mensaje

