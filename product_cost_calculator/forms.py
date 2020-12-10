from flask_login import current_user
from flask_wtf import FlaskForm
from sqlalchemy import and_
from wtforms import BooleanField, PasswordField, SelectField, StringField, SubmitField
from wtforms.fields.html5 import DateField, IntegerField
from wtforms.fields.simple import HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, ValidationError

from product_cost_calculator import session
from product_cost_calculator import db_funcs
from product_cost_calculator.db_funcs import get_all_units, get_unit_id
from product_cost_calculator.mappings import Ingredient, Product, Recipe, User


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    fullname = StringField('Full Name', validators=[DataRequired()])
    birthday = DateField('Date of Birth', validators=[Optional()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username: str) -> None:
        s = session()
        user = s.query(User).filter(User.username.ilike(username.data)).first()
        if user:
            raise ValidationError('Chosen username is unavailable. Please choose a diffrent one')

    def validate_email(self, email: str) -> None:
        s = session()
        user = s.query(User).filter(User.email==email.data.lower()).first()
        if user:
            raise ValidationError('An account already exists for the chosen email. Please chooses a different email or login.')



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

    def validate_email(self, email: str) -> None:
        s = session()
        user = s.query(User).filter(User.email==email.data.lower()).first()
        if not user:
            raise ValidationError('No account exists for the provided email.')


class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    amount = IntegerField('Final Amount', validators=[DataRequired()])
    unit = SelectField('Unit', choices=get_all_units(), coerce=get_unit_id, validators=[DataRequired()])
    public = BooleanField('Publish Publically')
    submit = SubmitField('Add')
    
    def validate_name(self, name: str) -> None:
        s = session()
        product = s.query(Product).filter(and_(Product.user_id==current_user.user_id,
                                               Product.name==name.data.lower())).first()
        if product:
            raise ValidationError('A product with the chosen name already exists on your profile. Please choose a different name.')


class RecipeForm(FlaskForm):
    product_id = HiddenField()
    ingredient = StringField('Ingredient', validators=[DataRequired()])
    amount = IntegerField('Amount', validators=[DataRequired()])
    unit = SelectField('Unit', choices=get_all_units(), coerce=get_unit_id, validators=[DataRequired()])
    submit = SubmitField('+')
    
    def validate_ingredient(self, ingredient: str) -> None:
        s = session()
        ingredient = s.query(Ingredient).filter(and_(Ingredient.name==ingredient.data.lower(),
                                                     Ingredient.unit_id==self.unit.data)).first()
        if ingredient is not None:
            recipe = s.query(Recipe).filter(and_(Recipe.product_id==self.product_id.data,
                                                Recipe.ingredient_id==ingredient.ingredient_id)).first()
            if recipe:
                raise ValidationError('The given ingredient is already found in the recipe.')


class UsernameForm(FlaskForm):
    username = StringField('New username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Current password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Change Username')
    
    def validate_username(self, username: str) -> None:
        if username.data == current_user.username:
            raise ValidationError('Please choose a new username.')
        s = session()
        user = s.query(User).filter(and_(User.username.ilike(username.data),
                                         User.username!=current_user.username)).first()
        if user:
            raise ValidationError('Chosen username is unavailable. Please choose a diffrent one')


class EmailForm(FlaskForm):
    email = StringField('New email', validators=[DataRequired(), Email()])
    password = PasswordField('Current password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Change Email')
    
    def validate_email(self, email: str) -> None:
        if email.data.lower() == current_user.email:
            raise ValidationError('Please choose a new email.')
        s = session()
        user = s.query(User).filter(User.email==email.data.lower()).first()
        if user:
            raise ValidationError('An account already exists for the chosen email.')


class PasswordForm(FlaskForm):
    cur_password = PasswordField('Current password', validators=[DataRequired(), Length(min=8)])
    new_password = PasswordField('New password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')
    
    def validate_new_password(self, new_password: str) -> None:
        if db_funcs.validate_password(current_user.email, new_password.data):
            raise ValidationError('Please choose a new password.')


class NameForm(FlaskForm):
    fullname = StringField('Full Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Change Name')
    
    def validate_fullname(self, fullname: str) -> None:
        if fullname.data.lower() == current_user.full_name:
            raise ValidationError('Please choose a new name.')


class BirthdayForm(FlaskForm):
    birthday = DateField('Date of Birth', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Change Date of Birth')
    
    def validate_birthday(self, birthday: str) -> None:
        if birthday.data == current_user.date_of_birth.date():
            raise ValidationError('Please choose a new date.')