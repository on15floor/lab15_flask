from app import db
from datetime import datetime


class Beget(db.Model):
    """ Модель базы данных новостей beget.ru """
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    text = db.Column(db.Text, nullable=False)
