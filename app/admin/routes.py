from flask import render_template, flash, redirect, url_for, abort, request
from flask_login import login_required, current_user
from flask_paginate import Pagination, get_page_args, get_page_parameter

from app.admin import admin
from app.admin.forms import EditUserForm
from app.auth.models import User, Profile, Role, Post



@admin.route('/index')
@login_required
def show_users():
    """Show users information"""

    per_page = 8
    page = request.args.get(get_page_parameter(), type=int, default=1)
    total = User.select().count()
    pagination = Pagination(page=page, per_page=per_page, total=total, record_name='users')

    users = User.select().paginate(page, per_page)

    return render_template('admin/show_users.html',
                           title='Show users',
                           users=users,
                           pagination=pagination)


@admin.route('/edit/user/<int:user_id>', methods=['GET'])
@login_required
def edit_user(user_id: int):
    """Edit user"""
    if not current_user.is_admin():
        abort(403)

    user = User.select().where(User.id == user_id).first()
    if not user:
        abort(404)

    form = EditUserForm()
    form.id.label.text = ''
    form.id.data = user.id
    form.username.data = user.username
    form.email.data = user.email
    return render_template(
        'admin/edit_user.html',
        title=f'Edit user {user.username}',
        form=form
    )


@admin.route('/update/user', methods=['POST'])
@login_required
def update_user():
    form = EditUserForm()
    if form.validate_on_submit():

        user = User.get(User.id == int(form.id.data))

        user.username = form.username.data
        user.email = form.email.data.strip().lower()
        user.role = int(form.role.data)

        user.save()

        flash(f'{user.username} updated', 'success')
    else:
        flash(f'{form.errors}', 'danger')

    return redirect(url_for('admin.show_users'))


@admin.route('/delete/users', methods=['POST'])
@login_required
def delete_users():
    """Delete selected users"""
    if not current_user.is_admin():
        flash('You don\'t have access to delete users', 'error')
        return redirect(url_for('admin.show_users'))

    selectors = list(map(int, request.form.getlist('selectors')))

    if current_user.id in selectors:
        flash('You can\'t delete yourself use profile page for this', 'warning')
        return redirect(url_for('admin.show_users'))

    if not selectors:
        flash('Nothing to delete', 'warning')
        return redirect(url_for('admin.show_users'))

    message = 'Deleted: '
    for selector in selectors:
        user = User.get(User.id == selector)
        profile = Profile.get(Profile.id == user.profile.id)

        message += f'{user.email} '

        Post.delete().where(Post.author == user).execute()
        user.delete_instance()
        profile.delete_instance()
    flash(message, 'info')
    return redirect(url_for('admin.show_users'))
