from flask import render_template, current_app

from app.auth.models import Role, Profile, Post, User
from app.main import main

@main.route('/')
def index():
    db = current_app.config['db']
    db.create_tables([Role, Profile, Post, User])

    if not Role.select().where(Role.name == 'user').first():
        Role(name='user').save()

    query = Post.select()
    for row in query:
        print(row.id, row.title, row.content,
              row.author.username, row.author.email,
              row.author.profile.avatar, row.author.profile.info, row.author.profile.city, row.author.profile.age)

    title = "Home"
    return render_template("main/index.html",
                           title=title,
                           posts=query)


@main.route('/about')
def about():
    query = User.select()
    title = "About"
    return render_template('about/about.html',
                           title=title,
                           list=query)
