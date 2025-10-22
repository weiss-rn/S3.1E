from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from flask_mysqldb import MySQL
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.urandom(24) 

app.config['MYSQL_HOST'] = '100.79.36.118'
app.config['MYSQL_USER'] = 'testuser'
app.config['MYSQL_PASSWORD'] = 'testpass'  # Add your password here
app.config['MYSQL_DB'] = 'testdb'  # Add your database name

mysql = MySQL(app)

# Upload configuration
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
    try:
        cur = mysql.connection.cursor()
        # Try to select image column if exists; fallback to select all
        try:
            cur.execute("SELECT * FROM stok")
        except Exception:
            cur.execute("SELECT id, kode, nama, harga FROM stok")
        data = cur.fetchall()
        cur.close()
        return render_template('index.html', data=data)
    except Exception as e:
        flash(f"Error: {str(e)}", "error")
        return render_template('index.html', data=[])

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
            
            # Validate harga is a number
            try:
                harga = float(harga)
            except ValueError:
                flash("Price must be a number!", "error")
                return render_template('add.html')
            
            # Handle optional image upload
            image_filename = None
            if 'image' in request.files:
                file = request.files['image']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    # Prepend unique part to reduce collisions
                    filename = f"{kode}_{filename}"
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    image_filename = filename

            cur = mysql.connection.cursor()
            # Try to insert image column if it exists
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
                # Fallback if table doesn't have image column
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
        # Attempt to fetch image filename so we can delete file
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
    # Serve uploaded files (images)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)