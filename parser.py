from bs4 import BeautifulSoup
import urllib2
from urlparse import urljoin

class Parser:
    def __init__(self, url):
        self.urls = []
        self.urls.append(url)

    def run(self):
        for url in self.urls:
            print url

            response = urllib2.urlopen(url)
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')

            links = soup.find_all('a')

            for link in links:
                href = urljoin(url, link.get('href'))
                if href.startswith("http") or href.startswith("https"):
                    self.urls.append(href)

            self.urls.remove(url)