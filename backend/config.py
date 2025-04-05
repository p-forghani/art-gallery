# backend/config.py

class Config:
    SECRET_KEY = 'super-secret-key'
    JWT_SECRET_KEY = 'jwt-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
