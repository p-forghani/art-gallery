from flask import Blueprint, jsonify
from app import mongo
import logging

logger = logging.getLogger(__name__)

store_bp = Blueprint('store', __name__)

@store_bp.route('/artworks', methods=['GET'])
def get_artworks():
    try:
        artworks = list(mongo.db.artworks.find())
        
        # Convert ObjectId to string for JSON serialization
        for artwork in artworks:
            artwork['_id'] = str(artwork['_id'])
            logger.info(f"Artwork data: {artwork}")
            
        return jsonify(artworks), 200
        
    except Exception as e:
        logger.error(f"Error fetching artworks: {str(e)}")
        return jsonify({"error": "Failed to fetch artworks"}), 500

@store_bp.route('/artwork/<artwork_id>', methods=['GET'])
def get_artwork(artwork_id):
    try:
        from bson.objectid import ObjectId
        
        artwork = mongo.db.artworks.find_one({"_id": ObjectId(artwork_id)})
        if not artwork:
            return jsonify({"error": "Artwork not found"}), 404
            
        # Convert ObjectId to string for JSON serialization
        artwork['_id'] = str(artwork['_id'])
        
        return jsonify(artwork), 200
        
    except Exception as e:
        logger.error(f"Error fetching artwork: {str(e)}")
        return jsonify({"error": "Failed to fetch artwork"}), 500

@store_bp.route('/fix-paths', methods=['GET'])
def fix_image_paths():
    try:
        # Get all artworks
        artworks = list(mongo.db.artworks.find())
        
        for artwork in artworks:
            # Extract filename from various path formats
            image_path = artwork.get('image_path', artwork.get('image_url', ''))
            
            # Special case for the renamed file
            if 'final-fantasy-vii-rebirth-aerith-gainsborough-vc-2880x1800.jpg' in image_path:
                new_path = '/uploads/final-fantasy.jpg'
            else:
                if 'http://' in image_path:
                    filename = image_path.split('/')[-1]
                else:
                    filename = image_path.replace('/uploads/', '')
                new_path = f'/uploads/{filename}'
            
            # Update with normalized path
            mongo.db.artworks.update_one(
                {"_id": artwork["_id"]},
                {"$set": {"image_path": new_path}}
            )
            
            if 'image_url' in artwork:
                # Remove old image_url field
                mongo.db.artworks.update_one(
                    {"_id": artwork["_id"]},
                    {"$unset": {"image_url": ""}}
                )
        
        return jsonify({"message": "Updated all image paths"}), 200
        
    except Exception as e:
        logger.error(f"Error fixing image paths: {str(e)}")
        return jsonify({"error": "Failed to fix image paths"}), 500
