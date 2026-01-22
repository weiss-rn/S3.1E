import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/scraped-detik')
def detik():
    try:
        html_doc = requests.get("https://www.detik.com/jatim/berita/indeks")
        soup = BeautifulSoup(html_doc.text, 'html.parser')
        populer_area = soup.find(attrs={'class': 'grid-row list-content'})
        images = populer_area.find_all(attrs={'class': 'list-content__item'})
        
        articles = []
        for image in images:
            try:
                title_tag = image.find(attrs={'class': 'media__title'})
                title = title_tag.get_text(strip=True) if title_tag else "No title"
                
                date_tag = image.find('div', {'class': 'media__date'})
                date = date_tag.find('span')['title'] if date_tag and date_tag.find('span') else "No date"
                
                link_tag = image.find('a')
                img_tag = link_tag.find('img') if link_tag else None
                img_src = img_tag['src'] if img_tag and img_tag.has_attr('src') else "No image"
                
                articles.append({
                    'title': title,
                    'date': date,
                    'image': img_src
                })
            except (AttributeError, KeyError, TypeError):
                continue

        return render_template('detik.html', articles=articles)
    
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

def if_the_list_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

app.jinja_env.filters['valid_prime'] = if_the_list_prime

if __name__ == '__main__':
    app.run(debug=True)