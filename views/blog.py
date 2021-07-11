from flask import render_template, request, redirect
from flask_security import login_required
from app import app, db
from models import Post


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
