from app import db
from datetime import datetime


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
