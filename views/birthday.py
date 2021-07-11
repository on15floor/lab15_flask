from app import app, db
from flask import render_template, request, redirect
from flask_security import login_required
from models import Birthday
from services.utils import get_now


def get_date():
    date_full = get_now()
    date_d = date_full.day
    date_m = date_full.month
    date_y = date_full.year
    return date_d, date_m, date_y


@app.route('/birthdays')
@login_required
def birthdays():
    """ Страница. Дни рождения """
    q = request.args.get('q')
    if q:
        birthdays_db = Birthday.query.filter(Birthday.name.contains(q) |
                                             Birthday.comment.contains(q)).order_by(Birthday.birth_month)
    else:
        birthdays_db = Birthday.query.order_by(Birthday.birth_month)
    return render_template('birthdays/birthdays.html', birthdays=birthdays_db, today=get_date())


@app.route('/birthdays/add', methods=['POST', 'GET'])
@login_required
def birthday_add():
    """ Страница. Дни рождения - Создание """
    if request.method == 'POST':
        name = request.form['name']
        male = True if request.form.getlist('male') else False
        birthday_list = request.form['birthday'].split('.')
        b_d = int(birthday_list[0])
        b_m = int(birthday_list[1])
        b_y = int(birthday_list[2])
        birthday_checked = True if request.form.getlist('birthday_checked') else False
        comment = request.form['comment']

        # Добавляем в БД
        birthday = Birthday(name=name, male=male, birth_day=b_d, birth_month=b_m, birth_year=b_y,
                            birthday_checked=birthday_checked, comment=comment)
        try:
            db.session.add(birthday)
            db.session.commit()
            return redirect('/birthdays')
        except:
            return "When birthday adding rise exception"
    else:
        return render_template('birthdays/birthday_create.html')


@app.route('/birthdays/<int:birthday_id>/update', methods=['POST', 'GET'])
@login_required
def birthday_update(birthday_id):
    """ Страница. Дни рождения - Редактирование """
    birthday = Birthday.query.get(birthday_id)

    if request.method == 'POST':
        birthday.name = request.form['name']
        birthday.male = True if request.form.getlist('male') else False
        birthday_list = request.form['birthday'].split('.')
        birthday.birth_day = int(birthday_list[0])
        birthday.birth_month = int(birthday_list[1])
        birthday.birth_year = int(birthday_list[2])
        birthday.birthday_checked = True if request.form.getlist('birthday_checked') else False
        birthday.comment = request.form['comment']

        # Обновляем БД
        try:
            db.session.commit()
            return redirect('/birthdays')
        except:
            return "When birthday updating rise exception"
    else:
        return render_template('birthdays/birthday_update.html', birthday=birthday)
