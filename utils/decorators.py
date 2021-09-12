from functools import wraps

from flask import request, jsonify

from config import Tokens


def token_required(f):
    """ Используй этот декоратор, если запрос необходимо сделать с проверкой токена """
    @wraps(f)
    def decorator(*args, **kwargs):
        if not request.args.get("token") == Tokens.FLASK_API_TOKEN:
            return jsonify({'status': 'error'})
        return f(*args, **kwargs)
    return decorator
