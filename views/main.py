from flask import render_template, request
from models import NoSmoking

from app import app


@app.route('/')
def index():
    """ Страница. Главная """
    return render_template('index.html')


@app.route('/ping')
def ping():
    """ Страница. Ping (возвращает IP) """
    ip_address = request.remote_addr
    return "Requester IP: " + ip_address


@app.errorhandler(404)
def page_not_fount():
    """ Страница. 404 """
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(exception):
    """ Страница. 500 """
    app.logger.error(exception)
    return render_template('500.html'), 500


@app.route('/no_smoking/<string:stop_time>')
def no_smoking(stop_time):
    """ Страница. Для тех кто бросил курить """
    no_smoking_db = NoSmoking.query.order_by(NoSmoking.id)
    return render_template('no_smoking.html', no_smoking_db=no_smoking_db, stop_time=stop_time)
