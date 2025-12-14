from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import os
from fungsi import Fungsi

url = "https://tekno.kompas.com/"

try:
    os.mkdir("temp")
except FileExistsError:
    pass

driver = webdriver.Chrome()
driver.set_page_load_timeout(3600)
driver.get(url)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

with open('temp/text.txt', 'w+', encoding='utf-8') as outfile:
    outfile.write(soup.prettify())

print("HTML file saved to temp/text.html")

# --- Parse saved HTML and extract titles ---
def extract_titles(soup, max_titles=100):
    titles = []
    seen = set()

    # 1) Look for explicit headline/property tags
    for tag in soup.select('[itemprop~=headline], h1, h2, h3'):
        text = tag.get_text(strip=True)
        if not text:
            continue
        if len(text) < 4:
            continue
        if text in seen:
            continue
        titles.append(text)
        seen.add(text)
        if len(titles) >= max_titles:
            return titles

    # 2) Look for anchor tags whose class contains 'title' or 'headline' or 'judul'
    for a in soup.find_all('a', class_=True):
        cls = ' '.join(a.get('class'))
        if any(k in cls.lower() for k in ('title', 'judul', 'headline')):
            text = a.get_text(strip=True)
            if text and text not in seen and len(text) > 4:
                titles.append(text)
                seen.add(text)
                if len(titles) >= max_titles:
                    return titles

    # 3) As fallback, search for divs with class containing 'article' and grab their first heading or link
    for div in soup.find_all('div', class_=True):
        classes = ' '.join(div.get('class') or [])
        if 'article' in classes.lower():
            # try to find a heading inside
            h = div.find(['h1', 'h2', 'h3', 'h4'])
            if h:
                text = h.get_text(strip=True)
                if text and text not in seen and len(text) > 4:
                    titles.append(text)
                    seen.add(text)
                    if len(titles) >= max_titles:
                        return titles
            # else try first link
            a = div.find('a')
            if a:
                text = a.get_text(strip=True)
                if text and text not in seen and len(text) > 4:
                    titles.append(text)
                    seen.add(text)
                    if len(titles) >= max_titles:
                        return titles

    return titles


try:
    titles = extract_titles(soup, max_titles=200)
    out_titles = os.path.join('temp', 'titles.txt')
    with open(out_titles, 'w', encoding='utf-8') as f:
        for t in titles:
            f.write(t + '\n')

    print(f"Extracted {len(titles)} titles and saved to {out_titles}")
    # quick preview
    for i, t in enumerate(titles[:20], 1):
        print(f"{i}. {t}")
except Exception as e:
    print("Error while extracting titles:", e)