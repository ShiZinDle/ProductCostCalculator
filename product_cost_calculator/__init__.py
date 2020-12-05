from flask import Flask
from flask_login.login_manager import LoginManager
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


with open('./secret_key.txt', 'r') as file:
    SECRET_KEY = file.read()
DB_PATH = 'product_cost.db'

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
login_manager = LoginManager(app)

engine = create_engine(f'sqlite:///{DB_PATH}', echo=True)
Base = declarative_base()
session = sessionmaker(bind=engine)

import product_cost_calculator.views