import os
from flask import Flask, render_template, request, redirect, session, url_for, abort
import mysql.connector

app = Flask(__name__, template_folder="static/templates", static_folder="static")
app.secret_key = os.urandom(24)

db = mysql.connector.connect(
    host="100.92.101.16",
    user="testuser",
    password="testpass",
    database="testdb"
)

cursor = db.cursor(dictionary=True)

@app.route('/')
def index():
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    return render_template('index.html', products=products)

@app.route('/product/<int:id>')
def product_data(id):
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
    cursor.execute(f"SELECT * FROM products WHERE id IN ({placeholders})", tuple(product_ids))
    products = cursor.fetchall()
    return render_template('checkout.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)
