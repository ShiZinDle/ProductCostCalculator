import datetime
import os
import tempfile

import bcrypt
import pytest

from recipe_hub import app, db
from recipe_hub.mappings import Ingredient, Product, Unit, User

HTTP_CODES = {
    'ok': 200,
    'found': 302,
    'unauthorized': 401,
}

ROUTES = {
    'login': '/login/',
    'logout': '/logout/',
    'register': '/register/',
    'products': '/products/',
    'view_product': '/product/',
    'new_product': '/product/add/',
    'share': '/share/',
    'delete_ingredient': '/delete/',
    'delete_product': '/delete/all/',
    'edit_username': '/profile/username/',
    'edit_email': '/profile/email/',
    'edit_password': '/profile/password/',
    'edit_name': '/profile/name/',
    'edit_birthday': '/profile/birthday/',
    'profile': '/profile/'
}
MESSAGES = {
    'missing_field': b'This field is required.',
    'invalid_username': b'Field must be between 2 and 20 characters long.',
    'unavailable_username': b'Chosen username is unavailable. Please choose a diffrent one',
    'unavailable_email': b'An account already exists for the chosen email.',
    'invalid_email': b'Invalid email address.',
    'invalid_password': b'Field must be at least 8 characters long.',
    'confirm_password_error': b'Field must be equal to ',
    'register_successfull': b'Account created for',
    'nonexistant_email_address': b'No account exists for the provided email.',
    'wrong_login_password': b'Login failed. Please try again.',
    'login_successfull': b'You have been logged in.',
    'existing_product': b'A product with the chosen name already exists on your profile. Please choose a different name.',
    'existing_ingredient': b'The given ingredient is already found in the recipe.',
    'edit': b'Change',
    'wrong_password': b'Wrong password. Please try again.',
    'username_success': b'Username changed to ',
    'same_username': b'Please choose a new username.',
    'email_success': b'Email changed to ',
    'same_email': b'Please choose a new email.',
    'password_success': b'Password changed.',
    'same_password': b'Please choose a new password.',
    'fullname_success': b'Name changed to ',
    'same_fullname': b'Please choose a new name.',
    'birthday_success': b'Date of birth changed to ',
    'same_birthday': b'Please choose a new date.',
}


def delete(entry):
    db.session.delete(entry)
    db.session.commit()


def add_yield_delete(fixture):
    db.session.add(fixture)
    db.session.commit()
    yield fixture
    delete(fixture)


def login(client, user):
    data = {'email': 'admin@admin.com', 'password': 'admin123'}
    client.post(ROUTES['login'], data=data)


def logout(client):
    client.get(ROUTES['login'])


def get_unit_name(unit_id):
    unit = Unit.query.get(unit_id)
    if unit.symbol:
        return unit.symbol
    return unit.name


@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False

    with app.test_client() as client:
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


@pytest.fixture(scope='module')
def user():
    admin = User(
        username='admin', email='admin@admin.com', full_name='admin admin',
        password_hash=bcrypt.hashpw('admin123'.encode(),bcrypt.gensalt()),
        date_of_birth=datetime.date(1970, 1, 1).strftime('%Y-%m-%d'))
    yield from add_yield_delete(admin)


@pytest.fixture(scope='module')
def user2():
    admin = User(
        username='admin2', email='admin2@admin.com', full_name='admin2 admin',
        password_hash=bcrypt.hashpw('admin123'.encode(),bcrypt.gensalt()),
        date_of_birth=datetime.date(1970, 1, 3).strftime('%Y-%m-%d'))
    yield from add_yield_delete(admin)


@pytest.fixture(scope='module')
def ingredient():
    ingredient = Ingredient(name='test ingredient', unit_id=1)
    yield from add_yield_delete(ingredient)


@pytest.fixture(scope='module')
def product(user):
    product = Product(name='test product', amount=500, unit_id=1,
                      user_id=user.user_id, public=False)
    yield from add_yield_delete(product)
