import requests
from bs4 import BeautifulSoup
from P4_1 import fungsi

def main_scraper(url, directory, limit=10):
    fungsi.create_directory(directory)
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
   
    parent_div = soup.find("div", {"class": "grid-row list-content list-content--column"})
    
    elements = []
    if parent_div:
        for i in range(1, limit + 1):
            id_selector = f"rec_loop_{i}"
            article = parent_div.find("article", {"id": id_selector})
            if article:
                elements.append(article)
    
    print(f"Found {len(elements)} articles")
    for index, element in enumerate(elements):
        print(f"Article {index + 1}: {element.get('id')}")
    
    return elements

if __name__ == "__main__":
    main_scraper("https://www.detik.com/", "test")

# import requests
# from bs4 import BeautifulSoup
# from P4_1 import fungsi

# def main_scraper(url, directory, limit=10):
#     fungsi.create_directory(directory)
#     response = requests.get(url)
#     response.raise_for_status()
#     soup = BeautifulSoup(response.text, 'html.parser')
   
#     # Debug: Check if parent div exists
#     parent_divs = soup.find_all("div", {"class": "grid-row list-content list-content--column"})
#     print(f"Found {len(parent_divs)} parent divs")
    
#     # Debug: Check if articles exist anywhere in the page
#     all_articles = soup.find_all("article", id=True)
#     print(f"Found {len(all_articles)} articles with IDs on the page")
#     for article in all_articles[:5]:  # Show first 5
#         print(f"  - {article.get('id')}")
    
#     # Try finding articles with rec_loop pattern anywhere
#     import re
#     rec_articles = soup.find_all("article", {"id": re.compile(r"rec_loop_\d+")})
#     print(f"\nFound {len(rec_articles)} articles with rec_loop_ pattern")
    
#     elements = []
    
#     # Method 1: Try finding in first parent div
#     if parent_divs:
#         parent_div = parent_divs[0]
#         print(f"\nSearching inside first parent div...")
#         for i in range(1, limit + 1):
#             id_selector = f"rec_loop_{i}"
#             article = parent_div.find("article", {"id": id_selector})
#             if article:
#                 elements.append(article)
#                 print(f"  Found: {id_selector}")
    
#     # Method 2: If nothing found, try searching entire page
#     if not elements:
#         print("\nNothing found in parent div, searching entire page...")
#         for i in range(1, limit + 1):
#             id_selector = f"rec_loop_{i}"
#             article = soup.find("article", {"id": id_selector})
#             if article:
#                 elements.append(article)
#                 print(f"  Found: {id_selector}")
    
#     print(f"\nTotal found: {len(elements)} articles")
#     return elements

# if __name__ == "__main__":
#     main_scraper("https://www.detik.com/", "test")