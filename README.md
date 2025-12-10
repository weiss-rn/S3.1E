# S3.1E Coursework Snapshot

This repo collects SP3/SPS3.1E semester submissions. Each top-level folder maps to a subject area:

- `Front-End/` - HTML/CSS/JS coursework by meeting (`P2`-`P11`) plus UTS. Mix of static pages and small Flask apps.
- `Back-End/` - Python/Flask backend exercises (`P2`-`P10`) plus UTS.
- `Data-Scrapping/` - Requests + BeautifulSoup scraping assignments (`P2`-`P10`).
- `PPBJ/` - Simple static site with a tiny Python HTTP server helper.

Getting started
1) Install Python 3.10+.
2) For Flask or scraping tasks, optionally create a venv: `python -m venv .venv && .\.venv\Scripts\activate` (Windows) or `python3 -m venv .venv && source .venv/bin/activate` (Unix).
3) Install per-project deps (see folder READMEs; common: `pip install flask mysql-connector-python requests beautifulsoup4`).

Navigation
- See `Front-End/README.md`, `Back-End/README.md`, and `Data-Scrapping/README.md` for meeting-by-meeting notes and run commands.
- Each subfolder may contain its own README with specifics for that exercise.
