from typing import Union

from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user
from flask_login.utils import login_required
from werkzeug.wrappers import Response

import recipe_hub.db_funcs as db_funcs
from recipe_hub import app
from recipe_hub.forms import (BirthdayForm, EmailForm, LoginForm, NameForm,
                              PasswordForm, ProductForm, RecipeForm,
                              RegisterForm, UsernameForm)


@app.route('/')
def home() -> str:
    products = db_funcs.get_all_public_products()
    return render_template('home.j2', products=products)


# Product
@app.route('/product/add/', methods=['GET', 'POST'])
@login_required
def add_product() -> Union[Response, str]:
    form = ProductForm()
    if form.validate_on_submit():
        product_id = db_funcs.add_product(name=form.name.data,
                             amount=form.amount.data,
                             unit=form.unit.data,
                             public=form.public.data)
        return redirect(url_for('view_product', product_id=product_id))
    return render_template('new_product.j2', form=form)


@app.route('/product/<int:product_id>/', methods=['GET', 'POST'])
def view_product(product_id: int) -> Union[Response, str]:
    try:
        product = db_funcs.get_product(product_id)
    except AttributeError:
        return redirect(url_for('home'))
    form = RecipeForm(product_id=product_id)
    if form.validate_on_submit():
        db_funcs.add_recipe(product_id=product_id,
                            ingredient=form.ingredient.data,
                            amount=form.amount.data,
                            unit_id=form.unit.data)
    recipe = db_funcs.get_recipe(product_id)
    try:
        if product['public'] or product['user_id'] == current_user.user_id:
            return render_template('view_product.j2', product=product, recipes=recipe, form=form)
        return redirect(url_for('home'))
    except AttributeError:
        return redirect(url_for('home'))


@app.route('/products/')
@login_required
def products() -> str:
    products = db_funcs.get_all_products(current_user.user_id)
    username = current_user.username
    return render_template('products.j2', username=username, products=products)


@app.route('/products/<int:product_id>/share/')
@login_required
def share(product_id: int) -> Response:
    db_funcs.share_product(product_id)
    return redirect(url_for('view_product', product_id=product_id))


# Recipe
@app.route('/products/<int:product_id>/delete/<int:ingredient_id>/')
@login_required
def delete_recipe(product_id: int, ingredient_id: int) -> Response:
    db_funcs.delete_recipe(product_id, ingredient_id)
    return redirect(url_for('view_product', product_id=product_id))


@app.route('/products/<int:product_id>/delete/all/')
@login_required
def delete_product(product_id: int) -> Response:
    db_funcs.delete_product(product_id)
    return redirect(url_for('products'))


# User
@app.route('/register/', methods=['GET', 'POST'])
def register() -> Union[Response, str]:
    form = RegisterForm()
    if form.validate_on_submit():
        db_funcs.add_user(username=form.username.data, password=form.password.data,
                          email=form.email.data, fullname=form.fullname.data,
                          birthday=form.birthday.data)
        flash(f'Account created for {form.username.data}.', 'success')
        return redirect(url_for('login'))
    return render_template('register.j2', form=form)


@app.route('/login/', methods=['GET', 'POST'])
def login() -> Union[Response, str]:
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        if db_funcs.validate_password(email, form.password.data):
            login_user(db_funcs.get_user_by_email(email), remember=form.remember.data)
            flash('You have been logged in.', 'success')
            return redirect(url_for('home'))
        flash('Login failed. Please try again.', 'danger')
    return render_template('login.j2', form=form)


@app.route('/logout/')
@login_required
def logout() -> Response:
    logout_user()
    return redirect(url_for('home'))


@app.route('/profile/<int:user_id>')
def profile(user_id: int) -> Union[Response, str]:
    user = db_funcs.get_user(user_id)
    products = db_funcs.get_all_products(user_id, public_only=True)
    if user is None:
        return redirect(url_for('home'))
    return render_template('profile.j2', user=user, products=products)


@app.route('/profile/username/', methods=['GET', 'POST'])
@login_required
def edit_username() -> Union[Response, str]:
    form = UsernameForm()
    if form.validate_on_submit():
        if db_funcs.validate_password(current_user.email, form.password.data):
            db_funcs.change_username(current_user.user_id, form.username.data)
            flash(f'Username changed to {form.username.data}.', 'success')
            return redirect(url_for('profile', user_id=current_user.user_id))
        flash('Wrong password. Please try again.', 'danger')
    return render_template('edit_username.j2', form=form)


@app.route('/profile/email/', methods=['GET', 'POST'])
@login_required
def edit_email() -> Union[Response, str]:
    form = EmailForm()
    if form.validate_on_submit():
        if db_funcs.validate_password(current_user.email, form.password.data):
            db_funcs.change_email(current_user.user_id, form.email.data)
            flash(f'Email changed to {form.email.data}.', 'success')
            return redirect(url_for('profile', user_id=current_user.user_id))
        flash('Wrong password. Please try again.', 'danger')
    return render_template('edit_email.j2', form=form)


@app.route('/profile/password/', methods=['GET', 'POST'])
@login_required
def edit_password() -> Union[Response, str]:
    form = PasswordForm()
    if form.validate_on_submit():
        if db_funcs.validate_password(current_user.email, form.cur_password.data):
            db_funcs.change_password(current_user.user_id, form.new_password.data)
            flash(f'Password changed.', 'success')
            return redirect(url_for('profile', user_id=current_user.user_id))
        flash('Wrong password. Please try again.', 'danger')
    return render_template('edit_password.j2', form=form)


@app.route('/profile/name/', methods=['GET', 'POST'])
@login_required
def edit_name() -> Union[Response, str]:
    form = NameForm()
    if form.validate_on_submit():
        if db_funcs.validate_password(current_user.email, form.password.data):
            db_funcs.change_fullname(current_user.user_id, form.fullname.data)
            flash(f'Name changed to {form.fullname.data}.', 'success')
            return redirect(url_for('profile', user_id=current_user.user_id))
        flash('Wrong password. Please try again.', 'danger')
    return render_template('edit_name.j2', form=form)


@app.route('/profile/birthday/', methods=['GET', 'POST'])
@login_required
def edit_birthday() -> Union[Response, str]:
    form = BirthdayForm()
    if form.validate_on_submit():
        if db_funcs.validate_password(current_user.email, form.password.data):
            db_funcs.change_birthday(current_user.user_id, form.birthday.data)
            birthday = form.birthday.data.strftime('%d/%m/%Y')
            flash(f'Date of birth changed to {birthday}.', 'success')
            return redirect(url_for('profile', user_id=current_user.user_id))
        flash('Wrong password. Please try again.', 'danger')
    return render_template('edit_birthday.j2', form=form)
