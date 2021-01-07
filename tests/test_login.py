import pytest

from tests import conftest

# Parameters
UNAUTHORIZED_ROUTE_OPTIONS = [
    (conftest.ROUTES['logout'],
     conftest.HTTP_CODES['unauthorized']),
    (conftest.ROUTES['products'],
     conftest.HTTP_CODES['unauthorized']),
    (conftest.ROUTES['new_product'],
     conftest.HTTP_CODES['unauthorized']),
    (conftest.ROUTES['edit_username'],
     conftest.HTTP_CODES['unauthorized']),
    (conftest.ROUTES['edit_email'],
     conftest.HTTP_CODES['unauthorized']),
    (conftest.ROUTES['edit_password'],
     conftest.HTTP_CODES['unauthorized']),
    (conftest.ROUTES['edit_name'],
     conftest.HTTP_CODES['unauthorized']),
    (conftest.ROUTES['edit_birthday'],
     conftest.HTTP_CODES['unauthorized']),
]
LOGIN_MESSAGE_OPTIONS = [
    ('admin@admin.com', '',
     conftest.MESSAGES['missing_field']),
    ('', 'test_password',
     conftest.MESSAGES['missing_field']),
    ('admin', 'test_password',
     conftest.MESSAGES['invalid_email']),
    ('a@a.com', 'test_password',
     conftest.MESSAGES['nonexistant_email_address']),
    ('admin@admin.com', 'test',
     conftest.MESSAGES['invalid_password']),
    ('admin@admin.com', 'admin111',
     conftest.MESSAGES['wrong_login_password'])
]


def test_login_page_returns_ok(client):
    assert (client.get(conftest.ROUTES['login']).status_code
            == conftest.HTTP_CODES['ok'])


@pytest.mark.parametrize('route, status_code', UNAUTHORIZED_ROUTE_OPTIONS)
def test_unauthorized_page(client, route, status_code):
    assert client.get(route).status_code == status_code


@pytest.mark.parametrize('email, password, message', LOGIN_MESSAGE_OPTIONS)
def test_login_fails(client, user, email, password, message):
    data = {'email': email,
            'password': password}
    assert message in client.post(conftest.ROUTES['login'], data=data).data


def test_login_logout(client, user):
    data = {'email': 'admin@admin.com',
            'password': 'admin123'}
    assert (conftest.MESSAGES['login_successfull']
            in client.post(conftest.ROUTES['login'], data=data,
                           follow_redirects=True).data)
    assert (client.get(conftest.ROUTES['logout']).status_code
            == conftest.HTTP_CODES['found'])