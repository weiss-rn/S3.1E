from selenium import webdriver

url = "http://id.indeed.com/"
params = {
    'q': 'front end developer',
    'l': 'Malang, East Java',
    'radius': '25'
}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0'}
driver = webdriver.Firefox()
full_url = f"{url}&q={params['q']}&l={params['l']}"
driver.get(full_url)
html = driver.page_source

print(html)

