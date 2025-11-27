from bs4 import BeautifulSoup
import requests

url = "https://id.indeed.com"
param = {
    'q': 'web developer',
    'l': 'Malang', 
    'vjk':'aff1cac2a018d658' 
}

headers = { 'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0" }

res = requests.get(url, params=param, headers=headers)
soup = BeautifulSoup(res.text, "html.parser")

print(soup.prettify())