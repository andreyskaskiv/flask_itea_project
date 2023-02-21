import os
import secrets
from hashlib import md5

from PIL import Image
from flask import current_app, url_for
from flask_login import LoginManager
from flask_mail import Message
from flask_mail import Mail

from app.auth.models import User

mail = Mail()

def create_login_manager():
    manager = LoginManager()
    manager.login_view = 'auth.login'

    return manager


login_manager = create_login_manager()
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.select().where(User.id == user_id).first()


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext

    picture_path = os.path.join(current_app.config['BASE_DIR'], 'app\static\profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    path_to_picture = '/static/profile_pics/' + picture_fn
    return path_to_picture


def get_avatar(email, size=128):
    digest = md5(email.lower().encode('utf-8')).hexdigest()
    url = f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
    return url


def is_admin(user_to_check):
    user = User.select().where(User.id == user_to_check.id).first()
    if user.role.name != 'admin':
        return False
    return True


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('auth.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


def get_quantity(obj, offset=0, per_page=10):
    return obj[offset: offset + per_page]
