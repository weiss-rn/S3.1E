from bs4 import BeautifulSoup

## P3.1
# html = "<div>Hello, Sekai!</div>"
# soup = BeautifulSoup(html, "html.parser")
# print(soup.p.text)

## P3.2
# html = """
# <div>This is a div</div>
# <p>This is a paragraph</p>
# <p>This is another paragraph</p>
# """
# soup = BeautifulSoup(html, "html.parser")
# print(soup.div.text)
# print(soup.find_all("p"))
# print(soup.find_all("div")[1])

## P3.3
# html = """
# <div>This is a div</div>
# <p>This is a paragraph</p>
# <div class="test">This is a div with a class</div>
# <p>This is another paragraph</p>
# """
# soup = BeautifulSoup(html, "html.parser")
# print(soup.find_all(class_="test"))

# Literally you can't find ID because it was never defined
# print(soup.find_all("P", id="first"))

## P3.4
# html = """
# <div id="d1" class="wide">
#     <p>This is a paragraph</p>
#     <img src="image.jpg" id="img1">
#     <p>This is another paragraph</p>
#     <a href="https://www.google.com">Google</a>
# </div>
# <div id="d2" class="small">
#     <p>This is a paragraph</p>
#     <img src="image.jpg" id="img2">
#     <p>This is another paragraph</p>
#     <a href="https://www.google.com">Google</a>
# </div>
# <div class="test">This is a div with a class</div>
# <p>This is another paragraph</p>
# """
# soup = BeautifulSoup(html, "html.parser")
# divs = soup.find_all('div', {'id': 'd1'})
# print(divs[0].p.text)

## P3.5
# html = """
#     <div id="d1" class="wide">
#         <p id='p1'>This is a paragraph</p>
#         <div><p>OK</p></div>
#         <img src="image.jpg" id="img1">
#         <a href="https://www.google.com">Google</a>
#     </div>
#         <div id="d1" class="small">
#         <p id='p1'>This is a paragraph</p>
#         <div><p>KO</p></div>
#         <img src="image.jpg" id="img2">
#         <a href="https://www.google.com">Google</a>
#     </div>-
# """
# soup = BeautifulSoup(html, "html.parser")
# divs = soup.find_all("div", {"id": "d1"})[1].div.p.text
# print(divs)

## P3.6
# html4 = """
#     <div>div1</div>
#     <div>div2</div>
#     <div>div3</div>
#     <div>div4</div>
#     <div>div5</div>
#     <div>div6</div>
#     <div>div7</div>
#     <div>div8</div>
#     <div>div9</div>
#     <div>div10</div>
# """
# soup = BeautifulSoup(html4, "html.parser")


# all_divs_2 = soup.find_all("div")
# divs = [div.text for i, div in enumerate(all_divs_2) if i % 2 == 0]
# print(divs)


## Pencarian Alternatif
# divx = soup.find_all("div")
# for i in range(0, len(divx), 2):
#     print(divx[i].text)

# divs = soup.find_all("div")[1::2]
# for div in divs:
#     print(div.text)

# print(soup.find_all("div")[1::2])

# divs = soup.find_all("div")[::2]
# for div in divs:
#     print(div.text)

# all_divs = soup.find_all("div")
# for i, div in enumerate(all_divs):
#     if i % 2 == 0:
#         print(div.text)

# even_divs = [tag for i, tag in enumerate(soup.find_all("div")) if i % 2 == 0]
# print(even_divs)

# even_divs_css = soup.select("div:nth-of-type(2n+1)")
# print(even_divs_css)
