import redis
import json
import os
from dotenv import load_dotenv


# CARGAR VARIABLES DE ENTORNO
load_dotenv()  # lee el archivo .env si existe

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

try:
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)
    r.ping()
except redis.ConnectionError as e:
    print("No se pudo conectar a KeyDB:", e)
    exit(1)


# FUNCIONES CRUD
def generar_clave(id_libro):
    return f"libro:{id_libro}"

def agregar_libro():
    id_libro = r.incr("libro:id")  # contador automático
    titulo = input("Título: ")
    autor = input("Autor: ")
    genero = input("Género: ")
    estado = input("Estado (leído/no leído): ")

    libro = {
        "id": id_libro,
        "titulo": titulo,
        "autor": autor,
        "genero": genero,
        "estado": estado
    }

    try:
        r.set(generar_clave(id_libro), json.dumps(libro))
        print("\nLibro agregado correctamente.\n")
    except redis.RedisError as e:
        print("Error al agregar el libro:", e)

def ver_libros():
    try:
        libros = []
        for key in r.scan_iter("libro:*"):
            if key != "libro:id":  # excluir el contador
                libros.append(json.loads(r.get(key)))
        if libros:
            print("\nLISTADO DE LIBROS:")
            for l in libros:
                print(f"ID: {l['id']} | Título: {l['titulo']} | Autor: {l['autor']} | Género: {l['genero']} | Estado: {l['estado']}")
        else:
            print("\nNo hay libros registrados.\n")
    except redis.RedisError as e:
        print("Error al recuperar libros:", e)

def actualizar_libro():
    id_libro = input("Ingrese el ID del libro a actualizar: ")
    clave = generar_clave(id_libro)
    try:
        libro_json = r.get(clave)
        if libro_json:
            libro = json.loads(libro_json)
            print("Deje en blanco si no desea cambiar un campo.")
            libro["titulo"] = input(f"Nuevo título ({libro['titulo']}): ") or libro['titulo']
            libro["autor"] = input(f"Nuevo autor ({libro['autor']}): ") or libro['autor']
            libro["genero"] = input(f"Nuevo género ({libro['genero']}): ") or libro['genero']
            libro["estado"] = input(f"Nuevo estado ({libro['estado']}): ") or libro['estado']

            r.set(clave, json.dumps(libro))
            print("\nLibro actualizado correctamente.\n")
        else:
            print("\nLibro no encontrado.\n")
    except redis.RedisError as e:
        print("Error al actualizar libro:", e)

def eliminar_libro():
    id_libro = input("Ingrese el ID del libro a eliminar: ")
    clave = generar_clave(id_libro)
    try:
        if r.delete(clave):
            print("\nLibro eliminado correctamente.\n")
        else:
            print("\nLibro no encontrado.\n")
    except redis.RedisError as e:
        print("Error al eliminar libro:", e)

def buscar_libros():
    criterio = input("Buscar por (titulo/autor/genero): ").lower()
    valor = input("Ingrese el valor de búsqueda: ")

    if criterio not in ["titulo", "autor", "genero"]:
        print("Criterio no válido.")
        return

    try:
        resultados = []
        for key in r.scan_iter("libro:*"):
            if key != "libro:id":
                libro = json.loads(r.get(key))
                if valor.lower() in libro[criterio].lower():
                    resultados.append(libro)
        if resultados:
            print("\nRESULTADOS:")
            for l in resultados:
                print(f"ID: {l['id']} | Título: {l['titulo']} | Autor: {l['autor']} | Género: {l['genero']} | Estado: {l['estado']}")
        else:
            print("\nNo se encontraron resultados.\n")
    except redis.RedisError as e:
        print("Error al buscar libros:", e)


# MENÚ PRINCIPAL
def menu():
    while True:
        print("""
===== BIBLIOTECA PERSONAL (KeyDB) =====
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
