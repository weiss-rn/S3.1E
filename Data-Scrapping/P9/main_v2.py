from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import os
import time
from urllib.parse import urljoin
from fungsi import Fungsi

base_url = "https://tekno.kompas.com/"

try:
    os.mkdir("temp")
except FileExistsError:
    pass

opts = webdriver.ChromeOptions()
# headless can be '--headless' or '--headless=new' depending on Chrome version
opts.add_argument('--headless=new')
opts.add_argument('--no-sandbox')
opts.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=opts)
driver.set_page_load_timeout(3600)

max_pages = 10  # safety limit
page = 1
all_articles_html = ""
current_url = base_url

try:
    while True:
        print(f"Scraping page {page}: {current_url}")
        driver.get(current_url)
        time.sleep(2)  # Wait for dynamic content to load

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Collect divs that contain 'article' in any class name (robust selector)
        article_divs = [
            tag for tag in soup.find_all('div', class_=True)
            if any('article' in c for c in (tag.get('class') or []))
        ]

        if not article_divs:
            print(f"Warning: No article blocks found on page {page}")

        for div in article_divs:
            all_articles_html += div.prettify() + "\n\n"

        all_articles_html += f"\n\n<!-- PAGE_BREAK_{page} -->\n\n"

        # Find next page link in pagination
        next_href = None
        # Prefer links that explicitly point to the next page number
        for a in soup.select('a.paging_link'):
            data_page = a.get('data-page')
            if data_page == str(page + 1):
                next_href = a.get('href')
                break

        if not next_href:
            for a in soup.select('a.paging_link'):
                if a.get_text(strip=True) == str(page + 1):
                    next_href = a.get('href')
                    break

        if not next_href:
            a_rel_next = soup.find('a', rel='next')
            if a_rel_next:
                next_href = a_rel_next.get('href')

        if not next_href:
            # fallback: look for a paging link with a 'next' symbol
            for a in soup.select('a.paging_link'):
                if a.get_text(strip=True) in ['›', '»', 'Next', 'Next ›', 'next']:
                    next_href = a.get('href')
                    break

        if not next_href:
            print(f"No next page found. Stopped at page {page}")
            break

        # Build absolute URL for next page and increment
        next_url = urljoin(base_url, str(next_href))
        page += 1
        if page > max_pages:
            print("Reached page limit")
            break

        current_url = next_url

except Exception as e:
    print("An error occurred while scraping:", e)

finally:
    # Save collected article blocks to a single file
    out_path = os.path.join('temp', 'articles.html')
    with open(out_path, 'w+', encoding='utf-8') as outfile:
        outfile.write(all_articles_html)

    print(f"Article blocks saved to {out_path} (pages scraped: {page})")
    driver.quit()