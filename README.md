# S3.1E Coursework Snapshot

Coursework submissions for SP3 / SPS3.1E. Each top-level folder groups assignments by subject area, and each `P#` folder typically represents a meeting.

## Folder map

- `Front-End/` - HTML/CSS/JS (plus a few small Flask + template demos). See `Front-End/README.md`.
- `Back-End/` - Python/Flask backend exercises and practice apps. See `Back-End/README.md`.
- `Data-Scrapping/` - Python scraping scripts using `requests` + `beautifulsoup4`. See `Data-Scrapping/README.md`.
- `PPBJ/` - Static site + simple Python HTTP server helper. See `PPBJ/README.md`.

## Requirements

- Python 3.10+ (used across Back-End and Data-Scrapping, and for Flask demos in Front-End).
- (Optional) MySQL/MariaDB for DB-backed exercises (several Flask projects query tables like `products`).

## Quick start (Python)

1) Create and activate a virtual environment (recommended):
   - Windows (PowerShell): `python -m venv .venv; .\.venv\Scripts\Activate.ps1`
   - macOS/Linux: `python3 -m venv .venv && source .venv/bin/activate`
2) Install dependencies as needed per folder (common packages):
   - Flask apps: `pip install flask mysql-connector-python`
   - Scraping scripts: `pip install requests beautifulsoup4`
3) Run the script/app in the chosen folder.

## How to run

- Static HTML/CSS/JS: open an `index.html` directly, or serve via `python -m http.server 8000` and browse `http://localhost:8000`.
- Python scripts (scraping/utilities): `cd` into the folder and run `python <script>.py`.
- Flask apps: `cd` into the folder and run `python app.py` (then open the printed localhost URL).

Tip: some folder names contain spaces; quote paths when using `cd`, e.g. `cd "Front-End/P10/Project Web - Spare Part Motor"`.

## Database notes (MySQL)

Some Flask projects are configured to connect to MySQL in their `app.py` (host/user/password/database are hard-coded). If you want to run them locally, update those connection settings to match your local DB.

Seed/schema files included in this repo (non-exhaustive):

- `Front-End/P11/schema-seed.sql`
- `Front-End/P11/Critical Fix in UI/UX copy/Seed.sql`
- `Front-End/P10/Project Web - Spare Part Motor/DB-Connector/schema.sql`
- `Back-End/P7/schema.sql`
- `Back-End/UTS/schema.sql`

## Navigation

- Start from the subject READMEs: `Front-End/README.md`, `Back-End/README.md`, `Data-Scrapping/README.md`, `PPBJ/README.md`.
- Many subfolders include additional notes/files specific to that exercise (SQL seeds, templates, assets, etc.).
