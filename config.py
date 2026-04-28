"""
Configuration Settings — Bookstore Management System
"""

import os
from datetime import timedelta

# ─────────────────────────────────────────────────────────
#  ROLE CONSTANTS
# ─────────────────────────────────────────────────────────
ROLE_ADMIN    = "admin"
ROLE_CUSTOMER = "customer"

# ─────────────────────────────────────────────────────────
#  HTTP STATUS CODE CONSTANTS
# ─────────────────────────────────────────────────────────
HTTP_OK           = 200
HTTP_CREATED      = 201
HTTP_BAD_REQUEST  = 400
HTTP_UNAUTHORIZED = 401
HTTP_FORBIDDEN    = 403
HTTP_NOT_FOUND    = 404
HTTP_CONFLICT     = 409

# ─────────────────────────────────────────────────────────
#  JWT
# ─────────────────────────────────────────────────────────
JWT_TOKEN_EXPIRES_SEC = 3600  # 1 saat


# ─────────────────────────────────────────────────────────
#  FLASK CONFIG CLASSES
# ─────────────────────────────────────────────────────────
class Config:
    """Base configuration — shared across all environments."""

    SECRET_KEY    = os.environ.get("SECRET_KEY",  "bookstore-secret-2024-dev")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET", "jwt-bookstore-2024-dev")

    SQLALCHEMY_DATABASE_URI       = os.environ.get("DATABASE_URL", "sqlite:///bookstore.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=JWT_TOKEN_EXPIRES_SEC)


class DevelopmentConfig(Config):
    """Development — debug on, SQLite file."""
    DEBUG   = True
    TESTING = False


class ProductionConfig(Config):
    """Production — debug off."""
    DEBUG   = False
    TESTING = False


class TestingConfig(Config):
    """Testing — in-memory SQLite."""
    DEBUG   = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


def get_config(env: str = None) -> Config:
    """Return the appropriate Config class for the given environment name."""
    env = env or os.environ.get("FLASK_ENV", "development")
    return {
        "development": DevelopmentConfig,
        "production":  ProductionConfig,
        "testing":     TestingConfig,
    }.get(env, DevelopmentConfig)
