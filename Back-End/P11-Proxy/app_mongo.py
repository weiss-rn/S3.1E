import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from bson.objectid import ObjectId


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://100.103.170.96:27017/testdb")
MONGO_DB = os.environ.get("MONGO_DB", "testdb")
MONGO_COLLECTION = os.environ.get("MONGO_COLLECTION", "barang")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def _as_float(value: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _as_int(value: str) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _doc_to_view_model(doc: dict) -> dict:
    return {
        "id": str(doc.get("_id")),
        "kode": doc.get("kode", ""),
        "nama": doc.get("nama", ""),
        "harga": doc.get("harga", 0),
        "gambar": doc.get("gambar"),
        "jumlah": doc.get("jumlah", 0),
    }


@app.route("/")
def index():
    docs = collection.find().sort("_id", -1)
    rows = [_doc_to_view_model(doc) for doc in docs]
    return render_template("index.html", stoks=rows)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        kode = request.form["kode"]
        nama = request.form["nama"]
        harga = _as_float(request.form.get("harga"))
        jumlah = _as_int(request.form.get("jumlah"))
        gambar = None

        file = request.files.get("gambar")
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            gambar = filename

        collection.insert_one(
            {"kode": kode, "nama": nama, "harga": harga, "gambar": gambar, "jumlah": jumlah}
        )
        return redirect(url_for("index"))
    return render_template("add.html")


@app.route("/edit/<id>", methods=["GET", "POST"])
def edit(id: str):
    try:
        obj_id = ObjectId(id)
    except Exception:
        return redirect(url_for("index"))

    doc = collection.find_one({"_id": obj_id})
    if not doc:
        return redirect(url_for("index"))

    if request.method == "POST":
        kode = request.form["kode"]
        nama = request.form["nama"]
        harga = _as_float(request.form.get("harga"))
        jumlah = _as_int(request.form.get("jumlah"))
        gambar = doc.get("gambar")

        file = request.files.get("gambar")
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            gambar = filename

        collection.update_one(
            {"_id": obj_id},
            {"$set": {"kode": kode, "nama": nama, "harga": harga, "gambar": gambar, "jumlah": jumlah}},
        )
        return redirect(url_for("index"))

    stok = _doc_to_view_model(doc)
    return render_template("edit.html", stoks=stok)


@app.route("/delete/<id>")
def delete(id: str):
    try:
        obj_id = ObjectId(id)
    except Exception:
        return redirect(url_for("index"))

    collection.delete_one({"_id": obj_id})
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)

