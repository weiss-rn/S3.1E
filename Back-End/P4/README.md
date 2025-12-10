# P4 - Flask Basics

Intro Flask exercises covering routing, templates, form handling, and simple auth-style flows.

Key files
- `app.py` / `routing_app.py`: core routes and simple examples.
- `decorator_app.py`: demonstrates decorator use on routes.
- Templates: `index.html`, `form.html`, `login.html`, `dashboard.html`.

Run locally
1) Install deps: `pip install flask`.
2) Start the sample: `python app.py` (or `python routing_app.py` / `python decorator_app.py`).
3) Open the printed localhost URL in your browser.

Notes
- Forms post back to the same app; no database is wired in this module.
- Adjust `debug=True` in the scripts if you do or do not want auto-reload.
