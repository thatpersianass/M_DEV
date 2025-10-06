import struct

formato = "i20s30s"
archivo = "registros.bin"

perros = [
    (1, "Luna", "Labrador Retriever"),
    (2, "Max", "Pastor Alemán"),
    (3, "Kira", "Bulldog Francés"),
    (4, "Rocky", "Golden Retriever"),
    (5, "Nala", "Beagle")
]

with open(archivo, "wb") as f:
    for id, nombre, raza in perros:
        registro = struct.pack(
            formato,
            id,
            nombre.encode("utf-8").ljust(20, b" "),
            raza.encode("utf-8").ljust(30, b" ")
        )
        f.write(registro)

print(f"Archivo '{archivo}' generado con {len(perros)} registros.")
