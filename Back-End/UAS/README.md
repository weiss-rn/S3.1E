# UAS - Stok UMKM CRUD

Inventory management app with image upload and CRUD for `barang`. This folder provides SQLite, MySQL, and MongoDB variants.

## Entry points

- `app_sqlite.py`: local SQLite database (`stokumkm.db`).
- `app_mysql.py`: MySQL backend with connection settings from env vars.
- `app_mongo.py`: MongoDB backend with connection settings from env vars.

## Run (SQLite)

1) `pip install flask`
2) `cd Back-End\UAS`
3) `python app_sqlite.py`

## Run (MySQL)

1) `pip install flask mysql-connector-python`
2) Set env vars or edit defaults:
   - `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD`
   - `MYSQL_DB`, `MYSQL_TABLE`, `MYSQL_POOL_SIZE`
3) `python app_mysql.py`

## Run (MongoDB)

1) `pip install flask pymongo`
2) Set env vars:
   - `MONGO_URI`, `MONGO_DB`, `MONGO_COLLECTION`
3) `python app_mongo.py`

## Seed data

- SQL: `Back-End/UAS/JSON/Seeq.sql`
- JSON: `Back-End/UAS/JSON/Seeq.json` (import with `mongoimport`)

## Notes

- Uploaded images are stored in `static/uploads`.
- `requirements.txt` lists the Python packages for this folder.
