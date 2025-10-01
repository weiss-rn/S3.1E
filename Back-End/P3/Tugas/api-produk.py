import os
import json
from flask import Flask
app = Flask(__name__)

json_path = os.path.join(os.path.dirname(__file__), 'data.json')
with open(json_path, 'r') as f:
    data = json.load(f)

@app.route('/')
def show_user_greeting():
    return "Selamat Datang Di Produk UMKM"

@app.route('/produk/snack')
def show_item_greeting():
    return "Halaman Produk Semua Snack"

@app.route('/produk/Soft_drink')
def show_drink_greeting():
    return "Halaman Produk Soft Drink"

@app.route('/produk/snack/<int:id>')
def show_snack_id(id):
    return f"Halaman Produk Makanan dengan id == {id}"

@app.route('/produk/Soft_drink/<int:id>')
def show_drink_id(id):
    return f"Halaman Produk Minuman dengan id == {id}"

if __name__ == '__main__':
    app.run(debug=True)
