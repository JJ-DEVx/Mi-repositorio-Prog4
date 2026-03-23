import sqlite3

# CONEXIÓN A LA BASE DE DATOS
# Esta función crea (o abre) la base de datos SQLite llamada biblioteca.db
def conectar():
    return sqlite3.connect("biblioteca.db")


# CREAR TABLA SI NO EXISTE
# Aquí se crea la tabla "libros" con sus campos
# id, titulo, autor, genero y estado
def crear_tabla():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS libros (id INTEGER PRIMARY KEY AUTOINCREMENT, titulo TEXT NOT NULL, autor TEXT NOT NULL, genero TEXT, estado TEXT)"
    )
    conn.commit()
    conn.close()


# AGREGAR LIBRO y Permite ingresar un nuevo libro a la base de datos
def agregar_libro():
    titulo = input("Título: ")
    autor = input("Autor: ")
    genero = input("Género: ")
    estado = input("Estado (leído/no leído): ")

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO libros (titulo, autor, genero, estado) VALUES (?, ?, ?, ?)", (titulo, autor, genero, estado))
    conn.commit()
    conn.close()

    print("Libro agregado correctamente")


# VER LIBROS
# Muestra todos los libros guardados
def ver_libros():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM libros")
    libros = cursor.fetchall()
    conn.close()

    if libros:
        print("LISTADO DE LIBROS")
        for libro in libros:
            print("ID:", libro[0], "| Título:", libro[1], "| Autor:", libro[2], "| Género:", libro[3], "| Estado:", libro[4])
    else:
        print("No hay libros registrados")


# ACTUALIZAR LIBRO
# Permite modificar los datos de un libro existente
def actualizar_libro():
    id_libro = input("Ingrese ID: ")

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM libros WHERE id = ?", (id_libro,))
    libro = cursor.fetchone()

    if libro:
        nuevo_titulo = input("Nuevo título: ") or libro[1]
        nuevo_autor = input("Nuevo autor: ") or libro[2]
        nuevo_genero = input("Nuevo género: ") or libro[3]
        nuevo_estado = input("Nuevo estado: ") or libro[4]

        cursor.execute("UPDATE libros SET titulo=?, autor=?, genero=?, estado=? WHERE id=?", (nuevo_titulo, nuevo_autor, nuevo_genero, nuevo_estado, id_libro))
        conn.commit()
        print("Libro actualizado")
    else:
        print("Libro no encontrado")

    conn.close()


# ELIMINAR LIBRO
# Elimina un libro usando su ID
def eliminar_libro():
    id_libro = input("Ingrese ID: ")

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM libros WHERE id = ?", (id_libro,))
    conn.commit()
    conn.close()

    print("Libro eliminado")


# BUSCAR LIBROS
# Permite buscar por título, autor o género
def buscar_libros():
    criterio = input("Buscar por (titulo/autor/genero): ").lower()
    valor = input("Valor: ")

    conn = conectar()
    cursor = conn.cursor()

    if criterio == "titulo":
        cursor.execute("SELECT * FROM libros WHERE titulo LIKE ?", ("%"+valor+"%",))
    elif criterio == "autor":
        cursor.execute("SELECT * FROM libros WHERE autor LIKE ?", ("%"+valor+"%",))
    elif criterio == "genero":
        cursor.execute("SELECT * FROM libros WHERE genero LIKE ?", ("%"+valor+"%",))
    else:
        print("Criterio inválido")
        return

    resultados = cursor.fetchall()
    conn.close()

    if resultados:
        print("RESULTADOS")
        for libro in resultados:
            print(libro)
    else:
        print("Sin resultados")


# MENÚ PRINCIPAL
# Controla la navegación del programa
def menu():
    crear_tabla()

    while True:
        print("===== BIBLIOTECA PERSONAL =====")
        print("1. Agregar libro")
        print("2. Ver libros")
        print("3. Actualizar libro")
        print("4. Eliminar libro")
        print("5. Buscar libros")
        print("6. Salir")

        opcion = input("Opción: ")

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
            print("Saliendo...")
            break
        else:
            print("Opción inválida")


# EJECUCIÓN DEL PROGRAMA
if __name__ == "__main__":
    menu()