"""
Flask Application Factory — Bookstore Management System

Usage:
    from app import create_app
    app = create_app("development")
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

from config import get_config

# ─────────────────────────────────────────────────────────
#  Extensions — created here, bound to app in create_app()
# ─────────────────────────────────────────────────────────
db  = SQLAlchemy()
jwt = JWTManager()


def create_app(env: str = "development") -> Flask:
    app = Flask(__name__)
    app.config.from_object(get_config(env))

    db.init_app(app)
    jwt.init_app(app)

    # 1. Önce modelleri import et (Kritik!)
    from app.models import User, Book, Sale 

    # 2. Blueprint'leri kaydet
    from app.routes import api_blueprint
    app.register_blueprint(api_blueprint)
    from app.views import views_blueprint
    app.register_blueprint(views_blueprint)

    # 3. Tabloları oluştur ve veriyi yükle
    with app.app_context():
        db.create_all() # Artık User tablosunu biliyor
        if User.query.count() == 0:
            from app.utils import restore_initial_database_state
            restore_initial_database_state()

    return app
