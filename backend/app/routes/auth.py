from flask import Blueprint, jsonify, request
from app import mongo
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Server is working!"}), 200

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        logger.info(f"Received registration request for email: {data.get('email')}")
        
        # Validate required fields
        required_fields = ['email', 'password', 'name']
        for field in required_fields:
            if not data.get(field):
                logger.error(f"Missing required field: {field}")
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Check if user already exists
        if mongo.db.users.find_one({"email": data['email']}):
            logger.warning(f"Email already registered: {data['email']}")
            return jsonify({"error": "Email already registered"}), 400
        
        # Create new user
        user = {
            "email": data['email'],
            "password": data['password'],  # In production, hash the password!
            "name": data['name']
        }
        
        result = mongo.db.users.insert_one(user)
        logger.info(f"Successfully registered user with id: {result.inserted_id}")
        
        # Generate access token
        access_token = create_access_token(identity=str(result.inserted_id))
        return jsonify({
            "message": "User registered successfully",
            "access_token": access_token
        }), 201
        
    except Exception as e:
        logger.error(f"Error during registration: {str(e)}")
        return jsonify({"error": "Registration failed"}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        logger.info(f"Received login request for email: {data.get('email')}")
        
        user = mongo.db.users.find_one({"email": data['email']})
        
        if user and user['password'] == data['password']:  # In production, verify hashed password!
            access_token = create_access_token(identity=str(user['_id']))
            logger.info(f"Successful login for user: {data['email']}")
            return jsonify({"access_token": access_token}), 200
        
        logger.warning(f"Failed login attempt for email: {data.get('email')}")
        return jsonify({"error": "Invalid credentials"}), 401
        
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        return jsonify({"error": "Login failed"}), 500
