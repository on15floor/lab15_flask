from flask import render_template
from app import app


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
    games = {'simple_cube': 'Simple Cube',
             'delimiter': 'Delimiter',
             'kot_guide': 'KoT Guide'}
    if game in games.keys():
        return render_template('/unity/privacy_policy.html', game=games[game])
    else:
        return render_template('404.html')
