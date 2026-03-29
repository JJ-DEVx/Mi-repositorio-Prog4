from flask import Flask, jsonify

app = Flask(__name__)

# Datos simulados (basados en Banco Mundial)
vacunas = [
    {"anio": 2000, "cobertura": 84},
    {"anio": 2001, "cobertura": 85},
    {"anio": 2002, "cobertura": 87},
    {"anio": 2003, "cobertura": 88},
    {"anio": 2004, "cobertura": 90},
    {"anio": 2005, "cobertura": 91},
    {"anio": 2006, "cobertura": 92},
    {"anio": 2007, "cobertura": 93},
    {"anio": 2008, "cobertura": 94},
    {"anio": 2009, "cobertura": 95},
    {"anio": 2010, "cobertura": 95},
    {"anio": 2011, "cobertura": 96},
    {"anio": 2012, "cobertura": 96},
    {"anio": 2013, "cobertura": 97},
    {"anio": 2014, "cobertura": 97},
    {"anio": 2015, "cobertura": 98},
    {"anio": 2016, "cobertura": 98},
    {"anio": 2017, "cobertura": 97},
    {"anio": 2018, "cobertura": 96},
    {"anio": 2019, "cobertura": 95}
]


# GET /vacunas
@app.route('/vacunas', methods=['GET'])
def obtener_todos():
    return jsonify(vacunas), 200


# GET /vacunas/<años>
@app.route('/vacunas/<int:anio>', methods=['GET'])
def obtener_por_anio(anio):
    for v in vacunas:
        if v["anio"] == anio:
            return jsonify(v), 200
    return jsonify({"error": "Año no encontrado"}), 404


# GET /vacunas/provincia/<nombre> (simulado)
@app.route('/vacunas/provincia/<nombre>', methods=['GET'])
def por_provincia(nombre):
    # Simulación (porque Banco Mundial no da provincias)
    resultado = []

    for v in vacunas:
        resultado.append({
            "provincia": nombre,
            "anio": v["anio"],
            "cobertura": v["cobertura"]
        })

    return jsonify(resultado), 200

# ==============================
if __name__ == '__main__':
    app.run(debug=True)
