import os
import secrets
import requests
import unicodedata
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, jsonify
from recipe2grocery import app, db, bcrypt
from recipe2grocery.forms import RegistrationForm, LoginForm, RecipeInputForm, UpdateProfileForm
from recipe2grocery.models import User, Recipes, Shopping_List
from flask_login import login_user, current_user, logout_user, login_required
from lxml import html


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home_page():
    form = RecipeInputForm()
    if form.validate_on_submit():
        recipe_input = Recipes(recipe_url=form.recipe_url_input.data, user=current_user)
        db.session.add(recipe_input)
        db.session.commit()
        return redirect(url_for('add_recipe_page'))
    return render_template('home.html', form=form)


@app.route('/shopping-list')
@login_required
def shopping_list_page():
    return render_template('shopping-list.html', title="Shopping List")


@app.route('/recipes')
@login_required
def recipes_page():
    recipe_history = Recipes.query.order_by('-id').all()
    return render_template('recipes.html', title="My Recipes", recipe_history=recipe_history)


@app.route('/recipes/add-recipe')
@login_required
def add_recipe_page():
    new_recipe = Recipes.query.order_by('-id').first()
    response = requests.get(new_recipe)
    recipe = html.fromstring(response.content)
    # All Recipes
    if 'allrecipe' in str(new_recipe):
        ingredient = recipe.xpath('//span[@itemprop="recipeIngredient"]/text()')
        print('Ingredients: ', ingredient)
    # Food Network
    elif 'foodnetwork' in str(new_recipe):
        ingredient = recipe.xpath('//p[@class="o-Ingredients__a-Ingredient"]/text()')
        ingredient_foodnetwork = ([s.replace('\xa0', '') for s in ingredient])
        ingredient = ingredient_foodnetwork
        print('Ingredients: ', ingredient)
    else:
        ### Need to move this to validate_on_submit on homepage
        print("Oops: We don't currently support this recipe platform. You can manually add the ingredients here.")
    return render_template('add-recipe.html', title="Add Recipe", new_recipe=new_recipe, ingredient=ingredient)


@app.route('/weekly-planner')
@login_required
def weekly_planner_page():
    return render_template('weekly-planner.html', title="Weekly Planner")


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (250, 250)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile_page():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.profile_picture = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('profile_page'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    profile_picture = url_for('static', filename='profile_pics/' + current_user.profile_picture)
    return render_template('profile.html',
                           title="Profile",
                           profile_picture=profile_picture,
                           form=form
                           )


@app.route('/about')
def about_page():
    return render_template('about.html', title="About")


@app.route('/contact')
def contact_page():
    return render_template('contact.html', title="Contact")


@app.route('/help')
def help_page():
    return render_template('help.html', title="Help")


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data.lower(), password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login_page'))
    return render_template('register.html', title="Register", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
            return redirect(url_for('home_page'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home_page'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title="Login", form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    return redirect(url_for('home_page'))
