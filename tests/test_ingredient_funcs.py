from sqlalchemy import and_

from recipe_hub import db_funcs
from recipe_hub.mappings import Ingredient
from tests import conftest


def test_add_ingredient():
    ingredient_name = 'aaa_ingredient_test_name_aaa'
    unit_id = 1
    assert Ingredient.query.filter(and_(
        Ingredient.name == ingredient_name.lower(),
        Ingredient.unit_id == unit_id)).first() is None
    ingredient_id = db_funcs.add_ingredient(ingredient_name, unit_id)
    ingredient = Ingredient.query.get(ingredient_id)
    assert ingredient is not None
    ingredient_id = db_funcs.add_ingredient(ingredient_name, unit_id)
    ingredient = Ingredient.query.get(ingredient_id)
    assert ingredient is not None
    conftest.delete(ingredient)


def test_get_ingredient_id(ingredient):
    assert db_funcs.get_ingredient_id(
        ingredient.name, ingredient.unit_id) == ingredient.ingredient_id


def test_get_ingredient_name(ingredient):
    assert db_funcs.get_ingredient_name(
        ingredient.ingredient_id) == ingredient.name


def test_get_ingredient_unit(ingredient):
    name = conftest.get_unit_name(ingredient.unit_id)
    assert db_funcs.get_ingredient_unit(ingredient.ingredient_id) == name
