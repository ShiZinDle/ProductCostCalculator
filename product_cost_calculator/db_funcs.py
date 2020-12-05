from datetime import date
from typing import Optional

import bcrypt

from product_cost_calculator import login_manager, session
from product_cost_calculator.mappings import User


# def add_unit(name):
#     c.execute('''INSERT INTO units (name)
#                  VALUES (?)''', name)
#     db.commit()


# def get_unit_id(name):
#     c.execute('''SELECT id
#                    FROM units
#                   WHERE name = ?''', name)
#     return c.fetchone()[0]


# def add_ingredient(name, unit):
#     unit_id = get_unit_id(unit)
#     c.execute('''INSERT INTO ingredients (name, unit_id)
#                  VALUES (?, ?)''', name, unit_id)
#     db.commit()


# def add_product(name, unit, amount, user_id, public=False):
#     unit_id = get_unit_id(unit)
#     c.execute('''INSERT INTO products (name, unit_id, amount, user_id, public)
#                  VALUES (?, ?, ?, ?, ?)''', (name, unit_id, amount, user_id, public))
#     db.commit()
#     return get_product_id(name, user_id)


# def get_product_id(name, user_id):
#     c.execute('''SELECT id
#                    FROM products
#                   WHERE name = ?
#                         AND user_id = ?''', (name, user_id))
#     return c.fetchone()[0]


# def get_product_name(product_id: int) -> str:
#     c.execute('''SELECT *
#                    FROM products
#                   WHERE id = ?''', product_id)


# def add_recipe(product_id, *ingredients):
#     rows = create_recipe_rows(product_id, *ingredients)
#     c.executemany('''INSERT INTO recipes
#                      VALUES (?, ?, ?)''', rows)


# def create_recipe_rows(product_id, *ingredients):
#     for row in ingredients:
#         yield (product_id, *row)


# def get_recipe(product_id: int) -> List[Any]:
#     c.execute('''SELECT r.amount, u.symbol, i.name
#                    FROM recipes AS r
#                         INNER JOIN ingredients AS i
#                         ON i.id = r.ingredient_id
#                         INNER JOIN units AS u
#                         ON u.id = i.unit_id
#                   WHERE product_id = ?''', product_id)
#     return c.fetchall()


def add_user(username: str, email: str, password: str,
             fullname: str, birthday: Optional[date]):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    s = session()
    user = User(username=username, password_hash=hashed_password,
                full_name=fullname, email=email, date_of_birth=birthday)
    s.add(user)
    s.commit()


def get_user(email: str) -> User:
    s = session()
    user = s.query(User).filter(User.email.ilike(email)).first()
    return user


def validate_password(email: str, password: str) -> bool:
    password_hash = get_user(email).password_hash
    return bcrypt.checkpw(password.encode(), password_hash)


@login_manager.user_loader
def load_user(user_id):
    s = session()
    return s.query(User).get(user_id)