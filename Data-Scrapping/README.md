# Data-Scrapping Coursework

Python scraping exercises organized by meeting (`P2`-`P11`). Scripts use `requests`, `beautifulsoup4`, and (for P9) `selenium`.

## Contents by meeting

- `P2`-`P3`: basic HTTP requests and simple parsing examples.
- `P4`: helper functions and selector practice (`P4.py`, `P4_1.py`, `P4_2.py`, `P4_3.py`).
- `P5`-`P7`: parsing, cleaning, and export exercises.
- `P8`: multi-step scrape with temp output (`main.py`, `main_v2.py`).
- `P9`: Selenium-based Kompas Tekno scraper (`main.py`, `main_alt.py`, `main_v2.py`).
- `P10`: single-script scrape (`main.py`).
- `P11`: Flask demo with query string login and a template.

## How to run a script

1) `cd` into the `P#` folder.
2) Install dependencies:
   - Requests + BS4: `pip install requests beautifulsoup4`
   - Selenium (P9): `pip install selenium`
   - Flask (P11): `pip install flask`
3) Execute the script, e.g., `python P4_3.py`.
4) Check the output directory or printed logs for saved files/results.

## Notes

- Many scripts write into `temp` or `hasil` subfolders in the same directory.
- Inspect target URLs/selectors before running; update them if the site structure changes.
- Selenium requires Chrome and a matching chromedriver on PATH.
