from app import app
from datetime import datetime


@app.template_filter('zfill')
def zfill(value, width):
    """ Zfill фильтр """
    return str(value).zfill(width)


@app.template_filter('percent_left')
def percent_left(date_start: str, total_days):
    """ Фильтр получает время начала события и его продолжительность.
    Рассчитывает на сегодняшний день процент выполнения """
    date_start = datetime.strptime(date_start, '%Y-%m-%d')
    date_now = datetime.now()
    date_delta = date_now-date_start
    print(date_delta.days)
    res = date_delta.days/float(total_days)*100
    return round(res, 2) if res <= 100 else 100
