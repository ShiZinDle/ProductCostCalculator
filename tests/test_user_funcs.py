import datetime

from bcrypt import checkpw

from recipe_hub import db_funcs
from recipe_hub.mappings import User
from tests import conftest

CHANGES = [
    (User.username, 'admin1', db_funcs.change_username),
    (User.email, 'admin1@admin1.com', db_funcs.change_email),
    (User.full_name, 'admin1 admin1', db_funcs.change_fullname),
    (User.date_of_birth, datetime.date(1970, 1, 2).strftime('%Y-%m-%d'), db_funcs.change_birthday)
]


def test_add_user():
    user_details = {'username': 'test', 'email': 'test@test.com',
                    'password': 'test1234', 'fullname': 'test user'}
    assert User.query.filter(
        User.username == user_details['username'].lower()).first() is None
    user_id = db_funcs.add_user(**user_details)
    user = User.query.get(user_id)
    assert user is not None
    conftest.delete(user)


def test_get_user(user):
    assert db_funcs.get_user(user.user_id) == user


def test_get_user_by_email(user):
    assert db_funcs.get_user_by_email(user.email) == user


def test_validate_password(user):
    assert db_funcs.validate_password(user.email, 'admin123')


def test_change_username(user):
    username = 'admin1'
    assert user.username != username
    db_funcs.change_username(user.user_id, username)
    assert user.username == username


def test_change_email(user):
    email = 'admin1@admin1.com'
    assert user.email != email
    db_funcs.change_email(user.user_id, email)
    assert user.email == email


def test_change_password(user):
    password = 'admin1234'
    assert not checkpw(password.encode(), user.password_hash)
    db_funcs.change_password(user.user_id, password)
    assert checkpw(password.encode(), user.password_hash)


def test_change_fullname(user):
    fullname = 'admin1 admin1'
    assert user.full_name != fullname
    db_funcs.change_fullname(user.user_id, fullname)
    assert user.full_name == fullname


def test_change_birthday(user):
    birthday = datetime.date(1970, 1, 2).strftime('%Y-%m-%d %H:%M:%S')
    assert str(user.date_of_birth) != birthday
    db_funcs.change_birthday(user.user_id, birthday)
    assert str(user.date_of_birth) == birthday