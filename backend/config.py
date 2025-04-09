import os
from dotenv import load_dotenv
import certifi

# Load environment variables from .env file
load_dotenv()

class Config:
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    
    # MongoDB settings
    MONGO_URI = 'mongodb+srv://alireza:ali1378reza1742@cluster0.ug6m1cu.mongodb.net/negar_studio?retryWrites=true&w=majority&appName=Cluster0&tlsAllowInvalidCertificates=true'
    
    # JWT settings
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'your-jwt-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour
