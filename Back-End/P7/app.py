from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from flask_mysqldb import MySQL
import os
import math
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.urandom(24) 


# Cofig MySQL Agar terhubung dengan Database
app.config['MYSQL_HOST'] = '100.117.130.109'
app.config['MYSQL_USER'] = 'testuser'
app.config['MYSQL_PASSWORD'] = 'testpass'
app.config['MYSQL_DB'] = 'testdb'

mysql = MySQL(app)

# Config khusus untuk upload gambar
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# READ - Tampilkan semua data
@app.route('/')
def index():
    search_query = request.args.get('search', '')
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1
    per_page = 5
    offset = (page - 1) * per_page
    
    cur = mysql.connection.cursor()
    
    try:
        # --- 1. Get TOTAL count for pagination ---
        count_query = "SELECT COUNT(*) FROM stok"
        count_params = []
        if search_query:
            count_query += " WHERE kode_sparepart LIKE %s OR nama_sparepart LIKE %s OR harga LIKE %s OR tipe_motor LIKE %s OR stok LIKE %s"
            search_term = '%' + search_query + '%'
            count_params = [search_term, search_term, search_term, search_term, search_term]
        
        cur.execute(count_query, count_params)
        total_rows = cur.fetchone()[0]
        total_pages = math.ceil(total_rows / per_page)

        # --- 2. Get DATA for the current page ---
        data_query = "SELECT * FROM stok"
        data_params = []
        if search_query:
            data_query += " WHERE kode_sparepart LIKE %s OR nama_sparepart LIKE %s OR harga LIKE %s OR tipe_motor LIKE %s OR stok LIKE %s"
            data_params = [search_term, search_term, search_term, search_term, search_term]
        
        data_query += " LIMIT %s OFFSET %s"
        data_params.extend([per_page, offset])
        
        cur.execute(data_query, data_params)
        data = cur.fetchall()

        return render_template('index.html', 
                               data=data, 
                               page=page, 
                               total_pages=total_pages, 
                               search=search_query)
    except Exception as e:
        flash(f"Error fetching data: {str(e)}", "error")
        return render_template('index.html', data=[], page=1, total_pages=1, search=search_query)
    finally:
        if cur:
            cur.close()

# CREATE - Tambah data
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Basic validation
        if not request.form['kode'] or not request.form['nama'] or not request.form['harga']:
            flash("All fields are required!", "error")
            return render_template('add.html')
        
        try:
            kode = request.form['kode']
            nama = request.form['nama']
            harga = request.form['harga']
            try:
                harga = float(harga)
            except ValueError:
                flash("Price must be a number!", "error")
                return render_template('add.html')
            
            image_filename = None
            if 'image' in request.files:
                file = request.files['image']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filename = f"{kode}_{filename}"
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    image_filename = filename

            cur = mysql.connection.cursor()
            try:
                if image_filename:
                    cur.execute(
                        "INSERT INTO stok (kode, nama, harga, image) VALUES (%s, %s, %s, %s)",
                        (kode, nama, harga, image_filename)
                    )
                else:
                    cur.execute(
                        "INSERT INTO stok (kode, nama, harga) VALUES (%s, %s, %s)",
                        (kode, nama, harga)
                    )
            except Exception:
                cur.execute(
                    "INSERT INTO stok (kode, nama, harga) VALUES (%s, %s, %s)",
                    (kode, nama, harga)
                )
            mysql.connection.commit()
            cur.close()
            flash("Item added successfully!", "success")
            return redirect(url_for('index'))
        except Exception as e:
            flash(f"Error: {str(e)}", "error")
            return render_template('add.html')
    return render_template('add.html')

# UPDATE - Edit data
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    try:
        cur = mysql.connection.cursor()
        if request.method == 'POST':
            # Basic validation
            if not request.form['kode'] or not request.form['nama'] or not request.form['harga']:
                flash("All fields are required!", "error")
                cur.execute("SELECT * FROM stok WHERE id=%s", (id,))
                data = cur.fetchone()
                cur.close()
                return render_template('edit.html', data=data)

            kode = request.form['kode']
            nama = request.form['nama']
            harga = request.form['harga']

            # Handle optional image upload on edit
            image_filename = None
            if 'image' in request.files:
                file = request.files['image']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filename = f"{kode}_{filename}"
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    image_filename = filename
                    # delete old image if present
                    try:
                        cur.execute("SELECT image FROM stok WHERE id=%s", (id,))
                        old = cur.fetchone()
                        if old and old[0] and old[0] != image_filename:
                            old_path = os.path.join(app.config['UPLOAD_FOLDER'], old[0])
                            if os.path.exists(old_path):
                                os.remove(old_path)
                    except Exception:
                        pass

            # Validate harga is a number
            try:
                harga = float(harga)
            except ValueError:
                flash("Price must be a number!", "error")
                cur.execute("SELECT * FROM stok WHERE id=%s", (id,))
                data = cur.fetchone()
                cur.close()
                return render_template('edit.html', data=data)

            # Try to update image column if exists
            try:
                if image_filename:
                    cur.execute(
                        "UPDATE stok SET kode=%s, nama=%s, harga=%s, image=%s WHERE id=%s",
                        (kode, nama, harga, image_filename, id)
                    )
                else:
                    cur.execute(
                        "UPDATE stok SET kode=%s, nama=%s, harga=%s WHERE id=%s",
                        (kode, nama, harga, id)
                    )
            except Exception:
                cur.execute(
                    "UPDATE stok SET kode=%s, nama=%s, harga=%s WHERE id=%s",
                    (kode, nama, harga, id)
                )
            mysql.connection.commit()
            cur.close()
            flash("Item updated successfully!", "success")
            return redirect(url_for('index'))
        else:
            cur.execute("SELECT * FROM stok WHERE id=%s", (id,))
            data = cur.fetchone()
            cur.close()
            if data is None:
                flash("Item not found!", "error")
                return redirect(url_for('index'))
            return render_template('edit.html', data=data)
    except Exception as e:
        flash(f"Error: {str(e)}", "error")
        return redirect(url_for('index'))

# DELETE - Hapus data
@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    try:
        cur = mysql.connection.cursor()
        try:
            cur.execute("SELECT image FROM stok WHERE id=%s", (id,))
            row = cur.fetchone()
            if row and row[0]:
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], row[0])
                if os.path.exists(image_path):
                    os.remove(image_path)
        except Exception:
            pass

        cur.execute("DELETE FROM stok WHERE id=%s", (id,))
        mysql.connection.commit()
        cur.close()
        flash("Item deleted successfully!", "success")
    except Exception as e:
        flash(f"Error: {str(e)}", "error")
    return redirect(url_for('index'))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)