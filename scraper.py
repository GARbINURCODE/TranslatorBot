import requests
from bs4 import BeautifulSoup


class ScraperCl:

    def __init__(self, url):
        self.url = url
        if self.url is not None and "https://" in self.url:
            self.response = requests.get(self.url).text
            self.soup = BeautifulSoup(self.response, 'html.parser')
        else:
            self.soup = None

    def get_title(self):
        return self.soup.title.string

    def get_content(self):
        text = []
        for i in self.soup.find_all('p'):
            if i.string != '\xa0' and i.string != '\n':
                text.append(i.text)
        return text
