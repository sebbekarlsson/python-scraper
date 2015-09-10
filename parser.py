from bs4 import BeautifulSoup
import urllib2
import urllib as urllib
from urlparse import urljoin
import sqlite3
from post import Post
import re as re
from threading import Lock
import yaml
import os

class Parser:
    def __init__(self, url, config):
        self.urls = []
        self.urls.append(url)
        self.config = config

        self.connection = sqlite3.connect('data.db')
        self.setup_database(self.connection)

        self.lock = Lock()

        self.extensions =\
        [
        '.jpg',
        '.jpeg',
        '.png',
        '.bmp',
        '.txt'
        ]

    def download_file(self, url, f):
        testfile = urllib.URLopener()
        testfile.retrieve(url, f)

    def basename(self, src):
        fname = os.path.basename(src)
        if '?' in fname:
            fname = fname.split('?')[0]
        if '.' in fname:
            return fname
        return None

    def get_new_url(self):
        #c = self.connection.cursor()
        #c.execute("SELECT * FROM posts WHERE post_type='url' AND post_content='{content}'".format(content=url))
        #self.connection.commit()
        #post = c.fetchone()

        #return post == None

    def run(self):
        while 1 == 1:
            try:
                for url in self.urls:
                    self.urls.remove(url)
                    print(url)

                    opener = urllib2.build_opener()
                    opener.addheaders = [('User-agent', 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)')]
                    response = opener.open(url)

                    html = response.read()
                    soup = BeautifulSoup(html, 'html.parser')
                    text = soup.text
                    links = soup.find_all('a')
                    images = soup.find_all('img')

                    post = Post(self.connection, url, url, 'url')
                    post.save()

                    download_path = 'sites/' + url
                    if not os.path.exists(download_path):
                        os.makedirs(download_path)

                    for image in images:
                        print('image')
                        src = urljoin(url, image.get('src'))
                        if src.startswith("http") or src.startswith("https"):
                                fname = self.basename(src)
                                if fname != None:
                                    self.download_file(src, download_path + fname)

                    print('ok')

                    '''self.reset_config()
                    for p in self.config:
                        textElements = re.findall(p['regex'], text)

                        if textElements != None:
                            for element in textElements:
                                post = Post(self.connection, element, element, p['type'])
                                post.save()'''
                    
                    for link in links:
                        href = urljoin(url, link.get('href'))
                        if href.startswith("http") or href.startswith("https"):
                            fname = self.basename(href)
                            if fname in self.extensions:
                                self.download_file(href, download_path + fname)
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
