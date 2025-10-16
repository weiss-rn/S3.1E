import requests
from bs4 import BeautifulSoup
from P4_1 import fungsi 

def main_scraper(url, directory):
    fungsi.create_directory(directory)
    source_code = requests.get(url)
    source_code.raise_for_status()
    soup = BeautifulSoup(source_code.text, 'html.parser')
    elements = soup.find_all(
        "div",
        {"class": "grid-row list-content list-content--column"},
        "article",
        {"class": "list-content__item column-4 recommendation_secondrow"}
    )
    print(elements)

if __name__ == "__main__":
    main_scraper("https://www.detik.com/", "test")