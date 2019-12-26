from flask import Flask
from requests import get
from bs4 import BeautifulSoup

url = 'https://habr.com/'
app = Flask('__main__')


def process_links(content):
    links = content.find_all('a')

    for link in links:
        if 'habr.com' in link['href']:
            link['href'] = link['href'].replace('https://habr.com', 'http://localhost:5000')


def process_texts(content):
    texts = content.find_all(text=True)

    for text in texts:
        new_text = []

        for word in text.split(' '):
            if len(word) == 6:
                word = word + '™'
            new_text.append(word)

        text.string.replace_with(' '.join(new_text))


def process_page(content):
    template = BeautifulSoup(content)

    process_links(template)
    process_texts(template)

    return template


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def server(path):
    response = get(url + path)
    response_type = response.headers['Content-Type']
    content = response.content

    if response_type == 'text/html; charset=UTF-8':
        content = process_page(content)

    return str(content)
