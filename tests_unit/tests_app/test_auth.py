import unittest
import warnings
from random import choice

from flask import url_for
from flask_login import login_user, logout_user

from app import create_app
from app.auth.forms import RegisterForm
from app.auth.models import User, Role, Profile
from app.weather.models import UserCity
from utils.fake_users.create_test_database import USERS, PROFILES, ROLES


class UserTestCase(unittest.TestCase):
    profiles_data = None
    users_data = None
    app = None
    ctx = None
    db = None
    roles = None
    user_data = None
    user_profile = None
    admin_data = None
    admin_profile = None

    @classmethod
    def create_tables(cls):
        """Create tables and fill Roles for auth app"""
        cls.db.create_tables([User, Profile, Role, UserCity])

    @classmethod
    def create_roles(cls, roles):
        roles_instances = {}
        for role in roles:
            role_instance = Role(
                name=role
            )
            role_instance.save()
            roles_instances[role] = role_instance.id
        return roles_instances

    @classmethod
    def setUpClass(cls):
        """Before all tests"""
        warnings.filterwarnings(action="ignore", category=ResourceWarning)
        warnings.filterwarnings(action="ignore", category=DeprecationWarning)
        cls.app = create_app('testing')
        cls.app.config['WTF_CSRF_ENABLED'] = False

        cls.db = cls.app.config['db']
        cls.users_data = USERS
        cls.profiles_data = PROFILES
        cls.create_tables()
        cls.roles = cls.create_roles(ROLES)
        cls.user_data = choice([user for user in cls.users_data if user.role == 'user'])
        cls.user_profile = choice(cls.profiles_data)
        cls.admin_data = choice([user for user in cls.users_data if user.role == 'admin'])
        cls.admin_profile = choice(cls.profiles_data)
        cls.ctx = cls.app.test_request_context()
        cls.ctx.push()
        cls.client = cls.app.test_client()

    @classmethod
    def tearDownClass(cls):
        """After all test"""
        cls.ctx.pop()

    def test_01_register_user(self):
        """Register user in auth register"""
        form = RegisterForm(
            username=self.user_data.username,
            email=self.user_data.email,
            age=self.user_profile.age,
            city=self.user_profile.city,
            info=self.user_profile.info,
            password=self.user_data.password,
            password_repeat=self.user_data.password,
            submit='Register'
        )
        response = self.client.post(
            url_for('auth.register'),
            data={
                'username': form.username.data,
                'email': form.email.data,
                'age': form.age.data,
                'city': form.city.data,
                'info': form.info.data,
                'password': form.password.data,
                'password_repeat': form.password.data,
                'submit': form.submit.data
            },
            follow_redirects=True
        )
        code = response.status_code
        data = response.get_data(as_text=True)
        self.assertEqual(code, 200)
        self.assertIn(
            f'{self.user_data.username} has added',
            data)
        self.assertEqual(response.request.path, url_for('auth.login'))
        user = User.select().where(User.username == self.user_data.username).first()
        self.assertTrue(user)

    def test_02_register_admin(self):
        """Register admin in auth register"""
        form = RegisterForm(
            username=self.admin_data.username,
            email=self.admin_data.email,
            age=self.admin_profile.age,
            city=self.admin_profile.city,
            info=self.admin_profile.info,
            password=self.admin_data.password,
            password_repeat=self.admin_data.password,
            submit='Register'
        )
        response = self.client.post(
            url_for('auth.register'),
            data={
                'username': form.username.data,
                'email': form.email.data,
                'age': form.age.data,
                'city': form.city.data,
                'info': form.info.data,
                'password': form.password.data,
                'password_repeat': form.password.data,
                'submit': form.submit.data
            },
            follow_redirects=True
        )
        code = response.status_code
        data = response.get_data(as_text=True)
        self.assertEqual(code, 200)
        self.assertIn(
            f'{self.admin_data.username} has added',
            data)
        self.assertEqual(response.request.path, url_for('auth.login'))
        user = User.select().where(User.username == self.admin_data.username).first()
        self.assertTrue(user)

    def test_03_register_user_invalid_username(self):
        """Register user in auth register with invalid name"""
        response = self.client.post(
            url_for('auth.register'),
            data={'username': '1',
                  'email': 'sandersjames@hotmail.com',
                  'info': 'Chiropractor',
                  'age': '36',
                  'city': 'PSC 8593, Box 9778\nAPO AA 35289',
                  'password': 'P>$f5jF6mZ',
                  'password_repeat': 'P>$f5jF6mZ',
                  'submit': 'Register'},
            follow_redirects=True)
        code = response.status_code
        data = response.get_data(as_text=True)
        self.assertEqual(code, 200)
        self.assertIn(
            'Usernames must have only letters, numbers, underscores',
            data)
        self.assertEqual(response.request.path, url_for('auth.register'))

    def test_04_register_user_with_exist_username(self):
        """Register user in auth register with exist username"""
        response = self.client.post(
            url_for('auth.register'),
            data={'username': self.user_data.username,
                  'email': 'sandersjames@hotmail.com',
                  'info': 'Chiropractor',
                  'age': '36',
                  'city': 'PSC 8593, Box 9778\nAPO AA 35289',
                  'password': 'P>$f5jF6mZ',
                  'password_repeat': 'P>$f5jF6mZ',
                  'submit': 'Register'},
            follow_redirects=True)
        code = response.status_code
        data = response.get_data(as_text=True)
        self.assertEqual(code, 200)
        self.assertIn(
            'That username is taken. Please choose a different one.',
            data)
        self.assertEqual(response.request.path, url_for('auth.register'))

    def test_05_register_user_with_exist_email(self):
        """Register user in auth register with exist username"""
        response = self.client.post(
            url_for('auth.register'),
            data={'username': 'peckhunter',
                  'email': self.user_data.email,
                  'info': 'Chiropractor',
                  'age': '36',
                  'city': 'PSC 8593, Box 9778\nAPO AA 35289',
                  'password': 'P>$f5jF6mZ',
                  'password_repeat': 'P>$f5jF6mZ',
                  'submit': 'Register'},
            follow_redirects=True)
        code = response.status_code
        data = response.get_data(as_text=True)
        self.assertEqual(code, 200)
        self.assertIn(
            'That email is taken. Please choose a different one.',
            data)
        self.assertEqual(response.request.path, url_for('auth.register'))

    def test_06_register_user_with_weak_password(self):
        """Register user in auth register with weak password"""
        response = self.client.post(
            url_for('auth.register'),
            data={'username': 'peckhunter',
                  'email': 'sandersjames@hotmail.com',
                  'info': 'Chiropractor',
                  'age': '36',
                  'city': 'PSC 8593, Box 9778\nAPO AA 35289',
                  'password': 'Pf5jF6mZ',
                  'password_repeat': 'P>$f5jF6mZ',
                  'submit': 'Register'},
            follow_redirects=True)
        code = response.status_code
        data = response.get_data(as_text=True)
        self.assertEqual(code, 200)
        self.assertIn(
            'Password must be at least 8 chars include Upper, Lower, Digit, Punctuation',
            data)
        self.assertEqual(response.request.path, url_for('auth.register'))

    def test_07_login_registered_user(self):
        """Login registered user"""
        response = self.client.post(
            url_for('auth.login'),
            data={
                'next': '',
                'email': self.user_data.email,
                'password': self.user_data.password,
                'remember_me': False,
                'submit': 'Log In'
            },
            follow_redirects=True
        )
        code = response.status_code
        data = response.get_data(as_text=True)
        self.assertEqual(code, 200)
        self.assertIn(
            f'Hello,\n            \n                {self.user_data.username}\n            \n',
            data)
        self.assertEqual(response.request.path, url_for('main.index'))
        logout_user()

    def test_08_with_already_logged_user(self):
        user = User.select().where(User.email == self.user_data.email).first()
        login_user(user)
        response = self.client.post(
            url_for('auth.login'),
            data={
                'next': '',
                'email': self.user_data.email,
                'password': self.user_data.password,
                'remember_me': False,
                'submit': 'Log In'
            },
            follow_redirects=True
        )
        code = response.status_code
        data = response.get_data(as_text=True)
        self.assertEqual(code, 200)
        # self.assertIn('You are already logged in.', data)
        self.assertEqual(response.request.path, url_for('main.index'))
        logout_user()

    def test_09_next_parameter_with_login_page(self):
        pass

    def test_10_login_with_invalid_password(self):
        response = self.client.post(
            url_for('auth.login'),
            data={
                'next': '',
                'email': self.user_data.email,
                'password': self.admin_data.password,
                'remember_me': False,
                'submit': 'Log In'
            },
            follow_redirects=True
        )
        code = response.status_code
        data = response.get_data(as_text=True)
        url = response.request.path
        self.assertEqual(code, 200)
        self.assertIn(
            'Login Unsuccessful. Please check email and password',
            data)
        self.assertEqual(url, url_for('auth.login'))

    def test_11_logout(self):
        user = User.select().where(User.email == self.user_data.email).first()
        login_user(user)
        response = self.client.get(
            url_for('auth.logout'),
            follow_redirects=True
        )
        code = response.status_code
        data = response.get_data(as_text=True)
        url = response.request.path
        self.assertEqual(code, 200)
        self.assertIn('Bye...', data)
        self.assertEqual(url, url_for('auth.login'))

        response_to_secret_page = self.client.get(
            url_for('auth.secret'),
            follow_redirects=True)
        code = response_to_secret_page.status_code
        data = response_to_secret_page.get_data(as_text=True)
        url = response_to_secret_page.request.path
        self.assertEqual(code, 200)
        self.assertIn('Please log in to access this page.', data)
        self.assertEqual(url, url_for('auth.login'))

    def test_12_profile_page_of_current_user(self):
        user = User.select().where(User.email == self.user_data.email).first()
        login_user(user)
        response = self.client.get(
            url_for('auth.account', user_id=user.id),
            follow_redirects=True
        )
        code = response.status_code
        data = response.get_data(as_text=True)
        url = response.request.path
        self.assertEqual(code, 200)

        self.assertIn(f'Account', data)
        self.assertIn(user.email, data)
        self.assertIn(str(user.profile.age), data)
        self.assertIn(user.profile.info, data)
        self.assertIn(user.profile.city, data)
        self.assertEqual(url, url_for('auth.account'))
        logout_user()

    def test_13_get_password_from_user(self):
        user = User.select().where(User.email == self.user_data.email).first()
        with self.assertRaises(AttributeError) as error:
            password = user.password
        self.assertEqual('password is not a valid attribute', str(error.exception))


if __name__ == '__main__':
    unittest.main()
