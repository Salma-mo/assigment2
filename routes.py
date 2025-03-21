from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User, Product, bcrypt
from datetime import timedelta

app = Blueprint('app', __name__)

#  User Registration
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(name=data['name'], username=data['username'], password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

# User Login with JWT (Token valid for 10 minutes)
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(minutes=10))
        return jsonify({'token': token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

#  Add a new product (Authentication required)
@app.route('/products', methods=['POST'])
@jwt_required()
def add_product():
    data = request.json
    new_product = Product(
        pname=data['pname'], description=data['description'],
        price=data['price'], stock=data['stock']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product added'}), 201

#  Get all products
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{'pid': p.pid, 'pname': p.pname, 'price': p.price} for p in products]), 200

#  Get a single product by ID
@app.route('/products/<int:pid>', methods=['GET'])
def get_product(pid):
    product = Product.query.get(pid)
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    return jsonify({'pid': product.pid, 'pname': product.pname, 'description': product.description, 'price': product.price, 'stock': product.stock}), 200

#  Update a product by ID (Authentication required)
@app.route('/products/<int:pid>', methods=['PUT'])
@jwt_required()
def update_product(pid):
    data = request.json
    product = Product.query.get(pid)

    if not product:
        return jsonify({'message': 'Product not found'}), 404

    product.pname = data.get('pname', product.pname)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.stock = data.get('stock', product.stock)

    db.session.commit()
    return jsonify({'message': 'Product updated'}), 200

#  Delete a product by ID (Authentication required)
@app.route('/products/<int:pid>', methods=['DELETE'])
@jwt_required()
def delete_product(pid):
    product = Product.query.get(pid)

    if not product:
        return jsonify({'message': 'Product not found'}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted'}), 200
