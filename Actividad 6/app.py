from flask import Flask, render_template, request, redirect, url_for, flash
import redis
import json

app = Flask(__name__)
app.secret_key = "clave"

# Conexión a KeyDB/Redis
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

def clave(id):
    return f"libro:{id}"

@app.route('/')
def index():
    libros = []
    for k in r.scan_iter("libro:*"):
        if k != "libro:id":
            libros.append(json.loads(r.get(k)))
    return render_template("index.html", libros=libros)

@app.route('/agregar', methods=['GET','POST'])
def agregar():
    if request.method == 'POST':
        id_libro = r.incr("libro:id")
        libro = {
            "id": id_libro,
            "titulo": request.form['titulo'],
            "autor": request.form['autor'],
            "genero": request.form['genero'],
            "estado": request.form['estado']
        }
        r.set(clave(id_libro), json.dumps(libro))
        flash("Libro agregado")
        return redirect('/')
    return render_template("agregar.html")

@app.route('/eliminar/<int:id>')
def eliminar(id):
    r.delete(clave(id))
    flash("Libro eliminado")
    return redirect('/')

@app.route('/editar/<int:id>', methods=['GET','POST'])
def editar(id):
    libro = json.loads(r.get(clave(id)))
    if request.method == 'POST':
        libro['titulo'] = request.form['titulo']
        libro['autor'] = request.form['autor']
        libro['genero'] = request.form['genero']
        libro['estado'] = request.form['estado']
        r.set(clave(id), json.dumps(libro))
        flash("Libro actualizado")
        return redirect('/')
    return render_template("editar.html", libro=libro)

@app.route('/buscar', methods=['GET','POST'])
def buscar():
    resultados = []
    if request.method == 'POST':
        valor = request.form['valor'].lower()
        for k in r.scan_iter("libro:*"):
            if k != "libro:id":
                libro = json.loads(r.get(k))
                if valor in libro['titulo'].lower():
                    resultados.append(libro)
    return render_template("buscar.html", libros=resultados)

if __name__ == '__main__':
    app.run(debug=True)