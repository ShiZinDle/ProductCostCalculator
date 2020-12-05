from flask_login import UserMixin
from sqlalchemy import (Binary, Boolean, Column, DateTime, Float, ForeignKey,
                        Integer, String)

from product_cost_calculator import Base

class User(Base, UserMixin):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password_hash = Column(Binary, nullable=False)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    date_of_birth = Column(DateTime)

class Unit(Base):
    __tablename__ = 'units'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    symbol = Column(String, unique=True)


class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    unit_id = Column(Integer, ForeignKey('units.id'), nullable=False)
    amount = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    public = Column(Boolean)


class Ingredient(Base):
    __tablename__ = 'ingredients'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    unit_id = Column(Integer, ForeignKey('units.id'), nullable=False)


class Supplier(Base):
    __tablename__ = 'suppliers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)


class Supply(Base):
    __tablename__ = 'supplies'
    
    id = Column(Integer, primary_key=True)
    ingredient_id = Column(Integer, ForeignKey('ingredients.id'), nullable=False)
    unit_id = Column(Integer, ForeignKey('units.id'), nullable=False)
    amount = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'), nullable=False)


class Recipe(Base):
    __tablename__ = 'recipes'
    
    product_id = Column(Integer, ForeignKey('products.id'), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey('ingredients.id'), primary_key=True)
    amount = Column(Float, nullable=False)