from bs4 import BeautifulSoup
import os
import requests

url = "https://id.indeed.com"
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0' }

def get_total_pages():
    param = {
        'q': 'web developer',
        'l': 'Malang', 
        'vjk':'aff1cac2a018d658' 
    }

    res = requests.get(url, params=param, headers=headers)
    try:
        os.mkdir("temp")
    except FileExistsError:
        pass

    with open('temp/rest.html', 'w+', encoding='utf-8') as outfile:
        outfile.write(res.text)
        outfile.close()

    soup = BeautifulSoup(res.text, 'html.parser')
    print(soup.prettify())

if __name__ == "__main__":
    get_total_pages()
