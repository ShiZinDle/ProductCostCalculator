from sqlalchemy import and_

from recipe_hub import db_funcs
from recipe_hub.mappings import Product, User
from tests import conftest


def test_get_product(product):
    username = User.query.get(product.user_id).username
    product_details = {'product_id': product.product_id,
                        'name': product.name,
                        'amount': product.amount,
                        'unit': conftest.get_unit_name(product.unit_id),
                        'user_id': product.user_id,
                        'username': username,
                        'public': product.public == 1}
    assert db_funcs.get_product(product.product_id) == product_details


def test_add_product(user):
    product_details = {'name': 'test_product',
                       'amount': 1,
                       'unit': 1,
                       'public': True}
    assert Product.query.filter(and_(
        Product.name == product_details['name'].lower(),
        Product.user_id == user.user_id)).first() is None
    product_id = db_funcs.add_product(**product_details, user_id=user.user_id)
    product = Product.query.get(product_id)
    assert product is not None
    conftest.delete(product)


def test_get_all_products(product):
    assert len(db_funcs.get_all_products(product.user_id)) == 1
    assert len(db_funcs.get_all_products(product.user_id, True)) == 0


def test_share_product(product):
    public = product.public
    db_funcs.share_product(product.product_id)
    assert product.public != public
    db_funcs.share_product(product.product_id)
    assert product.public == public


def test_delete_product(product):
    assert Product.query.get(product.product_id) is not None
    db_funcs.delete_product(product.product_id)
    assert Product.query.get(product.product_id) is None