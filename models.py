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

class Note(db.Model):
    __tablename__ = 'notes'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    content = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    tags = sqlalchemy.Column(sqlalchemy.String(100))
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=sqlalchemy.func.now())
    user = sqlalchemy.orm.relationship('User', backref='notes')