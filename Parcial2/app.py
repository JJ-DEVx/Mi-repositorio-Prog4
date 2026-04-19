from flask import Flask, jsonify

app = Flask(__name__)


# DATOS DE VACUNACIÓN
# Datos simulados basados en el indicador del Banco Mundial (SH.IMM.MEAS)
# Representan el porcentaje de niños (12-23 meses) vacunados contra el sarampión aqui en Panamá
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


# ENDPOINT: GET /vacunas
# Devuelve todos los registros de vacunación disponibles
# Lista de objetos JSON con año y cobertura
@app.route('/vacunas', methods=['GET'])
def obtener_todos():
    return jsonify(vacunas), 200


# ENDPOINT: GET /vacunas/<anio>
# Descripción:
# Devuelve el registro de vacunación correspondiente a un año específico
# Parámetro:
# anio (int) → Año a consultar
# Respuesta:
# Objeto JSON con los datos o error si no existe
@app.route('/vacunas/<int:anio>', methods=['GET'])
def obtener_por_anio(anio):
    for v in vacunas:
        if v["anio"] == anio:
            return jsonify(v), 200
    return jsonify({"error": "Año no encontrado"}), 404


# ENDPOINT: GET /vacunas/provincia/<nombre>
# Descripción:
# Devuelve datos simulados de vacunación por provincia
# Nota:
# El Banco Mundial no provee datos por provincia, por lo que se simulan
# Parámetro:
# nombre (string) → Nombre de la provincia
# Respuesta:
# Lista de registros con provincia, año y cobertura
@app.route('/vacunas/provincia/<nombre>', methods=['GET'])
def por_provincia(nombre):
    resultado = []

    for v in vacunas:
        resultado.append({
            "provincia": nombre,
            "anio": v["anio"],
            "cobertura": v["cobertura"]
        })

    return jsonify(resultado), 200


# EJECUCIÓN PRINCIPAL
# Inicia el servidor Flask en modo desarrollo
if __name__ == '__main__':
    app.run(debug=True)
