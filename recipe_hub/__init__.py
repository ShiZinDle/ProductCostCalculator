import os

from flask import Flask
from flask_login.login_manager import LoginManager
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
login_manager = LoginManager(app)

engine = create_engine(os.environ['DATABASE_URL'], echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

import recipe_hub.views