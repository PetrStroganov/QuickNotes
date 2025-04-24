from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length
from wtforms import BooleanField


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

class NoteForm(FlaskForm):
    title = StringField('Заголовок', validators=[
        DataRequired(message="Введите заголовок"),
        Length(max=100, message="Максимум 100 символов")
    ])
    content = TextAreaField('Содержание', validators=[
        DataRequired(message="Введите текст заметки"),
        Length(max=1000, message="Максимум 1000 символов")
    ])
    tags = StringField('Теги (через запятую)', validators=[
        Length(max=100, message="Максимум 100 символов")
    ])
    is_private = BooleanField('Приватная заметка')
