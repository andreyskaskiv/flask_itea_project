import json

from app.auth.models import User, Role, Profile, Post
from app.weather.models import UserCity
from definitions import PATH_TO_CREDENTIALS
from utils.fake_users.generator import ProfileDTO, BlogDTO, generate_profiles, generate_blogs


def clear_db():
    """Clearing the database before creating"""
    UserCity().delete().execute()
    Post().delete().execute()
    User.delete().execute()
    Role.delete().execute()
    Profile.delete().execute()


def write_to_db(profiles: list[ProfileDTO], blogs: list[BlogDTO]):
    """Filling the database with fake data"""
    if not Role.select().where(Role.name == 'user').first():
        roles = [
            ('user',),
            ('admin',)
        ]
        Role.insert_many(roles, fields=[Role.name]).execute()

    for profile, blog in zip(profiles, blogs):
        role = Role.select().where(Role.name == profile.role).first()

        profile_entity = Profile(avatar=profile.avatar,
                                 info=profile.info,
                                 city=profile.city,
                                 age=profile.age)
        profile_entity.save()
        user = User(username=profile.username,
                    email=profile.email,
                    password=profile.password,
                    role=role,
                    profile=profile_entity)
        user.save()

        post = Post(title=blog.title,
                    content=blog.post,
                    author=user.id)
        post.save()


def prepare_user_credentials(users: list[ProfileDTO]):
    """ Fetching data (username, email, password, role) to write to jason """
    users_prepared_to_json = []
    for user in users:
        temp = {
            'username': user.username,
            'email': user.email,
            'password': user.password,
            'role': user.role
        }
        users_prepared_to_json.append(temp)
    return users_prepared_to_json


def write_user_credentials_to_json(users: list[dict[str, str]], json_file: str):
    with open(json_file, 'w') as file:
        json.dump(users, file, indent=4)


def main(qty: int):
    clear_db()
    profiles = generate_profiles(qty)
    blogs = generate_blogs(qty)
    write_to_db(profiles, blogs)
    users_prepared_to_json = prepare_user_credentials(profiles)
    write_user_credentials_to_json(users_prepared_to_json, PATH_TO_CREDENTIALS)
