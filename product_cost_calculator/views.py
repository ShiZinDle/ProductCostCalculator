from flask import flash, redirect, render_template, url_for
from flask_login import login_user, logout_user

import product_cost_calculator.db_funcs as db_funcs
from product_cost_calculator import app
from product_cost_calculator.forms import LoginForm, RegisterForm


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
            return redirect(url_for('register'))
        flash('Login failed. Please try again.', 'danger')
    return render_template('login.j2', form=form)


@app.route('/logout')
def logout():
    logout_user()


@app.route('/product/<int:product_id>')
def get_product(product_id: int) -> str:
    name = db_funcs.get_product_name(product_id)
    recipe = db_funcs.get_recipe(product_id)
    return render_template('product.j2', name=name, recipe=recipe)
