import struct
import os

formato = "i20s30s"
tamaño_registro = struct.calcsize(formato)
archivo = "registros.bin"  # Nombre del archivo binario

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
                return {
                    "id": id,
                    "nombre": nombre.decode(errors="ignore").strip(),
                    "raza": raza.decode(errors="ignore").strip()
                }
    return None