from vk_parser import Parser
import time
from database import DataBase


parser = Parser()

parser.get_posts()
print("Loading complited !")

for post in parser.posts:
    if post.comments != 0:
        parser.get_comments(post, None)
        time.sleep(1)
   

for post in parser.posts:
    print(f"""
        {post.id} {post.description}
        views = {post.views}, likes = {post.likes}, reposts = {post.reposts}, comments = {post.comments}
    """)


print("__________________________________________________________________________________-")

for comment in parser.comments:
    print(f"""
        {comment.comment_id} {comment.content}
        form_id = {comment.from_id}, post_id = {comment.post_id}, parent_id = {comment.parent_id}
    """)


for user in parser.users:
    print(f"""
        {user.id}: {user.first_name} {user.last_name}
    """)

db = DataBase('localhost', 'root', '200habibov', 'vk_database')

for user in parser.users:
    db.add_user(user)
    print("User added !")

for post in parser.posts:
    db.add_post(post)
    print('Post added !')

for comment in parser.comments:
    if comment.parent_id == None:
        db.add_comment(comment)
        print('Comment added !')

for comment in parser.comments:
    if comment.parent_id != None:
        db.add_comment(comment)
        print('Comment added !')