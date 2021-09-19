import re
import requests
from bs4 import BeautifulSoup
import json

bicycles_urls = ['https://www.lapierre-bike.cz/produkt/overvolt-explorer-64-w-b400/4990',
                 'https://www.lapierre-bike.cz/produkt/esensium-22-w-m250/5946',
                 'https://www.lapierre-bike.cz/produkt/lapierre-ezesty-am-ltd-ultimate/5951',
                 'https://www.lapierre-bike.cz/produkt/lapierre-prorace-20-girl/5988',
                 'https://www.lapierre-bike.cz/produkt/lapierre-prorace-49/5978'
                 ]

HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
           }

HOST = 'https://www.lapierre-bike.cz'


def scrape_product_detail_page(product_detail_url, url):
    soup = BeautifulSoup(product_detail_url, 'lxml')
    main_info = soup.find("div", class_="center")
    price = soup.find('div', class_='cena')
    further_info = soup.find('table', class_='spec').find_all('td')
    weight_info = soup.find_all('td')
    additional_pics = soup.find_all('a', class_='html5lightbox')

    weight = None
    photos = []

    for photo in additional_pics:
        photos.append(photo.find('img').get('src'))

    if len(photos) == 0:
        photos = None

    for i in weight_info:
        a = (re.findall(r'\d+\D\d.kg', str(i)))
        if len(a) > 0:
            weight = a[0]

    bicycle = {'model': main_info.find("h1").text,
               'url': url,
               'main_photo_path': main_info.find('img').get('src'),
               'additional_photo_paths': photos,
               'price': price.find('span').text.replace('.', '').replace('CZK', '').strip(),
               'model_year': further_info[2].text,
               'parameters': {
                'weight': weight,
                'frame': further_info[5].text
            }

            }
    return bicycle


def main():
    bicycles_details = []
    for url in bicycles_urls:
        html = requests.get(url, headers=HEADERS)
        if html.status_code == 200:

            bicycles_details.append(scrape_product_detail_page(html.text, url))

        else:
            print('Error')

    with open('top-5-bikes.json', 'w') as file:
        json.dump(bicycles_details, file, indent=2, ensure_ascii=False)
    print(bicycles_details)


if __name__ == '__main__':
    main()
