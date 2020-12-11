from datetime import date
from random import shuffle
from typing import Dict, List, Optional, Union

import bcrypt
from flask_login import current_user
from sqlalchemy import and_, or_

from recipe_hub import login_manager, session
from recipe_hub.mappings import Ingredient, Product, Recipe, Unit, User


# Ingredient
def add_ingredient(name: str, unit_id: int) -> int:
    ingredient_id = get_ingredient_id(name, unit_id)
    if ingredient_id:
        return ingredient_id
    ingredient = Ingredient(name=name.lower(), unit_id=unit_id)
    session.add(ingredient)
    session.commit()
    return ingredient.ingredient_id


def get_ingredient_id(name: str, unit_id: int) -> Optional[int]:
    ingredient = session.query(Ingredient).filter(and_(Ingredient.name==name.lower(),
                                           Ingredient.unit_id==unit_id)).first()
    try:
        return ingredient.ingredient_id
    except AttributeError:
        return None


def get_ingredient_name(ingredient_id: int) -> str:
    return session.query(Ingredient).get(ingredient_id).name


def get_ingredient_unit(ingredient_id: int) -> str:
    ingredient = session.query(Ingredient).get(ingredient_id)
    return get_unit_name(ingredient.unit_id)



# Product
def get_product_id(name: str) -> int:
    product = session.query(Product).filter(and_(Product.product_id==current_user.user_id,
                                           Product.name==name.lower())).first()
    return product.product_id


def get_product(product_id: int) -> Dict[str, Union[bool, int, str]]:
    product = session.query(Product).get(product_id)
    return {'product_id': product.product_id,
            'name': product.name,
            'amount': product.amount,
            'unit': get_unit_name(product.unit_id),
            'cost': get_product_cost(product_id),
            'user_id': product.user_id,
            'username': get_user(product.user_id).username,
            'public': product.public == 1}


def add_product(name: str, amount: int, unit: int, public: bool) -> int:
    product = Product(name=name.lower(), amount=amount, unit_id=unit,
                      user_id=current_user.user_id, public=public)
    session.add(product)
    session.commit()
    return product.product_id


def delete_product(product_id: int) -> None:
    product = session.query(Product).filter(Product.product_id==product_id).first()
    session.delete(product)
    session.commit()


def get_all_products(user_id: int, public_only: bool = False) -> List[Dict[str, Union[int, str]]]:
    if public_only:
        products = session.query(Product.product_id).filter(and_(Product.user_id==user_id,
                                                        Product.public==public_only)).all()
    else:
        products = session.query(Product.product_id).filter(Product.user_id==user_id).all()
    all_products = [get_product(product) for product in products]
    return sorted(all_products, key=lambda product: product['name'])


def get_all_public_products() -> List[Dict[str, Union[int, str]]]:
    products = session.query(Product.product_id).filter(Product.public==True).all()
    all_products = [get_product(product) for product in products]
    shuffle(all_products)
    return all_products


def get_product_cost(product_id: int) -> int:
    pass


def share_product(product_id: int) -> None:
    product = session.query(Product).get(product_id)
    product.public = not product.public
    session.commit()


# Recipe
def add_recipe(product_id: int, ingredient: str, amount: int, unit_id: int) -> None:
    ingredient_id = add_ingredient(ingredient, unit_id)
    recipe = Recipe(product_id=product_id, ingredient_id=ingredient_id, amount=amount)
    session.add(recipe)
    session.commit()


def get_recipe(product_id: int) -> List[Dict[str, Union[int, str]]]:
    entries = session.query(Recipe).filter(Recipe.product_id==product_id).all()
    return [{'ingredient_id': entry.ingredient_id,
             'ingredient': get_ingredient_name(entry.ingredient_id),
             'amount': entry.amount,
             'unit': get_ingredient_unit(entry.ingredient_id),
             } for entry in entries]


def delete_recipe(product_id: int, ingredient_id: int) -> None:
    recipe = session.query(Recipe).filter(and_(Recipe.product_id==product_id,
                                         Recipe.ingredient_id==ingredient_id)).first()
    session.delete(recipe)
    session.commit()


# Unit
def get_unit_name(unit_id: int) -> str:
    unit = session.query(Unit).get(unit_id)
    if unit.symbol:
        return unit.symbol
    return f' {unit.name}'


def get_unit_id(name_or_symbol: str) -> int:
    unit = session.query(Unit).filter(or_(Unit.name==name_or_symbol.lower(),
                                    Unit.symbol==name_or_symbol.lower())).first()
    return unit.unit_id


def get_all_units() -> List[str]:
    units = session.query(Unit).all()
    all_units = []
    for unit in units:
        if unit.symbol:
            all_unitsession.append(unit.symbol)
        else:
            all_unitsession.append(unit.name)
    return all_units


def reset_units() -> None:
    units = session.query(Unit).all()
    if not units:
        for unit in UNITS:
            session.add(Unit(*unit))
        session.commit()


# User
def add_user(username: str, email: str, password: str,
             fullname: str, birthday: Optional[date]) -> int:
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    user = User(username=username, password_hash=hashed_password,
                full_name=fullname.lower(), email=email.lower(), date_of_birth=birthday)
    session.add(user)
    session.commit()
    return user.user_id


def get_user(user_id: int) -> User:
    user = session.query(User).get(user_id)
    return user


def get_user_by_email(email: str) -> User:
    user = session.query(User).filter(User.email==email.lower()).first()
    return user


def validate_password(email: str, password: str) -> bool:
    password_hash = get_user_by_email(email).password_hash
    return bcrypt.checkpw(password.encode(), password_hash)


@login_manager.user_loader
def load_user(user_id: int) -> User:
    return session.query(User).get(user_id)


def change_username(user_id: int, username: str) -> None:
    user = session.query(User).filter(User.user_id==user_id).first()
    user.username = username
    session.commit()


def change_email(user_id: int, email: str) -> None:
    user = session.query(User).filter(User.user_id==user_id).first()
    user.email = email.lower()
    session.commit()


def change_password(user_id: int, password: str) -> None:
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    user = session.query(User).filter(User.user_id==user_id).first()
    user.password_hash = hashed_password
    session.commit()


def change_fullname(user_id: int, fullname: str) -> None:
    user = session.query(User).filter(User.user_id==user_id).first()
    user.full_name = fullname.lower()
    session.commit()


def change_birthday(user_id: int, birthday: str) -> None:
    user = session.query(User).filter(User.user_id==user_id).first()
    user.date_of_birth = birthday
    session.commit()