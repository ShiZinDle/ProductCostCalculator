import datetime

import pytest

from recipe_hub.db_funcs import get_user_by_email
from tests import conftest

# Parameters
user_details = {'username': 'admin1',
            'email': 'admin1@admin.com',
            'password': 'admin123',
            'fullname': 'admin admin',
            'birthday': datetime.date(1970, 1, 1).strftime('%Y-%m-%d')}

REGISTER_MESSAGE_OPTIONS = [
    ('', user_details['email'],
     user_details['password'], user_details['password'],
     user_details['fullname'], user_details['birthday'],
     conftest.MESSAGES['missing_field']),
    (user_details['username'], '',
     user_details['password'], user_details['password'],
     user_details['fullname'], user_details['birthday'],
     conftest.MESSAGES['missing_field']),
    (user_details['username'], user_details['email'],
     '', user_details['password'],
     user_details['fullname'], user_details['birthday'],
     conftest.MESSAGES['missing_field']),
    (user_details['username'], user_details['email'],
     user_details['password'], '',
     user_details['fullname'], user_details['birthday'],
     conftest.MESSAGES['missing_field']),
    (user_details['username'], user_details['email'],
     user_details['password'], user_details['password'],
     '', user_details['birthday'],
     conftest.MESSAGES['missing_field']),
    ('1', user_details['email'],
     user_details['password'], user_details['password'],
     user_details['fullname'], user_details['birthday'],
     conftest.MESSAGES['invalid_username']),
    ('admin', user_details['email'],
     user_details['password'], user_details['password'],
     user_details['fullname'], user_details['birthday'],
     conftest.MESSAGES['unavailable_username']),
    ('ADMIN', user_details['email'],
     user_details['password'], user_details['password'],
     user_details['fullname'], user_details['birthday'],
     conftest.MESSAGES['unavailable_username']),
    (user_details['username'], 'admin',
     user_details['password'], user_details['password'],
     user_details['fullname'], user_details['birthday'],
     conftest.MESSAGES['invalid_email']),
    (user_details['username'], 'admin@admin.com',
     user_details['password'], user_details['password'],
     user_details['fullname'], user_details['birthday'],
     conftest.MESSAGES['unavailable_email']),
    (user_details['username'], 'ADMIN@ADMIN.COM',
     user_details['password'], user_details['password'],
     user_details['fullname'], user_details['birthday'],
     conftest.MESSAGES['unavailable_email']),
    (user_details['username'], user_details['email'],
     'admin', user_details['password'],
     user_details['fullname'], user_details['birthday'],
     conftest.MESSAGES['invalid_password']),
    (user_details['username'], user_details['email'],
     user_details['password'], 'admin',
     user_details['fullname'], user_details['birthday'],
     conftest.MESSAGES['confirm_password_error']),
    (user_details['username'], user_details['email'],
     user_details['password'], user_details['password'],
     user_details['fullname'], user_details['birthday'],
     conftest.MESSAGES['register_successfull']),
]


def test_register_page_returns_ok(client):
    assert (client.get(conftest.ROUTES['register']).status_code
            == conftest.HTTP_CODES['ok'])


@pytest.mark.parametrize(
    'username, email, password, confirm, fullname, birthday, message',
    REGISTER_MESSAGE_OPTIONS
)
def test_register(client, user, username, email, password,
                  confirm, fullname, birthday, message):
    data = {'username': username,
            'email': email,
            'password': password,
            'confirm_password': confirm,
            'fullname': fullname,
            'birthday': birthday}
    assert message in client.post(conftest.ROUTES['register'], data=data,
                                  follow_redirects=True).data
    admin = get_user_by_email('admin1@admin.com')
    if admin:
        conftest.db.session.delete(admin)
        conftest.db.session.commit()
