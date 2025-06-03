class HuffmanNode:
    def __init__(self, char=None, freq=0):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

def calcular_frecuencias(mensaje):
    frecuencias = {}
    for c in mensaje:
        if c in frecuencias:
            frecuencias[c] += 1
        else:
            frecuencias[c] = 1
    return frecuencias

def construir_arbol_huffman(frecuencias):
    #Para lista de nodos
    nodos = [HuffmanNode(char, freq) for char, freq in frecuencias.items()]

    while len(nodos) > 1:
        # Ordenar nodos por frecuencia ascendente
        nodos.sort(key=lambda n: n.freq)

        # Tomar los dos de menor frecuencia
        izquierdo = nodos.pop(0)
        derecho = nodos.pop(0)

        # Crear nodo padre
        padre = HuffmanNode(None, izquierdo.freq + derecho.freq)
        padre.left = izquierdo
        padre.right = derecho

        # Insertar nuevamente
        nodos.append(padre)

    return nodos[0] if nodos else None

def generar_codigos(nodo, codigo_actual="", tabla=None):
    if tabla is None:
        tabla = {}

    if nodo:
        if nodo.char is not None:
            tabla[nodo.char] = codigo_actual
        else:
            generar_codigos(nodo.left, codigo_actual + "0", tabla)
            generar_codigos(nodo.right, codigo_actual + "1", tabla)

    return tabla


