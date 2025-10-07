import os

color_rosa = "\033[95m"
reset_color = "\033[0m"

def crear_fichero():
    '''Crea un nuevo fichero de texto vacío con el nombre que indique el usuario'''
    nombref = "registros"
    ruta_completaf = nombref + ".txt"
    with open(ruta_completaf, "w") as arc:
        arc.write("")
    print(f"Fichero '{ruta_completaf}' creado correctamente.")

def ver_contenido():
    '''Muestra el contenido completo de un fichero, si existe'''
    nombrefic = "registros.txt"
    if os.path.exists(nombrefic):
        with open(nombrefic, "r") as arc:
            print(f"\n{color_rosa}CONTENIDO DEL FICHERO:{reset_color}\n")
            print(arc.read())
    else:
        print("El archivo no existe.")

def ver_por_id():
    '''Busca un registro específico dentro del fichero según el ID introducido'''
    nombrefic = "registros.txt"
    if not os.path.exists(nombrefic):
        print("El archivo no existe.")
        return
    
    buscar_id = input(f"Introduce el {color_rosa}ID{reset_color} que quieres buscar: ").strip()
    encontrado = False
    
    with open(nombrefic, "r") as arc:
        contenido = arc.read().strip()
        registros = contenido.split("\n\n")
    
    for reg in registros:
        if reg.startswith(f"id: {buscar_id}") or reg.startswith(f"id:{buscar_id}"):
            print(f"\n{color_rosa}REGISTRO ENCONTRADO:{reset_color}\n")
            print(reg)
            encontrado = True
            break
    
    if not encontrado:
        print("No se encontró un registro con ese ID.")

def obtener_siguiente_id(nombref):
    '''Devuelve el próximo ID disponible leyendo el último usado en el fichero'''
    if not os.path.exists(nombref):
        return 1
    
    with open(nombref, "r") as arc:
        contenido = arc.read().strip()
    
    if not contenido:
        return 1

    
    lineas = [linea for linea in contenido.splitlines() if linea.startswith("ID:")]
    if not lineas:
        return 1
    ultimo_id = int(lineas[-1].split(":")[1])
    return ultimo_id + 1

def modificar_fichero():
    '''Añade nuevos registros (ID, nombre y raza de un perro) a un fichero existente'''
    nombref = input("¿Cómo se llama el fichero (incluye .txt)? ")
    if not os.path.exists(nombref):
        print("El archivo no existe.")
        return

    while True:
        identificador = obtener_siguiente_id(nombref)  
        nombre = input("Nombre del perro: ")
        raza = input("Raza del perro: ")

        with open(nombref, "r") as arc:
            contenido = arc.read().strip()

        
        if contenido:
            registro = f"\n\nID: {identificador}\nNombre: {nombre}\nRaza: {raza}"
        else: 
            registro = f"ID: {identificador}\nNombre: {nombre}\nRaza: {raza}"

        
        with open(nombref, "a") as arc:
            arc.write(registro)

        masr = input("¿Quieres añadir otro registro? (s/n): ").lower()
        if masr != "s":
            break

    print("Registro(s) añadido(s) correctamente.")

def menu_principal():
    '''Muestra un menú interactivo para gestionar ficheros y registros'''
    while True: 
        print("\n--- Menú Ficheros ---") 
        print("1. Crear fichero") 
        print("2. Ver contenido de fichero") 
        print("3. Modificar (añadir registros)") 
        print("4. Ver registro por ID") 
        print("0. Salir") 
        opcion = input("Introduce el número correspondiente: ") 
        match opcion: 
            case '1': crear_fichero() 
            case '2': ver_contenido() 
            case '3': modificar_fichero() 
            case '4': ver_por_id() 
            case '0': 
                print("Saliendo...") 
                break 
            case _: 
                print("Opción no válida.") 

def main(): 
    '''Función principal'''
    menu_principal() 

if __name__ == "__main__": 
    main()
