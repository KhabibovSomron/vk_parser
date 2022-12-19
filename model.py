class Post:
    def __init__(self, description, id, images, comments, views, likes, reposts, owner_id):
        self.description = description
        self.id = id
        self.images = images
        self.comments = comments
        self.views = views
        self.likes = likes
        self.reposts = reposts
        self.owner_id = owner_id    

class Comment:
    def __init__(self, from_id, comment_id, post_id, parent_id, content):
        self.from_id = from_id
        self.comment_id = comment_id
        self.post_id = post_id
        self.parent_id = parent_id
        self.content = content

class User:
    def __init__(self, id, first_name, last_name):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name  