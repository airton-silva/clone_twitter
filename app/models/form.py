from flask_wtf import FlaskForm
from wtforms import StringField,  PasswordField, BooleanField, EmailField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField("username" , validators=[DataRequired()])
    password =  PasswordField("password", validators=[DataRequired()])
    remember_me = BooleanField("remember_me")

class UserForm(FlaskForm):
    name = StringField("name" , validators=[DataRequired()])
    username = StringField("username" , validators=[DataRequired()])
    password =  PasswordField("password", validators=[DataRequired()])
    email =  EmailField("email", validators=[DataRequired()])