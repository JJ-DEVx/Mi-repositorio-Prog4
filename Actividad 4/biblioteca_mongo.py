from pymongo import MongoClient, errors


# CONFIGURACIÓN DE CONEXIÓN
# Se cambian estos datos dependiendo si es MongoDB local o Atlas
MONGO_URI = "mongodb://localhost:27017/"  # para MongoDB local
# Ejemplo MongoDB Atlas:
# MONGO_URI = "mongodb+srv://usuario:contrasena@cluster.mongodb.net/test?retryWrites=true&w=majority"
DB_NAME = "biblioteca"
COLLECTION_NAME = "libros"

try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    coleccion = db[COLLECTION_NAME]
except errors.ConnectionFailure as e:
    print("No se pudo conectar a MongoDB:", e)
    exit(1)


# FUNCIONES CRUD
def agregar_libro():
    titulo = input("Título: ")
    autor = input("Autor: ")
    genero = input("Género: ")
    estado = input("Estado (leído/no leído): ")

    libro = {
        "titulo": titulo,
        "autor": autor,
        "genero": genero,
        "estado": estado
    }

    try:
        coleccion.insert_one(libro)
        print("\nLibro agregado correctamente.\n")
    except errors.PyMongoError as e:
        print("Error al agregar el libro:", e)

def ver_libros():
    try:
        libros = list(coleccion.find())
        if libros:
            print("\nLISTADO DE LIBROS:")
            for l in libros:
                print(f"ID: {l['_id']} | Título: {l['titulo']} | Autor: {l['autor']} | Género: {l['genero']} | Estado: {l['estado']}")
        else:
            print("\nNo hay libros registrados.\n")
    except errors.PyMongoError as e:
        print("Error al recuperar libros:", e)

def actualizar_libro():
    id_libro = input("Ingrese el ID del libro a actualizar: ")
    from bson import ObjectId
    try:
        libro = coleccion.find_one({"_id": ObjectId(id_libro)})
        if libro:
            print("Deje en blanco si no desea cambiar un campo.")
            nuevo_titulo = input(f"Nuevo título ({libro['titulo']}): ") or libro['titulo']
            nuevo_autor = input(f"Nuevo autor ({libro['autor']}): ") or libro['autor']
            nuevo_genero = input(f"Nuevo género ({libro['genero']}): ") or libro['genero']
            nuevo_estado = input(f"Nuevo estado ({libro['estado']}): ") or libro['estado']

            coleccion.update_one(
                {"_id": ObjectId(id_libro)},
                {"$set": {
                    "titulo": nuevo_titulo,
                    "autor": nuevo_autor,
                    "genero": nuevo_genero,
                    "estado": nuevo_estado
                }}
            )
            print("\nLibro actualizado correctamente.\n")
        else:
            print("\nLibro no encontrado.\n")
    except errors.PyMongoError as e:
        print("Error al actualizar libro:", e)
    except Exception:
        print("ID inválido. Debe ser un ObjectId válido.")

def eliminar_libro():
    id_libro = input("Ingrese el ID del libro a eliminar: ")
    from bson import ObjectId
    try:
        result = coleccion.delete_one({"_id": ObjectId(id_libro)})
        if result.deleted_count > 0:
            print("\nLibro eliminado correctamente.\n")
        else:
            print("\nLibro no encontrado.\n")
    except Exception:
        print("ID inválido. Debe ser un ObjectId válido.")

def buscar_libros():
    criterio = input("Buscar por (titulo/autor/genero): ").lower()
    valor = input("Ingrese el valor de búsqueda: ")

    if criterio not in ["titulo", "autor", "genero"]:
        print("Criterio no válido.")
        return

    try:
        resultados = list(coleccion.find({criterio: {"$regex": valor, "$options": "i"}}))
        if resultados:
            print("\nRESULTADOS:")
            for l in resultados:
                print(f"ID: {l['_id']} | Título: {l['titulo']} | Autor: {l['autor']} | Género: {l['genero']} | Estado: {l['estado']}")
        else:
            print("\nNo se encontraron resultados.\n")
    except errors.PyMongoError as e:
        print("Error al buscar libros:", e)


# MENÚ PRINCIPAL
def menu():
    while True:
        print("""
===== BIBLIOTECA PERSONAL (MongoDB) =====
1. Agregar libro
2. Ver libros
3. Actualizar libro
4. Eliminar libro
5. Buscar libros
6. Salir
""")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            agregar_libro()
        elif opcion == "2":
            ver_libros()
        elif opcion == "3":
            actualizar_libro()
        elif opcion == "4":
            eliminar_libro()
        elif opcion == "5":
            buscar_libros()
        elif opcion == "6":
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    menu()
