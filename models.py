from app import db
from datetime import datetime
from flask_security import UserMixin, RoleMixin


roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer, db.ForeignKey('role.id')))


class Post(db.Model):
    """ Модель базы данных постов в блоге """
    id = db.Column(db.Integer, primary_key=True)
    icon = db.Column(db.Text, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Article {self.id}'


class User(db.Model, UserMixin):
    """ Модель базы данных пользователя """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users'), lazy='dynamic')


class Role(db.Model, RoleMixin):
    """ Модель базы данных ролей пользователей """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)


class Birthday(db.Model):
    """ Модель базы данных дней рождений """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    male = db.Column(db.Boolean, default=True)
    birth_day = db.Column(db.Integer)
    birth_month = db.Column(db.Integer)
    birth_year = db.Column(db.Integer)
    birthday_checked = db.Column(db.Boolean, default=False)
    comment = db.Column(db.Text)
