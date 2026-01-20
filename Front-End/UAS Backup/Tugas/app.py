import os
import math
from contextlib import contextmanager
from flask import Flask, render_template, request, redirect, session, url_for, abort
import mysql.connector
from mysql.connector import pooling

app = Flask(__name__, template_folder="static/templates", static_folder="static")
app.secret_key = os.urandom(24)

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

_DB_CONFIG = {
    "host": "100.112.150.114",
    "user": "testuser",
    "password": "testpass",
    "database": "testdb",
}

_POOL = pooling.MySQLConnectionPool(
    pool_size=5,
    pool_reset_session=True,
    **_DB_CONFIG,
)

@contextmanager
def db_cursor(dictionary=True):
    conn = _POOL.get_connection()
    try:
        cur = conn.cursor(dictionary=dictionary)
        try:
            yield cur
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

if __name__ == '__main__':
    app.run(debug=True)
