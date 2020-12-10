from datetime import date
from random import shuffle
from typing import Dict, List, Optional, Union

import bcrypt
from flask_login import current_user
from sqlalchemy import and_, or_

from product_cost_calculator import login_manager, session
from product_cost_calculator.mappings import Ingredient, Product, Recipe, Unit, User


# User
def add_user(username: str, email: str, password: str,
             fullname: str, birthday: Optional[date]) -> int:
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    s = session()
    user = User(username=username, password_hash=hashed_password,
                full_name=fullname.lower(), email=email.lower(), date_of_birth=birthday)
    s.add(user)
    s.commit()
    return user.user_id


def get_user(user_id: int) -> User:
    s = session()
    user = s.query(User).get(user_id)
    return user


def get_user_by_email(email: str) -> User:
    s = session()
    user = s.query(User).filter(User.email==email.lower()).first()
    return user


def validate_password(email: str, password: str) -> bool:
    password_hash = get_user_by_email(email).password_hash
    return bcrypt.checkpw(password.encode(), password_hash)


@login_manager.user_loader
def load_user(user_id: int) -> User:
    s = session()
    return s.query(User).get(user_id)


def change_username(user_id: int, username: str) -> None:
    s = session()
    user = s.query(User).filter(User.user_id==user_id).first()
    user.username = username
    s.commit()


def change_email(user_id: int, email: str) -> None:
    s = session()
    user = s.query(User).filter(User.user_id==user_id).first()
    user.email = email.lower()
    s.commit()


def change_password(user_id: int, password: str) -> None:
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    s = session()
    user = s.query(User).filter(User.user_id==user_id).first()
    user.password_hash = hashed_password
    s.commit()


def change_fullname(user_id: int, fullname: str) -> None:
    s = session()
    user = s.query(User).filter(User.user_id==user_id).first()
    user.full_name = fullname.lower()
    s.commit()


def change_birthday(user_id: int, birthday: str) -> None:
    s = session()
    user = s.query(User).filter(User.user_id==user_id).first()
    user.date_of_birth = birthday
    s.commit()


# Product
def get_product_id(name: str) -> int:
    s = session()
    product = s.query(Product).filter(and_(Product.product_id==current_user.user_id,
                                           Product.name==name.lower())).first()
    return product.product_id


def get_product(product_id: int) -> Dict[str, Union[bool, int, str]]:
    s = session()
    product = s.query(Product).get(product_id)
    return {'product_id': product.product_id,
            'name': product.name,
            'amount': product.amount,
            'unit': get_unit_name(product.unit_id),
            'cost': get_product_cost(product_id),
            'user_id': product.user_id,
            'username': get_user(product.user_id).username,
            'public': product.public == 1}


def add_product(name: str, amount: int, unit: int, public: bool) -> int:
    s = session()
    product = Product(name=name.lower(), amount=amount, unit_id=unit,
                      user_id=current_user.user_id, public=public)
    s.add(product)
    s.commit()
    return product.product_id


def delete_product(product_id: int) -> None:
    s = session()
    product = s.query(Product).filter(Product.product_id==product_id).first()
    s.delete(product)
    s.commit()


def get_all_products() -> List[Dict[str, Union[int, str]]]:
    s = session()
    products = s.query(Product.product_id).filter(Product.user_id==current_user.user_id).all()
    all_products = [get_product(product) for product in products]
    return sorted(all_products, key=lambda product: product['name'])


def get_all_public_products() -> List[Dict[str, Union[int, str]]]:
    s = session()
    products = s.query(Product.product_id).filter(Product.public==1).all()
    all_products = [get_product(product) for product in products]
    shuffle(all_products)
    return all_products


def get_product_cost(product_id: int) -> int:
    pass


# Recipe
def add_recipe(product_id: int, ingredient: str, amount: int, unit_id: int) -> None:
    s = session()
    ingredient_id = add_ingredient(ingredient, unit_id)
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


def delete_recipe(product_id: int, ingredient_id: int) -> None:
    s = session()
    recipe = s.query(Recipe).filter(and_(Recipe.product_id==product_id,
                                         Recipe.ingredient_id==ingredient_id)).first()
    s.delete(recipe)
    s.commit()


# Ingredient
def add_ingredient(name: str, unit_id: int) -> int:
    s = session()
    ingredient_id = get_ingredient_id(name, unit_id)
    if ingredient_id:
        return ingredient_id
    ingredient = Ingredient(name=name.lower(), unit_id=unit_id)
    s.add(ingredient)
    s.commit()
    return ingredient.ingredient_id


def get_ingredient_id(name: str, unit_id: int) -> Optional[int]:
    s = session()
    ingredient = s.query(Ingredient).filter(and_(Ingredient.name==name.lower(),
                                           Ingredient.unit_id==unit_id)).first()
    try:
        return ingredient.ingredient_id
    except AttributeError:
        return None


def get_ingredient_name(ingredient_id: int) -> str:
    s = session()
    return s.query(Ingredient).get(ingredient_id).name


def get_ingredient_unit(ingredient_id: int) -> str:
    s = session()
    ingredient = s.query(Ingredient).get(ingredient_id)
    return get_unit_name(ingredient.unit_id)


# Unit
def get_unit_name(unit_id: int) -> str:
    s = session()
    unit = s.query(Unit).get(unit_id)
    if unit.symbol:
        return unit.symbol
    return f' {unit.name}'


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