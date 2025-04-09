from flask import jsonify, request
from flask_jwt_extended import (create_access_token, get_jwt_identity,
                                jwt_required)

from backend.app import db
from backend.app.models.user import User
from backend.app.routes import auth_bp
from backend.app.schemas.user_schema import UserSchema


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    schema = UserSchema()
    # Validate the input data
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400
    # Check if the user already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "User already exists"}), 409

    new_user = User(
        name=data['name'],
        email=data['email'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Registered"}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    schema = UserSchema(only=('email', 'password'))
    # Validate the input data
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400
    # Check if the user exists and verify the password
    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify({"message": "Invalid credentials"}), 401


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify(user.to_dict())
