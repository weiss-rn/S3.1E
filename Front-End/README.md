# Front-End Coursework

HTML/CSS/JavaScript exercises for the 3rd-semester "Dasar Pemrograman Frontend" course. Folders are grouped by meeting (`P2`-`P13`) plus `UTS` and `UAS`.

## Contents by meeting

- `P2`-`P3`: JS basics (syntax, alerts/dialogs, simple branching/loops).
- `P4`: functions and modules.
- `P5`: DOM events and interactions.
- `P6`: AJAX/jQuery selectors and data fetching.
- `P7`: interactivity and UI refinement.
- `P9`-`P10`: larger assignments (including spare-part web project with DB connector).
- `P11`: mobile-first ecommerce demo plus fixes and tasks (Flask + templates).
- `P12`-`P13`: product catalog with categories, cart, and admin CRUD (Flask + MySQL).
- `UTS`: midterm submission.
- `UAS`: final assignment (Flask app in `UAS/Tugas`).

## How to run

- Static pages: open the HTML file directly in your browser.
- Flask-based work:
  1) `cd` into the project folder.
  2) Install deps: `pip install flask mysql-connector-python` (plus any listed in the code).
  3) `python app.py` and open the printed localhost URL.
  4) Seed the DB if needed (see the `Seed.sql` or schema files in the folder).
