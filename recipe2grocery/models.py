from recipe2grocery import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile_picture = db.Column(db.String(20), nullable=False, default='default_profile.png')
    password = db.Column(db.String(60), nullable=False)
    recipe = db.relationship('Recipes', backref='user', lazy=True)
    shopping_list = db.relationship('Shopping_List', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.profile_picture}')"

class Recipes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #recipe_name = db.Column(db.String(70))
    recipe_url = db.Column(db.String(120))
    #recipe_image = db.Column(db.String(20), default='default_recipe.jpg')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #ingredientslist_item = db.relationship('Ingredients_List', backref='recipes', lazy=True)
    #shoppinglist_item = db.relationship('Shopping_List', backref='recipes', lazy=True)

    def __repr__(self):
        return f"{self.recipe_url}"


class Ingredients_List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ingredient_item = db.Column(db.String(70), nullable=False)
    #recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)

    def __repr__(self):
        return f"Ingredients_List('{self.ingredient_item}')"

class Shopping_List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shoppinglist_item = db.Column(db.String(70), nullable=False)
    #recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Shopping_List('{self.shoppinglist_item}')"

#class Weekly_Planner(db.Model):
