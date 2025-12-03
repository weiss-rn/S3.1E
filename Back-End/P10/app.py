import os
import secrets
from flask import Flask, render_template, redirect, url_for, request, abort, session
from flask_bootstrap import Bootstrap
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

MONGO_HOST = "100.74.35.6"
MONGO_PORT = "27017"
MONGO_USER = "root"
MONGO_PASS = "rootpassword"
MONGO_DB = "testdb"
MONGO_COLLECTION = "mycollection"

# client = MongoClient("mongodb://localhost:27017") - Localhost
# client = MongoClient(f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}")
client = MongoClient(f"mongodb://100.103.170.96:27017/testdb")


db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]


def get_csrf_token():
    token = session.get('csrf_token')
    if not token:
        token = secrets.token_hex(16)
        session['csrf_token'] = token
    return token


def validate_csrf(token):
    session_token = session.get('csrf_token')
    if not session_token or token != session_token:
        abort(400, "Invalid CSRF token.")


def parse_numeric(form_value, field_name, cast_type):
    try:
        value = cast_type(form_value)
    except (TypeError, ValueError):
        abort(400, f"{field_name} must be a number.")
    if value < 0:
        abort(400, f"{field_name} must not be negative.")
    return value

@app.route('/')
def index():
    items = collection.find()
    return render_template('index.html', items=items, csrf_token=get_csrf_token())

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        validate_csrf(request.form.get('csrf_token'))
        kode = request.form['kode']
        nama = request.form['nama']
        harga = parse_numeric(request.form.get('harga'), "Harga", float)
        jumlah = parse_numeric(request.form.get('jumlah'), "Jumlah", int)
        collection.insert_one({'kode': kode, 'nama': nama, 'harga': harga, 'jumlah': jumlah})
        return redirect(url_for('index'))
    return render_template('add.html', csrf_token=get_csrf_token())

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    item = collection.find_one({'_id': ObjectId(id)})
    if request.method == 'POST':
        validate_csrf(request.form.get('csrf_token'))
        kode = request.form['kode']
        nama = request.form['nama']
        harga = parse_numeric(request.form.get('harga'), "Harga", float)
        jumlah = parse_numeric(request.form.get('jumlah'), "Jumlah", int)
        collection.update_one({'_id': ObjectId(id)}, {'$set': {'kode': kode, 'nama': nama, 'harga': harga, 'jumlah': jumlah}})
        return redirect(url_for('index'))
    return render_template('edit.html', item=item, csrf_token=get_csrf_token())

@app.route('/delete/<id>', methods=['POST'])
def delete(id):
    validate_csrf(request.form.get('csrf_token'))
    collection.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
