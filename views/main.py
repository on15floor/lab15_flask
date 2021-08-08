from flask import render_template, request

from app import app


@app.route('/')
def index():
    """ Страница. Главная """
    return render_template('index.html')


@app.route('/ping')
def ping():
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
