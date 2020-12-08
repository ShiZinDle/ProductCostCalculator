from datetime import date
from typing import Dict, List, Optional, Union

import bcrypt
from flask_login import current_user
from sqlalchemy import and_, or_
# from sqlalchemy.sql.functions import current_user

from product_cost_calculator import login_manager, session
from product_cost_calculator.mappings import Ingredient, Product, Recipe, Unit, User


def add_user(username: str, email: str, password: str,
             fullname: str, birthday: Optional[date]) -> int:
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    s = session()
    user = User(username=username, password_hash=hashed_password,
                full_name=fullname.lower(), email=email.lower(), date_of_birth=birthday)
    s.add(user)
    s.commit()
    return user.user_id


def get_user(email: str) -> User:
    s = session()
    user = s.query(User).filter(User.email==email.lower()).first()
    return user


def validate_password(email: str, password: str) -> bool:
    password_hash = get_user(email).password_hash
    return bcrypt.checkpw(password.encode(), password_hash)


@login_manager.user_loader
def load_user(user_id: int) -> User:
    s = session()
    return s.query(User).get(user_id)


def get_product_id(name: str) -> int:
    s = session()
    product = s.query(Product).filter(and_(Product.product_id==current_user.user_id,
                                           Product.name==name.lower())).first()
    return product.product_id


def get_product(product_id: int) -> Dict[str, Union[int, str]]:
    s = session()
    product = s.query(Product).get(product_id)
    return {'product_id': product.product_id,
            'name': product.name,
            'amount': product.amount,
            'unit': get_unit_name(product.unit_id),
            'cost': get_product_cost(product_id)}


def add_product(name: str, amount: int, unit: int, public: bool) -> int:
    s = session()
    product = Product(name=name.lower(), amount=amount, unit_id=unit,
                      user_id=current_user.user_id, public=public)
    s.add(product)
    s.commit()
    return product.product_id


def get_all_products() -> List[Dict[str, Union[int, str]]]:
    s = session()
    products = s.query(Product.product_id).filter(Product.product_id==current_user.user_id).all()
    return [get_product(product) for product in products]


def add_recipe(product_id: int, ingredient: str, amount: int, unit: int) -> None:
    s = session()
    ingredient_id = get_ingredient_id(ingredient, unit)
    if not ingredient_id:
        ingredient_id = add_ingredient(ingredient, unit)
    recipe = Recipe(product_id=product_id, ingredient_id=ingredient_id, amount=amount)
    s.add(recipe)
    s.commit()


def get_recipe(product_id: int) -> List[Dict[str, Union[int, str]]]:
    s = session()
    entries = s.query(Recipe).filter(Recipe.product_id==product_id).all()
    return [{'ingredient_id': entry.ingredient_id,
             'ingredient': get_ingredient_name(entry.ingredient_id),
             'amount': entry.amount,
             'unit': get_ingredient_unit(entry.ingredient_id),
             } for entry in entries]


def add_ingredient(name: str, unit_id: int) -> int:
    s = session()
    ingredient = Ingredient(name=name.lower(), unit_id=unit_id)
    s.add(ingredient)
    s.commit()
    print(f'ingredient_id: {ingredient.ingredient_id}')
    return ingredient.ingredient_id


def get_ingredient_id(name: str, unit_id: int) -> int:
    s = session()
    ingredient = s.query(Ingredient).filter(and_(Ingredient.name==name.lower(),
                                           Ingredient.unit_id==unit_id)).first()
    return ingredient.ingredient_id


def get_ingredient_name(ingredient_id: int) -> str:
    s = session()
    return s.query(Ingredient).get(ingredient_id).name


def get_ingredient_unit(ingredient_id: int) -> str:
    s = session()
    ingredient = s.query(Ingredient).get(ingredient_id)
    return get_unit_name(ingredient.unit_id)


def get_unit_name(unit_id: int) -> str:
    s = session()
    unit = s.query(Unit).get(unit_id)
    if unit.symbol:
        return unit.symbol
    return unit.name


def get_unit_id(name_or_symbol: str) -> int:
    s = session()
    unit = s.query(Unit).filter(or_(Unit.name==name_or_symbol.lower(),
                                    Unit.symbol==name_or_symbol.lower())).first()
    return unit.unit_id


def get_all_units() -> List[str]:
    s = session()
    units = s.query(Unit).all()
    all_units = []
    for unit in units:
        if unit.symbol:
            all_units.append(unit.symbol)
        else:
            all_units.append(unit.name)
    return all_units


def delete_recipe(product_id: int, ingredient_id: int) -> None:
    s = session()
    recipe = s.query(Recipe).filter(and_(Recipe.product_id==product_id,
                                         Recipe.ingredient_id==ingredient_id)).first()
    s.delete(recipe)
    s.commit()


def get_product_cost(product_id: int) -> int:
    pass