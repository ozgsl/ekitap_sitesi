"""
API Routes — Bookstore Management System

Enhanced Blueprint containing all API endpoints:
    POST   /api/auth/login      -> Authenticate user
    POST   /api/auth/register   -> New user registration (NEW!)
    GET    /api/books           -> List all books
    GET    /api/books/<id>      -> Detail of a book
    POST   /api/books           -> Create (Admin)
    PUT    /api/books/<id>      -> Update (Admin)
    DELETE /api/books/<id>      -> Remove (Admin)
    GET    /api/sales           -> Sales history (Admin)
    POST   /api/sales           -> Purchase book
    GET    /api/admin/stats     -> Dashboard statistics
    POST   /api/admin/reset     -> System reset
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt,
)
from werkzeug.security import check_password_hash, generate_password_hash

from config import (
    ROLE_ADMIN, ROLE_CUSTOMER,
    HTTP_OK, HTTP_CREATED,
    HTTP_BAD_REQUEST, HTTP_UNAUTHORIZED,
    HTTP_FORBIDDEN, HTTP_NOT_FOUND, HTTP_CONFLICT,
)

api_blueprint = Blueprint("api", __name__, url_prefix="/api")


# ─────────────────────────────────────────────────────────
#  SHARED HELPERS
# ─────────────────────────────────────────────────────────

def _require_admin():
    """Check JWT claims for admin role."""
    if get_jwt().get("role") != ROLE_ADMIN:
        return jsonify({"error": "Admin yetkisi gerekli"}), HTTP_FORBIDDEN
    return None


# ─────────────────────────────────────────────────────────
#  AUTH
# ─────────────────────────────────────────────────────────

@api_blueprint.route("/auth/register", methods=["POST"])
def register_user():
    """
    POST /api/auth/register
    Body: { "username": "newuser", "password": "Password123!" }
    """
    from app import db
    from app.models import User

    data = request.get_json(silent=True) or {}
    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return jsonify({"error": "Kullanıcı adı ve parola zorunlu"}), HTTP_BAD_REQUEST

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Bu kullanıcı adı zaten alınmış"}), HTTP_CONFLICT

    new_user = User(
        username=username,
        password=generate_password_hash(password),
        role=ROLE_CUSTOMER
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Kayıt başarılı, giriş yapabilirsiniz"}), HTTP_CREATED


@api_blueprint.route("/auth/login", methods=["POST"])
def authenticate_user():
    """POST /api/auth/login"""
    from app.models import User

    data     = request.get_json(silent=True) or {}
    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return jsonify({"error": "Kullanıcı adı ve parola zorunlu"}), HTTP_BAD_REQUEST

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Kullanıcı adı veya parola hatalı"}), HTTP_UNAUTHORIZED

    token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role, "username": user.username},
    )
    return jsonify({"token": token, "role": user.role, "username": user.username}), HTTP_OK


# ─────────────────────────────────────────────────────────
#  BOOKS
# ─────────────────────────────────────────────────────────

@api_blueprint.route("/books", methods=["GET"])
def list_all_books():
    """GET /api/books"""
    from app.models import Book
    books = Book.query.order_by(Book.title).all()
    return jsonify([b.to_dict() for b in books]), HTTP_OK


@api_blueprint.route("/books/<int:book_id>", methods=["GET"])
def retrieve_book_details(book_id):
    """GET /api/books/<id>"""
    from app.models import Book
    book = Book.query.get_or_404(book_id)
    return jsonify(book.to_dict()), HTTP_OK


@api_blueprint.route("/books", methods=["POST"])
@jwt_required()
def create_new_book():
    """POST /api/books (Admin)"""
    from app import db
    from app.models import Book
    from app.utils import validate_book_payload

    err = _require_admin()
    if err: return err

    data = request.get_json(silent=True) or {}
    msg  = validate_book_payload(data)
    if msg: return jsonify({"error": msg}), HTTP_BAD_REQUEST

    book = Book(
        title=data["title"].strip(),
        author=data["author"].strip(),
        price=float(data["price"]),
        image=data.get("image", "").strip(),
        stock=int(data["stock"]),
    )
    db.session.add(book)
    db.session.commit()
    return jsonify({"id": book.id, "message": "Kitap eklendi"}), HTTP_CREATED


@api_blueprint.route("/books/<int:book_id>", methods=["PUT"])
@jwt_required()
def update_existing_book(book_id):
    """PUT /api/books/<id> (Admin)"""
    from app import db
    from app.models import Book
    from app.utils import validate_book_payload

    err = _require_admin()
    if err: return err

    book = Book.query.get_or_404(book_id)
    data = request.get_json(silent=True) or {}
    msg  = validate_book_payload(data)
    if msg: return jsonify({"error": msg}), HTTP_BAD_REQUEST

    book.title  = data["title"].strip()
    book.author = data["author"].strip()
    book.price  = float(data["price"])
    book.stock  = int(data["stock"])
    book.image  = data.get("image", "").strip() or book.image
    db.session.commit()
    return jsonify({"message": "Kitap güncellendi"}), HTTP_OK


@api_blueprint.route("/books/<int:book_id>", methods=["DELETE"])
@jwt_required()
def remove_book(book_id):
    """DELETE /api/books/<id> (Admin)"""
    from app import db
    from app.models import Book

    err = _require_admin()
    if err: return err

    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Kitap silindi"}), HTTP_OK


# ─────────────────────────────────────────────────────────
#  SALES
# ─────────────────────────────────────────────────────────

@api_blueprint.route("/sales", methods=["GET"])
@jwt_required()
def list_all_sales():
    """GET /api/sales (Admin)"""
    from app.models import Sale
    err = _require_admin()
    if err: return err

    sales = Sale.query.order_by(Sale.date.desc()).all()
    return jsonify([s.to_dict() for s in sales]), HTTP_OK


@api_blueprint.route("/sales", methods=["POST"])
@jwt_required()
def record_purchase():
    """POST /api/sales"""
    from app import db
    from app.models import Book, Sale
    from app.utils import validate_sale_request

    data    = request.get_json(silent=True) or {}
    book_id = data.get("book_id")
    amount  = data.get("amount")

    msg = validate_sale_request(book_id, amount)
    if msg:
        if "bulunamadı" in msg: return jsonify({"error": msg}), HTTP_NOT_FOUND
        if "Yetersiz stok" in msg: return jsonify({"error": msg}), HTTP_CONFLICT
        return jsonify({"error": msg}), HTTP_BAD_REQUEST

    book = Book.query.get(int(book_id))
    book.stock -= int(amount)
    sale = Sale(book_id=int(book_id), amount=int(amount))
    db.session.add(sale)
    db.session.commit()
    return jsonify({"id": sale.id, "message": "Satış kaydedildi"}), HTTP_CREATED


# ─────────────────────────────────────────────────────────
#  ADMIN
# ─────────────────────────────────────────────────────────

@api_blueprint.route("/admin/reset", methods=["POST"])
@jwt_required()
def reset_database_to_initial_state():
    """POST /api/admin/reset (Admin)"""
    from app.utils import restore_initial_database_state
    err = _require_admin()
    if err: return err

    seeded = restore_initial_database_state()
    return jsonify({
        "status":  "success",
        "message": "Sistem sıfırlandı",
        "seeded":  seeded,
    }), HTTP_OK


@api_blueprint.route("/admin/stats", methods=["GET"])
@jwt_required()
def retrieve_admin_statistics():
    """GET /api/admin/stats (Admin)"""
    from app import db
    from app.models import User, Book, Sale
    err = _require_admin()
    if err: return err

    total_revenue = db.session.query(
        db.func.coalesce(db.func.sum(Sale.amount * Book.price), 0)
    ).join(Book, Sale.book_id == Book.id).scalar()

    return jsonify({
        "total_books":   Book.query.count(),
        "total_users":   User.query.count(),
        "total_sales":   Sale.query.count(),
        "total_revenue": round(float(total_revenue), 2),
    }), HTTP_OK