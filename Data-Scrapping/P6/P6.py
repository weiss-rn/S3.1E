import os
import requests 
from P4_1 import fungsi
from bs4 import BeautifulSoup
from os import system

def get_details(url):
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print("Error fetching details:", e)
        return ""
    soup = BeautifulSoup(resp.text, "html.parser")
    container = soup.find("div", {"class":"read__content"}) or soup.find("div", {"class":"article__content"})
    paras = container.find_all("p") if container else soup.find_all("p")
    return "\n\n".join(p.get_text(strip=True) for p in paras if p.get_text(strip=True))

def main_scrapper(url, directory, file):
    fungsi.create_directory(directory)
    file_path = os.path.join(directory, file)
    fungsi.remove_file(file_path)

    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print("Error fetching list page:", e)
        return

    soup = BeautifulSoup(resp.text, "html.parser")
    article_boxes = soup.find_all("div", {"class":"article__box"})
    if not article_boxes:
        article_boxes = soup.find_all("article")

    for box in article_boxes:
        h3 = box.find("h3")
        link = h3.find("a") if h3 else box.find("a")
        if not link or not link.get("href"):
            continue
        title = link.get_text(strip=True)
        href = link.get("href")
        fungsi.write_to_file(file_path, "Title: " + title)
        fungsi.write_to_file(file_path, "URL: " + href)
        fungsi.write_to_file(file_path, "") 

        details = get_details(href)
        if details:
            fungsi.write_to_file(file_path, "Content:")
            for line in details.split("\n\n"):
                fungsi.write_to_file(file_path, line)
            fungsi.write_to_file(file_path, "")

    print("Scraping complete. Results saved to:", file_path)
system('cls' if os.name == 'nt' else 'clear')

main_scrapper("https://tekno.kompas.com/gadget", "hasil", "articlestitles.doc")

