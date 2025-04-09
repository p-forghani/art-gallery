from flask import Blueprint
from app.routes.auth import auth_bp
from app.routes.admin import admin_bp
from app.routes.store import store_bp
from app.routes.static import static_bp

##from app.routes import auth_routes, admin_routes, store_routes  # noqa

__all__ = ['auth_bp', 'admin_bp', 'store_bp', 'static_bp']
