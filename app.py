from flask import Flask, jsonify, request

app = Flask(__name__)

inventario = []

@app.route('/')
def inicio():
    return "API Inventario funcionando"

# GET
@app.route('/items', methods=['GET'])
def obtener_items():
    return jsonify(inventario)

# POST
@app.route('/items', methods=['POST'])
def agregar_item():
    data = request.json
    inventario.append(data)
    return jsonify(data)

# PUT
@app.route('/items/<int:id>', methods=['PUT'])
def actualizar_item(id):
    for item in inventario:
        if item['id'] == id:
            item.update(request.json)
            return jsonify(item)
    return {"error": "No encontrado"}

# DELETE
@app.route('/items/<int:id>', methods=['DELETE'])
def eliminar_item(id):
    global inventario
    inventario = [i for i in inventario if i['id'] != id]
    return {"mensaje": "Eliminado"}

app.run(debug=True)