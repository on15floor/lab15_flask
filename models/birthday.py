from app import db


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
