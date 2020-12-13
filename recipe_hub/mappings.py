from flask_login import UserMixin

from recipe_hub import db

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.Binary, nullable=False)
    full_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    date_of_birth = db.Column(db.DateTime)
    
    def get_id(self) -> int:
        return self.user_id

class Unit(db.Model):
    __tablename__ = 'units'
    
    unit_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    symbol = db.Column(db.String, unique=True)


class Product(db.Model):
    __tablename__ = 'products'
    
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.unit_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    public = db.Column(db.Boolean)


class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    
    ingredient_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.unit_id'), nullable=False)


class Supplier(db.Model):
    __tablename__ = 'suppliers'
    
    supplier_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), unique=True)


class Supply(db.Model):
    __tablename__ = 'supplies'
    
    supply_id = db.Column(db.Integer, primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.ingredient_id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.supplier_id'), nullable=False)


class Recipe(db.Model):
    __tablename__ = 'recipes'
    
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.ingredient_id'), primary_key=True)
    amount = db.Column(db.Integer, nullable=False)