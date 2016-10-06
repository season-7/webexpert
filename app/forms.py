from flask_wtf import FlaskForm # , RecaptchaField

from wtforms import StringField, PasswordField # BooleanField

from wtforms.validators import DataRequired, Email, EqualTo,Length


# Define the login form (WTForms)

class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[
        DataRequired(),Length(1,64),Email(), EqualTo('Email',message='Forgot your email address?')])
    password = PasswordField('Password', [
        DataRequired(),Length(1,64),EqualTo('Password',message='Must provide a password. ;-)')])


class RegisterForm(FlaskForm):
    email = StringField('Email Address', validators=[
            DataRequired(), Length(1, 64), Email(), EqualTo('Email', message='Forgot your email address?')])
    password = PasswordField('Password', [
            DataRequired(), Length(1, 64), EqualTo('Password', message='Must provide a password. ;-)')])