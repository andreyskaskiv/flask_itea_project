from flask import render_template, current_app

from app.auth.models import Role, Profile, User
from app.main import main

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@main.route('/')
def index():
    db = current_app.config['db']
    db.create_tables([Role, Profile, User])

    if not Role.select().where(Role.name == 'user').first():
        Role(name='user').save()

    title = "Home"
    return render_template("main/index.html",
                           title=title,
                           posts=posts)


@main.route('/about')
def about():
    info = User.select()
    title = "About"
    return render_template('about/about.html',
                           title=title,
                           list=info)
