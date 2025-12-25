# P9 - Selenium Scraper (Kompas Tekno)

Scraping experiments for https://tekno.kompas.com/ using Selenium and BeautifulSoup.

## Files

- `main.py`: saves prettified HTML to `temp/text.txt`, extracts titles to `temp/titles.txt`.
- `main_alt.py`: basic Selenium scrape for the gadget page and writes a placeholder file to `hasil/kompasparser.txt`.
- `main_v2.py`: paginated scraper that collects article blocks into `temp/articles.html`.
- `fungsi.py`: helper methods for directories and file IO.

## Requirements

- `pip install beautifulsoup4 selenium requests`
- Chrome and a matching chromedriver on PATH.

## Run

From the repository root:

```powershell
python .\Data-Scrapping\P9\main_v2.py
```

## Output

- `temp/` and `hasil/` directories are created if missing.
- `temp/articles.html` contains concatenated article blocks separated by `<!-- PAGE_BREAK_N -->` markers.
