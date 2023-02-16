from flask import render_template, current_app
from flask_login import login_required
from flask_paginate import Pagination, get_page_args

from app.auth.models import Role, Profile, Post, User
from app.auth.utils import get_quantity
from app.main import main

@main.route('/')
def index():
    db = current_app.config['db']
    db.create_tables([Role, Profile, Post, User])

    if not Role.select().where(Role.name == 'user').first():
        Role(name='user').save()

    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')

    blog = Post.select().order_by(Post.date_posted.desc())
    total = blog.count()

    pagination_posts = get_quantity(blog, offset=offset, per_page=per_page)

    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')

    title = "Home"
    return render_template('main/index.html',
                           posts=pagination_posts,
                           title=title,
                           page=page,
                           per_page=per_page,
                           pagination=pagination)


@main.route('/about')
@login_required
def about():
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')

    users = User.select()
    total = users.count()

    pagination_users = get_quantity(users, offset=offset, per_page=per_page)

    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')

    return render_template('about/about.html',
                           users=pagination_users,
                           page=page,
                           per_page=per_page,
                           pagination=pagination)
