from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message="Поле обязательно для заполнения"),
        Length(min=4, max=20, message="Логин должен быть от 4 до 20 символов")])
    email = StringField('Email', validators=[
        DataRequired(message="Поле обязательно для заполнения"),
        Email(message="Введите действительный email-адрес")])
    password = PasswordField('Password', validators=[
        DataRequired(message="Поле обязательно для заполнения"),
        Length(min=6, message="Пароль должен быть не менее 6 символов")])


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message="Поле обязательно для заполнения")])
    password = PasswordField('Password', validators=[DataRequired()])
