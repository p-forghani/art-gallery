from flask import Blueprint

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/test')
def admin_test():
    return {"message": "Admin works!"}
