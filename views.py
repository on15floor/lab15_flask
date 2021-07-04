from app import app, db
from flask import render_template, request, redirect
from flask_security import login_required
from models import Post, Birthday
from stocks import build_collection
from crypto import build_collection_crypto
from config import Vars
from datetime import datetime


@app.route('/')
@app.route('/home')
def index():
    """ Страница. Главная """
    return render_template('index.html')


@app.errorhandler(404)
def page_not_fount(e):
    """ Страница. 404 """
    return render_template('404.html'), 404


@app.route('/blog')
def blog():
    """ Страница. Блог """
    q = request.args.get('q')
    if q:
        posts = Post.query.filter(Post.title.contains(q) |
                                  Post.intro.contains(q) |
                                  Post.text.contains(q)).order_by(Post.date.desc())
    else:
        posts = Post.query.order_by(Post.date.desc())

    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    pages = posts.paginate(page=page, per_page=10)

    return render_template('blog/blog.html', posts=posts, pages=pages)


@app.route('/blog/<int:post_id>')
def blog_post(post_id):
    """ Страница. Пост """
    post = Post.query.get(post_id)
    return render_template('blog/post.html', post=post)


@app.route('/blog/<int:pos_id>/del')
@login_required
def blog_post_del(pos_id):
    """ Страница. Пост - Удаление """
    post = Post.query.get_or_404(pos_id)
    try:
        db.session.delete(post)
        db.session.commit()
        return redirect('/blog')
    except:
        return "When post deleting rise exception"


@app.route('/blog/create_post', methods=['POST', 'GET'])
@login_required
def blog_post_create():
    """ Страница. Пост - Создание """
    if request.method == 'POST':
        title = request.form['title']
        icon = request.form['icon']
        intro = request.form['intro']
        text = request.form['text']

        post = Post(icon=icon, title=title, intro=intro, text=text)
        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/blog')
        except:
            return "When post adding rise exception"
    else:
        return render_template('blog/post_create.html')


@app.route('/blog/<int:post_id>/update', methods=['POST', 'GET'])
@login_required
def blog_post_update(post_id):
    """ Страница. Пост - Релдактирование """
    post = Post.query.get(post_id)

    if request.method == 'POST':
        post.title = request.form['title']
        post.icon = request.form['icon']
        post.intro = request.form['intro']
        post.text = request.form['text']

        try:
            db.session.commit()
            return redirect(f'/blog/{post_id}')
        except:
            return "When post updating rise exception"
    else:
        return render_template('blog/post_update.html', post=post)


# Unity Pages
@app.route('/unity/simple_cube')
def unity_simple_cube():
    """ Страница. Unity - Simple Cube """
    return render_template('/unity/simple_cube.html')


@app.route('/unity/delimiter')
def unity_delimiter():
    """ Страница. Unity - Delimiter """
    return render_template('/unity/delimiter.html')


@app.route('/unity/kot_guide')
def unity_kot_guide():
    """ Страница. Unity - KoT Guide """
    return render_template('/unity/kot_guide.html')


@app.route('/unity/privacy_policy/<string:game>')
def unity_privacy_policy(game):
    """ Страница. Unity - Политика приватности """
    if game == 'simple_cube':
        return render_template('/unity/privacy_policy.html', game='Simple Cube')
    elif game == 'delimiter':
        return render_template('/unity/privacy_policy.html', game='Delimiter')
    elif game == 'kot_guide':
        return render_template('/unity/privacy_policy.html', game='KoT Guide')
    else:
        return render_template('404.html')


@app.route('/stocks')
@login_required
def stocks():
    """ Страница. Ценные бумаги """
    stats_br, stocks_br, operations_usd_br, operations_usd_profit_br = build_collection('2001148671')
    stats_iis, stocks_iis, operations_usd_iis, operations_usd_profit_iis = build_collection('2004836843')
    operations_usd = operations_usd_br + operations_usd_iis
    operations_usd.sort(key=lambda k: k["date"])
    operations_usd_profit = round(operations_usd_profit_br + operations_usd_profit_iis, 2)
    return render_template('stocks.html', stats_br=stats_br, stocks_br=stocks_br,
                           stats_iis=stats_iis, stocks_iis=stocks_iis,
                           operations_usd_iis=operations_usd_iis, operations_usd=operations_usd,
                           operations_usd_profit=operations_usd_profit, tax_plus=int(Vars.TINKOFF_TAX_PLUS))


@app.route('/crypto')
@login_required
def crypto():
    """ Страница. Криптовалюта """
    wallet, balance_wallet, deposits, balance_deposits = build_collection_crypto()
    return render_template('crypto.html', wallet=wallet, balance_wallet=balance_wallet,
                           deposits=deposits, balance_deposits=balance_deposits)


@app.route('/birthdays')
@login_required
def birthdays():
    """ Страница. Дни рождения """
    q = request.args.get('q')
    if q:
        birthdays_db = Birthday.query.filter(Birthday.name.contains(q) |
                                             Birthday.comment.contains(q)).order_by(Birthday.birthday.desc())
    else:
        birthdays_db = Birthday.query.order_by(Birthday.birthday.desc())
    return render_template('birthdays/birthdays.html', birthdays=birthdays_db)


@app.route('/birthdays/add', methods=['POST', 'GET'])
@login_required
def birthday_add():
    """ Страница. Дни рождения - Создание """
    if request.method == 'POST':
        name = request.form['name']
        if request.form.getlist('male'):
            male = True
        else:
            male = False
        birthday = datetime.date(datetime.strptime(request.form['birthday'], '%d.%m.%Y'))
        if request.form.getlist('birthday_checked'):
            birthday_checked = True
        else:
            birthday_checked = False
        comment = request.form['comment']

        birthday = Birthday(name=name, male=male, birthday=birthday, birthday_checked=birthday_checked, comment=comment)
        try:
            db.session.add(birthday)
            db.session.commit()
            return redirect('/birthdays')
        except:
            return "When birthday adding rise exception"
    else:
        return render_template('birthdays/birthday_add.html')
