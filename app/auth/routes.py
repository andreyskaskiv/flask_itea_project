from flask import render_template, request, redirect, flash, url_for
from flask_login import login_required, logout_user, current_user, login_user

from app.auth import auth
from app.auth.forms import LoginForm, RegisterForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from app.auth.models import User, Role, Profile
from app.auth.utils import save_picture, get_avatar, send_reset_email


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

@auth.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.select().where(User.email == form.email.data).first()
        send_reset_email(user)

        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_request.html', title='Reset Password', form=form)


@auth.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('auth.reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password = form.password.data
        db.session.commit()

        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_token.html', title='Reset Password', form=form)