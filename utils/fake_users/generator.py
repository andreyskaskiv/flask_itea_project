import random
from random import choice
from typing import NamedTuple

from faker import Faker
from faker.providers import BaseProvider
from password_generator import PasswordGenerator

from app.auth.utils import get_avatar
from utils.fake_users.generator_text import Text


class ProfileDTO(NamedTuple):
    username: str
    email: str
    password: str
    info: str
    city: str
    age: int
    avatar: str
    role: str


class BlogDTO(NamedTuple):
    title: str
    post: str


class RoleProvider(BaseProvider):
    roles = ('user', 'admin')

    def role(self) -> str:
        return choice(self.roles)


def generate_password(min_len: int = 10, max_len: int = 15):
    generator = PasswordGenerator()
    generator.minlen = min_len
    generator.maxlen = max_len
    return generator.generate()


def generate_age():
    return random.randint(20, 50)


def generate_profiles(qty: int) -> list[ProfileDTO]:
    """
    :param qty: amount of generated data
    :return: ProfileDTO(username, email, password, info, city, age, avatar, role)
    """
    profiles = []

    for _ in range(qty):
        profile = fake.profile()
        role = fake.role()
        username = profile['username']
        email = profile['mail']
        info = profile['job']
        city = profile['address']
        age = generate_age()
        password = generate_password()
        avatar = get_avatar(email)
        profiles.append(
            ProfileDTO(username, email, password, info, city, age, avatar, role))
    return profiles


def generate_blogs(qty: int, post_length: int = 20) -> list[BlogDTO]:
    """
    @param qty: amount of generated data,
    @param post_length: post length or number of sentences
    @return: BlogDTO(title, post)
    """
    blogs = []

    for _ in range(qty):
        title = text.title()
        post = text.text(post_length)
        blogs.append(
            BlogDTO(title, post))

    return blogs


fake = Faker()
fake.add_provider(RoleProvider)
text = Text()

# print(fake.profile())
# print(generate_profiles(2))

# print(generate_age())


# print(dir(text))
# print(text.title())
# print(text.text())

# print(generate_profiles(1))

