from flask import render_template, Markup
from app import app
from config import BASE_DIR
import markdown
import os


# Конвертирует файл Markdown
def get_markdown(file_name):
    data_file = os.path.join(BASE_DIR, f'static/docs/{file_name}')
    with open(data_file) as f:
        return markdown.markdown(f.read())


# Docs Pages
@app.route('/docs/<string:f>')
def docs_git(f):
    """ Страница. Docs """
    params = ['git', 'markdown', 'python', 'sql', 'bash']
    if f in params:
        return render_template('/docs.html', doc=Markup(get_markdown(f'{f}.md')))
    else:
        return render_template('404.html')
