import json
import os
from datetime import datetime

ruta = os.path.dirname(os.path.abspath(__file__))

file = "registros.json"
color_rosa = "\033[95m"
reset_color = "\033[0m"

FICHERO = f"{ruta}/{file}" 

id = 1

# ---------------------- Cargar/Guardar ----------------------
def cargar_datos():
    """Carga los registros desde el fichero JSON o devuelve una lista vacía si no existe."""
    if not os.path.exists(FICHERO):
        return []
    with open(FICHERO, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def guardar_datos(datos):
    """Guarda la lista de registros en el fichero JSON."""
    with open(FICHERO, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

# ---------------------- Validaciones ----------------------

def validar_nombre(nombre:str)-> bool:
    if len(nombre) <= 20:
        return True
    
    return False

def esta_vacio(dato)->bool:
    if len(dato) != 0:
        return False
    return True

# ---------------------- CRUD ----------------------
def crear_registro():
    datos = cargar_datos()
    
    while True:
        nombre = input("Introduce el nombre del can: ")
        if esta_vacio(nombre):
            print('El peludo tiene que tener un nombre...')
        elif not validar_nombre(nombre):
            print('El nombre tiene que tener como máximo 20 caracteres...')
        else:
            break

    while True:
        raza = input('Introduce la raza del chucho: ')
        if esta_vacio(raza):
            print('El pulgoso tiene que tener una raza...')
        else:
            break

    registro = {
        "ID": len(datos) + 1,
        "Nombre": nombre,
        "Raza": raza
    }

    datos.append(registro)
    guardar_datos(datos)
    print("Registro creado con éxito.")

def leer_registro():
    registros = []
    datos = cargar_datos()
    if not datos:
        print("No hay registros.")
        return

    opcion = ""
    while opcion not in ["a", "1"]:
        opcion = input(f"¿Quieres ver [{color_rosa}A{reset_color}]ll (todos) o [{color_rosa}1{reset_color}] (un registro por ID)? ").strip().lower()

    if opcion == "a":
        for reg in datos:
            registros.append(reg)
    elif opcion == "1":
        try:
            idx = int(input(f"Introduce el {color_rosa}ID{reset_color} (posición del registro): ")) - 1
            if 0 <= idx < len(datos):
                registros.append(datos[idx])
        except ValueError:
            print("ID inválido.")
            
    return registros
# ---------------------- Menú ----------------------
# def menu():
#     while True:
#         print('''
#         --- Gestión de Alumnos DAM ---
#             1. Crear registro
#             2. Leer registro(s)
#             0. Salir
#         ''')

#         opcion = input("Selecciona una opción: ")

#         if opcion == "1":
#             crear_registro()
#         elif opcion == "2":
#             leer_registro()
#         elif opcion == "0":
#             break
#         else:
#             print("Opción inválida.")

# ---------------------- Main ----------------------
# if __name__ == "__main__":
#     menu()
