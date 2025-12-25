import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import mysql.connector
from mysql.connector import pooling


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

MYSQL_HOST = os.environ.get("MYSQL_HOST", "100.117.130.109")
MYSQL_PORT = int(os.environ.get("MYSQL_PORT", "3306"))
MYSQL_USER = os.environ.get("MYSQL_USER", "testuser")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "testpass")
MYSQL_DB = os.environ.get("MYSQL_DB", "testdb")
MYSQL_TABLE = os.environ.get("MYSQL_TABLE", "barang")
MYSQL_POOL_SIZE = int(os.environ.get("MYSQL_POOL_SIZE", "5"))

_POOL = pooling.MySQLConnectionPool(
    pool_name="p11_proxy_pool",
    pool_size=MYSQL_POOL_SIZE,
    pool_reset_session=True,
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DB,
)


def init_db():
    conn = _POOL.get_connection()
    cur = conn.cursor()
    cur.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {MYSQL_TABLE} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            kode VARCHAR(50) NOT NULL,
            nama VARCHAR(100) NOT NULL,
            harga DECIMAL(12, 2) NOT NULL,
            gambar VARCHAR(255),
            jumlah INT NOT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
    )
    conn.commit()
    cur.close()
    conn.close()


init_db()


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    conn = _POOL.get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(f"SELECT id, kode, nama, harga, gambar, jumlah FROM {MYSQL_TABLE} ORDER BY id DESC")
    rows = cur.fetchall()
    cur.close()
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

        conn = _POOL.get_connection()
        cur = conn.cursor()
        cur.execute(
            f"INSERT INTO {MYSQL_TABLE} (kode, nama, harga, gambar, jumlah) VALUES (%s, %s, %s, %s, %s)",
            (kode, nama, harga, gambar, jumlah),
        )
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("index"))
    return render_template("add.html")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id: int):
    conn = _POOL.get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(f"SELECT id, kode, nama, harga, gambar, jumlah FROM {MYSQL_TABLE} WHERE id=%s", (id,))
    current = cur.fetchone()
    if not current:
        cur.close()
        conn.close()
        return redirect(url_for("index"))

    if request.method == "POST":
        kode = request.form["kode"]
        nama = request.form["nama"]
        harga = request.form["harga"]
        jumlah = request.form["jumlah"]
        gambar = current.get("gambar")

        file = request.files.get("gambar")
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            gambar = filename

        cur2 = conn.cursor()
        cur2.execute(
            f"UPDATE {MYSQL_TABLE} SET kode=%s, nama=%s, harga=%s, jumlah=%s, gambar=%s WHERE id=%s",
            (kode, nama, harga, jumlah, gambar, id),
        )
        conn.commit()
        cur2.close()
        cur.close()
        conn.close()
        return redirect(url_for("index"))

    stok = current
    cur.close()
    conn.close()
    return render_template("edit.html", stoks=stok)


@app.route("/delete/<int:id>")
def delete(id: int):
    conn = _POOL.get_connection()
    cur = conn.cursor()
    cur.execute(f"DELETE FROM {MYSQL_TABLE} WHERE id=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)

