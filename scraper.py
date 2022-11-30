import requests
from bs4 import BeautifulSoup


class ScraperCl:

    def __init__(self, url):
        self.url = url  # url of the page
        if self.url is not None and "https://" in self.url:  # check if url is valid
            self.response = requests.get(self.url).text  # get html code of the page
            self.soup = BeautifulSoup(self.response, 'html.parser')  # parse html code
        else:
            self.soup = None

    # Get title of the page
    def get_title(self):
        return self.soup.title.string

 # Get content of the page
    def get_content(self):
        text = []
        for i in self.soup.find_all('p'): # find all paragraphs
            if i.string != '\xa0' and i.string != '\n': # check if paragraph is not empty
                text.append(i.text)
        return text
