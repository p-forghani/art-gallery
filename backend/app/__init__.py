# backend/app/__init__.py
from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config
import os

mongo = PyMongo()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Create uploads directory if it doesn't exist
    uploads_dir = os.path.join(os.path.dirname(app.root_path), 'uploads')
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)

    # Configure static folder after creating it
    app.static_folder = uploads_dir
    app.static_url_path = '/uploads'
    
    # Enable CORS with proper configuration for file uploads
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "allow_headers": ["Content-Type", "Authorization"],
            "methods": ["GET", "POST", "OPTIONS"]
        },
        r"/uploads/*": {  # Add CORS for static files
            "origins": "*",
            "methods": ["GET"]
        }
    })
    
    # Initialize extensions
    mongo.init_app(app)
    jwt.init_app(app)

    # Register blueprints with /api prefix
    from app.routes import auth_bp, store_bp, admin_bp, static_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(store_bp, url_prefix='/api/store')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(static_bp)  # No prefix for static files

    return app
