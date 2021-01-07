from datetime import date

import pytest

from recipe_hub.mappings import User
from tests import conftest

NEW_USERNAME = 'admin1'
NEW_EMAIL = 'admin1@admin.com'
EMAIL = 'admin@admin.com'
PASSWORD = 'admin123'
INVALID_PASSWORD = 'admin12'
NEW_PASSWORD = 'admin1234'
NEW_FULLNAME = 'admin1 admin'
NEW_BIRTHDAY = date(1970, 1, 2)
PAGES = [
    (conftest.ROUTES['edit_username']),
    (conftest.ROUTES['edit_email']),
    (conftest.ROUTES['edit_password']),
    (conftest.ROUTES['edit_name']),
    (conftest.ROUTES['edit_birthday'])
]
EDITS = [
    # Username edits
    (conftest.ROUTES['edit_username'],
     {'username': '', 'password': PASSWORD},
     conftest.MESSAGES['missing_field']),
    (conftest.ROUTES['edit_username'],
     {'username': NEW_USERNAME, 'password': ''},
     conftest.MESSAGES['missing_field']),
    (conftest.ROUTES['edit_username'],
     {'username': NEW_USERNAME, 'password': INVALID_PASSWORD},
     conftest.MESSAGES['invalid_password']),
    (conftest.ROUTES['edit_username'],
     {'username': NEW_USERNAME, 'password': NEW_PASSWORD},
     conftest.MESSAGES['wrong_password']),
    (conftest.ROUTES['edit_username'],
     {'username': 'a', 'password': PASSWORD},
     conftest.MESSAGES['invalid_username']),
    (conftest.ROUTES['edit_username'],
     {'username': 'admin2', 'password': PASSWORD},
     conftest.MESSAGES['unavailable_username']),
    (conftest.ROUTES['edit_username'],
     {'username': 'admin', 'password': PASSWORD},
     conftest.MESSAGES['same_username']),
    (conftest.ROUTES['edit_username'],
     {'username': 'Admin', 'password': PASSWORD},  # Changing the username capitalization is permitted.
     conftest.MESSAGES['username_success']),
    (conftest.ROUTES['edit_username'],
     {'username': NEW_USERNAME, 'password': PASSWORD},
     conftest.MESSAGES['username_success']),
    # Email edits
    (conftest.ROUTES['edit_email'],
     {'email': '', 'password': PASSWORD},
     conftest.MESSAGES['missing_field']),
    (conftest.ROUTES['edit_email'],
     {'email': NEW_EMAIL, 'password': ''},
     conftest.MESSAGES['missing_field']),
    (conftest.ROUTES['edit_email'],
     {'email': NEW_EMAIL, 'password': INVALID_PASSWORD},
     conftest.MESSAGES['invalid_password']),
    (conftest.ROUTES['edit_email'],
     {'email': NEW_EMAIL, 'password': NEW_PASSWORD},
     conftest.MESSAGES['wrong_password']),
    (conftest.ROUTES['edit_email'],
     {'email': NEW_USERNAME, 'password': PASSWORD},
     conftest.MESSAGES['invalid_email']),
    (conftest.ROUTES['edit_email'],
     {'email': 'admin2@admin.com', 'password': PASSWORD},
     conftest.MESSAGES['unavailable_email']),
    (conftest.ROUTES['edit_email'],
     {'email': EMAIL, 'password': PASSWORD},
     conftest.MESSAGES['same_email']),
    (conftest.ROUTES['edit_email'],
     {'email': NEW_EMAIL, 'password': PASSWORD},
     conftest.MESSAGES['email_success']),
    # Fullname edits
    (conftest.ROUTES['edit_name'],
     {'fullname': '', 'password': PASSWORD},
     conftest.MESSAGES['missing_field']),
    (conftest.ROUTES['edit_name'],
     {'fullname': NEW_FULLNAME, 'password': ''},
     conftest.MESSAGES['missing_field']),
    (conftest.ROUTES['edit_name'],
     {'fullname': NEW_FULLNAME, 'password': INVALID_PASSWORD},
     conftest.MESSAGES['invalid_password']),
    (conftest.ROUTES['edit_name'],
     {'fullname': NEW_FULLNAME, 'password': NEW_PASSWORD},
     conftest.MESSAGES['wrong_password']),
    (conftest.ROUTES['edit_name'],
     {'fullname': 'admin admin', 'password': PASSWORD},
     conftest.MESSAGES['same_fullname']),
    (conftest.ROUTES['edit_name'],
     {'fullname': NEW_FULLNAME, 'password': PASSWORD},
     conftest.MESSAGES['fullname_success']),
    # Birthday edits
    (conftest.ROUTES['edit_birthday'],
     {'birthday': '',
      'password': PASSWORD},
     conftest.MESSAGES['missing_field']),
    (conftest.ROUTES['edit_birthday'],
     {'birthday': NEW_BIRTHDAY,
      'password': ''},
     conftest.MESSAGES['missing_field']),
    (conftest.ROUTES['edit_birthday'],
     {'birthday': NEW_BIRTHDAY,
      'password': INVALID_PASSWORD},
     conftest.MESSAGES['invalid_password']),
    (conftest.ROUTES['edit_birthday'],
     {'birthday': NEW_BIRTHDAY,
      'password': NEW_PASSWORD},
     conftest.MESSAGES['wrong_password']),
    (conftest.ROUTES['edit_birthday'],
     {'birthday': date(1970, 1, 1),
      'password': PASSWORD},
     conftest.MESSAGES['same_birthday']),
    (conftest.ROUTES['edit_birthday'],
     {'birthday': NEW_BIRTHDAY,
      'password': PASSWORD},
     conftest.MESSAGES['birthday_success']),
    # Password edits
    (conftest.ROUTES['edit_password'],
     {'cur_password': '', 'new_password': NEW_PASSWORD,
      'confirm_password': NEW_PASSWORD},
     conftest.MESSAGES['missing_field']),
    (conftest.ROUTES['edit_password'],
     {'cur_password': PASSWORD, 'new_password': '',
      'confirm_password': NEW_PASSWORD},
     conftest.MESSAGES['missing_field']),
    (conftest.ROUTES['edit_password'],
     {'cur_password': INVALID_PASSWORD, 'new_password': NEW_PASSWORD,
      'confirm_password': NEW_PASSWORD},
     conftest.MESSAGES['invalid_password']),
    (conftest.ROUTES['edit_password'],
     {'cur_password': PASSWORD, 'new_password': INVALID_PASSWORD,
      'confirm_password': INVALID_PASSWORD},
     conftest.MESSAGES['invalid_password']),
    (conftest.ROUTES['edit_password'],
     {'cur_password': NEW_PASSWORD, 'new_password': NEW_PASSWORD,
      'confirm_password': NEW_PASSWORD},
     conftest.MESSAGES['wrong_password']),
    (conftest.ROUTES['edit_password'],
     {'cur_password': PASSWORD, 'new_password': NEW_PASSWORD,
      'confirm_password': PASSWORD},
     conftest.MESSAGES['confirm_password_error']),
    (conftest.ROUTES['edit_password'],
     {'cur_password': PASSWORD, 'new_password': PASSWORD,
      'confirm_password': PASSWORD},
     conftest.MESSAGES['same_password']),
    (conftest.ROUTES['edit_password'],
     {'cur_password': PASSWORD, 'new_password': NEW_PASSWORD,
      'confirm_password': NEW_PASSWORD},
     conftest.MESSAGES['password_success'])
]


def test_nonexistant_profile_redirects(client):
    invalid_id = 0
    assert (client.get(f"{conftest.ROUTES['profile']}{invalid_id}/",
                       follow_redirects=True).status_code
            == conftest.HTTP_CODES['ok'])


def test_edit_available_upon_login(client, user):
    user_id = user.user_id
    assert (conftest.MESSAGES['edit']
            not in client.get(f"{conftest.ROUTES['profile']}{user_id}/").data)
    conftest.login(client, user)
    assert (conftest.MESSAGES['edit']
            in client.get(f"{conftest.ROUTES['profile']}{user_id}/").data)
    conftest.logout(client)


@pytest.mark.parametrize('path', PAGES)
def test_edit_page_returns_unauthorized(client, path):
    assert client.get(path).status_code == conftest.HTTP_CODES['unauthorized']


@pytest.mark.parametrize('path, data, message', EDITS)
def test_edit_profile(client, user, user2, path, data, message):
    conftest.login(client, user)
    assert message in client.post(path, data=data, follow_redirects=True).data
    if User.query.get(user.user_id).email == NEW_EMAIL:
        User.query.get(user.user_id).email = EMAIL
        conftest.db.session.commit()
    conftest.logout(client)