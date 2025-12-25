# P4 - Flask Basics

Intro to Flask routing, templates, and simple form handling.

## Files

- `app.py`: core routes and form handling.
- `routing_app.py`: routing examples.
- `decorator_app.py`: decorator-based routing.
- `templates/`: HTML pages (`index.html`, `form.html`, `login.html`, `dashboard.html`).

## Run locally

1) Install deps: `pip install flask`.
2) Start a sample: `python app.py` (or `python routing_app.py` / `python decorator_app.py`).
3) Open the printed localhost URL in your browser.

## Notes

- Forms post back to the same app; no database is used here.
- Adjust `debug=True` in the scripts if you want auto-reload.
