from bs4 import BeautifulSoup
import urllib2
from urlparse import urljoin
import sqlite3
from post import Post
import re as re
from threading import Lock
import yaml

class Parser:
    def __init__(self, url, config):
        self.urls = []
        self.urls.append(url)
        self.config = config

        self.connection = sqlite3.connect('data.db')
        self.setup_database(self.connection)

        self.lock = Lock()

    def run(self):
        while 1 == 1:
            try:
                for url in self.urls:
                    self.urls.remove(url)
                    print url

                    opener = urllib2.build_opener()
                    opener.addheaders = [('User-agent', 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)')]
                    response = opener.open(url)

                    html = response.read()
                    soup = BeautifulSoup(html, 'html.parser')
                    text = soup.text
                    links = soup.find_all('a')

                    post = Post(self.connection, url, url, 'url')
                    post.save()

                    self.reset_config()
                    for p in self.config:
                        textElements = re.findall(p['regex'], text)

                        if textElements != None:
                            for element in textElements:
                                post = Post(self.connection, element, element, p['type'])
                                post.save()
                    
                    for link in links:
                        href = urljoin(url, link.get('href'))
                        if href.startswith("http") or href.startswith("https"):
                            self.urls.append(href)
            except:
                pass
            

    def setup_database(self,connection):
        c = connection.cursor()

        table = "CREATE TABLE IF NOT EXISTS posts (post_id integer PRIMARY KEY, post_title varchar(120), post_content varchar(360), post_type varchar(120), post_date timestamp DEFAULT CURRENT_TIMESTAMP)"
        c.execute(table)

        connection.commit()

    def reset_config(self):
        self.config = yaml.load_all(open('config.yaml', 'r'))
