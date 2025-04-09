from flask import Blueprint, send_from_directory, current_app
import os
from urllib.parse import unquote

static_bp = Blueprint('static', __name__)

@static_bp.route('/uploads/<path:filename>')
def serve_file(filename):
    # URL decode the filename to handle spaces and special characters
    filename = unquote(filename)
    uploads_dir = os.path.join(os.path.dirname(current_app.root_path), 'uploads')
    return send_from_directory(uploads_dir, filename) 