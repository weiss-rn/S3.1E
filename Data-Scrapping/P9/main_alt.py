from selenium import webdriver
from bs4 import BeautifulSoup
from fungsi import Fungsi
import requests
import os

def main_scraper(url):
    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'}
    driver = webdriver.Chrome()
    full_url = f"{url}"
    driver.get(full_url)
    html = driver.page_source
    soup = BeautifulSoup('html', 'html.parser')
    hasil = soup.find_all("div", class_='latest--news mt2 clearfix')
    
    for i in range(len(hasil)):
        Card = hasil[i].find("div", {'class':'article__list clearfix'})
        Judul = hasil[i].find("a", {'class':'article__link'})
        if Card and Judul:
            print("Card : " + Card.text)
            print("Judul : " + Judul.text)
            print("=====================================")

    Fungsi.create_directory('hasil')
    file_path = os.path.join('hasil', 'kompasparser.txt')
    Fungsi.write_to_file(file_path, 'html')

main_scraper("https://tekno.kompas.com/gadget")