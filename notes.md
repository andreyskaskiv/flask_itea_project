pip freeze > requirements.txt

pip install -r requirements.txt


pip install python-dotenv


query = Post.select().order_by(Post.date_posted.desc())
for row in query:
    #     print(row.id, row.title, row.content,
    #           row.author.username, row.author.email,
    #           row.author.profile.avatar, row.author.profile.info, row.author.profile.city, row.author.profile.age)