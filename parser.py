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

            opener = urllib2.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)')]
            response = opener.open(url)

            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')

            links = soup.find_all('a')

            for link in links:
                href = urljoin(url, link.get('href'))
                if href.startswith("http") or href.startswith("https"):
                    self.urls.append(href)

            self.urls.remove(url)