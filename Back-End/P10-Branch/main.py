import math
import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

app = Flask(__name__, template_folder=TEMPLATE_DIR)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

MONGO_HOST = os.environ.get('MONGO_HOST', '100.121.179.108')
MONGO_PORT = os.environ.get('MONGO_PORT', '27017')
# MONGO_USER = os.environ.get('MONGO_USER', 'root')
# MONGO_PASS = os.environ.get('MONGO_PASS', 'rootpassword')
MONGO_DB = os.environ.get('MONGO_DB', 'testdb')
MONGO_COLLECTION = os.environ.get('MONGO_COLLECTION', 'stok')

MONGO_URI = os.environ.get(
    'MONGO_URI',
    # f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"
    f"mongodb://{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"
)

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def format_row_for_index(doc):
    """Return a tuple shaped for the index template."""
    stok = doc.get('stok')
    if stok is None:
        stok = doc.get('jumlah', 0)
    return (
        str(doc.get('_id')),
        doc.get('kode', ''),
        doc.get('nama', ''),
        doc.get('harga', 0),
        stok,
        doc.get('tipe_motor', ''),
        doc.get('image'),
        doc.get('description', '')
    )


def format_row_for_edit(doc):
    """Return a tuple shaped for the edit template."""
    stok = doc.get('stok')
    if stok is None:
        stok = doc.get('jumlah', 0)
    return (
        str(doc.get('_id')),
        doc.get('kode', ''),
        doc.get('nama', ''),
        doc.get('harga', 0),
        doc.get('image'),
        stok,
        doc.get('tipe_motor', ''),
        doc.get('description', '')
    )


def format_doc_for_detail(doc: dict) -> dict:
    stok = doc.get('stok')
    if stok is None:
        stok = doc.get('jumlah', 0)
    return {
        'id': str(doc.get('_id')),
        'kode': doc.get('kode', ''),
        'nama': doc.get('nama', ''),
        'harga': doc.get('harga', 0),
        'stok': stok,
        'tipe_motor': doc.get('tipe_motor', ''),
        'description': doc.get('description', ''),
        'image': doc.get('image'),
    }


@app.route('/')
def index():
    search_query = request.args.get('search', '').strip()
    try:
        page = max(int(request.args.get('page', 1)), 1)
    except (TypeError, ValueError):
        page = 1
    per_page = 5
    offset = (page - 1) * per_page

    filter_query = {}
    if search_query:
        regex = {'$regex': search_query, '$options': 'i'}
        or_clauses = [
            {'kode': regex},
            {'nama': regex},
            {'tipe_motor': regex},
            {'description': regex},
        ]
        try:
            or_clauses.append({'harga': float(search_query)})
        except ValueError:
            pass
        try:
            stok_value = int(search_query)
            or_clauses.extend([{'stok': stok_value}, {'jumlah': stok_value}])
        except ValueError:
            pass
        filter_query = {'$or': or_clauses}

    total_rows = collection.count_documents(filter_query)
    total_pages = max(1, math.ceil(total_rows / per_page)) if total_rows else 1
    cursor = collection.find(filter_query).skip(offset).limit(per_page)
    data = [format_row_for_index(doc) for doc in cursor]

    return render_template(
        'index.html',
        data=data,
        page=page,
        total_pages=total_pages,
        search=search_query
    )


@app.route('/detail/<id>')
def detail(id):
    try:
        obj_id = ObjectId(id)
    except Exception:
        flash("Invalid item ID.", "danger")
        return redirect(url_for('index'))

    doc = collection.find_one({'_id': obj_id})
    if not doc:
        flash("Item not found!", "danger")
        return redirect(url_for('index'))

    item = format_doc_for_detail(doc)
    return render_template('detail.html', item=item)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        kode = request.form.get('kode', '').strip()
        nama = request.form.get('nama', '').strip()
        harga_raw = request.form.get('harga', '').strip()
        stok_raw = request.form.get('stok', '').strip()
        tipe_motor = request.form.get('tipe_motor', '').strip()
        description = request.form.get('description', '').strip()

        if not kode or not nama or not harga_raw:
            flash("All required fields must be filled.", "danger")
            return render_template('add.html')

        try:
            harga = float(harga_raw)
        except ValueError:
            flash("Harga must be a number.", "danger")
            return render_template('add.html')

        stok = 0
        if stok_raw:
            try:
                stok = int(stok_raw)
            except ValueError:
                flash("Stok must be an integer.", "danger")
                return render_template('add.html')

        image_filename = None
        file = request.files.get('image')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = f"{kode}_{filename}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_filename = filename

        doc = {
            'kode': kode,
            'nama': nama,
            'harga': harga,
            'stok': stok,
            'jumlah': stok,
            'tipe_motor': tipe_motor,
            'description': description,
            'image': image_filename
        }

        collection.insert_one(doc)
        flash("Item added successfully!", "success")
        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    try:
        obj_id = ObjectId(id)
    except Exception:
        flash("Invalid item ID.", "danger")
        return redirect(url_for('index'))

    doc = collection.find_one({'_id': obj_id})
    if not doc:
        flash("Item not found!", "danger")
        return redirect(url_for('index'))

    if request.method == 'POST':
        kode_input = request.form.get('kode', '').strip()
        kode_original = doc.get('kode', '').strip()
        nama = request.form.get('nama', '').strip()
        harga_raw = request.form.get('harga', '').strip()
        stok_raw = request.form.get('stok', '').strip()
        tipe_motor = request.form.get('tipe_motor', '').strip()
        description = request.form.get('description', '').strip()

        if not kode_original or not nama or not harga_raw:
            flash("All required fields must be filled.", "danger")
            data = format_row_for_edit(doc)
            return render_template('edit.html', data=data)

        try:
            harga = float(harga_raw)
        except ValueError:
            flash("Harga must be a number.", "danger")
            data = format_row_for_edit(doc)
            return render_template('edit.html', data=data)

        if kode_input and kode_input != kode_original:
            flash("Kode tidak dapat diubah dan tetap menggunakan nilai awal.", "warning")

        stok = 0
        if stok_raw:
            try:
                stok = int(stok_raw)
            except ValueError:
                flash("Stok must be an integer.", "danger")
                data = format_row_for_edit(doc)
                return render_template('edit.html', data=data)

        image_filename = doc.get('image')
        file = request.files.get('image')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = f"{kode_original}_{filename}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_filename = filename

            old_image = doc.get('image')
            if old_image:
                old_path = os.path.join(app.config['UPLOAD_FOLDER'], old_image)
                if os.path.exists(old_path) and old_path != new_image_path:
                    try:
                        os.remove(old_path)
                    except OSError:
                        pass

        collection.update_one(
            {'_id': obj_id},
            {'$set': {
                'nama': nama,
                'harga': harga,
                'stok': stok,
                'jumlah': stok,
                'tipe_motor': tipe_motor,
                'description': description,
                'image': image_filename
            }}
        )
        flash("Item updated successfully!", "success")
        return redirect(url_for('index'))

    data = format_row_for_edit(doc)
    return render_template('edit.html', data=data)


@app.route('/delete/<id>', methods=['GET'])
def delete(id):
    try:
        obj_id = ObjectId(id)
    except Exception:
        flash("Invalid item ID.", "danger")
        return redirect(url_for('index'))

    doc = collection.find_one({'_id': obj_id})
    if not doc:
        flash("Item not found!", "danger")
        return redirect(url_for('index'))

    image_filename = doc.get('image')
    if image_filename:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
        if os.path.exists(image_path):
            try:
                os.remove(image_path)
            except OSError:
                pass

    collection.delete_one({'_id': obj_id})
    flash("Item deleted successfully!", "success")
    return redirect(url_for('index'))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)
