from flask import Blueprint, jsonify, request
from app import mongo
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

# Create blueprints
auth_bp = Blueprint('auth', __name__)
store_bp = Blueprint('store', __name__)
admin_bp = Blueprint('admin', __name__)

@auth_bp.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Server is working!"}), 200

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Check if user already exists
    if mongo.db.users.find_one({"email": data['email']}):
        return jsonify({"error": "Email already registered"}), 400
    
    # Create new user
    user = {
        "email": data['email'],
        "password": data['password'],  # In production, hash the password!
        "name": data['name']
    }
    mongo.db.users.insert_one(user)
    
    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = mongo.db.users.find_one({"email": data['email']})
    
    if user and user['password'] == data['password']:  # In production, verify hashed password!
        access_token = create_access_token(identity=str(user['_id']))
        return jsonify({"access_token": access_token}), 200
    
    return jsonify({"error": "Invalid credentials"}), 401 