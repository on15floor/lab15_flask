from datetime import datetime

from flask import render_template, request

from app import app
from models import NoSmoking


def build_collection(time_start: str, time_stop: str, price_start: int, price_stop: int) -> dict:
    """Собираем статистику в коллекцию для передачи в шаблон"""
    time_start = datetime.strptime(time_start, '%Y-%m-%d')
    time_stop = datetime.strptime(time_stop, '%Y-%m-%d')
    time_now = datetime.now()

    days_smoking = time_stop - time_start
    days_no_smoking = time_now - time_stop
    price_avg = (price_start + price_stop) / 2
    money_spent = days_smoking.days * price_avg
    money_saved = days_no_smoking.days * price_stop

    return {
        'time_start': time_start.strftime('%Y-%m-%d'),
        'time_stop': time_stop.strftime('%Y-%m-%d'),
        'time_now': time_now.strftime('%Y-%m-%d'),
        'days_smoking': days_smoking.days,
        'days_no_smoking': days_no_smoking.days,
        'price_start': price_start,
        'price_stop': price_stop,
        'price_avg': price_avg,
        'money_spent': money_spent,
        'money_saved': money_saved,
    }


@app.route('/no_smoking', methods=['POST', 'GET'])
def no_smoking():
    """ Страница. Для тех кто бросил курить """
    data_out = {}
    no_smoking_db = NoSmoking.query.order_by(NoSmoking.id)

    if request.method == 'GET':
        data_out = build_collection('2008-02-01', '2021-08-30', 50, 150)

    if request.method == 'POST':
        time_start = request.form['in_start_day']
        time_stop = request.form['in_stop_day']
        price_start = int(request.form['in_price_start'])
        price_stop = int(request.form['in_price_stop'])
        data_out = build_collection(time_start, time_stop, price_start, price_stop)

    return render_template('no_smoking.html', data_out=data_out, no_smoking_db=no_smoking_db)
