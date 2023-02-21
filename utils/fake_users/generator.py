import random
import string
from random import choice
from typing import NamedTuple

from faker import Faker
from faker.providers import BaseProvider
from password_generator import PasswordGenerator

from app.auth.utils import get_avatar


class ProfileDTO(NamedTuple):
    username: str
    email: str
    password: str
    info: str
    city: str
    age: int
    avatar: str
    role: str


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


def generate_users_posts():
    """ Generating random posts using 'ascii_lowercase + .?!,' """
    characters = string.ascii_lowercase + " "
    punctuation = ".?!, "

    post = []
    post_length = random.randint(20, 50)
    while len(post) < post_length:
        sentence_length = random.randint(10, 30)
        sentence = ''.join(random.choice(characters) for _ in range(sentence_length)).capitalize()
        sentence += random.choice(punctuation)
        post.append(sentence)
    blog_post = ' '.join(post)

    return blog_post


fake = Faker()
fake.add_provider(RoleProvider)

# print(fake.profile())
# print(generate_profiles(2))


# print(generate_age())
