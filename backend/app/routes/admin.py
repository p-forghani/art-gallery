from flask import Blueprint, jsonify, request, current_app
from app import mongo
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
import os
from werkzeug.utils import secure_filename
import logging
from flask_cors import cross_origin

logger = logging.getLogger(__name__)

admin_bp = Blueprint('admin', __name__)

# Configure upload folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@admin_bp.route('/upload', methods=['POST', 'OPTIONS'])
@cross_origin()
def upload_artwork():
    current_app.logger.info('Received upload request')
    current_app.logger.info(f'Request headers: {dict(request.headers)}')
    
    # Check JWT token before proceeding
    try:
        verify_jwt_in_request()
        current_user = get_jwt_identity()
        current_app.logger.info(f'Authenticated user: {current_user}')
    except Exception as e:
        current_app.logger.error(f'JWT Authentication failed: {str(e)}')
        return jsonify({'error': 'Authentication failed', 'details': str(e)}), 401

    current_app.logger.info(f'Request files: {request.files}')
    current_app.logger.info(f'Request form: {request.form}')
    
    if 'image' not in request.files:
        current_app.logger.error('No image part in request')
        return jsonify({'error': 'No image part in request'}), 400
    
    file = request.files['image']
    if file.filename == '':
        logger.error("No selected file")
        return jsonify({"error": "No selected file"}), 400
            
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        # Create uploads directory if it doesn't exist
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        
        # Save the file
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        logger.info(f"File saved to {file_path}")
        
        # Save artwork info to database
        artwork = {
            "title": request.form.get('name', filename),
            "description": request.form.get('description', ''),
            "price": float(request.form.get('price', 0)),
            "image_path": f"/uploads/{filename.replace(' ', '_')}",
            "artist_id": get_jwt_identity()
        }
        
        result = mongo.db.artworks.insert_one(artwork)
        logger.info(f"Successfully uploaded artwork with id: {result.inserted_id}")
        
        return jsonify({
            "message": "Artwork uploaded successfully",
            "artwork_id": str(result.inserted_id),
            "artwork": {
                **artwork,
                "_id": str(result.inserted_id)
            }
        }), 201
        
    logger.error("File type not allowed")
    return jsonify({"error": "File type not allowed"}), 400

@admin_bp.route('/artworks', methods=['GET'])
@cross_origin()
@jwt_required()
def get_artist_artworks():
    try:
        artist_id = get_jwt_identity()
        artworks = list(mongo.db.artworks.find({"artist_id": artist_id}))
        
        # Convert ObjectId to string for JSON serialization
        for artwork in artworks:
            artwork['_id'] = str(artwork['_id'])
            
        return jsonify(artworks), 200
        
    except Exception as e:
        logger.error(f"Error fetching artist artworks: {str(e)}")
        return jsonify({"error": "Failed to fetch artworks"}), 500
