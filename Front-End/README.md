# Front-End Coursework

HTML/CSS/JavaScript exercises for the 3rd-semester "Dasar Pemrograman Frontend" course. Folders are grouped by meeting (`P2`-`P11`) plus `UTS`.

Contents by meeting
- `P2`-`P3`: JS basics (syntax, alerts/dialogs, simple branching/loops).
- `P4`: Functions and modules.
- `P5`: DOM events and interactions.
- `P6`: AJAX/jQuery selectors and data fetching.
- `P7`: Deeper interactivity and UI refinement.
- `P9`-`P10`: Larger assignments (e.g., spare-part web project with DB connector).
- `P11`: Mobile-first ecommerce demo (Flask + templates) with cart/checkout flows.
- `UTS`: Midterm submission.

How to run
- Static pages: open the HTML file directly in your browser.
- Flask-based work (e.g., `P11/Ecommerce_dinamis_mobile`):
  1) `cd` into the project folder.
  2) Install deps: `pip install flask mysql-connector-python` (plus any listed in the code).
  3) `python app.py` and open the printed localhost URL.
  4) Seed the DB if needed (see `Front-End/P11/schema-seed.sql`).
