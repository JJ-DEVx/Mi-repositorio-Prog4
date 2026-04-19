# Biblioteca Personal en Python con MariaDB y SQLAlchemy

Descripción
Aplicación de línea de comandos en Python para administrar una biblioteca personal, utilizando MariaDB como base de datos y SQLAlchemy como ORM.  
Permite agregar, actualizar, eliminar, listar y buscar libros por título, autor o género.


Instalación de MariaDB

Seguimos estos pasos según el sistema operativo:

En mi caso soy Windows, dependerá del sistema operativo que se tenga:
1. Descargar MariaDB: https://mariadb.org/download/  
2. Ejecutar el instalador y seguir los pasos.  
3. Durante la instalación, configurar un usuario y contraseña (por ejemplo: `root` / `1234`).  

Comandos para crear la base de datos y tabla(s)
1. Ingresar al cliente de MariaDB:
2. Crear la base de datos:
3. Crear el usuario y asignarle permisos:
4. La tabla se crea automáticamente con SQLAlchemy al ejecutar el programa, no se necesita crearla manualmente

Instrucciones para configurar la cadena de conexión
1. Instalar dependencias:
2. Ejecutar el programa:
3. Usar el menú interactivo para agregar, ver, actualizar, eliminar y buscar libros.

Nota: El programa requiere MariaDB corriendo.
Si se ejecuta sin MariaDB, la conexión fallará.
SQLAlchemy se encarga de crear la tabla libros automáticamente si no existe.