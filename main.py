import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


def get_data() -> None:

    headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Origin': 'https://www.givenchybeauty.com',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://www.givenchybeauty.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    }
    base_url = 'https://www.givenchybeauty.com'
    sections_urls = [
            '/%D0%BF%D0%B0%D1%80%D1%84%D1%8E%D0%BC%D0%B5%D1%80%D0%B8%D1%8F/',
            '/%D0%BC%D0%B0%D0%BA%D0%B8%D1%8F%D0%B6/',
            '/%D1%83%D1%85%D0%BE%D0%B4-%D0%B7%D0%B0-%D0%BA%D0%BE%D0%B6%D0%B5%D0%B9/' 
            ]
    categories_names = []
    products_names = []
    products_descriptions = []
    products_hrefs = []
    session = requests.Session()
    
    print('>> [INFO] Parsing products links...')
    for section_url in sections_urls:
        response = session.get(('https://www.givenchybeauty.com/ru' +
                section_url), headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        hrefs = [base_url + a['href'] for a in soup.find_all("a",
            class_="giv-ProductTile-link", href=True)]
        products_hrefs += hrefs

    print('>> [INFO] Parsing products info...')
    for product_href in products_hrefs:
        response = session.get(product_href, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        products_names.append(soup.find(class_='product-name').get_text())
        categories_names.append(soup.find(class_='giv-ProductContent-productTypology').get_text())
        products_descriptions.append(soup.find(class_='giv-ProductDescription-contentDetail-Detail-contentText').get_text())

    
    data = {
           'Products_names': products_names,
           'Categories_names': categories_names,
           'Products_descriptions': products_descriptions,
           'Links': products_hrefs 
           }
    df = pd.DataFrame(data)
    df.to_excel('./gvnch_products.xlsx')


def main() -> None:
    current_time = datetime.now().strftime('%H:%M:%S')
    print(f'>> [INFO] {current_time}. Start parsing.')
    get_data()
    current_time = datetime.now().strftime('%H:%M:%S')
    print(f'>> [INFO] {current_time}. Finished.')


if __name__ == '__main__':
    main()

