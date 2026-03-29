import json
import os

# Archivo donde se guardan los artículos
ARCHIVO = "articulos.json"


# CARGAR DATOS
# Esta lee el archivo JSON y devuelve la lista de artículos
def cargar_datos():
    if not os.path.exists(ARCHIVO):
        return []
    try:
        with open(ARCHIVO, "r") as f:
            return json.load(f)
    except:
        return []


# GUARDAR DATOS
# Guarda la lista de artículos en el archivo JSON
def guardar_datos(datos):
    with open(ARCHIVO, "w") as f:
        json.dump(datos, f, indent=4)


# REGISTRAR ARTÍCULO
# Solicita datos al usuario y crea un nuevo artículo
def registrar():
    datos = cargar_datos()

    nombre = input("Nombre: ")
    categoria = input("Categoría: ")

    # Validación de datos numéricos
    try:
        cantidad = int(input("Cantidad: "))
        precio = float(input("Precio unitario: "))
    except:
        print("❌ Error: cantidad o precio inválido")
        return

    descripcion = input("Descripción: ")

    # Validación de campos obligatorios
    if not nombre or not categoria:
        print("❌ Campos obligatorios vacíos")
        return

    articulo = {
        "id": len(datos) + 1,
        "nombre": nombre,
        "categoria": categoria,
        "cantidad": cantidad,
        "precio": precio,
        "descripcion": descripcion
    }

    datos.append(articulo)
    guardar_datos(datos)

    print("✅ Artículo registrado correctamente")


# LISTAR ARTÍCULOS
# Muestra todos los artículos registrados en formato ordenado
def listar():
    datos = cargar_datos()

    if not datos:
        print("No hay artículos registrados")
        return

    print("\nID | Nombre | Categoría | Cantidad | Precio")
    print("-" * 60)

    for a in datos:
        print(f"{a['id']} | {a['nombre']} | {a['categoria']} | {a['cantidad']} | {a['precio']}")


# BUSCAR ARTÍCULOS
# Permite buscar artículos por nombre o categoría
def buscar():
    datos = cargar_datos()
    valor = input("Buscar por nombre o categoría: ").lower()

    resultados = [
        a for a in datos
        if valor in a["nombre"].lower() or valor in a["categoria"].lower()
    ]

    if resultados:
        print("\nResultados encontrados:")
        for a in resultados:
            print(f"{a['id']} | {a['nombre']} | {a['categoria']}")
    else:
        print("❌ No se encontraron resultados")


# EDITAR ARTÍCULO
# Permite modificar los datos de un artículo existente mediante su ID
def editar():
    datos = cargar_datos()

    try:
        id_buscar = int(input("ID del artículo a editar: "))
    except:
        print("❌ ID inválido")
        return

    for a in datos:
        if a["id"] == id_buscar:
            print("Dejar vacío para mantener el valor actual")

            nuevo_nombre = input(f"Nombre ({a['nombre']}): ") or a["nombre"]
            nueva_categoria = input(f"Categoría ({a['categoria']}): ") or a["categoria"]

            try:
                nueva_cantidad = input(f"Cantidad ({a['cantidad']}): ")
                nueva_cantidad = int(nueva_cantidad) if nueva_cantidad else a["cantidad"]

                nuevo_precio = input(f"Precio ({a['precio']}): ")
                nuevo_precio = float(nuevo_precio) if nuevo_precio else a["precio"]
            except:
                print("❌ Datos numéricos inválidos")
                return

            nueva_desc = input(f"Descripción ({a['descripcion']}): ") or a["descripcion"]

            a.update({
                "nombre": nuevo_nombre,
                "categoria": nueva_categoria,
                "cantidad": nueva_cantidad,
                "precio": nuevo_precio,
                "descripcion": nueva_desc
            })

            guardar_datos(datos)
            print("✅ Artículo actualizado correctamente")
            return

    print("❌ Artículo no encontrado")


# ELIMINAR ARTÍCULO
# Elimina un artículo del sistema usando su ID
def eliminar():
    datos = cargar_datos()

    try:
        id_buscar = int(input("ID del artículo a eliminar: "))
    except:
        print("❌ ID inválido")
        return

    nuevos = [a for a in datos if a["id"] != id_buscar]

    if len(nuevos) == len(datos):
        print("❌ Artículo no encontrado")
        return

    guardar_datos(nuevos)
    print("✅ Artículo eliminado correctamente")


# MENÚ PRINCIPAL
# Controla la interacción con el usuario mediante opciones
def menu():
    while True:
        print("\n--- SISTEMA DE ARTÍCULOS ---")
        print("1. Registrar")
        print("2. Listar")
        print("3. Buscar")
        print("4. Editar")
        print("5. Eliminar")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar()
        elif opcion == "2":
            listar()
        elif opcion == "3":
            buscar()
        elif opcion == "4":
            editar()
        elif opcion == "5":
            eliminar()
        elif opcion == "6":
            print("👋 Saliendo del sistema...")
            break
        else:
            print("❌ Opción inválida")


# EJECUCIÓN PRINCIPAL
# Punto de entrada del programa
if __name__ == "__main__":
    menu()