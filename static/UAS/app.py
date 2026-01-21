import os
import math
from contextlib import contextmanager
from threading import Lock
from uuid import uuid4
from flask import Flask, render_template, request, redirect, session, url_for, abort, flash
import mysql.connector
from mysql.connector import pooling
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder="static/templates", static_folder="static")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")
app.config["ADMIN_USERNAME"] = os.environ.get("ADMIN_USERNAME", "admin")
app.config["ADMIN_PASSWORD"] = os.environ.get("ADMIN_PASSWORD", "admin123")

CATEGORIES = [
    {"slug": "semua", "label": "Semua", "icon": "fa-boxes"},
    {"slug": "oli", "label": "Oli", "icon": "fa-oil-can"},
    {"slug": "rem", "label": "Rem", "icon": "fa-circle-stop"},
    {"slug": "ban", "label": "Ban", "icon": "fa-circle"},
    {"slug": "mesin", "label": "Mesin", "icon": "fa-cog"},
    {"slug": "kelistrikan", "label": "Kelistrikan", "icon": "fa-bolt"},
    {"slug": "rantai", "label": "Rantai", "icon": "fa-link"},
]

CATEGORY_BY_SLUG = {item["slug"]: item for item in CATEGORIES}
CATEGORY_LABELS = {item["slug"]: item["label"] for item in CATEGORIES}
PRODUCT_CATEGORIES = [item for item in CATEGORIES if item["slug"] != "semua"]
DEFAULT_CATEGORY = PRODUCT_CATEGORIES[0]["slug"] if PRODUCT_CATEGORIES else "semua"

UPLOAD_FOLDER = os.path.join(app.static_folder, "img")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

_DB_CONFIG = {
    "host": "emma-temp-db-over-epycvps.tail88b018.ts.net",
    "user": "testuser",
    "password": "testpass",
    "database": "testdb",
}

_POOL = None
_POOL_LOCK = Lock()

def _get_pool():
    global _POOL
    if _POOL is not None:
        return _POOL
    with _POOL_LOCK:
        if _POOL is None:
            _POOL = pooling.MySQLConnectionPool(
                pool_size=5,
                pool_reset_session=True,
                **_DB_CONFIG,
            )
    return _POOL

@contextmanager
def db_cursor(dictionary=True, commit=False):
    conn = _get_pool().get_connection()
    try:
        cur = conn.cursor(dictionary=dictionary)
        try:
            yield cur
            if commit:
                conn.commit()
        except Exception:
            if commit:
                conn.rollback()
            raise
        finally:
            cur.close()
            conn.close()
    except Exception:
        try:
            conn.close()
        except Exception:
            pass
        raise

@app.context_processor
def inject_catalog_context():
    return {"categories": CATEGORIES, "category_labels": CATEGORY_LABELS}

@app.template_global()
def url_for_params(endpoint, params=None, **kwargs):
    merged = {}
    if params:
        merged.update(params)
    merged.update(kwargs)
    return url_for(endpoint, **merged)

def _parse_positive_int(value, default=1):
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    return parsed if parsed > 0 else default

def _is_admin_authenticated():
    return session.get("is_admin") is True

def _normalize_category(value):
    normalized = (value or "").strip().lower()
    if normalized in CATEGORY_BY_SLUG and normalized != "semua":
        return normalized
    return None

def _allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def _store_uploaded_image(file_storage):
    if not file_storage or not file_storage.filename:
        return None, None

    filename = secure_filename(file_storage.filename)
    if not filename:
        return None, "Nama file gambar tidak valid."
    if not _allowed_file(filename):
        return None, "Format gambar harus png, jpg, jpeg, gif, atau webp."

    unique_name = f"{uuid4().hex}_{filename}"
    file_storage.save(os.path.join(UPLOAD_FOLDER, unique_name))
    return unique_name, None

def _get_product(product_id):
    with db_cursor() as cursor:
        cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        return cursor.fetchone()

@app.before_request
def _require_admin_login():
    if not request.path.startswith("/admin"):
        return None
    normalized_path = request.path.rstrip("/") or "/"
    if normalized_path in ("/admin/login", "/admin/logout"):
        return None
    if _is_admin_authenticated():
        return None
    next_url = request.full_path
    if next_url.endswith("?"):
        next_url = next_url[:-1]
    session["admin_next"] = next_url
    return redirect(url_for("admin_login", next=next_url))

def _fetch_products_page(search_query, category_slug, page, per_page):
    clauses = []
    params = []

    if category_slug and category_slug != "semua":
        clauses.append("category = %s")
        params.append(category_slug)

    if search_query:
        like = f"%{search_query}%"

        category_match = None
        normalized = search_query.strip().lower()
        if normalized:
            if normalized in CATEGORY_BY_SLUG:
                category_match = normalized
            else:
                for slug, label in CATEGORY_LABELS.items():
                    if normalized == label.lower():
                        category_match = slug
                        break

        if category_match and category_match != "semua":
            clauses.append("(name LIKE %s OR category = %s)")
            params.extend([like, category_match])
        else:
            clauses.append("name LIKE %s")
            params.append(like)

    where_sql = (" WHERE " + " AND ".join(clauses)) if clauses else ""

    with db_cursor() as cursor:
        cursor.execute("SELECT COUNT(*) AS total FROM products" + where_sql, tuple(params))
        total = (cursor.fetchone() or {}).get("total") or 0

        total_pages = max(1, math.ceil(total / per_page)) if total else 1
        page = min(max(1, page), total_pages)
        offset = (page - 1) * per_page

        cursor.execute(
            "SELECT * FROM products" + where_sql + " ORDER BY id DESC LIMIT %s OFFSET %s",
            tuple(params + [per_page, offset]),
        )
        products = cursor.fetchall()

    return {
        "products": products,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages,
        "q": search_query,
    }

@app.route('/')
def index():
    q = (request.args.get("q") or "").strip()
    page = _parse_positive_int(request.args.get("page"), default=1)
    paging = _fetch_products_page(q, "semua", page, per_page=9)
    return render_template(
        "index.html",
        endpoint="index",
        url_params={},
        active_category="semua",
        **paging,
    )

@app.route('/produk')
def products():
    q = (request.args.get("q") or "").strip()
    page = _parse_positive_int(request.args.get("page"), default=1)
    paging = _fetch_products_page(q, "semua", page, per_page=9)
    return render_template(
        "index.html",
        endpoint="products",
        url_params={},
        active_category="semua",
        **paging,
    )

@app.route('/kategori/<slug>')
def category(slug):
    if slug not in CATEGORY_BY_SLUG:
        abort(404)

    q = (request.args.get("q") or "").strip()
    page = _parse_positive_int(request.args.get("page"), default=1)
    paging = _fetch_products_page(q, slug, page, per_page=9)
    return render_template(
        "index.html",
        endpoint="category",
        url_params={"slug": slug},
        active_category=slug,
        **paging,
    )

@app.route('/product/<int:id>')
def product_data(id):
    with db_cursor() as cursor:
        cursor.execute("SELECT * FROM products WHERE id = %s", (id,))
        product = cursor.fetchone()
    if not product:
        abort(404)
    return render_template('product_detail.html', product=product)

@app.route('/add_to_cart/<int:id>')
def add_to_cart(id):
    if "cart" not in session:
        session["cart"] = []
    session["cart"].append(id)
    session.modified = True
    return redirect(request.referrer or url_for('index'))

@app.route('/cart')
def cart():
    if "cart" not in session:
        session["cart"] = []

    cart_items = []
    with db_cursor() as cursor:
        for pid in session["cart"]:
            cursor.execute("SELECT * FROM products WHERE id = %s", (pid,))
            product = cursor.fetchone()
            if product:
                cart_items.append(product)
    return render_template('cart.html', cart_items=cart_items)

@app.route('/checkout')
def checkout():
    product_ids = session.get("cart", [])
    if not product_ids:
        return render_template('checkout.html', products=[])

    placeholders = ", ".join(["%s"] * len(product_ids))
    with db_cursor() as cursor:
        cursor.execute(f"SELECT * FROM products WHERE id IN ({placeholders})", tuple(product_ids))
        products = cursor.fetchall()
    return render_template('checkout.html', products=products)

@app.route('/admin', strict_slashes=False)
def admin_root():
    return redirect(url_for('admin_products'))

@app.route('/admin/login', methods=['GET', 'POST'], strict_slashes=False)
def admin_login():
    next_url = (
        request.args.get("next")
        or request.form.get("next")
        or session.get("admin_next")
        or url_for("admin_products")
    )
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""
        if (
            username == app.config["ADMIN_USERNAME"]
            and password == app.config["ADMIN_PASSWORD"]
        ):
            session["is_admin"] = True
            session.pop("admin_next", None)
            flash("Login berhasil.", "success")
            return redirect(url_for("admin_products"))
        flash("Username atau password salah.", "danger")
    return render_template("admin_login.html", next_url=next_url)

@app.route('/admin/logout', strict_slashes=False)
def admin_logout():
    session.pop("is_admin", None)
    flash("Anda telah keluar.", "success")
    return redirect(url_for("admin_login"))

@app.route('/admin/products', strict_slashes=False)
def admin_products():
    q = (request.args.get("q") or "").strip()
    category = (request.args.get("category") or "semua").strip().lower()
    if category not in CATEGORY_BY_SLUG:
        category = "semua"
    page = _parse_positive_int(request.args.get("page"), default=1)
    paging = _fetch_products_page(q, category, page, per_page=10)
    return render_template(
        "admin_products.html",
        active_category=category,
        product_categories=PRODUCT_CATEGORIES,
        **paging,
    )

@app.route('/admin/products/add', methods=['GET', 'POST'], strict_slashes=False)
def admin_add_product():
    form_data = None
    if request.method == 'POST':
        form_data = {
            "name": (request.form.get("name") or "").strip(),
            "category": (request.form.get("category") or "").strip().lower(),
            "price": (request.form.get("price") or "").strip(),
            "description": (request.form.get("description") or "").strip(),
            "image": (request.form.get("image") or "").strip(),
        }

        errors = []
        if not form_data["name"]:
            errors.append("Nama produk wajib diisi.")

        category = _normalize_category(form_data["category"])
        if not category:
            errors.append("Kategori wajib dipilih.")

        try:
            price = float(form_data["price"])
            if price < 0:
                raise ValueError
        except ValueError:
            errors.append("Harga harus berupa angka.")
            price = 0

        description = form_data["description"] or None
        image_name = form_data["image"] or None

        uploaded_name, upload_error = _store_uploaded_image(request.files.get("image_file"))
        if upload_error:
            errors.append(upload_error)

        if errors:
            for error in errors:
                flash(error, "danger")
            return render_template(
                "admin_form.html",
                page_title="Tambah Produk",
                page_subtitle="Isi detail produk baru untuk katalog.",
                submit_label="Simpan",
                product=None,
                form_data=form_data,
                product_categories=PRODUCT_CATEGORIES,
                default_category=DEFAULT_CATEGORY,
            )

        image = uploaded_name or image_name

        with db_cursor(commit=True) as cursor:
            cursor.execute(
                "INSERT INTO products (name, category, description, price, image) VALUES (%s, %s, %s, %s, %s)",
                (form_data["name"], category, description, price, image),
            )

        flash("Produk berhasil ditambahkan.", "success")
        return redirect(url_for('admin_products'))

    return render_template(
        "admin_form.html",
        page_title="Tambah Produk",
        page_subtitle="Isi detail produk baru untuk katalog.",
        submit_label="Simpan",
        product=None,
        form_data=form_data,
        product_categories=PRODUCT_CATEGORIES,
        default_category=DEFAULT_CATEGORY,
    )

@app.route('/admin/products/<int:product_id>/edit', methods=['GET', 'POST'], strict_slashes=False)
def admin_edit_product(product_id):
    product = _get_product(product_id)
    if not product:
        abort(404)

    form_data = None
    if request.method == 'POST':
        form_data = {
            "name": (request.form.get("name") or "").strip(),
            "category": (request.form.get("category") or "").strip().lower(),
            "price": (request.form.get("price") or "").strip(),
            "description": (request.form.get("description") or "").strip(),
            "image": (request.form.get("image") or "").strip(),
        }

        errors = []
        if not form_data["name"]:
            errors.append("Nama produk wajib diisi.")

        category = _normalize_category(form_data["category"])
        if not category:
            errors.append("Kategori wajib dipilih.")

        try:
            price = float(form_data["price"])
            if price < 0:
                raise ValueError
        except ValueError:
            errors.append("Harga harus berupa angka.")
            price = 0

        description = form_data["description"] or None
        image_name = form_data["image"] or None

        uploaded_name, upload_error = _store_uploaded_image(request.files.get("image_file"))
        if upload_error:
            errors.append(upload_error)

        if errors:
            for error in errors:
                flash(error, "danger")
            return render_template(
                "admin_form.html",
                page_title="Edit Produk",
                page_subtitle="Perbarui data produk yang sudah ada.",
                submit_label="Perbarui",
                product=product,
                form_data=form_data,
                product_categories=PRODUCT_CATEGORIES,
                default_category=DEFAULT_CATEGORY,
            )

        image = uploaded_name or image_name or product.get("image")

        with db_cursor(commit=True) as cursor:
            cursor.execute(
                "UPDATE products SET name = %s, category = %s, description = %s, price = %s, image = %s WHERE id = %s",
                (form_data["name"], category, description, price, image, product_id),
            )

        flash("Produk berhasil diperbarui.", "success")
        return redirect(url_for('admin_products'))

    return render_template(
        "admin_form.html",
        page_title="Edit Produk",
        page_subtitle="Perbarui data produk yang sudah ada.",
        submit_label="Perbarui",
        product=product,
        form_data=form_data,
        product_categories=PRODUCT_CATEGORIES,
        default_category=DEFAULT_CATEGORY,
    )

@app.route('/admin/products/<int:product_id>/delete', methods=['POST'], strict_slashes=False)
def admin_delete_product(product_id):
    with db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
        deleted = cursor.rowcount

    if deleted:
        flash("Produk berhasil dihapus.", "success")
    else:
        flash("Produk tidak ditemukan.", "warning")
    return redirect(url_for('admin_products'))

if __name__ == '__main__':
    app.run(debug=True)
