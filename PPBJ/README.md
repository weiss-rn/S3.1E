# PPBJ

Simple static site (`index.html`, `about.html`, `services.html`) plus a lightweight Python HTTP server helper (`httpd.py`).

Run locally
1) `cd PPBJ`
2) Start a server:
   - `python httpd.py` (uses the helper script), or
   - `python -m http.server 8000` (built-in server)
3) Open `http://localhost:8000` in your browser to browse the pages.

Notes
- No external dependencies required beyond Python 3.
- Edit the HTML files directly to adjust content or styling.
