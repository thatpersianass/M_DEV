import json, os, struct
import registros_json as rj
import binario as b
import textoplano_pro as tp

formato = "i20s30s"
tamaño_registro = struct.calcsize(formato)
color_rosa = "\033[95m"
reset_color = "\033[0m"

def obtener_archivo_actual():
    """
    Detecta automáticamente cuál es el archivo de trabajo actual.
    """
    posibles = ["registros.json", "registros.bin", "registros.txt"]
    for nombre in posibles:
        if os.path.exists(nombre):
            return nombre
        
    print("❌ No se encontró ningún archivo de registros.")
    return None

def tipo_archivo(nombre_archivo):
    """
    Devuelve el tipo de archivo según su extensión.
    Args:
        nombre_archivo (str): Nombre del archivo.
    """
    if not os.path.exists(nombre_archivo):
        return None
    _, extension = os.path.splitext(nombre_archivo)
    extension = extension.lower().replace(".", "")
    return extension if extension in ("json", "txt", "bin") else None

def eliminar_archivo(nombre):
    """
    Elimina un archivo si existe.
    Args:
        nombre (str): Nombre del archivo a eliminar.
    """
    if os.path.exists(nombre):
        os.remove(nombre)

def json_a_bin(archivo_json):
    """
    Convierte un archivo JSON a formato binario (.bin).
    Args:
        archivo_json (str): Nombre del archivo JSON de entrada.
    """
    if not os.path.exists(archivo_json):
        print("❌ No se encontró el archivo JSON.")
        return

    with open(archivo_json, "r", encoding="utf-8") as f_json:
        try:
            registros = json.load(f_json)
        except json.JSONDecodeError:
            print("❌ Error: el archivo JSON no tiene un formato válido.")
            return

    if not isinstance(registros, list):
        print("❌ El JSON debe contener una lista de objetos.")
        return

    with open("registros.bin", "wb") as f_bin:
        for perro in registros:
            try:
                id = int(perro.get("id") or perro.get("ID") or -1)
                nombre = str(perro.get("nombre") or perro.get("Nombre") or "")
                raza = str(perro.get("raza") or perro.get("Raza") or "")

                nombre_bytes = nombre.encode("utf-8")[:20].ljust(20, b" ")
                raza_bytes = raza.encode("utf-8")[:30].ljust(30, b" ")

                registro = struct.pack(formato, id, nombre_bytes, raza_bytes)
                f_bin.write(registro)
            except Exception as e:
                print(f"⚠️ Error al procesar registro {perro}: {e}")

    eliminar_archivo(archivo_json)

def json_a_txt(archivo_json):
    """
    Convierte un archivo JSON a formato de texto (.txt).
    Args:
        archivo_json (str): Nombre del archivo JSON de entrada.
    """
    try:
        with open(archivo_json, "r", encoding="utf-8") as f:
            datos = json.load(f)
        with open("registros.txt", "w", encoding="utf-8") as f_txt:
            for registro in datos:
                for clave, valor in registro.items():
                    f_txt.write(f"{clave}: {valor}\n")
                f_txt.write("\n")
        eliminar_archivo(archivo_json)
    except Exception as e:
        print(f"❌ Error al convertir JSON a TXT: {e}")

def bin_a_json():
    """
    Convierte el archivo binario de perros a un archivo JSON.
    """
    if not os.path.exists("registros.bin"):
        print("❌ No se encontró el archivo binario.")
        return

    registros = []

    with open("registros.bin", "rb") as f:
        while True:
            datos = f.read(tamaño_registro)
            if not datos:
                break

            id, nombre, raza = struct.unpack(formato, datos)
            if id != -1:
                registros.append({
                    "id": id,
                    "nombre": nombre.decode(errors="ignore").strip(),
                    "raza": raza.decode(errors="ignore").strip()
                })

    with open("registros.json", "w", encoding="utf-8") as f_json:
        json.dump(registros, f_json, ensure_ascii=False, indent=4)

    eliminar_archivo("registros.bin")

def bin_a_txt(archivo_bin):
    """
    Convierte un archivo BIN a formato TXT reutilizando bin_a_json().
    Args:
        archivo_bin (str): Nombre del archivo BIN de entrada.
    """
    #BIN → JSON
    bin_a_json()

    #JSON → TXT
    json_a_txt("registros.json")

def txt_a_json(archivo_txt, retornar_lista=False):
    """
    Convierte un archivo TXT estructurado a JSON.
    Args:
        archivo_txt (str): Nombre del archivo TXT de entrada.
        retornar_lista (bool): Si es True, retorna la lista de registros en lugar de escribir en un archivo.
    """
    registros = []
    try:
        with open(archivo_txt, "r", encoding="utf-8") as f:
            bloque = {}
            for linea in f:
                linea = linea.strip()
                if not linea:
                    if bloque:
                        registros.append(bloque)
                        bloque = {}
                else:
                    clave, valor = linea.split(": ", 1)
                    bloque[clave] = valor
            if bloque:
                registros.append(bloque)

        if retornar_lista:
            return registros

        with open("registros.json", "w", encoding="utf-8") as f_json:
            json.dump(registros, f_json, indent=4, ensure_ascii=False)

        eliminar_archivo(archivo_txt)

    except Exception as e:
        print(f"❌ Error al convertir TXT a JSON: {e}")
        return []

def txt_a_bin(archivo_txt):
    """
    Convierte un archivo TXT a BIN reutilizando txt_a_json() y json_a_bin().
    Args:
        archivo_txt (str): Nombre del archivo TXT de entrada.
    """
    try:
        #TXT → JSON
        txt_a_json(archivo_txt)

        #JSON → BIN
        json_a_bin("registros.json")

        eliminar_archivo(archivo_txt)

    except Exception as e:
        print(f"❌ Error al convertir TXT a BIN: {e}")

def mostrar_datos(registros):
    """
    Muestra los datos de los registros en un formato legible.
    Args:
        registros (list): Lista de diccionarios con los datos de los perros.
    """
    if not registros:
        print("No hay registros en el archivo con ese ID.")
        return

    ancho = 30
    print(f"{color_rosa}-" * ancho)
    print(f"\n{color_rosa}{'LISTA DE PERROS'.center(ancho)}{reset_color}\n")
    for reg in registros:
        print(f"{color_rosa}-" * ancho)
        print(f"{color_rosa}ID:{reset_color} {reg['id']}")
        print(f"{color_rosa}Nombre:{reset_color} {reg['nombre']}")
        print(f"{color_rosa}Raza:{reset_color} {reg['raza']}")
        print(f"{color_rosa}-" * ancho)

def busqueda_id():
    """
    Retorna True si el usuario quiere buscar por ID, False si quiere ver todos.
    """
    buscar_id = ""
    while buscar_id not in ('s','n'):
        buscar_id = input(f"¿Quieres buscar por ID? ({color_rosa}s{reset_color}/{color_rosa}n{reset_color}): ").strip().lower()
    return buscar_id == 's'
        
def menu():
    ancho = 40
    borde = f"{color_rosa}+" + "-" * (ancho - 2) + f"+{reset_color}"
    print()
    print(borde)
    print(f"{color_rosa}|{'MENU'.center(ancho - 2)}|{reset_color}")
    print(borde)

    opciones = [
        "Escribir",
        "Leer",
        "Exportar fichero",
        "Salir"
    ]

    for i, opcion in enumerate(opciones, start=1):
        numero = f"{i}."
        linea = f"{numero} {opcion}".ljust(ancho - 4)
        linea_coloreada = linea.replace(numero, f"{color_rosa}{numero}{reset_color}", 1)
        print(f"{color_rosa}|{reset_color} {linea_coloreada} {color_rosa}|{reset_color}")

    print(borde)

def obtener_id():
    '''Solicita un ID válido al usuario'''
    while True:
        id_input = input(f"Introduce el {color_rosa}ID{reset_color} (posición del registro): ").strip()
        if id_input.isdigit():
            return int(id_input)
        else:
            print("ID no válido. Debe ser un número entero.")

def submenu(tipo_archivo):
    match tipo_archivo:
        case "json":
            print(f"\n{color_rosa}Formatos disponibles para JSON:{reset_color}")
            print(f"{color_rosa}1.{reset_color} JSON → BIN")
            print(f"{color_rosa}2.{reset_color} JSON → TXT")
        case "bin":
            print(f"\n{color_rosa}Formatos disponibles para BIN:{reset_color}")
            print(f"{color_rosa}1.{reset_color} BIN → JSON")
            print(f"{color_rosa}2.{reset_color} BIN → TXT")
        case "txt":
            print(f"\n{color_rosa}Formatos disponibles para TXT:{reset_color}")
            print(f"{color_rosa}1.{reset_color} TXT → JSON")
            print(f"{color_rosa}2.{reset_color} TXT → BIN")
    print(f"{color_rosa}3.{reset_color} Salir al menú principal")

rj.guardar_datos([])
archivo = obtener_archivo_actual()
while True:
    tipo_actual = tipo_archivo(archivo)
    menu()
    opcion = input(f"Seleccione una opción ({color_rosa}1{reset_color}-{color_rosa}4{reset_color}): ").strip()
    match opcion:

        case "1":
            match tipo_actual:
                case "json":
                    rj.crear_registro()

                case "bin":
                    bin_a_json()
                    archivo = "registros.json"
                    rj.crear_registro()
                    json_a_bin("registros.json")
                    archivo = "registros.bin"

                case "txt":
                    txt_a_json(archivo)
                    archivo = "registros.json"
                    rj.crear_registro()
                    json_a_txt("registros.json")
                    archivo = "registros.txt"

        case "2":
            match tipo_actual:
                case "json":
                    registros = rj.leer_registro()
                    mostrar_datos(registros)

                case "bin":
                    while True:
                        buscar_id = busqueda_id()
                        if not buscar_id:
                            registros = b.leer_todos()
                            mostrar_datos(registros)
                            break

                        registro = b.leer_por_id(obtener_id())
                        mostrar_datos(registro)
                        break

                case "txt":
                    while True:
                        buscar_id = busqueda_id()
                        if not buscar_id:
                            tp.ver_contenido()
                            break
                        tp.ver_por_id()
                        break
                        
        case "3":
            while True:
                submenu(tipo_actual)
                sub_opcion = input(f"\nSeleccione una opción ({color_rosa}1{reset_color}-{color_rosa}3{reset_color}): ").strip()
                match (tipo_actual, sub_opcion):

                    case ("json", "1"):
                        json_a_bin(archivo)
                        archivo = "registros.bin"
                        break

                    case ("json", "2"):
                        json_a_txt(archivo)
                        archivo = "registros.txt"
                        break
                    
                    case ("bin", "1"):
                        bin_a_json()
                        archivo = "registros.json"
                        break

                    case ("bin", "2"):
                        bin_a_txt(archivo)
                        archivo = "registros.txt"
                        break

                    case ("txt", "1"):
                        txt_a_json(archivo)
                        archivo = "registros.json"
                        break

                    case ("txt", "2"):
                        txt_a_bin(archivo)
                        archivo = "registros.bin"
                        break

                    case ("json" | "bin" | "txt", "3"):
                        print(f"{color_rosa}Volviendo al menú principal...{reset_color}")
                        break

                    case _:
                        print("Opción no válida.")

        case "4":
            print(f"{color_rosa}Saliendo del programa...{reset_color}")
            break

        case _:
            print("Opción no válida.")