from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventario.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    numeroSerie = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)

# Crear BD
with app.app_context():
    db.create_all()

# GET
@app.route('/items', methods=['GET'])
def obtener_items():
    items = Item.query.all()
    resultado = []
    for i in items:
        resultado.append({
            "id": i.id,
            "nombre": i.nombre,
            "numeroSerie": i.numeroSerie,
            "descripcion": i.descripcion
        })
    return jsonify(resultado)

# POST (con validación)
@app.route('/items', methods=['POST'])
def agregar_item():
    data = request.json

    if not data.get('nombre') or not data.get('numeroSerie') or not data.get('descripcion'):
        return {"error": "Todos los campos son obligatorios"}, 400

    nuevo = Item(
        nombre=data['nombre'],
        numeroSerie=data['numeroSerie'],
        descripcion=data['descripcion']
    )

    db.session.add(nuevo)
    db.session.commit()

    return {"mensaje": "Item agregado"}

# PUT
@app.route('/items/<int:id>', methods=['PUT'])
def actualizar_item(id):
    item = Item.query.get(id)
    if not item:
        return {"error": "No encontrado"}, 404

    data = request.json

    item.nombre = data.get('nombre', item.nombre)
    item.numeroSerie = data.get('numeroSerie', item.numeroSerie)
    item.descripcion = data.get('descripcion', item.descripcion)

    db.session.commit()
    return {"mensaje": "Actualizado"}

# DELETE
@app.route('/items/<int:id>', methods=['DELETE'])
def eliminar_item(id):
    item = Item.query.get(id)
    if not item:
        return {"error": "No encontrado"}, 404

    db.session.delete(item)
    db.session.commit()
    return {"mensaje": "Eliminado"}

app.run(debug=True)