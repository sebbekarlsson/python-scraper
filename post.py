class Post:
    def __init__(self, connection, title, content, type):
        self.title = title
        self.content = content
        self.connection = connection
        self.type = type

    def save(self):
        c = self.connection.cursor()
        c.execute("SELECT post_title FROM posts WHERE post_title='"+self.title+"'")
        post = c.fetchone()

        if post == None:
            c.execute("INSERT INTO posts (post_title, post_content, post_type) VALUES('"+self.title+"', '"+self.content+"', '"+self.type+"')")
            self.connection.commit()