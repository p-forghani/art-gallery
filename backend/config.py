### backend/config.py

class Config:
    # Security Key for Flask sessions
    SECRET_KEY = 'super-secret-key'

    # SQLite database file
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'

    # Disable overhead of tracking modifications
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Secret for JWT token encryption
    JWT_SECRET_KEY = 'your-jwt-secret-key'
