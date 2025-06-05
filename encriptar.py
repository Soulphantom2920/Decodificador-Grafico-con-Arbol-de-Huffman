from árbol_huffman import calcular_frecuencias, construir_arbol_huffman, generar_codigos

def codificar_mensaje(mensaje, tabla_codigos):
    bits = ""
    for c in mensaje:
        bits += tabla_codigos[c]
    return bits

def empaquetar_bits(bits):
    padding = (8 - len(bits) % 8) % 8
    bits += "0" * padding

    bytes_codificados = bytearray()
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        bytes_codificados.append(int(byte, 2))

    return bytes_codificados, padding

def guardar_binario(nombre_archivo, frecuencias, bytes_codificados, padding):
    with open(nombre_archivo, "wb") as f:
        cantidad_caracteres = len(frecuencias)
        f.write(cantidad_caracteres.to_bytes(4, byteorder='big'))  # 4 bytes

        for char, freq in frecuencias.items():
            f.write(char.encode('utf-8'))         # 1 byte
            f.write(freq.to_bytes(2, byteorder='big'))  # 2 bytes

        f.write(bytes([padding]))  # 1 byte

        f.write(bytes_codificados)

def comprimir_mensaje(mensaje, nombre_archivo_binario):
    frecuencias = calcular_frecuencias(mensaje)
    arbol = construir_arbol_huffman(frecuencias)
    tabla_codigos = generar_codigos(arbol)

    bits_codificados = codificar_mensaje(mensaje, tabla_codigos)
    bytes_codificados, padding = empaquetar_bits(bits_codificados)

    guardar_binario(nombre_archivo_binario, frecuencias, bytes_codificados, padding)

    return tabla_codigos, bits_codificados
