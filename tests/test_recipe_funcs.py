from sqlalchemy import and_

from recipe_hub import db, db_funcs
from recipe_hub.mappings import Recipe
from tests import conftest


def test_add_recipe(product, ingredient):
    amount = 500
    unit = 1
    assert Recipe.query.filter(and_(
        Recipe.product_id == product.product_id,
        Recipe.ingredient_id == ingredient.ingredient_id)).first() is None
    db_funcs.add_recipe(product.product_id, ingredient.name, amount, unit)
    recipe = Recipe.query.filter(and_(
        Recipe.product_id == product.product_id,
        Recipe.ingredient_id == ingredient.ingredient_id)).first()
    assert recipe is not None
    conftest.delete(recipe)


def test_get_recipe(product, ingredient):
    recipe = Recipe(product_id=product.product_id,
                    ingredient_id=ingredient.ingredient_id, amount=500)
    db.session.add(recipe)
    db.session.commit()
    assert len(db_funcs.get_recipe(product.product_id)) == 1
    conftest.delete(recipe)


def test_delete_recipe(product, ingredient):
    recipe = Recipe(product_id=product.product_id,
                    ingredient_id=ingredient.ingredient_id, amount=500)
    db.session.add(recipe)
    db.session.commit()
    assert Recipe.query.filter(and_(
        Recipe.product_id == product.product_id,
        Recipe.ingredient_id == ingredient.ingredient_id)).first() is not None
    db_funcs.delete_recipe(product.product_id, ingredient.ingredient_id)
    recipe = Recipe.query.filter(and_(
        Recipe.product_id == product.product_id,
        Recipe.ingredient_id == ingredient.ingredient_id)).first()
    assert recipe is None





# def test_get_recipe(recipe):
#     recipe, product_id, _ = recipe
#     assert len(db_funcs.get_recipe(product_id)) == 1


# def test_delete_recipe(recipe):
#     recipe, product_id, ingredient_id = recipe
#     assert Recipe.query.filter(and_(
#         Recipe.product_id == product_id,
#         Recipe.ingredient_id == ingredient_id)).first() is not None
#     db_funcs.delete_recipe(product_id, ingredient_id)
#     recipe = Recipe.query.filter(and_(
#         Recipe.product_id == product_id,
#         Recipe.ingredient_id == ingredient_id)).first()
#     assert recipe is None
