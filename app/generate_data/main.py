import random

from app.auth.models import Post, User, Profile
from app.auth.utils import get_avatar
from app.generate_data.utils import (generate_random_name,
                                     generate_random_email,
                                     generate_random_password,
                                     generate_random_city,
                                     generate_users_posts)


def write_to_profile(avatar, info, city, age):
    """ Populate the profile table in the database """
    profile = Profile(avatar=avatar,
                      info=info,
                      city=city,
                      age=age)
    profile.save()
    return profile.id


def write_to_user(username, email, password, profile_id, role=1):
    """ Populate the user table in the database """
    user = User(username=username,
                email=email,
                password=password,
                role=role,
                profile=profile_id)
    user.save()


def write_to_post(title, content, user_id):
    """ Populate post table in database """
    post = Post(title=title,
                content=content,
                author=user_id)
    post.save()


def database_cleanup():
    """ Delete admin, users and posts """
    Post().delete().execute()
    User().delete().execute()
    Profile().delete().execute()


def create_admin():
    """ Create admin """
    username_admin = 'Andrii'
    email_admin = 'admin_level_god@mail.com'
    avatar_admin = get_avatar(email_admin)
    age_admin = '88'
    city_admin = 'Kharkiv'
    info_admin = 'hello, itea'
    password_admin = generate_random_password()

    profile_id = write_to_profile(avatar_admin, info_admin, city_admin, age_admin)
    write_to_user(username_admin, email_admin, password_admin, profile_id, role=2)

    return email_admin, password_admin


def create_users():
    """ Create users  """
    for data in range(20):
        username_generate = generate_random_name()
        email_generate = generate_random_email(username_generate)
        avatar_generate = get_avatar(email_generate)
        age_generate = '88'
        city_generate = generate_random_city()
        info_generate = 'hello, python'
        password_generate = generate_random_password()

        profile_id = write_to_profile(avatar_generate, info_generate, city_generate, age_generate)
        write_to_user(username_generate, email_generate, password_generate, profile_id)


def create_blog():
    """ Create posts """
    users = User.select()
    for data in range(20):
        user_id = random.choice([user.id for user in users])
        content_generate = generate_users_posts()
        title_generate = content_generate[:25].capitalize()

        write_to_post(title_generate, content_generate, user_id)


def create_data():
    """ Create admin, users and posts """
    database_cleanup()

    email_admin, password_admin = create_admin()
    create_users()
    create_blog()
    return email_admin, password_admin
