from datetime import datetime

from flask import render_template, request

from app import app
from models import NoSmoking


@app.route('/no_smoking', methods=['POST', 'GET'])
def no_smoking():
    """ Страница. Для тех кто бросил курить """
    # Постоянные
    time_start = '2008-02-01'
    time_stop = '2021-08-30'
    price_start = 50
    price_stop = 150

    # Время
    time_start = datetime.strptime(time_start, '%Y-%m-%d')
    time_stop = datetime.strptime(time_stop, '%Y-%m-%d')
    time_now = datetime.now()

    # Расчеты статистики
    days_smoking = time_stop - time_start
    days_no_smoking = time_now - time_stop
    price_avg = (price_start + price_stop) / 2
    money_spent = days_smoking.days * price_avg
    money_saved = days_no_smoking.days * price_stop

    data_out = {
        'time_start': time_start.strftime('%Y-%m-%d'),
        'time_stop': time_stop.strftime('%Y-%m-%d'),
        'time_now': time_now.strftime('%Y-%m-%d'),
        'days_smoking': days_smoking.days,
        'days_no_smoking': days_no_smoking.days,
        'price_avg': price_avg,
        'money_spent': money_spent,
        'money_saved': money_saved,
    }

    # БД
    no_smoking_db = NoSmoking.query.order_by(NoSmoking.id)

    return render_template('no_smoking.html', data_out=data_out, no_smoking_db=no_smoking_db)
