from app import app, db
from flask import render_template, request, redirect
from flask_security import login_required
from models import Post
from tinkoff import build_collection


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


@app.route('/create_post', methods=['POST', 'GET'])
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
def stocks():
    """ Страница. Ценные бумаги """
    stats_br, stocks_br = build_collection('2001148671')
    stats_iis, stocks_iis = build_collection('2004836843')
    return render_template('stocks.html', stats_br=stats_br, stocks_br=stocks_br,
                           stats_iis=stats_iis, stocks_iis=stocks_iis)