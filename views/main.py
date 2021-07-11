from flask import render_template, request
from app import app


@app.route('/')
@app.route('/home')
def index():
    """ Страница. Главная """
    return render_template('index.html')


@app.errorhandler(404)
def page_not_fount():
    """ Страница. 404 """
    return render_template('404.html'), 404


@app.route('/ping')
def ping():
    ip_address = request.remote_addr
    return "Requester IP: " + ip_address
