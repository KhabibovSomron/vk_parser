from mysql.connector import connect, Error
from model import User, Post, Comment

class DataBase:
    def __init__(self, host, user, password, db_name):
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name
    
    def execute_sql_code(self, sql_code, tuple):
        try:
            with connect(
                host=self.host,
                user=self.user,
                password=self.password
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(sql_code, tuple)
                    connection.commit()
        except Error as e:
            print(e)

    def show_table(self, table_name):
        try:
            with connect(
                host=self.host,
                user=self.user,
                password=self.password
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(f'select * from {self.db_name}.{table_name}')
                    for item in cursor:
                        print(item)
        except Error as e:
            print(e)
    
    def add_post(self, post: Post):
        insert_post_query = f"""
            INSERT INTO {self.db_name}.posts (id_posts, description, views, likes, reposts)
            VALUES
                ({post.id}, %s, {post.views}, {post.likes}, {post.reposts})
        """

        self.execute_sql_code(insert_post_query, (post.description,))
        
        insert_post_images = f"""
            INSERT INTO {self.db_name}.images (url, post_id)
            VALUES (%s, {post.id})
        """
        for image in post.images:
            self.execute_sql_code(insert_post_images, (image,))

    
    def add_comment(self, comment: Comment):
        if comment.parent_id != None:
            insert_comment_query = f"""
                INSERT INTO {self.db_name}.comments (id_comments, from_id, content, post_id, parent)
                VALUES ({comment.comment_id}, {comment.from_id}, %s, {comment.post_id}, {comment.parent_id})
            """
        else:
            insert_comment_query = f"""
                INSERT INTO {self.db_name}.comments (id_comments, from_id, content, post_id)
                VALUES ({comment.comment_id}, {comment.from_id}, %s, {comment.post_id})
            """

        self.execute_sql_code(insert_comment_query, (comment.content, ))

    def add_user(self, user: User):

        insert_user_query = f"""
            INSERT INTO {self.db_name}.users (id_users, first_name, last_name)
            VALUES ({user.id}, %s, %s)
        """

        self.execute_sql_code(insert_user_query, (user.first_name, user.last_name))