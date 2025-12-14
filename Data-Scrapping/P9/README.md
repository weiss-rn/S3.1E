# P9 Scraper

This script (`main_v2.py`) scrapes article blocks from https://tekno.kompas.com/ using Selenium and saves collected article HTML blocks into `temp/articles.html`.

Usage:

1. Install dependencies (e.g., `beautifulsoup4`, `selenium`).

2. Make sure Chrome and compatible chromedriver are installed and on PATH.

3. Run the scraper from the repository root:

```powershell
python .\Data-Scrapping\P9\main_v2.py
```

Output:
- `temp/articles.html` — contains the prettified HTML for all article blocks scraped, separated by `<!-- PAGE_BREAK_N -->` markers.

Notes:
- The script runs in headless mode and stops automatically after scraping up to 10 pages (configurable via `max_pages`).
- If you need to tweak selectors, search for the `article_divs` list comprehension in `main_v2.py`.
