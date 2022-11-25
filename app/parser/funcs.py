import re
from urllib.error import URLError
from urllib.request import urlopen
from bs4 import BeautifulSoup



class Funcs:

    def __init__(self, url_path=None):
        self.url_path = url_path

    def send_request(self, url_path=None):
        try:
            html = urlopen(url_path) if url_path else urlopen(self.url_path)
            bs = BeautifulSoup(html.read(), features="html.parser")
        except URLError:
            return ValueError("URL Error")
        else:
            return bs

    def start_kr(self, url_path=None):
        html = self.send_request("https://ru.wikipedia.org"+ url_path) if url_path else self.send_request()
        links = html.findAll('a', href=re.compile('^(/wiki/)((?!:).)*$'))
        tem=[]
        for link in links:
            if "href" in link.attrs:
                tem.append(link)

        return tem

    def read_page(self, url_path=None):
        url_path = f'https://ru.wikipedia.org{url_path}' if url_path else url_path
        try:

            html = self.send_request(url_path)
            ph = html.find('h1', {'id': 'firstHeading'}).get_text()
            pb = html.find('div', {'class': 'mw-parser-output'}).find('p').get_text()

        except AttributeError as e:
            print(f'Error: {e}')
        else:
            return ph, pb