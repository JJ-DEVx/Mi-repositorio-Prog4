# =========================================
# BIBLIOTECA PERSONAL CON MARIA DB + SQLALCHEMY
# =========================================

# Librerías necesarias
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# =========================================
# CONFIGURACIÓN DE LA BASE DE DATOS
# =========================================
# Cambia estos datos por tu configuración
USUARIO = "tu_usuario"
CONTRASENA = "tu_contrasena"
HOST = "localhost"
BD = "biblioteca"

# Crear la cadena de conexión
DATABASE_URL = f"mysql+pymysql://{USUARIO}:{CONTRASENA}@{HOST}/{BD}"

# Crear el motor y la sesión
engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# =========================================
# MODELO ORM DEL LIBRO
# =========================================
class Libro(Base):
    __tablename__ = 'libros'

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(100), nullable=False)
    autor = Column(String(100), nullable=False)
    genero = Column(String(50))
    estado = Column(String(20))

    def __repr__(self):
        return f"ID:{self.id} | {self.titulo} | {self.autor} | {self.genero} | {self.estado}"

# Crear la tabla si no existe
Base.metadata.create_all(engine)

# =========================================
# FUNCIONES CRUD
# =========================================
def agregar_libro():
    try:
        titulo = input("Título: ")
        autor = input("Autor: ")
        genero = input("Género: ")
        estado = input("Estado (Leído/No leído): ")

        nuevo_libro = Libro(titulo=titulo, autor=autor, genero=genero, estado=estado)
        session.add(nuevo_libro)
        session.commit()
        print("\nLibro agregado correctamente.\n")
    except SQLAlchemyError as e:
        session.rollback()
        print("Error al agregar libro:", e)

def ver_libros():
    libros = session.query(Libro).all()
    if libros:
        print("\nLISTADO DE LIBROS:")
        for libro in libros:
            print(libro)
        print()
    else:
        print("\nNo hay libros registrados.\n")

def actualizar_libro():
    try:
        id_libro = input("Ingrese ID del libro a actualizar: ")
        libro = session.query(Libro).filter_by(id=id_libro).first()
        if libro:
            print("Deja en blanco si no deseas cambiar un campo.")
            nuevo_titulo = input(f"Nuevo título ({libro.titulo}): ") or libro.titulo
            nuevo_autor = input(f"Nuevo autor ({libro.autor}): ") or libro.autor
            nuevo_genero = input(f"Nuevo género ({libro.genero}): ") or libro.genero
            nuevo_estado = input(f"Nuevo estado ({libro.estado}): ") or libro.estado

            libro.titulo = nuevo_titulo
            libro.autor = nuevo_autor
            libro.genero = nuevo_genero
            libro.estado = nuevo_estado
            session.commit()
            print("\nLibro actualizado correctamente.\n")
        else:
            print("\nLibro no encontrado.\n")
    except SQLAlchemyError as e:
        session.rollback()
        print("Error al actualizar libro:", e)

def eliminar_libro():
    try:
        id_libro = input("Ingrese ID del libro a eliminar: ")
        libro = session.query(Libro).filter_by(id=id_libro).first()
        if libro:
            session.delete(libro)
            session.commit()
            print("\nLibro eliminado correctamente.\n")
        else:
            print("\nLibro no encontrado.\n")
    except SQLAlchemyError as e:
        session.rollback()
        print("Error al eliminar libro:", e)

def buscar_libros():
    criterio = input("Buscar por (titulo/autor/genero): ").lower()
    valor = input("Ingrese el texto a buscar: ")

    if criterio not in ["titulo", "autor", "genero"]:
        print("Criterio no válido.")
        return

    resultados = session.query(Libro).filter(getattr(Libro, criterio).like(f"%{valor}%")).all()
    if resultados:
        print("\nRESULTADOS:")
        for libro in resultados:
            print(libro)
        print()
    else:
        print("\nNo se encontraron resultados.\n")

# =========================================
# MENÚ PRINCIPAL
# =========================================
def menu():
    while True:
        print("""
===== BIBLIOTECA PERSONAL (MariaDB + SQLAlchemy) =====
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

# =========================================
# EJECUCIÓN
# =========================================
if __name__ == "__main__":
    menu()