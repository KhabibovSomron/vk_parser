import requests
from model import Post, Comment, User

class Parser:
    def __init__(self):
        with open('key.txt', 'r') as file:
            self.key = file.readline()
        
        self.version = 5.131
        self.community_name = 'aniterror'
        self.posts = []
        self.comments = []
        self.users = []

    def get_posts(self):
        offset = 1
        count = 50
        i = 0
        status_code = 200
        while status_code == 200:

            response = requests.get('https://api.vk.com/method/wall.get', params={
                'access_token': self.key,
                'v': self.version,
                'domain': self.community_name,
                'count': count,
                'offset': offset
            })

            status_code = response.status_code

            data = response.json()
            for post in data["response"]['items']:
                id = post["id"]
                description = post["text"]
                images = []
                comments =  post["comments"]["count"]
                views = post["views"]["count"]
                likes = post["likes"]["count"]
                reposts = post["reposts"]["count"]
                owner_id = post["owner_id"]
                # print(f"""
                #     {i}: {id} {description}
                #     comments = {comments['count']}, likes = {likes}, views = {views}, reposts = {reposts}, owner_id = {owner_id}
                # """)
                for image in post['attachments']:
                    image_size_list = image['photo']['sizes']
                    images.append(image_size_list[len(image_size_list) - 1]['url'])
                
                i += 1
                self.posts.append(Post(description, id, images, comments, views, likes, reposts, owner_id))
            
            offset += 1
            if i >= 49:
                status_code = 404

    def get_comments(self, post: Post, comment_id):
    
        count = 100    
        if comment_id != None:
            params={
                'access_token': self.key,
                'v': self.version,
                'owner_id': post.owner_id,
                'post_id': post.id,
                'count': count,
                'extended': '1',
                'comment_id': comment_id
            }
        else:
            params={
                'access_token': self.key,
                'v': self.version,
                'owner_id': post.owner_id,
                'post_id': post.id,
                'count': count,
                'extended': '1',
            }

        response = requests.get('https://api.vk.com/method/wall.getComments', params=params)
        
        comments = response.json()["response"]["items"]
        for comment in comments:
            id = comment["id"]
            from_id = comment["from_id"]
            content = comment["text"]
            post_id = comment.get("post_id")
            if comment_id != None:
                parent = comment["parents_stack"][0]
            else: 
                parent = None
            
            try:
                if comment["thread"]["count"] != 0:
                    self.get_comments(post, id)
            except KeyError:
                pass
            
            self.comments.append(Comment(from_id, id, post_id, parent, content))

        profiles = response.json()["response"]["profiles"]
        users = self.users
        for user in profiles:
            user_id = user["id"]
            first_name = user["first_name"]
            last_name = user["last_name"]
            new_user = User(user_id, first_name, last_name)
            flag = True
            for old_user in self.users:
                if old_user.id == new_user.id:
                    flag = False
            if flag:
                self.users.append(new_user)