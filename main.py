#Este código es para pruebas, no tomar en cuenta

from encriptar import comprimir_mensaje
from desencriptar import leer_y_decomprimir

def menu():
    while True:
        print("\n===== MENÚ PRINCIPAL =====")
        print("1. Codificar mensaje y guardar como archivo .bin")
        print("2. Decodificar mensaje desde archivo .bin")
        print("3. Salir")
        opcion = input("Seleccione una opción (1-3): ")

        if opcion == "1":
            mensaje = input("Ingrese el mensaje a codificar: ")
            nombre_archivo = input("Nombre del archivo de salida (.bin): ")
            tabla, bits = comprimir_mensaje(mensaje, nombre_archivo)
            print("\nCodificación completada.")
            print("Tabla de códigos generada:")
            for char, codigo in tabla.items():
                print(f"{repr(char)}: {codigo}")
            print(f"Mensaje codificado en bits: {bits}")

        elif opcion == "2":
            nombre_archivo = input("Ingrese el nombre del archivo .bin a leer: ")
            try:
                mensaje = leer_y_decomprimir(nombre_archivo)
                print("\nMensaje decodificado correctamente:")
                print(mensaje)
            except FileNotFoundError:
                print("❌ Archivo no encontrado.")
            except Exception as e:
                print(f"⚠️ Error al decodificar: {e}")

        elif opcion == "3":
            print("Saliendo del programa.")
            break
        else:
            print("Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    menu()
