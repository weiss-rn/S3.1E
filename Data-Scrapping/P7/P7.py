import os
import requests
from bs4 import BeautifulSoup
from P4_1 import fungsi

def get_details(article_url):
    base_url = "https://tekno.kompas.com"
    if article_url.startswith("/"):
        article_url = base_url + article_url
    elif not article_url.startswith("http"):
        article_url = f"{base_url}/{article_url.lstrip('/')}"
    
    try:
        resp = requests.get(article_url, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print(f"Failed to retrieve article {article_url}: {e}")
        return
    
    soup = BeautifulSoup(resp.text, "html.parser")

    title_tag = soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else "No title found"

    content_tags = soup.find_all("p")
    content = "\n".join(p.get_text(strip=True) for p in content_tags if p.get_text(strip=True))
    
    file_path = os.path.join(current_directory, current_file)
    fungsi.write_to_file(file_path, f"Detail URL: {article_url}")
    fungsi.write_to_file(file_path, f"Detail Title: {title}")
    fungsi.write_to_file(file_path, f"Detail Content:\n{content}\n")
    print(f"Isi Web dengan konten for {article_url}")

def main_scrapper(url, directory, file):
    global current_directory, current_file
    current_directory, current_file = directory, file
    fungsi.create_directory(directory)
    source_code = requests.get(url)
    source_text = source_code.text
    soup = BeautifulSoup(source_text, "html.parser")
    articles = soup.find("div", {"class":["row mt3 col-offset-fluid clearfix"]})
    articles2 = articles.find("div", {"class":["col-bs10-7"]})
    articles3 = articles2.find("div", {"class":["row article__wrap__grid--flex col-offset-fluid mt2"]})
    articles4 = articles3.find_all("div", {"class":["article__box"]})

    if not articles4:
        print("No articles found.")
        return
    articles4 = articles4[:3]
    
    os.system("cls")
    
    for article4 in articles4:
        article_url = article4.h3.a.get("href")
        print("URL: ", article_url)
        print("Title: ", article4.h3.text, "\n")
        file_path = os.path.join(directory, file)
        fungsi.write_to_file(file_path, "URL: " + article_url)
        fungsi.write_to_file(file_path, "Title: " + article4.h3.text + "\n")
        get_details(article_url)

main_scrapper("https://tekno.kompas.com/gadget", "hasil", "output-scraping.txt")

