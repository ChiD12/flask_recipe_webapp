from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo
from Cooking.models import User

class RecipeForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(min=2, max=120)])
    image= StringField('image')
    ingredients = StringField('ingredients', validators=[DataRequired(),Length(min=2,max = 300)])
    steps = StringField('steps', validators=[DataRequired(),Length(min=2, max = 300)])
    submit = SubmitField('Enter Recipe')


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RequestPasswordResetForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email')

class ResetForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Comfirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')