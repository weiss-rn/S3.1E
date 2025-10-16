from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import os

app = Flask(__name__)
app.secret_key = os.urandom(24) 

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # Add your password here
app.config['MYSQL_DB'] = 'crud_flask'  # Add your database name

mysql = MySQL(app)

# READ - Tampilkan semua data
@app.route('/')
def index():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM stok")
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
            
            cur = mysql.connection.cursor()
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
            
            # Validate harga is a number
            try:
                harga = float(harga)
            except ValueError:
                flash("Price must be a number!", "error")
                cur.execute("SELECT * FROM stok WHERE id=%s", (id,))
                data = cur.fetchone()
                cur.close()
                return render_template('edit.html', data=data)
            
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
        cur.execute("DELETE FROM stok WHERE id=%s", (id,))
        mysql.connection.commit()
        cur.close()
        flash("Item deleted successfully!", "success")
    except Exception as e:
        flash(f"Error: {str(e)}", "error")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)