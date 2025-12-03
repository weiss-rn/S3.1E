from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_mysqldb import MySQL
import math
import os
from werkzeug.utils import secure_filename

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..'))
TEMPLATE_FOLDER = os.path.join(PROJECT_ROOT, 'templates')
STATIC_FOLDER = os.path.join(PROJECT_ROOT, 'static')

os.makedirs(TEMPLATE_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)

app = Flask(
    __name__,
    template_folder=TEMPLATE_FOLDER,
    static_folder=STATIC_FOLDER,
    static_url_path='/static'
)
app.secret_key = os.urandom(24)


# Config MySQL agar terhubung dengan Database
app.config['MYSQL_HOST'] = 'emma-temp-db-over-epycvps.tail88b018.ts.net'
app.config['MYSQL_USER'] = 'testuser'
app.config['MYSQL_PASSWORD'] = 'testpass'
app.config['MYSQL_DB'] = 'testdb'

mysql = MySQL(app)

# Config khusus untuk upload gambar
UPLOAD_FOLDER = os.path.join(STATIC_FOLDER, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def fetch_all_dict(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def fetch_one_dict(cursor):
    row = cursor.fetchone()
    if not row:
        return None
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))


# READ - Tampilkan semua data
@app.route('/')
def index():
    search_query = request.args.get('search', '').strip()
    try:
        page = max(int(request.args.get('page', 1)), 1)
    except ValueError:
        page = 1

    per_page = 9
    offset = (page - 1) * per_page

    cur = mysql.connection.cursor()
    try:
        # --- 1. Get TOTAL count for pagination ---
        count_query = "SELECT COUNT(*) FROM stok"
        count_params = []
        if search_query:
            count_query += " WHERE kode_sparepart LIKE %s OR nama_sparepart LIKE %s OR tipe_motor LIKE %s"
            search_term = f"%{search_query}%"
            count_params = [search_term, search_term, search_term]

        cur.execute(count_query, count_params)
        total_rows = cur.fetchone()[0]
        total_pages = max(math.ceil(total_rows / per_page), 1)

        # --- 2. Get DATA for the current page ---
        data_query = """
            SELECT id, kode_sparepart, nama_sparepart, harga, stok, tipe_motor, image
            FROM stok
        """
        data_params = []
        if search_query:
            data_query += " WHERE kode_sparepart LIKE %s OR nama_sparepart LIKE %s OR tipe_motor LIKE %s"
            data_params = [search_term, search_term, search_term]

        data_query += " ORDER BY id DESC LIMIT %s OFFSET %s"
        data_params.extend([per_page, offset])

        cur.execute(data_query, data_params)
        data = fetch_all_dict(cur)

        prices = [float(item.get('harga', 0)) for item in data] if data else []
        min_price = min(prices) if prices else 0
        max_price = max(prices) if prices else 0

        return render_template(
            'index.html',
            data=data,
            page=page,
            total_pages=total_pages,
            search=search_query,
            min_price=min_price,
            max_price=max_price
        )
    except Exception as e:
        flash(f"Error fetching data: {str(e)}", "error")
        return render_template(
            'index.html',
            data=[],
            page=1,
            total_pages=1,
            search=search_query,
            min_price=0,
            max_price=0
        )
    finally:
        cur.close()


# CREATE - Tambah data
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        kode = request.form.get('kode_sparepart', '').strip()
        nama = request.form.get('nama_sparepart', '').strip()
        harga = request.form.get('harga', '').strip()
        stok = request.form.get('stok', '').strip()
        tipe_motor = request.form.get('tipe_motor', '').strip()

        if not kode or not nama or not harga or not stok:
            flash("Kode, nama, harga, dan stok wajib diisi.", "error")
            return render_template('add.html')

        try:
            harga_val = float(harga)
        except ValueError:
            flash("Harga harus berupa angka.", "error")
            return render_template('add.html')

        try:
            stok_val = int(stok)
        except ValueError:
            flash("Stok harus berupa angka.", "error")
            return render_template('add.html')

        image_filename = None
        file = request.files.get('image')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = f"{kode}_{filename}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_filename = filename

        cur = mysql.connection.cursor()
        try:
            cur.execute(
                """
                INSERT INTO stok (kode_sparepart, nama_sparepart, harga, stok, tipe_motor, image)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (kode, nama, harga_val, stok_val, tipe_motor, image_filename)
            )
            mysql.connection.commit()
            flash("Spare part berhasil ditambahkan.", "success")
            return redirect(url_for('index'))
        except Exception as e:
            mysql.connection.rollback()
            flash(f"Error: {str(e)}", "error")
            return render_template('add.html')
        finally:
            cur.close()
    return render_template('add.html')


# UPDATE - Edit data
@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit(item_id):
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT * FROM stok WHERE id=%s", (item_id,))
        existing = fetch_one_dict(cur)

        if not existing:
            flash("Item tidak ditemukan.", "error")
            return redirect(url_for('index'))

        if request.method == 'POST':
            kode = request.form.get('kode_sparepart', '').strip()
            nama = request.form.get('nama_sparepart', '').strip()
            harga = request.form.get('harga', '').strip()
            stok = request.form.get('stok', '').strip()
            tipe_motor = request.form.get('tipe_motor', '').strip()

            if not kode or not nama or not harga or not stok:
                flash("Kode, nama, harga, dan stok wajib diisi.", "error")
                return render_template('edit.html', data=existing)

            try:
                harga_val = float(harga)
            except ValueError:
                flash("Harga harus berupa angka.", "error")
                return render_template('edit.html', data=existing)

            try:
                stok_val = int(stok)
            except ValueError:
                flash("Stok harus berupa angka.", "error")
                return render_template('edit.html', data=existing)

            image_filename = existing.get('image')
            file = request.files.get('image')
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = f"{kode}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                # delete old image if present and different
                if image_filename and image_filename != filename:
                    old_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
                    if os.path.exists(old_path):
                        os.remove(old_path)
                image_filename = filename

            cur.execute(
                """
                UPDATE stok
                SET kode_sparepart=%s, nama_sparepart=%s, harga=%s, stok=%s, tipe_motor=%s, image=%s
                WHERE id=%s
                """,
                (kode, nama, harga_val, stok_val, tipe_motor, image_filename, item_id)
            )
            mysql.connection.commit()
            flash("Data spare part berhasil diperbarui.", "success")
            return redirect(url_for('index'))

        return render_template('edit.html', data=existing)
    except Exception as e:
        mysql.connection.rollback()
        flash(f"Error: {str(e)}", "error")
        return redirect(url_for('index'))
    finally:
        cur.close()


# DELETE - Hapus data
@app.route('/delete/<int:item_id>', methods=['POST'])
def delete(item_id):
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT image FROM stok WHERE id=%s", (item_id,))
        row = cur.fetchone()
        image_filename = row[0] if row else None

        cur.execute("DELETE FROM stok WHERE id=%s", (item_id,))
        mysql.connection.commit()

        if image_filename:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            if os.path.exists(image_path):
                os.remove(image_path)

        flash("Item berhasil dihapus.", "success")
    except Exception as e:
        mysql.connection.rollback()
        flash(f"Error: {str(e)}", "error")
    finally:
        cur.close()
    return redirect(url_for('index'))


@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)
