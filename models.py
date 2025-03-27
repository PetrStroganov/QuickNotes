import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    username = sqlalchemy.Column(sqlalchemy.String(50), nullable=False, unique=True)
    email = sqlalchemy.Column(sqlalchemy.String(100), nullable=False, unique=True)
    password = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
