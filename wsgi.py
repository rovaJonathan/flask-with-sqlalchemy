# pylint: disable=missing-docstring

from flask import Flask, abort, request
from config import Config
from flask_migrate import Migrate

BASE_URL = '/api/v1'

app = Flask(__name__)
app.config.from_object(Config)


from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

from models import Product
from schemas import many_product_schema, one_product_schema

migrate = Migrate(app, db)

@app.route('/hello', methods=['GET'])
def hello():
    return "Hello World!", 200

@app.route(f'{BASE_URL}/products', methods=['GET'])
def get_many_product():
    products = db.session.query(Product).all() # SQLAlchemy request => 'SELECT * FROM products'
    return many_product_schema.jsonify(products), 200

@app.route(f'{BASE_URL}/products/<int:id>')
def get_product(id):
    product = db.session.query(Product).get(id)
    if product is None:
        abort(404)
    return one_product_schema.jsonify(product), 200

@app.route(f'{BASE_URL}/products', methods=['POST'])
def create_product():
    payload = request.get_json()

    if payload is None:
        abort(400)

    name = payload.get('name')

    if name is None:
        abort(400)

    if name == '' or not isinstance(name, str):
        abort(422)

    product = Product()
    product.name = name

    db.session.add(product)
    db.session.commit()

    return one_product_schema.jsonify(product), 201

@app.route('/api/v1/products/<int:id_product>', methods=["DELETE"])
def delete_one_product(id_product):
    product = Product.query.filter_by(id=id_product).delete()

    if product is None:
        abort(404)
    
    db.session.commit()

    return '', 204

@app.route(f'/api/v1/products/<int:id>', methods=['PATCH'])
def update_product(id):
    data = request.get_json()
    if data is None:
        abort(400)

    name = data.get('name')

    if name is None:
        abort(400)

    if name == '' or not isinstance(name, str):
        abort(422)

    product = db.session.query(Product).get(id)

    if product is None:
        abort(404)

    product.name = name
    db.session.commit()

    return one_product_schema.jsonify(product), 200