"""
Page Routes (HTML views) — Bookstore Management System

Routes:
    GET /           → login page
    GET /dashboard  → main SPA dashboard
"""

from flask import Blueprint, render_template

views_blueprint = Blueprint("views", __name__)


@views_blueprint.route("/")
def index():
    """Render the login page."""
    return render_template("login.html")


@views_blueprint.route("/dashboard")
def dashboard():
    """Render the dashboard (auth guard handled client-side via JWT in localStorage)."""
    return render_template("dashboard.html")
