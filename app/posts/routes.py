from flask import render_template, redirect, flash, url_for, request, abort
from flask_login import current_user, login_required
from flask_paginate import Pagination, get_page_parameter

from app.auth.models import Post, User
from app.posts import posts
from app.posts.forms import PostForm


@posts.route("/")
def blog():
    per_page = 5
    page = request.args.get(get_page_parameter(), type=int, default=1)
    total = Post.select().count()
    pagination = Pagination(page=page, per_page=per_page, total=total, record_name='users')
    posts = Post.select().paginate(page, per_page).order_by(Post.date_posted.desc())

    title = "Blog"
    return render_template('posts/blog.html',
                           posts=posts,
                           title=title,
                           pagination=pagination)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data,
                    author=current_user.id)
        post.save()

        flash('Your posts has been created!', 'success')
        return redirect(url_for('posts.blog'))

    return render_template('posts/create_post.html',
                           title='New Post',
                           form=form,
                           legend='New Post')


@posts.route("/post/<int:post_id>")
def show_post(post_id):
    post = Post.select().where(Post.id == post_id).first()
    if not post:
        abort(404)

    return render_template('posts/posts.html',
                           title=post.title,
                           post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    posts = Post.select().where(Post.id == post_id).first()
    if not posts:
        abort(404)

    if posts.author != current_user:
        abort(403)

    form = PostForm()
    if form.validate_on_submit():
        posts.title = form.title.data
        posts.content = form.content.data
        posts.save()

        flash('Your posts has been updated!', 'success')
        return redirect(url_for('posts.show_post', post_id=posts.id))

    elif request.method == 'GET':
        form.title.data = posts.title
        form.content.data = posts.content
    return render_template('posts/create_post.html',
                           title='Update Post',
                           form=form,
                           legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    posts = Post.select().where(Post.id == post_id).first()
    if not posts:
        abort(404)

    if posts.author != current_user:
        abort(403)

    posts.delete().where(Post.id == post_id).execute()
    flash('Your posts has been deleted!', 'success')
    return redirect(url_for('posts.blog'))


@posts.route("/user/<string:username>")
def user_posts(username):
    user = User.select().where(User.username == username).first()

    if not user:
        abort(404)

    per_page = 5
    page = request.args.get(get_page_parameter(), type=int, default=1)
    total = (Post
             .select()
             .where(Post.author == user)).count()

    pagination = Pagination(page=page, per_page=per_page, total=total, record_name='posts')

    posts = (Post
             .select()
             .where(Post.author == user)
             .paginate(page, per_page)
             .order_by(Post.date_posted.desc()))

    return render_template('posts/user_posts.html',
                           title="Title author",
                           user=user,
                           posts=posts,
                           pagination=pagination)
