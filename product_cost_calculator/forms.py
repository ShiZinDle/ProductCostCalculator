from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, PasswordField, SelectField, StringField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, ValidationError

from product_cost_calculator import session
from product_cost_calculator.db_funcs import get_all_units, get_unit_id
from product_cost_calculator.mappings import User


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
            raise ValidationError('Chosen username is unavailable, please choose a diffrent one')

    def validate_email(self, email: str) -> None:
        s = session()
        user = s.query(User).filter(User.email.ilike(email.data)).first()
        if user:
            raise ValidationError('An account already exists for the chosen email. Please chooses a different email or login.')



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

    def validate_email(self, email: str) -> None:
        s = session()
        user = s.query(User).filter(User.email.ilike(email.data)).first()
        if not user:
            raise ValidationError('No account exists for the provided email.')


class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    amount = IntegerField('Final Amount', validators=[DataRequired()])
    unit = SelectField('Unit', choices=get_all_units(), coerce=get_unit_id, validators=[DataRequired()])
    public = BooleanField('Publish Publically')
    submit = SubmitField('Add')


class RecipeForm(FlaskForm):
    ingredient = StringField('Ingredient', validators=[DataRequired()])
    amount = IntegerField('Amount', validators=[DataRequired()])
    unit = SelectField('Unit', choices=get_all_units(), coerce=get_unit_id, validators=[DataRequired()])
    submit = SubmitField('+')