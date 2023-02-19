import random
import string

from app.generate_data.name.parser import run_parser


def generate_random_password(characters_number: int = 20):
    """ Random password generation 'zbjv(7#Q3on\5fNKVx'1' """
    allowed_chars = string.ascii_letters + string.digits + string.punctuation
    random_password = ''.join(random.choice(allowed_chars) for _ in range(characters_number))
    return random_password


def generate_random_name():
    """ Random name generation with baby_names """
    names_parser = run_parser()
    names = names_parser['BoysNames'] + names_parser['GirlsNames']
    return random.choice(names)


def generate_random_email(username_generate: str, characters_number: int = 5):
    """ Random email generation 'sckekxbrlb@gmail.com' """
    allowed_chars = string.ascii_letters + '_'
    random_email = ''.join(random.choice(allowed_chars) for _ in range(characters_number))
    return f"{username_generate}_{random_email}@gmail.com"


def generate_random_city():
    """ Selects a random city from the list """
    citys = ['Kyiv', 'Kharkiv', 'Dnipro', 'Odesa', 'Lviv']
    return random.choice(citys)


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
