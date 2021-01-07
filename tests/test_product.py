from sqlalchemy import and_

from recipe_hub.mappings import Product, Recipe, Unit
from tests import conftest


def test_products_page_fails(client):
    assert (client.get(conftest.ROUTES['products']).status_code
            == conftest.HTTP_CODES['unauthorized'])


def test_products_page_returns_ok(client, user):
    conftest.login(client, user)
    assert (client.get(conftest.ROUTES['products']).status_code
            == conftest.HTTP_CODES['ok'])
    conftest.logout(client)


def test_nonexistant_product_redirects(client):
    invalid_id = 0
    assert (client.get(f"{conftest.ROUTES['view_product']}{invalid_id}/",
                       follow_redirects=True).status_code
            == conftest.HTTP_CODES['ok'])


def test_product_add_success(client, user):
    conftest.login(client, user)
    data = {'name': 'test_product',
            'amount': 500,
            'unit': 'g',
            'public': True}
    assert (client.post(conftest.ROUTES['new_product'], data=data,
                        follow_redirects=True).status_code
            == conftest.HTTP_CODES['ok'])
    product = Product.query.filter(
        and_(Product.name == data['name'],
            Product.user_id == user.user_id)).first()
    assert product is not None
    conftest.delete(product)
    conftest.logout(client)


def test_add_remove_recipe(client, user, product, ingredient):
    product_id = product.product_id
    ingredient_id = ingredient.ingredient_id
    conftest.login(client, user)
    assert Recipe.query.filter(
        and_(Recipe.product_id == product_id,
             Recipe.ingredient_id == ingredient_id)).first() is None
    unit = Unit.query.get(ingredient.unit_id)
    if unit.symbol:
        name = unit.symbol
    else:
        name = unit.name
    data = {'ingredient': ingredient.name,
            'amount': 500,
            'unit': name}
    client.post(f"{conftest.ROUTES['view_product']}{product_id}/",
                data=data)
    assert Recipe.query.filter(
        and_(Recipe.product_id == product_id,
             Recipe.ingredient_id == ingredient_id)).first() is not None
    assert (conftest.MESSAGES['existing_ingredient']
            in client.post(f"{conftest.ROUTES['view_product']}{product_id}/",
                data=data).data)
    client.get(f"{conftest.ROUTES['view_product']}{product_id}"
               f"{conftest.ROUTES['delete_ingredient']}{ingredient_id}/")
    assert Recipe.query.filter(
        and_(Recipe.product_id == product_id,
             Recipe.ingredient_id == ingredient_id)).first() is None
    conftest.logout(client)


def test_product_add_fail(client, user):
    conftest.login(client, user)
    data = {'name': 'test product',
            'amount': 500,
            'unit': 'g',
            'public': True}
    assert (conftest.MESSAGES['existing_product']
            in client.post(conftest.ROUTES['new_product'], data=data).data)
    conftest.logout(client)


def test_share_product(client, user, product):
    conftest.login(client, user)
    product_id = product.product_id
    public = product.public
    client.get(f"{conftest.ROUTES['view_product']}{product_id}"
               f"{conftest.ROUTES['share']}")
    assert Product.query.get(product_id).public != public
    client.get(f"{conftest.ROUTES['view_product']}{product_id}"
               f"{conftest.ROUTES['share']}")
    assert Product.query.get(product_id).public == public
    conftest.logout(client)


def test_delete_product(client, user, product):
    product_id = product.product_id
    conftest.login(client, user)
    client.get(f"{conftest.ROUTES['view_product']}"
               f"{product_id}{conftest.ROUTES['delete_product']}")
    assert Product.query.get(product_id) is None
    conftest.logout(client)