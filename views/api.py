import requests
from bs4 import BeautifulSoup
from flask import jsonify

from app import app, db
from models import Birthday, Beget
from services.telegram import TBot
from utils.decorators import token_required
from utils.utils import get_date_integer


@app.route('/api/v1.0/get_birthdays', methods=['GET'])
@token_required
def birthday():
    """ Отправка информации о сегодняшних именниках """
    date_today = get_date_integer()
    t = TBot()
    birthday_people = ''

    birthdays_db = Birthday.query.filter(Birthday.birth_month.contains(date_today[1])).all()
    for b in birthdays_db:
        if date_today[0] == b.birth_day:
            male = '🚹' if b.male == 1 else '🚺'
            birthday_checked = '✅' if b.birthday_checked == 1 else '❌'
            # Определяем возраст
            if b.birth_month >= date_today[1]:
                if b.birth_day > date_today[0]:
                    age = date_today[2] - b.birth_year - 1
                else:
                    age = date_today[2] - b.birth_year
            else:
                age = date_today[2] - b.birth_year - 1
            birthday_people += f'{male}{birthday_checked}{b.name} [{age} лет]\n'
    if birthday_people:
        t.send_message(message=f'Сегодня свои дни рождения празднуют:\n {birthday_people}')

    return jsonify({'status': 'success'})


@app.route('/api/v1.0/get_beget_news', methods=['GET'])
@token_required
def get_beget_news():
    """ Проверка новостей beget.ru и отправка новых """

    def beget_news_pars() -> list:
        response = requests.get("https://beget.com/ru/news/2021/beget-12-years")
        soup = BeautifulSoup(response.text, 'html.parser')
        beget_news = soup.find_all("ul", {"class": "nav nav-category-tree flex-nowrap my-0"})
        res = []
        for n in beget_news[0].contents:
            res.append(n.text.strip())
        return res

    news_in = beget_news_pars()
    news_db_data = Beget.query.order_by(Beget.id).all()
    news_db_text = []
    for n in news_db_data:
        news_db_text.append(n.text)

    # Проверяем наличие новый новостей
    for n in news_in:
        if n not in news_db_text:
            news = Beget(text=n)
            try:
                db.session.add(news)
                db.session.commit()
            except:
                return "When news adding rise exception"
            finally:
                t = TBot()
                t.send_message(message=f'ℹ️Beget news:\n {n}')

    return jsonify({'status': 'success'})


@app.route('/api/v1.0/test_token', methods=['GET'])
@token_required
def get_test():
    return jsonify({'status': 'success'})
