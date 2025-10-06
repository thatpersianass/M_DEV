import struct
import json
import os

# Formato binario: id (int), nombre (20 bytes), raza (30 bytes)
formato = "i20s30s"
tamaño_registro = struct.calcsize(formato)
archivo_json = "registros.json"
archivo_bin = "registros.bin"

def json_a_binario():
    """
    Convierte el archivo JSON de perros a un archivo binario.
    Sobrescribe perros.bin si ya existe.
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

    with open(archivo_bin, "wb") as f_bin:
        for perro in registros:
            try:
                id = int(perro.get("id", -1))
                nombre = str(perro.get("nombre", ""))[:20]
                raza = str(perro.get("raza", ""))[:30]

                registro = struct.pack(
                    formato,
                    id,
                    nombre.encode("utf-8").ljust(20, b" "),
                    raza.encode("utf-8").ljust(30, b" ")
                )
                f_bin.write(registro)
            except Exception as e:
                print(f"⚠️ Error al procesar registro {perro}: {e}")

    print(f"✅ Archivo '{archivo_bin}' generado con {len(registros)} registros.")


if __name__ == "__main__":
    json_a_binario()
