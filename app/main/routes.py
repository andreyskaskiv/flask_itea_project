from flask import render_template, current_app

from app.auth.models import Role, Profile, Post, User
from app.main import main


@main.route('/')
def index():
    db = current_app.config['db']
    db.create_tables([Role, Profile, Post, User])

    if not Role.select().where(Role.name == 'user').first():
        roles = [
            ('user',),
            ('admin',)
        ]
        Role.insert_many(roles, fields=[Role.name]).execute()

    title = "Home"
    return render_template('main/index.html',
                           title=title)
