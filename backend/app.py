from flask import Flask, jsonify,request
from flask_cors import CORS
from transformations.inutiles import eliminar_inutiles
from transformations.no_alcanzables import eliminar_no_alcanzables
from transformations.lambda_ import eliminar_lambda
from transformations.unitarias import eliminar_unitarias
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.get("/api/saludo")
def saludo():
    return jsonify({"mensaje": "Hola desde Flask!"})

@app.post("/api/procesar-gramatica")
def procesar_gramatica():
    data = request.get_json()

    variables = data["variables"]
    terminales = data["terminales"]
    inicial = data["inicial"]
    producciones_raw = data["producciones"]
    operacion = data["operacion"]  # "inutiles", "no-alcanzables", "lambda", "unitarias", "todas"

    # Normalizar producciones
    producciones = {
        v: [list(p.strip()) for p in producciones_raw[v].split("|") if p.strip()]
        for v in variables
    }

    gramatica = {
        "variables": variables,
        "terminales": terminales,
        "inicial": inicial,
        "producciones": producciones,
    }

    # Seleccionar operación
    if operacion == "inutiles":
        resultado = eliminar_inutiles(gramatica)

    elif operacion == "no-alcanzables":
        resultado = eliminar_no_alcanzables(gramatica)

    elif operacion == "lambda":
        resultado = eliminar_lambda(gramatica)

    elif operacion == "unitarias":
        resultado = eliminar_unitarias(gramatica)

    elif operacion == "todas":
        g = eliminar_inutiles(gramatica)
        g = eliminar_no_alcanzables(g)
        g = eliminar_lambda(g)
        g = eliminar_unitarias(g)
        resultado = g

    else:
        return jsonify({"error": "Operación no válida"}), 400

    return jsonify(resultado)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
