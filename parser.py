from bs4 import BeautifulSoup
import urllib2
from urlparse import urljoin
import sqlite3
from post import Post

class Parser:
    def __init__(self, url):
        self.urls = []
        self.urls.append(url)

        self.connection = sqlite3.connect('data.db')
        self.setup_database(self.connection)

    def run(self):
        for url in self.urls:
            print url

            opener = urllib2.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)')]
            response = opener.open(url)

            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')

            links = soup.find_all('a')

            post = Post(self.connection, url, url)
            post.save()

            for link in links:
                href = urljoin(url, link.get('href'))
                if href.startswith("http") or href.startswith("https"):
                    self.urls.append(href)

            self.urls.remove(url)

    def setup_database(self,connection):
        c = connection.cursor()

        table = "CREATE TABLE IF NOT EXISTS posts (post_id integer PRIMARY KEY, post_title varchar(120), post_content varchar(360), post_date timestamp)"
        c.execute(table)

        connection.commit()
