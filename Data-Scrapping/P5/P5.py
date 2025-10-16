from bs4 import BeautifulSoup
from P4_1 import fungsi
import os
import requests

def main_scraper(url, directory):
    fungsi.create_directory(directory) #Membuat Directory
    source_code = requests.get(url)
    source_text = source_code.text
    soup = BeautifulSoup(source_text, "html.parser")
    articles = soup.find_all("div", {'class':'article3_box'})
    # articles2 = soup.find_all(True, {'class':['article__box', 'article__title']}) #Penulisan Multiple class

    for article in articles:
        print("URL : " + article.a.get("href"))
        print("Judul : " + article.text)


    # for article2 in articles2:
    #     print ( "-" * 30)
    #     print("URL2 : " + article2.a.get("href"))
    #     print("Judul2 : " + article2.text)
    #     print( "-" * 30)cls

main_scraper("https://tekno.kompas.com/gadget", "Hasil")
