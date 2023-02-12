from flask import render_template, request, redirect, flash, url_for
from flask_login import login_required, logout_user, current_user, login_user

from app.auth import auth
from app.auth.forms import LoginForm, RegisterForm, UpdateAccountForm
from app.auth.models import User, Role, Profile
from app.auth.utils import save_picture, get_avatar


@auth.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.select().where(User.email == form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)
            user.save()
            return redirect(request.args.get("next") or url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    title = "Login"
    return render_template("auth/login.html",
                           title=title,
                           form=form)


@auth.route("/register", methods=("POST", "GET"))
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        if not User.select().where(User.email == form.email.data).first():
            user_role = Role.select().where(Role.name == 'user').first()  # Change!!!

            profile = Profile(avatar="default.png",
                              # avatar=get_avatar(form.email.data.lower()),
                              info=form.info.data,
                              city=form.city.data,
                              age=form.age.data)
            profile.save()

            user = User(username=form.username.data,
                        email=form.email.data,
                        password=form.password.data,
                        role=user_role,
                        profile=profile.id)
            user.save()

            flash(f'{user.username} has added')
            return redirect(url_for('auth.login'))

        flash(f"User with this {form.email.data} already exists")

    title = "Registration"
    return render_template("auth/register.html",
                           title=title,
                           form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Bye...", "success")
    return redirect(url_for('auth.login'))


@auth.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():

        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.profile.avatar = picture_file
            current_user.profile.save()
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.save()

        flash('Your account has been updated!', 'success')
        return redirect(url_for('auth.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.profile.avatar)

    return render_template('auth/account.html',
                           title='Account',
                           image_file=image_file,
                           form=form)
