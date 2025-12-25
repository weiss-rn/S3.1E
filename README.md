# S3.1E Coursework

Assignments for SP3 / SPS3.1E. Each top-level folder groups a subject area, and most meetings are organized as `P#`.

## Folder map

- `Front-End/` - HTML/CSS/JS exercises plus Flask-based UI demos.
- `Back-End/` - Python and Flask backend exercises.
- `Data-Scrapping/` - Requests, BeautifulSoup, Selenium, and a small Flask demo.
- `PPBJ/` - Static site tasks and helper scripts (no README yet).
- `static/` - Shared assets used by some tasks.

## Requirements

- Python 3.10+ for most scripts and Flask apps.
- Optional: MySQL/MariaDB for DB-backed tasks.
- Optional: MongoDB for UAS (Back-End).
- Optional: Chrome and chromedriver for Selenium scrapers (Data-Scrapping/P9).

## Quick start

1) Create and activate a virtual environment (recommended).
2) Install dependencies for the folder you want to run.
3) Run the script or Flask app from that folder.

## How to run

- Static HTML/CSS/JS: open an `index.html` directly, or serve via `python -m http.server 8000`.
- Python scripts: `python <script>.py`.
- Flask apps: `python app.py`, then open the printed localhost URL.
- DB-backed apps: update credentials in the script or set environment variables where supported.

Tip: some folder names contain spaces; quote paths when using `cd`, e.g. `cd "Front-End/P10/Project Web - Spare Part Motor"`.

## Seed and sample data

- `Back-End/P7/schema.sql`, `Back-End/P7/seed.sql`
- `Back-End/UTS/schema.sql`, `Back-End/UTS/seed.sql`
- `Back-End/UAS/JSON/Seeq.sql`, `Back-End/UAS/JSON/Seeq.json`
- `Front-End/P10/Project Web - Spare Part Motor/DB-Connector/schema.sql`
- `Front-End/P10/Project Web - Spare Part Motor/DB-Connector/seed.sql`
- `Front-End/P11/schema-seed.sql`
- `Front-End/P11/Tugas/Seed.sql`
- `Front-End/P11/Critical Fix in UI/UX copy/Seed.sql`
- `Front-End/P12/Seed.sql`, `Front-End/P13/Seed.sql`
- `Front-End/UAS/Tugas/Seed.sql`

## Navigation

- Start with subject READMEs: `Front-End/README.md`, `Back-End/README.md`, `Data-Scrapping/README.md`.
- Subfolders often include templates, static assets, and data seeds for each exercise.
