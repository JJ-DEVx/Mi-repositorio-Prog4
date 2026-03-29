from flask import Flask, render_template, request, redirect, flash
import requests

app = Flask(__name__)
app.secret_key = "clave123"

API_URL = "http://127.0.0.1:5001"

@app.route('/')
def index():
    try:
        res = requests.get(f"{API_URL}/books")
        libros = res.json()
    except:
        libros = []
        flash("Error con la API")

    return render_template("index.html", libros=libros)

@app.route('/agregar', methods=['GET','POST'])
def agregar():
    if request.method == 'POST':
        data = {
            "titulo": request.form['titulo'],
            "autor": request.form['autor'],
            "genero": request.form['genero'],
            "estado": request.form['estado']
        }

        requests.post(f"{API_URL}/books", json=data)
        flash("Libro agregado")
        return redirect('/')

    return render_template("agregar.html")

@app.route('/editar/<int:id>', methods=['GET','POST'])
def editar(id):

    if request.method == 'POST':
        data = {
            "titulo": request.form['titulo'],
            "autor": request.form['autor'],
            "genero": request.form['genero'],
            "estado": request.form['estado']
        }

        requests.put(f"{API_URL}/books/{id}", json=data)
        flash("Actualizado")
        return redirect('/')

    res = requests.get(f"{API_URL}/books/{id}")
    libro = res.json()

    return render_template("editar.html", libro=libro)

@app.route('/eliminar/<int:id>', methods=['GET','POST'])
def eliminar(id):

    if request.method == 'POST':
        requests.delete(f"{API_URL}/books/{id}")
        flash("Eliminado")
        return redirect('/')

    res = requests.get(f"{API_URL}/books/{id}")
    libro = res.json()

    return render_template("eliminar.html", libro=libro)

@app.route('/buscar', methods=['GET','POST'])
def buscar():
    resultados = []

    if request.method == 'POST':
        valor = request.form['valor'].lower()

        res = requests.get(f"{API_URL}/books")
        libros = res.json()

        for libro in libros:
            if (valor in libro['titulo'].lower() or
                valor in libro['autor'].lower() or
                valor in libro['genero'].lower()):
                resultados.append(libro)

    return render_template("buscar.html", libros=resultados)

if __name__ == '__main__':
    app.run(debug=True)