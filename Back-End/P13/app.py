from flask import Flask, render_template, request, redirect, url_for
import os
import sqlite3
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "static", "uploads")
app.config["DATABASE"] = os.path.join(app.root_path, "stokumkm.db")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

def db():
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS barang(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kode TEXT NOT NULL,
        nama TEXT NOT NULL,
        harga REAL NOT NULL,
        gambar TEXT,
        jumlah INTEGER NOT NULL
        )
    """
    )
    conn.commit()
    conn.close()


init_db()


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    conn = db()
    rows = conn.execute("SELECT * FROM barang").fetchall()
    conn.close()
    return render_template("index.html", stoks=rows)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        kode = request.form["kode"]
        nama = request.form["nama"]
        harga = request.form["harga"]
        jumlah = request.form["jumlah"]
        gambar = None

        file = request.files.get("gambar")
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            gambar = filename

        conn = db()
        conn.execute(
            "INSERT INTO barang (kode, nama, harga, gambar, jumlah) VALUES (?, ?, ?, ?, ?)",
            (kode, nama, harga, gambar, jumlah),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("add.html")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = db()
    current = conn.execute("SELECT * FROM barang WHERE id=?", (id,)).fetchone()
    if not current:
        conn.close()
        return redirect(url_for("index"))

    if request.method == "POST":
        kode = request.form["kode"]
        nama = request.form["nama"]
        harga = request.form["harga"]
        jumlah = request.form["jumlah"]
        gambar = current["gambar"]

        file = request.files.get("gambar")
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            gambar = filename

        conn.execute(
            "UPDATE barang SET kode=?, nama=?, harga=?, jumlah=?, gambar=? WHERE id=?",
            (kode, nama, harga, jumlah, gambar, id),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    stok = current
    conn.close()
    return render_template("edit.html", stoks=stok)


# --- DELETE ---
@app.route("/delete/<int:id>")
def delete(id):
    conn = db()
    conn.execute("DELETE FROM barang WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
