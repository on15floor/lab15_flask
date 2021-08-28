from flask import render_template, request, redirect
from flask_security import login_required

from app import app, db
from models import Birthday
from utils.utils import get_date_integer


@app.route('/birthdays/<string:f>')
@login_required
def birthdays(f):
    """ Страница. Дни рождения """
    q = request.args.get('q')
    date_today = get_date_integer()
    if q:
        birthdays_db = Birthday.query.filter(Birthday.name.contains(q) |
                                             Birthday.comment.contains(q)).order_by(Birthday.birth_month)
    else:
        if f == 'all':
            birthdays_db = Birthday.query.order_by(Birthday.birth_month)
        elif f == 'today':
            birthdays_db = Birthday.query.filter(Birthday.birth_month.contains(date_today[1]))
        elif f == 'w':
            birthdays_db = Birthday.query.filter(Birthday.male.contains(0))
        elif f == 'm':
            birthdays_db = Birthday.query.filter(Birthday.male.contains(1))
        else:
            return render_template('404.html')

    return render_template('birthdays/birthdays.html', birthdays=birthdays_db, today=date_today)


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
            return redirect('/birthdays/all')
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
            return redirect('/birthdays/all')
        except:
            return "When birthday updating rise exception"
    else:
        return render_template('birthdays/birthday_update.html', birthday=birthday)


@app.route('/birthdays/<int:birthday_id>/del')
@login_required
def birthday_del(birthday_id):
    """ Страница. День рождения - Удаление """
    birthday = Birthday.query.get(birthday_id)
    try:
        db.session.delete(birthday)
        db.session.commit()
        return redirect('/birthdays/all')
    except:
        return "When birthday deleting rise exception"
