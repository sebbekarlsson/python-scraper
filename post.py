class Post:
    def __init__(self, connection, title, content):
        self.title = title
        self.content = content
        self.connection = connection

    def save(self):
        c = self.connection.cursor()
        c.execute("INSERT INTO posts (post_title, post_content) VALUES('"+self.title+"', '"+self.content+"')")
        self.connection.commit()