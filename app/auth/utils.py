import os
import secrets
from hashlib import md5

from PIL import Image
from flask import current_app


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext

    picture_path = os.path.join(current_app.config['BASE_DIR'], 'app\static\profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def get_avatar(email, size=128):
    digest = md5(email.lower().encode('utf-8')).hexdigest()
    url = f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
    return url
