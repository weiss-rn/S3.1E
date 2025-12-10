# P4 - Requests + BeautifulSoup

Shows how to fetch pages, parse them with BeautifulSoup, and persist results.

Scripts
- `P4.py`: basic request and parsing demo.
- `P4_1.py`: helper functions (directory creation, fetch utilities).
- `P4_2.py`: iterative scraping with selectors to extract elements.
- `P4_3.py`: paginated scrape that saves matching elements to disk with a configurable limit.

Run locally
1) Install deps: `pip install requests beautifulsoup4`.
2) Execute the script you want, e.g., `python P4_3.py`.
3) Review the saved files/logs in the output directory set in the script.

Tips
- Update target URLs/selectors if the source site layout changes.
- Network failures will raise exceptions; wrap in try/except if you need softer handling.
