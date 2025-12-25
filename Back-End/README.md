# Back-End Coursework

Python and Flask backend exercises for the 3rd-semester "Dasar Pemrograman Backend" course. Folders are grouped by meeting (`P2`-`P13`) plus `UTS` and `UAS`.

## Contents by meeting

- `P2`-`P3`: core Python (syntax, modules, JSON/file handling).
- `P4`: Flask routing, templates, form handling (see `Back-End/P4/README.md`).
- `P5`-`P6`: forms, static assets, and CRUD basics.
- `P7`: templates, file uploads, and MySQL examples.
- `P9`-`P10`: CRUD apps and data seeds.
- `P10-Branch`: branch-style CRUD app with `seed.json`.
- `P11`-`P13`: stokumkm inventory CRUD using SQLite with templates/static assets.
- `UTS`: midterm submission with schema and seed SQL.
- `UAS`: inventory CRUD with SQLite, MySQL, and MongoDB entry points.

## How to run a Flask exercise

1) `cd` into the chosen `P#` folder.
2) (Optional) create a venv: `python -m venv .venv` and activate it.
3) Install dependencies if needed (common: `pip install flask mysql-connector-python`).
4) Run the app, typically `python app.py` (some folders have multiple entry points).
5) Open the printed localhost URL in your browser.

## Tips

- Check inline comments or environment variables for credentials.
- For DB-backed examples, update connection settings and run any seed SQL provided in the folder.
