from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user
from flask_login.utils import login_required
# from sqlalchemy.sql.functions import current_user

import product_cost_calculator.db_funcs as db_funcs
from product_cost_calculator import app
from product_cost_calculator.forms import LoginForm, ProductForm, RecipeForm, RegisterForm


@app.route('/')
def home():
    return render_template('base.j2')


@app.route('/register', methods=['GET', 'POST'])
def register() -> str:
    form = RegisterForm()
    if form.validate_on_submit():
        db_funcs.add_user(username=form.username.data, password=form.password.data,
                          email=form.email.data, fullname=form.fullname.data,
                          birthday=form.birthday.data)
        flash(f'Account created for {form.username.data}.', 'success')
        return redirect(url_for('login'))
    return render_template('register.j2', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login() -> str:
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        if db_funcs.validate_password(email, form.password.data):
            login_user(db_funcs.get_user(email), remember=form.remember.data)
            flash('You have been logged in.', 'success')
            return redirect(url_for('home'))
        flash('Login failed. Please try again.', 'danger')
    return render_template('login.j2', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/product/add', methods=['GET', 'POST'])
@login_required
def add_product() -> str:
    form = ProductForm()
    if form.validate_on_submit():
        product_id = db_funcs.add_product(name=form.name.data,
                             amount=form.amount.data,
                             unit=form.unit.data,
                             public=form.public.data)
        return redirect(url_for('view_product', product_id=product_id))
    return render_template('new_product.j2', form=form)


@app.route('/product/<int:product_id>', methods=['GET', 'POST'])
def view_product(product_id: int) -> str:
    product = db_funcs.get_product(product_id)
    form = RecipeForm()
    if form.validate_on_submit():
        db_funcs.add_recipe(product_id=product_id,
                            ingredient=form.ingredient.data,
                            amount=form.amount.data,
                            unit=form.unit.data)
    recipe = db_funcs.get_recipe(product_id)
    return render_template('view_product.j2', product=product, recipes=recipe, form=form)


@app.route('/profile')
@login_required
def profile() -> str:
    products = db_funcs.get_all_products()
    username = current_user.username
    return render_template('profile.j2', username=username, products=products)


@app.route('/product/<int:product_id>/delete/<int:ingredient_id>')
@login_required
def delete_recipe(product_id: int, ingredient_id: int) -> str:
    db_funcs.delete_recipe(product_id, ingredient_id)
    return redirect(url_for('view_product', product_id=product_id))