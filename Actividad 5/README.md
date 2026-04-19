Biblioteca Personal en Python con KeyDB

# Descripción
Aplicación de línea de comandos que gestiona una biblioteca personal usando KeyDB (compatible con Redis).  
Cada libro se almacena como un objeto JSON serializado en memoria.

 Requisitos
- Python 3
- KeyDB o Redis
- Librerías Python: redis, python-dotenv

# Instalación de KeyDB Local
1. Descargar KeyDB: https://keydb.dev/downloads/  
2. Instalar y ejecutar el servicio KeyDB  
3. Verificar que el puerto por defecto (6379) esté disponible

#Configuración
1. Crear un archivo `.env` en la misma carpeta que `biblioteca_keydb.py`: 
text
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=   # si aplica

2. Ajustamos los valores según tu entorno.

# Ejecución
1. Instalar dependencias:
2. Ejecutar el programa:
3. Se mostrará un menú interactivo:

Ejemplos de entradas válidas
 Cuando agregamos un libro:
{
  "id": 1,
  "titulo": "Cien Años de Soledad",
  "autor": "Gabriel García Márquez",
  "genero": "Novela",
  "estado": "leído"
}

1. Validaciones y manejo de errores comunes
Error de conexión: Si KeyDB no está corriendo o la conexión falla, el programa muestra: No se pudo conectar a KeyDB: <detalle del error>

2. Clave no encontrada:
Al actualizar o eliminar un libro inexistente, se muestra: Libro no encontrado

3. Búsquedas sin resultados:
Si ningún libro coincide con el criterio, el programa muestra:
No se encontraron resultados

4. Documentos mal estructurados:
Si algún campo está vacío, el programa solicita corrección o usa valores predeterminados.


Nota: Nota
Cada libro se guarda como JSON en memoria con clave libro:<id>
El contador de ID se maneja automáticamente con la clave libro:id
El programa que realice maneja automáticamente la creación, actualización, eliminación y búsqueda de libros
