import os
from pathlib import Path
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://id.indeed.com"
SEARCH_URL = f"{BASE_URL}/jobs"  # Hit the actual job search endpoint.
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
}
TEMP_DIR = Path(__file__).resolve().parent / "temp"


def get_total_pages():
    params = {
        "q": "web developer",
        "l": "Malang",
        'vjk': "aff1cac2a018d658"
    }

    TEMP_DIR.mkdir(exist_ok=True)

    try:
        # Guard the network call with timeout and status check.
        res = requests.get(SEARCH_URL, params=params, headers=HEADERS, timeout=10)
        res.raise_for_status()
    except requests.RequestException as exc:
        print(f"Request failed: {exc}")
        return 0

    # Keep the latest response for debugging.
    (TEMP_DIR / "last_response.html").write_text(res.text, encoding="utf-8")

    soup = BeautifulSoup(res.text, "html.parser")

    page_numbers = []
    for anchor in soup.select(
        'nav[aria-label="pagination"] a, ul.pagination-list a, a[aria-label^="Page"], a[aria-label^="Halaman"]'
    ):
        text = anchor.get_text(strip=True)
        try:
            page_numbers.append(int(text))
        except ValueError:
            continue

    total_pages = max(page_numbers) if page_numbers else 1
    print(f"Total pages found: {total_pages}")
    return total_pages


if __name__ == "__main__":
    get_total_pages()
