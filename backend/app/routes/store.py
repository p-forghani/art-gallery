from flask import Blueprint, jsonify
from app.models.art import Art

store_bp = Blueprint('store', __name__)

@store_bp.route('/', methods=['GET'])
def get_all_products():
    products = Art.query.order_by(Art.date_created.desc()).all()
    return jsonify([product.to_dict() for product in products])

@store_bp.route('/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    product = Art.query.get_or_404(product_id)
    return jsonify(product.to_dict())
