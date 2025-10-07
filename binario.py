import struct
import os

formato = "i20s30s"
tamaño_registro = struct.calcsize(formato)
archivo = "registros.bin"  

def leer_todos():
    """
    Lee todos los registros de perros del archivo binario y devuelve una lista de diccionarios.
    Cada diccionario contiene: id, nombre, raza.
    """
    registros = []
    if not os.path.exists(archivo):
        return registros

    with open(archivo, "rb") as f:
        while True:
            datos = f.read(tamaño_registro)
            if not datos:
                break
            id, nombre, raza = struct.unpack(formato, datos)
            if id != -1:
                registro = {
                    "id": id,
                    "nombre": nombre.decode(errors="ignore").strip(),
                    "raza": raza.decode(errors="ignore").strip()
                }
                registros.append(registro)
    return registros

def leer_por_id(buscar_id):
    """
    Devuelve un diccionario con los datos del perro cuyo ID coincide con buscar_id.
    Si no se encuentra, devuelve None.
    """
    if not os.path.exists(archivo):
        return None

    with open(archivo, "rb") as f:
        while True:
            datos = f.read(tamaño_registro)
            if not datos:
                break
            id, nombre, raza = struct.unpack(formato, datos)
            if id == buscar_id:
                return [{
                    "id": id,
                    "nombre": nombre.decode(errors="ignore").strip(),
                    "raza": raza.decode(errors="ignore").strip()
                }]
    return None

# Probar código

if __name__ == "__main__":
    while True:
        print("\n=== MENÚ DE LECTURA (PERRERA) ===")
        print("1. Mostrar todos los perros")
        print("2. Buscar perro por ID")
        print("0. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            perros = leer_todos()
            if not perros:
                print("No hay registros en el archivo.")
            else:
                print("\n=== LISTA DE PERROS ===")
                for p in perros:
                    print(f"ID: {p['id']}")
                    print(f"Nombre: {p['nombre']}")
                    print(f"Raza: {p['raza']}")
                    print("-" * 30)

        elif opcion == "2":
            try:
                buscar_id = int(input("Introduce el ID del perro: "))
                perro = leer_por_id(buscar_id)
                if perro:
                    print("\n=== RESULTADO ===")
                    print(f"ID: {perro['id']}")
                    print(f"Nombre: {perro['nombre']}")
                    print(f"Raza: {perro['raza']}")
                else:
                    print("No se encontró ningún perro con ese ID.")
            except ValueError:
                print("El ID debe ser un número entero.")

        elif opcion == "0":
            print("Saliendo...")
            break
        else:
            print("Opción no válida.")