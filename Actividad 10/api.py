from flask import Flask, request, jsonify

app = Flask(__name__)

libros = []
contador = 1

@app.route('/books', methods=['GET'])
def obtener_libros():
    return jsonify(libros), 200

@app.route('/books/<int:id>', methods=['GET'])
def obtener_libro(id):
    for libro in libros:
        if libro["id"] == id:
            return jsonify(libro), 200
    return jsonify({"error": "No encontrado"}), 404

@app.route('/books', methods=['POST'])
def agregar_libro():
    global contador
    data = request.json

    if not data.get("titulo") or not data.get("autor"):
        return jsonify({"error": "Datos inválidos"}), 400

    libro = {
        "id": contador,
        "titulo": data["titulo"],
        "autor": data["autor"],
        "genero": data.get("genero", ""),
        "estado": data.get("estado", "")
    }

    libros.append(libro)
    contador += 1

    return jsonify(libro), 201

@app.route('/books/<int:id>', methods=['PUT'])
def actualizar_libro(id):
    data = request.json

    for libro in libros:
        if libro["id"] == id:
            libro.update(data)
            return jsonify(libro), 200

    return jsonify({"error": "No encontrado"}), 404

@app.route('/books/<int:id>', methods=['DELETE'])
def eliminar_libro(id):
    global libros
    libros = [l for l in libros if l["id"] != id]
    return jsonify({"mensaje": "Eliminado"}), 200

if __name__ == '__main__':
    app.run(port=5001, debug=True)