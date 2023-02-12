from flask import Blueprint

posts = Blueprint('posts', __name__, url_prefix='/posts')

from app.posts import routes