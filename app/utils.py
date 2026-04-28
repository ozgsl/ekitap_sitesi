"""
Utility Functions — Bookstore Management System

Includes:
    - validate_book_payload()       — validate POST/PUT body for books
    - validate_sale_request()       — validate purchase request
    - restore_initial_database_state() — wipe DB and re-seed with high-quality assets
"""

from werkzeug.security import generate_password_hash
from config import ROLE_ADMIN, ROLE_CUSTOMER

# ─────────────────────────────────────────────────────────
#  SEED DATA
# ─────────────────────────────────────────────────────────
INITIAL_USERS = [
    {"username": "admin", "password": "Admin123!", "role": ROLE_ADMIN},
    {"username": "alice", "password": "Alice123!", "role": ROLE_CUSTOMER},
    {"username": "bob",   "password": "Bob123!",   "role": ROLE_CUSTOMER},
]

INITIAL_BOOKS = [
    {"title": "Clean Code",                 "author": "Robert C. Martin", "price": 45.90, "stock": 20, "isbn": "9780132350884"},
    {"title": "The Pragmatic Programmer",   "author": "Hunt & Thomas",    "price": 52.00, "stock": 15, "isbn": "9780135957059"},
    {"title": "Design Patterns",            "author": "Gang of Four",     "price": 60.50, "stock": 10, "isbn": "9780201633610"},
    {"title": "Introduction to Algorithms", "author": "Cormen et al.",    "price": 89.99, "stock":  8, "isbn": "9780262033848"},
]


# ─────────────────────────────────────────────────────────
#  DATABASE RESET
# ─────────────────────────────────────────────────────────
def restore_initial_database_state() -> dict:
    """
    Wipe all data and re-seed the database to its initial state.
    Uses high-quality 'Large' covers from Open Library for the new UI.
    """
    # Import here to avoid circular imports at module load time
    from app import db
    from app.models import User, Book, Sale

    # FK kısıtlamaları nedeniyle önce satışları, sonra diğerlerini temizliyoruz
    Sale.query.delete()
    Book.query.delete()
    User.query.delete()
    db.session.commit()

    # Kullanıcıları ekle
    for u in INITIAL_USERS:
        db.session.add(User(
            username=u["username"],
            password=generate_password_hash(u["password"]),
            role=u["role"],
        ))

    # Kitapları yüksek kaliteli (L) kapak görselleriyle ekle
    for b in INITIAL_BOOKS:
        isbn      = b.get("isbn", "")
        # Yeni UI'da (2/3 aspect ratio) daha net görünmesi için 'L' boyutuna geçildi
        cover_url = f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg" if isbn else ""
        
        db.session.add(Book(
            title=b["title"],
            author=b["author"],
            price=b["price"],
            image=b.get("image") or cover_url,
            stock=b["stock"],
        ))

    db.session.commit()
    return {"users_count": len(INITIAL_USERS), "books_count": len(INITIAL_BOOKS)}


# ─────────────────────────────────────────────────────────
#  VALIDATION HELPERS
# ─────────────────────────────────────────────────────────
def validate_book_payload(data: dict) -> str | None:
    """Validate request body for book create/update."""
    for field in ("title", "author", "price", "stock"):
        if field not in data or not str(data[field]).strip():
            return f"Zorunlu alan eksik: {field}"

    try:
        price = float(data["price"])
        stock = int(data["stock"])
        if price < 0 or stock < 0:
            return "Fiyat ve stok negatif olamaz"
        if price > 999_999.99:
            return "Fiyat çok yüksek (max: 999999.99)"
    except (ValueError, TypeError):
        return "Fiyat sayı, stok tam sayı olmalıdır"

    return None


def validate_sale_request(book_id, amount) -> str | None:
    """Validate a purchase request."""
    if not book_id or not amount:
        return "book_id ve amount zorunlu"

    try:
        book_id = int(book_id)
        amount  = int(amount)
        if amount <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return "Miktar pozitif bir tam sayı olmalı"

    from app.models import Book
    book = Book.query.get(book_id)
    if not book:
        return f"Kitap (ID: {book_id}) bulunamadı"
    if book.stock < amount:
        return f"Yetersiz stok (mevcut: {book.stock}, istenen: {amount})"

    return None