from flask_wtf import FlaskForm
from wtforms import StringField,  PasswordField, BooleanField, EmailField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField("username" , validators=[DataRequired()])
    password =  PasswordField("password", validators=[DataRequired()])
    remember_me = BooleanField("remember_me")

class UserForm(FlaskForm):
    name = StringField("name" , validators=[DataRequired(), Length(min=3, max=100)])
    username = StringField("username" , validators=[DataRequired(), Length(min=3, max=100)])
    password =  PasswordField("password", validators=[DataRequired(), Length(min=5, max=100)])
    email =  EmailField("email", validators=[DataRequired(), Length(min=3, max=100)])

class UserFormUpdate(FlaskForm):
    name = StringField("name" , validators=[DataRequired(), Length(min=3, max=100)])
    username = StringField("username" , validators=[DataRequired(), Length(min=3, max=100)])
    email =  EmailField("email", validators=[DataRequired(), Length(min=3, max=100)])