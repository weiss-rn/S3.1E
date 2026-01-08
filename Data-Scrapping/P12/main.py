import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":
    html_doc = requests.get("https://www.detik.com/jatim/berita/indeks")
    soup = BeautifulSoup(html_doc.text, 'html.parser')

    populer_area = soup.find(attrs={'class': 'grid-row list-content'})
    if not populer_area:
        print("Could not find the popular area.")
        exit(1)

    titles = populer_area.find_all(attrs={'class': 'media__title'})
    # images = populer_area.find_all(attrs={'class': 'media__image'})
    images = populer_area.find_all(attrs={'class': 'list-content__item'})

    for image in images:
        title_tag = image.find(attrs={'class': 'media__title'})
        title = title_tag.get_text(strip=True) if title_tag else "No title"
        date_tag = image.find('div', {'class': 'media__date'})
        date = date_tag.find('span')['title'] if date_tag and date_tag.find('span') else "No date"
        img_tag = image.find('a').find('img') if image.find('a') else None
        img_src = img_tag['src'] if img_tag and img_tag.has_attr('src') else "No image"

        print(f"Title: {title}\nDate: {date}\nImage: {img_src}\n")


