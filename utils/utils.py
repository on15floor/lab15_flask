import re
from datetime import datetime

from pytz import timezone

from config import Vars


def localize(d: datetime) -> datetime:
    return timezone(Vars.TIME_ZONE).localize(d)


def get_now() -> datetime:
    return localize(datetime.now())


def get_date_integer():
    """Функция возвращает сегодняшнюю дату в виде трех переменных типа int: день, месяц, год"""
    date_full = get_now()
    date_d = date_full.day
    date_m = date_full.month
    date_y = date_full.year
    return date_d, date_m, date_y


def removing_extra_spaces(s: str) -> str:
    """Функция удаляет лишние пробелы (в начале, в конце строки и дубли)"""
    return re.sub(" +", " ", s).strip()
