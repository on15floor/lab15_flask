from app import db


class NoSmoking(db.Model):
    """ Модель стадий бросания курения """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    time = db.Column(db.Float, nullable=False)
    time_descr = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
