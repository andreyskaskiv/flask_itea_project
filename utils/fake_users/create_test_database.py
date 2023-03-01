from typing import NamedTuple

from utils.fake_users.generator import generate_profiles, ProfileDTO


class UsersTestDTO(NamedTuple):
    username: str
    email: str
    password: str
    role: str


class ProfileTestDTO(NamedTuple):
    avatar: str
    info: str
    city: str
    age: int


def generate_users_profiles(profiles: list[ProfileDTO]):
    """"""
    test_profiles = []
    test_users = []

    for profile in profiles:
        role = profile.role
        username = profile.username
        email = profile.email
        info = profile.info
        city = profile.city
        age = profile.age
        password = profile.password
        avatar = profile.avatar
        test_profiles.append(ProfileTestDTO(avatar, info, city, age))
        test_users.append(UsersTestDTO(username, email, password, role))

    return test_users, test_profiles


USERS, PROFILES = generate_users_profiles(generate_profiles(20))

ROLES = ['user', 'admin']

