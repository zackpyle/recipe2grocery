from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from recipe2grocery.models import User
import re


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
            DataRequired(),
            Length(min=5, max=20)
            ]
    )
    email = StringField('Email', validators=[
            DataRequired(),
            Email()
            ]
    )
    password = PasswordField('Password', validators=[
            DataRequired(),
            Length(min=8, max=25)
            ]
    )
    confirm_password = PasswordField('Confirm Password', validators=[
            DataRequired(),
            EqualTo('password')
            ]
    )
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already taken. Please choose different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
            DataRequired(),
            Email()
            ]
    )
    password = PasswordField('Password', validators=[
            DataRequired()
            ]
    )
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class RecipeInputForm(FlaskForm):
    recipe_url_input = StringField('Recipe URL', validators=[
            DataRequired()
            ],
            render_kw={"placeholder": "Recipe URL"}
    )
    submit = SubmitField('Add Recipe')

    def validate_recipe_url_input(self, recipe_url_input):
        if re.search(r'https?\:\/\/(www\.)?(allrecipes|foodnetwork)\.com\/.*', str(recipe_url_input)) is None:
            raise ValidationError("Oops. We don't currently support this recipe platform... Please try again with a different website.")


class UpdateProfileForm(FlaskForm):
    username = StringField('Username', validators=[
            DataRequired(),
            Length(min=5, max=20)
            ]
        )
    email = StringField('Email', validators=[
            DataRequired(),
            Email()
            ]
        )
    picture = FileField('Update Profile Picture',
                        validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    submit = SubmitField('Update Profile')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is already taken. Please choose different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is already taken. Please choose different one.')
