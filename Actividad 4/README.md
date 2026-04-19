-Instrucciones para instalar MongoDB (local o Atlas)

Local (Windows / Linux / macOS)
1. Descargar MongoDB: https://www.mongodb.com/try/download/community  
2. Instalar y ejecutar el servicio MongoDB localmente  
3. Asegurarse de que `mongod` esté corriendo

MongoDB Atlas (Remoto)
1. Crear cuenta en https://www.mongodb.com/cloud/atlas  
2. Crear cluster gratuito  
3. Obtener la cadena de conexión (URI) para Python  
4. Reemplazar `MONGO_URI` en el archivo `biblioteca_mongo.py`

-Configuración de la cadena de conexión
En `biblioteca_mongo.py`, modifica:

python
MONGO_URI = "mongodb://usuario:contrasena@localhost:27017/"  # o tu URI de Atlas
DB_NAME = "biblioteca"
COLLECTION_NAME = "libros"

-Comando para ejecutar la aplicación
1. Instalar dependencias:
2. Ejecutar el programa:
3. Se mostrará el menú interactivo para agregar, ver, actualizar, eliminar y buscar libros.

-Ejemplos de entradas válidas y estructura esperada del documento
Cuando agregamos un libro, se crea un documento JSON así:
{
  "_id": "ObjectId generado automáticamente",
  "titulo": "Cien Años de Soledad",
  "autor": "Gabriel García Márquez",
  "genero": "Novela",
  "estado": "leído"
}
titulo: texto
autor: texto
genero: texto (opcional)
estado: "leído" o "no leído"

-Validaciones para errores comunes
1. Error de conexión
Si MongoDB no está corriendo o la URI es incorrecta, el programa muestra: No se pudo conectar a MongoDB: <detalle del error>

2. Documentos mal estructurados
Si algún campo se deja vacío, el programa utiliza valores predeterminados o solicita corrección.

3. Búsquedas sin resultados
Si no se encuentra ningún libro con el criterio buscado, el programa muestra: No se encontraron resultados.

4. ID inválido
Al actualizar o eliminar, si ingresamos un ID que no existe o no es un ObjectId válido, se muestra un mensaje de error claro.

Nota: Cada libro es un documento independiente en la colección libros. El programa maneja automáticamente la creación de documentos y la recuperación de datos.





