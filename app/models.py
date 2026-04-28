"""
SQLAlchemy Models — Bookstore Management System

Models:
    User  — system users (admin / customer)
    Book  — bookstore inventory
    Sale  — purchase records
"""

from datetime import datetime
from app import db
from config import ROLE_CUSTOMER


class User(db.Model):
    """
    System user.

    Roles:
        'admin'    — full access: book management, stats, reset
        'customer' — can browse & purchase books
    """
    __tablename__ = "users"

    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role     = db.Column(db.String(20), nullable=False, default=ROLE_CUSTOMER)

    def to_dict(self) -> dict:
        """Serialize to JSON-safe dict."""
        return {"id": self.id, "username": self.username, "role": self.role}


class Book(db.Model):
    """
    Book inventory item.

    Fields:
        title  — book title
        author — author name(s)
        price  — price in TRY
        image  — cover image URL
        stock  — current stock count
    """
    __tablename__ = "books"

    id     = db.Column(db.Integer, primary_key=True)
    title  = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    price  = db.Column(db.Float, nullable=False)
    image  = db.Column(db.String(300), default="")
    stock  = db.Column(db.Integer, nullable=False, default=0)

    def to_dict(self) -> dict:
        """Serialize to JSON-safe dict."""
        return {
            "id":     self.id,
            "title":  self.title,
            "author": self.author,
            "price":  self.price,
            "image":  self.image,
            "stock":  self.stock,
        }


class Sale(db.Model):
    """
    Purchase record.

    Constraints:
        book_id — FK → books.id (must exist)
        amount  — positive integer
        date    — auto-set to UTC now
    """
    __tablename__ = "sales"

    id      = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    amount  = db.Column(db.Integer, nullable=False)
    date    = db.Column(db.DateTime, default=datetime.utcnow)

    book = db.relationship("Book", backref="sales")

    def to_dict(self) -> dict:
        """Serialize to JSON-safe dict."""
        return {
            "id":         self.id,
            "book_id":    self.book_id,
            "book_title": self.book.title if self.book else "—",
            "amount":     self.amount,
            "date":       self.date.strftime("%Y-%m-%d %H:%M"),
        }
