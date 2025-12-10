# Back-End Coursework

Python/Flask backend exercises for the 3rd-semester "Dasar Pemrograman Backend" course. Folders are grouped by meeting (`P2`-`P10`) plus `UTS`.

Contents by meeting
- `P2`-`P3`: Core Python (syntax, arithmetic helpers, simple modules, JSON/file handling).
- `P4`: Intro to Flask (routing, templates, form handling, login/dashboard demos).
- `P5`-`P6`: Flask with forms, static assets, and basic CRUD against in-memory/data sources.
- `P7`: Advanced Flask patterns (template features, file upload handling).
- `P9`-`P10`: Extended Flask/database work and final practice apps.
- `UTS`: Midterm submission.

How to run a Flask exercise
1) `cd` into the chosen `P#` folder.
2) (Optional) create a venv: `python -m venv .venv && .\.venv\Scripts\activate` (Windows) or `python3 -m venv .venv && source .venv/bin/activate` (Unix).
3) Install dependencies if needed (common: `pip install flask mysql-connector-python`).
4) Run the app, typically `python app.py` (some folders have multiple entry points like `routing_app.py`).
5) Open the printed localhost URL in your browser.

Tips
- Check inline comments for required environment variables or credentials.
- For DB-backed examples, confirm the connection string/host and run any seed SQL provided in the folder before testing.
