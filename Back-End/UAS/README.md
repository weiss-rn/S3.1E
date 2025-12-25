# P11-Proxy

Same CRUD UI as `app.py`, but with external databases:

- MySQL: `app_mysql.py`
- MongoDB: `app_mongo.py`

## Run

1) Install deps (pick what you need):
   - `pip install flask mysql-connector-python pymongo`
2) `cd Back-End/P11-Proxy`
3) Start one of:
   - SQLite (local): `python app.py`
   - MySQL (external): `python app_mysql.py`
   - MongoDB (external): `python app_mongo.py`

## Connection settings

### MySQL (`app_mysql.py`)

Environment variables (defaults are taken from existing P7 MySQL example):

- `MYSQL_HOST` (default `100.117.130.109`)
- `MYSQL_PORT` (default `3306`)
- `MYSQL_USER` (default `testuser`)
- `MYSQL_PASSWORD` (default `testpass`)
- `MYSQL_DB` (default `testdb`)
- `MYSQL_TABLE` (default `barang`)

Seed SQL: `JSON/Seeq.sql`

### MongoDB (`app_mongo.py`)

- `MONGO_URI` (default `mongodb://100.103.170.96:27017/testdb`)
- `MONGO_DB` (default `testdb`)
- `MONGO_COLLECTION` (default `barang`)

Seed JSON: `JSON/Seeq.json` (import with `mongoimport --db testdb --collection barang --file JSON/Seeq.json --jsonArray`)

