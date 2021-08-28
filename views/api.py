from flask import jsonify

from app import app
from models import Birthday
from services.telegram import TBot
from utils.utils import get_date_integer


@app.route('/api/v1.0/get_birthdays', methods=['GET'])
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
