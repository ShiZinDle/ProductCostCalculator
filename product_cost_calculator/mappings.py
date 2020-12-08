from flask_login import UserMixin
from sqlalchemy import (Binary, Boolean, Column, DateTime, Float, ForeignKey,
                        Integer, String)

from product_cost_calculator import Base, engine

class User(Base, UserMixin):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password_hash = Column(Binary, nullable=False)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    date_of_birth = Column(DateTime)
    
    def get_id(self) -> int:
        return self.user_id

class Unit(Base):
    __tablename__ = 'units'
    
    unit_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    symbol = Column(String, unique=True)


class Product(Base):
    __tablename__ = 'products'
    
    product_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    unit_id = Column(Integer, ForeignKey('units.unit_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    public = Column(Boolean)


class Ingredient(Base):
    __tablename__ = 'ingredients'
    
    ingredient_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    unit_id = Column(Integer, ForeignKey('units.unit_id'), nullable=False)


class Supplier(Base):
    __tablename__ = 'suppliers'
    
    supplier_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), unique=True)


class Supply(Base):
    __tablename__ = 'supplies'
    
    supply_id = Column(Integer, primary_key=True)
    ingredient_id = Column(Integer, ForeignKey('ingredients.ingredient_id'), nullable=False)
    amount = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    supplier_id = Column(Integer, ForeignKey('suppliers.supplier_id'), nullable=False)


class Recipe(Base):
    __tablename__ = 'recipes'
    
    product_id = Column(Integer, ForeignKey('products.product_id'), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey('ingredients.ingredient_id'), primary_key=True)
    amount = Column(Integer, nullable=False)


Base.metadata.create_all(engine)