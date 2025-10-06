import struct
import os
import json

formato = "i20s30s"
tamaño_registro = struct.calcsize(formato)
archivo_bin = "registros.bin"
archivo_json = "registros.json"

def binario_a_json():
    """
    Convierte el archivo binario de perros a un archivo JSON.
    """
    if not os.path.exists(archivo_bin):
        print("❌ No se encontró el archivo binario.")
        return

    registros = []

    with open(archivo_bin, "rb") as f:
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

    with open(archivo_json, "w", encoding="utf-8") as f_json:
        json.dump(registros, f_json, ensure_ascii=False, indent=4)

    print(f"✅ Archivo '{archivo_json}' generado con {len(registros)} registros.")


if __name__ == "__main__":
    binario_a_json()
