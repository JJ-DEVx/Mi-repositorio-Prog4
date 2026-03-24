from flask import Flask, render_template, request, redirect, flash
import redis
import json
from tasks import enviar_correo

app = Flask(__name__)
app.secret_key = "clave123"

# Conexión a KeyDB/Redis
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

def clave(id):
    return f"libro:{id}"


# LISTAR LIBROS
@app.route('/')
def index():
    libros = []
    for k in r.scan_iter("libro:*"):
        if k != "libro:id":
            libro = json.loads(r.get(k))
            libros.append(libro)
    return render_template("index.html", libros=libros)


# AGREGAR LIBRO
@app.route('/agregar', methods=['GET','POST'])
def agregar():
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        genero = request.form['genero']
        estado = request.form['estado']

        if not titulo or not autor:
            flash("Campos obligatorios vacíos")
            return redirect('/agregar')

        id_libro = r.incr("libro:id")

        libro = {
            "id": id_libro,
            "titulo": titulo,
            "autor": autor,
            "genero": genero,
            "estado": estado
        }

        r.set(clave(id_libro), json.dumps(libro))

        # CORREO ASÍNCRONO
        enviar_correo.delay(
            "Libro agregado",
            "correo@ejemplo.com",
            f"Se agregó el libro: {titulo}"
        )

        flash("Libro agregado correctamente")
        return redirect('/')

    return render_template("agregar.html")


# EDITAR LIBRO
@app.route('/editar/<int:id>', methods=['GET','POST'])
def editar(id):
    libro_json = r.get(clave(id))

    if not libro_json:
        flash("Libro no encontrado")
        return redirect('/')

    libro = json.loads(libro_json)

    if request.method == 'POST':
        libro['titulo'] = request.form['titulo']
        libro['autor'] = request.form['autor']
        libro['genero'] = request.form['genero']
        libro['estado'] = request.form['estado']

        r.set(clave(id), json.dumps(libro))
        flash("Libro actualizado correctamente")
        return redirect('/')

    return render_template("editar.html", libro=libro)


# ELIMINAR LIBRO (CON CONFIRMACIÓN)
@app.route('/eliminar/<int:id>', methods=['GET','POST'])
def eliminar(id):
    clave_libro = clave(id)
    libro_json = r.get(clave_libro)

    if not libro_json:
        flash("Libro no encontrado")
        return redirect('/')

    libro = json.loads(libro_json)

    if request.method == 'POST':

        # CORREO ASÍNCRONO
        enviar_correo.delay(
            "Libro eliminado",
            "correo@ejemplo.com",
            f"Se eliminó el libro: {libro['titulo']}"
        )

        r.delete(clave_libro)
        flash("Libro eliminado correctamente")
        return redirect('/')

    return render_template("eliminar.html", libro=libro)


# BUSCAR LIBROS
@app.route('/buscar', methods=['GET','POST'])
def buscar():
    resultados = []

    if request.method == 'POST':
        valor = request.form['valor'].lower()

        for k in r.scan_iter("libro:*"):
            if k != "libro:id":
                libro = json.loads(r.get(k))

                if (valor in libro['titulo'].lower() or
                    valor in libro['autor'].lower() or
                    valor in libro['genero'].lower()):
                    
                    resultados.append(libro)

        if not resultados:
            flash("No se encontraron resultados")

    return render_template("buscar.html", libros=resultados)


# INICIAR APP
if __name__ == '__main__':
    app.run(debug=True)
