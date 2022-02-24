import requests
import csv
from bs4 import BeautifulSoup

URL = "https://www.whtop.com"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                  '98.0.4758.102 Safari/537.36',
    'Accept': '*/*'
}
FIELDS = ['Name', 'Link 1', 'Link 2', 'Location']


def get_html(page=None):
    r = requests.get(url=f"{URL}/directory/{page}", headers=HEADERS, timeout=3)
    with open('test.html', 'w') as f:
        f.write(r.text)


def get_content(result):
    with open('test.html', 'r') as file:
        html = file.read()
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='company clearer')
    for item in items:
        result.append(
            {
                'title': item.find('div', class_='company-title').get_text().split('/')[0],
                'link 1': f"{URL}{item.find('a').get('href')}",
                'link 2': f"{URL}{item.find('a', class_='external visit _frs11').get('href')}",
                'location': item.find('span', class_='gray').get_text()
            }
        )


def save_file(items):
    with open('file.csv', 'a', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(FIELDS)
        for item in items:
            writer.writerow([item.get('title'), item.get('link 1'), item.get('link 2'), item.get('location')])


def main():
    result = []
    for page in range(300, 600):
        try:
            print(page)
            get_html(page=f'pageno/{page}')
            get_content(result)
        except:
            with open('error.txt', 'a')as f:
                f.write(f"{page}\n")
            continue
    save_file(result)


if __name__ == '__main__':
    main()
